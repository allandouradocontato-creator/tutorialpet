"""Agente 31 - Aprimorador de Landing.
Le data/landing/metricas.csv (cria vazio se nao existir), calcula conversao por landing e grava
data/landing/proposta_<slug>.md com UMA mudanca testavel (hipotese, como testar de graca, criterio de decisao).
Sem dados: diz 'sem dados ainda' e sugere como medir. Regras completas em prompt.md.
Uso: python agents/31_aprimorador_landing/agent.py [slug]
"""
import os, sys, csv, glob, datetime
import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CSV = os.path.join(RAIZ, "data", "landing", "metricas.csv")
COLS = ["data", "slug", "visitas", "cliques_checkout", "vendas"]
MIN_VISITAS = 100
META_CLIQUE, META_COMPRA, META_CONV = 0.03, 0.05, 0.015

def garantir_csv():
    os.makedirs(os.path.dirname(CSV), exist_ok=True)
    if not os.path.exists(CSV):
        with open(CSV, "w", newline="", encoding="utf-8") as f: csv.writer(f).writerow(COLS)

def ler():
    agg = {}
    with open(CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                a = agg.setdefault(r["slug"].strip(), {"visitas": 0, "cliques": 0, "vendas": 0, "dias": set()})
                a["visitas"] += int(r["visitas"] or 0); a["cliques"] += int(r["cliques_checkout"] or 0)
                a["vendas"] += int(r["vendas"] or 0); a["dias"].add(r["data"])
            except (ValueError, KeyError, AttributeError):
                continue
    return agg

def div(a, b): return a / b if b else 0.0

COMO_MEDIR = (
    "- Visitas: Microsoft Clarity (grátis, já na landing) mostra sessões por dia; Vercel Analytics (plano grátis) também.\n"
    "- Cliques no checkout: Clarity > Eventos/Smart events no botão `data-origem` (topo, meio, oferta, barra), ou contar sessões que chegam ao checkout pelo `utm_content`.\n"
    "- Vendas: painel da Kiwify, filtrando por `utm_campaign` do produto.\n"
    "- Preencher uma linha por dia em data/landing/metricas.csv (data,slug,visitas,cliques_checkout,vendas) e rodar este agente de novo."
)

def escolher(v, c, b, conv):
    if v < MIN_VISITAS:
        return None
    if c < META_CLIQUE:
        return ("TÍTULO (promessa do topo)", "titulo",
                f"A taxa de clique ({c:.1%}) está abaixo de {META_CLIQUE:.0%}: o visitante não vê motivo para ir ao checkout. Um título que nomeia a dor concreta (ex.: o vizinho que reclama, o latido quando você sai) deve atrair mais cliques do que a promessa genérica.",
                "Trocar `promessa` e `subpromessa` na variante B; manter todo o resto igual.")
    if b < META_COMPRA:
        return ("OFERTA (preço de/por, garantia e bônus em destaque)", "oferta",
                f"Os cliques são bons ({c:.1%}), mas só {b:.1%} dos cliques compram: a decisão trava na oferta. Mostrar o preço 'de' riscado e a garantia logo no bloco da oferta reduz o risco percebido.",
                "Na variante B preencher `oferta.preco_de` e destacar a garantia nos `itens` da oferta; não mudar título nem ordem.")
    if conv < META_CONV:
        return ("PROVA SOCIAL (depoimentos reais)", "prova_social",
                f"Cliques e compra no checkout estão ok, mas a conversão total ({conv:.1%}) está abaixo de {META_CONV:.1%}. Falta confiança antes do clique; depoimentos reais reduzem a dúvida.",
                "Na variante B preencher `prova_social` SOMENTE com depoimentos reais e autorizados de compradores (nunca inventar); se não houver, testar a ORDEM das seções (oferta logo após os benefícios).")
    return ("TÍTULO (ganho incremental)", "titulo",
            f"Todas as taxas estão acima da meta (clique {c:.1%}, compra {b:.1%}, conversão {conv:.1%}). O próximo ganho vem de afinar a promessa do topo.",
            "Variante B com outra formulação da `promessa`, sem alterar o resto.")

def proposta(slug, a):
    v, k, s = a["visitas"], a["cliques"], a["vendas"]
    c, b, conv = div(k, v), div(s, k), div(s, v)
    esc = escolher(v, c, b, conv)
    hoje = datetime.date.today().isoformat()
    cab = (f"# Proposta de melhoria da landing: {slug} ({hoje})\n\n"
           f"Dados ({len(a['dias'])} dia(s)): visitas {v}, cliques no checkout {k}, vendas {s}.\n"
           f"Taxa de clique {c:.1%} · taxa de compra no checkout {b:.1%} · conversão total {conv:.2%}.\n\n")
    if not esc:
        return cab + (f"## Dados insuficientes\nMenos de {MIN_VISITAS} visitas na janela: nenhuma mudança agora (mudar com amostra pequena é chute).\n"
                      "Ação: gerar tráfego (post, anúncio autorizado) e voltar a rodar.\n\n## Como medir\n" + COMO_MEDIR + "\n")
    nome, chave, hip, como = esc
    return cab + (f"## Uma mudança desta rodada: {nome}\n\n### Hipótese\n{hip}\n\n### O que muda\n{como}\n\n"
                  "### Como testar de graça (variante B por UTM)\n"
                  f"1. Editar `config/produtos_landing/{slug}.yaml`, bloco `variantes: B:` com só o campo da alavanca (`{chave}`).\n"
                  "2. Rodar `python agents/30_fabrica_landing/agent.py " + slug + "`: gera `saida/" + slug + "/b/index.html` com `utm_content=...-var-b` no checkout.\n"
                  "3. Publicar a B numa rota separada (`/b/`) e dividir o tráfego por link: posts/anúncios pares apontam para A, ímpares para B (ou 50/50 no anúncio).\n"
                  "4. Ler a venda por `utm_content` na Kiwify e as visitas no Clarity; lançar os números em data/landing/metricas.csv (slug `" + slug + "` para A e `" + slug + "-b` para B).\n\n"
                  "### Critério de decisão\n"
                  f"- Mínimo de {MIN_VISITAS} visitas por variante e 7 dias de teste.\n"
                  "- B vence se a conversão total for pelo menos 30% maior que a de A (ou 3 vendas a mais); então B vira a página principal.\n"
                  "- Se empatar ou perder, manter A e testar outra alavanca na próxima rodada. Uma mudança por vez.\n\n"
                  "Regras: sem promessa de cura, preço sem 'por dia/mês', prova social só real.\n")

def main(args):
    garantir_csv()
    agg = ler()
    slugs = args or sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(RAIZ, "config", "produtos_landing", "*.yaml")))
    if not agg:
        print("sem dados ainda: data/landing/metricas.csv está vazio (colunas: " + ",".join(COLS) + ").")
        print("Como medir:\n" + COMO_MEDIR)
        return 0
    for slug in slugs:
        if slug not in agg:
            print(f"{slug}: sem dados ainda."); continue
        txt = proposta(slug, agg[slug])
        out = os.path.join(RAIZ, "data", "landing", f"proposta_{slug}.md")
        open(out, "w", encoding="utf-8").write(txt)
        print(f"{slug}: proposta gravada em {os.path.relpath(out, RAIZ)}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

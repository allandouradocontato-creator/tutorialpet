"""Agente 09 — Monetization.

Otimiza posicionamento de anúncios e sugere diversificação de receita — mas só de
verdade depois que a conta AdSense do site estiver aprovada. Antes disso, roda em modo
"aguardando aprovação": ainda gera o plano (checklist geral + categorias de
diversificação, nenhuma delas específica de uma campanha real), mas não recomenda nada
como ação imediata e nunca insere código de anúncio ou gera um link de afiliado real.

Uso isolado:
    python agents/09_monetization/agent.py --site pets-tutores-iniciantes
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent
ROOT = AGENT_DIR.parents[1]
for p in (ROOT, AGENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.config import load_env_file, load_site  # noqa: E402
from core.io import now_iso  # noqa: E402
from core.log import get_logger  # noqa: E402

AGENT_NAME = "09_monetization"
SCHEMA_VERSION = "1.0"
MONETIZATION_DIR = ROOT / "data" / "monetization"

STATUS_QUE_LIBERA_PLANO_ATIVO = "aprovado"

# --------------------------------------------------------------------------- conteúdo do plano
ANUNCIOS_BOAS_PRATICAS = [
    "Nunca exibir mais anúncios do que conteúdo visível na tela — a política do Google não fixa "
    "mais um número exato, mas pune páginas dominadas por anúncios.",
    "Evitar anúncio logo acima da dobra ocupando a maior parte da tela em mobile — prejudica "
    "experiência e Core Web Vitals, que também pesam no ranqueamento.",
    "Nunca posicionar um anúncio de forma que pareça parte da navegação ou do conteúdo editorial "
    "de forma enganosa (exigir rótulo claro tipo 'Publicidade'/'Anúncio').",
    "Manter espaçamento mínimo entre unidades de anúncio e entre anúncio e botões/links clicáveis, "
    "para evitar cliques acidentais (proibido incentivar ou induzir clique em anúncio).",
    "Nunca usar pop-up ou intersticial agressivo que bloqueie o conteúdo antes de carregar.",
    "Posições de referência, testadas amplamente pelo mercado, para conteúdo no formato deste site: "
    "um anúncio após a introdução, um no meio do artigo (entre H2s), um antes do FAQ/CTA final.",
    "Em mobile, preferir menos unidades e anúncios responsivos — excesso prejudica velocidade de "
    "carregamento e a experiência em telas pequenas.",
]

# Categorias, não parcerias reais — nenhum link é inventado aqui.
DIVERSIFICACAO_PETS = [
    {"categoria": "Afiliados de petshops online",
     "descricao": "Programas de afiliados de grandes petshops/marketplaces com catálogo de produtos "
                   "para cães e gatos — avaliar comissão e prazo de cookie antes de aderir a qualquer um."},
    {"categoria": "Afiliados de fabricantes de ração e produtos específicos",
     "descricao": "Alguns fabricantes têm programa de afiliados próprio, com foco nos produtos "
                   "mencionados nos artigos de alimentação e cuidados diários."},
    {"categoria": "Produtos digitais próprios",
     "descricao": "Ex.: e-book 'Primeiros 30 dias com seu filhote', checklist imprimível de "
                   "primeiros cuidados, mini-curso por e-mail — capitaliza a persona do site sem "
                   "depender de terceiros."},
    {"categoria": "Newsletter com curadoria",
     "descricao": "Lista de e-mail com dicas + ofertas curadas (quando houver parcerias reais no "
                   "futuro) — constrói audiência própria, menos dependente de busca orgânica."},
    {"categoria": "Conteúdo patrocinado (com disclosure)",
     "descricao": "Opção de longo prazo, só depois que o site tiver tráfego relevante — exige "
                   "aviso claro de publicidade em qualquer conteúdo patrocinado, sem exceção."},
]


def render_plan(site: dict, status_adsense: str, plano_ativo: bool) -> str:
    hoje = now_iso()
    L = [f"# Plano de monetização — {site['site_id']}", "", f"- **Gerado em:** {hoje}",
         f"- **status_adsense atual:** `{status_adsense}`"]
    if not plano_ativo:
        L += [
            "",
            "> ⛔ **AGUARDANDO APROVAÇÃO NO ADSENSE.** Nenhuma ação real de monetização foi (ou será) "
            "tomada por este agente. O conteúdo abaixo é só planejamento — nenhum código de anúncio é "
            "inserido, nenhum link de afiliado é gerado, e nenhum posicionamento é aplicado a artigo "
            "nenhum enquanto `status_adsense` não for `aprovado` em "
            f"`config/sites/{site['site_id']}.yaml`.",
        ]
    else:
        L += ["", "✅ Conta aprovada — o plano abaixo pode orientar a implementação real (feita fora "
                    "deste pipeline, no CMS/tema do site)."]

    L += ["", "## Checklist de boas práticas de posicionamento de anúncios", ""]
    L += [f"- [ ] {item}" for item in ANUNCIOS_BOAS_PRATICAS]

    L += ["", "## Diversificação de receita sugerida para o nicho de pets", "",
          "*(Categorias apenas — nenhum link ou parceria real foi inventado aqui.)*", ""]
    for item in DIVERSIFICACAO_PETS:
        L += [f"### {item['categoria']}", "", item["descricao"], ""]

    L += ["## Próximos passos", ""]
    if not plano_ativo:
        L += [
            f"- [ ] Aplicar ao Google AdSense (gate `aprovacao_candidatura_adsense`, fora deste pipeline) "
            "e atualizar `status_adsense` para `aprovado` só depois da confirmação real do Google.",
            "- [ ] Rodar o agente 06 (platform compliance) e conferir o relatório de prontidão antes de aplicar.",
            "- [ ] Revisar este checklist de novo quando `status_adsense` mudar — o agente vai destravar "
            "o plano ativo automaticamente.",
        ]
    else:
        L += [
            "- [ ] Implementar as posições de anúncio no tema/CMS seguindo o checklist acima.",
            "- [ ] Escolher 1–2 categorias de diversificação para testar primeiro, com poucos artigos.",
            "- [ ] Revisitar este plano periodicamente (junto com o agente 10) para manter conformidade.",
        ]
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- entrypoint
def run(context: dict) -> dict:
    log = context["logger"]
    site_id = context["site_id"]
    site = context.get("site") or load_site(site_id)

    status_adsense = (site.get("monetizacao") or {}).get("status_adsense", "nao_aplicado")
    plano_ativo = status_adsense == STATUS_QUE_LIBERA_PLANO_ATIVO

    plano_md = render_plan(site, status_adsense, plano_ativo)
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    out_path = MONETIZATION_DIR / f"plano_{date_str}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(plano_md, encoding="utf-8")

    pendencias = []
    if not plano_ativo:
        pendencias.append(f"status_adsense = '{status_adsense}' — este agente permanece em modo "
                            "'aguardando aprovação' até esse campo virar 'aprovado' em "
                            f"config/sites/{site_id}.yaml (preenchido manualmente após a aprovação real).")
    else:
        pendencias.append("Conta aprovada — revisar o plano ativo e decidir a primeira posição de "
                           "anúncio a implementar.")

    output = {
        "agent": AGENT_NAME, "schema_version": SCHEMA_VERSION, "site_id": site_id, "gerado_em": now_iso(),
        "status": "ok",  # agente informativo — nunca bloqueia pipeline, só sinaliza modo via 'plano_ativo'
        "status_adsense": status_adsense, "plano_ativo": plano_ativo,
        "plano": str(out_path.relative_to(ROOT)), "pendencias_humanas": pendencias,
    }
    log.info(f"[{AGENT_NAME}] status_adsense={status_adsense} plano_ativo={plano_ativo} → {out_path.relative_to(ROOT)}")
    return output


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Agente 09 — plano de monetização (uso isolado)")
    parser.add_argument("--site", required=True, help="site_id (arquivo em config/sites/)")
    args = parser.parse_args()

    load_env_file()
    run_id = f"{now_iso().replace(':', '').replace('+0000', 'Z')}-{AGENT_NAME}"
    output = run({"site_id": args.site, "logger": get_logger(run_id)})
    return 0 if output["status"] == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())

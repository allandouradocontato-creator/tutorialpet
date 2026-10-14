"""Agente 29 - Marketing de Produto (sem LLM pago).
Le fila_temas + catalogo_tema_produto + produtos_relacionados + data/ofertas/*.json (mais recente),
liga cada tema da fila a um produto (proprio, afiliado ou 'sem produto'), pontua e grava
data/marketing/plano_semana.md. Acrescenta ao catalogo temas novos sugeridos (status: ideia).
Roda sem erro mesmo sem ofertas. Uso: python agents/29_marketing_produto/agent.py
"""
import os, re, sys, glob, json, datetime, unicodedata
import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CAT = os.path.join(RAIZ, "config", "catalogo_tema_produto.yaml")
FILA = os.path.join(RAIZ, "config", "fila_temas.yaml")
REL = os.path.join(RAIZ, "config", "produtos_relacionados.yaml")
SAIDA = os.path.join(RAIZ, "data", "marketing", "plano_semana.md")
STOP = set("a o as os de da do das dos e em no na para pra por com sem um uma que se ao como qual quais quanto quantos quando "
           "pode posso ser ter mais muito pet pets".split())

def norm(s):
    s = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

GENERICAS_RAW = {"cachorro", "gato", "cao", "caes", "filhote", "casa", "escolher", "lugar", "certo", "fazer", "ensinar",
             "acostumar", "evitar", "montar", "organizar", "melhor", "melhores", "idoso", "senior", "rotina", "tipo", "tipos", "limpar", "escovar", "escova", "sofa", "pelo", "seguranca", "viagem", "espaco", "pata", "patas"}

GENERICAS = {w[:7] for w in GENERICAS_RAW}

def toks(s):
    out = set()
    for w in re.findall(r"[a-z0-9]+", norm(s)):
        if w in STOP or len(w) < 3:
            continue
        out.add(w[:7])
    return out

def carregar(p, padrao):
    try:
        return yaml.safe_load(open(p, encoding="utf-8")) or padrao
    except Exception:
        return padrao

def ofertas_recentes():
    arqs = sorted(glob.glob(os.path.join(RAIZ, "data", "ofertas", "*.json")))
    if not arqs:
        return {}, None
    try:
        return json.load(open(arqs[-1], encoding="utf-8")), os.path.basename(arqs[-1])
    except Exception:
        return {}, None

def num(x):
    try:
        return float(x)
    except Exception:
        return 0.0

def melhor_oferta(prod, ofertas):
    lst = ofertas.get(prod.get("busca_shopee", ""))
    if not isinstance(lst, list) or not lst:
        return None
    return max(lst, key=lambda o: num(o.get("commissionRate")) * num(o.get("price")))

def pontuar_tema(t, ofertas):
    """0-100. Dor 25 (tem dor registrada), intencao 35, comissao 15, preco 10, oferta real 15."""
    pts = 25 if t.get("dor") else 10
    pts += 7 * min(max(int(t.get("intencao") or 3), 1), 5)
    best = None
    for p in t.get("produtos", []):
        o = melhor_oferta(p, ofertas)
        if o and (best is None or num(o.get("commissionRate")) * num(o.get("price")) > num(best.get("commissionRate")) * num(best.get("price"))):
            best = o
    if best:
        com = num(best.get("commissionRate"))  # Shopee devolve fracao (0.08) ou percentual
        com = com * 100 if com <= 1 else com
        pts += min(com / 10, 1) * 15
        preco = num(best.get("price"))
        pts += 10 if 20 <= preco <= 150 else 5
        pts += 15
    else:
        pts += 7  # estimativa neutra, aguardando oferta
    if any(p.get("tipo") == "proprio" for p in t.get("produtos", [])):
        pts += 5
    return round(min(pts, 100)), best

def casar(termo, temas, proprio):
    a = toks(termo)
    ac = a - GENERICAS
    melhor, escore = None, 0
    for t in temas:
        b = (toks(t["tema"]) | toks(" ".join(p.get("busca_shopee", "") for p in t.get("produtos", [])))) - GENERICAS
        comum = ac & b
        s = len(comum) if len(comum) >= 2 else 0
        if not s and comum:
            bp = toks(" ".join(p.get("busca_shopee", "") for p in t.get("produtos", []))) - GENERICAS
            s = 2 if comum & bp else 0
        if s > escore:
            melhor, escore = t, s
    if melhor and escore >= 2:
        return melhor, "catalogo"
    for pr in proprio:
        if any((toks(k) - GENERICAS) and (toks(k) - GENERICAS) <= a for k in pr.get("palavras_chave", [])):
            return pr, "proprio"
    return None, None

def busca_sugerida(termo):
    w = [x for x in norm(termo).split() if x not in STOP and x not in ("escolher", "melhor", "melhores", "montar", "organizar")]
    return " ".join(w[:4])

def main():
    cat = carregar(CAT, {"temas": []})
    temas = cat.get("temas", [])
    fila = carregar(FILA, {"temas": []}).get("temas", [])
    proprio = carregar(REL, {"produtos": []}).get("produtos", [])
    ofertas, arq = ofertas_recentes()
    ja = {norm(t["tema"]) for t in temas}

    linhas, sem, novos = [], [], []
    pontos_cat = {t["tema"]: pontuar_tema(t, ofertas)[0] for t in temas}
    for it in fila:
        if it.get("status") != "pendente":
            continue
        termo = it["termo"]
        alvo, via = casar(termo, temas, proprio)
        if via == "catalogo":
            tipos = sorted({p.get("tipo") for p in alvo["produtos"]})
            linhas.append((pontos_cat[alvo["tema"]], termo, "/".join(tipos), alvo["tema"]))
        elif via == "proprio":
            linhas.append((60, termo, "proprio", alvo["nome"]))
        else:
            sem.append((termo, it.get("pilar", "")))
            if it.get("pilar") == "produtos_compras" and norm(termo) not in ja:
                novos.append((termo, busca_sugerida(termo)))
    linhas.sort(key=lambda x: -x[0])

    hoje = datetime.date.today().isoformat()
    md = [f"# Plano de marketing de produto - {hoje}", "",
          f"Ofertas lidas: {arq or 'nenhuma (rodar agente 28 com SHOPEE_APP_ID/SHOPEE_SECRET)'}. Temas no catalogo: {len(temas)}.", "",
          "## 1. Fila de temas pendentes ligada a produto (maior pontuacao primeiro)", "",
          "| Pontos | Tema da fila | Tipo | Produto/assunto do catalogo |", "|---|---|---|---|"]
    md += [f"| {p} | {t} | {tp} | {a} |" for p, t, tp, a in linhas] or ["| - | nenhum | - | - |"]
    md += ["", "## 2. Temas da fila SEM produto (ir para o fim da fila)", ""]
    md += [f"- {t} ({pl})" for t, pl in sem] or ["- nenhum"]
    md += ["", "## 3. Catalogo: ranking de assuntos (artigo existente = pode receber CTA agora)", "",
           "| Pontos | Assunto | Artigo existente | Status das ofertas |", "|---|---|---|---|"]
    for t in sorted(temas, key=lambda x: -pontos_cat[x["tema"]]):
        sts = ",".join(sorted({p.get("status", "?") for p in t.get("produtos", [])}))
        md.append(f"| {pontos_cat[t['tema']]} | {t['tema']} | {t.get('artigo_existente') or 'FALTA ARTIGO'} | {sts} |")
    sem_art = [t["tema"] for t in temas if not t.get("artigo_existente")]
    md += ["", "## 4. Temas novos sugeridos ao catalogo (status: ideia)", ""]
    md += [f"- {t} (busca Shopee: {b})" for t, b in novos] or ["- nenhum novo nesta rodada"]
    md += ["", "## 5. Acoes", "",
           f"- Escrever artigo para assuntos de alta pontuacao sem artigo: {', '.join(sem_art) or 'nenhum'}.",
           "- Artigos com produto e sem link: rodar agente 28 (ofertas) e gerar link com sub_id por artigo.",
           "- Regras: sem alegacao medica, veterinario em saude, link de afiliado marcado, nunca preco por dia/mes.", ""]
    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    open(SAIDA, "w", encoding="utf-8").write("\n".join(md))

    if novos:
        extra = ""
        for termo, busca in novos:
            extra += (f'  - tema: "{termo}"\n    artigo_existente: null\n    dor: "a definir (sugerido pelo agente 29)"\n'
                      f'    intencao: 3\n    origem: marketing_produto\n    produtos:\n'
                      f'      - {{tipo: afiliado, busca_shopee: "{busca}", status: ideia}}\n')
        with open(CAT, "a", encoding="utf-8") as f:
            f.write(extra)
    print(f"plano gravado: {os.path.relpath(SAIDA, RAIZ)} | pendentes ligados: {len(linhas)} | sem produto: {len(sem)} | temas novos no catalogo: {len(novos)}")
    for p, t, tp, a in linhas[:8]:
        print(f"  {p:>3}  {t}  ->  {tp}: {a}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

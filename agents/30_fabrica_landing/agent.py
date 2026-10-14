"""Agente 30 - Fabrica de Landing (Tutorial Pet).
Uso: python agents/30_fabrica_landing/agent.py [slug|caminho.yaml ...]   (sem argumento: todos em config/produtos_landing/)
Le o YAML do produto, valida e gera templates/landing/saida/<slug>/index.html + vercel.json
(e <slug>/b/index.html para cada variante em `variantes`, com utm_content=var-b para medir por UTM).
Sem dependencias alem de PyYAML. Nao grava chaves; IDs de pixel/clarity vem do YAML (publicos).
"""
import os, re, sys, json, glob, html, time
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl
import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEMPLATE = os.path.join(RAIZ, "templates", "landing", "landing.template.html")
SAIDA = os.path.join(RAIZ, "templates", "landing", "saida")
PRODUTOS = os.path.join(RAIZ, "config", "produtos_landing")

# --- validacoes ---------------------------------------------------------
ALEGACAO_MEDICA = re.compile(
    r"\b(cura\w*|curar|curad\w+|trat(a|ar|amento)s?\b|rem[eé]dio\w*|medicament\w+|medica[cç][aã]o|"
    r"elimina\w* (a )?ansiedade|acaba\w* com (a )?ansiedade|doen[cç]a\w*|terapia|prescri\w+)", re.I)
PRECO_RECORRENTE = re.compile(r"R\$\s*[\d.,]+\s*(por|/|ao|a)\s*(dia|m[eê]s|semana)\b|\b(por|ao)\s+(dia|m[eê]s)\s*:?\s*R\$", re.I)
# trechos ressalvados: o proprio aviso pode dizer "nao substitui avaliacao veterinaria"
CAMPOS_IGNORADOS_ALEGACAO = {"aviso_conteudo"}

def textos(d, pref=""):
    if isinstance(d, dict):
        for k, v in d.items(): yield from textos(v, f"{pref}{k}.")
    elif isinstance(d, list):
        for i, v in enumerate(d): yield from textos(v, f"{pref}{i}.")
    elif isinstance(d, str):
        yield pref.rstrip("."), d

def validar(p):
    erros, avisos = [], []
    for c in ("slug", "nome", "promessa", "subpromessa", "oferta", "checkout_url", "faq", "passos", "beneficios"):
        if not p.get(c): erros.append(f"campo obrigatorio ausente: {c}")
    if not str(p.get("checkout_url", "")).startswith("https://"):
        erros.append("checkout_url obrigatorio e deve comecar com https://")
    if not (p.get("oferta") or {}).get("preco_por"): erros.append("oferta.preco_por ausente")
    if not p.get("privacidade_url"): erros.append("politica de privacidade nao linkada (privacidade_url)")
    if not p.get("termos_url"): erros.append("termos nao linkados (termos_url)")
    if not p.get("garantia_dias"): erros.append("garantia_dias ausente")
    for caminho, t in textos({k: v for k, v in p.items() if k != "variantes"}):
        if caminho.split(".")[0] in CAMPOS_IGNORADOS_ALEGACAO: continue
        m = ALEGACAO_MEDICA.search(t)
        if m: erros.append(f"possivel promessa de cura/alegacao medica em '{caminho}': '{m.group(0)}'")
        if PRECO_RECORRENTE.search(t): erros.append(f"preco com 'por dia/mes' em '{caminho}'")
    for k in ("preco_de", "preco_por"):
        v = str((p.get("oferta") or {}).get(k, ""))
        if re.search(r"dia|m[eê]s|semana", v, re.I): erros.append(f"oferta.{k} nao pode citar dia/mes: '{v}'")
    af = p.get("link_afiliado_opcional") or {}
    if af.get("url") and not af.get("texto"): erros.append("link de afiliado sem texto")
    if not (p.get("aviso_conteudo") or "").strip(): avisos.append("aviso_conteudo vazio (recomendado ressalva educativa)")
    for v in (p.get("variantes") or {}).values():
        for k in ("promessa", "subpromessa"):
            if k in v and ALEGACAO_MEDICA.search(v[k]): erros.append(f"variante com alegacao medica em {k}")
    return erros, avisos

# --- render -------------------------------------------------------------
def com_utm(url, utm, origem, extra=None):
    u = urlsplit(url)
    q = dict(parse_qsl(u.query))
    for k, v in (utm or {}).items(): q["utm_" + k] = str(v)
    q["utm_content"] = origem + (("-" + extra) if extra else "")
    return urlunsplit((u.scheme, u.netloc, u.path, urlencode(q), u.fragment))

def contexto(p, variante=None):
    p = dict(p)
    if variante: p.update(variante)
    o, af, m, an = p.get("oferta") or {}, p.get("link_afiliado_opcional") or {}, p.get("midia") or {}, p.get("analytics") or {}
    extra = "var-" + variante["_id"].lower() if variante else None
    preco = o.get("preco_por", "")
    c = dict(m)
    c.update({
        "nome": p["nome"], "titulo_pagina": p.get("titulo_pagina") or p["nome"], "descricao": p.get("descricao", ""),
        "promessa": p["promessa"], "subpromessa": p["subpromessa"], "micro_topo": p.get("micro_topo", ""),
        "passos_titulo": p.get("passos_titulo", "Simples de seguir"), "passos": p["passos"], "beneficios": p["beneficios"],
        "secao_dores": bool(p.get("secao_dores") and p.get("dores")), "dores": p.get("dores") or [],
        "dores_eyebrow": "Você se reconhece?", "dores_titulo": "Isso acontece com muita gente",
        "oferta_titulo": o.get("titulo", "Comece hoje"), "preco_de": o.get("preco_de", ""), "preco_por": preco,
        "itens_oferta": o.get("itens", []), "garantia_dias": p["garantia_dias"], "plataforma": p.get("plataforma", "Kiwify"),
        "faq": p["faq"], "aviso_conteudo": p.get("aviso_conteudo", ""), "empresa": p.get("empresa", ""),
        "contato_texto": p.get("contato_texto", ""), "privacidade_url": p["privacidade_url"], "termos_url": p["termos_url"],
        "prova_social": p.get("prova_social") or [],
        "afiliado_url": af.get("url", ""), "afiliado_texto": af.get("texto", ""), "afiliado_chamada": af.get("chamada", ""),
        "clarity_id": an.get("clarity_id", ""), "meta_pixel_id": an.get("meta_pixel_id", ""),
        "cta_texto_topo": p.get("cta_texto_topo") or f"Quero o {p['nome']} · {preco}",
        "cta_texto_meio": p.get("cta_texto_meio") or "Quero começar agora",
        "cta_texto_oferta": p.get("cta_texto_oferta") or f"Quero o {p['nome']}",
        "cta_texto_barra": p.get("cta_texto_barra") or f"Quero o {p['nome']} · {preco}",
    })
    for origem in ("topo", "meio", "oferta", "barra"):
        c["cta_" + origem] = com_utm(p["checkout_url"], p.get("utm"), origem, extra)
    return c

def val(c, nome):
    item = c.get("item")
    if nome == "item": v = item
    elif nome.startswith("item."): v = item.get(nome[5:], "") if isinstance(item, dict) else ""
    else: v = c.get(nome, "")
    return html.escape(str(v), quote=True) if v is not None else ""

def render(tpl, c):
    for _ in range(5):  # blocos IF (aninhaveis por nomes distintos)
        tpl = re.sub(r"<!--IF (\w+)-->(.*?)<!--/IF \1-->", lambda m: m.group(2) if c.get(m.group(1)) else "", tpl, flags=re.S)
    def each(m):
        out = []
        for it in c.get(m.group(1)) or []:
            cc = dict(c); cc["item"] = it
            out.append(re.sub(r"\{\{([\w.]+)\}\}", lambda x: val(cc, x.group(1)), m.group(2)))
        return "".join(out)
    tpl = re.sub(r"<!--EACH (\w+)-->(.*?)<!--/EACH \1-->", each, tpl, flags=re.S)
    tpl = re.sub(r"\{\{([\w.]+)\}\}", lambda x: val(c, x.group(1)), tpl)
    return tpl

def checar_saida(h, p):
    erros = []
    if re.search(r"\{\{|<!--(IF|EACH|/)", h): erros.append("placeholder nao resolvido na saida")
    if "privacidade" not in h or "Termos de uso" not in h: erros.append("saida sem links de privacidade/termos")
    af = (p.get("link_afiliado_opcional") or {}).get("url")
    if af and "(link de afiliado)" not in h: erros.append("link de afiliado sem aviso na saida")
    if af and 'rel="sponsored' not in h: erros.append("link de afiliado sem rel=sponsored")
    return erros

VERCEL = {"cleanUrls": True, "trailingSlash": False, "headers": [
    {"source": "/(.*)", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"},
                                     {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}]},
    {"source": "/(fotos|.*\\.(?:jpg|png|mp4|webp))", "headers": [{"key": "Cache-Control", "value": "public, max-age=86400"}]}]}

def gerar(caminho):
    p = yaml.safe_load(open(caminho, encoding="utf-8"))
    erros, avisos = validar(p)
    for a in avisos: print(f"  aviso: {a}")
    if erros:
        for e in erros: print(f"  ERRO: {e}")
        return False
    tpl = open(TEMPLATE, encoding="utf-8").read()
    pasta = os.path.join(SAIDA, p["slug"]); os.makedirs(pasta, exist_ok=True)
    h = render(tpl, contexto(p))
    e2 = checar_saida(h, p)
    if e2:
        for e in e2: print(f"  ERRO: {e}")
        return False
    open(os.path.join(pasta, "index.html"), "w", encoding="utf-8").write(h)
    json.dump(VERCEL, open(os.path.join(pasta, "vercel.json"), "w", encoding="utf-8"), indent=2)
    n = 1
    for vid, v in (p.get("variantes") or {}).items():
        v = dict(v); v["_id"] = vid
        hb = render(tpl, contexto(p, v))
        os.makedirs(os.path.join(pasta, vid.lower()), exist_ok=True)
        open(os.path.join(pasta, vid.lower(), "index.html"), "w", encoding="utf-8").write(hb); n += 1
    print(f"  ok: {os.path.relpath(pasta, RAIZ)}/index.html ({len(h)//1024} KB, {n} versao(oes)) + vercel.json")
    return True

def main(args):
    t0 = time.time()
    alvos = []
    for a in args or sorted(glob.glob(os.path.join(PRODUTOS, "*.yaml"))):
        alvos.append(a if a.endswith(".yaml") else os.path.join(PRODUTOS, a + ".yaml"))
    ok = True
    for a in alvos:
        print(f"[fabrica_landing] {os.path.basename(a)}"); ok &= gerar(a)
    print(f"[fabrica_landing] {'concluido' if ok else 'COM ERROS'} em {time.time()-t0:.2f}s")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

"""Agente 33 - Cacador diario de ofertas (MVP: Hotmart marketplace + Kindle BR).
Spec: cacador-diario.md. So le paginas PUBLICAS; nao cria conta, nao compra, nao baixa conteudo pago.
Saida: data/cacador/AAAA-MM-DD.json, data/cacador/prateleira.json (nota>=60, 30 dias) e
data/cacador/falhas.json (toda falha de captura vira linha para o Livro de Gaps).
Uso: python agent.py            (rodada real)
     python agent.py --teste    (usa agents/33_cacador_diario/fixtures, sem rede)
Os seletores sao de melhor esforco: a 1a rodada na nuvem mostra o que ajustar (ver falhas.json).
"""
import sys, os, re, json, datetime, urllib.request, html as H

HOJE = datetime.date.today().isoformat()
OUT = "data/cacador"
UA = {"User-Agent": "Mozilla/5.0 (compatible; FabricaCacador/0.1; leitura publica)", "Accept-Language": "pt-BR,pt;q=0.9"}
FONTES = [
    {"id": "hotmart", "regiao": "BR", "url": "https://hotmart.com/pt-br/marketplace/produtos", "tipo": "hotmart"},
    {"id": "kindle_br", "regiao": "BR", "url": "https://www.amazon.com.br/gp/bestsellers/digital-text", "tipo": "kindle"},
]

def baixar(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "replace")

def num(s):
    s = re.sub(r"[^\d,.]", "", s or "")
    if "," in s: s = s.replace(".", "").replace(",", ".")
    try: return float(s)
    except ValueError: return 0.0

def ler_hotmart(txt):
    """Procura __NEXT_DATA__ / JSON-LD; devolve itens {titulo,preco,avaliacoes,posicao}."""
    itens, blocos = [], re.findall(r'<script[^>]*type="application/(?:ld\+)?json"[^>]*>(.*?)</script>', txt, re.S)
    blocos += re.findall(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', txt, re.S)
    def andar(o):
        if isinstance(o, dict):
            n = o.get("name") or o.get("title") or o.get("productName")
            if n and (o.get("price") or o.get("offers") or o.get("rating") or o.get("ratingValue")):
                p = o.get("price") or (o.get("offers") or {}).get("price") if isinstance(o.get("offers"), dict) else o.get("price")
                itens.append({"titulo": str(n)[:140], "preco": num(str(p or 0)),
                              "avaliacoes": int(num(str(o.get("reviewCount") or o.get("ratingCount") or 0))),
                              "link": o.get("url") or ""})
            for v in o.values(): andar(v)
        elif isinstance(o, list):
            for v in o: andar(v)
    for b in blocos:
        try: andar(json.loads(b))
        except Exception: pass
    return itens

def ler_kindle(txt):
    itens = []
    for m in re.finditer(r'<div[^>]*id="gridItemRoot".*?(?=<div[^>]*id="gridItemRoot"|$)', txt, re.S):
        bloco = m.group(0)
        t = re.search(r'<div[^>]*class="[^"]*line-clamp[^"]*"[^>]*>(.*?)</div>', bloco, re.S) or re.search(r'alt="([^"]{5,140})"', bloco)
        if not t: continue
        titulo = H.unescape(re.sub(r"<[^>]+>", "", t.group(1))).strip()
        p = re.search(r"R\$\s*([\d.,]+)", bloco); a = re.search(r">\s*([\d.]+)\s*<\/span>\s*<\/a>", bloco)
        l = re.search(r'href="(/[^"]*/dp/[^"?]+)', bloco)
        itens.append({"titulo": titulo, "preco": num(p.group(1)) if p else 0.0,
                      "avaliacoes": int(num(a.group(1))) if a else 0,
                      "link": "https://www.amazon.com.br" + l.group(1) if l else ""})
    return itens

LEITORES = {"hotmart": ler_hotmart, "kindle": ler_kindle}

def nota(item, pos, total, fontes_n):
    s = max(0, 40 - pos * 40 // max(total, 1))                    # ranking/prova de venda direta (ate 40)
    s += min(item["avaliacoes"] // 25, 15)                         # avaliacoes (entra na mesma faixa, +15)
    s += 10 if fontes_n >= 2 else 0                                 # recorrencia
    return min(s, 100)                                             # anuncio ativo/engajamento entram na fase 2

def main(teste=False):
    os.makedirs(OUT, exist_ok=True)
    falhas, achados = [], {}
    for f in FONTES:
        try:
            txt = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", f"{f['tipo']}.html"), encoding="utf-8").read() if teste else baixar(f["url"])
            itens = LEITORES[f["tipo"]](txt)[:30]
            if not itens: falhas.append({"data": HOJE, "fonte": f["id"], "erro": "0 itens lidos (seletor/bloqueio)", "contorno": "ajustar leitor ou usar Chrome logado"})
            for i, it in enumerate(itens):
                k = re.sub(r"\W+", "", it["titulo"].lower())[:40]
                reg = achados.setdefault(k, {**it, "fontes": [], "regiao": f["regiao"], "melhor_pos": i, "total": len(itens)})
                reg["fontes"].append(f["id"]); reg["melhor_pos"] = min(reg["melhor_pos"], i)
        except Exception as e:
            falhas.append({"data": HOJE, "fonte": f["id"], "erro": str(e)[:200], "contorno": "tentar de novo amanha; se persistir, Chrome logado"})
    lista = []
    for r in achados.values():
        r["nota"] = nota(r, r["melhor_pos"], r["total"], len(set(r["fontes"])))
        r["nove_pontos"] = None   # extracao dos 9 pontos: passo 2 (modelo barato) sobre a pagina da oferta
        lista.append(r)
    lista.sort(key=lambda x: -x["nota"])
    json.dump({"data": HOJE, "itens": lista}, open(f"{OUT}/{HOJE}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    try: pr = json.load(open(f"{OUT}/prateleira.json", encoding="utf-8"))["itens"]
    except Exception: pr = []
    corte = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    pr = [x for x in pr if x.get("visto", "") >= corte and x["titulo"] not in {l["titulo"] for l in lista}]
    pr += [{**l, "visto": HOJE} for l in lista if l["nota"] >= 60]
    json.dump({"atualizado": HOJE, "itens": sorted(pr, key=lambda x: -x["nota"])[:60]}, open(f"{OUT}/prateleira.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if falhas:
        try: antigas = json.load(open(f"{OUT}/falhas.json", encoding="utf-8"))
        except Exception: antigas = []
        json.dump(antigas + falhas, open(f"{OUT}/falhas.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(lista)} ofertas; {sum(1 for l in lista if l['nota']>=60)} com nota>=60; {len(falhas)} falhas")

if __name__ == "__main__":
    main("--teste" in sys.argv)

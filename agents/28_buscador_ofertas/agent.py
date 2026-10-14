"""Agente 28 - Buscador de Ofertas (Shopee Afiliados).
Le config/catalogo_tema_produto.yaml, busca ofertas por tema na API aberta de afiliados da Shopee
(productOfferV2), ordena por comissao x vendas x nota e grava data/ofertas/<data>.json + .md.
Precisa dos segredos SHOPEE_APP_ID e SHOPEE_SECRET (portal de afiliados > API). Sem eles, sai com aviso.
ATENCAO: formato da assinatura e dos campos conforme a documentacao do portal; validar com chaves reais.
"""
import os, sys, json, time, hashlib, datetime, urllib.request
import yaml

URL = "https://open-api.affiliate.shopee.com.br/graphql"

def chamar(app_id, secret, query):
    payload = json.dumps({"query": query}, separators=(",", ":"))
    ts = str(int(time.time()))
    sig = hashlib.sha256((app_id + ts + payload + secret).encode()).hexdigest()
    req = urllib.request.Request(URL, data=payload.encode(), headers={
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={app_id}, Timestamp={ts}, Signature={sig}"})
    return json.load(urllib.request.urlopen(req, timeout=30))

def buscar(app_id, secret, termo, n=8):
    q = ('{ productOfferV2(keyword:"%s", sortType:2, page:1, limit:%d){ nodes{ productName price '
         'commissionRate sales ratingStar offerLink productLink } } }') % (termo.replace('"', ''), n)
    r = chamar(app_id, secret, q)
    return (((r.get("data") or {}).get("productOfferV2") or {}).get("nodes")) or [], r.get("errors")

def pontuar(o):
    try:
        return float(o.get("commissionRate") or 0) * float(o.get("price") or 0) * (float(o.get("ratingStar") or 0) / 5) * min(int(o.get("sales") or 0), 5000) ** 0.5
    except Exception:
        return 0

def main():
    app_id, secret = os.getenv("SHOPEE_APP_ID"), os.getenv("SHOPEE_SECRET")
    if not (app_id and secret):
        print("AVISO: faltam SHOPEE_APP_ID/SHOPEE_SECRET (portal de afiliados Shopee > API)."); return 0
    cat = yaml.safe_load(open("config/catalogo_tema_produto.yaml", encoding="utf-8"))
    saida = {}
    for t in cat["temas"]:
        for p in t["produtos"]:
            if p.get("tipo") == "afiliado" and p.get("busca_shopee"):
                nodes, err = buscar(app_id, secret, p["busca_shopee"])
                saida[p["busca_shopee"]] = sorted(nodes, key=pontuar, reverse=True)[:5] if nodes else {"erro": err}
    os.makedirs("data/ofertas", exist_ok=True)
    d = datetime.date.today().isoformat()
    json.dump(saida, open(f"data/ofertas/{d}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("ofertas gravadas:", d, {k: (len(v) if isinstance(v, list) else v) for k, v in saida.items()})
    return 0

if __name__ == "__main__":
    sys.exit(main())

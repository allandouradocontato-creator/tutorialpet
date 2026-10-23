"""Baixa fotos reais (Pexels) para os e-books Sozinho em Casa e Adestramento Basico.
Uso: python scripts/baixar_fotos_ebooks.py [--max-req 150] [--mapa data/produtos/ebooks_novo_visual/fotos_mapa.json]
Le o mapa, baixa ate 3 candidatas por consulta (largura 1000 px, JPEG q80, <=200 KB) em
data/produtos/ebooks_novo_visual/fotos/<secao>/<id>_<n>.jpg e grava creditos.json (fotografo + URL).
Retomavel: consultas ja completas sao puladas. Respeita o limite da API (200/h): para ao atingir --max-req
ou quando o cabecalho X-Ratelimit-Remaining ficar baixo; basta rodar de novo na hora seguinte.
Precisa de PEXELS_API_KEY (segredo do GitHub). A chave nunca e impressa."""
import argparse, io, json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--mapa", default="data/produtos/ebooks_novo_visual/fotos_mapa.json")
ap.add_argument("--saida", default="data/produtos/ebooks_novo_visual/fotos")
ap.add_argument("--max-req", type=int, default=150)
ap.add_argument("--reserva", type=int, default=8, help="para se restarem menos requisicoes que isso")
args = ap.parse_args()

UA = {"User-Agent": "Mozilla/5.0 TutorialPet"}
chave = os.environ["PEXELS_API_KEY"].strip()
mapa = json.loads(Path(args.mapa).read_text(encoding="utf-8"))
N = mapa.get("candidatas_por_consulta", 3)
saida = Path(args.saida); saida.mkdir(parents=True, exist_ok=True)
cred_path = saida / "creditos.json"
cred = json.loads(cred_path.read_text(encoding="utf-8")) if cred_path.exists() else []
usadas = {c["foto_id"] for c in cred}
RUIM = re.compile(r"shelter|cage|caged|sad|sick|ill\b|injur|abandon|stray|rescue|homeless|bleed|wound|dead|aggress|angry|bite|muzzle|crying|lonely|tied|chain|hospital bed|cone", re.I)
BOM = re.compile(r"dog|puppy|cat\b|kitten|pet\b|canine|labrador|retriever|corgi|beagle|poodle|spaniel|pug|husky|terrier", re.I)
reqs = 0; restante = None

def get(url, api=False, tentativas=4):
    global reqs, restante
    for t in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={**UA, **({"Authorization": chave} if api else {})})
            with urllib.request.urlopen(req, timeout=60) as r:
                if api:
                    reqs += 1
                    h = r.headers.get("X-Ratelimit-Remaining")
                    if h and h.isdigit(): restante = int(h)
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print("429 limite da API; encerrando este lote"); raise SystemExit(3)
            time.sleep(2 * (t + 1))
        except Exception:
            time.sleep(2 * (t + 1))
    return None

def comprimir(dados, dest):
    im = Image.open(io.BytesIO(dados)).convert("RGB")
    if im.width > 1000: im = im.resize((1000, round(im.height * 1000 / im.width)), Image.LANCZOS)
    for q in (80, 74, 68, 62):
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
        if buf.tell() <= 200_000: break
    else:
        im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=62, optimize=True)
    dest.write_bytes(buf.getvalue())

def salvar():
    cred_path.write_text(json.dumps(cred, ensure_ascii=False, indent=1), encoding="utf-8")

feitas = pend = 0
for sec in mapa["secoes"]:
    pasta = saida / sec["secao"]; pasta.mkdir(parents=True, exist_ok=True)
    for c in sec["consultas"]:
        if len(list(pasta.glob(f"{c['id']}_*.jpg"))) >= N: continue
        if reqs >= args.max_req or (restante is not None and restante < args.reserva):
            pend += 1; continue
        url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode({"query": c["q"], "per_page": 15, "locale": "en-US"})
        bruto = get(url, api=True)
        time.sleep(1.0)
        if not bruto: print("sem resposta", c["id"]); pend += 1; continue
        fotos = json.loads(bruto).get("photos", [])
        def nota(p):
            alt = p.get("alt", "") or ""
            return (0 if RUIM.search(alt) else 2) + (1 if BOM.search(alt) else 0) + (0.5 if p["width"] >= 1000 else 0)
        fotos = [p for p in fotos if not RUIM.search(p.get("alt", "") or "") and p["id"] not in usadas]
        fotos.sort(key=nota, reverse=True)
        n = 0
        for p in fotos:
            if n >= N: break
            dest = pasta / f"{c['id']}_{n+1}.jpg"
            dados = get(p["src"].get("large2x") or p["src"]["large"])
            if not dados: continue
            try: comprimir(dados, dest)
            except Exception as e: print("img invalida", p["id"], str(e)[:60]); continue
            usadas.add(p["id"]); n += 1
            cred.append({"arquivo": f"{sec['secao']}/{dest.name}", "secao": sec["secao"], "consulta_id": c["id"], "consulta": c["q"],
                         "foto_id": p["id"], "alt": p.get("alt", ""), "fotografo": p["photographer"],
                         "fotografo_url": p.get("photographer_url", ""), "pagina": p["url"]})
        if n < N: print(f"aviso: {c['id']} '{c['q']}' so {n} candidatas")
        feitas += 1
        if feitas % 10 == 0: salvar()
salvar()
print(f"consultas feitas neste lote: {feitas}; pendentes: {pend}; requisicoes: {reqs}; fotos totais: {len(cred)}")

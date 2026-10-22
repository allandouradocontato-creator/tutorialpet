"""Baixa candidatas Pexels (fotos reais) para a ficha visual do manual. Uso: python scripts/baixar_fotos_ficha.py <pasta_saida>
Grava <pasta>/<tema>_<n>.jpg e creditos.json. Precisa de PEXELS_API_KEY (segredo do GitHub)."""
import json, os, sys, urllib.parse, urllib.request
from pathlib import Path

TEMAS = {
    "porta": "dog waiting by front door at home",
    "relogio": "dog resting calmly at home alone",
    "brinquedo": "dog chewing toy on floor",
    "passeio": "dog walking on leash park sunny",
    "triste": "sad dog looking at door",
    "calmo": "happy dog lying on sofa",
}
UA = {"User-Agent": "Mozilla/5.0 TutorialPet"}
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
chave = os.environ["PEXELS_API_KEY"].strip()
cred = []
for tema, q in TEMAS.items():
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode({"query": q, "per_page": 6})
    req = urllib.request.Request(url, headers={**UA, "Authorization": chave})
    dados = json.loads(urllib.request.urlopen(req, timeout=60).read())
    for i, p in enumerate(dados.get("photos", [])[:6]):
        dest = out / f"{tema}_{i}.jpg"
        try:
            dest.write_bytes(urllib.request.urlopen(urllib.request.Request(p["src"]["large"], headers=UA), timeout=60).read())
            cred.append({"arquivo": dest.name, "tema": tema, "alt": p.get("alt", ""), "fotografo": p["photographer"], "pagina": p["url"]})
        except Exception as e:  # noqa: BLE001
            print("falhou", tema, i, str(e)[:80])
(out / "creditos.json").write_text(json.dumps(cred, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(cred), "fotos")

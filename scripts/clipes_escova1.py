#!/usr/bin/env python3
"""Clipes Pexels para o video 1 da escova (cachorro peludo/engracado). Uso: python3 scripts/clipes_escova1.py out [por_busca]
Baixa preferindo retrato (altura>largura), HD, 5-20 s; grava out/<busca>_<id>.mp4 e out/indice.json (credito do autor)."""
import os, sys, json, urllib.request, urllib.parse
from pathlib import Path
Q = ["dog blow drying", "dog grooming salon", "fluffy puppy", "shih tzu", "poodle grooming", "dog brushing fur", "golden retriever fur", "dog bath tub", "dog hair wind", "dog shaking fur"]
def get(url, key):
    r = urllib.request.Request(url, headers={"Authorization": key, "User-Agent": "tutorialpet/1.0"})
    return json.load(urllib.request.urlopen(r, timeout=40))
def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    key = os.environ["PEXELS_API_KEY"].strip(); idx = []
    for q in Q:
        try: d = get("https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": q, "per_page": 12, "orientation": "portrait"}), key)
        except Exception as e:
            print("busca falhou", q, e); continue
        got = 0
        for v in d.get("videos", []):
            if got >= n: break
            if not (4 <= v.get("duration", 0) <= 25): continue
            fs = [f for f in v["video_files"] if f.get("file_type") == "video/mp4" and f.get("height", 0) >= f.get("width", 0) and 720 <= f.get("height", 0) <= 1920]
            if not fs: continue
            f = sorted(fs, key=lambda x: x["height"])[0]
            p = out / f"{q.replace(' ', '_')}_{v['id']}.mp4"
            try:
                rq = urllib.request.Request(f["link"], headers={"User-Agent": "Mozilla/5.0 tutorialpet"}); p.write_bytes(urllib.request.urlopen(rq, timeout=90).read())
            except Exception as e:
                print("falhou", v["id"], e); continue
            idx.append({"busca": q, "id": v["id"], "arquivo": p.name, "dur": v["duration"], "autor": v["user"]["name"], "url": v["url"], "altura": f["height"]}); got += 1
    (out / "indice.json").write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8"); print(len(idx), "clipes")
main()

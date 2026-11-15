"""Gera voz (ElevenLabs, clone da Dra. Natasha) + clipes (Pexels) de um pedido em data/collab_natasha/.
Uso: python3 scripts/collab_video_assets.py data/collab_natasha/pedido_01.json out
Chaves vem do ambiente (secrets do GitHub); nada e impresso. Saida: out/voz.mp3, out/palavras.json, out/clips/*.mp4, out/info.json"""
import base64, json, os, re, subprocess, sys, urllib.parse, urllib.request
from pathlib import Path

ped = json.load(open(sys.argv[1], encoding="utf-8")); out = Path(sys.argv[2]); (out / "clips").mkdir(parents=True, exist_ok=True)
EK = os.environ["ELEVENLABS_API_KEY"].strip()

def eleven(path, body=None, method="GET"):
    req = urllib.request.Request("https://api.elevenlabs.io" + path, data=body, method=method,
                                 headers={"xi-api-key": EK, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=120))

def saldo():
    d = eleven("/v1/user/subscription"); return d["character_limit"] - d["character_count"], d.get("tier")

if not ped.get('pular_voz'):
    antes, tier = saldo(); print("SALDO_ANTES", antes, "plano", tier)
    voz = [v for v in eleven("/v1/voices")["voices"] if ped["voz_nome_contem"] in v["name"].lower()]
    print("VOZES_ENCONTRADAS", [(v["name"], v["voice_id"]) for v in voz])
    if not voz: sys.exit("sem voz da Natasha na conta")
    vid = voz[0]["voice_id"]
    body = json.dumps({"text": ped["texto"], "model_id": ped["modelo"],
                       "voice_settings": {"stability": ped["stability"], "similarity_boost": ped["similarity_boost"], "style": 0.0, "use_speaker_boost": True}}).encode()
    d = eleven(f"/v1/text-to-speech/{vid}/with-timestamps", body, "POST")
    bruto = out / "voz_bruta.mp3"; bruto.write_bytes(base64.b64decode(d["audio_base64"]))
    json.dump(d["alignment"], open(out / "alinhamento_bruto.json", "w"))  # guarda ANTES de qualquer outra etapa (evita pagar duas vezes)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(bruto), "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-ar", "44100", "-b:a", "192k", str(out / "voz.mp3")], check=True)
    al = d["alignment"]; pal, cur, ini, fim, dentro = [], "", None, None, False
    for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c == "[": dentro = True; continue
        if c == "]": dentro = False; continue
        if dentro: continue
        if c.isspace():
            if cur: pal.append([ini, fim, cur]); cur = ""
            continue
        if not cur: ini = a
        cur += c; fim = b
    if cur: pal.append([ini, fim, cur])
    pal = [p for p in pal if re.search(r"\w", p[2])]
    json.dump(pal, open(out / "palavras.json", "w", encoding="utf-8"), ensure_ascii=False)
    depois, _ = saldo(); print("SALDO_DEPOIS", depois, "gasto_caracteres", antes - depois, "pct_do_saldo_antes", round(100 * (antes - depois) / antes, 3))
    print("VOZ_ID", vid, "palavras", len(pal), "fim_s", pal[-1][1])

PK = os.environ.get("PEXELS_API_KEY", "").strip(); XK = os.environ.get("PIXABAY_API_KEY", "").strip(); info = []
RUIM = re.compile(r"sad|shelter|stray|sick|abandon|cage|injur|vet-clinic|dying|dirty", re.I)
pexels_vivo = bool(PK)

def candidatos(busca):
    global pexels_vivo
    if pexels_vivo:
        url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": busca, "orientation": "portrait", "per_page": 15})
        try:
            lista = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": PK}), timeout=40)).get("videos", [])
            res = []
            for v in lista:
                fs = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4" and (f.get("height") or 0) >= 1080]
                if fs and not RUIM.search(v.get("url", "")):
                    fs.sort(key=lambda f: abs((f.get("height") or 0) - 1920))
                    res.append({"fonte": "pexels", "id": v["id"], "link": fs[0]["link"], "pagina": v.get("url"), "autor": (v.get("user") or {}).get("name"), "retrato": True})
            if res: return res
        except Exception as e:
            print("pexels falhou", busca, str(e)[:60]); pexels_vivo = False
    if XK:
        url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": XK, "q": busca, "per_page": 20, "safesearch": "true"})
        try:
            hits = json.load(urllib.request.urlopen(url, timeout=40)).get("hits", [])
        except Exception as e:
            print("pixabay falhou", busca, str(e)[:60]); return []
        res = []
        for h in hits:
            if RUIM.search(h.get("tags", "") + h.get("pageURL", "")): continue
            vv = h.get("videos", {}); f = vv.get("large") or vv.get("medium")
            if not f or not f.get("url") or (f.get("height") or 0) < 1080 and (f.get("width") or 0) < 1080: continue
            res.append({"fonte": "pixabay", "id": h["id"], "link": f["url"], "pagina": h.get("pageURL"), "autor": h.get("user"), "retrato": (f.get("height") or 0) > (f.get("width") or 0), "tags": h.get("tags")})
        res.sort(key=lambda r: not r["retrato"])
        return res
    return []

for slot, busca in ped["cenas"].items():
    k = 0
    for c in candidatos(busca):
        if k >= 3: break
        bruto = out / "clips" / f"{slot}_{k}_raw.mp4"
        try:
            urllib.request.urlretrieve(c["link"], bruto)
            dest = out / "clips" / f"{slot}_{k}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(bruto), "-t", "2.5", "-an", "-vf",
                            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30",
                            "-c:v", "libx264", "-crf", "26", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(dest)], check=True)
            bruto.unlink(); info.append({"slot": slot, "arq": dest.name, "busca": busca, **{x: c[x] for x in c if x != "link"}}); k += 1
        except Exception as e:
            print("clip falhou", slot, str(e)[:100]); bruto.unlink(missing_ok=True)
json.dump(info, open(out / "info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("CLIPES", len(info), "slots", sorted({i["slot"] for i in info}), "pexels_vivo", pexels_vivo)

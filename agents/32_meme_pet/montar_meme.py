"""Monta vídeos de meme/identificação (Criador de Audiência, 15/10/2026): clipe do animal certo + texto grande + carimbo + música.
Sem voz (não gasta ElevenLabs). Uso: python agents/32_meme_pet/montar_meme.py /tmp/media [max_itens] [id ...]
Saída: /tmp/media/pacotes/<slug>/{video.mp4,legenda.txt,roteiro.json,manifest.json} no mesmo formato da fábrica."""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
FEITOS = ROOT / "data" / "audiencia" / "memes_feitos.txt"
DUR = 8.0
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(map(str, cmd[:3]))}: {r.stderr[-800:]}")
    return r.stdout


def _mv6():
    spec = importlib.util.spec_from_file_location("mv6", ROOT / "agents" / "17_video" / "montar_video6.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def quebra(t: str, n: int) -> str:
    return "\n".join(textwrap.wrap(t, n)) or t


def montar(item: dict, media: Path, mv6) -> bool:
    slug = "meme-" + item["id"]
    pkg = media / "pacotes" / slug
    if (pkg / "video.mp4").exists():
        return False
    tmp = ROOT / "data" / "audiencia" / "_tmp" / slug
    tmp.mkdir(parents=True, exist_ok=True)
    chave = os.environ.get("PEXELS_API_KEY", "").strip()
    clipes = mv6.pexels_videos(item["busca"], chave, 1, tmp, "clip") if chave else []
    if not clipes:
        print("  sem clipe para", slug)
        return False
    (tmp / "topo.txt").write_text(quebra(item["topo"], 17), encoding="utf-8")
    (tmp / "base.txt").write_text(quebra(item["base"], 15), encoding="utf-8")
    musicas = sorted((ROOT / "biblioteca" / "musica").glob("*.mp3"))
    musica = musicas[sum(map(ord, slug)) % len(musicas)] if musicas else None
    estilo = f"fontfile={FONTE}:fontcolor=white:borderw=7:bordercolor=black:line_spacing=12:fontsize=70:x=(w-text_w)/2"
    vf = (f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,"
          f"drawtext=textfile={tmp / 'topo.txt'}:{estilo}:y=330,"
          f"drawtext=textfile={tmp / 'base.txt'}:{estilo}:fontsize=84:y=1130")
    bruto = tmp / "bruto.mp4"
    sh(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(clipes[0]), "-t", str(DUR), "-an", "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-r", "30", str(bruto)])
    carimbo = ROOT / "assets" / "carimbo_tutorialpet.png"
    comc = tmp / "carimbo.mp4"
    sh(["ffmpeg", "-y", "-i", str(bruto), "-i", str(carimbo), "-filter_complex",
        "[0:v][1:v]overlay=x=44:y=150:format=auto[v]", "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "21", "-pix_fmt", "yuv420p", str(comc)])
    pkg.mkdir(parents=True, exist_ok=True)
    final = pkg / "video.mp4"
    if musica:
        sh(["ffmpeg", "-y", "-i", str(comc), "-stream_loop", "-1", "-i", str(musica), "-t", str(DUR), "-filter_complex",
            f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:d=0.5,afade=t=out:st={DUR - 1}:d=1[a]",
            "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(final)])
    else:
        final.write_bytes(comc.read_bytes())
    hashtags = item.get("tags", ["#tutorialpet"])
    artigo = item.get("artigo", "")
    legenda = item["legenda"] + ("\nhttps://tutorialpet.com.br" + artigo if artigo else "") + "\n" + " ".join(hashtags)
    (pkg / "legenda.txt").write_text(legenda, encoding="utf-8")
    (pkg / "roteiro.json").write_text(json.dumps({
        "titulo_video": item["topo"] + " " + item["base"], "gancho_3s": item["topo"] + " " + item["base"],
        "hashtags": hashtags, "formato": "meme_identificacao", "animal": item["animal"], "busca_clipe": item["busca"],
        "origem": "Criador de Audiência (data/audiencia/ideias.md)"}, ensure_ascii=False, indent=1), encoding="utf-8")
    (pkg / "manifest.json").write_text(json.dumps({
        "slug": slug, "status": "aprovado", "formato": "meme_identificacao", "tipo": "extra_audiencia",
        "criado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "artigo_url_futura": "https://tutorialpet.com.br" + artigo if artigo else "",
        "guardiao": {"status": "ok", "ok": [f"animal do clipe: {item['animal']} (busca '{item['busca']}', filtro de estilo Pexels)",
                                              "sem voz; texto original; carimbo aplicado"],
                     "em": datetime.now(timezone.utc).isoformat(timespec="seconds")},
        "aprovado_por": "Criador de Audiência: classe liberada (regra do Allan, 15/10/2026)"}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("pronto:", slug)
    return True


def main() -> int:
    media = Path(sys.argv[1])
    maximo = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    so = set(sys.argv[3:])
    fila = yaml.safe_load((ROOT / "config" / "memes_pet.yaml").read_text(encoding="utf-8"))["itens"]
    feitos = set(FEITOS.read_text(encoding="utf-8").split()) if FEITOS.exists() else set()
    mv6 = _mv6()
    n = 0
    for it in fila:
        if n >= maximo:
            break
        if it["classe"] != "liberada" or it["id"] in feitos or (so and it["id"] not in so):
            continue
        try:
            if montar(it, media, mv6):
                feitos.add(it["id"])
                n += 1
        except Exception as exc:  # noqa: BLE001
            print("ERRO", it["id"], exc)
    FEITOS.parent.mkdir(parents=True, exist_ok=True)
    FEITOS.write_text("\n".join(sorted(feitos)) + "\n", encoding="utf-8")
    print("produzidos agora:", n)
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())

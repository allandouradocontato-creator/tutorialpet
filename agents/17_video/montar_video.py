"""Agente 17 - Vídeo vertical 9:16 a partir do roteiro (100% gratuito).

Voz: edge-tts (vozes neurais pt-BR, grátis) | Imagens: Pexels (chave grátis no .env) | Montagem: FFmpeg.
Uso:  python agents/17_video/montar_video.py data/social/roteiros/<slug>.json
Saída: data/social/videos/<slug>.mp4  (+ <slug>.legenda.txt com a legenda pronta)
Teste sem rede: adicione --offline (voz de bip + vídeo de teste).
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

VOZ = os.environ.get("VOZ_PTBR", "pt-BR-FranciscaNeural")
W, H = 1080, 1920


def sh(cmd: list[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"falhou: {' '.join(cmd[:3])}...\n{r.stderr[-1500:]}")
    return r.stdout


def achar_fonte() -> str:
    for p in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if Path(p).exists():
            return p
    return ""


def esc_fonte(p: str) -> str:
    return p.replace("\\", "/").replace(":", "\\:")


def duracao(arq: Path) -> float:
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=nw=1:nk=1", str(arq)]).strip())


async def _tts(texto: str, saida: Path) -> None:
    import edge_tts
    await edge_tts.Communicate(texto, VOZ, rate="+0%").save(str(saida))


def narrar(texto: str, saida: Path, offline: bool) -> None:
    if offline:
        n = max(2.0, len(texto.split()) / 2.5)
        sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"sine=frequency=300:duration={n}", str(saida)])
    else:
        asyncio.run(_tts(texto, saida))


def baixar_pexels(busca: str, saida: Path, chave: str) -> bool:
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        {"query": busca, "orientation": "portrait", "size": "medium", "per_page": 8})
    req = urllib.request.Request(url, headers={"Authorization": chave, "User-Agent": "tutorialpet"})
    try:
        dados = json.load(urllib.request.urlopen(req, timeout=30))
        for v in dados.get("videos", []):
            arqs = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("height", 0) >= 720]
            if arqs:
                arqs.sort(key=lambda f: abs(f.get("height", 0) - 1920))
                urllib.request.urlretrieve(arqs[0]["link"], saida)
                return True
    except Exception as exc:  # noqa: BLE001
        print("  pexels:", exc)
    return False


def quebrar(texto: str, n: int = 24) -> str:
    linhas, atual = [], ""
    for pal in texto.split():
        if len(atual) + len(pal) + 1 > n and atual:
            linhas.append(atual)
            atual = pal
        else:
            atual = (atual + " " + pal).strip()
    linhas.append(atual)
    return "\n".join(linhas)


def montar_cena(i: int, cena: dict, tmp: Path, chave: str, offline: bool, fonte: str) -> Path:
    voz = tmp / f"voz{i}.mp3"
    narrar(cena["narracao"], voz, offline)
    dur = duracao(voz) + 0.35
    fundo = tmp / f"fundo{i}.mp4"
    tem = False
    if offline:
        sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"testsrc2=size={W}x{H}:rate=30:duration={dur}", str(fundo)])
        tem = True
    elif chave:
        tem = baixar_pexels(cena.get("visual_busca_banco_livre", "dog home"), fundo, chave)
    if tem:
        entrada = ["-stream_loop", "-1", "-i", str(fundo)]
        base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1"
    else:
        entrada = ["-f", "lavfi", "-i", f"color=c=0x1f3a5f:s={W}x{H}:r=30"]
        base = "setsar=1"
    txt = tmp / f"txt{i}.txt"
    txt.write_text(quebrar(cena.get("texto_na_tela", "")), encoding="utf-8")
    vf = base
    if fonte and cena.get("texto_na_tela"):
        vf += (f",drawtext=fontfile='{esc_fonte(fonte)}':textfile='{esc_fonte(str(txt))}':fontsize=68:fontcolor=white:"
               f"borderw=6:bordercolor=black:line_spacing=12:x=(w-text_w)/2:y=h*0.68")
    saida = tmp / f"cena{i}.mp4"
    sh(["ffmpeg", "-y", *entrada, "-i", str(voz), "-t", f"{dur:.2f}", "-vf", vf,
        "-map", "0:v", "-map", "1:a", "-af", "apad", "-shortest",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2", str(saida)])
    return saida


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    offline = "--offline" in sys.argv
    if not args:
        sys.exit("uso: python montar_video.py data/social/roteiros/<slug>.json [--offline]")
    if not shutil.which("ffmpeg"):
        sys.exit("FFmpeg não encontrado no PATH.")
    from core.config import load_env_file
    load_env_file()
    chave = os.environ.get("PEXELS_API_KEY", "").strip()
    rot = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    slug = rot.get("slug") or Path(args[0]).stem
    cenas = list(rot["cenas"])
    if rot.get("chamada_final"):
        cenas.append({"narracao": rot["chamada_final"], "visual_busca_banco_livre": "happy dog owner home",
                      "texto_na_tela": "Link na legenda"})
    fonte = achar_fonte()
    out_dir = ROOT / "data" / "social" / "videos"
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        partes = []
        for i, c in enumerate(cenas):
            print(f"cena {i + 1}/{len(cenas)}")
            partes.append(montar_cena(i, c, tmp, chave, offline, fonte))
        lista = tmp / "lista.txt"
        lista.write_text("".join(f"file '{p.as_posix()}'\n" for p in partes), encoding="utf-8")
        final = out_dir / f"{slug}.mp4"
        sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy", str(final)])
    (out_dir / f"{slug}.legenda.txt").write_text(rot.get("legenda", ""), encoding="utf-8")
    print("vídeo pronto:", final, f"({duracao(final):.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

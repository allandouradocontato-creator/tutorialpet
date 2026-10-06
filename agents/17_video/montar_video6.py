"""Agente 17 v4 - vídeo vertical 9:16 com mais retenção (100% gratuito).

Novidades: gancho forte no 1º segundo, legendas palavra-por-palavra (tempos reais do edge-tts),
cortes rápidos (2 imagens por cena), música de fundo opcional (data/social/musica/*.mp3, volume baixo).
Uso:  python agents/17_video/montar_video4.py data/social/roteiros/<slug>.json [--offline]
Saída: data/social/videos/<slug>_v2.mp4
"""
from __future__ import annotations

import asyncio
import json
import re
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

VOZ = os.environ.get("VOZ_PTBR", "pt-BR-FranciscaNeural")
W, H = 1080, 1920


def sh(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)
    if r.returncode != 0:
        raise RuntimeError(f"falhou: {' '.join(map(str, cmd[:3]))}...\n{r.stderr[-1500:]}")
    return r.stdout


def achar_fonte() -> str:
    for p in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if Path(p).exists():
            return p
    return ""


def esc(p: str) -> str:
    return p.replace("\\", "/").replace(":", "\\:")


def duracao(arq) -> float:
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "default=nw=1:nk=1", str(arq)]).strip())


async def _tts(texto: str, saida: Path) -> list[tuple[float, float, str]]:
    import edge_tts
    try:
        com = edge_tts.Communicate(texto, VOZ, boundary="WordBoundary")
    except TypeError:
        com = edge_tts.Communicate(texto, VOZ)
    palavras = []
    with open(saida, "wb") as f:
        async for ch in com.stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                ini = ch["offset"] / 1e7
                palavras.append((ini, ini + ch["duration"] / 1e7, ch["text"]))
    return palavras


def narrar(texto: str, saida: Path, offline: bool):
    if offline:
        n = max(2.0, len(texto.split()) / 2.5)
        sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"sine=frequency=300:duration={n}", str(saida)])
        ws = texto.split()
        return [(i * n / len(ws), (i + 1) * n / len(ws), w) for i, w in enumerate(ws)]
    palavras = asyncio.run(_tts(texto, saida))
    if not palavras:  # fallback: distribui igualmente
        n = duracao(saida)
        ws = texto.split()
        palavras = [(i * n / len(ws), (i + 1) * n / len(ws), w) for i, w in enumerate(ws)]
    return palavras


def ass_tempo(t: float) -> str:
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def gerar_ass(palavras, destino: Path, gancho: str | None, dur: float) -> None:
    cab = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n"
           "[V4+ Styles]\nFormat: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,"
           "Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
           "Style: Leg,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,2,2,60,60,520,1\n"
           "Style: Gancho,Arial,104,&H0000E5FF,&H0000E5FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,9,3,8,60,60,260,1\n\n"
           "[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
    linhas = []
    if gancho:
        linhas.append(f"Dialogue: 1,{ass_tempo(0)},{ass_tempo(min(3.0, dur))},Gancho,,0,0,0,,{{\\fad(80,200)}}{gancho.upper()}")
    grupos = [palavras[i:i + 3] for i in range(0, len(palavras), 3)]
    for gi, g in enumerate(grupos):
        prox = grupos[gi + 1][0][0] if gi + 1 < len(grupos) else None
        for k, (ini, fim, _) in enumerate(g):
            fim_ev = g[k + 1][0] if k + 1 < len(g) else max(fim, ini + 0.25)
            if k + 1 == len(g) and prox is not None:
                fim_ev = min(fim_ev, prox)  # nunca sobrepor o próximo grupo de legenda
            txt = " ".join(
                (f"{{\\c&H0000E5FF&}}{w[2].upper()}{{\\c&HFFFFFF&}}" if j == k else w[2].upper())
                for j, w in enumerate(g))
            linhas.append(f"Dialogue: 0,{ass_tempo(ini)},{ass_tempo(fim_ev)},Leg,,0,0,0,,{txt}")
    destino.write_text(cab + "\n".join(linhas) + "\n", encoding="utf-8")


def curl_bin() -> str:
    return shutil.which("curl.exe") or shutil.which("curl") or "curl"


GENTE = {"woman", "women", "man", "men", "girl", "boy", "people", "person", "persons", "hand", "hands", "owner",
         "owners", "child", "children", "kid", "kids", "family", "couple", "trainer", "lady", "human", "leg", "legs",
         "feet", "foot", "baby", "toddler", "male", "female", "teen", "student", "walking-with", "holding", "petting",
         "hugging", "playing-with", "cuddling", "yoga", "class"}


def tem_gente(v: dict) -> bool:
    """Pexels coloca a descricao no endereco da pagina; descarta clipes que citam pessoas ou maos."""
    partes = re.split(r"[^a-z]+", str(v.get("url", "")).lower().split("/video/")[-1])
    return any(p in GENTE for p in partes)


def pexels_videos(busca: str, chave: str, quantos: int, destino: Path, tag: str) -> list[Path]:
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        {"query": busca, "orientation": "portrait", "size": "medium", "per_page": 40})
    saidas = []
    try:
        r = subprocess.run([curl_bin(), "-sS", "-m", "40", "-H", f"Authorization: {chave}", url],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        for v in json.loads(r.stdout).get("videos", []):
            if tem_gente(v):
                continue
            arqs = [f for f in v.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("height", 0) >= 720]
            if not arqs:
                continue
            arqs.sort(key=lambda f: abs(f.get("height", 0) - 1920))
            out = destino / f"{tag}_{len(saidas)}.mp4"
            d = subprocess.run([curl_bin(), "-sS", "-L", "-m", "120", "-o", str(out), arqs[0]["link"]], capture_output=True)
            if d.returncode == 0 and out.exists() and out.stat().st_size > 10000:
                saidas.append(out)
            if len(saidas) >= quantos:
                break
    except Exception as exc:  # noqa: BLE001
        print("  pexels:", exc)
    return saidas


def quebrar(txt: str, n: int = 22) -> str:
    return txt


def montar_cena(i: int, cena: dict, tmp: Path, chave: str, offline: bool, primeira: bool) -> Path:
    voz = tmp / f"voz{i}.mp3"
    palavras = narrar(cena["narracao"], voz, offline)
    dur = duracao(voz) + 0.3
    ass = tmp / f"leg{i}.ass"
    gancho = cena.get("texto_na_tela") if primeira else None
    gerar_ass(palavras, ass, gancho, dur)

    fundos: list[Path] = []
    if offline:
        for k in range(2):
            f = tmp / f"fundo{i}_{k}.mp4"
            sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"testsrc2=size={W}x{H}:rate=30:duration=6", str(f)])
            fundos.append(f)
    elif chave:
        fundos = pexels_videos(cena.get("visual_busca_banco_livre", "dog home"), chave, 2, tmp, f"f{i}")
    partes = []
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1"
    if fundos:
        seg = dur / len(fundos)
        for k, f in enumerate(fundos):
            p = tmp / f"p{i}_{k}.mp4"
            sh(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(f), "-t", f"{seg:.2f}", "-vf", base + ",eq=saturation=1.1",
                "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", str(p)])
            partes.append(p)
    else:
        p = tmp / f"p{i}_0.mp4"
        sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c=0x1f3a5f:s={W}x{H}:r=30", "-t", f"{dur:.2f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", str(p)])
        partes.append(p)
    lst = tmp / f"l{i}.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in partes), encoding="utf-8")
    mudo = tmp / f"m{i}.mp4"
    sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(mudo)])
    saida = tmp / f"cena{i}.mp4"
    # legendas queimadas: ASS no diretório temporário (evita problemas de caminho do Windows)
    sh(["ffmpeg", "-y", "-i", mudo.name, "-i", voz.name, "-vf", f"subtitles={ass.name}",
        "-map", "0:v", "-map", "1:a", "-af", "apad", "-shortest", "-t", f"{dur:.2f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2", saida.name], cwd=str(tmp))
    return saida


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    offline = "--offline" in sys.argv
    if not args:
        sys.exit("uso: python montar_video4.py data/social/roteiros/<slug>.json [--offline]")
    if not shutil.which("ffmpeg"):
        sys.exit("FFmpeg não encontrado.")
    from core.config import load_env_file
    load_env_file()
    chave = os.environ.get("PEXELS_API_KEY", "").strip()
    rot = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    slug = rot.get("slug") or Path(args[0]).stem
    cenas = list(rot["cenas"])
    if rot.get("gancho_3s") and cenas:
        cenas[0] = dict(cenas[0], texto_na_tela=cenas[0].get("texto_na_tela") or rot["gancho_3s"])
    if rot.get("chamada_final"):
        cenas.append({"narracao": rot["chamada_final"], "visual_busca_banco_livre": "happy dog owner home", "texto_na_tela": ""})
    out_dir = ROOT / "data" / "social" / "videos"
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / f"{slug}_v2.mp4"
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        partes = []
        for i, c in enumerate(cenas):
            print(f"cena {i + 1}/{len(cenas)}")
            partes.append(montar_cena(i, c, tmp, chave, offline, i == 0))
        lista = tmp / "lista.txt"
        lista.write_text("".join(f"file '{p.as_posix()}'\n" for p in partes), encoding="utf-8")
        bruto = tmp / "bruto.mp4"
        sh(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy", str(bruto)])
        musicas = sorted((ROOT / "data" / "social" / "musica").glob("*.mp3")) if (ROOT / "data" / "social" / "musica").exists() else []
        if musicas:
            print("música de fundo:", musicas[0].name)
            sh(["ffmpeg", "-y", "-i", str(bruto), "-stream_loop", "-1", "-i", str(musicas[0]), "-filter_complex",
                "[1:a]volume=0.55,afade=t=in:d=1.5[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.95[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", str(final)])
        else:
            shutil.copy(bruto, final)
    (out_dir / f"{slug}_v2.legenda.txt").write_text(rot.get("legenda", ""), encoding="utf-8")
    print("vídeo pronto:", final, f"({duracao(final):.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

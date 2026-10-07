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


def _palavras_do_alinhamento(chars, inicios, fins) -> list[tuple[float, float, str]]:
    """Converte o alinhamento por caractere da ElevenLabs em (início, fim, palavra)."""
    palavras, atual, t0, t1 = [], [], None, 0.0
    for c, a, b in zip(chars, inicios, fins):
        if c.isspace():
            if atual:
                palavras.append((t0, t1, "".join(atual)))
                atual, t0 = [], None
            continue
        if t0 is None:
            t0 = a
        atual.append(c)
        t1 = b
    if atual:
        palavras.append((t0, t1, "".join(atual)))
    return palavras


def _normalizar_volume(arq: Path, alvo_lufs: float = -14.0) -> None:
    """O Eleven v4 sai ~5 dB mais baixo que o v3 (-19 LUFS). Sobe a narração para -14 LUFS (padrão de Reels/TikTok),
    sem mudar duração nem tom. Se o ffmpeg falhar, mantém o áudio original."""
    tmp = arq.with_suffix(".norm.mp3")
    try:
        sh(["ffmpeg", "-y", "-i", str(arq), "-af", f"loudnorm=I={alvo_lufs}:TP=-1.5:LRA=7", "-ar", "44100", "-b:a", "192k", str(tmp)])
        if tmp.exists() and tmp.stat().st_size > 1000:
            tmp.replace(arq)
    except Exception as e:  # noqa: BLE001
        print(f"  aviso: normalização de volume falhou ({type(e).__name__}); mantendo o áudio original", flush=True)
        tmp.unlink(missing_ok=True)


def _tts_elevenlabs(texto: str, saida: Path):
    """Narra com a ElevenLabs (plano pago do Allan). Devolve as palavras com tempos, ou None se não for possível.

    Precisa de ELEVENLABS_API_KEY e ELEVENLABS_VOICE_ID no ambiente (secrets do GitHub). Sem eles, ou se a
    chamada falhar duas vezes, devolve None e a fábrica usa o edge-tts como antes. A chave nunca é impressa.
    """
    chave = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    voz_id = os.environ.get("ELEVENLABS_VOICE_ID", "").strip()
    cfgv = {}
    try:  # o ID da voz e os ajustes de emoção não são segredo: ficam em config/voz_elevenlabs.yaml
        import yaml
        cfgv = yaml.safe_load((ROOT / "config" / "voz_elevenlabs.yaml").read_text(encoding="utf-8")) or {}
    except Exception:
        cfgv = {}
    if not voz_id:
        voz_id = str(cfgv.get("voice_id") or "").strip()
    if not chave or not voz_id:
        return None
    import base64
    import urllib.error
    import urllib.request
    modelo = os.environ.get("ELEVENLABS_MODEL") or cfgv.get("model_id") or "eleven_multilingual_v2"
    dados = {"text": texto, "model_id": modelo}
    if os.environ.get("ELEVENLABS_STABILITY"):  # só para testes de voz
        cfgv["stability"] = float(os.environ["ELEVENLABS_STABILITY"])
    if cfgv.get("stability") is not None:  # padrão da Duda: estabilidade baixa (Criativo) = mais emoção
        dados["voice_settings"] = {"stability": float(cfgv["stability"]),
                                   "similarity_boost": float(cfgv.get("similarity_boost", 0.75)),
                                   "style": float(cfgv.get("style", 0.0)),
                                   "use_speaker_boost": True}
    corpo = json.dumps(dados).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voz_id}/with-timestamps", data=corpo, method="POST",
        headers={"xi-api-key": chave, "Content-Type": "application/json"})
    for tentativa in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.load(r)
            saida.write_bytes(base64.b64decode(d["audio_base64"]))
            _normalizar_volume(saida)
            al = d.get("alignment") or {}
            print(f"  ElevenLabs ({modelo}): {len(texto)} caracteres narrados (~{len(texto)} créditos)", flush=True)
            ch, ini, fim = [], [], []
            dentro = False  # tira as tags de emoção [warmly] das legendas
            for c, a, b in zip(al.get("characters", []), al.get("character_start_times_seconds", []),
                               al.get("character_end_times_seconds", [])):
                if c == "[":
                    dentro = True
                    continue
                if c == "]":
                    dentro = False
                    continue
                if not dentro:
                    ch.append(c); ini.append(a); fim.append(b)
            return _palavras_do_alinhamento(ch, ini, fim)
        except urllib.error.HTTPError as e:
            print(f"  ElevenLabs: HTTP {e.code} (tentativa {tentativa})", flush=True)
            if e.code in (401, 403, 404, 422):  # chave, voz ou plano inválidos: repetir não ajuda
                break
        except Exception as e:  # rede, prazo, JSON
            print(f"  ElevenLabs: {type(e).__name__} (tentativa {tentativa})", flush=True)
    print("  ElevenLabs indisponível: usando a voz grátis (edge-tts)", flush=True)
    return None


def narrar(texto: str, saida: Path, offline: bool):
    sem_tags = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", texto)).strip()  # tags de emoção só servem à ElevenLabs
    if offline:
        n = max(2.0, len(sem_tags.split()) / 2.5)
        sh(["ffmpeg", "-y", "-f", "lavfi", "-i", f"sine=frequency=300:duration={n}", str(saida)])
        ws = sem_tags.split()
        return [(i * n / len(ws), (i + 1) * n / len(ws), w) for i, w in enumerate(ws)]
    pal_el = _tts_elevenlabs(texto, saida)
    if pal_el is not None:
        if not pal_el:  # sem alinhamento: distribui igualmente
            n = duracao(saida)
            ws = texto.split()
            pal_el = [(i * n / len(ws), (i + 1) * n / len(ws), w) for i, w in enumerate(ws)]
        return pal_el
    # Prazo na voz: o edge-tts pode ficar mudo a partir de IP de nuvem; 90 s por trecho, 2 tentativas.
    palavras = None
    for _ in range(2):
        try:
            palavras = asyncio.run(asyncio.wait_for(_tts(sem_tags, saida), timeout=90))
            break
        except asyncio.TimeoutError:
            print("  edge-tts: sem resposta em 90 s, tentando de novo", flush=True)
    if palavras is None:
        raise RuntimeError("edge-tts não respondeu (2 tentativas de 90 s)")
    if not palavras:  # fallback: distribui igualmente
        n = duracao(saida)
        ws = sem_tags.split()
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


def _estilo_viral() -> dict:
    try:
        import yaml
        return yaml.safe_load((ROOT / "config" / "estilo_viral.yaml").read_text(encoding="utf-8")) or {}
    except Exception:  # noqa: BLE001
        return {}


_EV = _estilo_viral()
_COR = _EV.get("cor", {})
EQ_COR = f"eq=saturation={_COR.get('saturacao', 1.1)}:brightness={_COR.get('brilho', 0)}:contrast={_COR.get('contraste', 1.0)}"
CORTES_POR_CENA = int(_EV.get("cortes", {}).get("cortes_por_cena", 2))


def tem_gente(v: dict) -> bool:
    """Pexels coloca a descricao no endereco da pagina; descarta clipes que citam pessoas ou maos."""
    partes = re.split(r"[^a-z]+", str(v.get("url", "")).lower().split("/video/")[-1])
    return any(p in GENTE for p in partes)


def pexels_videos(busca: str, chave: str, quantos: int, destino: Path, tag: str) -> list[Path]:
    saidas = _pexels_videos(busca, chave, quantos, destino, tag)
    if not saidas:  # busca eliminada pelo filtro de estilo: refaz com o animal em cena fofa
        animal = "cat" if re.search(r"\b(cat|kitten|gato)", busca.lower()) else "puppy" if "puppy" in busca.lower() else "dog"
        saidas = _pexels_videos(f"cute {animal} playing", chave, quantos, destino, tag)
    if len(saidas) < quantos:  # biblioteca de mídia: completa com outras fontes grátis (Pixabay)
        try:
            from core.biblioteca_midia import videos_pixabay
            saidas += videos_pixabay(busca, quantos - len(saidas), destino, tag, tem_gente)
        except Exception as exc:  # noqa: BLE001
            print("  biblioteca:", exc)
    return saidas


def _pexels_videos(busca: str, chave: str, quantos: int, destino: Path, tag: str) -> list[Path]:
    url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
        {"query": busca, "orientation": "portrait", "size": "medium", "per_page": 40})
    saidas = []
    try:
        r = subprocess.run([curl_bin(), "-sS", "-m", "40", "-H", f"Authorization: {chave}", url],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        from core.estilo_visual import ordenar  # só vídeo fofo e atraente, nunca triste/doente/bagunçado
        for v in ordenar(json.loads(r.stdout).get("videos", [])):
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
        fundos = pexels_videos(cena.get("visual_busca_banco_livre", "dog home"), chave, CORTES_POR_CENA, tmp, f"f{i}")
    partes = []
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,setsar=1"
    if fundos:
        seg = dur / len(fundos)
        for k, f in enumerate(fundos):
            p = tmp / f"p{i}_{k}.mp4"
            sh(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(f), "-t", f"{seg:.2f}", "-vf", base + "," + EQ_COR,
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
        carimbo = ROOT / "assets" / "carimbo_tutorialpet.png"  # patinha + "Tutorial Pet" em TODO vídeo (regra 07/10/2026)
        if carimbo.exists():
            com_carimbo = tmp / "bruto_carimbo.mp4"
            sh(["ffmpeg", "-y", "-i", str(bruto), "-i", str(carimbo), "-filter_complex",
                "[0:v][1:v]overlay=x=44:y=150:format=auto[v]", "-map", "[v]", "-map", "0:a?", "-c:v", "libx264",
                "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "copy", str(com_carimbo)])
            bruto = com_carimbo
        # biblioteca de música (Pixabay Music, licença livre): uma faixa por vídeo, escolhida pelo slug para variar
        pasta_m = ROOT / "biblioteca" / "musica"
        musicas = sorted(pasta_m.glob("*.mp3")) if pasta_m.exists() else []
        if not musicas and (ROOT / "data" / "social" / "musica").exists():
            musicas = sorted((ROOT / "data" / "social" / "musica").glob("*.mp3"))
        if musicas:
            # só faixas ENERGÉTICAS (config/estilo_viral.yaml -> musica.faixas_energeticas); alterna pelo slug
            prefer = [m for m in musicas if m.name in (_EV.get("musica", {}).get("faixas_energeticas") or [])]
            pool = prefer or musicas
            faixa = pool[sum(map(ord, slug)) % len(pool)]
            vol_db = float(_EV.get("musica", {}).get("volume_db", -7))  # nível da música em relação a -14 LUFS (voz)
            print("música de fundo:", faixa.name, "nível", vol_db, "dB (normalizada, com ducking sob a voz)")
            # 1) normaliza a faixa (as da biblioteca variam de -8 a -16 LUFS); 2) abaixa quando a Duda fala (sidechain)
            # e sobe nas pausas, o que dá energia sem encobrir a voz
            sh(["ffmpeg", "-y", "-i", str(bruto), "-stream_loop", "-1", "-i", str(faixa), "-filter_complex",
                f"[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,volume={vol_db}dB,afade=t=in:d=1.0[m];"
                "[0:a]asplit=2[v][vsc];"
                "[m][vsc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350:makeup=1[duck];"
                "[v][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.95[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(final)])
        else:
            shutil.copy(bruto, final)
    (out_dir / f"{slug}_v2.legenda.txt").write_text(rot.get("legenda", ""), encoding="utf-8")
    print("vídeo pronto:", final, f"({duracao(final):.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

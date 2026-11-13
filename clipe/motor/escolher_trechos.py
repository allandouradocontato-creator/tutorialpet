#!/usr/bin/env python3
"""Escolhe os melhores trechos de um vídeo do cliente (só ffmpeg + numpy, custo zero, sem GPU).

Para cada janela candidata (passo de 0,25 s) calcula uma nota com:
  - movimento moderado (o pet fazendo algo; parado = nota baixa, câmera tremendo = penalizada),
  - volume do áudio (latido, risada, voz = trecho vivo),
  - exposição (nem escuro nem estourado) e contraste (imagem nítida),
  - corte seco dentro da janela (troca de cena no meio do trecho = penalidade forte).
Depois pega as K melhores janelas SEM sobreposição (nunca repete trecho) e devolve em ordem cronológica.

Uso:  python3 escolher_trechos.py video.mp4 --dur 1.7 --k 3      (imprime JSON: [[inicio, duracao, nota], ...])
Sem numpy ou se a análise falhar, cai num plano simples: janelas espaçadas igualmente.
"""
import argparse, json, subprocess, sys

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

FW, FH, FPS_A, MAX_S = 48, 84, 4, 120   # miniatura em cinza, 4 quadros/s, analisa no máx. 120 s do vídeo
PASSO = 1                                 # janelas a cada 1 quadro (0,25 s)


def _out(cmd):
    r = subprocess.run(cmd, capture_output=True)
    return r.stdout if r.returncode == 0 else b""


def duracao(video):
    t = _out(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)]).decode().strip()
    try:
        return float(t)
    except ValueError:
        return 0.0


def _plano_simples(dur_video, dur, k):
    """Sem análise: janelas igualmente espaçadas (ainda sem sobreposição)."""
    if dur_video < 0.8:
        return []
    dur = min(dur, dur_video)
    n = max(1, min(k, int(dur_video // dur)))
    if n == 1:
        return [(round(max(0, (dur_video - dur) / 2), 2), round(dur, 2), 0.0)]
    passo = (dur_video - dur) / (n - 1)
    return [(round(i * passo, 2), round(dur, 2), 0.0) for i in range(n)]


def analisar(video):
    """Devolve dict com séries por quadro (4/s): movimento, brilho, contraste, corte, áudio (ou None se falhar)."""
    if np is None:
        return None
    bruto = _out(["ffmpeg", "-v", "error", "-t", str(MAX_S), "-i", str(video), "-an", "-vf",
                  f"fps={FPS_A},scale={FW}:{FH},format=gray", "-f", "rawvideo", "-"])
    n = len(bruto) // (FW * FH)
    if n < 3:
        return None
    q = np.frombuffer(bruto[: n * FW * FH], dtype=np.uint8).reshape(n, FH, FW).astype(np.float32)
    mov = np.zeros(n, dtype=np.float32)
    mov[1:] = np.abs(np.diff(q, axis=0)).mean(axis=(1, 2))
    brilho = q.mean(axis=(1, 2))
    contraste = q.std(axis=(1, 2))
    corte = mov > 45.0  # troca brusca de cena entre dois quadros
    aud = np.zeros(n, dtype=np.float32)
    pcm = _out(["ffmpeg", "-v", "error", "-t", str(MAX_S), "-i", str(video), "-vn", "-ac", "1", "-ar", "8000", "-f", "s16le", "-"])
    if len(pcm) > 8000:
        a = np.frombuffer(pcm[: len(pcm) // 2 * 2], dtype=np.int16).astype(np.float32) / 32768.0
        passo = 8000 // FPS_A
        m = len(a) // passo
        if m >= 1:
            rms = np.sqrt((a[: m * passo].reshape(m, passo) ** 2).mean(axis=1))
            p95 = float(np.percentile(rms, 95))
            if p95 > 0.005:  # tem som de verdade (não só ruído/silêncio)
                rms = np.clip(rms / p95, 0, 1)
                aud[: min(n, m)] = rms[: min(n, m)]
    return {"n": n, "mov": mov, "brilho": brilho, "contraste": contraste, "corte": corte, "aud": aud}


def _nota(an, i, w):
    mov = float(an["mov"][i + 1: i + w].mean()) if w > 1 else float(an["mov"][i])
    s_mov = min(mov / 10.0, 1.0)
    if mov > 28.0:                       # câmera tremendo / movimento caótico
        s_mov *= max(0.0, 1.0 - (mov - 28.0) / 30.0)
    s_aud = float(an["aud"][i: i + w].mean())
    s_con = min(float(an["contraste"][i: i + w].mean()) / 45.0, 1.0)
    b = float(an["brilho"][i: i + w].mean())
    s_exp = 1.0 if 35 <= b <= 225 else 0.4
    cortes = int(an["corte"][i + 1: i + w].sum())
    nota = 0.45 * s_mov + 0.25 * s_aud + 0.15 * s_con + 0.15 * s_exp - 0.6 * cortes
    if i == 0:                           # o 1º quadro costuma ter tranco de câmera
        nota -= 0.05
    return nota


def escolher(video, dur, k=3):
    """[(inicio_s, duracao_s, nota)] em ordem cronológica, até k janelas sem sobreposição."""
    dv = duracao(video)
    if dv < 0.8:
        return []
    if dv <= dur + 0.2:                   # vídeo curto: usa ele todo como uma cena
        return [(0.0, round(dv - 0.05, 2), 0.0)]
    try:
        an = analisar(video)
    except Exception:
        an = None
    if an is None:
        return _plano_simples(dv, dur, k)
    n = an["n"]
    w = max(2, int(round(dur * FPS_A)))
    if n < w + 1:
        return _plano_simples(dv, dur, k)
    cand = [(_nota(an, i, w), i) for i in range(0, n - w + 1, PASSO)]
    cand.sort(reverse=True)
    escolhidas = []
    for nota, i in cand:
        if len(escolhidas) >= k:
            break
        if all(i + w + 1 <= j or j + w + 1 <= i for _, j in escolhidas):  # folga de 1 quadro, nunca sobrepõe
            escolhidas.append((nota, i))
    return [(round(i / FPS_A, 2), round(w / FPS_A, 2), round(nota, 3)) for nota, i in sorted(escolhidas, key=lambda x: x[1])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--dur", type=float, default=1.7)
    ap.add_argument("--k", type=int, default=3)
    a = ap.parse_args()
    print(json.dumps(escolher(a.video, a.dur, a.k)))


if __name__ == "__main__":
    sys.exit(main())

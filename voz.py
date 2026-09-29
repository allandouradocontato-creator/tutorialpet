"""Narração pt-BR gratuita e local (Kokoro ONNX + espeak-ng). Sem cota, sem nuvem paga.
Uso: from voz import narrar; narrar("texto", "saida.wav", voz="pf_dora")"""
import json, os, re, shutil, subprocess, sys
import wave
import numpy as np, onnxruntime as ort

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.environ.get("KOKORO_MODEL", os.path.join(BASE, "kokoro-v1.0.onnx"))
VOICES = os.environ.get("KOKORO_VOICES", os.path.join(BASE, "voices-v1.0.bin"))
ESPEAK = os.environ.get("ESPEAK_BIN") or shutil.which("espeak-ng") or "espeak-ng"
ESPEAK_DATA = os.environ.get("ESPEAK_DATA_PATH")
SR = 24000
_sess = _voices = _vocab = None

def _load():
    global _sess, _voices, _vocab
    if _sess is None:
        _sess = ort.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
        _voices = np.load(VOICES, allow_pickle=True)
        cfg = json.load(open(os.path.join(BASE, "config.json"), encoding="utf-8"))
        _vocab = cfg["vocab"]
    return _sess

def _fonemas(txt):
    env = dict(os.environ)
    if ESPEAK_DATA: env["ESPEAK_DATA_PATH"] = ESPEAK_DATA
    out = subprocess.run([ESPEAK, "-q", "--ipa", "-v", "pt-br", txt], capture_output=True, text=True, env=env, encoding="utf-8")
    return " ".join(out.stdout.split())

def _sintetiza(fon, voz, vel):
    sess = _load()
    toks = [_vocab[c] for c in fon if c in _vocab][:510]
    if not toks: return np.zeros(0, dtype=np.float32)
    style = _voices[voz][min(len(toks), len(_voices[voz])) - 1]
    names = {i.name: i for i in sess.get_inputs()}
    tk = "input_ids" if "input_ids" in names else "tokens"
    sp = np.array([vel], dtype=np.float32) if "float" in names["speed"].type else np.array([max(1, round(vel))], dtype=np.int32)
    a = sess.run(None, {tk: np.array([[0, *toks, 0]], dtype=np.int64), "style": np.asarray(style, dtype=np.float32), "speed": sp})[0]
    return a.squeeze()

def narrar(texto, saida, voz="pf_dora", vel=1.0, pausa=0.25):
    frases = [f.strip() for f in re.split(r"(?<=[.!?:;])\s+", texto) if f.strip()]
    partes = []
    for f in frases:
        partes.append(_sintetiza(_fonemas(f), voz, vel))
        partes.append(np.zeros(int(pausa * SR), dtype=np.float32))
    audio = np.concatenate(partes) if partes else np.zeros(SR, dtype=np.float32)
    pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2")
    with wave.open(saida, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return len(audio) / SR

if __name__ == "__main__":
    print(narrar(" ".join(sys.argv[2:]) or "Olá, esta é a voz da Tutorial Pet.", sys.argv[1] if len(sys.argv) > 1 else "teste.wav"))

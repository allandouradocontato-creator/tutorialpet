#!/usr/bin/env python3
"""Transcreve audio.wav de cada pasta curadoria/lote5/<id>/ com faster-whisper (carrega WAV com wave+numpy)."""
import sys,glob,os,wave
import numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
for p in sorted(glob.glob("curadoria/lote5/*/audio.wav")):
    d=os.path.dirname(p); out=d+"/transcricao.txt"
    if os.path.exists(out): continue
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    segs,info=m.transcribe(a,beam_size=1,vad_filter=False)
    L=[f"[{s.start:05.1f}-{s.end:05.1f}] {s.text.strip()}" for s in segs]
    open(out,'w',encoding='utf-8').write(f"idioma={info.language} ({info.language_probability:.2f})\n"+('\n'.join(L) if L else '(sem fala detectada)'))
    print(d,info.language,len(L),'trechos')

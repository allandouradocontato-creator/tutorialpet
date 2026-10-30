#!/usr/bin/env python3
"""Baixa e prepara 1 candidato: original.mp4, folha.jpg (1 fps, tile 6x8, timestamp), audio.wav, transcricao.txt, comentarios.txt.
Uso: preparar_candidato.py <id_curto> <url> [lang]"""
import sys,os,subprocess,json,wave
import numpy as np
cid,url=sys.argv[1],sys.argv[2]; lang=sys.argv[3] if len(sys.argv)>3 else None
d=f"curadoria/lote4/{cid}"; os.makedirs(d,exist_ok=True)
def sh(c): return subprocess.run(c,shell=True,capture_output=True,text=True)
if not os.path.exists(f"{d}/original.mp4"):
    sh(f'yt-dlp -q -f "best[height<=1080]/best" -o "{d}/original.mp4" "{url}"')
if os.path.exists(f"{d}/original.mp4"):
    sh(f'ffmpeg -y -v error -i {d}/original.mp4 -vf "fps=1,drawtext=text=\'%{{pts\\:hms}}\':fontsize=40:fontcolor=yellow:box=1:boxcolor=black@0.6:x=10:y=10,scale=270:-1,tile=6x8" -frames:v 1 -q:v 3 {d}/folha.jpg')
    sh(f'ffmpeg -y -v error -i {d}/original.mp4 -ac 1 -ar 16000 {d}/audio.wav')
# comentários
r=sh(f'yt-dlp -q --no-download --write-comments --extractor-args "tiktok:comment_count=30" -j "{url}"')
com=[]
try:
    j=json.loads([l for l in r.stdout.splitlines() if l.startswith('{')][0])
    cs=sorted(j.get('comments') or [],key=lambda c:-(c.get('like_count') or 0))[:10]
    com=[f"{c.get('like_count')} curtidas | {c.get('text','')[:200]}" for c in cs]
except Exception as e: pass
open(f"{d}/comentarios.txt",'w',encoding='utf-8').write('\n'.join(com) if com else 'n/d (yt-dlp não devolveu comentários; tentar pelo Chrome)')

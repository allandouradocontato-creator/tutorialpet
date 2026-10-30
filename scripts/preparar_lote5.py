#!/usr/bin/env python3
"""Baixa e prepara (original.mp4, folha.jpg 1 fps, audio.wav) os candidatos do lote 5 em curadoria/lote5/<cid>/.
Uso: preparar_lote5.py A|B   (lê data/remix/lote5_filtro_A.csv ou _B.csv + /tmp/sel.json)"""
import sys,os,csv,json,re,subprocess,unicodedata
from concurrent.futures import ThreadPoolExecutor
v=sys.argv[1]; sel=set(json.load(open('/tmp/sel.json'))[v]); off=int(sys.argv[2]) if len(sys.argv)>2 else 0
rows=[r for r in csv.DictReader(open(f'data/remix/lote5_filtro_{v}.csv',encoding='utf-8')) if r['id'] in sel]
rows.sort(key=lambda r:-float(r['compart_pct']))
def slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return '_'.join(re.findall(r'[a-z0-9]+',s)[:3]) or 'video'
def sh(c): return subprocess.run(c,shell=True,capture_output=True,text=True)
def go(a):
    n,r=a; cid=f"{v.lower()}{n:02d}"; d=f"curadoria/lote5/{cid}"; os.makedirs(d,exist_ok=True)
    if not os.path.exists(f"{d}/original.mp4"):
        sh(f'yt-dlp -q -f "best[height<=1080]/best" -o "{d}/original.mp4" "{r["link"]}"')
    ok=os.path.exists(f"{d}/original.mp4")
    if ok:
        sh(f'ffmpeg -y -v error -i {d}/original.mp4 -vf "fps=1,drawtext=text=\'%{{pts\\:hms}}\':fontsize=40:fontcolor=yellow:box=1:boxcolor=black@0.6:x=10:y=10,scale=270:-1,tile=6x8" -frames:v 1 -q:v 3 {d}/folha.jpg')
        sh(f'ffmpeg -y -v error -i {d}/original.mp4 -ac 1 -ar 16000 {d}/audio.wav')
    nome=f"{cid}_{r['conta'].lstrip('@').replace('.','_')}_{slug(r['titulo'])}"
    json.dump(dict(cid=cid,id=r['id'],nome=nome,link=r['link'],conta=r['conta'],views=r['views'],compart_pct=r['compart_pct'],dur=r['dur'],idade_d=r['idade_d'],titulo=r['titulo'],baixou=ok),open(f"{d}/meta.json",'w'),ensure_ascii=False)
    return cid,ok
with ThreadPoolExecutor(4) as ex:
    for cid,ok in ex.map(go,enumerate(rows,1+off)): print(cid,'ok' if ok else 'FALHOU')

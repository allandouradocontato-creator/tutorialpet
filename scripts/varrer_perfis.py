#!/usr/bin/env python3
"""Lista vídeos recentes (<= N dias) de perfis via yt-dlp (sem navegador). Uso: varrer_perfis.py contas.txt saida_raw.txt [dias] [min_views]"""
import sys,json,subprocess,time
from concurrent.futures import ThreadPoolExecutor
contas=[c.strip().lstrip('@') for c in open(sys.argv[1]) if c.strip() and not c.startswith('#')]
out=sys.argv[2]; dias=float(sys.argv[3]) if len(sys.argv)>3 else 7.5; minv=int(sys.argv[4]) if len(sys.argv)>4 else 0
def f(c):
    try:
        o=subprocess.run(["yt-dlp","-j","--flat-playlist","--playlist-end","18",f"https://www.tiktok.com/@{c}"],capture_output=True,text=True,timeout=150).stdout
        r=[json.loads(x) for x in o.splitlines() if x.startswith('{')]
        return c,r
    except Exception as e: return c,[]
now=time.time(); lines=[]
with ThreadPoolExecutor(6) as ex:
    for c,r in ex.map(f,contas):
        k=[x for x in r if (now-(int(x['id'])>>32))/86400<=dias and (x.get('view_count') or 0)>=minv]
        print(c,len(r),'vídeos;',len(k),'recentes com views>=',minv,[ (x.get('view_count'),x['id']) for x in k][:4])
        if k: lines.append('# fonte: perfil @'+c); lines.append(' '.join(f"@{c}:{x['id']}" for x in k))
open(out,'a',encoding='utf-8').write('\n'.join(lines)+'\n')

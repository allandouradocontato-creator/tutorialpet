#!/usr/bin/env python3
"""Mede em paralelo links curtos (@user/video/id ou @user:id) via yt-dlp. Uso: medir_lote.py raw.txt saida.csv [min_views]"""
import sys,re,json,subprocess,csv,time
from concurrent.futures import ThreadPoolExecutor
raw,out=sys.argv[1],sys.argv[2]; minv=int(sys.argv[3]) if len(sys.argv)>3 else 0
links={}
src=None
for l in open(raw,encoding='utf-8'):
    l=l.strip()
    if l.startswith('# fonte:'): src=l[8:].strip(); continue
    for t in l.split():
        m=re.match(r'(@[^/: ]+)[:/](?:video/)?(\d{15,})',t)
        if m: links.setdefault(m.group(2),(m.group(1),src))
def med(i):
    u,s=links[i]
    url=f"https://www.tiktok.com/{u}/video/{i}"
    try:
        o=subprocess.run(["yt-dlp","-j","--no-download",url],capture_output=True,text=True,timeout=120).stdout
        d=json.loads([x for x in o.splitlines() if x.startswith('{')][0])
        return dict(id=i,conta=u,fonte=s,link=url,views=d.get('view_count'),curtidas=d.get('like_count'),coment=d.get('comment_count'),compart=d.get('repost_count'),dur=d.get('duration'),ts=d.get('timestamp'),titulo=(d.get('title') or '')[:90].replace('\n',' '))
    except Exception as e:
        return dict(id=i,conta=u,fonte=s,link=url,views=None,titulo='ERRO '+str(e)[:40])
with ThreadPoolExecutor(8) as ex: rows=list(ex.map(med,links))
now=time.time()
for r in rows:
    r['idade_d']=round((now-(int(r['id'])>>32))/86400,1)
rows.sort(key=lambda r:-(r['views'] or 0))
with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['id','conta','fonte','link','views','curtidas','coment','compart','dur','idade_d','ts','titulo']);w.writeheader()
    for r in rows: w.writerow({k:r.get(k) for k in w.fieldnames})
ok=[r for r in rows if (r['views'] or 0)>=minv]
print(len(links),'medidos;',sum(1 for r in rows if r['views'] is None),'erros;',len(ok),'com views >=',minv)
for r in ok[:40]: print(r['views'],r['conta'],r['dur'],'s',r['idade_d'],'d',round(100*(r['compart'] or 0)/r['views'],2),'%sh',r['link'].split('/video/')[1])

#!/usr/bin/env python3
"""Aplica a régua v5 (vertente A) em CSVs medidos. Uso: filtro_v5.py A|B saida.csv med1.csv [med2.csv ...]
A: views>=3 mi, compart>=2 %, idade<=30 d, dur 12-45 s. B: views>=300 mil, idade<=90 d (comentários/Shopee conferidos à parte)."""
import sys,csv
v,out,ins=sys.argv[1],sys.argv[2],sys.argv[3:]
rows={}
for f in ins:
    for r in csv.DictReader(open(f,encoding='utf-8')):
        rows.setdefault(r['id'],r)
res=[]
for r in rows.values():
    try: vw=int(float(r['views'])); sh=int(float(r['compart'] or 0)); d=float(r['dur']); age=float(r['idade_d'])
    except: r['passou']='n';r['motivo']='sem medida';res.append(r);continue
    if vw<=0: r['passou']='n';r['motivo']='sem medida';res.append(r);continue
    p=100*sh/vw; m=[]
    if v=='A':
        if vw<3_000_000:m.append('views<3mi')
        if p<2:m.append('compart<2%')
        if age>30:m.append('>30d')
        if d<12 or d>45:m.append('dur fora 12-45')
    else:
        if vw<300_000:m.append('views<300k')
        if age>90:m.append('>90d')
        if d<8 or d>60:m.append('dur fora 8-60')
    r['compart_pct']=round(p,2); r['passou']='s' if not m else 'n'; r['motivo']=','.join(m) or '—'; res.append(r)
res.sort(key=lambda r:(r['passou']!='s',-float(r.get('compart_pct') or 0)))
cols=['id','conta','fonte','link','views','curtidas','coment','compart','compart_pct','dur','idade_d','passou','motivo','titulo']
w=csv.DictWriter(open(out,'w',newline='',encoding='utf-8'),fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(res)
ok=[r for r in res if r['passou']=='s']
print(len(res),'medidos;',len(ok),'passam')
for r in ok: print(r['conta'],r['views'],r['dur'],'s',r['idade_d'],'d',r['compart_pct'],'%',r['id'])

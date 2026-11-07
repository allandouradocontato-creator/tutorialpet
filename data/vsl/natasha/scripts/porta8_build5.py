import subprocess,json,math,os,sys
O='/mnt/user-data/outputs'; P8=O+'/porta8'; DL='/mnt/user-data/uploads/Downloads/'
D='/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha'
os.makedirs('/tmp/p8/seg',exist_ok=True); os.makedirs('/tmp/p8/cap',exist_ok=True)
V18=DL+'VSL_Sozinho_em_Casa/teste_v2_v5/v18/vsl_c1_culpa_B_v18_natasha_1080.mp4'
C={'C1':DL+'Caramel_dog_waiting_by_door_a405e05d.mp4','C2':DL+'Dog_sitting_among_feathers_af874c50.mp4','C3':DL+'Dog_sitting_and_lying_down_5603756d.mp4','C4':DL+'Woman_looking_at_dog_with_f9343197.mp4','C5':DL+'Woman_opening_box_with_puppy_a87176e0.mp4','T':O+'/porta5/porta5_flow_thor_neutro_porta_v2.mp4','P':D+'/scripts/produto_anim2.mp4','V2':'/tmp/p8/V2.mp4','V3':'/tmp/p8/V3.mp4','V4':'/tmp/p8/V4.mp4','V5':'/tmp/p8/V5.mp4'}
IMG={'G':'/tmp/p7/card_garantia_crmv.png','R':'/tmp/p7/card_preco_v3.png'}
OFF=121.9; FE_AT=207.45; END=213.4
# (start, src, ss)
segs=[(0.0,'C4',0.4),(3.0,'V5',1.0),(6.0,'V4',0.0),
(11.6,'C5',0.3),(16.0,'C5',4.5),(19.9,'V2',0.0),(27.8,'V2',2.0),
(33.2,'C3',0.5),(36.0,'V3',0.0),(44.0,'C4',3.0),
(50.9,'C1',1.0),(54.5,'C2',0.5),(63.0,'V5',0.0),
(71.0,'V4',0.0),(79.0,'T',0.5),(83.0,'C1',3.0),
(88.8,'P',0.0),(92.0,'C3',2.0),(99.8,'C4',1.0),
(103.4,'C1',4.2),(110.5,'T',0.5),(116.5,'C5',2.0),
(121.9,'V5',0.0),(129.8,'C1',0.5),(131.5,'V3',0.0),(139.4,'T',1.0),
(146.2,'P',0.0),(149.8,'C3',3.0),(158.7,'C1',0.0),(166.0,'V2',0.0),
(173.6,'T',0.0),(179.5,'C1',2.0),
(185.3,'iG',0),(196.2,'iR',0),(207.4,'F',0)]
X=0.0
EQ="eq=contrast=1.05:saturation=1.1"
paths=[]
for i,(S,k,ss) in enumerate(segs):
    nxt=segs[i+1][0] if i+1<len(segs) else END
    L=round(nxt-S,3)
    out=f'/tmp/p8/seg/s{i:02d}.mp4'
    if k=='F':
        cmd=['ffmpeg','-y','-loglevel','error','-ss','52.06','-t','5.1','-i',V18,'-vf','setpts=1.06*PTS,scale=1080:1920,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=2,format=yuv420p','-an','-c:v','libx264','-crf','18','-t',str(L),out]
    elif k[0]=='i':
        N=int(math.ceil(L*30))+2
        vf=f"scale=1080:1920,zoompan=z='1+0.03*on/{N}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={N}:s=1080x1920:fps=30,format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-loop','1','-i',IMG[k[1]],'-vf',vf,'-t',str(L),'-r','30','-an','-c:v','libx264','-crf','18',out]
    else:
        pad='tpad=stop_mode=clone:stop_duration=6,'
        vf=f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,{pad}{EQ if k!='P' else 'null'},format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-ss',str(ss),'-t',str(L),'-i',C[k],'-vf',vf,'-an','-c:v','libx264','-crf','18','-t',str(L),out]
    if not os.path.exists(out) or os.path.getsize(out)<1000:
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode: print(i,k,r.stderr[-300:])
    paths.append(out)
open('/tmp/p8/list.txt','w').write(''.join(f"file '{p}'\n" for p in paths))
# captions
A=json.load(open('/tmp/p7/words_a5.json')); B=json.load(open('/tmp/p7/words_c20.json')); F=json.load(open('/tmp/p7/words_fe.json'))
def fix(t,ctx):
    t2=t.rstrip(',.!?'); p=t[len(t2):]
    m={'torre':'Thor','14':'catorze','10':'dez','97':'noventa e sete','27':'vinte e sete','pirrasa':'pirraça','CRMV6174':'CRMV 6174','-lata':'vira-lata'}
    if t2 in m: t2=m[t2]
    return t2+p
words=[]
for s,e,t in A:
    t=fix(t,'a')
    if t.lower().startswith('catorze') and 103<s<104.2: t='Catorze'
    words.append([s,e,t])
for s,e,t in B:
    words.append([s+OFF,e+OFF,fix(t,'b')])
for s,e,t in []:
    words.append([s+FE_AT,e+FE_AT,t])
# merge 'vira' + 'vira-lata'
w2=[]
for w in words:
    if w[2]=='vira-lata' and w2 and w2[-1][2]=='vira': w2[-1][1]=w[1]; w2[-1][2]='vira-lata'; continue
    w2.append(w)
# 'O sozinho em casa.' title
for i,w in enumerate(w2):
    if w[2]=='sozinho' and 90.5<w[0]<92: w[2]='Sozinho'
    if w[2]=='casa.' and 90.5<w[0]<92.5: w[2]='Casa.'
    if w[2]=='em' and 91<w[0]<92: w[2]='em'
    if w[2]=='sozinho' and OFF+24<w[0]<OFF+25.5: w[2]='Sozinho'
    if w[2]=='casa,' and OFF+25<w[0]<OFF+26: w[2]='Casa,'
words=w2
blocks=[];cur=[]
for w in words:
    cur.append(w); txt=' '.join(x[2] for x in cur)
    if w[2][-1] in ',.?!' or len(txt)>60: blocks.append(cur);cur=[]
if cur: blocks.append(cur)
fin=[]
for b in blocks:
    txt=' '.join(x[2] for x in b)
    if len(txt)>48: m=len(b)//2; fin+=[b[:m],b[m:]]
    else: fin.append(b)
caps=[]
for j,b in enumerate(fin):
    txt=' '.join(x[2] for x in b); a=b[0][0]; e=b[-1][1]+0.15
    if j+1<len(fin): e=min(e,fin[j+1][0][0]-0.02)
    if len(txt)>24:
        ws=txt.split(' '); best=None
        for q in range(1,len(ws)):
            l1=' '.join(ws[:q]);l2=' '.join(ws[q:]); d=abs(len(l1)-len(l2))
            if best is None or d<best[0]: best=(d,l1,l2)
        lines=[best[1],best[2]]
    else: lines=[txt]
    caps.append((a,e,lines))
json.dump(caps,open('/tmp/p8/caps.json','w'),ensure_ascii=False)
hooks=[(9.9,11.6),(21.8,23.5),(30.6,32.5),(48.7,50.7),(60.0,62.9),(68.8,70.8),(81.4,83.2),(86.3,88.6),(100.4,103.0),(116.2,120.6),(OFF+7.3,OFF+9.1),(OFF+63.4,OFF+64.7),(OFF+75.2,OFF+76.8)]
Z='+'.join(f"between(t,{a},{b})*0.12*(t-{a})/({b}-{a})" for a,b in hooks)
f='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; dt=[]
for j,(a,e,lines) in enumerate(caps):
    for q,l in enumerate(lines):
        fn=f'/tmp/p8/cap/c{j}_{q}.txt'; open(fn,'w').write(l)
        dt.append(f"drawtext=fontfile={f}:textfile={fn}:fontsize=64:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y=h*0.66+{q*82}:enable='between(t,{a:.2f},{e:.2f})'")
vf=f"scale=w='1080*(1+{Z})':h=-2:eval=frame,crop=1080:1920,setsar=1,{','.join(dt)}"
open('/tmp/p8/vf.txt','w').write(vf)
r=subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i','/tmp/p8/list.txt','-filter_script:v','/tmp/p8/vf.txt','-t',str(END),'-an','-r','30','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','/tmp/p8/long5_v.mp4'],capture_output=True,text=True);print(r.stderr[-800:])
print(os.path.getsize('/tmp/p8/long5_v.mp4'))

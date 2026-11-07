import subprocess,json,math,os
O='/mnt/user-data/outputs'; DL='/mnt/user-data/uploads/Downloads/'
D='/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha'
os.makedirs('/tmp/p9/seg7',exist_ok=True); os.makedirs('/tmp/p9/cap',exist_ok=True)
V18=DL+'VSL_Sozinho_em_Casa/teste_v2_v5/v18/vsl_c1_culpa_B_v18_natasha_1080.mp4'
C={'C1':DL+'Caramel_dog_waiting_by_door_a405e05d.mp4','C2':DL+'Dog_sitting_among_feathers_af874c50.mp4','C3':DL+'Dog_sitting_and_lying_down_5603756d.mp4','C4':DL+'Woman_looking_at_dog_with_f9343197.mp4','T':O+'/porta5/porta5_flow_thor_neutro_porta_v2.mp4','P':D+'/scripts/produto_anim2.mp4','V2':'/tmp/p8/V2.mp4','V3':'/tmp/p8/V3.mp4','V4':'/tmp/p8/V4.mp4','V5':'/tmp/p8/V5.mp4'}
C['Tb']=C['T']
C['PT']=DL+'Puppy_tearing_sofa_cushion_open_318ddab4.mp4'; C['WW']=DL+'Woman_comforting_whimpering_puppy_e505f866.mp4'; C['DP']=DL+'Dog_pacing_by_door_bd053778.mp4'; C['Db']=C['DP']
IMG={'iG':'/tmp/p7/card_garantia_crmv.png','iR':'/tmp/p7/card_preco_v3.png',
'sN2':O+'/porta7/porta7_still_N2_filhote_corre_v3.jpg','s02':O+'/porta7/porta7_still_02_cestinha_corpo_inteiro_v3.jpg',
's03':O+'/porta6/porta6_still_03_primeira_noite.jpg','s03b':O+'/porta6/porta6_still_03_primeira_noite.jpg',
's06':O+'/porta7/porta7_still_06_choro_v2.jpg','s10':O+'/porta6/porta6_still_10_volta.jpg'}
A_CUT=81.2
O7=81.7; D7,D8,D9,D10=22.674,24.033,24.189,20.428
O8=O7+D7+0.4; O9=O8+D8+0.4; O10=O9+D9+0.4; FE_AT=O10+D10+0.3; END=round(FE_AT+5.95,2)
segs=[(0.0,'C4',0.4),(3.0,'PT',1.0),(6.0,'V4',0.0),
(11.6,'sN2',0),(15.3,'s02',0),(19.9,'V2',0.0),(23.4,'WW',0.5),(27.2,'V2',3.5),(30.4,'s03b',0),
(33.2,'C3',0.5),(36.0,'V3',0.0),(44.0,'C4',3.0),(50.9,'C1',1.0),(54.5,'C2',0.5),(63.0,'s06',0),(66.0,'DP',1.0),
(71.0,'Tb',0.5),(74.0,'Db',0.5),(77.4,'V4',2.0),(79.1,'Db',4.5),(79.9,'V4',5.8),
(81.2,'V5',0.0),(84.0,'PT',2.0),(88.2,'C2',0.5),(90.3,'C4',0.5),(95.3,'V5',4.5),(98.0,'V5',6.0),(99.3,'V4',3.0),
(O8,'P',0.0),(110.0,'C3',3.0),(113.5,'C1',4.0),(117.0,'C4',2.0),(124.0,'C1',0.5),(125.3,'T',3.0),
(O9,'C4',5.0),(O9+2.5,'C1',0.0),(O9+5.2,'C4',3.0),(O9+7.3,'C1',1.5),(O9+11.5,'C3',0.5),(O9+16.3,'C1',4.2),(O9+18.3,'C4',0.4),(O9+21.3,'s10',0),
(O10,'P',0.0),(O10+5.2,'C2',1.0),(O10+7.7,'C3',2.0),(O10+9.9,'sN2',0),(O10+10.7,'C1',2.0),(O10+11.5,'C3',1.0),(O10+12.4,'C4',3.0),(O10+13.2,'T',0.5),(O10+14.6,'iR',0),(O10+16.4,'iG',0),(FE_AT,'F',0)]
segs=sorted(segs,key=lambda s:s[0])
EQ="eq=contrast=1.05:saturation=1.1"
var=[("1+0.10*on/{N}","iw/2-iw/zoom/2","ih/2-ih/zoom/2"),("1.10-0.10*on/{N}","iw/2-iw/zoom/2","ih/2-ih/zoom/2"),("1.06","(iw-iw/zoom)*on/{N}","ih/2-ih/zoom/2"),("1.06","(iw-iw/zoom)*(1-on/{N})","ih/2-ih/zoom/2")]
fnt='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
paths=[]
for i,(S,k,ss) in enumerate(segs):
    nxt=segs[i+1][0] if i+1<len(segs) else END
    L=round(nxt-S,3)
    out=f'/tmp/p9/seg7/s{i:02d}.mp4'
    if k=='F':
        cmd=['ffmpeg','-y','-loglevel','error','-ss','52.06','-t','5.1','-i',V18,'-vf','setpts=1.06*PTS,scale=1080:1920,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=2,format=yuv420p','-an','-c:v','libx264','-crf','18','-t',str(L),out]
    elif k in ('iG','iR','s10'):
        N=int(math.ceil(L*30))+2
        vf=f"scale=1080:1920,zoompan=z='1+0.03*on/{N}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={N}:s=1080x1920:fps=30,format=yuv420p" if k!='s10' else f"scale=2160:3840,zoompan=z='1+0.10*on/{N}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={N}:s=1080x1920:fps=30,{EQ},format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-loop','1','-i',IMG[k],'-vf',vf,'-t',str(L),'-r','30','-an','-c:v','libx264','-crf','18',out]
    elif k in IMG:
        N=int(math.ceil(L*30))+2; v=var[i%4]
        vf=f"scale=2160:3840,zoompan=z='{v[0].format(N=N)}':x='{v[1].format(N=N)}':y='{v[2]}':d={N}:s=1080x1920:fps=30,{EQ},noise=alls=6:allf=t,format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-loop','1','-i',IMG[k],'-vf',vf,'-t',str(L),'-r','30','-an','-c:v','libx264','-crf','18',out]
    else:
        pad='tpad=stop_mode=clone:stop_duration=6,'
        if k in ('Tb','Db'):
            tr=f"eq=contrast=1.15:saturation=0.55:brightness=-0.04,noise=alls=24:allf=t,vignette=PI/3.2,drawtext=fontfile={fnt}:text='REC':x=70:y=90:fontsize=48:fontcolor=red:borderw=3:bordercolor=black,drawtext=fontfile={fnt}:text='CAM 01  03\\:12\\:07':x=70:y=1800:fontsize=40:fontcolor=white:borderw=3:bordercolor=black"
            vf=f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,{pad}{tr},format=yuv420p"
        else:
            vf=f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,{pad}{EQ if k!='P' else 'null'},format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-ss',str(ss),'-t',str(L),'-i',C[k],'-vf',vf,'-an','-c:v','libx264','-crf','18','-t',str(L),out]
    if not os.path.exists(out) or os.path.getsize(out)<1000:
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode: print(i,k,r.stderr[-300:])
    paths.append(out)
open('/tmp/p9/list.txt','w').write(''.join(f"file '{p}'\n" for p in paths))
# ---- captions
A=json.load(open('/tmp/p7/words_a5.json'))
W={b:json.load(open(f'/tmp/p9/w_{b}.json')) for b in ['B7b','B8','B9','B10']}
words=[]
for s,e,t in A:
    if s>=81.0: continue
    t2=t.rstrip(',.!?'); p=t[len(t2):]
    if t2=='torre': t2='Thor'
    words.append([s,e,t2+p])
def add(b,off,fix):
    for s,e,t in fix(W[b]): words.append([s+off,e+off,t])
def f7(w):
    out=[]
    for s,e,t in w:
        m={'800':'oitocentos','fide,':'o feed,','tor':'Thor'}
        out.append([s,e,m.get(t,t)])
    return out
def f8(w):
    out=[]
    for s,e,t in w:
        if t=='sozinho': t='Sozinho'
        if t=='casa.' and s<2.5: t='Casa.'
        m={'10':'Dez','14,':'catorze,','a':'a','destradora.':'adestradora.'}
        t=m.get(t,t)
        if t=='a' and 17.3<s<17.6: continue
        out.append([s,e,t])
    return out
def f10(w):
    out=[];skip=0
    for s,e,t in w:
        if t in ('$','27,'): continue
        if t=='R': t='Vinte e sete reais,'
        if t=='de' and 5.8<s<6.0: t='disser'
        if t=='ser' and 6.0<s<6.2: continue
        if t=='14': t='catorze'
        if t=='vira': t='vira-lata'
        if t=='-lata': continue
        if t=='raça.': pass
        out.append([s,e,t])
    return out
add('B7b',O7,f7); add('B8',O8,f8); add('B10',O10,f10)
# B9 manual blocks by index
b9=W['B9']
blocks9=[(0,1,'Dia catorze.'),(2,4,'Oito horas fora.'),(5,9,'O vizinho na porta dela.'),(10,12,'Ela pensou: acabou.'),(13,15,'E ele disse:'),(16,18,'Você doou o Thor?'),(19,23,'Nunca mais ouvi ele latir.'),(24,26,'A casa inteira.'),(27,30,'Nada rasgado, nada arranhado.'),(31,35,'O Thor abanando o rabo.'),(36,38,'Não era manha.'),(39,40,'Era medo.'),(41,43,'E medo passa.'),(44,47,'E o controle remoto…'),(48,52,'nunca mais subiu na geladeira.')]
manual=[]
for a,b,t in blocks9: manual.append([b9[a][0]+O9,b9[b][1]+O9,t])
words.sort(key=lambda w:w[0])
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
for b in fin:
    caps.append([b[0][0],b[-1][1]+0.15,' '.join(x[2] for x in b)])
for a,e,t in manual: caps.append([a,e+0.1,t])
caps.sort(key=lambda c:c[0])
for j in range(len(caps)-1): caps[j][1]=min(caps[j][1],caps[j+1][0]-0.02)
out=[]
for a,e,txt in caps:
    if len(txt)>24:
        ws=txt.split(' '); best=None
        for q in range(1,len(ws)):
            l1=' '.join(ws[:q]);l2=' '.join(ws[q:]); d=abs(len(l1)-len(l2))
            if best is None or d<best[0]: best=(d,l1,l2)
        lines=[best[1],best[2]]
    else: lines=[txt]
    out.append((a,e,lines))
caps=out
json.dump(caps,open('/tmp/p9/caps.json','w'),ensure_ascii=False)
hooks=[(9.9,11.6),(21.8,23.5),(30.6,32.5),(48.7,50.7),(60.0,62.9),(68.8,70.8),
(O7+16.3,O7+17.6),(O7+19.0,O7+20.4),(O8+20.4,O8+24.0),(O9+2.4,O9+4.0),(O9+4.6,O9+6.2),(O10+0.0,O10+1.8)]
Z='+'.join(f"between(t,{a:.2f},{b:.2f})*0.12*(t-{a:.2f})/({b:.2f}-{a:.2f})" for a,b in hooks)
dt=[]
for j,(a,e,lines) in enumerate(caps):
    for q,l in enumerate(lines):
        fn=f'/tmp/p9/cap/c{j}_{q}.txt'; open(fn,'w').write(l)
        dt.append(f"drawtext=fontfile={fnt}:textfile={fn}:fontsize=64:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y=h*0.66+{q*82}:enable='between(t,{a:.2f},{e:.2f})'")
vf=f"scale=w='1080*(1+{Z})':h=-2:eval=frame,crop=1080:1920,setsar=1,{','.join(dt)}"
open('/tmp/p9/vf.txt','w').write(vf)
json.dump({'O7':O7,'O8':O8,'O9':O9,'O10':O10,'FE_AT':FE_AT,'END':END},open('/tmp/p9/times.json','w'))
print('times',O7,O8,O9,O10,FE_AT,END,len(segs))
if os.environ.get('FINAL')=='1':
    r=subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i','/tmp/p9/list.txt','-filter_script:v','/tmp/p9/vf.txt','-t',str(END),'-an','-r','30','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','/tmp/p9/long7_v.mp4'],capture_output=True,text=True);print(r.stderr[-800:])
    print(os.path.getsize('/tmp/p9/long7_v.mp4'))

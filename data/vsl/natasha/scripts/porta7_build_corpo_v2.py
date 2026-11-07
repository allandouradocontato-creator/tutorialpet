import subprocess,json,math,os
O='/mnt/user-data/outputs'; Q=O+'/porta7'; DL='/mnt/user-data/uploads/Downloads/'
D='/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha'
V18=DL+'VSL_Sozinho_em_Casa/teste_v2_v5/v18/vsl_c1_culpa_B_v18_natasha_1080.mp4'
os.makedirs('/tmp/p7/segd',exist_ok=True); os.makedirs('/tmp/p7/capd',exist_ok=True)
C={'C1':DL+'Caramel_dog_waiting_by_door_a405e05d.mp4','C2':DL+'Dog_sitting_among_feathers_af874c50.mp4','C3':DL+'Dog_sitting_and_lying_down_5603756d.mp4','C4':DL+'Woman_looking_at_dog_with_f9343197.mp4','T':O+'/porta5/porta5_flow_thor_neutro_porta_v2.mp4','P':D+'/scripts/produto_anim2.mp4'}
S6=O+'/porta6/porta6_still_%s.jpg'
IMG={'09':S6%'09_saida_calma','10':S6%'10_volta','G':'/tmp/p7/card_garantia_crmv.png','R':'/tmp/p7/card_preco_v3.png'}
SH=0.48
segs=[(0.00,'A'),(2.10,'v','C4',0.4),(6.10,'v','C2',0.5),(10.58,'i','09'),(15.48,'i','10'),(19.18,'v','C3',2.0),(23.48,'v','P',0.0),(26.48,'v','C1',1.0),(30.98,'v','C3',0.5),(34.98,'v','C4',1.0),(40.88,'v','T',0.0),(45.58,'i','G'),(49.48,'i','R'),(53.38,'F')]
END=58.68; X=0.12
EQ="eq=contrast=1.05:saturation=1.1"
paths=[]
for i,s in enumerate(segs):
    S,k=s[0],s[1]
    nxt=segs[i+1][0] if i+1<len(segs) else END
    L=round(nxt-S+(X if i+1<len(segs) else 0),3)
    out=f'/tmp/p7/segd/s{i:02d}.mp4'
    if k=='A':
        cmd=['ffmpeg','-y','-loglevel','error','-ss','10.28','-t',str(L),'-i',V18,'-vf','scale=1080:1920,setsar=1,fps=30,format=yuv420p','-an','-c:v','libx264','-crf','18',out]
    elif k=='F':
        cmd=['ffmpeg','-y','-loglevel','error','-ss','52.06','-t','5.1','-i',V18,'-vf','setpts=1.06*PTS,scale=1080:1920,setsar=1,fps=30,format=yuv420p','-an','-c:v','libx264','-crf','18','-t',str(L),out]
    elif k=='i':
        a=s[2]; N=int(math.ceil(L*30))+2
        if a in ('09','10'):
            vf=f"scale=2160:3840,zoompan=z='1+0.10*on/{N}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={N}:s=1080x1920:fps=30,{EQ},format=yuv420p"
        else:
            vf=f"scale=1080:1920,zoompan=z='1+0.03*on/{N}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={N}:s=1080x1920:fps=30,format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-loop','1','-i',IMG[a],'-vf',vf,'-t',str(L),'-r','30','-an','-c:v','libx264','-crf','18',out]
    else:
        a,ss=s[2],s[3]
        vf=f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,{'tpad=stop_mode=clone:stop_duration=0.6,' if a=='P' else EQ+','}format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-ss',str(ss),'-t',str(L),'-i',C[a],'-vf',vf,'-an','-c:v','libx264','-crf','18',out]
    if not os.path.exists(out) or os.path.getsize(out)<1000:
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode: print(i,r.stderr[-300:])
    paths.append(out)
# captions: OPEN words (2.2..6.1) + v19 words T>=5.62 shifted
OW=json.load(open('/tmp/p7/words_open.json'))
CW=json.load(open('/tmp/p7/cwords.json'))
num={'14':'Catorze','10':'dez','97':'noventa e sete','27':'vinte e sete'}
words=[]
for s,e,t in OW:
    if s>=2.2 and s<6.0: words.append((s,e,t))
for t,s,e in CW:
    if s<5.62 or s>=52.9: continue
    if t=='a' and abs(s-14.46)<0.05: continue
    if t=='volto' and abs(s-14.02)<0.05: t='volto,'
    t2=t.rstrip(',.!?'); p=t[len(t2):]
    if t2 in num: t=num[t2]+p
    if t2.lower() in('sozinho','casa') and 24<s<26.1: t=t2.capitalize()+p
    words.append((s+SH,e+SH,t))
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
json.dump(caps,open('/tmp/p7/capsd.json','w'),ensure_ascii=False)
ins=[];fl=[]
for i,p in enumerate(paths): ins+=['-i',p]; fl.append(f"[{i}:v]setpts=PTS-STARTPTS[v{i}]")
last='v0'
for i in range(1,len(paths)):
    fl.append(f"[{last}][v{i}]xfade=transition=fade:duration={X}:offset={segs[i][0]:.2f}[x{i}]"); last=f"x{i}"
f='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; dt=[]
for j,(a,e,lines) in enumerate(caps):
    for q,l in enumerate(lines):
        fn=f'/tmp/p7/capd/c{j}_{q}.txt'; open(fn,'w').write(l)
        dt.append(f"drawtext=fontfile={f}:textfile={fn}:fontsize=62:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y=h*0.66+{q*80}:enable='between(t,{a:.2f},{e:.2f})'")
fl.append(f"[{last}]{','.join(dt)},trim=0:{END},setpts=PTS-STARTPTS[cv]")
r=subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[cv]','-t',str(END),'-an','-c:v','libx264','-preset','veryfast','-crf','20','/tmp/p7/corpo4_video.mp4'],capture_output=True,text=True);print(r.stderr[-800:])
# corpo voice = open[0:6.1] + v19[5.62:52.9] + fecho
VO_OPEN=Q+'/vsl_filme_corpo_abertura_v1.mp3'; V19=Q+'/vsl_filme_corpo_voz_v19.mp3'; FE=D+'/fecho/FECHO_gravado_sem_Eu_sou_a_doutora_Natasha.mp3'
fa=("[0:a]atrim=0:6.1,asetpts=PTS-STARTPTS,aresample=44100[o];[1:a]atrim=5.62:52.9,asetpts=PTS-STARTPTS,aresample=44100[b];[2:a]atrim=0:5.3,asetpts=PTS-STARTPTS,aresample=44100[f];"
    "[o][b][f]concat=n=3:v=0:a=1,loudnorm=I=-16:TP=-1.5,aresample=44100[cvoz]")
r=subprocess.run(['ffmpeg','-y','-loglevel','error','-i',VO_OPEN,'-i',V19,'-i',FE,'-filter_complex',fa,'-map','[cvoz]','/tmp/p7/corpo4_voz.wav'],capture_output=True,text=True);print(r.stderr[-500:])
print(os.path.getsize('/tmp/p7/corpo4_video.mp4'))

import subprocess,json,math,os
O='/mnt/user-data/outputs'; Q=O+'/porta7'; DL='/mnt/user-data/uploads/Downloads/'
D='/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha/scripts'
os.makedirs('/tmp/p7/segc',exist_ok=True); os.makedirs('/tmp/p7/capc',exist_ok=True)
C={'C1':DL+'Caramel_dog_waiting_by_door_a405e05d.mp4','C2':DL+'Dog_sitting_among_feathers_af874c50.mp4','C3':DL+'Dog_sitting_and_lying_down_5603756d.mp4','C4':DL+'Woman_looking_at_dog_with_f9343197.mp4','T':O+'/porta5/porta5_flow_thor_neutro_porta_v2.mp4','P':D+'/produto_anim2.mp4'}
S6=O+'/porta6/porta6_still_%s.jpg'
IMG={'N':'/tmp/p7/nat.png','09':S6%'09_saida_calma','10':S6%'10_volta','G':'/tmp/p7/card_garantia_crmv.png','R':'/tmp/p7/card_preco_v3.png','F':'/tmp/p7/cta_last.png'}
segs=[(0.00,'i','N'),(5.60,'v','C2',0.5),(10.10,'i','09'),(15.00,'i','10'),(18.70,'v','C3',2.0),(23.00,'v','P',0.0),(26.00,'v','C1',1.0),(30.50,'v','C3',0.5),(34.50,'v','C4',1.0),(40.40,'v','T',0.0),(45.10,'i','G'),(49.00,'i','R'),(52.90,'i','F')]
END=58.12; X=0.12
EQ="eq=contrast=1.05:saturation=1.1"
var=[("1+0.10*on/{N}","iw/2-iw/zoom/2","ih/2-ih/zoom/2"),("1.10-0.10*on/{N}","iw/2-iw/zoom/2","ih/2-ih/zoom/2")]
paths=[]
for i,s in enumerate(segs):
    S,k,a=s[0],s[1],s[2]
    nxt=segs[i+1][0] if i+1<len(segs) else END
    L=round(nxt-S+(X if i+1<len(segs) else 0),3)
    out=f'/tmp/p7/segc/s{i:02d}.mp4'
    if k=='i':
        N=int(math.ceil(L*30))+2
        if a in ('N','09','10'):
            v=var[i%2]; vf=f"scale=2160:3840,zoompan=z='{v[0].format(N=N)}':x='{v[1]}':y='{v[2]}':d={N}:s=1080x1920:fps=30,{EQ},format=yuv420p"
        else:
            vf=f"scale=1080:1920,zoompan=z='1+0.03*on/{N}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={N}:s=1080x1920:fps=30,format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-loop','1','-i',IMG[a],'-vf',vf,'-t',str(L),'-r','30','-an','-c:v','libx264','-crf','18',out]
    else:
        ss=s[3]
        vf=f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,{'tpad=stop_mode=clone:stop_duration=0.6,' if a=='P' else EQ+','}format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-ss',str(ss),'-t',str(L),'-i',C[a],'-vf',vf,'-an','-c:v','libx264','-crf','18',out]
    if not os.path.exists(out) or os.path.getsize(out)<1000:
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode: print(i,r.stderr[-300:])
    paths.append(out)
# captions
W=json.load(open('/tmp/p7/cwords.json'))
num={'14':'Catorze','10':'dez','97':'noventa e sete','27':'vinte e sete'}
words=[]
for t,s,e in W:
    if t=='a' and abs(s-14.46)<0.05: continue
    if t=='volto' and abs(s-14.02)<0.05: t='volto,'
    t2=t.rstrip(',.!?'); p=t[len(t2):]
    if t2 in num: t=num[t2]+p
    t=t.replace('sozinho','Sozinho').replace('casa','Casa') if t.lower().startswith(('sozinho','casa')) and s>24 and s<26.1 else t
    words.append((s,e,t))
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
json.dump(caps,open('/tmp/p7/capsc.json','w'),ensure_ascii=False)
# corpo video
ins=[];fl=[]
for i,p in enumerate(paths): ins+=['-i',p]; fl.append(f"[{i}:v]setpts=PTS-STARTPTS[v{i}]")
last='v0'
for i in range(1,len(paths)):
    fl.append(f"[{last}][v{i}]xfade=transition=fade:duration={X}:offset={segs[i][0]:.2f}[x{i}]"); last=f"x{i}"
f='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; dt=[]
for j,(a,e,lines) in enumerate(caps):
    for q,l in enumerate(lines):
        fn=f'/tmp/p7/capc/c{j}_{q}.txt'; open(fn,'w').write(l)
        y0='h*0.78' if a>=52.9 else 'h*0.66'
        dt.append(f"drawtext=fontfile={f}:textfile={fn}:fontsize=62:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y={y0}+{q*80}:enable='between(t,{a:.2f},{e:.2f})'")
fl.append(f"[{last}]{','.join(dt)},trim=0:{END},setpts=PTS-STARTPTS[cv]")
corpo='/tmp/p7/corpo_video.mp4'
cmd=['ffmpeg','-y','-hide_banner','-loglevel','error']+ins+['-i','/tmp/p7/glow.png','-filter_complex',';'.join(fl)+f";[cv][{len(paths)}:v]overlay=enable='gte(t,55.0)+lt(t,55.0)*gte(t,53.0)*lt(mod(t-53.0,0.5),0.25)':shortest=1[o]",'-map','[o]','-t',str(END),'-an','-c:v','libx264','-preset','veryfast','-crf','20','-movflags','+faststart',corpo]
# glow image must loop as input
cmd=cmd[:cmd.index('/tmp/p7/glow.png')-1]+['-loop','1','-i','/tmp/p7/glow.png']+cmd[cmd.index('/tmp/p7/glow.png')+1:]
r=subprocess.run(cmd,capture_output=True,text=True);print(r.stderr[-1200:])
# long = ato1 v2 + corpo
A=Q+'/porta7_filme_ato1_v2.mp4'; AV=Q+'/vsl_filme_ato1_voz_v1.mp3'; CV=Q+'/vsl_filme_corpo_voz_v19.mp3'; M=DL+'atlasaudio-party-music-617594.mp3'
AEND=48.2; OFF=AEND-X; TOT=OFF+END
fl=[f"[0:v][1:v]xfade=transition=fade:duration={X}:offset={OFF:.2f},trim=0:{TOT:.2f},setpts=PTS-STARTPTS[vout]",
 f"[2:a]loudnorm=I=-16:TP=-1.5,apad=whole_dur={OFF:.2f},atrim=0:{OFF:.2f}[a1]",
 f"[3:a]loudnorm=I=-16:TP=-1.5,adelay={int(OFF*1000)}|{int(OFF*1000)},apad=whole_dur={TOT:.2f},atrim=0:{TOT:.2f}[a2]",
 f"[a1][a2]amix=inputs=2:duration=longest:normalize=0[va]",
 f"[4:a]atrim=0:{TOT:.2f},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-1.5,volume=-10dB,afade=t=in:d=0.5,afade=t=out:st={TOT-1.2:.2f}:d=1.2[ma]",
 "[va][ma]amix=inputs=2:duration=first:normalize=0[aout]"]
out=Q+'/porta7_vsl_filme_v1_longa.mp4'
cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-i',A,'-i',corpo,'-i',AV,'-i',CV,'-i',M,'-filter_complex',';'.join(fl),'-map','[vout]','-map','[aout]','-c:v','libx264','-preset','veryfast','-crf','21','-c:a','aac','-b:a','160k','-movflags','+faststart',out]
r=subprocess.run(cmd,capture_output=True,text=True);print(r.stderr[-1500:])
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out,'-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','64k',Q+'/porta7_vsl_filme_v1_longa_leve.mp4'])
print(TOT,os.path.getsize(out))

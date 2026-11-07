import subprocess,json,math,os,re
O='/mnt/user-data/outputs'; Q=O+'/porta7'; DL='/mnt/user-data/uploads/Downloads/'
S6=O+'/porta6/porta6_still_%s.jpg'
C={'C1':DL+'Caramel_dog_waiting_by_door_a405e05d.mp4','C2':DL+'Dog_sitting_among_feathers_af874c50.mp4','C3':DL+'Dog_sitting_and_lying_down_5603756d.mp4','C4':DL+'Woman_looking_at_dog_with_f9343197.mp4','C5':DL+'Woman_opening_box_with_puppy_a87176e0.mp4','T':O+'/porta5/porta5_flow_thor_neutro_porta_v2.mp4'}
V2={'06':Q+'/porta7_still_06_choro_v2.jpg','07':Q+'/porta7_still_07_quase_devolve_v2.jpg'}
def STP(a): return V2.get(a) or S6%ST[a]
ST={'01':'01_sonho','03':'03_primeira_noite','04':'04_destruicao','05':'05_bilhete_vizinho','06':'06_choro','07':'07_quase_devolve','08':'08_descoberta','09':'09_saida_calma','10':'10_volta'}
segs=[(0.00,'C2',2.2),(1.60,'s','04'),(3.10,'C4',0.4),(5.10,'s','06'),(6.36,'s','01'),(7.96,'s','01'),(9.46,'C5',0.3),(13.64,'s','03'),(15.54,'C3',1.5),(17.42,'C1',0.0),(19.44,'s','04'),(20.94,'C2',4.5),(22.98,'s','05'),(24.68,'C3',4.8),(26.28,'s','05'),(27.76,'s','06'),(29.26,'s','06'),(30.66,'s','07'),(32.66,'s','07'),(34.60,'s','08'),(36.30,'s','08'),(37.96,'C1',2.5),(41.52,'s','09'),(43.02,'T',0.5),(44.72,'s','10'),(46.20,'C1',5.5)]
END=48.2; X=0.12
EQ="eq=contrast=1.05:saturation=1.1"
var=[("1+0.10*on/{N}","iw/2-iw/zoom/2","ih/2-ih/zoom/2"),("1.10-0.10*on/{N}","iw/2-iw/zoom/2","ih/2-ih/zoom/2"),("1.06","(iw-iw/zoom)*on/{N}","ih/2-ih/zoom/2"),("1.06","(iw-iw/zoom)*(1-on/{N})","ih/2-ih/zoom/2")]
paths=[]
for i,(S,k,a) in enumerate(segs):
    nxt=segs[i+1][0] if i+1<len(segs) else END
    L=round(nxt-S+(X if i+1<len(segs) else 0),3)
    out=f'/tmp/p7/seg/s{i:02d}.mp4'
    if k=='s':
        N=int(math.ceil(L*30))+2; v=var[i%4]
        vf=f"scale=2160:3840,zoompan=z='{v[0].format(N=N)}':x='{v[1].format(N=N)}':y='{v[2]}':d={N}:s=1080x1920:fps=30,{EQ},noise=alls=6:allf=t,format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-loop','1','-i',STP(a),'-vf',vf,'-t',str(L),'-r','30','-an','-c:v','libx264','-crf','18',out]
    else:
        vf=f"scale=1080:1920:flags=lanczos,setsar=1,fps=30,{EQ},format=yuv420p"
        cmd=['ffmpeg','-y','-loglevel','error','-ss',str(a),'-t',str(L),'-i',C[k],'-vf',vf,'-an','-c:v','libx264','-crf','18',out]
    r=subprocess.run(cmd,capture_output=True,text=True); 
    if r.returncode: print(i,k,r.stderr[-300:])
    paths.append(out)
# captions
W=json.load(open('/tmp/p7/words.json'))
words=[]
for s,e,t in W:
    if t=='14': t='Catorze'
    words.append((s,e,t))
blocks=[];cur=[]
for w in words:
    cur.append(w)
    txt=' '.join(x[2] for x in cur)
    if w[2][-1] in ',.?!' or len(txt)>60:
        blocks.append(cur);cur=[]
if cur: blocks.append(cur)
fin=[]
for b in blocks:
    txt=' '.join(x[2] for x in b)
    if len(txt)>48:
        m=len(b)//2; fin+= [b[:m],b[m:]]
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
json.dump(caps,open('/tmp/p7/caps.json','w'),ensure_ascii=False)
ins=[];fl=[]
for i,p in enumerate(paths): ins+=['-i',p]; fl.append(f"[{i}:v]setpts=PTS-STARTPTS[v{i}]")
last='v0'
for i in range(1,len(paths)):
    off=segs[i][0]
    fl.append(f"[{last}][v{i}]xfade=transition=fade:duration={X}:offset={off:.2f}[x{i}]"); last=f"x{i}"
f='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; dt=[]
for j,(a,e,lines) in enumerate(caps):
    for q,l in enumerate(lines):
        fn=f'/tmp/p7/cap/c{j}_{q}.txt'; open(fn,'w').write(l)
        y=f"h*0.66+{q*80}"
        dt.append(f"drawtext=fontfile={f}:textfile={fn}:fontsize=62:fontcolor=white:borderw=7:bordercolor=black:x=(w-text_w)/2:y={y}:enable='between(t,{a:.2f},{e:.2f})'")
fl.append(f"[{last}]{','.join(dt)},trim=0:{END},setpts=PTS-STARTPTS[vout]")
n=len(paths); VO=Q+'/vsl_filme_ato1_voz_v1.mp3'; M=DL+'atlasaudio-party-music-617594.mp3'
ins+=['-i',VO,'-i',M]
fl.append(f"[{n}:a]loudnorm=I=-16:TP=-1.5,apad=whole_dur={END},atrim=0:{END}[va]")
fl.append(f"[{n+1}:a]atrim=0:{END},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-1.5,volume=-10dB,afade=t=in:d=0.5,afade=t=out:st={END-0.8}:d=0.8[ma]")
fl.append("[va][ma]amix=inputs=2:duration=first:normalize=0[aout]")
out=Q+'/porta7_filme_ato1_v2.mp4'
cmd=['ffmpeg','-y','-hide_banner','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[vout]','-map','[aout]','-c:v','libx264','-preset','veryfast','-crf','21','-c:a','aac','-b:a','160k','-movflags','+faststart',out]
r=subprocess.run(cmd,capture_output=True,text=True);print(r.stderr[-1500:])
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out,'-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','64k',Q+'/porta7_filme_ato1_v2_leve.mp4'])
for fn in ('porta7_filme_ato1_v2.mp4','porta7_filme_ato1_v2_leve.mp4'): print(fn,os.path.getsize(Q+'/'+fn))
print(len(caps),'blocos de legenda')

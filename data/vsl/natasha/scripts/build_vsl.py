import subprocess, re, json, sys, os
from PIL import Image, ImageDraw, ImageFont
U="/mnt/user-data/uploads/Downloads"; O="/mnt/user-data/outputs/natasha_voz"; W="/tmp/nat/work"
FONT="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
def sh(c): 
    r=subprocess.run(c,shell=True,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-1500:]); raise SystemExit(1)
    return r.stderr+r.stdout
def dur(f): return float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{f}"').strip())
def speech_axis(audio):
    out=sh(f'ffmpeg -i "{audio}" -af silencedetect=noise=-38dB:d=0.12 -f null - 2>&1')
    D=dur(audio); sil=[]; s=None
    for l in out.splitlines():
        m=re.search(r'silence_start: ([\d.]+)',l)
        if m: s=float(m.group(1))
        m=re.search(r'silence_end: ([\d.]+)',l)
        if m and s is not None: sil.append((s,float(m.group(1)))); s=None
    if s is not None: sil.append((s,D))
    # speech segments
    seg=[];t=0
    for a,b in sil:
        if a>t+0.05: seg.append((t,a))
        t=b
    if t<D-0.05: seg.append((t,D))
    return seg,D
def map_time(seg,x):  # x = fraction of speech time -> real time
    tot=sum(b-a for a,b in seg); k=x*tot
    for a,b in seg:
        if k<=b-a: return a+k
        k-=b-a
    return seg[-1][1]
def caption_png(text,path,size=76):
    f=ImageFont.truetype(FONT,size); W_=940
    words=text.split(); lines=[];cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if f.getlength(t)<=W_: cur=t
        else: lines.append(cur);cur=w
    lines.append(cur)
    lh=int(size*1.22); H=lh*len(lines)+30
    im=Image.new("RGBA",(1000,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    for i,l in enumerate(lines):
        x=(1000-f.getlength(l))/2; y=10+i*lh
        d.text((x,y),l,font=f,fill=(255,255,255,255),stroke_width=9,stroke_fill=(20,20,20,255))
    im.save(path); return H
def label_png(lines,path,size=30):
    f=ImageFont.truetype(FONT,size); wmax=int(max(f.getlength(l) for l in lines))+36
    h=len(lines)*int(size*1.45)+18
    im=Image.new("RGBA",(wmax,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,wmax-1,h-1),radius=18,fill=(20,20,20,150))
    for i,l in enumerate(lines): d.text((18,9+i*int(size*1.45)),l,font=f,fill=(255,255,255,255))
    im.save(path)
def build(name,audio,cuts,chunks,music,musvol=0.10):
    seg,D=speech_axis(audio); T=D+0.7
    # captions timing by char proportion
    n=[len(c) for c in chunks]; tot=sum(n); cum=0; times=[]
    for c,l in zip(chunks,n):
        a=map_time(seg,cum/tot); cum+=l; b=map_time(seg,cum/tot); times.append((a,b))
    times=[(0 if i==0 else times[i][0], times[i+1][0] if i+1<len(times) else T) for i in range(len(times))]
    if 'TIMES_OVERRIDE' in globals(): times=TIMES_OVERRIDE
    if callable(cuts): cuts=cuts(times,T)
    inp=[];fc=[];vi=0
    for (f,ss,dd) in cuts:
        inp.append(f'-ss {ss} -t {dd} -i "{f if f.startswith("/") else U+"/"+f}"')
    for i,(f,ss,dd) in enumerate(cuts):
        fc.append(f'[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,trim=duration={dd},setpts=PTS-STARTPTS[v{i}]')
    fc.append(''.join(f'[v{i}]' for i in range(len(cuts)))+f'concat=n={len(cuts)}:v=1:a=0[bg]')
    k=len(cuts)
    # inputs: audio, music, carimbo, labels, captions
    inp.append(f'-i "{audio}"'); ai=k; k+=1
    inp.append(f'-stream_loop -1 -i "{U}/{music}"'); mi=k; k+=1
    inp.append(f'-i /home/claude/tutorialpet/assets/carimbo_tutorialpet.png'); ci=k; k+=1
    label_png(["Dra. Natasha Braga · CRMV 6174"],f"{W}/{name}_lab.png")
    inp.append(f'-i {W}/{name}_lab.png'); li=k; k+=1
    inp.append('-i /tmp/nat/natasha_circulo.png'); pi=k; k+=1
    barp=f"{W}/{name}_bar.png"; _f=ImageFont.truetype(FONT,38); _t="Sozinho em Casa · manual + app · R$ 27"; _w=int(_f.getlength(_t))+60
    _im=Image.new("RGBA",(_w,84),(0,0,0,0)); _d=ImageDraw.Draw(_im); _d.rounded_rectangle((0,0,_w-1,83),radius=22,fill=(232,93,4,235)); _d.text((30,17),_t,font=_f,fill=(255,255,255,255)); _im.save(barp)
    inp.append(f'-i {barp}'); bi=k; k+=1
    fc.append(f'[{ci}:v]scale=300:-1[car]'); fc.append(f'[bg][{pi}:v]overlay=50:150[ph]'); fc.append(f'[ph][car]overlay=290:165[o1]')
    fc.append(f'[o1][{li}:v]overlay=290:253[o1b]'); fc.append(f'[o1b][{bi}:v]overlay=(W-w)/2:1780:enable=\'gte(t,1)\'[o2]')
    last='o2'; capin=[]
    for j,(c,(a,b)) in enumerate(zip(chunks,times)):
        p=f"{W}/{name}_c{j}.png"; H=caption_png(c,p); inp.append(f'-i {p}'); ii=k; k+=1
        y=1380-H//2
        fc.append(f'[{last}][{ii}:v]overlay=40:{y}:enable=\'between(t,{a:.2f},{b:.2f})\'[c{j}]'); last=f'c{j}'
    fc.append(f'[{last}]format=yuv420p,fade=t=out:st={T-0.4:.2f}:d=0.4[vout]')
    fc.append(f'[{ai}:a]apad=whole_dur={T},volume=1.0[vo];[{mi}:a]volume={musvol},atrim=0:{T},afade=t=out:st={T-0.8:.2f}:d=0.8[mu];[vo][mu]amix=inputs=2:duration=first:normalize=0[aout]')
    full=f'{O}/{name}_9x16_1080.mp4'; light=f'{O}/{name}_LEVE_540.mp4'
    cmd=f'ffmpeg -v error -y {" ".join(inp)} -filter_complex "{";".join(fc)}" -map "[vout]" -map "[aout]" -t {T:.2f} -c:v libx264 -preset veryfast -crf 22 -c:a aac -b:a 160k -movflags +faststart "{full}"'
    sh(cmd)
    sh(f'ffmpeg -v error -y -i "{full}" -vf scale=540:960 -c:v libx264 -preset veryfast -crf 31 -c:a aac -b:a 96k -movflags +faststart "{light}"')
    print(name,T,[ (round(a,1),round(b,1),c) for c,(a,b) in zip(chunks,times)]); print(os.path.getsize(full)//1024,os.path.getsize(light)//1024,"KB")

import subprocess, re, json, sys, os
from PIL import Image, ImageDraw, ImageFont
U="/mnt/user-data/uploads/Downloads"; O="/mnt/user-data/outputs/v10"; W="/tmp/v10/work"
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

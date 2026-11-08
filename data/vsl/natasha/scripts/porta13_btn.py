# porta13_btn.py : pílula inicial "SAIBA COMO RESOLVER ▸" (600x84) + botão laranja (860x120) + transição 0,3 s. Canvas 920x140, y=1550.
from PIL import Image,ImageDraw,ImageFont
import subprocess,os,shutil
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
CW,CH=920,140
big=Image.open('/tmp/p11/btn_full.png')   # laranja 1720x240 @2x
def pill(w=600,h=84):
    S=2; b=Image.new('RGBA',(w*S,h*S),(0,0,0,0)); d=ImageDraw.Draw(b)
    d.rounded_rectangle((0,0,w*S-1,h*S-1),radius=h*S//2,fill=(0,0,0,140))
    d.rounded_rectangle((3,3,w*S-4,h*S-4),radius=h*S//2-3,outline=(255,255,255,235),width=4)
    f=ImageFont.truetype(F,int(h*S*0.42)); t='SAIBA COMO RESOLVER ▸'; tw=d.textlength(t,font=f)
    d.text(((w*S-tw)/2,h*S*0.27),t,font=f,fill=(255,255,255,255),stroke_width=2,stroke_fill=(0,0,0,200))
    return b
P=pill()
def put(im,w,h,alpha=1.0):
    r=im.resize((max(2,int(w)),max(2,int(h))),Image.LANCZOS)
    if alpha<1: r.putalpha(r.getchannel('A').point(lambda v:int(v*alpha)))
    c=Image.new('RGBA',(CW,CH),(0,0,0,0)); c.paste(r,((CW-r.width)//2,(CH-r.height)//2),r); return c
def enc(name,frames,fps=30):
    d='/tmp/p11/bf_'+name; shutil.rmtree(d,ignore_errors=True); os.makedirs(d)
    for i,im in enumerate(frames): im.save(f'{d}/f{i:03d}.png')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(fps),'-i',d+'/f%03d.png','-c:v','qtrle','-pix_fmt','argb',f'/tmp/p11/{name}.mov'],check=True)
def pulse(t,amp,start):  # 0.4 s a partir de start
    u=t-start
    return 1+amp*(1-abs(u/0.2-1)) if 0<=u<0.4 else 1.0
# pílula: loop de 8 s, pulso leve nos últimos 0,4 s
enc('pill',[put(P,600*pulse(i/30,0.04,7.6),84*pulse(i/30,0.04,7.6)) for i in range(240)])
# laranja: loop de 5 s, pulso nos últimos 0,4 s (1,00->1,06->1,00)
enc('orange',[put(big,860*pulse(i/30,0.06,4.6),120*pulse(i/30,0.06,4.6)) for i in range(150)])
# transição 0,3 s: laranja cresce de 70 % a 100 % com fade-in
enc('grow',[put(big,860*(0.70+0.30*(i+1)/9),120*(0.70+0.30*(i+1)/9),alpha=min(1,(i+1)/6)) for i in range(9)])
print('ok')

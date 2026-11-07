# porta12_btn.py : botão de compra "QUERO O SOZINHO EM CASA · R$ 27" (860x120), pulso 1.00->1.06->1.00 em 0.4 s a cada 5 s. Gera btn.mov (rgba, 5 s em loop)
from PIL import Image,ImageDraw,ImageFont
import subprocess,os,shutil
F='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
W0,H0=860,120; CW,CH=920,140
b=Image.new('RGBA',(W0*2,H0*2),(0,0,0,0)); d=ImageDraw.Draw(b)
d.rounded_rectangle((0,0,W0*2-1,H0*2-1),radius=H0,fill=(255,106,0,255))
d.rounded_rectangle((6,6,W0*2-7,H0*2-7),radius=H0-6,outline=(255,190,120,255),width=5)
f=ImageFont.truetype(F,84); t='QUERO O SOZINHO EM CASA · R$ 27'
tw=d.textlength(t,font=f)
if tw>W0*2-120: f=ImageFont.truetype(F,int(84*(W0*2-120)/tw)); tw=d.textlength(t,font=f)
d.text(((W0*2-tw)/2,H0-f.size*0.62),t,font=f,fill=(255,255,255,255),stroke_width=3,stroke_fill=(120,40,0,255))
b.save('/tmp/p11/btn_full.png')
fr='/tmp/p11/btnfr'; shutil.rmtree(fr,ignore_errors=True); os.makedirs(fr)
for i in range(150):
    t=i/30; s=1+0.06*(1-abs(t/0.2-1)) if t<0.4 else 1.0
    w=int(W0*s); h=int(H0*s); im=b.resize((w,h),Image.LANCZOS)
    c=Image.new('RGBA',(CW,CH),(0,0,0,0)); c.paste(im,((CW-w)//2,(CH-h)//2),im); c.save(f'{fr}/f{i:03d}.png')
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','30','-i',fr+'/f%03d.png','-c:v','qtrle','-pix_fmt','argb','/tmp/p11/btn.mov'],check=True)
print('ok')

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math
P='/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf'
F=lambda w,s: ImageFont.truetype(P%w,s)
NAVY=(27,20,100); PINK=(255,90,138); TEAL=(46,196,182); YEL=(255,211,64); PUR=(128,98,255); CREAM=(255,244,224)
def rr(img,r):
    m=Image.new('L',img.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0)+img.size,r,fill=255); img=img.convert('RGBA'); img.putalpha(m); return img
def shadow(im,off=(0,24),blur=34,op=110):
    a=im.split()[3].point(lambda v:v*op//255); s=Image.new('RGBA',(im.width+2*blur+abs(off[0]),im.height+2*blur+abs(off[1])),(0,0,0,0))
    sh=Image.new('RGBA',im.size,(20,10,60,255)); sh.putalpha(a); s.paste(sh,(blur+off[0],blur+off[1])); s=s.filter(ImageFilter.GaussianBlur(blur/2)); return s,blur
def paste_sh(base,im,xy,**k):
    s,b=shadow(im,**k); base.alpha_composite(s,(xy[0]-b,xy[1]-b)); base.alpha_composite(im,xy)
def paw(d,cx,cy,s,col):
    d.ellipse((cx-s*.55,cy-s*.1,cx+s*.55,cy+s*.7),fill=col)
    for dx,dy,r in [(-.8,-.45,.28),(-.3,-.85,.3),(.3,-.85,.3),(.8,-.45,.28)]:
        d.ellipse((cx+dx*s-r*s,cy+dy*s-r*s,cx+dx*s+r*s,cy+dy*s+r*s),fill=col)
def logo(width=900, dark=True):
    S=2400; im=Image.new('RGBA',(S,520),(0,0,0,0)); d=ImageDraw.Draw(im)
    bs=300; d.ellipse((0,40,bs,40+bs),fill=PINK); paw(d,bs/2,40+bs*0.52,bs*0.30,(255,255,255))
    d.ellipse((bs*0.62,40+bs*0.62,bs*0.62+150,40+bs*0.62+150),fill=YEL)
    d.text((bs*0.62+75,40+bs*0.62+78),'\u2665',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',84),fill=NAVY,anchor='mm')
    f=F('Bold',230); x=bs+50; col=NAVY if dark else (255,255,255)
    d.text((x,0),'Sozinho',font=f,fill=col); w=d.textlength('Sozinho ',font=f); d.text((x+w,0),'em Casa',font=f,fill=PINK)
    d.text((x+6,300),'PROTOCOLO DE 14 DIAS  \u00b7  TUTORIAL PET',font=F('Bold',60),fill=col)
    im=im.crop(im.getbbox()); return im.resize((width,int(im.height*width/im.width)),Image.LANCZOS)
def appicon(sz=1024):
    im=Image.new('RGBA',(sz,sz),NAVY+(255,)); d=ImageDraw.Draw(im)
    d.ellipse((-sz*.25,-sz*.25,sz*.55,sz*.55),fill=PINK); d.ellipse((sz*.6,sz*.55,sz*1.3,sz*1.25),fill=TEAL); d.ellipse((sz*.68,-sz*.1,sz*1.05,sz*.27),fill=YEL)
    paw(d,sz*.5,sz*.42,sz*.2,(255,255,255))
    d.text((sz/2,sz*.74),'Sozinho',font=F('Bold',int(sz*.13)),fill=(255,255,255),anchor='mm')
    d.text((sz/2,sz*.86),'em Casa',font=F('Bold',int(sz*.13)),fill=YEL,anchor='mm')
    return rr(im,int(sz*.22))
def ebook(w=420):
    cov=Image.open('/home/claude/tutorialpet/assets/vsl/capa_vsl.png').convert('RGB')
    h=int(w*1.42); c=cov.resize((int(w*1.0),int(w*1.0)))
    b=Image.new('RGBA',(w,h),CREAM+(255,)); b.paste(c,(0,int(h*0.04)))
    d=ImageDraw.Draw(b); d.rectangle((0,0,w,int(h*0.04)),fill=NAVY); d.rectangle((0,h-int(h*.1),w,h),fill=NAVY)
    d.text((w/2,h-int(h*.05)),'E-BOOK  ·  MANUAL COMPLETO',font=F('Bold',int(w*.05)),fill=(255,255,255),anchor='mm')
    b=rr(b,16); spine=Image.new('RGBA',(26,h),(14,10,70,255)); b.alpha_composite(spine,(0,0)); b=rr(b.convert('RGB'),16)
    # light edge
    return b
def phone(w=400):
    app=Image.open('/tmp/nat/prod/app_full.png').convert('RGB'); h=int(w*1.95)
    scr=app.resize((w-30,int((w-30)*app.height/app.width))).crop((0,0,w-30,h-30))
    fr=Image.new('RGBA',(w,h),(20,16,40,255)); fr=rr(fr,48)
    s=rr(scr,34); fr.alpha_composite(s,(15,15))
    d=ImageDraw.Draw(fr); d.rounded_rectangle((w//2-50,22,w//2+50,38),8,fill=(20,16,40))
    return fr
def card(dog='/tmp/nat/prod/dog_full.png',video=False):
    W,H=1080,1920; bg=Image.new('RGBA',(W,H),CREAM+(255,)); d=ImageDraw.Draw(bg)
    d.ellipse((-300,-300,520,520),fill=PINK); d.ellipse((700,-200,1400,500),fill=TEAL)
    d.ellipse((-200,1250,380,1830),fill=PUR); d.ellipse((780,1480,1350,2050),fill=YEL)
    # dog photo panel
    ph=Image.open(dog).convert('RGB'); ph=ph.crop((0,230,720,1030)).resize((860,955),Image.LANCZOS)
    if video: ph=ph.crop((0,15,860,565))
    ph=rr(ph,60); paste_sh(bg,ph,(110,590 if video else 340))
    L=logo(800); plate=Image.new('RGBA',(L.width+90,L.height+70),CREAM+(255,)); plate=rr(plate,46); py=315 if video else 100; paste_sh(bg,plate,((W-plate.width)//2,py),off=(0,10),blur=18,op=70); bg.alpha_composite(L,((W-L.width)//2,py+35))
    eb=ebook(330 if video else 380).rotate(7,expand=True,resample=Image.BICUBIC); paste_sh(bg,eb,(70,800 if video else 880))
    pm=phone(300 if video else 340).rotate(-5,expand=True,resample=Image.BICUBIC); paste_sh(bg,pm,(660,690 if video else 860))
    # badges
    def pill(txt,xy,col,fg=(255,255,255)):
        f=F('Bold',40); w=d.textlength(txt,font=f)+70; r=Image.new('RGBA',(int(w),84),(0,0,0,0)); dd=ImageDraw.Draw(r); dd.rounded_rectangle((0,0,int(w),84),42,fill=col); dd.text((w/2,42),txt,font=f,fill=fg,anchor='mm'); paste_sh(bg,r,xy,off=(0,10),blur=14,op=90)
    if not video: pill('E-BOOK',(110,1450),NAVY); pill('APLICATIVO',(640,1450),PINK)
    t=Image.new('RGBA',(W,300),(0,0,0,0)); td=ImageDraw.Draw(t)
    td.text((W/2,60),'Manual + aplicativo',font=F('Bold',64),fill=NAVY,anchor='mm')
    td.text((W/2,150),'que ensinam seu pet a ficar tranquilo',font=F('SemiBold' if __import__('os').path.exists(P%'SemiBold') else 'Bold',44),fill=NAVY,anchor='mm')
    if not video: bg.alpha_composite(t,(0,1580))
    return bg.convert('RGB')
if __name__=='__main__':
    card().save('/tmp/nat/prod/produto_card.png'); card(video=True).save('/tmp/nat/prod/produto_card_video.png')
    logo(1400).save('/tmp/nat/prod/logo_sozinho_em_casa.png')
    appicon().save('/tmp/nat/prod/icone_app_sozinho_em_casa.png')

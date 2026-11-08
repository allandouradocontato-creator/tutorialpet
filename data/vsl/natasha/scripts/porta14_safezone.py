# porta14_safezone.py: 6 quadros com bandas vermelhas (topo 14 %, base 35 %, laterais 6 %) + thumbs 1080x1920
import json,subprocess,sys
from PIL import Image,ImageDraw
T=json.load(open('/tmp/p11/times.json')); FE=T['FE_AT']; O10=T['O10']
V='/tmp/p11/long_v.mp4'; OUT='/mnt/user-data/outputs/porta14/'
pts=[(1,'0:01'),(36,'0:36'),(110,'1:50'),(153,'2:33'),(186,'3:06'),(FE+3,'fecho')]
W,H=540,960; sh=Image.new('RGB',(W*3,H*2),'black')
for i,(t,l) in enumerate(pts):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{t:.2f}','-i',V,'-frames:v','1','-vf',f'scale={W}:{H}','/tmp/p11/fr/z.png'])
    im=Image.open('/tmp/p11/fr/z.png').convert('RGBA'); ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    red=(255,0,0,70)
    d.rectangle((0,0,W,int(H*0.14)),fill=red); d.rectangle((0,int(H*0.65),W,H),fill=red)
    d.rectangle((0,0,int(W*0.06),H),fill=red); d.rectangle((int(W*0.94),0,W,H),fill=red)
    im=Image.alpha_composite(im,ov).convert('RGB'); ImageDraw.Draw(im).text((8,int(H*0.14)+4),l,fill=(255,255,0))
    sh.paste(im,((i%3)*W,(i//3)*H))
sh.save(OUT+'porta14_safezone.jpg',quality=88)
for n,t in [(1,0.5),(2,36.5),(3,77.5)]:
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{t:.2f}','-i',V,'-frames:v','1','-q:v','2',OUT+f'porta14_thumb_{n}.jpg'])
print('ok')

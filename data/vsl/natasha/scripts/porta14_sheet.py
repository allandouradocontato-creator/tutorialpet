import json,subprocess,sys
from PIL import Image,ImageDraw
T=json.load(open('/tmp/p11/times.json')); f=sys.argv[1]; outp=sys.argv[2]
O9=T['O9'];O9b=T['O9b'];O10=T['O10'];FE=T['FE_AT']
pts=[(3,'3'),(12,'12'),(16,'16'),(24,'24'),(28,'28'),(31,'31'),(37,'37'),(45,'45'),(55,'55'),(64,'64'),(67,'67'),(75,'75'),(80,'80'),(85,'85'),(100,'100'),
(O9+3,'corredor'),(O9+10,'porta'),(O9+12,'flash'),(O9+d if (d:=T['d5']+0.2) else 0,'preto'),(O9b+1,'reveal'),(O9b+4.5,'inteira'),(O10+2,'controle'),(O10+13.9,'vira-lata'),(O10+22,'preco'),(O10+25.5,'garantia'),(FE+2,'fecho'),(0.5,'pilula'),(T['O8']+0.15,'trans'),(3.5,'3.5'),(4.5,'4.5'),(T['O8']+7,'1:57'),(O9+14,'d14+14'),(O9+15.5,'d14+15.5'),(O10+12.9,'filhote'),(O10+13.6,'idoso'),(O10+14.4,'vira-lata'),(O10+14.95,'raca1'),(O10+15.4,'raca2'),(76,'76'),(94,'94'),(98,'98'),(104,'104'),(130,'130'),(O9+2,'d14+2'),(O9+9,'d14+9'),(O9b+1,'rev+1'),(O9b+5,'rev+5'),(O9b+9,'rev+9'),(T['O8']+1,'O8+1'),(O10+5,'O10+5'),(FE+0.5,'fecho0'),(O10+T['T11'][0]+0.4,'B11'),(O10+T['T11'][1]-0.1,'B11fim'),(O10+T['T11'][1]+0.9,'De97'),(O10+27.5,'garantia2'),(1.0,'t1'),(36.5,'t36'),(0.5,'t0.5'),(77.5,'t77')]
W,H=216,384
cols=5; rows=(len(pts)+cols-1)//cols
sh=Image.new('RGB',(W*cols,H*rows),'black')
for i,(t,l) in enumerate(pts):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{t:.2f}','-i',f,'-frames:v','1','-vf',f'scale={W}:{H}','/tmp/p11/fr/x.png'])
    im=Image.open('/tmp/p11/fr/x.png').convert('RGB'); ImageDraw.Draw(im).text((6,6),f'{l} {t:.1f}s',fill=(255,255,0))
    sh.paste(im,((i%cols)*W,(i//cols)*H))
sh.save(outp,quality=85)

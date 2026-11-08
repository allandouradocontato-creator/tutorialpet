# porta15_check.py: emendas (numérico + visual), teste do estranho
import json,subprocess,numpy as np,sys
from PIL import Image,ImageDraw
O='/mnt/user-data/outputs/porta15/porta15_%s.mp4'
CAPS=json.load(open('/tmp/p11/caps.json'))
SB={'P1f':'Seu cachorro late ou destrói tudo quando você sai?','P1':'Seu cachorro late ou destrói tudo quando você sai?','P2':'A Carol quase doou o Thor. Até descobrir o Sozinho em Casa.','P3':'Catorze dias depois,','P3full':'Catorze dias depois, ela abriu a porta.','P4':'A Carol tentou de tudo pelo Thor.'}
res={}
for n in ['corte1_susto','corte2_vizinho','corte3_dicas']:
    R=json.load(open(f'/tmp/p11/c15/{n}.json'));tj=R['juncoes'];P=R['parts'];vs=R['vs'];ve=R['ve']
    y=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',O%n,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
    db=lambda a,b:float(20*np.log10(np.sqrt((y[int(a*16000):int(b*16000)]**2).mean())+1e-7))
    jumps=[round(db(t,t+0.05)-db(t-0.05,t),1) for t in tj]
    # roteiro falado
    script=[];t=0
    for i,(s,e) in enumerate(zip(vs,ve)):
        p=P[i]
        if p[0]=='B': script.append((round(t,2),'[ponte] '+SB[p[1]]))
        else:
            for ca,ce,ls in CAPS:
                if ce>s+0.3 and ca<e-0.3: script.append((round(t+max(ca,s)-s,2),' '.join(ls)))
        t+=e-s
    res[n]=dict(R=R,jumps=jumps,script=script)
    print(n,R['dur'],R['I'],R['TP'],'saltos',jumps,'margens',R['margens'])
    # contato de emendas: quadro antes/depois
    W,H=216,384;im=Image.new('RGB',(W*(2*len(tj)+1),H))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',O%n,'-frames:v','1','-vf',f'scale={W}:{H}','/tmp/p11/fr/q.png']);im.paste(Image.open('/tmp/p11/fr/q.png'),(0,0))
    for k,t in enumerate(tj):
        for j,dt in enumerate((-0.07,0.07)):
            subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{t+dt:.3f}','-i',O%n,'-frames:v','1','-vf',f'scale={W}:{H}','/tmp/p11/fr/q.png'])
            im.paste(Image.open('/tmp/p11/fr/q.png'),((1+2*k+j)*W,0))
    im.save(f'/tmp/p11/fr/j15_{n}.jpg',quality=82)
json.dump({k:dict(script=v['script'],jumps=v['jumps'],R=v['R']) for k,v in res.items()},open('/tmp/p11/c15/check.json','w'),ensure_ascii=False)

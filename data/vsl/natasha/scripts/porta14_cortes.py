# porta14_cortes.py: 3 cortes (susto, vizinho, dicas) a partir de long_nb (sem botão) + mix.wav; cortes no silêncio, acrossfade 0.15 s só no áudio, botão laranja desde 0, loudnorm -14
import subprocess,os,json,sys,numpy as np
sys.path.insert(0,'/tmp/p11'); from norm14 import normalize_mux,measure,sh
OUT=os.environ.get('OUT','/mnt/user-data/outputs/porta14'); os.makedirs('/tmp/p11/c14',exist_ok=True)
T=json.load(open('/tmp/p11/times.json')); FE=T['FE_AT']; END=T['END']; O9=T['O9']; O9b=T['O9b']; O10=T['O10']; d5=T['d5']; BL0=O9+d5; BL1=O9b
CAPS=json.load(open('/tmp/p11/caps.json'))
raw=subprocess.run(['ffmpeg','-v','error','-i','/tmp/p11/voz14.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
y=np.frombuffer(raw,np.float32);h=160;n=len(y)//h
r=np.sqrt((y[:n*h].reshape(n,h)**2).mean(1)); act=r>r.max()*10**(-40/20)
# intervalos de silêncio >= 80 ms
SIL=[];i=0
while i<n:
    if not act[i]:
        j=i
        while j<n and not act[j]: j+=1
        if (j-i)*0.01>=0.08: SIL.append((i*0.01,j*0.01))
        i=j
    else: i+=1
def near(t,tol):
    best=None
    for s,e in SIL:
        dd=0 if s<=t<=e else min(abs(t-s),abs(t-e))
        if dd<=tol and (best is None or dd<best[0]): best=(dd,s,e)
    return best
def snap_end(t):
    for tol in (0.15,0.5):
        b=near(t,tol)
        if b: break
    if not b: raise SystemExit(f'sem silencio perto de {t}')
    _,s,e=b
    x=min(t,s+0.35) if s<=t<=e and t-s>=0.08 else s+min(0.10,e-s)
    return x,s,e,b[0]
def snap_start(t):
    for tol in (0.15,0.5):
        b=near(t,tol)
        if b: break
    if not b: raise SystemExit(f'sem silencio perto de {t}')
    _,s,e=b
    x=max(t,e-0.30) if s<=t<=e and e-t>=0.08 else max(s,e-0.10)
    return x,s,e,b[0]
CUTS={'corte1_susto':[(0,11.40),(71.84,80.10),(137.30,157.50),(169.70,175.90),(184.30,FE-0.2),(FE,END)],
'corte2_vizinho':[(44.56,45.95),(50.92,54.29),(135.06,163.40),(169.70,179.30),(179.38,181.60),(184.30,FE-0.2),(FE,END)],
'corte3_dicas':[(91.34,109.40),(109.95,125.90),(131.14,134.55),(152.16,157.40),(176.20,179.30),(184.30,FE-0.2),(FE,END)]}
DROP={'corte1_susto':[(145.82,147.56)]}   # "Será que aconteceu alguma coisa?" só se passar de 59,5 s
def plan(rs):
    P=[]
    for k,(a,b) in enumerate(rs):
        if k==0 and a==0: A,sa,ea=0.0,None,None
        else: A,sa,ea,_=snap_start(a)
        if b>=END-1e-6: B,sb,eb=END,None,None
        else: B,sb,eb,_=snap_end(b)
        P.append([A,B,sa,ea,sb,eb])
    # junta partes quase contíguas (<0.12 s do original)
    M=[P[0]]
    for q in P[1:]:
        if q[0]-M[-1][1]<0.35: M[-1][1]=q[1];M[-1][4]=q[4];M[-1][5]=q[5]
        else: M.append(q)
    return M
def build(name,rs):
    P=plan(rs); tot=sum(b-a for a,b,*_ in P)
    if name in DROP and tot>59.5+0.5:   # estimativa antes do crossfade
        for (da,db) in DROP[name]:
            Q=[]
            for p in P:
                if p[0]<da<p[1]:
                    xa,xs,xe,_=snap_end(da); ya,ys,ye,_=snap_start(db)
                    Q+= [[p[0],xa,p[2],p[3],xs,xe],[ya,p[1],ys,ye,p[4],p[5]]]
                else: Q.append(p)
            P=Q
        tot=sum(b-a for a,b,*_ in P)
    # sobreposições
    D=[]
    for i in range(len(P)-1):
        m1=P[i][1]-P[i][4]; m2=P[i+1][3]-P[i+1][0]
        D.append(round(max(0.08,min(0.15,m1,m2)),3))
    vs=[];ve=[];A=[]
    for i,(a,b,*_) in enumerate(P):
        vs.append(a+(D[i-1]/2 if i>0 else 0)); ve.append(b-(D[i]/2 if i<len(D) else 0))
    vdur=sum(e-s for s,e in zip(vs,ve)); adur=tot-sum(D)
    # áudio: voz (acrossfade D, só em silêncio) + cama (música/sfx) com acrossfade longo 0,4 s centrado na junção (degraus de nível suavizados)
    sh(['ffmpeg','-y','-loglevel','error','-i','/tmp/p11/mix.wav','-i','/tmp/p11/voz14.wav','-filter_complex','[1:a]aformat=channel_layouts=mono,aeval=-val(0)|-val(0)[vi];[0:a][vi]amix=inputs=2:normalize=0:duration=first[o]','-map','[o]','-ar','44100','/tmp/p11/bed.wav']) if not os.path.exists('/tmp/p11/bed.wav') else None
    DB=0.4; fa=[]
    for i,(a,b,*_) in enumerate(P):
        h=0 if i==0 else DB/2-D[i-1]/2; t=0 if i==len(P)-1 else DB/2-D[i]/2
        fa.append(f'[0:a]aformat=channel_layouts=mono,atrim={a:.4f}:{b:.4f},asetpts=PTS-STARTPTS[a{i}]')
        fa.append(f'[1:a]atrim={a-h:.4f}:{b+t:.4f},asetpts=PTS-STARTPTS[b{i}]')
    cv=cb='';cv='a0';cb='b0'
    for i in range(len(D)):
        fa.append(f'[{cv}][a{i+1}]acrossfade=d={D[i]}:c1=tri:c2=tri[x{i}]'); cv=f'x{i}'
        fa.append(f'[{cb}][b{i+1}]acrossfade=d={DB}:c1=tri:c2=tri[y{i}]'); cb=f'y{i}'
    fa.append(f'[{cv}]aformat=channel_layouts=stereo[vv];[{cb}]aformat=channel_layouts=stereo[bb];[vv][bb]amix=inputs=2:normalize=0:duration=longest[o]')
    wav=f'/tmp/p11/c14/{name}.wav'
    sh(['ffmpeg','-y','-loglevel','error','-i','/tmp/p11/voz14.wav','-i','/tmp/p11/bed.wav','-filter_complex',';'.join(fa),'-map','[o]','-ar','44100',wav])
    # vídeo: trims de long_nb (corte seco) + botão laranja desde 0 (escondido no preto de 0,4 s, se houver)
    fv=[f'[{i}:v]setpts=PTS-STARTPTS[v{i}]' for i in range(len(vs))]
    fv.append(''.join(f'[v{i}]' for i in range(len(P)))+f'concat=n={len(P)}:v=1:a=0[c]')
    hide=''; t=0
    for (s,e) in zip(vs,ve):
        if s<BL1 and e>BL0: hide+=f"*not(between(t,{t+max(0,BL0-s):.3f},{t+min(e,BL1)-s:.3f}))"
        t+=e-s
    fv.append(f"[c][{len(vs)}:v]overlay=x=(W-w)/2:y=1100:enable='1{hide}':eof_action=pass,format=yuv420p[o]")
    vid=f'/tmp/p11/c14/{name}_v.mp4'
    inp=[]
    for s_,e_ in zip(vs,ve): inp+=['-ss',f'{s_:.4f}','-t',f'{e_-s_:.4f}','-i','/tmp/p11/long_nb.mp4']
    if not os.environ.get('REUSE'): sh(['ffmpeg','-y','-hide_banner','-loglevel','error']+inp+['-stream_loop','-1','-i','/tmp/p11/orange.mov','-filter_complex',';'.join(fv),'-map','[o]','-t',f'{adur:.3f}','-an','-r','30','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',vid])
    out=f'{OUT}/porta14_{name}.mp4'
    I,PK,tp=normalize_mux(vid,wav,out)
    sh(['ffmpeg','-y','-loglevel','error','-i',out,'-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','96k',out.replace('.mp4','_leve.mp4')])
    dv=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out],capture_output=True,text=True).stdout)
    # roteiro falado (legendas) com tempos de saída
    script=[];t=0
    for (s,e,(a,b,*_)) in zip(vs,ve,P):
        for ca,ce,ls in CAPS:
            if ce>s+0.05 and ca<e-0.05 and ca>=s-0.13: script.append((round(t+max(ca,s)-s,2),' '.join(ls)))
        t+=e-s
    rep=dict(name=name,dur=round(dv,2),I=I,TP=PK,tpalvo=tp,parts=[[round(p[0],3),round(p[1],3)] for p in P],D=D,script=script,
      margens=[[round(P[i][1]-P[i][4],3),round(P[i+1][3]-P[i+1][0],3)] for i in range(len(D))])
    json.dump(rep,open(f'/tmp/p11/c14/{name}.json','w'),ensure_ascii=False,indent=1)
    print(name,rep['dur'],I,PK,P and [[round(p[0],2),round(p[1],2)] for p in P],D,flush=True)
if __name__=='__main__':
    for nm in (sys.argv[1:] or CUTS): build(nm,CUTS[nm])

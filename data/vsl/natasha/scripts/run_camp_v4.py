import sys,re,math,glob,os
sys.path.insert(0,'/tmp/nat')
exec(open('/tmp/nat/build_vsl.py').read())
C=U+"/VSL_Sozinho_em_Casa/clipes/"; V="/tmp/nat/vsl/"
VZ=open(os.environ.get('VZFILE','/tmp/nat/vozes_v2_antigo.md'),encoding='utf-8').read()
KEYS={'C1':('C1 CULPA','VSL2'),'C2':('C2 VIZINHO','VSL3'),'C3':('C3 DICA','VSL4'),'C5':('C5 ERRO','VSL5'),'C6':('C6 IDENT','VSL6')}
AUDIO={'C1':'C1_culpa','C2':'C2_vizinho','C3':'C3_dica_solta','C5':'C5_erro_na_saida','C6':'C6_identificacao'}
SUB=[('catorze','14'),('dez minutos','10 minutos'),('dez dicas','10 dicas'),('noventa e sete por vinte e sete reais','R$ 97 por R$ 27'),('cem por cento','100%'),('dois bônus','2 bônus'),('noventa e sete por vinte e sete','R$ 97 por R$ 27'),('Dra.','Dra.')]
def body(k):
    m=re.search(r'## '+KEYS[k][0]+r'[^\n]*\n(.*?)(?=\n## |\Z)',VZ,re.S); t=m.group(1).strip().replace('Pode.De','Pode. De')
    for a,b in SUB: t=t.replace(a,b)
    return t
def chunks_of(t):
    t=t.replace('Dra. ','Dra.§'); sents=re.split(r'(?<=[.!?])\s+',t); out=[]
    for s in sents:
        if len(s)<=40: out.append(s); continue
        parts=re.split(r'(?<=[,:;])\s+',s); cur=''
        for p in parts:
            if cur and len(cur)+1+len(p)>40: out.append(cur); cur=p
            else: cur=(cur+' '+p).strip()
        if cur: out.append(cur)
    out=[o.replace('§',' ') for o in out]
    # merge tiny
    res=[]
    for c in out:
        if res and len(c)<14 and len(res[-1])+len(c)<46: res[-1]+=' '+c
        else: res.append(c)
    return res
def dogdur(f): return dur(f)
PROB=[C+x for x in ["vizinho_23_estressado_na_porta_do_apartamento_IA_HeyGen.mp4","cachorro_21_filhote_rasgando_travesseiro_penas_IA_HeyGen.mp4","cachorro_22_arranhando_porta_e_sofa_IA_HeyGen.mp4","cachorro_24_filhote_xixi_no_tapete_IA_HeyGen.mp4","cachorro_07_pulando_na_cama_bagunca.mp4","cachorro_09_sala_brinquedo_espalhado_no_chao.mp4","cachorro_11_filhote_golden_mordendo_no_tapete.mp4","cachorro_06_branco_mastigando_brinquedo_no_tapete.mp4","cachorro_12_preto_com_brinquedo_roxo.mp4"]]+[U+"/14743099_2160_2784_30fps.mp4",U+"/13308555_2160_3840_24fps.mp4"]
CALM=[C+x for x in ["cachorro_01_deitado_no_chao_esperando.mp4","cachorro_03_sentado_olhando_pra_cima.mp4","cachorro_05_poodle_no_colo.mp4","cachorro_02_olhando_porta_de_vidro.mp4","cachorro_08_inocente_olhando_pra_cima.mp4","cachorro_10_esperando_no_topo_da_escada.mp4","cachorro_04_poodle_filhote_vermelho.mp4"]]+[U+"/"+x for x in ["10814082-hd_1440_2560_25fps.mp4","5416676-uhd_2160_3840_24fps.mp4","9314158-uhd_2160_3840_25fps.mp4","10914654-hd_1080_1920_30fps.mp4","5877808-hd_1080_1920_30fps.mp4","17029743-hd_1080_1920_24fps.mp4","10726238-hd_1080_1920_30fps.mp4","12879576-hd_1080_1920_30fps.mp4","19770674-hd_1080_1920_30fps.mp4"]]
DUR={}
CL=lambda n: C+n+'.mp4'
KW=[('olha assim',['cachorro_01_deitado_no_chao_esperando']),
('chave',['cachorro_02_olhando_porta_de_vidro','cachorro_10_esperando_no_topo_da_escada']),
('coração apertado',['cachorro_08_inocente_olhando_pra_cima','cachorro_03_sentado_olhando_pra_cima']),
('culpa',['cachorro_08_inocente_olhando_pra_cima','cachorro_03_sentado_olhando_pra_cima']),
('nasce sabendo',['cachorro_03_sentado_olhando_pra_cima','cachorro_05_poodle_no_colo']),
('bilhete',['vizinho_23_estressado_na_porta_do_apartamento_IA_HeyGen']),
('late o dia',['vizinho_23_estressado_na_porta_do_apartamento_IA_HeyGen','cachorro_07_pulando_na_cama_bagunca']),
('latindo',['cachorro_07_pulando_na_cama_bagunca','cachorro_12_preto_com_brinquedo_roxo']),
('má pessoa',['cachorro_05_poodle_no_colo','cachorro_08_inocente_olhando_pra_cima']),
('maldade',['cachorro_08_inocente_olhando_pra_cima','cachorro_04_poodle_filhote_vermelho']),
('sofre sozinho',['cachorro_02_olhando_porta_de_vidro','cachorro_01_deitado_no_chao_esperando']),
('destruindo',['cachorro_21_filhote_rasgando_travesseiro_penas_IA_HeyGen','cachorro_22_arranhando_porta_e_sofa_IA_HeyGen']),
('destrói',['cachorro_21_filhote_rasgando_travesseiro_penas_IA_HeyGen','cachorro_22_arranhando_porta_e_sofa_IA_HeyGen']),
('xixi',['cachorro_24_filhote_xixi_no_tapete_IA_HeyGen']),
('chora',['cachorro_12_preto_com_brinquedo_roxo','cachorro_02_olhando_porta_de_vidro']),
('petisco',['cachorro_06_branco_mastigando_brinquedo_no_tapete','cachorro_11_filhote_golden_mordendo_no_tapete']),
('bronca',['cachorro_08_inocente_olhando_pra_cima','cachorro_03_sentado_olhando_pra_cima']),
('abraço longo',['cachorro_05_poodle_no_colo']),
('já volto',['cachorro_05_poodle_no_colo','cachorro_04_poodle_filhote_vermelho']),
('evento',['cachorro_10_esperando_no_topo_da_escada','cachorro_02_olhando_porta_de_vidro']),
('algo grave',['cachorro_10_esperando_no_topo_da_escada','cachorro_09_sala_brinquedo_espalhado_no_chao']),
('fechar a porta',['cachorro_02_olhando_porta_de_vidro','cachorro_01_deitado_no_chao_esperando']),
('sofre quando',['cachorro_02_olhando_porta_de_vidro','cachorro_01_deitado_no_chao_esperando']),
('sofrendo sozinho',['cachorro_02_olhando_porta_de_vidro','cachorro_01_deitado_no_chao_esperando']),
]
CNT={}
def slots(pool):
    out=[]; k=0
    while True:
        added=False
        for f in pool:
            d=DUR.setdefault(f,dur(f)); s=0.3+2.4*k
            if s+1.9<=d-0.1: out.append((f,s)); added=True
        if not added: break
        k+=1
    return out
def make(k):
    t=body(k); ch=chunks_of(t)+["Vem fazer seu amiguinho","ficar tranquilo, sozinho em casa!","Clique no botão agora!"]
    import os
    audio=os.environ.get("VOZ_AUDIO") or f"/home/claude/tutorialpet/data/vsl/natasha/vozes/completos/VOZ_{AUDIO[k]}_natasha_com_fecho.mp3"
    sol=next(i for i,c in enumerate(ch) if c.startswith('Em 14 dias'))
    seg,D=speech_axis(audio); T=D+0.7
    n=[len(c) for c in ch]; tot=sum(n); cum=0; tm=[]
    for c,l in zip(ch,n):
        a=map_time(seg,cum/tot); cum+=l; b=map_time(seg,cum/tot); tm.append((a,b))
    times=[(0 if i==0 else tm[i][0], tm[i+1][0] if i+1<len(tm) else T) for i in range(len(tm))]
    sp=slots(PROB) ; sc=[x for x in slots(CALM) if 'cachorro_01_' not in x[0]]
    off=['C1','C2','C3','C5','C6'].index(k)*3
    sp=sp[off%max(1,len(sp)):]+sp[:off%max(1,len(sp))]
    cuts=[]; used=set(); firstprod=False
    def fill(d,pool):
        n=max(1,math.ceil(d/1.9)); L=d/n; out=[]
        for _ in range(n):
            while pool and pool[0] in used: pool.pop(0)
            f,s=pool.pop(0); used.add((f,s)); out.append((f,round(s,2),round(L,3)))
        return out
    for i,((a,b),c) in enumerate(zip(times,ch)):
        d=b-a; items=[]
        low=c.lower()
        if c.startswith('Clique'): items=[(V+'cta.mp4',0,round(d,3))] if d<=1.85 else [(V+'cta.mp4',0,1.8)]+fill(d-1.8,sc)
        elif c.startswith('Vem fazer') or c.startswith('ficar tranquilo'):
            st=0 if c.startswith('Vem') else 1.9
            items=[(V+'produto_anim.mp4',st,round(min(d,1.9),3))]
            if d>1.9: items+=fill(d-1.9,sc)
        elif ' app ' in ' '+low+' ' and not firstprod:
            firstprod=True; m=min(d,2.6); items=[(V+'produto_anim2.mp4',0,round(m,3))]
            if d>m: items+=fill(d-m,sc)
        elif 'R$ 97' in c: m=min(d,2.5); items=[(V+'preco2.mp4',0,round(m,3))]+(fill(d-m,sc) if d>m+0.1 else [])
        elif 'devolvemos' in low: m=min(d,2.6); items=[(V+'garantia2.mp4',0,round(m,3))]+(fill(d-m,sc) if d>m+0.1 else [])
        elif 'Natasha' in c: m=min(d,1.8); items=[(V+'natasha_full.mp4',0,round(m,3))]+(fill(d-m,sp) if d>m+0.1 else [])
        else:
            hit=next((fs for kw,fs in KW if kw in low and fs),None)
            if hit:
                n=max(1,math.ceil(d/1.9)); L=d/n; items=[]
                for q in range(n):
                    f=CL(hit[q%len(hit)]); df=DUR.setdefault(f,dur(f)); c_=CNT.get(f,0); st=0.3+2.4*c_
                    if st+L>df-0.05: st=max(0,(0.3+2.4*c_)%max(0.5,df-L-0.1))
                    CNT[f]=c_+1; items.append((f,round(st,2),round(L,3)))
            else: items=fill(d,sp if i<sol else sc)
        # fix rounding to exact d
        tot_=sum(x[2] for x in items); items[-1]=(items[-1][0],items[-1][1],round(items[-1][2]+d-tot_,3))
        cuts+=items
    global TIMES_OVERRIDE; TIMES_OVERRIDE=times
    name=f"{KEYS[k][1]}_natasha_sozinho_em_casa_{AUDIO[k]}_{os.environ.get('VOZ_TAG','v2')}"
    import builtins
    build(name,audio,lambda tm_,T_:cuts,ch,"gr0za-party-party-music-569750.mp3",musvol=0.10)
if __name__=='__main__': make(sys.argv[1])

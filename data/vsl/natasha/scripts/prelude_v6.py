import sys,re,math,glob,os
exec(open('/tmp/v10/helpers_v6.py').read())
C="/mnt/user-data/uploads/VSL_Sozinho_em_Casa/clipes/"; V="/tmp/nat/vsl/"
VZ=open('/tmp/tp/data/vsl/campanhas/vozes_natasha_para_gravar.md',encoding='utf-8').read()
KEYS={'C1':('C1 CULPA','VSL2'),'C2':('C2 VIZINHO','VSL3'),'C3':('C3 DICA','VSL4'),'C5':('C5 ERRO','VSL5'),'C6':('C6 IDENT','VSL6')}
AUDIO={'C1':'C1_culpa','C2':'C2_vizinho','C3':'C3_dica_solta','C5':'C5_erro_na_saida','C6':'C6_identificacao'}
SUB=[('catorze','14'),('dez minutos','10 minutos'),('dez dicas','10 dicas'),('noventa e sete por vinte e sete reais','R$ 97 por R$ 27'),('cem por cento','100%'),('dois bônus','2 bônus'),('Dez minutos','10 minutos'),('noventa e sete por vinte e sete','R$ 97 por R$ 27'),('Dra.','Dra.')]
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
KW.append(('vizinho',['vizinho_23_estressado_na_porta_do_apartamento_IA_HeyGen']))
BAN=('cachorro_01_','cachorro_04_','cachorro_07_','vizinho_13_','vizinho_14_','vizinho_15_','10914654')
isban=lambda f: any(b in f for b in BAN)
PROB=[f for f in PROB if not isban(f)]; CALM=[f for f in CALM if not isban(f)]
KW=[(k,[x for x in fs if not isban(x)]) for k,fs in KW]
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

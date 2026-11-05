import sys; sys.path.insert(0,'/tmp/nat')
exec(open('/tmp/nat/build_vsl.py').read())
C=U+"/VSL_Sozinho_em_Casa/clipes/"; V="/tmp/nat/vsl/"
AUD="/tmp/nat/audio_v9.mp3"
APP="/home/claude/tutorialpet/assets/vsl/app_demo.mp4"
TIMES_OVERRIDE=[(0,3.8),(3.8,5.6),(5.6,9.8),(9.8,12.0),(12.0,14.4),(14.4,18.4),(18.4,21.4),(21.4,26.6),(26.6,29.1),(29.1,33.7),(33.7,36.9),(36.9,38.7),(38.7,40.55),(40.55,42.6),(42.6,44.35)]
plan=[
 [(U+"/12879576-hd_1080_1920_30fps.mp4",0,1.9),(C+"cachorro_12_preto_com_brinquedo_roxo.mp4",1.0,1.9)],
 [(C+"vizinho_23_estressado_na_porta_do_apartamento_IA_HeyGen.mp4",0.3,1.8)],
 [(C+"cachorro_21_filhote_rasgando_travesseiro_penas_IA_HeyGen.mp4",0.4,2.1),(C+"cachorro_22_arranhando_porta_e_sofa_IA_HeyGen.mp4",0.4,2.1)],
 [(C+"cachorro_08_inocente_olhando_pra_cima.mp4",0.3,1.1),(C+"cachorro_24_filhote_xixi_no_tapete_IA_HeyGen.mp4",0.4,1.1)],
 [(C+"cachorro_03_sentado_olhando_pra_cima.mp4",1.0,1.2),(U+"/5877808-hd_1080_1920_30fps.mp4",1.0,1.2)],
 [(V+"produto_anim2.mp4",0,1.3),(V+"produto_anim2.mp4",1.3,1.3),(V+"produto_anim2.mp4",2.6,1.4)],
 [(C+"cachorro_10_esperando_no_topo_da_escada.mp4",0.5,1.5),(C+"cachorro_09_sala_brinquedo_espalhado_no_chao.mp4",0.5,1.5)],
 [(V+"produto_anim.mp4",0,1.3),(V+"produto_anim.mp4",1.3,1.3),(V+"produto_anim.mp4",2.6,1.3),(V+"produto_anim2.mp4",3.9,1.3)],
 [(V+"preco2.mp4",0,2.5)],
 [(V+"garantia2.mp4",0,2.6),(C+"cachorro_11_filhote_golden_mordendo_no_tapete.mp4",1.0,2.0)],
 [(U+"/17029743-hd_1080_1920_24fps.mp4",0.5,1.6),(APP,17.0,1.6)],
 [(V+"natasha_full.mp4",0,1.8)],
 [(V+"produto_anim.mp4",0,1.85)],
 [(V+"produto_anim.mp4",1.85,1.0),(V+"produto_anim.mp4",2.85,1.05)],
 [(V+"cta.mp4",0,1.8)],
]
def cuts(times,T):
    out=[]
    for (a,b),items in zip(times,plan):
        tot=sum(d for _,_,d in items); assert abs(tot-(b-a))<0.12,(a,b,tot)
        for f,ss,dd in items: assert dd<=2.6; out.append((f,ss,dd))
    return out
build("natasha_tutorialpet_VSL_sozinho_em_casa_voz_natasha_v11_produto_14s_e_manual",AUD,cuts,
 ["Seu cachorro late, chora e destrói tudo quando você sai?","O vizinho já reclamou!","Já tentou de tudo: TV ligada, petisco, brinquedo.","Não é culpa sua. Nem dele.","Ele só nunca aprendeu a ficar sozinho.","Plano de 14 dias: um passo por dia,","poucos minutos, sem grito e sem punição!","Manual e aplicativo que ajustam o exercício ao seu cachorro.","Só R$ 27, pagamento único!","Garantia de 14 dias: não gostou, devolvemos tudo.","Toque em Comprar agora e comece o Dia 1 hoje!","Eu sou a doutora Natasha.","Vem fazer seu amiguinho","ficar tranquilo, sozinho em casa!","Clique no botão agora!"],
 "gr0za-party-party-music-569750.mp3",musvol=0.10)

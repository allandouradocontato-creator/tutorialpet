exec(open('/tmp/v10/prelude_v6.py').read()); O="/mnt/user-data/outputs/v16"
import json
PAD=0.4; XF=0.35; FPS=30; XFS=[0.35,0.12,0.35]; XA=[0.35,0.30,0.35]
AB=U+"/natasha_avatar_teste_01_oi_eu_sou_a_doutora.mp4"
FE=U+"/natasha_avatar_fecho_01_eu_sou_a_doutora_vem_fazer.mp4"; FE_SS=1.78
MUS=U+"/gr0za-party-party-music-569750.mp3"
def norm(inp,out,pre=None,ss=None,t=None,tail=None):
    """loudnorm 2 passes -> -16 LUFS TP -1.5, mono->stereo 44.1k, PAD s de silencio no inicio e fim"""
    opt=(f"-ss {ss} " if ss else "")+(f"-t {t} " if t else "")
    r=subprocess.run(f'ffmpeg -hide_banner -nostats {opt}-i "{inp}" -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null -',shell=True,capture_output=True,text=True).stderr
    j=json.loads(r[r.rindex('{'):r.rindex('}')+1])
    ln=f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true"
    sh(f'ffmpeg -v error -y {opt}-i "{inp}" -af "aresample=44100,{ln},aresample=44100,adelay={int(PAD*1000)}:all=1,apad=pad_dur={tail if tail else PAD}" -ac 2 "{out}"')
    return dur(out)
def cap_filters(caps,y_center,base,k0,inp,fc,tag,size=76):
    last=base
    for j,(c,a,b) in enumerate(caps):
        p=f"{tag}_c{j}.png"; H=caption_png(c,p,size); inp.append(f'-i {p}'); ii=k0+j
        fc.append(f'[{last}][{ii}:v]overlay=40:{int(y_center-H/2)}:enable=\'between(t,{a:.2f},{b:.2f})\'[c{j}]'); last=f'c{j}'
    return last
def render_scenes(cuts,L,caps,tag):
    if os.environ.get('REUSE') and os.path.exists(f'{tag}.mp4'): return f'{tag}.mp4'
    inp=[];fc=[]
    for (f,ss,dd) in cuts: inp.append(f'-ss {ss} -t {dd} -i "{f}"')
    for i,(f,ss,dd) in enumerate(cuts):
        fc.append(f'[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps={FPS},setsar=1,trim=duration={dd},setpts=PTS-STARTPTS[v{i}]')
    fc.append(''.join(f'[v{i}]' for i in range(len(cuts)))+f'concat=n={len(cuts)}:v=1:a=0[bg]')
    last=cap_filters(caps,1380,'bg',len(cuts),inp,fc,tag)
    out=f"{tag}.mp4"
    sh(f'ffmpeg -v error -y {" ".join(inp)} -filter_complex "{";".join(fc)}" -map "[{last}]" -t {L:.3f} -r {FPS} -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p "{out}"')
    return out
def avatar_clip(src,a,b,c,d,L_lead,L_tail,fecho,tag,caps,cap_y,cap_size,panel=False):
    """Natasha: lead = pausa natural a..b em câmera lenta até L_lead; main b..c; tail = c..d em câmera lenta até L_tail. Sem reverse."""
    top=240; keep=(1180-top) if fecho else (1920-top)
    def slow(x0,x1,L,lab):
        return (f"[a_{lab}]trim={x0}:{x1},setpts=(PTS-STARTPTS)*{L/(x1-x0):.4f},minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1,"
                f"fps=30,trim=0:{L},setpts=PTS-STARTPTS[s_{lab}]")
    f=(f"[0:v]crop=608:1080:236:420,scale=1080:1920,setsar=1,split=3[a_l][a_m][a_t];"
       + slow(a,b,L_lead,'l')+";"
       + f"[a_m]trim={b}:{c},setpts=PTS-STARTPTS,fps=30[s_m];"
       + slow(c,d,L_tail,'t')+";"
       + "[s_l][s_m][s_t]concat=n=3:v=1:a=0[p];[p]split[p1][p2];"
       + f"[p1]crop=1080:2:0:0,scale=1080:{top},boxblur=18[ex];[p2]crop=1080:{keep}:0:0[mn];[ex][mn]vstack[av]")
    L=L_lead+(c-b)+L_tail
    inp=[f'-i "{src}"']; fcl=[f]; base='av'
    if fecho:
        inp.append(f'-loop 1 -i {W}/painel_fecho.png'); 
        fcl.append(f'color=c=0xFCF3DE:s=1080x1920:r=30:d={L:.3f}[cr];[cr][av]overlay=0:0:shortest=1[avc]')
        fcl.append(f'[1:v]format=rgba,fade=t=in:st=0.65:d=0.3:alpha=1[pn];[avc][pn]overlay=0:1180:shortest=1[bgf]'); base='bgf'
    last=cap_filters(caps,cap_y,base,len(inp),inp,fcl,tag,cap_size)
    out=f"{tag}.mp4"
    sh(f'ffmpeg -v error -y {" ".join(inp)} -filter_complex "{";".join(fcl)}" -map "[{last}]" -t {L:.3f} -r {FPS} -c:v libx264 -preset veryfast -crf 16 -pix_fmt yuv420p "{out}"')
    return out,L
def render_abertura(caps,tag):
    return avatar_clip(AB,0,0.11,2.21,2.48,PAD,0.22,False,tag,caps,1560,76)
def render_fecho(caps,tag):
    return avatar_clip(FE,1.59,1.86,7.00,7.28,PAD,0.7,True,tag,caps,1040,56)
def split_text(k):
    t=body(k); i=t.index('[AVATAR'); j=t.index(']',i)
    return t[:i].strip(), t[j+1:].strip()
def times_for(ch,audio,off):
    seg,D=speech_axis(audio); n=[len(c) for c in ch]; tot=sum(n); cum=0; tm=[]
    for c,l in zip(ch,n):
        a=map_time(seg,cum/tot); cum+=l; b=map_time(seg,cum/tot); tm.append((a+off,b+off))
    return [(0 if i==0 else tm[i][0], tm[i+1][0] if i+1<len(tm) else None) for i in range(len(tm))],D,seg
BAN=BAN+('10814082','5416676','9314158','14743099','13308555','17029743','12879576','19770674','5877808','10726238','cachorro_30_','cachorro_31_','cachorro_34_','chave_49_')  # cenas vazias/ar livre fora do problema
def CP(n): return C+n+'.mp4'
_OK=[CP(x) for x in ['cachorro_32_barriga_pra_cima_feliz_pexels','cachorro_33_branco_brincando_com_osso_pexels','cachorro_35_feliz_recebendo_carinho_pexels','cachorro_40_dorme_no_sofa_com_tutor_pexels','cachorro_42_golden_dormindo_no_sofa_pexels','cachorro_44_dorme_de_barriga_pra_cima_pexels','cachorro_45_tutora_notebook_com_cachorro_pexels','cachorro_46_comendo_no_pote_pexels','cachorro_47_tutora_computador_cachorro_ao_lado_pexels','cachorro_48_tutora_abracando_no_chao_pexels','cachorro_50_correndo_no_corredor_pexels','cachorro_54_dorme_no_sofa_close_pexels','cachorro_55_brincando_na_sala_pexels','cachorro_11_filhote_golden_mordendo_no_tapete','cachorro_12_preto_com_brinquedo_roxo','cachorro_06_branco_mastigando_brinquedo_no_tapete','cachorro_05_poodle_no_colo']]
CALM=_OK
_E=lambda *n:[x for x in n]
KW=[('ensina seu cachorro',['cachorro_32_barriga_pra_cima_feliz_pexels','cachorro_42_golden_dormindo_no_sofa_pexels','cachorro_40_dorme_no_sofa_com_tutor_pexels']),
('10 minutos',['cachorro_45_tutora_notebook_com_cachorro_pexels','cachorro_35_feliz_recebendo_carinho_pexels']),
('fica tranquilo',['cachorro_44_dorme_de_barriga_pra_cima_pexels','cachorro_54_dorme_no_sofa_close_pexels','cachorro_42_golden_dormindo_no_sofa_pexels']),
('fica em paz',['cachorro_44_dorme_de_barriga_pra_cima_pexels','cachorro_54_dorme_no_sofa_close_pexels','cachorro_42_golden_dormindo_no_sofa_pexels']),
('pega a chave',['cachorro_43_espiando_porta_de_vidro_pexels','cachorro_32_barriga_pra_cima_feliz_pexels']),
('trabalha sem ligar',['cachorro_47_tutora_computador_cachorro_ao_lado_pexels','cachorro_45_tutora_notebook_com_cachorro_pexels']),
('volta e encontra',['cachorro_50_correndo_no_corredor_pexels','cachorro_55_brincando_na_sala_pexels']),
('relaxa enquanto',['cachorro_42_golden_dormindo_no_sofa_pexels','cachorro_44_dorme_de_barriga_pra_cima_pexels','cachorro_54_dorme_no_sofa_close_pexels']),
('come direito',['cachorro_46_comendo_no_pote_pexels']),
('coração não dispara',['cachorro_52_dois_na_janela_pexels','cachorro_08_inocente_olhando_pra_cima']),
('cachorro calmo é',['cachorro_48_tutora_abracando_no_chao_pexels','cachorro_32_barriga_pra_cima_feliz_pexels']),
('silêncio no corredor',['cachorro_54_dorme_no_sofa_close_pexels','cachorro_42_golden_dormindo_no_sofa_pexels','cachorro_40_dorme_no_sofa_com_tutor_pexels']),
('nenhum bilhete',['vizinho_23_estressado_na_porta_do_apartamento_IA_HeyGen']),
('cruza com o vizinho',['cachorro_55_brincando_na_sala_pexels','cachorro_48_tutora_abracando_no_chao_pexels','cachorro_35_feliz_recebendo_carinho_pexels']),
('latir o dia inteiro',['cachorro_52_dois_na_janela_pexels','cachorro_22_arranhando_porta_e_sofa_IA_HeyGen']),
('cansaço e coração',['cachorro_08_inocente_olhando_pra_cima','cachorro_41_amarelo_olhando_pra_cima_pexels']),
('um cachorro em paz',['cachorro_44_dorme_de_barriga_pra_cima_pexels','cachorro_42_golden_dormindo_no_sofa_pexels']),
('descansa e envelhece',['cachorro_48_tutora_abracando_no_chao_pexels','cachorro_40_dorme_no_sofa_com_tutor_pexels']),
('2 bônus',['cachorro_55_brincando_na_sala_pexels','cachorro_33_branco_brincando_com_osso_pexels']),
('seu para sempre',['cachorro_48_tutora_abracando_no_chao_pexels'])]
def make6(k):
    prob_t,corpo_t=split_text(k); tag0=f"c{k[1]}"
    tvoz={'C1':'c1_culpa','C2':'c2_vizinho'}[k]
    vp=f"/mnt/user-data/uploads/VSL_Sozinho_em_Casa/vozes_v6/vsl_{tvoz}_voz_v8_problema.mp3"; vb=f"/mnt/user-data/uploads/VSL_Sozinho_em_Casa/vozes_v6/vsl_{tvoz}_voz_{'v7' if k=='C2' else 'v9'}_corpo.mp3"
    # ---- áudio por bloco, cada um a -16 LUFS
    Wk=f"{W}/{k}"
    Lp=norm(vp,Wk+"_a_prob.wav"); Lb=norm(vb,Wk+"_a_corpo.wav")
    La=norm(AB,Wk+"_a_aber.wav",ss=0.11,t=2.10,tail=0.4)
    Lf=norm(FE,Wk+"_a_fecho.wav",ss=1.86,t=5.14,tail=0.7)
    # ---- bloco 1: problema
    DUR.clear()
    if k=='C1': _pool=[CP(x) for x in ['cachorro_50_correndo_no_corredor_pexels','cachorro_43_espiando_porta_de_vidro_pexels','cachorro_41_amarelo_olhando_pra_cima_pexels','cachorro_08_inocente_olhando_pra_cima','cachorro_02_olhando_porta_de_vidro']]
    else: _pool=[CP(x) for x in ['cachorro_31_branco_latindo_no_portao_pexels','cachorro_30_latindo_brincando_na_grama_pexels','cachorro_21_filhote_rasgando_travesseiro_penas_IA_HeyGen','cachorro_22_arranhando_porta_e_sofa_IA_HeyGen','cachorro_52_dois_na_janela_pexels']]
    sp=slots(_pool); off=0
    used=set(); 
    def fill(d,pool):
        n=max(1,math.ceil(d/1.5)); L=d/n; out=[]
        for _ in range(n):
            while pool and pool[0] in used: pool.pop(0)
            f,s=pool.pop(0); used.add((f,s)); out.append((f,round(s,2),round(L,3)))
        return out
    cuts=fill(Lp,sp)
    cuts[-1]=(cuts[-1][0],cuts[-1][1],round(cuts[-1][2]+Lp-sum(c[2] for c in cuts),3))
    _,Dp,_=times_for([prob_t],vp,PAD)
    PQ={'C1':["Seu cachorro sofre toda vez que você sai de casa,","e você sai com o coração apertado?"],'C2':["Seu cachorro passa o dia inteiro latindo, estressado,","quando você sai?"]}[k]
    _tp,_,_=times_for(PQ,vp,PAD); _cut=_tp[1][0]
    b1=render_scenes(cuts,Lp,[(PQ[0],0.0,_cut),(PQ[1],_cut,Lp-0.45)],Wk+"_b1")
    # ---- bloco 2: abertura
    b2,L2=render_abertura([("Oi! Eu sou a doutora Natasha.",PAD+0.05,PAD+2.1)],Wk+"_b2")
    # ---- bloco 3: corpo
    ch=chunks_of(corpo_t); seg,Db=speech_axis(vb)
    n=[len(c) for c in ch]; tot=sum(n); cum=0; tm=[]
    for c,l in zip(ch,n):
        a=map_time(seg,cum/tot); cum+=l; b=map_time(seg,cum/tot); tm.append((a+PAD,b+PAD))
    times=[(0 if i==0 else tm[i][0], tm[i+1][0] if i+1<len(tm) else Lb) for i in range(len(tm))]
    sc=[x for x in slots(CALM) if 'cachorro_01_' not in x[0]]
    PA=dur('/tmp/v16/produto_anim_v16.mp4'); CARD=[('/tmp/v16/produto_anim2_v16.mp4',5.2),('/tmp/v16/produto_anim_v16.mp4',PA)]; cs={'i':0,'o':0.0}; st_={'prod':0,'done':0,'leva':0}
    def card_slice(d,reset=False):
        if reset: cs['i']=0; cs['o']=0.0
        out=[]; rem=d
        while rem>0.01:
            f,fd=CARD[cs['i']%len(CARD)]; take=min(rem,fd-cs['o'])
            out.append((f,round(cs['o'],2),round(take,3))); rem-=take; cs['o']+=take
            if cs['o']>=fd-0.01: cs['i']+=1; cs['o']=0.0
        return out
    cuts=[]; firstprod=False; CNT.clear()
    TM={}
    for i,((a,b),c) in enumerate(zip(times,ch)):
        d=b-a; low=c.lower(); TM[c[:8]]=a
        if c.startswith('E esse é o Sozinho'): st_['prod']=1; items=card_slice(d,True)
        elif st_['prod'] and not st_['done']:
            items=card_slice(d)
            if c.endswith('com calma.'): st_['done']=1
        elif c.startswith('Você leva'): st_['leva']=1; items=card_slice(d,True)
        elif st_['leva'] and ' app ' in ' '+low+' ': st_['leva']=0; items=card_slice(d)
        elif ' app ' in ' '+low+' ' and not firstprod:
            firstprod=True; m=min(d,2.6); items=[('/tmp/v16/produto_anim2_v16.mp4',0,round(m,3))]
            if d>m: items+=fill(d-m,sc)
        elif (k=='C1' and c.startswith('Cachorro calmo')) or (k=='C2' and c.startswith('descansa e envelhece')):
            items=[('/tmp/v16/prova_v16.mp4',0,round(min(d,3.0),3))]
        elif 'R$ 97' in c: m=min(d,2.5); items=[('/tmp/v16/preco_v16.mp4',0,round(m,3))]+(fill(d-m,sc) if d>m+0.1 else [])
        elif 'devolvemos' in low: m=min(d,4.1); items=[('/tmp/v16/garantia_v16.mp4',0,round(m,3))]
        else:
            hit=next((fs for kw,fs in KW if kw in low and fs),None)
            if hit:
                nn=max(1,math.ceil(d/1.5)); Lq=d/nn; items=[]
                for q in range(nn):
                    f=CL(hit[q%len(hit)]); df=DUR.setdefault(f,dur(f)); c_=CNT.get(f,0); st=0.3+2.4*c_
                    if st+Lq>df-0.05: st=max(0,(0.3+2.4*c_)%max(0.5,df-Lq-0.1))
                    CNT[f]=c_+1; items.append((f,round(st,2),round(Lq,3)))
            else: items=fill(d,sc)
        tt=sum(x[2] for x in items); items[-1]=(items[-1][0],items[-1][1],round(items[-1][2]+d-tt,3))
        cuts+=items
    assert not [f for f,_,_ in cuts if isban(f)]
    caps=[(c,times[i][0],times[i][1]-(0.45 if i==len(ch)-1 else 0)) for i,c in enumerate(ch)]
    b3=render_scenes(cuts,Lb,caps,Wk+"_b3")
    # ---- bloco 4: fecho
    fseg,_=speech_axis(Wk+"_a_fecho.wav")
    fch=["Vem fazer seu amiguinho ficar tranquilo, sozinho em casa!","Clique no botão agora!"]
    tms,_,_=times_for(fch,Wk+"_a_fecho.wav",0)
    fcaps=[]; 
    for i,c in enumerate(fch):
        a=tms[i][0] if i else fseg[0][0]; b=tms[i][1] if tms[i][1] is not None else fseg[-1][1]+0.15
        fcaps.append((c,a,b))
    b4,L4=render_fecho(fcaps,Wk+"_b4")
    # ---- união: vídeo xfade, voz acrossfade (nos silêncios), música contínua
    Ls=[Lp,L2,Lb,L4]; blocks=[b1,b2,b3,b4]; wavs=[Wk+x for x in ["_a_prob.wav","_a_aber.wav","_a_corpo.wav","_a_fecho.wav"]]
    inp=[f'-i "{b}"' for b in blocks]+[f'-i "{w}"' for w in wavs]+[f'-ss 8 -stream_loop -1 -i "{MUS}"']
    fc=[]; acc=Ls[0]; prev='0:v'
    for i in range(1,4):
        X_=XFS[i-1]; off_=acc-X_; fc.append(f'[{prev}][{i}:v]xfade=transition=fade:duration={X_}:offset={off_:.3f}[x{i}]'); prev=f'x{i}'; acc+=Ls[i]-X_
    T=acc
    pa='4:a'
    for i in range(1,4):
        fc.append(f'[{pa}][{4+i}:a]acrossfade=d={XA[i-1]}:c1=tri:c2=tri[y{i}]'); pa=f'y{i}'
    # identidade: círculo + pílula + CRMV + barra de preço, 100% do vídeo
    label_png(["Dra. Natasha Braga · CRMV 6174"],f"{W}/lab.png")
    barp=f"{W}/bar.png"; _f=ImageFont.truetype(FONT,38); _t="Sozinho em Casa · manual + app · R$ 27"; _w=int(_f.getlength(_t))+60
    _im=Image.new("RGBA",(_w,84),(0,0,0,0)); _d=ImageDraw.Draw(_im); _d.rounded_rectangle((0,0,_w-1,83),radius=22,fill=(232,93,4,235)); _d.text((30,17),_t,font=_f,fill=(255,255,255,255)); _im.save(barp)
    FS=sum(Ls[:3])-sum(XFS)+0.25
    s3=Ls[0]-XFS[0]+Ls[1]-XFS[1]; s4=s3+Lb-XFS[2]
    wins=[(s3+0.8,s3+5.8),(s3+TM['Pra ele:'],s3+TM['Pra ele:']+4.0),(s3+TM['De R$ 97'],s3+TM['De R$ 97']+4.0),(s4+0.7,T-0.5)]
    WIN='+'.join(f'between(t,{a:.2f},{b:.2f})' for a,b in wins)
    base=9
    inp+= [f'-i {W}/circulo.png',f'-i {W}/pilula.png',f'-i {W}/lab.png',f'-i {barp}','-loop 1 -i /tmp/v16/btn_a.png','-loop 1 -i /tmp/v16/btn_b.png']
    ib=base+4
    BTN=(f"[{ib}:v]scale=960:-1[ba];[{ib+1}:v]scale=960:-1[bb];[o4][ba]overlay=60:1584:enable='({WIN})*lt(mod(t,0.6),0.3)'[o4a];[o4a][bb]overlay=60:1584:enable='({WIN})*gte(mod(t,0.6),0.3)'[o5];")
    fc.append(f'[{prev}][{base}:v]overlay=50:150[o1];[{base+1}:v]scale=300:-1[pl];[o1][pl]overlay=290:165[o2];[o2][{base+2}:v]overlay=290:253[o3];[o3][{base+3}:v]overlay=(W-w)/2:1780:enable=\'lt(t,{FS:.2f})\'[o4];{BTN}[o5]format=yuv420p,fade=t=out:st={T-0.4:.2f}:d=0.4[vout]')
    fc.append(f'[{pa}]apad=whole_dur={T}[vo];[8:a]anull[x]' if False else f'[{pa}]apad=whole_dur={T}[vo]')
    fc.append(f'[{4+4}:a]volume=0.22,atrim=0:{T:.2f},afade=t=out:st={T-0.8:.2f}:d=0.8[mu];[vo][mu]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[aout]')
    name=f"vsl_{ {'C1':'c1_culpa','C2':'c2_vizinho'}[k] }_B_v16_natasha"
    full=f'{O}/{name}_1080.mp4'; light=f'{O}/{name}_LEVE.mp4'
    sh(f'ffmpeg -v error -y {" ".join(inp)} -filter_complex "{";".join(fc)}" -map "[vout]" -map "[aout]" -t {T:.2f} -r {FPS} -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 160k -movflags +faststart "{full}"')
    sh(f'ffmpeg -v error -y -i "{full}" -vf scale=540:960 -c:v libx264 -preset veryfast -crf 26 -c:a aac -b:a 96k -movflags +faststart "{light}"')
    json.dump({'T':T,'blocks':Ls,'caps':[(c,round(a,2),round(b,2)) for c,a,b in caps],'fcaps':fcaps,'cuts':[(os.path.basename(f),s,d) for f,s,d in cuts]},open(f'{W}/{k}_info.json','w'),ensure_ascii=False,indent=1)
    print(k,'T=',round(T,2),'blocos',[round(x,2) for x in Ls],os.path.getsize(full)//1024,os.path.getsize(light)//1024,'KB')
if __name__=='__main__': make6(sys.argv[1])

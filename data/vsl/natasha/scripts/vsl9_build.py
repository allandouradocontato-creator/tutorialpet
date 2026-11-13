"""VSL9 "E se fosse você?" — montagem 1080x1920 30fps (voz Dra. Natasha clonada, SEM musica de fundo).
Regra 73: so cenas novas (geradas p/ VSL9 no Gemini/Flow ou bancos livres); nenhuma cena da VSL8.
Uso: python3 vsl9_build.py   (le /home/claude/vsl9/*, escreve /home/claude/vsl9/out/*)
"""
import subprocess, json, os, sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
B='/home/claude/vsl9'; W=B+'/work'; O=B+'/out'; V=B+'/voz'; G=B+'/gen'
U='/mnt/user-data/uploads/Downloads'
os.makedirs(W,exist_ok=True); os.makedirs(O,exist_ok=True)
CARDS='/home/claude/tutorialpet/data/vsl/natasha/cards_v16'
SC='/home/claude/tutorialpet/data/vsl/natasha/scripts'
SF='/home/claude/tutorialpet/data/vsl/natasha/sfx'
CAR='/home/claude/tutorialpet/assets/carimbo_tutorialpet.png'
V8W='/home/claude/vsl8/work'   # so cartoes de marca (preco/garantia) e selo da Dra.: nao sao cenas
FONT="/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
def sh(c):
    r=subprocess.run(c,shell=True,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-2500:]); raise SystemExit(1)
    return r.stdout
dur=lambda p: float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{p}"').strip())
GAP=0.10
D1,D2,D3=[dur(f'{V}/vsl9_voz_natasha_{k}.mp3') for k in ('F01-F06','F07-F09','F10-F11')]
B1=0.0; B2=D1+GAP; B3=B2+D2+GAP
NT0=B3+6.72; NL=6.72   # fecho: Dra. Natasha falando (clipe HeyGen da VSL8, com audio proprio; fala comeca 0.26s -> corto 0.12s)
T=round(NT0+NL,3)
print('B2',B2,'B3',B3,'NT0',NT0,'T',T)
# ---------------- fontes de cena (todas novas) ----------------
F=dict(
 cam=G+'/g1_cam_sofa_rasgando.mp4', porta=G+'/g2_porta_choro.mp4', panico=G+'/g3_cam_panico_porta.mp4',
 chao=G+'/g4_homem_chao_bagunca.mp4', treino=G+'/g5b_mulher_labrador_feliz.mp4',
 rec_feliz=G+'/g6_rec_caramelo_dorme_acorda_feliz.mp4', filhote=G+'/px_filhote_feliz_bola.mp4', golden=G+'/px_golden_feliz_lingua.mp4',
 vira=G+'/px_cachorro_sorrindo_b.mp4', raca=G+'/px_cachorro_sorrindo_a.mp4',
 lab=U+'/14743099_2160_2784_30fps (1).mp4', homem=G+'/px_vizinho_incomodado_celular.mp4',
 mulher=U+'/6024827-hd_1080_1920_30fps.mp4', beagle=U+'/12127169_2160_3840_30fps.mp4',
 idoso=U+'/15089094_2160_3840_24fps.mp4', felpudo=U+'/7279139-uhd_2160_3840_24fps (1).mp4')
SEGS=[]
def seg(name,src,t0,t1,ss=0.0,z=0.0,fx=0.5,fy=0.5,pp=False,extra=''):
    """segmento global t0..t1 (s); ss = inicio no clipe; z = zoom final (0.12 = +12%); fx,fy = foco do corte"""
    d=t1-t0; out=f'{W}/s_{name}.mp4'
    sp=f'{W}/sp_{name}.mp4'
    inp=F[src]
    if pp: # ping-pong p/ clipes curtos
        sh(f'ffmpeg -v error -y -i "{inp}" -filter_complex "[0:v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0,loop=loop=3:size=400" -an {sp}'); inp=sp; ss=0
    vf=(f"scale=w='2*ceil(max(1080/iw,1920/ih)*iw*(1+{z}*t/{d:.3f})/2+0.01)':h=-2:eval=frame,"
        f"crop=1080:1920:'(iw-1080)*{fx}':'(ih-1920)*{fy}',tpad=stop_mode=clone:stop_duration=1,fps=30,format=yuv420p{extra}")
    sh(f'ffmpeg -v error -y -ss {ss} -t {d+0.05:.3f} -i "{inp}" -an -vf "{vf}" -t {d:.3f} -c:v libx264 -preset veryfast -crf 18 {out}')
    SEGS.append((t0,out)); return out
def split(name,t0,t1,top,bot):
    d=t1-t0; out=f'{W}/s_{name}.mp4'
    (s1,ss1,fy1),(s2,ss2,fy2)=top,bot
    prep=[]
    for k,(s,ss,fy,pp) in enumerate(((s1,ss1,fy1,False),(s2,ss2,fy2,True))):
        inp=F[s]; sp=f'{W}/sp_{name}{k}.mp4'
        if pp:
            sh(f'ffmpeg -v error -y -i "{inp}" -filter_complex "[0:v]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0,loop=loop=3:size=400" -an {sp}'); inp=sp; ss=0
        pv=f'{W}/sp_{name}{k}_c.mp4'
        sh(f'ffmpeg -v error -y -ss {ss} -t {d+0.05:.3f} -i "{inp}" -an -vf "scale=1080:-2,crop=1080:960:0:(ih-960)*{fy},fps=30,format=yuv420p" -t {d:.3f} -c:v libx264 -preset veryfast -crf 18 {pv}')
        prep.append(pv)
    sh(f'ffmpeg -v error -y -i {prep[0]} -i {prep[1]} -filter_complex "[0:v][1:v]vstack=2,drawbox=y=954:w=1080:h=12:color=white@1:t=fill[o]" -map "[o]" -c:v libx264 -preset veryfast -crf 18 {out}')
    SEGS.append((t0,out))
if __name__=='__main__':
    # ---------- F1..F6 (bloco 1) ----------
    seg('f1','cam',0.0,4.5,ss=0.3,z=0.10,fx=0.4,fy=0.5)                 # F1 camera REC: cachorro destruindo o sofa
    seg('f2a','porta',4.5,6.4,ss=0.0,fx=0.5)                             # F2 pessoa sai, porta fecha
    seg('f2b','porta',6.4,8.5,ss=4.0,z=0.10,fx=0.55)                     # F2 cachorro chora/arranha a porta
    seg('f3a','cam',8.5,11.0,ss=6.5,z=0.08,fx=0.45)                      # F3 sofa ja era
    seg('f3b','lab',11.0,14.15,ss=0.0,z=0.06,fx=0.25)                    # F3 outro cachorro latindo
    split('f4',14.15,17.0,('homem',0.0,0.1),('mulher',0.0,0.65))        # F4 tela dividida: vizinho em casa / pessoa no trabalho
    seg('f5','chao',17.0,22.6,ss=0.4,z=0.12,fx=0.5,fy=0.4)               # F5 pessoa no chao, mao na cabeca
    seg('f6','panico',22.6,B2,ss=0.4,z=0.55,fx=0.45,fy=0.55)             # F6 zoom da camera no cachorro em panico
    # ---------- F7..F9 (bloco 2) ----------
    seg('f7','treino',B2,B2+8.37,ss=0.0,z=0.05)                          # F7 pessoa treinando com o celular (+ card do produto)
    t=B2+8.37
    seg('f8a','filhote',t,B2+9.2,ss=1.0,z=0.06,fx=0.5,fy=0.75)          # F8 filhote (feliz, brincando)
    seg('f8b','golden',B2+9.2,B2+9.9,ss=1.5,z=0.05,fy=0.5)               # F8 idoso (golden de focinho claro, lingua de fora)
    seg('f8c','vira',B2+9.9,B2+10.7,ss=1.0,z=0.05,fx=0.5,fy=0.5)         # F8 vira-lata (branco, lingua de fora)
    seg('f8d','raca',B2+10.7,B2+11.7,ss=0.3,z=0.05,fx=0.5,fy=0.45)       # F8 de raca (sorrindo)
    seg('f9a','rec_feliz',B2+11.7,B3,ss=2.9,z=0.0)                       # F9 camera: dorme tranquilo e acorda FELIZ (boca aberta, rabo balancando)
    # ---------- F10..F11 (bloco 3) ----------
    seg('f10','treino',B3,NT0,ss=0.5,z=0.10)                             # fundo p/ cards de preco/garantia (escurecido depois) - labradora feliz
    # F11: Natasha (natasha_full.mp4 em loop com zoom suave)
    sh(f'ffmpeg -v error -y -ss 0.16 -t {NL:.3f} -i /home/claude/vsl8/work/nat_pres.mp4 -an -vf "tpad=stop_mode=clone:stop_duration=1,fps=30,format=yuv420p" -t {NL:.3f} -c:v libx264 -preset veryfast -crf 18 {W}/s_f11.mp4')
    SEGS.append((NT0,W+'/s_f11.mp4'))
    # concat
    SEGS.sort()
    open(W+'/list.txt','w').write(''.join(f"file '{p}'\n" for _,p in SEGS))
    sh(f'ffmpeg -v error -y -f concat -safe 0 -i {W}/list.txt -c:v libx264 -preset veryfast -crf 18 -r 30 {W}/base.mp4')
    print('base ok',dur(W+'/base.mp4'))
    json.dump(dict(B2=B2,B3=B3,T=T,NT0=NT0),open(W+'/meta.json','w'))

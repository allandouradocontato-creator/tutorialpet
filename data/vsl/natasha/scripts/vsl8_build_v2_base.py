"""VSL8 'A Câmera' v2 - monta o vídeo-base (sem legendas/overlays) na linha do tempo de SAÍDA.
Pausa C3 de 0,7 s inserida no silêncio da voz (6,14-6,48 s): tudo depois de 6,31 s desloca +0,7 s.
Cenas novas (Gemini/Flow) de 0 a 20,0 s; de 20,0 s em diante reaproveita os cortes v1 já renderizados (seg_016..seg_041 + prod.mp4).
"""
import subprocess, json, sys, os
B='/home/claude/vsl8'; G=B+'/gem'; C=B+'/clips'; W=B+'/work'; O=B+'/out'
N4B=G+'/N4b_camera_sofa_gemini.mp4'
N4=G+'/N4_camera_sofa_gemini.mp4'
HAS4B=os.path.exists(N4B)
print('N4b existe:',HAS4B)
def sh(c):
    r=subprocess.run(c,shell=True,capture_output=True,text=True)
    if r.returncode: print(r.stderr[-2500:]); raise SystemExit(1)
    return r.stdout
J=json.load(open(O+'/vsl8_cortes.json')); PA=0.7
T2=J['T']+PA
src={'N1':G+'/N1_thor_porta_gemini.mp4','N2':G+'/N2_thor_latindo_sozinho_flow.mp4','N3':G+'/N3_vizinho_casa_gemini_5s_a_10s_celular_mao_direita.mp4',
     'N4':N4,'N4B':(N4B if HAS4B else N4),'N5':G+'/N5_carol_escritorio_gemini.mp4','N6':G+'/N6_carol_corre_gemini.mp4','F2':C+'/vsl8_F2_despedida_festa.mp4'}
# (a,b,fonte,ss,zoom)  tempos de saída
plan=[(0,1.4,'N4',2.0,1.0),(1.4,2.19,'N1',0.2,1.0),(2.19,2.98,'N1',1.6,1.12),
 (2.98,4.32,'F2',0.0,1.0),(4.32,5.66,'F2',1.9,1.1),(5.66,7.0,'F2',3.8,1.0),
 (7.0,8.13,'N1',2.3,1.0),(8.13,9.26,'N1',7.0,1.1),
 (9.26,10.63,'N2',3.6,1.0),(10.63,12.0,'N2',5.2,1.08),
 (12.0,12.89,'SPLIT',0,1.0),(12.89,13.78,'SPLIT',1,1.0),
 (13.78,15.09,'N4B',3.2,1.0),(15.09,16.4,'N4B',4.9,1.0),
 (16.4,17.6,'N6',2.8,1.0),(17.6,18.8,'N6',4.8,1.0),(18.8,20.0,'N6',6.8,1.0)]
parts=[]
for i,(a,b,s,ss,z) in enumerate(plan):
    out=f'{W}/v2seg_{i:02d}.mp4'; L=b-a; nf=round(b*30)-round(a*30)
    if s=='SPLIT':
        n3=[0.0,2.2][int(ss)]; n5=[2.0,4.2][int(ss)]
        # topo: vizinho (N3, 720x1280 -> recorte 720x640 do rosto), base: Carol no escritório (N5)
        fc=(f"[0:v]crop=720:640:0:200,scale=1080:960,fps=30,setsar=1[t];"
            f"[1:v]crop=720:640:0:260,scale=1080:960,fps=30,setsar=1[bt];"
            f"[t][bt]vstack=inputs=2,drawbox=x=0:y=955:w=1080:h=10:color=white@1:t=fill,format=yuv420p[o]")
        sh(f'ffmpeg -v error -y -ss {n3} -t {L+0.1:.3f} -i {src["N3"]} -ss {n5} -t {L+0.1:.3f} -i {src["N5"]} -filter_complex "{fc}" -map "[o]" -an -frames:v {nf} -c:v libx264 -preset veryfast -crf 20 {out}')
    elif s=='N2':
        vf=(f"scale=w='1080*(1+0.16*t/{L:.3f})':h='1920*(1+0.16*t/{L:.3f})':eval=frame:flags=bicubic,crop=1080:1920,fps=30,format=yuv420p")
        sh(f'ffmpeg -v error -y -ss {ss} -t {L+0.1:.3f} -i {src[s]} -an -vf "{vf}" -frames:v {nf} -c:v libx264 -preset veryfast -crf 20 {out}')
    else:
        cx=0.5+0.04*((i%3)-1)*(z>1)
        rec=(',lenscorrection=k1=-0.25:k2=0.0,vignette=PI/4,noise=alls=12:allf=t,eq=saturation=0.7:contrast=1.1' if (s=='N4B' and HAS4B) else '')
        vf=(f"scale=1080:1920:flags=bicubic,crop=iw/{z}:ih/{z}:(iw-iw/{z})*{cx}:(ih-ih/{z})*0.5,scale=1080:1920,fps=30{rec},format=yuv420p")
        sh(f'ffmpeg -v error -y -ss {ss} -t {L+0.1:.3f} -i {src[s]} -an -vf "{vf}" -frames:v {nf} -c:v libx264 -preset veryfast -crf 20 {out}')
    parts.append((a,b,out))
# cortes v1 reaproveitados (a>=19.3 -> +0,7 s). Mesmo numero de quadros (0,7 s = 21 quadros).
for i,(a,b,c,s,z) in enumerate(J['segs']):
    if a>=19.3-1e-6 and c!='__prod__':
        if i==21:  # 'train' parado (mov. <2.5): re-renderiza com punch-in em rampa
            Lr=b-a; nfr=round((b+PA)*30)-round((a+PA)*30); o=f'{W}/v2seg_train21.mp4'
            vf=f"scale=1080:1920,scale=w='1080*(1.05+0.14*t/{Lr:.3f})':h='1920*(1.05+0.14*t/{Lr:.3f})':eval=frame,crop=1080:1920,fps=30,format=yuv420p"
            sh(f'ffmpeg -v error -y -ss 2.6 -t {Lr+0.1:.3f} -i {C}/vsl8_F8_treino_celular.mp4 -an -vf "{vf}" -frames:v {nfr} -c:v libx264 -preset veryfast -crf 20 {o}')
            parts.append((a+PA,b+PA,o))
        else: parts.append((a+PA,b+PA,f'{W}/seg_{i:03d}.mp4'))
parts.append((J['o3']+PA+7.3,T2,f'{W}/prod.mp4'))
parts.sort()
with open(f'{W}/v2list.txt','w') as f:
    for a,b,p in parts: f.write(f"file '{p}'\n")
sh(f'ffmpeg -v error -y -f concat -safe 0 -i {W}/v2list.txt -c copy {W}/base_v2.mp4')
d=float(sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {W}/base_v2.mp4'))
print('base_v2 duracao',round(d,3),'esperado',round(T2,3))
json.dump({'T2':T2,'PA':PA,'o2':J['o2']+PA,'o3':J['o3']+PA,'camera':os.path.basename(src['N4B']),'rec_overlay':HAS4B},open(O+'/vsl8_v2_meta.json','w'))

import subprocess,os
O='/mnt/user-data/outputs/porta8'; L=O+'/porta8_vsl_filme_v4_longa.mp4'; OFF=121.9
cuts={'corte1_susto':[(0,11.6),(68.5,88.7),(OFF-0.1,OFF+9.1),(OFF+74.9,OFF+85.4),(207.4,213.4)],
'corte2_vizinho':[(44.5,50.7),(54.4,63.1),(71.0,88.7),(OFF-0.1,OFF+9.1),(OFF+64.7,OFF+74.4),(207.4,213.4)]}
for n,rs in cuts.items():
    parts=[]
    for i,(a,b) in enumerate(rs):
        p=f'/tmp/p8/{n}_p{i}.mp4'; d=b-a
        r=subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{a:.3f}','-i',L,'-t',f'{d:.3f}','-af',f'afade=t=in:d=0.05,afade=t=out:st={d-0.06:.3f}:d=0.06','-c:v','libx264','-preset','veryfast','-crf','20','-r','30','-c:a','aac','-ar','44100','-b:a','192k',p],capture_output=True,text=True)
        if r.returncode: print(n,i,r.returncode,r.stderr[-300:])
        parts.append(p)
    open(f'/tmp/p8/{n}.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
    out=f'{O}/porta8_{n}.mp4'
    r=subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'/tmp/p8/{n}.txt','-c','copy',out],capture_output=True,text=True);print(r.returncode,r.stderr[-300:])
    r=subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out,'-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','96k',out.replace('.mp4','_leve.mp4')],capture_output=True,text=True);print(r.returncode,r.stderr[-300:])
    for f in (out,out.replace('.mp4','_leve.mp4')):
        print(os.path.basename(f),subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,duration','-of','csv=p=0',f],capture_output=True,text=True).stdout.replace('\n',' '))

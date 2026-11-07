import subprocess,os,json
O='/mnt/user-data/outputs/porta9'; L=O+'/porta9_vsl_filme_v5_longa.mp4'
T=json.load(open('/tmp/p9/times.json')); O7,O8,O9,O10,FE,END=[T[k] for k in ['O7','O8','O9','O10','FE_AT','END']]
cuts={'corte1_susto':[(0,11.4),(68.6,81.3),(O7+13.8,O8-0.3),(O9,O9+12.6),(O10+13.2,FE-0.2),(FE,END)],
'corte2_vizinho':[(44.5,50.7),(54.4,63.1),(71.0,81.3),(O7+13.8,O8-0.3),(O9+2.5,O9+12.9),(O10+13.2,FE-0.2),(FE,END)]}
for n,rs in cuts.items():
    parts=[];tot=0
    for i,(a,b) in enumerate(rs):
        p=f'/tmp/p9/c/{n}_p{i}.mp4'; d=b-a; tot+=d
        r=subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{a:.3f}','-i',L,'-t',f'{d:.3f}','-af',f'afade=t=in:d=0.05,afade=t=out:st={d-0.06:.3f}:d=0.06','-c:v','libx264','-preset','veryfast','-crf','20','-r','30','-c:a','aac','-ar','44100','-b:a','192k',p],capture_output=True,text=True)
        if r.returncode: print(n,i,r.stderr[-300:])
        parts.append(p)
    open(f'/tmp/p9/c/{n}.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
    out=f'{O}/porta9_{n}.mp4'
    r=subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'/tmp/p9/c/{n}.txt','-c','copy',out],capture_output=True,text=True);print(r.returncode,r.stderr[-200:])
    r=subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out,'-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','96k',out.replace('.mp4','_leve.mp4')],capture_output=True,text=True);print(r.returncode,r.stderr[-200:])
    print(n,round(tot,1),os.path.getsize(out),os.path.getsize(out.replace('.mp4','_leve.mp4')))

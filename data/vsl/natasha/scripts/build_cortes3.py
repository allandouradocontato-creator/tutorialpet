import subprocess,os
Q='/mnt/user-data/outputs/porta7'; L=Q+'/porta7_vsl_filme_v2_longa.mp4'; OFF=50.88
os.makedirs('/tmp/p7/cut',exist_ok=True)
def cp(a,b): return (OFF+a,OFF+b)
cuts={
 'corte1_susto':[(0.0,24.4),(39.0,42.7),cp(23.1,34.5),cp(40.4,58.12)],
 'corte2_vizinho':[(19.3,42.7),cp(1.76,10.0),cp(23.1,34.5),cp(45.1,58.12)],
}
for name,parts in cuts.items():
    fs=[];tot=0
    for i,(a,b) in enumerate(parts):
        f=f'/tmp/p7/cut/{name}_{i}.mp4'; d=b-a; tot+=d
        r=subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',f'{a:.2f}','-i',L,'-t',f'{d:.2f}','-af',f'afade=t=in:d=0.04,afade=t=out:st={d-0.06:.2f}:d=0.06','-c:v','libx264','-preset','veryfast','-crf','21','-c:a','aac','-b:a','160k','-ar','44100',f],capture_output=True,text=True)
        if r.returncode: print(r.stderr[-300:])
        fs.append(f)
    out=f'{Q}/porta7_v2_{name}.mp4'
    ins=[x for f in fs for x in ('-i',f)]
    r=subprocess.run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',''.join(f"[{i}:v][{i}:a]" for i in range(len(fs)))+f"concat=n={len(fs)}:v=1:a=1[v][a]",'-map','[v]','-map','[a]','-c:v','libx264','-preset','veryfast','-crf','21','-c:a','aac','-b:a','160k','-movflags','+faststart',out],capture_output=True,text=True);print(r.returncode,r.stderr[-300:])
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out,'-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','64k',out.replace('.mp4','_leve.mp4')])
    print(name,round(tot,1),os.path.getsize(out))

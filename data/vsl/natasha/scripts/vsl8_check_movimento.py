import subprocess, numpy as np, sys
f=sys.argv[1]; W,H=135,240
raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'fps=10,scale={W}:{H},format=gray','-f','rawvideo','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.uint8).reshape(-1,H,W).astype(float); d=np.abs(np.diff(a,axis=0)).mean((1,2))
bad=[]
for i in range(0,len(d)-9,5):
    m=d[i:i+10].mean()
    if m<2.5: bad.append((i/10,round(m,2)))
print('janelas de 1 s com movimento medio <2.5 (inicio em s):',bad)

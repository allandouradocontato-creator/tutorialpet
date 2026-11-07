import subprocess,numpy as np,sys,json
f=sys.argv[1]
w,h=108,192
raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'fps=10,scale={w}:{h},format=gray','-f','rawvideo','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.uint8).reshape(-1,w*h).astype(np.float32)
d=np.abs(a[1:]-a[:-1]).mean(1)
bad=[];run=0
for i,x in enumerate(d):
    if x<1.0: run+=1
    else:
        if run>=5: bad.append((round((i-run)/10,1),round(i/10,1),a[i].mean()))
        run=0
if run>=5: bad.append(((len(d)-run)/10,len(d)/10,a[-1].mean()))
print('frames',len(a),'seqs>=0.5s iguais:',bad)
print('menor diff medio >0:',sorted(d)[:5])

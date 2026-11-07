import subprocess,numpy as np,sys,json
f=sys.argv[1]; w,h=108,192
raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'fps=10,scale={w}:{h},format=gray','-f','rawvideo','-'],capture_output=True).stdout
a=np.frombuffer(raw,np.uint8).reshape(-1,w*h).astype(np.float32)
d=np.abs(a[1:]-a[:-1]).mean(1)
# movimento por janela de 1 s
win=[(i/10,float(d[i:i+10].mean())) for i in range(0,len(d)-9,5)]
json.dump(win,open(sys.argv[2],'w'))
low=[(t,round(m,2)) for t,m in win if m<float(sys.argv[3]) and a[int(t*10)].mean()>8]
print('janelas 1s com movimento <',sys.argv[3],':',low)

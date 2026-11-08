# porta14_norm.py: loudnorm 2 passes (I=-14, LRA=11) + mux AAC; reduz TP alvo até true peak do arquivo final <= -1.0 dBTP
import subprocess,json,re
def sh(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: raise SystemExit('FAIL '+' '.join(c)[:300]+' :: '+r.stderr[-500:])
    return r.stderr
def measure(f):
    o=sh(['ffmpeg','-nostats','-hide_banner','-i',f,'-af','ebur128=peak=true','-f','null','-']).split('Summary')[-1]
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS',o)[-1]),float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS',o)[-1])
def normalize_mux(video,wav,out,vcodec=('-c:v','copy')):
    tp=-1.3
    while True:
        o=sh(['ffmpeg','-nostats','-hide_banner','-i',wav,'-af',f'loudnorm=I=-14:TP={tp}:LRA=11:print_format=json','-f','null','-'])
        m=json.loads(o[o.rindex('{'):o.rindex('}')+1])
        sh(['ffmpeg','-y','-loglevel','error','-i',wav,'-af',f"loudnorm=I=-14:TP={tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}",'-ar','44100','/tmp/p11/_ln.wav'])
        sh(['ffmpeg','-y','-loglevel','error','-i',video,'-i','/tmp/p11/_ln.wav','-map','0:v','-map','1:a',*vcodec,'-c:a','aac','-b:a','192k','-shortest',out])
        I,P=measure(out)
        if P<=-1.0 or tp<=-3.5: return I,P,tp
        tp-=0.6

import subprocess,os
Q='/mnt/user-data/outputs/porta7'; DL='/mnt/user-data/uploads/Downloads/'
X=0.12; AEND=53.5; OFF=AEND-X; END=58.68; TOT=OFF+END
A=Q+'/porta7_filme_ato1_v4.mp4'; CORPO='/tmp/p7/corpo4_video.mp4'
AV=Q+'/vsl_filme_ato1_voz_v3.mp3'; CV='/tmp/p7/corpo4_voz.wav'; M='/tmp/p7/music_tears.mp3'
fl=f"[0:v][1:v]xfade=transition=fade:duration={X}:offset={OFF:.2f},trim=0:{TOT:.2f},setpts=PTS-STARTPTS[vout]"
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',A,'-i',CORPO,'-filter_complex',fl,'-map','[vout]','-an','-c:v','libx264','-preset','veryfast','-crf','21','/tmp/p7/long4_v.mp4'])
fa=(f"[0:a]loudnorm=I=-16:TP=-1.5,aresample=44100,apad=whole_dur={OFF:.2f},atrim=0:{OFF:.2f},asetpts=PTS-STARTPTS[a1];"
    f"[1:a]loudnorm=I=-16:TP=-1.5,aresample=44100,asetpts=PTS-STARTPTS[a2];[a1][a2]concat=n=2:v=0:a=1,apad=whole_dur={TOT:.2f},atrim=0:{TOT:.2f}[va];"
    f"[2:a]aresample=44100,atrim=0:{TOT:.2f},asetpts=PTS-STARTPTS,loudnorm=I=-16:TP=-1.5,aresample=44100,volume=-10dB,afade=t=in:d=0.5,afade=t=out:st={TOT-1.2:.2f}:d=1.2[ma];[va][ma]amix=inputs=2:duration=first:normalize=0[aout]")
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',AV,'-i',CV,'-i',M,'-filter_complex',fa,'-map','[aout]','-c:a','aac','-b:a','160k','/tmp/p7/long4_a.m4a'])
out=Q+'/porta7_vsl_filme_v3_longa.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','/tmp/p7/long4_v.mp4','-i','/tmp/p7/long4_a.m4a','-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',out])
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out,'-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','64k',Q+'/porta7_vsl_filme_v3_longa_leve.mp4'])
print(TOT,os.path.getsize(out))

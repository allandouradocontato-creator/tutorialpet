# porta14_audio.py (v10: B11 tick, loudnorm -14 2 passes)
# porta13_audio.py (parte 2): sonoplastia + mix + mux
import subprocess,json,os
S='/tmp/p7/sfx/'; M='/tmp/p7/music_tears.mp3'
T=json.load(open('/tmp/p11/times.json'))
T11=T['T11']; SH=T['pos7'][2]-T['CUT_B']
for k in ['A_END','O7','O8','O9','O9b','O10','FE_AT','END','dl','d5','d6','d7','d8']: globals()[k]=T[k]
OUT=os.environ.get('OUT','/tmp/p11/out'); os.makedirs(OUT,exist_ok=True)
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: print('ERR',r.stderr[-500:])
p2=T['pos2']; pos8=T['pos8']; L9a=T['L9a']; L9b=T['L9b']
def mo(r):
    if r<2.35: return r
    if r<6.55: return p2[2]+(r-4.15)*L9a/2.4
    if r<8.65: return p2[3]+(r-6.55)
    if r<13.65: return p2[5]+(r-11.15)
    if r<17.62: return p2[6]+(r-13.65)*L9b/3.97
    return p2[7]+(r-17.62)
def mo8(r):
    if r<18.32: return r
    if r<20.46: return pos8[1]+(r-18.38)
    return pos8[2]+(r-20.46)
q=lambda r:O7+mo(r); q8=lambda r:O8+mo8(r)
import bisect
B5M=T['b5map']
def g5(t):
    xs=[a for a,b in B5M]
    if t<=xs[0]: return B5M[0][1]
    if t>=xs[-1]: return B5M[-1][1]+(t-xs[-1])
    i=bisect.bisect_right(xs,t)-1; (a0,b0),(a1,b1)=B5M[i],B5M[i+1]
    return b0+(t-a0)*(b1-b0)/(a1-a0)
run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','sine=frequency=2300:duration=0.03','-af','afade=t=out:st=0.01:d=0.02,apad=pad_dur=0.97','/tmp/p11/tick1.wav'])
run(['ffmpeg','-y','-loglevel','error','-stream_loop','16','-i','/tmp/p11/tick1.wav','-t','16.5','/tmp/p11/tickbed.wav'])
up=('bass_hit','brass','suspense','boing','trombone','slide','funny','drum','horror','impacto','piano','string')
BL0=O9+d5; BL1=O9b   # preto mudo
d=dl
cues=[
(10.8,'sfx_bass_hit',-4),(11.0,'sfx_brass_strings_suspense',-9),(23.4,'sfx_cartoon_surprise_suspense',-9),(32.4,'sfx_brass_strings_suspense',-9),
(34.5,'sfx_cachorro_latindo',-12),(37.0,'sfx_boing',-9),(39.0,'sfx_metal_boing',-11),(43.9,'sfx_slide_funny',-8),(42.95,'sfx_trombone_decepcao',-10),
(50.6,'sfx_bass_hit',-4),(50.8,'sfx_horror_drum',-10),(51.4,'sfx_cachorro_latindo',-12),(53.0,'sfx_filhote_latidos',-14),
(61.7,'sfx_piano_falha',-8),(62.9,'sfx_bass_hit',-5),
(66.2+d,'sfx_click_botao',-6),(69.9+d,'sfx_heartbeat_impact',-6),(70.9+d,'sfx_brass_strings_suspense',-9),(71.6+d,'sfx_notificacao_celular',-12),
(T['pos1'][3]+1.9,'sfx_cachorro_choro',-12),
(q(15.0),'sfx_notificacao_celular@1.6',-14),(q(19.88),'sfx_bass_hit',-2),(q(19.95),'sfx_horror_drum@2.0',-9),
(O8+0.0,'sfx_chimes_vitoria',-7),(O8+2.1,'sfx_conquista',-12),(O8+15.1,'sfx_boing',-7),(O8+15.3,'sfx_slide_funny',-9),
# dia 14
(O9+0.1,'sfx_drum_roll_suspense@3.9',-8),(O9+g5(4.5),'sfx_bass_hit',-5),
(O9+g5(8.9),'sfx_heartbeat_impact@%.2f'%(d5-g5(8.9)-0.4),-6),(O9+g5(13.3),'sfx_suspense_swell@3.0',-12),
# reveal
(O9b+0.0,'sfx_chimes_vitoria',-5),(O9b+0.1,'sfx_conquista',-6),(O9b+0.2,'sfx_moeda_win',-11),(O9b+5.4,'sfx_chimes_vitoria',-10),
# beneficios
(O10+4.3,'sfx_boing',-10),(O10+4.6,'sfx_conquista',-10),(O10+22.4+SH,'sfx_moedas_clinking',-4),(O10+26.0+SH,'sfx_chimes_vitoria',-9),(O10+T11[0]+0.12,'TICK',-16),(O10+T11[0]+0.72,'TICK',-16),
(FE_AT+4.9,'sfx_click_botao',-5),(FE_AT+5.1,'sfx_chimes_vitoria',-9)]
ins=['-i','/tmp/p11/voz14.wav','-stream_loop','-1','-i',M,'-i','/tmp/p11/tickbed.wav']
g=(f"-19+3*between(t,{O8:.2f},{q8(20.4):.2f})+3*between(t,{O9:.2f},{BL0:.2f})+4*between(t,{O9b:.2f},{O10:.2f})+3*between(t,{O10:.2f},{FE_AT:.2f})")
mute=f"between(t,{q(19.2):.2f},{q(19.9):.2f})+between(t,{q8(20.5):.2f},{O9+0.1:.2f})+between(t,{BL0:.2f},{BL1:.2f})"
fl=[f"[1:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{T['END']},afade=t=in:d=1.5,afade=t=out:st={T['END']-4}:d=4,volume='pow(10,({g})/20)*(1-min(1,{mute}))':eval=frame[mus]",
    "[0:a]aformat=channel_layouts=stereo[vz]",
    f"[2:a]aresample=44100,aformat=channel_layouts=stereo,volume=-26dB,adelay={int(O7*1000)}|{int(O7*1000)}[tk]"]
lab=['vz','mus','tk']
for i,(t,n,db) in enumerate(cues):
    trim=None
    if '@' in n: n,trim=n.split('@'); trim=float(trim)
    if n!='TICK' and any(u in n for u in up) and 'cachorro' not in n: db+=3
    ins+=['-i','/tmp/p11/tick1.wav' if n=='TICK' else S+n+'.mp3']
    f=f"[{i+3}:a]"+(f"atrim=0:{trim},afade=t=out:st={max(trim-0.25,0)}:d=0.25," if trim else '')+f"aresample=44100,aformat=channel_layouts=stereo,volume={db}dB,adelay={int(t*1000)}|{int(t*1000)}[s{i}]"
    fl.append(f); lab.append(f's{i}')
# mudo total no preto (voz+sfx+musica)
fl.append(''.join(f'[{l}]' for l in lab)+f"amix=inputs={len(lab)}:normalize=0:duration=longest,volume='1-between(t,{BL0:.2f},{BL1:.2f})':eval=frame,alimiter=limit=0.95,atrim=0:{T['END']}[out]")
run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','/tmp/p11/mix.wav'])
import re
LN='I=-14:TP=-1.3:LRA=11'
o=subprocess.run(['ffmpeg','-nostats','-hide_banner','-i','/tmp/p11/mix.wav','-af',f'loudnorm={LN}:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
m=json.loads(o[o.rindex('{'):o.rindex('}')+1])
run(['ffmpeg','-y','-loglevel','error','-i','/tmp/p11/mix.wav','-af',f"loudnorm={LN}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}",'-ar','44100','/tmp/p11/mix_ln.wav'])
run(['ffmpeg','-y','-loglevel','error','-i','/tmp/p11/long_v.mp4','-i','/tmp/p11/mix_ln.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',OUT+'/porta14_vsl_filme_v10_longa.mp4'])
run(['ffmpeg','-y','-loglevel','error','-i',OUT+'/porta14_vsl_filme_v10_longa.mp4','-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','96k',OUT+'/porta14_vsl_filme_v10_longa_leve.mp4'])
for f in ['porta14_vsl_filme_v10_longa','porta14_vsl_filme_v10_longa_leve']: print(f,os.path.getsize(OUT+'/'+f+'.mp4'))

import subprocess,json,os
O='/mnt/user-data/outputs/porta10'; S='/tmp/p7/sfx/'
T=json.load(open('/tmp/p9/times.json')); O7,O8,O9,O10,FE_AT,END=[T[k] for k in ['O7','O8','O9','O10','FE_AT','END']]
A1='/mnt/user-data/outputs/porta7/vsl_filme_ato1_voz_v4.mp3'
FE='/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha/fecho/FECHO_gravado_sem_Eu_sou_a_doutora_Natasha.mp3'
M='/tmp/p7/music_tears.mp3'
V={b:f'/mnt/user-data/outputs/porta9/vsl_filme_p9_{b}_voz.mp3' for b in ['B7b','B8','B9','B10']}
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print('ERR',r.stderr[-500:])
mono="aresample=44100,aformat=channel_layouts=mono"
fa=(f"[0:a]atrim=0:81.2,asetpts=PTS-STARTPTS,afade=t=out:st=81.16:d=0.04,{mono}[a];"
    f"[1:a]{mono},adelay={int(O7*1000)}[b1];[2:a]{mono},adelay={int(O8*1000)}[b2];[3:a]{mono},adelay={int(O9*1000)}[b3];[4:a]{mono},adelay={int(O10*1000)}[b4];"
    f"[5:a]{mono},adelay={int(FE_AT*1000)}[f];[a][b1][b2][b3][b4][f]amix=inputs=6:normalize=0:duration=longest,loudnorm=I=-16:TP=-1.5,aresample=44100,apad=whole_dur={END}[v]")
run(['ffmpeg','-y','-loglevel','error','-i',A1,'-i',V['B7b'],'-i',V['B8'],'-i',V['B9'],'-i',V['B10'],'-i',FE,'-filter_complex',fa,'-map','[v]','-t',str(END),'/tmp/p9/voz6.wav'])
# tick-tock bed
run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','sine=frequency=2300:duration=0.03','-af','afade=t=out:st=0.01:d=0.02,apad=pad_dur=0.97','/tmp/p9/tick1.wav'])
run(['ffmpeg','-y','-loglevel','error','-stream_loop','16','-i','/tmp/p9/tick1.wav','-t','16.5','/tmp/p9/tickbed.wav'])
up=('bass_hit','brass','suspense','boing','trombone','slide','funny','drum','horror','impacto','piano','string')
cues=[
(10.8,'sfx_bass_hit',-4),(11.0,'sfx_brass_strings_suspense',-9),
(23.4,'sfx_cartoon_surprise_suspense',-9),
(32.4,'sfx_brass_strings_suspense',-9),
(34.5,'sfx_cachorro_latindo',-12),
(37.0,'sfx_boing',-9),(39.0,'sfx_metal_boing',-11),(43.9,'sfx_slide_funny',-8),
(42.95,'sfx_trombone_decepcao',-10),
(50.6,'sfx_bass_hit',-4),(50.8,'sfx_horror_drum',-10),
(51.4,'sfx_cachorro_latindo',-12),(53.0,'sfx_filhote_latidos',-14),
(61.7,'sfx_piano_falha',-8),(62.9,'sfx_bass_hit',-5),
(66.2,'sfx_click_botao',-6),(69.9,'sfx_heartbeat_impact',-6),(70.9,'sfx_brass_strings_suspense',-9),
(71.6,'sfx_notificacao_celular',-12),
(78.2,'sfx_cachorro_choro',-12),
# B7b tensa
(O7+16.7,'sfx_notificacao_celular@1.6',-8),
(O7+19.88,'sfx_bass_hit',-2),(O7+19.95,'sfx_horror_drum@2.0',-9),
# B8 alegria
(O8+0.0,'sfx_chimes_vitoria',-7),(O8+2.1,'sfx_conquista',-12),(O8+15.1,'sfx_boing',-7),(O8+15.3,'sfx_slide_funny',-9),
# B9 falsa tragédia -> explosao
(O9+0.2,'sfx_drum_roll_suspense@3.9',-8),(O9+3.92,'sfx_bass_hit',-2),(O9+4.0,'sfx_impacto_cinematico@2.5',-10),
(O9+11.58,'sfx_chimes_vitoria',-5),(O9+11.6,'sfx_conquista',-6),(O9+11.7,'sfx_moeda_win',-10),
(O9+16.3,'sfx_filhote_latidos@1.6',-13),(O9+20.86,'sfx_moeda_win',-8),(O9+22.9,'sfx_chimes_vitoria',-9),
# B10 venda
(O10+1.0,'sfx_boing',-10),(O10+2.0,'sfx_conquista',-9),(O10+15.56,'sfx_moedas_clinking',-4),(O10+19.9,'sfx_chimes_vitoria',-9),
(FE_AT+4.9,'sfx_click_botao',-5),(FE_AT+5.1,'sfx_chimes_vitoria',-9),
]
ins=['-i','/tmp/p9/voz6.wav','-stream_loop','-1','-i',M,'-i','/tmp/p9/tickbed.wav']
g=f"-19+3*between(t,{O8:.2f},{O8+20.4:.2f})-12*between(t,{O9+0.3:.2f},{O9+11.5:.2f})+4*between(t,{O9+11.5:.2f},{O9+18:.2f})+2*between(t,{O10:.2f},{FE_AT:.2f})"
mute=f"between(t,{O7+19.2:.2f},{O7+19.9:.2f})+between(t,{O8+20.5:.2f},{O9+0.3:.2f})+between(t,{O9+5.4:.2f},{O9+6.6:.2f})"
fl=[f"[1:a]aresample=44100,aformat=channel_layouts=stereo,atrim=0:{END},afade=t=in:d=1.5,afade=t=out:st={END-4}:d=4,volume='pow(10,({g})/20)*(1-min(1,{mute}))':eval=frame[mus]",
    "[0:a]aformat=channel_layouts=stereo[vz]",
    f"[2:a]aresample=44100,aformat=channel_layouts=stereo,volume=-26dB,adelay={int(O7*1000)}|{int(O7*1000)}[tk]"]
lab=['vz','mus','tk']
for i,(t,n,db) in enumerate(cues):
    trim=None
    if '@' in n: n,trim=n.split('@'); trim=float(trim)
    if any(u in n for u in up) and 'cachorro' not in n: db+=3
    ins+=['-i',S+n+'.mp3']
    f=f"[{i+3}:a]"+(f"atrim=0:{trim},afade=t=out:st={max(trim-0.25,0)}:d=0.25," if trim else '')+f"aresample=44100,aformat=channel_layouts=stereo,volume={db}dB,adelay={int(t*1000)}|{int(t*1000)}[s{i}]"
    fl.append(f); lab.append(f's{i}')
fl.append(''.join(f'[{l}]' for l in lab)+f"amix=inputs={len(lab)}:normalize=0:duration=longest,alimiter=limit=0.95,atrim=0:{END}[out]")
run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','/tmp/p9/mix7.wav'])
run(['ffmpeg','-y','-loglevel','error','-i','/tmp/p9/long7_v.mp4','-i','/tmp/p9/mix7.wav','-map','0:v','-map','1:a','-c:v','libx264','-preset','veryfast','-crf','24','-c:a','aac','-b:a','192k','-shortest',O+'/porta10_vsl_filme_v6prov_longa.mp4'])
run(['ffmpeg','-y','-loglevel','error','-i',O+'/porta10_vsl_filme_v6prov_longa.mp4','-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','96k',O+'/porta10_vsl_filme_v6prov_longa_leve.mp4'])
for f in ['porta10_vsl_filme_v6prov_longa','porta10_vsl_filme_v6prov_longa_leve']:
    print(f,os.path.getsize(O+'/'+f+'.mp4'),subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,duration','-of','csv=p=0',O+'/'+f+'.mp4'],capture_output=True,text=True).stdout.replace('\n',' '))

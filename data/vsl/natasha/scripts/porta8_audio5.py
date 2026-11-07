import subprocess,os
O='/mnt/user-data/outputs/porta8'; S='/tmp/p7/sfx/'
OFF=121.9; FE_AT=207.45; END=213.4
A1='/mnt/user-data/outputs/porta7/vsl_filme_ato1_voz_v4.mp3'; B=O+'/vsl_filme_corpo_voz_v20.mp3'
FE='/home/claude/allandouradocontato-creator/tutorialpet/data/vsl/natasha/fecho/FECHO_gravado_sem_Eu_sou_a_doutora_Natasha.mp3'
M='/tmp/p7/music_tears.mp3'
# voice stem
fa=(f"[0:a]aresample=44100,aformat=channel_layouts=mono[a];[1:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(OFF*1000)}[b];"
    f"[2:a]aresample=44100,aformat=channel_layouts=mono,adelay={int(FE_AT*1000)}[f];[a][b][f]amix=inputs=3:normalize=0:duration=longest,loudnorm=I=-16:TP=-1.5,aresample=44100,apad=whole_dur={END}[v]")
r=subprocess.run(['ffmpeg','-y','-loglevel','error','-i',A1,'-i',B,'-i',FE,'-filter_complex',fa,'-map','[v]','-t',str(END),'/tmp/p8/voz5.wav'],capture_output=True,text=True);print(r.stderr[-400:])
# sfx cues: (time, file, dB)
cues=[
(10.8,'sfx_bass_hit',-4),(11.0,'sfx_brass_strings_suspense',-9),
(23.4,'sfx_cartoon_surprise_suspense',-9),
(32.4,'sfx_brass_strings_suspense',-9),
(34.5,'sfx_cachorro_latindo',-12),
(37.0,'sfx_boing',-9),(39.0,'sfx_metal_boing',-11),(43.9,'sfx_slide_funny',-8),
(46.0,'sfx_trombone_decepcao',-10),
(50.6,'sfx_bass_hit',-4),(50.8,'sfx_horror_drum',-10),
(51.4,'sfx_cachorro_latindo',-12),(53.0,'sfx_filhote_latidos',-14),
(61.7,'sfx_piano_falha',-8),(62.9,'sfx_bass_hit',-5),
(66.2,'sfx_click_botao',-6),(69.9,'sfx_heartbeat_impact',-6),(70.9,'sfx_brass_strings_suspense',-9),
(71.6,'sfx_notificacao_celular',-12),
(78.2,'sfx_cachorro_choro',-12),(83.1,'sfx_impacto_cinematico',-8),
(86.9,'sfx_bass_hit',-5),(88.6,'sfx_chimes_vitoria',-9),
(99.7,'sfx_slide_funny',-8),(99.9,'sfx_boing',-10),
(102.8,'sfx_brass_strings_suspense',-9),
(108.9,'sfx_chimes_vitoria',-10),(113.0,'sfx_conquista',-10),
(116.2,'sfx_trombone_decepcao',-10),(118.0,'sfx_conquista',-9),
(OFF+7.4,'sfx_cartoon_string_suspense',-11),(OFF+8.4,'sfx_chimes_vitoria',-11),
(OFF+14.2,'sfx_boing',-10),(OFF+18.0,'sfx_trombone_decepcao',-10),
(OFF+23.8,'sfx_conquista',-10),
(OFF+37.0,'sfx_moeda_win',-12),(OFF+46.5,'sfx_boing',-10),
(OFF+59.4,'sfx_chimes_vitoria',-10),
(OFF+63.4,'sfx_brass_strings_suspense',-10),(OFF+66.9,'sfx_moeda_win',-11),
(OFF+72.3,'sfx_conquista',-12),
(OFF+78.9,'sfx_moedas_clinking',-6),(OFF+85.0,'sfx_funny_fail_low',-8),(OFF+85.1,'sfx_boing',-12),
(FE_AT+4.9,'sfx_click_botao',-6),(FE_AT+5.1,'sfx_chimes_vitoria',-10),
]
ins=['-i','/tmp/p8/voz5.wav','-stream_loop','-1','-i',M]
fl=[f"[1:a]aresample=44100,aformat=channel_layouts=stereo,volume=-19dB,afade=t=in:d=1.5,afade=t=out:st={END-4}:d=4,atrim=0:{END}[mus]",
    "[0:a]aformat=channel_layouts=stereo[vz]"]
lab=['vz','mus']
for i,(t,n,db) in enumerate(cues):
    ins+=['-i',S+n+'.mp3']
    fl.append(f"[{i+2}:a]aresample=44100,aformat=channel_layouts=stereo,volume={db}dB,adelay={int(t*1000)}|{int(t*1000)}[s{i}]"); lab.append(f's{i}')
fl.append(''.join(f'[{l}]' for l in lab)+f"amix=inputs={len(lab)}:normalize=0:duration=longest,alimiter=limit=0.95,atrim=0:{END}[out]")
r=subprocess.run(['ffmpeg','-y','-loglevel','error']+ins+['-filter_complex',';'.join(fl),'-map','[out]','-ar','44100','/tmp/p8/mix5.wav'],capture_output=True,text=True);print(r.stderr[-600:])
r=subprocess.run(['ffmpeg','-y','-loglevel','error','-i','/tmp/p8/long5_v.mp4','-i','/tmp/p8/mix5.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',O+'/porta8_vsl_filme_v4_longa.mp4'],capture_output=True,text=True);print(r.stderr[-400:])
r=subprocess.run(['ffmpeg','-y','-loglevel','error','-i',O+'/porta8_vsl_filme_v4_longa.mp4','-vf','scale=-2:640','-c:v','libx264','-crf','30','-preset','veryfast','-c:a','aac','-b:a','96k',O+'/porta8_vsl_filme_v4_longa_leve.mp4'],capture_output=True,text=True);print(r.stderr[-400:])
for f in ['porta8_vsl_filme_v4_longa','porta8_vsl_filme_v4_longa_leve']:
    print(f,subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,duration','-of','csv=p=0',O+'/'+f+'.mp4'],capture_output=True,text=True).stdout.replace('\n',' '))

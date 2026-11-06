Dados até 2026-11-06 07:35 (Fortaleza)
Número do dia: rotinas falhando ou suspensas por erro = 0. CORRIGI: 1 (E203 pinscher promovido) | PRECISO DO ALLAN: 0 | rodada continua até o publicar_blog fechar
| rotina | estado | último run | idade do último resultado | problema | correção |
|---|---|---|---|---|---|
| 17 rotinas ativas (1+1, Diretores, Medidor, Auditor Anúncios, Operador, Agendador, lembretes, Vigia) | ok | todas SUCCEEDED; next_run futuro (Operador 07:41 F, Agendador 08:15 F) | <=24 h | - | - |
| Desligadas por decisão (Executor, Virais, Pesquisadores, Humorista, Utilidade) | off | - | - | não é falha | - |
| fabrica.yml | verde | #42076244257 05/11 14:36 F (schedule) | ~17 h (<30 h) | cron das 06h F não rodou hoje (igual a 05/11) | monitorar; alerta só >30 h |
| publicar_blog.yml | rodando | #42201996740 06/11 07:21 F (push 7a0b9cb) | - | - | conferir verde + 200 na ronda 11:19 (E34) |
| Blog hoje | 0/1 -> 1/1 em curso | último artigo 05/11 15:25 F (~16 h) | ~16 h | dia sem artigo às 07:20 | E203: pinscher-giselle 0 em blog_aprovados.txt (7a0b9cb) |
| AdSense | 0 FALHA na auditoria local | auditoria 06/11 | - | - | - |
| FB/IG (Zernio) | ok | publicados 05/11 (FB 22:01 Z, IG 18:02 Z); 10 agendados | <24 h | 8 falhas antigas (mídia 422), 0 novas | E151; retry proibido |
| TikTok (Buffer) | ok | castração 05/11 20:20 F; hoje 07:20 F vacina agendada, 07/11 fujão, 08/11 atum | ~11 h | atum 08/11 ainda com erro 'unknown' (E200) | Agendador 08:15 F refaz; Vigia não republica |
| Issues falhou/nao publicou | 21 abertas, última 02/11 | - | - | só histórico, runs verdes desde então | fechar na revisão |
| Estoque media sem artigo | 2 aprovados fora da fila | - | - | V2.2: 1/dia | 1+1 de 12:17 F cobre amanhã |

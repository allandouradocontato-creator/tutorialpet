Dados até 2026-11-02 07:30 (Fortaleza)
Número do dia: rotinas falhando ou suspensas por erro = 0 (desligadas por ordem do Allan 02/11, E177). CORRIGI: 3 | PRECISO DO ALLAN: 0
| rotina | estado | último run | idade do último resultado | problema | correção |
|---|---|---|---|---|---|
| Rotinas ativas (14: 1+1, Diretores Op/Cont/Prod/Aud, Medidor, Auditor Anúncios, Agendador, Segurança, Vigia + 4 lembretes) | ok | todas SUCCEEDED, next_run futuro | <=10 h | nenhuma falha | - |
| fabrica.yml | SEM turno 06h de hoje (último verde 01/11 21:21Z, ~13 h) | cron 09:07Z/09:37Z não rodou (3º dia seguido) | ~13 h | cron do GitHub descartado | CORRIGI: dispatch REST 10:22Z foi cancelado (concorrência com publicar_blog); redisparado 41429007069 após o publicar (pending) |
| publicar_blog.yml | #87 FALHOU 07:02Z (abandono-de-animal: capa), issue #42 aberta | 02/11 06:54Z | ~3,5 h | abandono sem capa (capas_pendentes) | CORRIGI: promovi gato-pode-comer-atum (cf71e41), push dispara #41428320519 |
| reforco_blog.yml | disparado | 10:22Z | - | 3 rascunhos sem Fontes | CORRIGI: dispatch REST 41428322700 |
| Blog hoje | 1/1 (gato-pode-comer-atum 200, commit f7f0947) | - | - | abandono travou | promovido gato-pode-comer-atum; CONFIRMADO curl 200 às 07:5x |
| AdSense | 1 FALHA: buraco 15/09-06/10 (irrecuperável) | - | - | - | só o tempo resolve |
| Zernio FB/IG | 8 failed antigos (mídia 422), nenhum novo; agendados ok | FB 01/11 23:04Z, IG 23:01Z | <9 h | - | ficha E151 existente |
| Buffer TikTok | 0 erro; agendado até 04/11 13:20Z | - | - | - | Agendador cobre |
| Issues abertas | #42 nova (blog 02/11); #14-#41 antigas | - | - | - | fecha com publicar verde |

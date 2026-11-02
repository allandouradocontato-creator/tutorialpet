Dados até 2026-11-02 11:50 (Fortaleza)
Número do dia: rotinas falhando ou suspensas por erro = 0 (desligadas por ordem do Allan 02/11, E177). CORRIGI: 1 | PRECISO DO ALLAN: 0
| rotina | estado | último run | idade do último resultado | problema | correção |
|---|---|---|---|---|---|
| Rotinas ativas (1+1, Diretores Op/Cont/Prod/Aud, Medidor, Auditor Anúncios, Agendador, Segurança, Vigia + lembretes) | ok | todas SUCCEEDED, next_run futuro (Diretor Conteúdo 11:37 em disparo) | <=12 h | nenhuma falha | - |
| fabrica.yml | verde | #41429007069 02/11 10:27Z | ~4 h | - | cron das 06h segue sem rodar (4º dia), dispatch cobriu |
| publicar_blog.yml | verde | push #41428320519 10:22Z | ~4 h | issue #42 aberta (falha das 07:02Z, já sanada) | fecha com verde |
| reforco_blog.yml | gato-pode-comer-atum no ar (200) mas sem seção Fontes | 10:22Z verde, não pegou o artigo publicado depois | - | auditoria AdSense: 1 FALHA Fontes | CORRIGI: dispatch REST #41465143157 14:46Z; conferir na ronda 15:19 |
| Blog hoje | 2/1 (abandono + gato-pode-comer-atum) | f7f0947 10:27Z | ~4 h | - | ok |
| AdSense | 2 FALHA: buraco 15/09-06/10 (irrecuperável) + Fontes (acima) | - | - | - | só o tempo / reforço |
| Zernio FB/IG | 8 failed antigos (mídia 422), nenhum novo; agendados ok | FB 02/11 02:04Z, IG 02:05Z | ~12 h | - | ficha E151 existente |
| Buffer TikTok | 0 erro; agendado até 05/11 13:20Z | - | - | - | Agendador cobre |
| Issues abertas | #42 (blog 02/11) e antigas #14-#41 | - | - | - | fecha com verde |

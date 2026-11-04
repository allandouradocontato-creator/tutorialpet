Dados até 2026-11-04 07:20 (Fortaleza)
Número do dia: rotinas falhando ou suspensas por erro = 0. CORRIGI: 1 | PRECISO DO ALLAN: 0 | (E34: só encerra com run verde)
| rotina | estado | último run | idade do último resultado | problema | correção |
|---|---|---|---|---|---|
| 12 rotinas ativas (1+1, Diretores Operação/Audiência/Produto/Conteúdo, Medidor, Auditor Anúncios, Agendador, Segurança, lembretes, Vigia) | ok | todas SUCCEEDED; Vigia = esta ronda (PENDING); next_run futuro | <=22 h | nenhum | - |
| Desligadas por decisão (22/10 e 02/11) | off | - | - | não são falha | - |
| fabrica.yml | verde | #41682644948 03/11 17:16Z | ~17 h | cron 06h (09:07Z) e 09:37Z de hoje não geraram rodada | dentro do limite 30 h; se 12:19Z sem rodada, dispatch |
| publicar_blog.yml | verde | #41706062982 03/11 19:44Z | ~14 h | - | push de promoção 20e7b97 dispara nova rodada |
| Blog hoje | 0/1 às 07:20 | último artigo 03/11 19:55Z | ~14 h | dia sem artigo | promovi adocao-responsavel-o-que-a-lei-exige... (rascunho 1261 pal., com Fontes) em blog_aprovados.txt (20e7b97); conferir 200 na ronda 11:19 |
| AdSense | 1 FALHA | auditoria 04/11 | - | só buraco 15/09-06/10 (histórico, irrecuperável); vacina-antirrabica agora com Fontes (reforço 2916478 OK, E34 fechado) | - |
| Posts FB/IG (Zernio) | ok | 22 agendados | estoque >24 h | 8 failed antigos (URL de mídia, set-out), 0 novos | nada novo |
| TikTok (Buffer) | atenção | 2 agendados TikTok (04/11 e 05/11 13:20Z), 0 erro | estoque ~1 dia | abaixo de 2 dias | Agendador roda 08:15 (11:15Z); conferir na ronda 11:19 |
| Issues antigas "falhou/nao publicou" | abertas | última 02/11 | - | sem falha nova | fechar na revisão |

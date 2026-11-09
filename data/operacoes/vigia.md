Dados até 2026-11-09 07:25 (Fortaleza) | CORRIGI: 1 | PRECISO DO ALLAN: 0 | TUDO OK (com 2 conferências abertas)
Número do dia: rotinas falhando/suspensas = 0 (meta zero). 14 ativas, todas SUCCEEDED; Vigia desta rodada PENDING = eu.
| rotina | estado | último run | idade do último resultado | problema | correção |
|---|---|---|---|---|---|
| rotinas ativas (14) | ok | Estrategista 09/11 07:08 F; Dir. Operação 08/11 21:41 F; Agendador 08/11 16:15 F; Rotina 1+1 08/11 12:18 F | <16 h | - | - |
| rotinas desligadas (por decisão) | ok | Executor, Virais, Humorista, Conferente etc. | - | enabled=false desde 22/10-02/11 | decisão já tomada |
| fabrica.yml | verde | run 42498875213 08/11 13:14 F (schedule) | ~18 h (limite 30 h) | - | - |
| publicar_blog.yml | verde | run 42471092479 08/11 07:21 F | ~24 h | roda 07:21 F (push) | - |
| Blog | 0/1 hoje (07:25 F, ainda cedo) | último artigo 08/11 (abandono-de-animal) | ~21 h | AdSense: 1 FALHA 'ritmo' (datePublished mais novo 06/11) | CORRIGI: 'melhor-fonte-de-agua-para-gato-vale-a-pena 0' em blog_aprovados.txt (commit db07b8c); publicar_blog dispara no push; conferir 11:19 (E34) |
| FB/IG (Zernio) | ok | FB 08/11 14:04 F, IG 15:07 F | ~17 h | 8 erros antigos de mídia (sem novos) | retry proibido (E151); 6 agendados |
| TikTok (Buffer) | 1 enviado ontem 10:21 F; hoje 0 agendado | 08/11 10:21 F (sent) | ~21 h | nenhum agendado para 09/11 (só 10/11 10:20 F); Buffer sem métricas atualizadas (0 views, metricsUpdatedAt = criação) | Operador 07:41 F e Agendador 08:15 F completam (E219/E221); conferir 11:19; E223 (0 views) fica para 10/11 |
| Issues falhou/nao publicou | 30 abertas, última 02/11 | - | 7 dias | histórico (blog verde desde 03/11) | fechar na revisão |
Créditos ElevenLabs: creditos_eleven.yml última saída 28/10 (stale, não medido).

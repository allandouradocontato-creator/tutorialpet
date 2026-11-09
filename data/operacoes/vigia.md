Dados até 2026-11-09 19:30 (Fortaleza) | CORRIGI: 0 | PRECISO DO ALLAN: 2 (E215; V09 fire_trigger do Agendador negado 2x) | sem rotina caída
Número do dia: rotinas falhando/suspensas = 0 (meta zero). Ativas todas SUCCEEDED (Vigia desta rodada PENDING = eu). add_repo indisponível na sessão; clone local já em main (5e490b8).
| rotina | estado | último run | idade do último resultado | problema | correção |
|---|---|---|---|---|---|
| rotinas ativas (14) | ok | Agendador 16:15 F; Rotina 1+1 12:21 F; Dir. Audiência 09:23 F; Operador 07:41 F; Auditor Anúncios 09:34 F | <12 h | - | - |
| desligadas por decisão | ok | Executor, Virais, Humorista etc. | - | enabled=false desde 22/10-02/11 | decisão já tomada |
| fabrica.yml | verde | run 42688511391 09/11 16:58 F (schedule) | ~2,5 h | - | - |
| publicar_blog.yml | verde | run 42600296941 09/11 07:21 F (push) | ~12 h | - | - |
| Blog | 1/1 hoje (site 200) | melhor-fonte-de-agua-para-gato 07:26 F | 12 h | AdSense 1 FALHA 'ritmo' falsa (E215: datePublished = data do rascunho 06/11) | E215 aguarda ok do Allan |
| FB/IG (Zernio) | ok | FB 10:05 e IG 11:02 F (devolução/escova) | ~8 h | 8 erros antigos de mídia, nenhum novo | retry proibido (E151) |
| Estoque FB/IG | 1 dia | agendado: FB+IG 10/11 10:00 F (adoção); IG vet x3 (14/11+) | - | FB só 1 agendado; 11/11 e 12/11 vazios; Agendador 16:15 F não cobriu (V09) | fire_trigger Agendador NEGADO pelo classificador (2ª vez); roda sozinho 08:15 F de 10/11; V09 segue aberta |
| TikTok (Buffer) | 3/3 hoje | castração 14:21 F sent; cama P2 20:20 F agendada; 10/11 10:20 adoção | - | sem erro; views ainda zeradas/baixas (E223) | conferir 10/11 |
| Issues falhou/nao publicou | 30 abertas, histórico (última 02/11) | - | 7 dias | blog verde desde 03/11 | fechar na revisão |
Créditos ElevenLabs: creditos_eleven.yml última saída 28/10 (stale, não medido).

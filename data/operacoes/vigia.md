Dados até 2026-10-27 19:25 (Fortaleza) | Vigia v2 | Número do dia: rotinas falhando/suspensas = 0 (meta zero); falhas abertas: 8 Zernio (vídeo/imagem 404/422, iguais a 26/10)
CORRIGI: 0 (redisparo seria queimado: mesmo saldo ElevenLabs/cota Gemini; E34) | PRECISO DO ALLAN: 1 (ElevenLabs sem créditos, V19) | abertos nuvem: V10-V19
| rotina | estado | último run / idade | problema | correção |
|---|---|---|---|---|
| rotinas ativas | ok | todas SUCCEEDED; só o Vigia PENDING (esta rodada); nenhuma next_run vencida | - | nada |
| fabrica.yml | VERMELHO #165-170 (15:30Z-21:34Z, agendadas); último verde #161 10:40Z (~12 h) | ElevenLabs 306 vs ~748 (preflight) + Gemini 429; issues #19-26 abertas | ALERTA FÁBRICA PARADA (>6 h; limite 30 h ainda não) | V19; não redisparo; sugerir pausar o cron da fábrica até recarga (queima Actions e abre 1 issue por rodada) |
| publicar_blog.yml | #62 vermelho 14:29Z; último verde #59 26/10 18:22Z (~28 h) | 2 reprovados quality_editor + capa Gemini 429/503; issue #18 | perto do limite 30 h | V19 (capa Pexels); 5 aprovados já promovidos hoje |
| blog (ritmo) | abaixo de 4/dia (último commit de artigo 27/10 10:04Z, ~12 h) | rascunhos sem capa | não promovi mais: falharia igual (E34) | V19 |
| Zernio/Buffer | 8 Zernio em erro | iguais a 26/10 | mídia 404 | V10/V14 (retry proibido) |
| estoque posts | ~2 dias | Buffer/Zernio agendados até 29/10 | acaba sem vídeo novo | depende de V19 |
| ElevenLabs | CRÍTICO | 306 créditos | - | Allan (V19) |
Idade do último resultado: artigo novo ~12 h; fábrica verde ~12 h; publicar_blog verde ~28 h.

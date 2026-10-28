Dados até 2026-10-28 07:25 (Fortaleza) | Vigia v2 | Número do dia: rotinas falhando/suspensas = 0 de 24 ativas (meta zero); desligadas de propósito: 26 (22/10) + Medidor (teste encerrado) + Guerrilha (device_absent, precisa do Chrome)
CORRIGI: 1 (promovi 2 aprovados com Fontes; publicar_blog dispara sozinho) | PRECISO DO ALLAN: 1 (ElevenLabs, V19) | abertos nuvem: V17-V20, E131
| rotina | estado | último run / idade | problema | correção |
|---|---|---|---|---|
| rotinas ativas | ok | todas SUCCEEDED; Vigia PENDING = esta rodada; nenhuma next_run vencida | - | nada |
| fabrica.yml | VERMELHO #162-172; último verde #161 27/10 10:40Z (~21 h); nenhuma rodada desde 00:47Z | ElevenLabs 306 vs ~540-750 (preflight) + Gemini 429; issues #19-28 | ALERTA FÁBRICA PARADA (limite 30 h em ~9 h) | não redisparei (E34, mesmo saldo); V19 Allan; E131(1) preflight não derrubar rodada ainda NÃO aplicado |
| publicar_blog.yml | #62 vermelho 27/10 14:29Z; último verde #59 26/10 18:22Z (~40 h) | quality_editor reprovou 2 + capa Gemini 429/503 | ALERTA BLOG PARADO (>30 h) | promovi escova-de-dentes-gato e slow-feed (Fontes ok, cota Gemini nova no dia); push dispara o workflow; conferir verde no próximo Vigia |
| blog (ritmo) | 0 artigos hoje, 0 ontem após 10:04Z; plano 3-4/dia | rascunhos sem Fontes (6 de 8 livres) | abaixo do plano | 2 promovidos; demais rascunhos sem Fontes não promovo (AdSense); E120/E121 |
| Zernio | 8 posts em erro (mídia 404/422), iguais a 27/10 | V10/V14 | retry proibido | ficha existente |
| estoque posts | ~1-2 dias (agendados até 29/10) | sem vídeo novo | acaba | depende de V19 |
| ElevenLabs | CRÍTICO | 306 créditos | - | Allan (V19) |
| AdSense | 3 FALHAS: buraco de ritmo 15/09-06/10 (histórico), 5 sem capa, 10 sem Fontes | - | - | E121; ritmo só se resolve com publicar_blog verde |
Idade do último resultado: artigo novo ~24 h (27/10 10:04Z); fábrica verde ~21 h; publicar_blog verde ~40 h.

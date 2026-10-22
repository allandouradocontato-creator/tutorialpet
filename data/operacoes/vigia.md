Dados até 2026-10-22 15:30 (Fortaleza)
# Vigia de Rotinas — 22/10/2026 (rodada 15:19)
Número do departamento: 1 rotina presa (Executor PENDING 8,4 h, sem commit); Medidor e Diretor de Operação voltaram a SUCCEEDED (14:20Z). Guerrilha desligada (depende do PC).
Já funciona e replicar: blog com 3 artigos no ar hoje (plano 3: cumprido), fábrica #108 verde, publicar_blog #34-36 verdes, 0 post em erro (Zernio/Buffer), 0 issue aberta, 17 posts FB/IG agendados. Replicar = promover aprovado e disparar publicar_blog na hora. Habilidade que falta: push da fábrica (GITHUB_TOKEN) não dispara workflow; teste grátis: dispatch REST após cada aprovação da fábrica.

| Rotina/engrenagem | Estado | Último run | Problema | Correção aplicada | Idade do último resultado |
|---|---|---|---|---|---|
| Executor de Decisões | ALERTA | 22/10 09:54Z PENDING | sem commit, livro vencido (E32) | fire_trigger 18:21Z (1x/dia usada) | 8,4 h em PENDING |
| Medidor / Dir. Operação | OK | 22/10 14:20Z SUCCEEDED | V05 fechado com evidência | - | 4 h |
| Guerrilha | DESLIGADA | device_absent | depende do Chrome | já em execucao.md (V05) | - |
| Demais rotinas ativas | OK | SUCCEEDED / prazo | 0 vencida, 0 suspensa | - | < 24 h |
| Rotinas desligadas por Allan (16:41Z) | informativo | - | Humorista, Utilidade, Cobrança, Afiliados, Pesquisadores etc. | nenhuma | - |
| fabrica.yml | OK | #108 14:37Z verde; #109 em curso | - | - | 3,7 h |
| publicar_blog.yml | OK | #36 18:01Z verde | rampa-pet aprovada 18:18Z sem página | dispatch REST 18:22Z | 0,3 h |
| Blog no ar | OK | 3 artigos 22/10 (lagrima, gato-morde, petiscos) | AdSense: 4 FALHAS (capas repetidas, galgo sem capa, 3 saúde sem fonte, buraco 15/09-06/10 histórico) | galgo em capas_refazer; dispatch reforco_blog.yml | < 1 h |
| Posts FB/IG/TikTok | OK | publicados hoje, 0 erro, 17 agendados Zernio | fila TikTok (E25) não conferida | - | < 6 h |
| ElevenLabs | sem dado | creditos_eleven #7 20/10 | sem saída nova | - | 44 h+ |

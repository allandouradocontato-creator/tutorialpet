Dados até 2026-10-24 07:19 (Fortaleza) | Vigia v2 | Número do dia: rotinas falhando/suspensas = 0 (meta zero)
| rotina | estado | último run / idade | problema | correção |
|---|---|---|---|---|
| 40 rotinas (19 ativas; 21 desligadas por ordem do Allan 22/10) | ok | todas SUCCEEDED; nenhuma next_run vencida; Vigia atual PENDING (esta rodada, normal) | - | nada (não religar as desligadas) |
| Zernio FB/IG | ok | 0 em erro; 10 posts agendados; último IG 23/10 23:03Z, FB 22:05Z (<12 h) | - | - |
| Buffer TikTok | ok | 0 em erro; fila até 26/10 | - | - |
| fabrica.yml | ok | #verde 23/10 23:58Z (idade ~10 h) | - | - |
| publicar_blog.yml | ok | #verde 24/10 10:44Z (24 min) | - | - |
| blog (ritmo) | ABAIXO do plano | 1 de 4 no ar (limpar-patas 200; plano dia par = 4) | último artigo 23/10 18:33Z (~16 h, <30 h) | CORRIGI parcial: promovi 3 (c6d03b8), só 1 saiu; slow-feed e enriquecer-idosos foram para capas_pendentes (sem foto de animal). Ação: fotos_refazer do slow-feed + disparo da fábrica de artigos (0 rascunhos livres; 6 presos em capas_pendentes). Conferir às 11:19 e re-promover |
| AdSense | 2 FALHA (eram 3) | auditoria 07:2x | CORRIGI: 3 artigos de saúde sem fonte (reforco_blog marcava "revisão" mas não citava fonte e o site é montado de data/seo_onpage/otimizados): adicionei "Fontes e referências" (WSAVA/CFMV/ASPCA), rebuild, commit 2a80750. Restam: 5 sem capa (sem foto de animal, E56) e buraco 15/09-06/10 (histórico, não corrigível) | capas: ficha E56 já aberta |
| Reprovados | pendência | guia-peitoral, cachorro-chorando, passear, gato-sozinho 3/3 ou 2/3 | reescrita esgotada | V07 aberta (Redator) |
| Issue #7 SAUDE 23/10 | aberta | 01:00Z | alerta antigo (1 aprovado fora do ar; guia-peitoral) | mesma causa do reprovado; V07 |
Idade do último resultado: artigo no ar ~16 h; FB/IG <12 h; TikTok com fila; fábrica ~10 h; publicar_blog verde ~16 h. gh CLI funcionou via API nesta rodada.

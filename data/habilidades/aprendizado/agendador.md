# Aprendizado: agendador

Formato: 1 linha por rodada.

| data | jogada | resultado (n/métrica) | mantém/altera/descarta |
|---|---|---|---|
2026-10-23 | agendar pacote velho 'ok' sem uso (sinais-de-envelhecimento) quando fabrica nao entrega | 3 redes 26/10 10:00-11:00, n=1, sem metrica ainda | mantem
2026-10-24 | agendar 4 pacotes aprovados parados (ate 28/10) + gancho banido barrado (gato-morde); TikTok limitado pelo Buffer 10/10 | FB/IG 8 posts ok, TikTok 2 de 5 (3 pendentes), n=4 | mantem; proxima rodada completa TikTok quando a fila liberar
2026-10-26 16:20 | rodada C: estoque ja cobre ate 29/10 A (FB/IG 8 cada, TikTok 8/10); 2 candidatos aprovados barrados pelo portao de gancho (gato-cachorro-convivencia, fonte-agua-medo) | n=2 barrados | mantem
2026-10-28 | 16:3x ciclo C: 0 pacote liberado (2 ok barrados pelo portão; 5 com portão ok mas guardião revisar por clipe repetido/espécie errada/CTA igual) e evergreen sem vídeo na media (purgado) | n=0 agendados | altera: reposição só com pacote novo; fábrica disparada
2026-10-30 | Rodada 12:15: portao de gancho barrou os 2 pacotes ok (agent.py: GANCHO BANIDO); estoque sem reposicao | n=2 pacotes barrados | altera: fabrica disparada via fabrica_disparo.txt
2026-11-01 | Rodada 12:15: estoque FB/IG/TikTok cobre hoje (2 publicados + 2 agendados por rede) e 02-03/11 (3/dia); único pacote ok (gato-morde-carinho) barrado pelo portão (roteiro ainda com gancho banido); fábrica já disparada 08:25 e 11:19, não repetida | n=0 agendados novos | mantém: aguardar fábrica
2026-11-12 | rodada 12:15: pacote direitos-do-consumidor aprovado mas artigo 404 (publicador 13:10 ainda nao rodou) -> nao agendado; TikTok banido (3 posts em erro) | n=1 rodada | mantem: so agendar com artigo 200; tratar TikTok como fora ate Allan resolver

# Aprendizado: auditor_anuncios

Agente: data/painel/agentes/auditor_anuncios.md (contrato de 22/10/2026). Uma linha por rodada. Número ruim = troca de jogada na mesma rodada.

| data | jogada | resultado (n, métrica) | mantém/altera/descarta |
|---|---|---|---|
2026-10-29 | auditoria da campanha VSL v12 ativa (teto R$30/dia) | n=2 anúncios, gasto R$19,31, B lidera CTR/checkout | mantém
2026-10-31 | auditoria 28-31/10 (Windsor + decisão) | n=159 cliques, 9 checkouts, R$ 8,03/checkout, 0 compras conhecidas; C mulheres R$ 4,86 vs B R$ 7,55; gasto R$ 72 > R$ 54 | altera: decisão passa de manter para pausar B (campanha acaba hoje)
2026-11-03 | auditoria 28/10-03/11 (Windsor) | gasto R$177,65, 31 inícios (R$5,73), 0 compras pixel; conjunto DIRETO CHECKOUT B não documentado | altera: conferir toda criação de conjunto novo contra 05 Decisões na leitura

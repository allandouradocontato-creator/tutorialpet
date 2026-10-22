# Auditoria AdSense (2026-10-22)

| Item | Resultado | Detalhe |
|---|---|---|
| pagina sobre | PASSA |  |
| pagina contato | PASSA |  |
| pagina politica-de-privacidade | PASSA |  |
| pagina termos | PASSA |  |
| ads.txt com pub-id | PASSA |  |
| robots.txt nao bloqueia Mediapartners/Google | PASSA |  |
| sitemap.xml | PASSA |  |
| volume >= 30 artigos | PASSA | 60 artigos |
| ultimo artigo <= 2 dias | PASSA | ultimo em 2026-10-21 (1 dias) |
| sem buracos > 3 dias nos ultimos 30 dias | FALHA | buracos: [('2026-09-15', '2026-10-06')] |
| artigos >= 900 palavras | PASSA | 0 curtos: [] |
| estrutura com >= 3 subtitulos | PASSA | [] |
| meta description em todos | PASSA | [] |
| autoria/assinatura visivel | PASSA | [] |
| capa unica por artigo | FALHA | 7 artigos em 3 grupos repetidos |
| sem capa proibida (agressiva) | PASSA | [] |
| todos com capa | FALHA | ['galgo-italiano-temperamento-e-cuidados-da-raca-do-plinio-cachorro-da-anitta'] |
| artigos de saude citam veterinario | PASSA | [] |
| artigos de saude com fonte citada | FALHA | 3 sem fonte: ['vacinas-para-filhote-de-cachorro', 'alimentos-proibidos-para-cachorro', 'plantas-toxicas-para-gatos'] |
| privacidade cita Google/AdSense e cookies | PASSA |  |

## Corrigir (4)
- **sem buracos > 3 dias nos ultimos 30 dias**: buracos: [('2026-09-15', '2026-10-06')] -> manter 1+ artigo/dia
- **capa unica por artigo**: 7 artigos em 3 grupos repetidos -> refazer por tema (config/capas_refazer.txt)
- **todos com capa**: ['galgo-italiano-temperamento-e-cuidados-da-raca-do-plinio-cachorro-da-anitta'] -> gerar capa
- **artigos de saude com fonte citada**: 3 sem fonte: ['vacinas-para-filhote-de-cachorro', 'alimentos-proibidos-para-cachorro', 'plantas-toxicas-para-gatos'] -> citar fonte confiavel

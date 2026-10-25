# Auditoria AdSense (2026-10-25)

| Item | Resultado | Detalhe |
|---|---|---|
| pagina sobre | PASSA |  |
| pagina contato | PASSA |  |
| pagina politica-de-privacidade | PASSA |  |
| pagina termos | PASSA |  |
| ads.txt com pub-id | PASSA |  |
| robots.txt nao bloqueia Mediapartners/Google | PASSA |  |
| sitemap.xml | PASSA |  |
| volume >= 30 artigos | PASSA | 71 artigos |
| ultimo artigo <= 2 dias | PASSA | ultimo em 2026-10-24 (1 dias) |
| sem buracos > 3 dias nos ultimos 30 dias | FALHA | buracos: [('2026-09-15', '2026-10-06')] |
| artigos >= 900 palavras | PASSA | 0 curtos: [] |
| estrutura com >= 3 subtitulos | PASSA | [] |
| meta description em todos | PASSA | [] |
| autoria/assinatura visivel | PASSA | [] |
| capa unica por artigo | PASSA | 0 artigos em 0 grupos repetidos |
| sem capa proibida (agressiva) | PASSA | [] |
| todos com capa | FALHA | ['como-misturar-racao-seca-e-umida-para-cachorro-corretamente', 'como-organizar-a-rotina-de-alimentacao-de-caes-e-gatos-juntos', 'como-ensinar-filhote-a-fazer-xixi-no-tapete-higienico', 'como-tirar-cheiro-de-xixi-de-cachorro-do-quintal', 'como-escovar-pelo-de-gato-que-nao-gosta-de-escova'] |
| artigos de saude citam veterinario | PASSA | [] |
| artigos de saude com fonte citada | PASSA | 0 sem fonte: [] |
| privacidade cita Google/AdSense e cookies | PASSA |  |

## Corrigir (2)
- **sem buracos > 3 dias nos ultimos 30 dias**: buracos: [('2026-09-15', '2026-10-06')] -> manter 1+ artigo/dia
- **todos com capa**: ['como-misturar-racao-seca-e-umida-para-cachorro-corretamente', 'como-organizar-a-rotina-de-alimentacao-de-caes-e-gatos-juntos', 'como-ensinar-filhote-a-fazer-xixi-no-tapete-higienico', 'como-tirar-cheiro-de-xixi-de-cachorro-do-quintal', 'como-escovar-pelo-de-gato-que-nao-gosta-de-escova'] -> gerar capa

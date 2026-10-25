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
| volume >= 30 artigos | PASSA | 72 artigos |
| ultimo artigo <= 2 dias | PASSA | ultimo em 2026-10-24 (1 dias) |
| sem buracos > 3 dias nos ultimos 30 dias | FALHA | buracos: [('2026-09-15', '2026-10-06')] |
| artigos >= 900 palavras | PASSA | 0 curtos: [] |
| estrutura com >= 3 subtitulos | PASSA | [] |
| meta description em todos | PASSA | [] |
| autoria/assinatura visivel | PASSA | [] |
| capa unica por artigo | PASSA | 0 artigos em 0 grupos repetidos |
| sem capa proibida (agressiva) | PASSA | [] |
| todos com capa | FALHA | ['como-misturar-racao-seca-e-umida-para-cachorro-corretamente', 'como-organizar-a-rotina-de-alimentacao-de-caes-e-gatos-juntos', 'como-tirar-cheiro-de-xixi-de-cachorro-do-quintal', 'como-escovar-pelo-de-gato-que-nao-gosta-de-escova', 'como-escolher-comedouro-duplo-elevado-para-gatos-idosos'] |
| artigos de saude citam veterinario | PASSA | [] |
| TODOS os artigos com secao Fontes e referencias (>=2 links) | FALHA | 69 sem fonte: ['como-limpar-manchas-de-lagrima-acida-em-cachorro-branco', 'primeiros-dias-do-filhote-em-casa', 'galgo-italiano-temperamento-e-cuidados-da-raca-do-plinio-cachorro-da-anitta', 'quanto-tempo-um-cachorro-pode-ficar-sozinho'] |
| sem texto de modelo visivel | PASSA |  |
| autor nomeado (pessoa) nos artigos | PASSA | byline ainda 'Equipe Tutorial Pet' |
| Sobre tem secao de equipe/autor | PASSA |  |
| privacidade cita Google/AdSense e cookies | PASSA |  |

## Corrigir (3)
- **sem buracos > 3 dias nos ultimos 30 dias**: buracos: [('2026-09-15', '2026-10-06')] -> manter 1+ artigo/dia
- **todos com capa**: ['como-misturar-racao-seca-e-umida-para-cachorro-corretamente', 'como-organizar-a-rotina-de-alimentacao-de-caes-e-gatos-juntos', 'como-tirar-cheiro-de-xixi-de-cachorro-do-quintal', 'como-escovar-pelo-de-gato-que-nao-gosta-de-escova', 'como-escolher-comedouro-duplo-elevado-para-gatos-idosos'] -> gerar capa
- **TODOS os artigos com secao Fontes e referencias (>=2 links)**: 69 sem fonte: ['como-limpar-manchas-de-lagrima-acida-em-cachorro-branco', 'primeiros-dias-do-filhote-em-casa', 'galgo-italiano-temperamento-e-cuidados-da-raca-do-plinio-cachorro-da-anitta', 'quanto-tempo-um-cachorro-pode-ficar-sozinho'] -> pesquisar fontes reais e inserir antes do fechamento

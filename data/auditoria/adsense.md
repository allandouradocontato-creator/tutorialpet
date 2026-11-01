# Auditoria AdSense (2026-11-01)

| Item | Resultado | Detalhe |
|---|---|---|
| pagina sobre | PASSA |  |
| pagina contato | PASSA |  |
| pagina politica-de-privacidade | PASSA |  |
| pagina termos | PASSA |  |
| ads.txt com pub-id | PASSA |  |
| robots.txt nao bloqueia Mediapartners/Google | PASSA |  |
| sitemap.xml | PASSA |  |
| volume >= 30 artigos | PASSA | 109 artigos |
| ultimo artigo <= 2 dias | PASSA | ultimo em 2026-11-01 (0 dias) |
| sem buracos > 3 dias nos ultimos 30 dias | FALHA | buracos: [('2026-09-15', '2026-10-06')] |
| artigos >= 900 palavras | PASSA | 0 curtos: [] |
| estrutura com >= 3 subtitulos | PASSA | [] |
| meta description em todos | PASSA | [] |
| autoria/assinatura visivel | PASSA | [] |
| capa unica por artigo | PASSA | 0 artigos em 0 grupos repetidos |
| sem capa proibida (agressiva) | PASSA | [] |
| todos com capa | FALHA | ['cachorro-chorando-quando-fico-sozinho-o-que-fazer'] |
| artigos de saude citam veterinario | PASSA | [] |
| TODOS os artigos com secao Fontes e referencias (>=2 links) | FALHA | 4 sem fonte: ['como-escolher-cama-para-cachorro-de-porte-grande', 'quando-castrar-cachorro-filhote-idade-ideal', 'como-adotar-um-gato-adulto-e-por-que-ele-e-mais-facil-do-que-parece', 'como-remover-subpelo-de-cachorro-na-epoca-de-muda'] |
| sem texto de modelo visivel | PASSA |  |
| autor nomeado (pessoa) nos artigos | PASSA | byline ainda 'Equipe Tutorial Pet' |
| Sobre tem secao de equipe/autor | PASSA |  |
| privacidade cita Google/AdSense e cookies | PASSA |  |

## Corrigir (3)
- **sem buracos > 3 dias nos ultimos 30 dias**: buracos: [('2026-09-15', '2026-10-06')] -> manter 1+ artigo/dia
- **todos com capa**: ['cachorro-chorando-quando-fico-sozinho-o-que-fazer'] -> gerar capa
- **TODOS os artigos com secao Fontes e referencias (>=2 links)**: 4 sem fonte: ['como-escolher-cama-para-cachorro-de-porte-grande', 'quando-castrar-cachorro-filhote-idade-ideal', 'como-adotar-um-gato-adulto-e-por-que-ele-e-mais-facil-do-que-parece', 'como-remover-subpelo-de-cachorro-na-epoca-de-muda'] -> pesquisar fontes reais e inserir antes do fechamento

# Auditoria AdSense (2026-10-26)

| Item | Resultado | Detalhe |
|---|---|---|
| pagina sobre | PASSA |  |
| pagina contato | PASSA |  |
| pagina politica-de-privacidade | PASSA |  |
| pagina termos | PASSA |  |
| ads.txt com pub-id | PASSA |  |
| robots.txt nao bloqueia Mediapartners/Google | PASSA |  |
| sitemap.xml | PASSA |  |
| volume >= 30 artigos | PASSA | 77 artigos |
| ultimo artigo <= 2 dias | PASSA | ultimo em 2026-10-25 (1 dias) |
| sem buracos > 3 dias nos ultimos 30 dias | FALHA | buracos: [('2026-09-15', '2026-10-06')] |
| artigos >= 900 palavras | PASSA | 0 curtos: [] |
| estrutura com >= 3 subtitulos | PASSA | [] |
| meta description em todos | PASSA | [] |
| autoria/assinatura visivel | PASSA | [] |
| capa unica por artigo | PASSA | 0 artigos em 0 grupos repetidos |
| sem capa proibida (agressiva) | PASSA | [] |
| todos com capa | FALHA | ['como-misturar-racao-seca-e-umida-para-cachorro-corretamente', 'como-organizar-a-rotina-de-alimentacao-de-caes-e-gatos-juntos', 'como-tirar-cheiro-de-xixi-de-cachorro-do-quintal', 'como-ensinar-filhote-de-gato-a-interagir-com-caes-adultos', 'melhores-petiscos-naturais-mastigaveis-para-saude-dental-de-caes'] |
| artigos de saude citam veterinario | PASSA | [] |
| TODOS os artigos com secao Fontes e referencias (>=2 links) | FALHA | 7 sem fonte: ['como-escolher-fonte-de-agua-ideal-para-gatos-que-tem-medo', 'como-identificar-sinais-de-estresse-em-caes-multicaes-em-espaco-pequeno', 'como-evitar-choque-termico-em-cachorros-nos-dias-quentes', 'como-ensinar-filhote-de-gato-a-interagir-com-caes-adultos'] |
| sem texto de modelo visivel | PASSA |  |
| autor nomeado (pessoa) nos artigos | PASSA | byline ainda 'Equipe Tutorial Pet' |
| Sobre tem secao de equipe/autor | PASSA |  |
| privacidade cita Google/AdSense e cookies | PASSA |  |

## Corrigir (3)
- **sem buracos > 3 dias nos ultimos 30 dias**: buracos: [('2026-09-15', '2026-10-06')] -> manter 1+ artigo/dia
- **todos com capa**: ['como-misturar-racao-seca-e-umida-para-cachorro-corretamente', 'como-organizar-a-rotina-de-alimentacao-de-caes-e-gatos-juntos', 'como-tirar-cheiro-de-xixi-de-cachorro-do-quintal', 'como-ensinar-filhote-de-gato-a-interagir-com-caes-adultos', 'melhores-petiscos-naturais-mastigaveis-para-saude-dental-de-caes'] -> gerar capa
- **TODOS os artigos com secao Fontes e referencias (>=2 links)**: 7 sem fonte: ['como-escolher-fonte-de-agua-ideal-para-gatos-que-tem-medo', 'como-identificar-sinais-de-estresse-em-caes-multicaes-em-espaco-pequeno', 'como-evitar-choque-termico-em-cachorros-nos-dias-quentes', 'como-ensinar-filhote-de-gato-a-interagir-com-caes-adultos'] -> pesquisar fontes reais e inserir antes do fechamento

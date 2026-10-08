# Auditoria semanal — 2026-10-08 (execução de TESTE pedida pelo Allan, 12:11)
Limite: site e app ao vivo NÃO abriram (4ª tentativa; permissão de leitura de URL sem resposta). Site auditado pelo código (build_site.py + site/build); app sem evidência alguma (o código do app não está neste repositório).

## O que está bom
- Fábrica: 5/5 últimas execuções OK (#14–#18); última 15m23s, vídeo+artigo 80% do tempo, sem avisos.
- Já entregue depois da auditoria anterior: banner de cookies (PR #3; Analytics/Clarity só após "Aceitar") e vídeo opcional no corpo (PR #4). Sobre, Contato, Privacidade, Termos, sitemap e robots existem no código.

## Lacunas que impedem fechar o sistema (ordem de impacto) e decisão recomendada
1. Alcance no Facebook ~zero: 15 posts, alcance 1–3, 0 compartilhamentos (nenhum post novo melhorou). 12 de 15 são link com CTA de venda na abertura. Decisão: aprovar a sugestão 3 (CTA e link no 1º comentário, A/B de 6 posts) até 18/10.
2. Vídeo não chega ao blog: o campo existe, mas só 1 dos 25 artigos usa vídeo; a fábrica não preenche video_url sozinha. Decisão: fábrica grava video_url do dia no artigo (custo R$ 0), veredito 17/10.
3. Artigos sem imagem no corpo (só capa) e ads.txt com ID placeholder; sem meta do Search Console. Decisão: imagens no corpo (lazy, alt); Allan cria Search Console e informa o código de verificação; ID do AdSense só quando a conta existir.
4. Aplicativo Sozinho em Casa (prioridade alta): nenhuma auditoria feita. Decisão: liberar o domínio ou colar o texto/prints das telas; sem isso não há avanço.

## Não consegui verificar (e por quê)
- tutorialpet.com.br ao vivo (cookies funcionando, velocidade no celular, vídeo tocando, indexação): WebFetch pede permissão e ninguém responde na rotina.
- sozinho-em-casa.streamlit.app (onboarding, telas, celular): mesmo bloqueio; o código do app não está no repo.
- Search Console e AdSense: sem conexão/credenciais para a rotina.
- Ajuste: pré-aprovar WebFetch para os 2 domínios nas permissões da rotina; dar acesso de leitura ao repo do app; PageSpeed (grátis) via URL liberada.

## Nota da minha capacidade de auditar: 5/10
Forte: ler execuções, métricas do Metricool, código do site, causa raiz e sugestão testável. Falta: ver o produto real (site/app no celular), medir velocidade, ler Search Console, comparar com concorrentes. Com URLs liberadas sobe para ~7.

## Sugestões pendentes (máx. 3; custo R$ 0 todas)
1. Facebook: CTA no 1º comentário, A/B de 6 posts, alcance em 48h. Veredito 18/10/2026.
2. Vídeo do dia no artigo automático + imagens no corpo; medir tempo na página (Clarity) 7 dias. Veredito 17/10/2026.
3. Liberar acesso ao site/app ao vivo e abrir o Search Console. Veredito 10/10/2026.

# Auditoria semanal — 2026-10-08, 2ª rodada (Auditor de Processo)
Limite (2ª rodada seguida): site e app ao vivo NÃO abriram (permissão de leitura de URL sem resposta); nada foi buscado por outro meio. Site auditado pelo código (site/build) — sem mudança desde a rodada anterior; app Sozinho em Casa SEM evidência. Sugestões 1–3 seguem sem decisão do Allan.

## O que está bom
- Fábrica: 5/5 últimas execuções OK (#14–#18). Última (#18, 08/10): 15m23s total; vídeo+artigo 12m15s (80%), repor fila 2m, dependências 36s. Sem avisos, alerta pulado.
- Site: sitemap (31 URLs) e robots.txt no ar (200, ~1s); Sobre, Contato, Privacidade e Termos existem; viewport mobile, canonical e JSON-LD nos artigos; Analytics + Clarity ligados.

## 3 maiores gargalos (causa raiz)
1. Alcance orgânico ~zero no Facebook: 14 posts de 24/09–06/10 = 1–3 pessoas alcançadas, 0 compartilhamentos, 0–1 vídeo. Causa: 12 de 14 são "link" com texto de artigo genérico e CTA do e-book colado no início (R$ 9,90); o Facebook corta alcance de post-link e de abertura vendedora. Os 2 posts "photo" (3 e 2 de alcance) superam os "link" (1–2). Mesmo texto duplicado em photo+link no mesmo minuto (06/10).
2. Blog não está pronto para AdSense: sem banner de consentimento (só texto na política) mas Analytics/Clarity disparam sem consentimento (LGPD); ads.txt com ID placeholder pub-0000000000000000; nenhum <img> no corpo dos 25 artigos (25 imagens existem em site/build/imagens, só servem de capa) e nenhum vídeo, apesar de a fábrica gerar um por dia; sem meta de verificação do Search Console. Causa: build_site.py nunca teve etapa de consentimento nem de mídia no corpo.
3. Vídeo (80% do tempo da rodada) não chega ao blog: o mesmo vídeo diário não é incorporado ao artigo. Causa: pacote vai para branch media e o gerador do site não o lê.

## Sugestões (máx. 3)
1. Banner de cookies grátis (script próprio ~40 linhas no build_site.py; Analytics/Clarity só após "Aceitar"). Custo R$ 0. Ganho: pré-requisito AdSense/LGPD. Teste grátis: abrir o site no celular e conferir no DevTools que gtag/clarity só carregam após aceitar. Veredito: decidir até 14/10/2026.
2. Imagem e vídeo no corpo do artigo (img com loading=lazy e alt; vídeo do dia em <video preload="none" poster>), via build_site.py. Custo R$ 0. Ganho: páginas "ricas" para o AdSense e tempo de leitura. Teste: aplicar em 3 artigos, medir tempo/ página no Clarity por 7 dias. Veredito: 17/10/2026.
3. Facebook: tirar o CTA do e-book da abertura (vai para o 1º comentário) e postar foto/vídeo com link só no comentário, 1 post por artigo. Custo R$ 0. Ganho esperado: sair de 1–3 para dezenas de alcance (hipótese). Teste: 6 posts A/B (vídeo+comentário vs. link atual), comparar alcance/compartilhamentos em 48h. Veredito: 18/10/2026.

## Pendência de acesso
- Para auditar o app e o site ao vivo: o Allan libera tutorialpet.com.br e sozinho-em-casa.streamlit.app para a rotina ou cola aqui o texto das telas do app (onboarding, home, protocolo). Sem isso o domínio 'Aplicativo' (prioridade alta) não avança.

## Evidências
- Execuções: actions/runs/37754499550 (#18, 15m23s: dependências 36s, vídeo+artigo 12m15s, repor fila 2m03s, auditoria 3s, sem avisos) e #14–#17, todas success.
- Métricas: Metricool brand 7123441, posts FB 24/09–06/10 (alcance 1–3, shares 0).
- Código: site/build/*.html (sem <img> no corpo; sem "cookie" fora de politica-de-privacidade.html), site/build/ads.txt.

Dados até 2026-10-09 10:50 (Fortaleza) — Metricool (getScheduledPosts + IGRE/FBRE/TKPO, uma rede por vez, horários UTC-3h), Actions e código conferidos agora.
# Auditoria semanal — 2026-10-09 (Otimizador de Processo)
Limites: tutorialpet.com.br e sozinho-em-casa.streamlit.app NÃO abriram (permissão de URL sem resposta, 7ª vez); repo do app negado (add_repo indisponível). Site auditado pelo código; app sem evidência.

## O que está bom
- Fábrica: 5/5 OK (#20–#24; 10m54s, 7m08s, 6m03s, 6m24s, 7m07s). #24 (06:08 de hoje, rodada agendada) gerou "plantas-toxicas-para-gatos", aprovado sozinho pelo Guardião; etapa Produzir 5m26s, dependências 38s. 2 rodadas/dia já em vigor.
- Facebook virou a rede líder: 12 reels, 2.888 views, 57 curtidas. Gato/água 12:00 de ontem = 942 views/12 curtidas (23h); versão 19:35 = 728/3 (15h). Ambos 'recente (parcial)'.
- Instagram saiu do zero: 143 views em 12 reels; caixa de areia (40h) 75 views, 4 curtidas, 1 compartilhamento, 1 salvo; tempo médio ~4–6 s.
- TikTok: 896 views, 45 curtidas, 1 compartilhamento em 3 posts. Banho 766/39 (43h); "anos" 105/3 (40h); gato/água 25/3 (23h, parcial).

## Posts × rede (idade em h; <48h = recente, parcial)
- Gato/água v1 (23h): FB 942 · IG 20 · TT 25. Gato/água v2 (15h): FB 728 · IG 34 (TT não postou).
- Sozinho (46h): FB 325/8 · IG 5. Caixa de areia (40h): FB 130/6 · IG 75/4. Anos (40h): FB 56/4 · IG 0 · TT 105/3. Banho (44h): FB 28/2 · IG 5 · TT 766/39.
- >48h: meses/rua FB 220 · alimentos 209 · 28/09 221; demais <20. Alcance FB vem 0 (limite da API); TikTok sem alcance/% assistido/Para Você na API.
- Ganchos: pergunta curta sobre problema do pet ("Seu gato quase não bebe água da tigela?", "banho… cheirinho forte?", "quantas horas sozinho") lidera; "Com quantos anos…" fraco (FB 56, IG 0), pausa confirmada. A rede pesa tanto quanto o gancho: banho TT 766 × FB 28; gato/água FB 942 × TT 25.
- CTA: todos usam link no 1º comentário (landing vercel + artigo) e o post de abertura só o institucional; sem diferença mensurável entre CTAs; amostra pequena.
- Correção ao semanal de 08/10: lá IG tinha "0 curtidas" e FB ~114/post; o Metricool atrasa, hoje FB ~240/post e IG teve 4 curtidas. A conclusão "TikTok é a rede que responde" vale só para o banho.

## 3 maiores gargalos (causa raiz)
1. Buraco na publicação: último agendamento foi 08/10 19:35; nada agendado para hoje (10:50) e o pacote de 06:15 está parado há 4h35. TikTok sem post novo desde 08/10 12:00. Causa provável: o Agendador de Posts não rodou/agendou após a mudança para 2 vídeos/dia (a confirmar). Pior: o formato que está rendendo (gato, FB 12h) não é repetido.
2. Instagram com distribuição baixa (média ~12 views/reel), conta nova e CTA/tempo médio de 4–6 s; sem teste isolado ainda.
3. Blog não pronto p/ AdSense: ads.txt com pub-0000…, só 3 de 31 páginas com <img> (25 fotos existem em site/build/imagens), 1 artigo com vídeo; banner de cookies já está nas 31 páginas, política, termos, sobre, contato e sitemap (31 URLs) existem; sem Search Console.

## Como ficar mais rápido e gastar menos
- 2 rodadas/dia já cortou ~50% de Gemini/ElevenLabs; manter até 16/10. Pacotes antigos 'aguardando_revisao' (6) não são reaproveitados: usar um deles para preencher falha do Agendador custa R$ 0.
- Testes de voz/layout só com o pacote do dia. Auditor de terça/sexta sem acesso ao app repete o mesmo texto: liberar acesso ou rodar só 1x/semana.
- Jev para triagem (nota 10): custo ~zero.

## Comprar x produzir / Ferramentas
- PLR traduzido: não para o blog (AdSense exige original); para o 2º e-book vale (US$ 10–40, 2–3 dias vs 1–2 semanas) só após o produto 1 vender. Reavaliar 24/10/2026.
- Assinar agora: nenhuma. Ativar grátis: Search Console, PageSpeed Insights, Bing Webmaster, e-mail grátis (MailerLite/Brevo). Dispensar: anúncios pagos até haver orgânico constante.

## Sugestões (máx. 3, custo R$ 0)
1. Fechar o buraco de publicação: conferir/reativar o Agendador e agendar hoje o pacote "plantas tóxicas" (FB 12h e 17h, TikTok 18h, IG 20h) + 1 antigo se faltar. Ganho: volta a ter 2 posts/dia; teste: getScheduledPosts às 12:00. Veredito 10/10/2026.
2. Repetir a fórmula campeã por 7 dias: gancho de pergunta curta de problema do gato/cachorro, FB 12h–12:30 e TikTok 18h–19h, IG só 1/dia; comparar views/post por rede. Veredito 16/10/2026.
3. Blog: build liga a foto pelo slug (alt+lazy) e Allan cria Search Console e ID real do ads.txt. Ganho: 28 artigos com imagem (requisito AdSense). Veredito 17/10/2026.

## Nota da minha capacidade de auditar: 5/10 (com URLs e repo do app: ~7). Forte: Actions, Metricool, código. Fraco: ver site/app real, PageSpeed, Search Console.

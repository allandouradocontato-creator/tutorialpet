Dados até 2026-10-08 19:11 (Fortaleza) — Metricool, Actions e código conferidos agora. Horários do Metricool vêm em UTC (-3h).
# Auditoria semanal — 2026-10-08 (Otimizador de Processo)
Limites: site e app ao vivo NÃO abriram (permissão de URL sem resposta, 6ª vez); repo do app negado (add_repo indisponível). Site auditado pelo código; app sem evidência. Posts de 08/10 12:00 no FB/IG ainda não aparecem nas métricas (atraso do Metricool): não conclui nada sobre eles; nada novo agendado após 12:00 de hoje até agora.

## O que está bom
- Fábrica: 5/5 últimas execuções OK (#17–#21; 7m08s, 10m54s, 7m08s, 15m24s, 8m). #21 aprovou sozinha (Guardião) o pacote do gato/água. Tempo por etapa não medido nesta rodada.
- TikTok é a rede que responde: 3 posts, 896 views, 45 curtidas, 1 compartilhamento (~300 views/post). Destaques <48h: banho do cachorro 766 views/39 curtidas (27h); "Com quantos anos…" 105 (24h); gato/água 25 em 7h (recente, parcial).
- Facebook (Reels): 10 posts, ~1.141 views, 40 curtidas (alcance vem 0 por limite da API). Destaque: "Quanto tempo o cachorro pode ficar sozinho" 317 views/8 curtidas em 31h; meses/rua 219 (51h).

## Posts <48h (recente, parcial) × rede
- TikTok: banho 766 · anos 105 · gato/água 25. FB: sozinho 317 · anos 51 · caixa de areia 79 (24h) · banho 19 (28h). IG: caixa de areia 6 views/alcance 11 · banho 0 · sozinho 4 · anos 0.
- Ganchos: pergunta ligada à dor do tutor ("cheirinho forte", "quantas horas sozinho") puxa mais que a reflexiva ("Com quantos anos você descobriu…": FB 51, TT 105, IG 0). Mesmo vídeo do banho: TikTok 766 × FB 19 → a rede pesa mais que o gancho; horário 12h–12:30 foi o melhor no FB (317 e 208).
- CTA: todos pedem link no 1º comentário; o comentário com a landing vercel e o institucional rendem igual (sem diferença visível); amostra pequena (3 dias), tratar como indício.
- Redes: TikTok ~300 views/post, Facebook ~114, Instagram ~2 (19 views em 10 reels, 0 curtidas, tempo médio 4–9 s).

## 3 maiores gargalos (causa raiz)
1. Instagram quase sem distribuição (alcance ≤11, 0 curtidas em 10 reels). Causa provável: conta nova sem histórico + 4 posts/dia no mesmo formato; ainda sem teste que isole a causa.
2. Produção acima da necessidade: 4 rodadas/dia (Gemini + ElevenLabs) enquanto só TikTok/FB dão sinal e a amostra é pequena. Gasta crédito sem decidir nada.
3. Blog ainda não pronto p/ AdSense: ads.txt com ID placeholder (pub-0000…), sem Search Console, 31 páginas com só 3 <img>, embora 25 fotos já existam em site/build/imagens (28 artigos sem imagem_capa no front-matter; o build não liga a foto pelo slug). Vídeo no corpo só em 1 artigo.

## Como ficar mais rápido e gastar menos
- Reduzir de 4 para 2 rodadas/dia até haver 7 dias de dados; economia ≈ metade de Gemini/ElevenLabs/minutos de Actions; qualidade igual (o mesmo vídeo vai às 3 redes).
- Postar mais cedo (12h) no FB e priorizar TikTok; pausar teste de IG por 3 dias para isolar causa, sem custo.
- Testes de voz/layout nunca com a rodada completa (erro de 07/10); rotina de terça/sexta sem acesso ao app repete texto: liberar acesso ou reduzir.
- Jev para classificação/triagem (nota 10): custo ~zero; manter.

## Comprar x produzir / Ferramentas
- PLR traduzido: não para o blog (AdSense exige original). Para a esteira (2º e-book pet) vale: US$ 10–40, 2–3 dias contra 1–2 semanas produzindo; só após produto 1 vender. Veredito: reavaliar 24/10/2026.
- Assinar agora: nenhuma. Ativar grátis: Search Console, PageSpeed Insights, Bing Webmaster, MailerLite/Brevo (e-mail grátis). Dispensar: anúncios pagos até haver orgânico consistente e landing única.

## Sugestões (máx. 3, custo R$ 0)
1. Cortar para 2 rodadas/dia e testar horário 12h: custo R$ 0; ganho ≈ -50% de gasto de API. Teste: 7 dias, comparar views médias/post TikTok e FB. Veredito 15/10/2026.
2. Blog: build liga a foto pelo slug (lazy + alt) e grava video_url do dia; Allan cria Search Console. Ganho: 28 artigos com imagem, requisito AdSense. Teste: 3 artigos, 7 dias (Clarity). Veredito 17/10/2026.
3. Liberar leitura de tutorialpet.com.br e sozinho-em-casa.streamlit.app e dar o repo sozinho-em-casa-app à rotina; sem isso o domínio Aplicativo não avança. Veredito 10/10/2026.

## Nota da minha capacidade de auditar: 5/10 (com acesso ao app e URLs: ~7). Forte: Actions, Metricool, código. Fraco: ver produto real no celular, PageSpeed, Search Console.

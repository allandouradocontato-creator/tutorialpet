Dados até 2026-10-16 10:47 (Fortaleza) — Zernio (FB/IG), Buffer (TikTok), Actions (logs reais), manifests da branch media, 20+ rotinas, código do blog e do app lidos agora. tutorialpet.com.br ao vivo NÃO aberto (WebFetch recusou; sem curl por regra): blog auditado pelo código; 11ª rodada sem o app ao vivo (repo lido via GitHub).
# Auditoria semanal — 2026-10-16 (Otimizador de Processo)

## ALERTAS
- publicar_blog #17 (16/10 07:51) FALHOU no push: "cannot pull with rebase: You have unstaged changes". Os 3 artigos aprovados hoje (conviverem-em-paz, bola-de-pelo, frutas-no-verão) foram commitados no runner, mas NÃO chegaram à main: não existem em site/build, ou seja 404 no ar. Os pacotes de vídeo deles (2 "aprovado", 1 "revisar") travam no Agendador (regra "artigo 200"). Mesma classe do erro de 13/10.
- Erros de publicação: nenhum (Zernio posts_list_failed vazio; Buffer sem status error). Contas FB/IG saudáveis (token até 02/12 e 12/12).
- Atraso do cron da fábrica: #66 saiu 13:39Z em vez de 13:00Z (Vigia: 09:00Z e 09:37Z de hoje nem rodaram). Windsor.ai (anúncios) segue pedindo reconexão e o Caçador de referências está suspenso (precisa do PC do Allan).

## Rodadas (log real)
- fabrica.yml: #62–#65 verdes (#64 8 s pela trava de 4 h; #63 11 min; #65 9 min, disparo do Conferente); #66 em andamento. publicar_blog: #14–#16 ok/cancelado, #17 falha (acima). lote.yml: 5/5 verdes (último 08/10). Custo: ~711 créditos ElevenLabs por rodada que produz (ultimo.md); saldo real NÃO lido (workflow creditos_eleven.yml existe; estimativa 30–50% do plano de 39.419 usado desde 07/10).

## O que está bom
- Estoque saudável: Zernio 12 vídeos agendados (FB+IG) até 19/10 19:00; Buffer 7 TikToks até 18/10 20:20 (limite grátis de 10 na fila: cobre ~2,3 dias); 9 pacotes "meme" extra_pronto de reserva. Publicação sem buraco desde 13/10.
- Rotinas v2 OK com os conectores certos: Agendador (08:15/12:15/16:15), Conferente (07:47), Estrategista, Especialista TikTok e Agente de SEO têm Zernio+Buffer e rodaram com sucesso. ads.txt agora com ID real (pub-7204207473239947), verificação Search Console no ar, banner de cookies, sitemap 49 URLs, ?v=hash nas imagens no build.

## Posts × rede (20/09→agora; ≥72h salvo nota)
- Views: Facebook 6.338 (45 posts; 4.955 nos 37 com ≥72h) · TikTok ~2.200 (Buffer, 11 posts de 09/10 em diante, ~200/post; última semana 72–202) · Instagram 697 (22 posts; 283 nos 14 com ≥72h; pulo 68–90%, 11% do FB).
- Campeões (≥72h): gato/água FB 1.013 + 796 + 526 (3 posts); banho TT 893/988; sozinho 7h FB 357. Recentes (<72h, parciais): FB 204–281 views em 16–49 h (consistente); TikTok 14–15/10 72–202 views, tempo médio 2,1–2,8 s (cai de 5–7 s do 09/10): o gancho não segura. Melhor interação recente: "Gato é suspeito? Quem manda na sua casa?" (meme-g1, FB 18 h: 281 views, 16 reações, 4 comentários) e TikTok 15/10 13:20 (202 views, 24 curtidas, 12% engaj.). Amostra pequena, só indício: série de humor engaja mais que o tutorial.
- Rede pesa mais que gancho (mesmo tema: FB 1.013 × TT 577 × IG 22); Buffer não devolve % assistido.

## 3 maiores gargalos (causa raiz)
1. Publicação do artigo é frágil: o passo final de publicar_blog usa `git pull --rebase` com arquivos não adicionados (git add só site/build, data/quality_editor, seo_onpage, visual); basta o runner mexer em outro arquivo para o push cair em silêncio. Sem alarme, o pacote só aparece parado 2–3 h depois.
2. Retenção baixa nos 3 s iniciais (TikTok 2–3 s, IG pulo 68–90%): vídeo de 50–55 s com gancho de pergunta; efeito só será julgável após 72 h do teste de 7 dias (15–21/10).
3. Dependência do PC/login do Allan em rotinas e anúncios: Caçador de referências suspenso (device_absent), Windsor pedindo reconexão, Caçador de estilo e Segurança sem Zernio/Buffer (ainda citam Metricool).

## Como ficar mais rápido e gastar menos (máx. 3)
1. Blindar o passo de push do publicar_blog: trocar por `git add -A site data config; git pull --rebase --autostash; git push` e, se o push falhar, abrir issue (alerta). Custo R$ 0 (1 linha). Ganho: fim do 404 recorrente e de ~3 h de pacote parado/rodada. Teste: workflow_dispatch com os 3 slugs de hoje e conferir 200. Veredito: fazer agora (17/10).
2. Pular vídeo novo enquanto houver ≥5 dias de pacotes prontos (hoje: 12 agendados + 4 aprovados + 9 memes) e usar o estoque meme. Custo R$ 0. Ganho: ~700 créditos por rodada evitada (plano de 39.419 créditos, renova dia 7). Teste: Conferente já conta pacotes prontos; observar créditos em 20/10. Veredito 20/10.
3. Gancho: testar vídeo curto (25–35 s) com gancho de humor/estranhamento nas 3 primeiras palavras, só no TikTok, 1 variável por vez (Especialista TikTok). Custo R$ 0. Ganho: tempo médio >4 s. Teste: 5 posts até 21/10. Veredito 22/10.

## Comprar x produzir / Ferramentas
- Nada a assinar. Dispensar: Metricool (já fora) e Windsor até haver anúncio rodando. Buffer grátis basta (10/fila). PLR: reavaliar 24/10. App: fixar requirements (hoje streamlit>=1.38, pillow>=10.0 sem teto) e token ?k=.

## Tarefas manuais devolvidas ao Allan
- 0 nesta rodada por falha de processo; ficam só identidade/login: reconectar Windsor, 2FA, chave ElevenLabs, verificação TikTok; Claude fecha: push do publicar_blog, artigos 404, produto Kiwify 3JprCCK, recriar Caçador de estilo/Segurança com Zernio+Buffer.

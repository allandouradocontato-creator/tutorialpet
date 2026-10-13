Dados até 2026-10-13 16:30 (Fortaleza) — Zernio (FB/IG), Buffer (TikTok), Actions e código lidos agora; tutorialpet.com.br e streamlit.app NÃO abriram (permissão de URL sem resposta, 9ª vez): site auditado pelo código; app auditado pelo código (repo privado lido pela 1ª vez via GitHub).
# Auditoria semanal — 2026-10-13 (Otimizador de Processo)

## ALERTAS
- Estoque agendado é de ~1,5 dia, não de 5: Zernio tem 3 vídeos (14/10 10:00, 14/10 19:00, 15/10 10:00) e Buffer 3 TikToks (14/10 10:20, 20:20, 15/10 10:20). A nota "10 vídeos agendados" não confere. O pacote aprovado hoje (por-que-o-gato-esconde-a-comida) ainda está "aprovado", sem agendar.
- 3 de 5 rotinas estão cegas: Conferente de Estoque, Estrategista e Especialista TikTok só têm Metricool (bloqueado). Só Agendador e este Otimizador têm Zernio+Buffer.
- Posts "Teste Buffer" (TikTok 12:10), "Teste Zernio" (FB 12:21, IG 12:36; status partial) estão públicos nas contas, duplicando o post real das 11:20.
- Falhas de publicação: nenhuma (posts_list_failed vazio; Zernio e Buffer saudáveis). Publicação ficou parada 10/10 10:20 → 13/10 11:20 (73 h, limite do Metricool); já normalizada.

## O que está bom
- Fábrica 5/5 verdes (#39–#43); só #40 (17m30) e #41 (16m) produziram, as outras 3 pularam em ~8 s pela trava de 4 h. Custo hoje ≈ 2 rodadas × ~538 créditos ElevenLabs ≈ 1.076. publicar_blog 5/5 verdes (45 s hoje, 5 artigos). lote 6/6 verdes (último 08/10).
- Pacote de hoje passou no Guardião (gancho abertura_pare, 16 clipes inéditos, voz eleven_v4). Blog: 39 URLs no sitemap, cookies em 40/40 páginas, privacidade/termos/sobre/contato.
- Repo do app é privado; app.py (443 linhas) sem chave no código.

## Posts × rede (20/09 → agora; idade ≥72h salvo indicação; Zernio IG exato, FB Zernio/Buffer, TikTok Buffer)
- Totais de vídeo: TikTok 6 posts ≥72h = 2.382 views (397/post) [+1 de hoje, 5h, 14 views: recente (parcial)]; Facebook ~3.800 views (Zernio, 15 posts); Instagram 14 posts = 283 views (tempo médio 3–4 s, pulo 63–85%). IG ≈ 4% das ~6.470 views. Compartilhamentos: 4 no total.
- Banho (pergunta concreta; CTA "leia o artigo", 144 h): TikTok 893 views/49 curtidas/1 comp. (campeão) · FB ~252 · IG 0.
- Gato/água (pergunta; 124 h): FB 1.013 · TT 577/30 curtidas · IG 22. Repostado 09/10 (92 h): FB 524 · TT 281 · IG 99.
- Plantas ("pode ser fatal"; CTA "salve", 94 h): FB 333 · TT 309/19 · IG 27. Areia/erro (78 h): FB 295 · TT 191 · IG não saiu. "Com quantos anos" (142 h): FB 237 · TT 131 · IG 0.
- Hoje 11:20 (cachorro sozinho/brinquedos, 5 h, parcial): TT 14 · FB/IG ~0. Leitura: pergunta de problema concreto segue vencedora; a rede pesa tanto quanto o gancho (banho TT 893 × FB 252; gato/água FB 1.013 × TT 577). Sem dado de alcance/% assistido no TikTok (Buffer não devolve).

## 3 maiores gargalos (causa raiz)
1. Estoque curto (1,5 dia). Causa: o fluxo "aprovado → agendado" depende do Agendador e há pacotes parados: 1 aprovado hoje + 9 em "aguardando_revisao" (7 de 06–07/10 sem Guardião, alguns já postados à mão como banho/caixa de areia; 2 com "revisar"). Buffer grátis aceita só 10 na fila por canal.
2. Rotinas decidem no escuro. Causa: conectores ficam fixos na criação da rotina; update_trigger não troca. O Conferente conta estoque no Metricool e pode disparar a fábrica (~538 créditos) sem necessidade ou deixar de disparar.
3. Blog sem AdSense. Causa: ads.txt ainda com pub-0000…; sem Search Console; 13 artigos sem <img> (inclui "escovar dentes", publicado hoje); só 1 página com vídeo; vercel.json sem headers de segurança. App: sem login, quem tem o link abre tudo e o progresso só vive na sessão (arquivo .json) — risco baixo a R$ 9,90, mas fraco para retenção.

## Como ficar mais rápido e gastar menos (máx. 3)
1. Zerar estoque parado antes de produzir mais vídeo. Custo R$ 0. Ganho: Agendador agenda os pacotes antigos que o Guardião liberar (rodar o Guardião retroativo nos 9) e chega a 5 dias sem gastar ~538 créditos/rodada; enquanto estoque ≥5 dias, pular a rodada de vídeo. Teste grátis: rodar o Guardião nos 9 e contar quantos ficam "ok". Veredito 15/10/2026.
2. Recriar Conferente, Estrategista e Especialista TikTok com Zernio+Buffer (Claude executa, nada para o Allan). Custo R$ 0. Ganho: contagem de estoque e métricas reais, sem disparo de fábrica por engano. Teste: próxima rodada do Conferente (14/10 07:47) deve listar posts do Zernio/Buffer. Veredito 14/10/2026.
3. AdSense/blog: Claude liga foto por slug nos 13 artigos, põe headers no vercel.json e trava o app por link com token (?k=, checado no app, entregue pela Kiwify). Allan só fornece o ID do AdSense e autoriza o Search Console. Custo R$ 0. Ganho: requisitos de aprovação e produto protegido. Veredito 17/10/2026.

## Comprar x produzir / Ferramentas
- PLR traduzido: não serve ao blog (AdSense quer original); para 2º e-book só após o produto 1 vender. Reavaliar 24/10/2026.
- Assinar: nada agora. Zernio (uso 0 créditos) e Buffer grátis bastam; só olhar upgrade do Buffer se a fila passar de 10/canal. Dispensar: Metricool (já fora; deixar só leitura do histórico) e os canais FB/IG duplicados no Buffer. Anúncios pagos só com orgânico constante.

## Tarefas manuais devolvidas ao Allan
- 0 novas nesta rodada. Abertas só por exigirem identidade/2FA: ID AdSense, Search Console, 2FA, chave ElevenLabs, verificação TikTok. Automatizáveis por Claude: tratar o produto Kiwify duplicado (3JprCCK), apagar posts de teste (FB via Zernio; IG/TikTok pelo navegador logado) e recriar as 3 rotinas.

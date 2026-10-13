Dados até 2026-10-13 16:41 (Fortaleza) — Zernio (FB/IG), Buffer (TikTok/estoque), Actions, manifests (branch media), triggers e código lidos agora. Metricool histórico não consultado (fora do plano; Zernio+Buffer cobrem 20/09→hoje). tutorialpet.com.br conferido por curl (HTTP); streamlit.app NÃO aberto: app auditado pelo código (repo lido via git; 10ª rodada sem abrir o app ao vivo).
# Auditoria semanal — 2026-10-13 (Otimizador de Processo)

## ALERTAS
- Pacote aprovado hoje (por-que-o-gato-esconde-a-comida-na-tigela, 13:12) NÃO foi agendado: o Agendador das 15:15 rodou OK (3 min), mas o artigo dá 404 (slug fora de config/blog_aprovados.txt) e a regra "aguardando artigo" bloqueia o agendamento. Estoque agendado: 3 vídeos Zernio (14/10 10:00, 14/10 19:00, 15/10 10:00) + 3 Buffer TikTok (14/10 10:20, 20:20, 15/10 10:20) = ~1,7 dia; a nota "10 vídeos/5 dias" segue errada.
- Conferente (07:47), Estrategista e Especialista TikTok continuam SÓ com Metricool+Windsor (sem Zernio/Buffer). Conferente de amanhã vai contar estoque às cegas e pode disparar fábrica (~538 créditos) sem necessidade. Só Agendador e Otimizador têm Zernio+Buffer.
- Erros de publicação: nenhum (posts_list_failed vazio). Posts de teste ("Teste Buffer" TikTok, "Teste Zernio" FB+IG) seguem públicos, duplicando o real das 11:20.

## Rodada extra 16:42 (pedido do Allan): por que só 3 vídeos e nada hoje à noite
- Divergência: "10 vídeos em 5 dias" era a META do adendo do Agendador, não o agendado. Em 13/10 11:17 só 3 pacotes estavam prontos (ração, brinquedos, enxoval) e foram agendados; dos 16 pacotes, 8 estão "aguardando_revisao" (sem Guardião) e 1 aprovado sem artigo no ar. Hoje à noite (FB 19:00/TikTok 20:20) ficou vazio porque o pacote do turno B não existia a tempo e o aprovado das 13:12 travou no 404. Zernio e Buffer reconferidos agora: iguais ao que o Allan vê (3 + 3).
- Correção: (1) publicar o artigo de hoje e deixar o Agendador agendar o pacote (slot livre mais próximo); (2) rodar Guardião retroativo nos 8 parados; (3) Conferente/Estrategista/Especialista TikTok confirmados só com Metricool+Windsor — recriar com Zernio+Buffer; nota 11 corrigida.

## O que está bom
- Fábrica 5/5 verdes (#39–#43): só #40 (17m30) e #41 (16m) produziram; #39/#42/#43 saíram em ~8 s pela trava de 4 h (economia). Custo hoje ≈ 2 × 538 = ~1.076 créditos ElevenLabs. publicar_blog 5/5 verdes (45 s; 5 artigos aprovados hoje). lote 5/5 verdes (último 08/10).
- Guardião aprovou o pacote de hoje (gancho abertura_pare, 16 clipes inéditos, eleven_v4). Publicação normalizada desde 13/10 11:20 após 73 h parada. Agendador saudável e Metricool de agendamento desativado.

## Posts × rede (20/09→agora; idade ≥72h salvo nota; vídeos com views)
- Views: Facebook 4.942 (Zernio, 15 vídeos, ~330/post) · TikTok 2.382 (Buffer, 6 posts ≥72h, 397/post) · Instagram 283 (Zernio, 14 posts, ~20/post; pulo 63–85%, 3–4 s). IG ≈ 4% do total; compartilhamentos: TikTok 3, IG 1, FB 0.
- Gato/água (pergunta concreta; 125 h): FB 1.013 (+796 no 2º post, 117 h; +525 repost, 92 h) · TT 577/30 curtidas · IG 22. Banho (144 h, CTA "leia o artigo"): TT 893/49 curtidas (campeão) · FB 35 · IG 0 — Zernio mostra FB 35, o ~252 antigo (Metricool) divergia: vale o Zernio. Plantas ("pode ser fatal", 94 h): FB 333 · TT 309 · IG 27. Areia/erro (78 h): FB 300 · TT 191. "Com quantos anos" (142 h): FB 64 · TT 131 · IG 0 (pausado, correto).
- Hoje 11:20 (cachorro ansioso sozinho, 5 h, parcial): TT 14 views · FB/IG ainda sem leitura. Pergunta de problema concreto segue vencendo; o efeito da REDE é grande (banho TT 893 × FB 35; gato/água FB 1.013 × TT 577) → testar o mesmo vídeo em horários trocados antes de concluir gancho. Buffer não devolve % assistido do TikTok (tempo médio 5–7 s).

## 3 maiores gargalos (causa raiz)
1. Estoque curto por etapa manual escondida: aprovar o artigo (foto + blog_aprovados.txt) não acontece junto com a aprovação do pacote; o Agendador exige artigo 200 e para. Hoje: 1 aprovado travado + 8 em "aguardando_revisao" (16 pacotes: 6 agendados). Quem fecha a ponta é o Conferente, que está cego.
2. Rotinas decidem no escuro: conectores são fixados na criação e update_trigger não troca; 3 de 5 rotinas que medem ou contam posts sem Zernio/Buffer.
3. Blog sem AdSense: ads.txt ainda pub-0000000000000000; sem Search Console; 13 artigos sem <img> (de 35; ligar foto por slug); só 1 página com vídeo; vercel.json sem headers de segurança. App (443 linhas): sem login nem token (quem tem o link abre tudo), requirements sem versão fixa (streamlit>=1.38, pillow>=10.0), progresso só na sessão.

## Como ficar mais rápido e gastar menos (máx. 3)
1. Ligar "aprovar pacote" a "aprovar artigo": o Agendador/Conferente adiciona o slug (foto candidata 1) em blog_aprovados.txt no mesmo passo, e o Guardião retroativo libera os 8 parados. Custo R$ 0. Ganho: estoque de 1,7 → 5 dias sem gastar ~538 créditos/rodada (pular vídeo novo enquanto estoque ≥5 dias). Teste grátis: acrescentar hoje o slug de hoje e ver o Agendador das 08:15 agendá-lo. Veredito 14/10/2026.
2. Recriar Conferente, Estrategista e Especialista TikTok com Zernio+Buffer (Claude cria a partir de sessão com os conectores; nada para o Allan). Custo R$ 0. Ganho: estoque e métricas reais, sem disparo falso. Teste: 14/10 07:47 deve listar posts Zernio/Buffer; senão desativar o Conferente até recriar. Veredito 14/10/2026.
3. AdSense/app: Claude liga foto por slug nos 13 artigos, headers no vercel.json, fixa versões do requirements e trava o app por token ?k= entregue pela Kiwify. Allan só dá o ID do AdSense e autoriza o Search Console. Custo R$ 0. Veredito 17/10/2026.

## Comprar x produzir / Ferramentas
- PLR: não serve ao blog (AdSense quer original); 2º e-book só após o 1º vender. Reavaliar 24/10/2026. Assinar: nada. Zernio e Buffer grátis bastam; olhar upgrade do Buffer só se a fila passar de 10/canal. Dispensar: Metricool (só leitura de histórico) e os canais FB/IG duplicados no Buffer. Economia: manter a trava de 4 h; ElevenLabs só em rodada que o estoque exigir.

## Tarefas manuais devolvidas ao Allan
- 0 novas nesta rodada. Abertas só por exigirem identidade/2FA: ID AdSense, Search Console, 2FA, chave ElevenLabs, verificação TikTok. Claude executa: produto Kiwify duplicado (3JprCCK), apagar posts de teste, recriar 3 rotinas, artigo de hoje.

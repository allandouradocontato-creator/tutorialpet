# Auditoria semanal — 2026-10-08 (Otimizador de Processo; rodada de teste 12:47)
Limites: site e app ao vivo NÃO abriram (5ª vez; permissão de URL sem resposta) e o repo do app não está liberado nesta rotina (add_repo indisponível). Site auditado pelo código/build; app sem evidência.

## O que está bom
- Fábrica: 5/5 últimas execuções OK (#14–#18), sem avisos, alerta de issue nunca disparou.
- Já mesclado: cookies LGPD (PR #3), vídeo opcional no artigo (PR #4). Sobre, Contato, Privacidade, Termos, sitemap e robots existem.

## 3 maiores gargalos (causa raiz)
1. Alcance quase zero em todas as redes (20/09–06/10): Facebook 21 posts, alcance 0–4, 0 compartilhamentos; Instagram 6 reels, alcance 0–4; TikTok sem nenhum post no Metricool. Causa: contas novas sem audiência e conteúdo = link de artigo; nenhum gancho/CTA se destacou (amostra pequena, nada >4). Único sinal: 2 posts de foto de 06/10 tiveram 2–3 cliques (podem ser cliques do próprio Allan).
2. Destino do link inconsistente: o CTA de venda aponta para 3 lugares (checkout Kiwify NcQChat, checkout 3JprCCK, app streamlit que dorme) e não para a landing vercel, contrariando a regra "landing única". Em 06/10 cada artigo saiu 2x (foto + link) com texto igual, no mesmo minuto. Causa: texto e link montados em dois pontos diferentes, sem checagem de destino.
3. Blog ainda não pronto para AdSense: ads.txt com ID placeholder (pub-000…), sem meta do Search Console, só 3 das 31 páginas têm <img> (artigos sem imagem no corpo, sem lazy-load), vídeo no corpo depende de preenchimento manual. Causa: build_site.py não puxa imagem nem video_url do pacote da fábrica.

## Como ficar mais rápido e gastar menos
- Rodadas manuais: 5 execuções "workflow_dispatch" em 07/10 (cada uma = artigo Gemini + voz + vídeo, ~6 min). Testes de voz/layout devem usar modo sem ElevenLabs/Gemini ou reaproveitar o pacote do dia.
- Rodada agendada de hoje levou 15m23s contra 5–8m das manuais: etapa "Produzir" 12m15s vs 5m20s e "Repor fila" 2m vs 53s. Provável retentativa por cota do Gemini (429); registrar tempo por chamada no auditor 25 para confirmar.
- Postar 1x por artigo (foto OU link), não 2x: corta 50% dos posts e do ruído sem perder alcance (já é ~0).
- Auditor 2x/semana sem URL liberada repete o mesmo texto: gasto de tokens sem dado novo.

## Comprar x produzir (PLR)
- PLR traduzido: NÃO para o blog (AdSense reprova texto não original; Gemini grátis já gera 1 artigo/dia). Só vale para a esteira (2º e-book pet) depois do sistema fechado; estimativa US$ 10–40 por pacote, 2–3 dias para traduzir/adaptar contra ~1–2 semanas produzindo. Veredito: adiar; reavaliar 24/10/2026.
## Ferramentas: assinar x dispensar
- Assinar agora: nenhuma paga. Ativar grátis: Search Console, PageSpeed Insights, Bing Webmaster (Clarity já ligado após cookies). Ganho: indexação e velocidade medidas.
- Dispensar/pausar: ElevenLabs/Gemini em rodadas de teste; anúncios até haver landing única e orgânico >0 (regra do Guardião de Gasto).

## O que me impede de auditar site e app ao vivo
1. WebFetch pede permissão por URL e ninguém responde na rotina: pré-aprovar tutorialpet.com.br e sozinho-em-casa.streamlit.app.
2. Repo do app (sozinho-em-casa-app) fora do escopo desta rotina e add_repo indisponível: liberar leitura.
3. Sem Search Console/AdSense/PageSpeed conectados.

## Nota da minha capacidade de auditar: 5/10 (com 1 e 2 liberados: ~7)
Forte: Actions, Metricool, código do site, causa raiz. Fraco: ver o produto real no celular, medir velocidade, ler Search Console.

## Sugestões (máx. 3, custo R$ 0)
1. Landing única + 1 post por artigo: publicador usa só sozinhoemcasa-kohl.vercel.app?utm_… no 1º comentário e remove o duplicado foto+link. Ganho: dados limpos de clique e metade dos posts. Teste: 6 posts, cliques por UTM em 7 dias. Veredito 15/10/2026.
2. Blog para AdSense: build puxa imagem da fábrica para o corpo (lazy+alt) e grava video_url do dia; Allan cria Search Console e informa o código. Ganho: tempo na página (Clarity) e requisitos do AdSense. Teste: 3 artigos novos, 7 dias. Veredito 17/10/2026.
3. Liberar WebFetch para tutorialpet.com.br e sozinho-em-casa.streamlit.app e dar o repo do app à rotina; sem isso o domínio Aplicativo (prioridade alta) não avança. Veredito 10/10/2026.

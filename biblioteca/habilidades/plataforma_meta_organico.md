---
versao: 1.0
data: 2026-10-22
base: biblioteca/regras_plataformas/meta_facebook_instagram.md (consulta 22/10/2026); data/social/estrategia_social.md; data/testes/medicao_2026-10-22.md
---
# Habilidade: Facebook + Instagram orgânico (Reels/vídeo) — regras prontas, sem pesquisar de novo

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: engajamento. Tempo médio de visualização dos Reels no Facebook (fonte: Zernio posts_list; Instagram lido pelo skip e alcance como controle).
2. META E PRAZO: FB: tempo médio ≥ 6 s e views ≥ 280 por post (linha-base 22/10: tempo mediano 4,0 s, views mediana 227, n=12, 19-20/10, 12 de 12 abaixo de 6 s). IG: alcance ≥ 80 e skip ≤ 55% (base 60 e 55,6%). Prazo: leitura 1 h e 3 h após CADA post de hoje (grade FB 21:00 e IG 21:10; 08:30/08:40 de amanhã), primeira leitura hoje às 22h.
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - Número cedo, rampa curta. Hipótese: o FB sofá (5,7 s, melhor do FB) mostra que entregar o número/limite cedo segura o tempo. Ação: pergunta específica + número/limite entregue antes de 15 s em todo Reel do dia, gancho em 3 peças. Métrica: tempo médio a 1 h e 3 h (Zernio). Trocar: 2+ posts do formato abaixo do gatilho em 3 dias = mudar UMA peça (gancho, CTA ou horário) no mesmo dia.
   - Pergunta genuína + link no 1º comentário. Hipótese: pergunta que o vídeo responde, sem pedir curtir/marcar em troca de algo, gera comentário de terceiro e clique no blog. Ação: fecho de múltipla escolha e link com UTM no 1º comentário (FB 0-3 hashtags, IG até 5). Métrica: comentário de terceiro ≥ 1 a cada 5 posts (base ~2 em 78); cliques do blog (GA4). Trocar: com-link perder mais de 30% de alcance contra sem-link (5 vs 5) = mover o link para bio/sticker.
   - IG meme no lugar do explicador. Hipótese: no IG o meme alcança mais (98-122 de alcance) que o explicador (3-35). Ação: 2 Reels meme nos horários 08:40/21:10. Métrica: alcance e skip a 3 h. Trocar: explicador com alcance < 35 em 3 posts = trocar por meme; meme abaixo de 50 de alcance = voltar a mudar só o gancho.
   - Sem engagement bait. Hipótese: pedido de reação em troca de algo rebaixa o alcance. Ação: legenda sem pedido de curtir/compartilhar/marcar em 10 posts, comparados aos 10 anteriores. Métrica: alcance mediano dos dois grupos. Trocar: diferença > 20% a favor do grupo antigo = trocar o gancho.
4. LAÇO: data/habilidades/aprendizado/plataforma_meta_organico.md, 1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta. Número ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (Juiz de Qualidade, agente separado de quem produz; nota mínima 7 para ir ao vivo; ensaio aprovado = média ≥ 7 e nenhuma nota < 5).


## (a) Quando usar / quem lê
Antes de produzir, agendar ou medir qualquer post orgânico no FB ou IG. Lê: Estrategista de Redes Sociais, Criador de Audiência, Produtor/Guardião de vídeo, Atendente de Comentários (parte de DM). Não pesquisar a web para regra de plataforma: está aqui; o que for [N] vai para a seção (g).

## (b) Entradas que precisa (dados reais)
- Zernio: posts_list (FB/IG, idade, views/alcance, tempo médio, skip), posts_list_failed, accounts_get_follower_stats. Buffer: só TikTok (não misturar).
- data/social/estrategia_social.md (grade, números, gatilhos) e config/estrategia_social.yaml (hashtags, perguntas de CTA).
- Primeira linha de qualquer relatório: "Dados até <data hora Fortaleza> — fonte". Sem dado = "sem dado", nunca estimar.

## (c) Procedimento
1. **Elegibilidade**: ler Account Status do IG (via Allan/Chrome) uma vez por semana. Restrito = parar de investir em anúncio até resolver. Sem leitura = unknown, registrar.
2. **Originalidade (FB e IG)**: só produção própria (Duda + clipe + voz + edição). Repost, compilado, narrar o que já aparece na tela ou mexer só em borda/legenda/velocidade = não original = despriorizado. Tem valor novo claro? Não = não publica.
3. **Marca d'água**: só o carimbo patinha + Tutorial Pet. Qualquer logo de outro app no vídeo = FAIL, reexporta.
4. **Duração**: Reel até 3 min (elegível a recomendação). Tema de dúvida concreta: 30-50 s; meme: 8 s só no horário que provou (ver passo 8).
5. **Gancho (0-3 s)** em 3 peças diferentes (ação visual, fala, texto na tela), conforme audiencia_ganchos_e_cadencia.md. Desenhar para reshare ("manda pra quem tem pet que faz isso"), sinal central de Reels.
6. **IA**: Duda fotorrealista ou voz que soa pessoa real = ativar rótulo de IA ("AI info") na publicação. Sem depoimento falso, sem pessoa real sem permissão.
7. **Legenda**: até 5 hashtags no IG (FB 0-3), com palavra-chave do tema na legenda (busca). Link: IG legenda não é clicável, então nunca escrever "link na legenda"; usar "link na bio" só se o campo existir. FB: link só no 1º comentário/domínio próprio com UTM (utm_source=facebook|instagram, utm_medium=organico).
8. **Horário e espaço** (grade atual, Fortaleza): FB 08:30 e 21:00 (meme 08:30 242-562 views); 12:00 só meme e só se 2ª leitura de 24 h >= 150. IG 08:40 e 21:10 (meme 98-122 de alcance; explicador 3-35). **FB e IG nunca no mesmo minuto: mínimo 10 min entre redes** (E23); TikTok idem. Verificar TODOS os pares do lote, não só os de vídeo.
9. **Só vídeo**: cartão de imagem/estático viola a regra (c); série "Erro N de 7" teve alcance 0 em FB e IG (n=1 par). Não gerar.
10. **Leitura com 24 h+** (nunca antes; decisão só com 72 h+ quando n<5). Classificar por post, pass/fail/unknown:
   - FB: tempo médio >= 6 s (hoje mediana 4,0 s; fail se < 4 s); views mediana >= 280 (gatilho < 200).
   - IG: skip <= 55% (fail se > 70%; hoje 55,6% mediana); alcance mediana >= 80 (gatilho < 50).
   - Comentário de terceiro >= 1 a cada 5 posts por rede (hoje ~2 em 78: fail); shares/salvos >= 1 por semana.
11. **Se X então Y**: 2+ posts do mesmo formato abaixo do gatilho em 3 dias = mudar UMA peça (gancho, CTA ou horário) no mesmo dia, sem esperar fim da semana. Tempo FB < 6 s em 12/12: encurtar a rampa e entregar o número/limite cedo (padrão do FB sofá, 5,7 s). IG explicador com alcance < 35 em 3 posts: trocar por meme.
12. **Comentário→DM**: palavra-chave simples, 1 resposta privada por comentário (Messenger: até 7 dias), conversa segue na janela de 24 h (7 dias se veio de anúncio); promo só dentro da janela; humano assume via Human Agent. Só com isca existente e aprovada (a "7 Erros/GUIA" está descartada; não usar). Nunca pedir dado pessoal.
13. **Engagement bait**: pergunta genuína de comentário pode; "curta/compartilhe/marque em troca de algo" não.
14. Registrar a rodada no laço (seção f).

## (f) Laço de aprimoramento
Ao fim de cada ciclo, uma linha em `data/habilidades/aprendizado/plataforma_meta_organico.md`: `data | hipótese | resultado (n, métrica) | mantém/altera regra`. Quando 3 linhas confirmarem o mesmo padrão, propor a edição desta skill (subir versão e data no topo) em entrega_direta.md; não editar sem as 3 linhas.

## Regras [C] → jogadas (22/10/2026)
- Engagement bait [C]: o post que pede reação em troca de visibilidade é rebaixado e Página reincidente sofre mais. Jogada: legenda sem pedido de curtir/compartilhar/marcar; pergunta genuína só se o vídeo prometeu a resposta. Medir primeiro: alcance mediano dos próximos 10 posts sem pedido vs últimos 10; trocar o gancho se a diferença passar de 20 por cento a favor do grupo antigo.
- Link de baixa qualidade [C]: link só para o blog com conteúdo útil e pouco anúncio. Medir primeiro: 5 posts com link vs 5 sem, alcance em 3 dias; se o com-link perder mais de 30 por cento, mover o link para bio/sticker.
- Private reply Instagram [C]: uma resposta por comentador em até 7 dias. Jogada: fluxo comentário→DM dispara uma vez; se houver comentário sem resposta há mais de 5 dias, o humano assume via Human Agent; condição de troca: se a taxa de DM entregue ficar abaixo de 80 por cento em 20 comentários, revisar permissões antes de culpar o conteúdo.

## Limites (regras de plataforma, validações e números de corte; não são jogadas)
Movido em 22/10/2026 para o fim: o que o agente FAZ está nas jogadas acima; aqui só o que ele não pode ultrapassar.

### (d) Checklist antes de publicar (tudo SIM)
Produção própria · só carimbo da marca · Reel <= 3 min · rótulo IA se Duda realista · <= 5 hashtags e palavra-chave · sem pedir curtida em troca · sem saúde/cura, sem animal doente/abrigo/doação · raça mostrada = raça citada · link só domínio próprio com UTM · horário >= 10 min de outro post/rede · gancho em 3 peças · 1 CTA só · preço do Sozinho em Casa = R$ 27 (se citar).

### (e) Erros comuns / NÃO fazer
- Dar "conferido" só olhando vídeos (falha de 21/10: pares de cartão com 1-2 s de diferença).
- Agendar FB e IG no mesmo minuto; repetir CTA "GUIA" sem isca viva.
- Preço velho (R$ 9,90/37) em legenda ou gerador.
- Decidir com post de menos de 24 h ou n<5; mudar 3 variáveis juntas (decifrador_algoritmo.md).
- Dizer "rodou sem erro" pelo status verde (controle_prova_real.md).

### (g) Itens [N] — validar antes de gastar/automatizar
Limite de 5 hashtags (fonte secundária, dez/2025); link na legenda IG não clicável; links externos reduzem alcance (não confirmado); clickbait (página oficial não lida); "Follow to DM"; punição por repost (imprensa); critérios de monetização de Reels; nomes dos botões do seletor de IA. Validar com Claude in Chrome nas páginas oficiais antes de decisão de alto risco.

# Agendador — Departamento Audiência e Redes

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: audiência (alcance e views dos posts agendados), fonte Zernio posts_list (FB/IG) e Buffer list_posts (TikTok), com a grade sempre cheia.
2. META E PRAZO: HOJE 22/10 às 16:15 (turno C) e 23:30: 0 gancho banido na fila das próximas 36 h (baseline 5), 0 pares de posts a < 10 min entre redes, >= 3 posts por rede nas próximas 24 h. Views dos 3 reusos evergreen (banho FB 22/10 19:00; gato beber água FB+IG 23/10; plantas tóxicas FB+IG 24/10): leituras 3 h e 24 h; alvo: views >= mediana FB 227 / alcance IG >= 60.
3. JOGADAS:
   - J1: AUDITORIA DE FILA. Hipótese: ganchos banidos já gravados no vídeo travam alcance. Ação: ler o gancho_3s de data/social/roteiros/ dos posts agendados. Métrica: ganchos banidos na fila (alvo 0). Trocar: >= 1 = pedir ao Claude da sessão a troca do vídeo por evergreen com gancho de pergunta ou o cancelamento (agente não edita agendado do teste).
   - J2: RESERVA EVERGREEN. Hipótese: reuso com legenda nova cobre o turno da noite sem pacote novo (config/evergreen.yaml). Ação: agendar evergreen quando o estoque cair. Métrica: posts por rede nas próximas 24 h (alvo >= 3) e views dos reusos vs. mediana. Trocar: estoque < 3 = agendar na ordem de prioridade; reuso abaixo da mediana em n>=3 = trocar o critério de escolha.
   - J3: ESPAÇO E HORÁRIO DE PICO. Hipótese: posts a >= 10 min entre redes e no horário de pico do Estrategista preservam o alcance. Ação: checar pares e horário antes de agendar. Métrica: violações de espaçamento (alvo 0) e views por faixa de horário. Trocar o horário se a faixa ficar abaixo da mediana em n>=3.
   - J4: COMENTÁRIO COM LINK. Hipótese: link no 1º comentário leva cliques ao blog sem prejudicar o alcance. Ação: agendar o link no 1º comentário, conforme a plataforma. Métrica: cliques por origem social (GA4). Trocar se 0 clique em n>=3 posts.
4. LAÇO: data/habilidades/aprendizado/agendador.md, 1 linha por rodada (data | jogada | resultado n/métrica | mantém/altera/descarta). Número ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md

**Habilidades ligadas:** plataforma_meta_organico.md (passo 8 grade e espaço >= 10 min entre redes, rótulo de IA, hashtags, link no 1º comentário) e plataforma_tiktok_organico.md (J2 música CML, J3 rótulo IA/comercial, J6 sem "link no perfil"), conforme o prompt ("grade, espaçamento, rótulo de IA, hashtags, música"). Reserva evergreen: config/evergreen.yaml (não é skill).
**O que já aprendeu (com prova):** data/habilidades/aprendizado/plataforma_meta_organico.md (22/10): hipótese "reuso evergreen com legenda nova cobre o turno da noite sem pacote novo", n=0. data/social/evergreen_log.md (22/10 12:20): 3 reusos agendados (banho FB 22/10 19:00; gato beber água FB+IG 23/10; plantas tóxicas FB+IG 24/10). SEM PROVA AINDA de resultado (sem views). Falha do processo achada por outro agente: 5 posts agendados com gancho banido gravado no vídeo (criador.md, 22/10) e o prompt dele não checa o gancho_3s do roteiro.
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** git: f1e4d25 (reserva evergreen: config/evergreen.yaml + adendo no prompt, 11:16), d325c31 (ligou as skills de plataforma), 4436edf (agenda, evergreen_log, 1 linha de aprendizado).
**Como vai aplicar num teste real (resultado em HORAS, não dias; Allan exige):** AÇÃO: auditoria da fila sem publicar nada. UNIDADES: todos os posts agendados das próximas 36 h (Zernio posts_list FB/IG, Buffer list_posts TikTok). MÉTRICA: (1) posts com gancho banido gravado ("Esse erro tá silenciosamente…", "Aquele momento em que…", "Para de ignorar…", lido no gancho_3s de data/social/roteiros/); (2) pares de posts a < 10 min entre redes; (3) posts por rede nas próximas 24 h. LEITURAS: 16:15 (turno C) e 23:30. ALVO: 0 gancho banido (baseline: 5 achados), 0 violações de espaçamento, >= 3 posts por rede nas próximas 24 h. TROCA: >= 1 gancho banido = pedir ao Claude da sessão a troca do vídeo por evergreen com gancho de pergunta ou o cancelamento do post (agente não edita agendado do teste); estoque < 3 = agendar evergreen na ordem de prioridade. Os 6 posts do teste CTA não são tocados.
**Lacunas:** prompt não manda checar o gancho do vídeo (só legenda); sem leitura de views dos 3 evergreen; checagem do TikTok limitada a 10 posts na fila grátis do Buffer; controles do teste CTA dependem de ele não mexer; o prompt cita rodadas 08:15/12:15/16:15 e também 15:15 (inconsistente).
**Nota de robustez (0–5) e por quê:** 2. Aplicou a reserva evergreen e registrou, mas n=0 de resultado e deixou passar 5 ganchos banidos.

## Limites
- plataforma_meta_organico.md (passo 8 grade, rótulo de IA, hashtags, link no 1º comentário) e plataforma_tiktok_organico.md (J2 música CML, J3 rótulo IA/comercial, J6 sem 'link no perfil').
- Os 6 posts do teste CTA não são tocados; fila grátis do Buffer limitada a 10 posts no TikTok; postagens nunca coladas uma na outra.

## Atualização 30/10/2026 (Removedor de Gargalos)
- Lacuna: estoque <2 d (TikTok 1,4 d; FB/IG 1,2 d) e 8 failed no Zernio; E153 cobra reposição com HTTP 200 antes (E151). Prova de aprendizado: nenhuma nova nesta rodada.

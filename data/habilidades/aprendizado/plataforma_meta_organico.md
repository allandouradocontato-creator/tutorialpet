# Aprendizado: plataforma_meta_organico

Skill: biblioteca/habilidades/plataforma_meta_organico.md (v1.0, 22/10/2026). Uma linha por ciclo. Com 3 linhas confirmando o mesmo padrão, propor a edição da skill (versão e data no topo) em entrega_direta.md.

| data | hipótese | resultado (n, métrica) | mantém/altera regra |
|---|---|---|---|
2026-10-22 | hipótese: reuso evergreen com legenda nova no FB/IG cobre o turno da noite sem pacote novo | resultado: n=0 (medir com 72h+) | mantém
2026-10-22 | passo 13 (pergunta genuína de comentário pode, sem 'curta/marque') + passo 8 (>=10 min entre redes, mínimo 20 min entre os 6 posts) | resultado: n=2 posts Meta teste (FB 6ad8a16d…, IG 6ad8a16b…), sem leitura (< 24 h); piso atual comentário de terceiro ≈2 em 78 | mantém
2026-10-22 | hipótese: trocar "erro fatal"/pergunta aberta por pergunta genuína que o vídeo responde e fecho de múltipla escolha, link no 1º comentário (FB 6ada299df5b065b06b2263b0, 6ad232c93a272e4280ce9481, 6ada29d0ce999cf09365ef20) | resultado: n=0 (alvo FB views >= 280, base mediana 227; 1 comentário de terceiro) | mantém
2026-10-22 16:30 | Portão de gancho + estoque 36 h: agendar só pacote com artigo 200 | n=3 pacotes aprovados (cronograma, sinais-envelhecimento, guia-peitoral) com artigo 404; cinto (FB/IG 23/10 10:00/11:00, TikTok 23/10 14:20) com gancho banido 'Para de usar…' | altera: Agendador deve rodar o portão também sobre o que o Claude da sessão já agendou
2026-10-23 | hipótese: ler horários reais no Zernio antes de usar o turno sugerido pelo agent.py evita colisão | agenda.json estava defasada (turno C de 23/10 já ocupado); ajustei na mão 5 slots | mantém; conferir Zernio primeiro
2026-10-23 | passo 13 (sem engagement bait; pergunta genuína de 1 palavra) + J1 número cedo (C5, C6) | n=0 (lote r23 sem leitura 72 h); base FB comentário de terceiro ≈2 em 78 | mantém
2026-10-23 | regra de decisão da skill (Diretor): sem isca ao ar, nenhuma mudança de plataforma; medir FB/IG por follower-stats | n=0 (FB 8, IG 0, janela 72 h não iniciada) | mantém
2026-10-24 | estoque FB/IG ate 26/10 A; rampa e caldo (re-gancho aprovados) agendados 26/10 B/C | n=2 pacotes, sem leitura ainda | mantem
2026-10-24 | regra de decisão da skill: pergunta binária de rotina, sem comando de curtir/comentar (limite Meta isca de engajamento) | n=0 posts do lote publicados | mantém
2026-10-24 | decisão de plataforma: sem isca ao ar não se muda canal/formato; manter FB+IG piloto do mimo | n=0 (FB 8, IG 0; follower-stats quebrado) | mantém
2026-10-25 | Meta: sem isca de engajamento (CTA em forma de pergunta 1/2), vídeo só, 3 temas novos para não reciclar | n=0 posts do lote lidos | mantém
2026-10-25 | decisão do Diretor: canal do piloto segue FB+IG; PDF pronto, falta ok do Allan e Chrome; cartão de imagem ainda agendado (contra E97) vai ao Allan | n=0 janela de 72 h (FB 8, IG 0) | mantém
2026-10-25 | portão de gancho (frame 0 ≤6 palavras) barra 100% dos pacotes recentes, inclusive os já agendados | n=10 pacotes testados, 10 barrados | ALTERA: Roteirista/portão precisam alinhar; agendador não agendou novos
2026-10-26 | portão de gancho + estoque 3 dias | 2 pacotes agendados (28/10 C, 29/10 A), 2 barrados por gancho (n=4) | mantém
2026-10-26 | passo 8 (meme só no horário provado) e passo 5 (gancho em 3 peças) | FB meme r23 n=2 abaixo de 1,5x; FB mediana 208 views (n=12), IG alcance 37 | mantém, meme só em FB 08:30/21:00 e IG 08:40/21:10
2026-10-26 | passo de medição + payoff até o s4 (E114): isca ao vivo depende do Allan | FB 9 seguidores (+2/7d), IG 0 | mantém
2026-10-26 | portão de gancho barrou 2 pacotes aprovados (filhote-gato-x-cães, fonte-água-gatos) e artigo exercícios-mentais-gatos-idosos está 404 | n=3 pacotes, 0 agendáveis; turno A de 26/10 falhou nas 3 redes (video.mp4 de sinais-de-envelhecimento-em-gatos-senior ausente na branch media) | altera: fábrica deve reescrever gancho dos 2 pacotes e conferir 200 do vídeo antes de agendar
2026-10-27 | regras Meta (isca de engajamento, originalidade): 0 'curta/comente/compartilhe' como comando, CTA binário 1/2; só nosso material | 3 ideias, n=0 leituras | mantém
2026-10-27 | passo de medição diária (from_date/to_date) + manter isca sem dado ao vivo | FB 9 (+2/7d), IG 0; n=0 leituras de isca | mantém
2026-10-27 | hipótese: gate do frame 0 (≤6 palavras) trava todo pacote novo e o estoque cai a ~2 dias | 2 de 2 pacotes 'ok' barrados (14 e 12 palavras); 0 pacotes novos agendáveis na rodada 12:15, fábrica redisparada | altera: Criador de Audiência deve gerar texto_na_tela curto já na origem
2026-10-27 | portão frame 0 (<=6 palavras) barra pacotes com gancho longo; hipótese: fábrica ainda gera frame 0 longo | 5 de 6 pacotes ok recentes barrados (n=6) | mantém; fábrica precisa encurtar texto_na_tela
2026-10-28 | skill lida por título; hipótese: vídeo ≤15 s e T0 curto seguram retenção (IG ≤15 s alcance 102 x 39, n14/n36) | lote r28 todo em 6-10 s; n=0 posts do lote lidos | mantém
2026-10-28 | remix: botão da Meta só no app do celular; é o único jeito legítimo de pegar carona em viral de terceiro (repostar, mesmo editado, é proibido; criador com remix desligado = descartar); Zernio e Buffer não fazem remix, quem toca no botão é o Allan ou a Natasha | n=0 remixes publicados | mantém
2026-10-28 | agenda lida: Zernio 4 pares FB+IG até 30/10 e Buffer 5 TikToks até 30/10 10:20 (41 a 57 s); plano grátis do Buffer = teto de 10 agendados, então 3/dia por 5 dias (15) não cabe | n=1 conta | altera: TikTok até 10 agendados (2/dia nos horários 10:20 e 20:20); reposição só com pacote de Guardião "ok"
2026-10-29 | estoque <3 posts/24h e 2 pacotes novos bloqueados (revisar + artigo 404) -> evergreen com legenda nova | n=2 videos reusados, resultado a medir em 72h | mantem
2026-10-30 | slots livres vs saturados (FB/IG 4 posts hoje, TikTok 4) | carrinho-de-passeio levado para 31/10 B/C | n=3 posts | mantem
2026-10-30 | jogadas 'sem engagement bait' e 'pergunta genuína + link no 1º comentário': 14 CTAs sem comando, link só no 1º comentário, meme no IG nos picos 11:00/20:00 | n=0 posts do lote lidos (comparar com os 10 anteriores em 03/11) | mantém
2026-10-30 | CTA sem comando de engajamento e pergunta genuína nas 3 ideias novas | n=0 posts medidos | mantém
2026-10-30 | hipótese: reserva evergreen (gancho pergunta concreta, legenda nova) cobre dias sem pacote novo com gancho liberado | n=3 vídeos reagendados (arranhar-sofa, patas-inverno, plantas), resultado em 72 h | mantém
2026-10-31 | sem comando de curtir/comentar/compartilhar na legenda; pergunta binária divide, CTA a/b | n=0 posts medidos (3 ideias propostas); FB mediana 189 views, comentário de terceiro ~0 | mantém
2026-10-31 | regra: início de conta pequena depende de constância; 1º seguidor IG após 86 posts | IG 0→1, FB 9→10 (n=1) | mantém

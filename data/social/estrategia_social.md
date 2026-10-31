Dados até 2026-10-31 07:07 (Fortaleza) — Zernio (FB, IG; sync 31/10 06:26) e Buffer (TikTok; métricas até 30/10 18:15, defasagem até 24 h). 20ª edição (anterior 30/10 07:10). Conta nova, n pequeno: afirmo número, não causa; ajo com hipótese. Git de rede travou de novo (pull >2 min): usei o clone local.
## 0. ERROS E ESTADO (topo)
- ERRO Zernio: os mesmos 8 posts falhos (nada novo; não retentei): Sozinho em Casa 26/10 (FB 6adc3564e6b92ce2d51b7c71, 6adc3569e6b92ce2d51b7c7d; IG 6adc35677beb87d559d17906, 6adc356c7beb87d559d17925; "rupload 422"/"couldn't fetch media"), gatinho-senior (FB 6adb7b5c73f85b064967b8a1, IG 6adb7b5f8d696b7f05e0841d), humor "Quem mais?" (FB 6ad232d7c8e9ce3699c93928, IG 6ad232da9ee766016c2d05da). Limpeza = E153 (sem retry em lote).
- Buffer: 0 em erro nas 50 mais recentes.
- AGENDADO Zernio (6 posts, FB+IG): piscina (FB 6ae39d578962cd50f89dc343, IG 6ae39d5a8962cd50f89dc379), cachorro idoso (FB 6ae47e175ee788b7fc74209a, IG 6ae47e195ee788b7fc7420ab), sofá, patas no chão frio, planta/gato (3 pares novos). Buffer TikTok: 8 agendados até 02/11 10:20. Estoque ≈1,5 dia (E153).
## 1. Nossos números (24/10 a 31/10; posts com 24h+)
| Rede | n | Resultado | Retenção |
|---|---|---|---|
| FB | 17 | views mediana 189; 0 shares; 30 curtidas; 7 cliques | tempo médio mediano 3,9 s (<6 s) |
| IG | 17 | views mediana 29; 1 share, 1 salvo | skip mediano 72,7% (>70%) |
| TikTok | 20 (24-31/10) | 4.418 views, 250 reações, 5 shares, 4 comentários | tempo médio 2,88 s (<4 s) |
- Comentários de terceiros: ~0 em FB/IG (o "1" por post é o nosso 1º comentário com o link). TikTok: 4 comentários em 20 posts.
- SINAL FORTE (R1, react curto 18-23 s com Duda; n=3, um parcial de 10 h): FB 678 views/7,9 s (08:30 de 30/10), 555/8,1 s (21:00 de 29/10), 274/6,0 s (21:01 de 30/10, 10 h); IG skip 30% e 21% (21:10), mas 08:40 de 30/10 teve 1 view (falha de distribuição, não conta); TikTok "Time beija" 472 views/7,06 s/26 reações/1 share, "Ela não deixa" 171/4,56 s. Explicadores de 42-56 s: FB 3,5-4,7 s, IG skip 63-90%, TikTok 1,2-3,4 s.
- Parciais <24h (não decidem): FB 30/10 14:03 217, 19:03 230, 10:04 300; IG 30/10 11:02 119 (skip 67%), 15:02 98 (65%), 20:04 106 (67%); TikTok 30/10 17:20 45 views, 23:20 sem leitura.
- Ligação com tema/gancho/CTA: tags do Buffer seguem vazias (E141/E150 sem efeito); só dá para ligar por formato e duração. Seguidores: sem leitura nova (28/10: FB 9, IG 0, TikTok 21).
## 2. Gatilho (regra_mudanca_rapida.md): DISPAROU (explicadores)
FB 3,9 s; IG skip 72,7%; TikTok 2,88 s. Mas R1 passou no critério do plano de 30/10 (FB ≥6 s e IG skip ≤55% em 2 de 2 válidos + TikTok ≥4 s em 2 de 2): ESCALAR. Plano: data/social/plano_de_mudanca_2026-10-31.md (E160-E162).
## 3. Horários (Fortaleza) — grade mantida
| Rede | Melhor 1 | Melhor 2 | Observação |
|---|---|---|---|
| FB | 10:00 | 19:00 | react 08:30 (678, n1) e 21:00 (555, n1) são os melhores números da conta; 12:00 suspenso |
| IG | 11:00 | 20:00 | react só 21:10 (skip 21-30%, n2); 08:40 fora (1 view) |
| TikTok | 10:20 | 20:20 | mediana de views por slot 10:20 182 (n10), 14:20 200 (n12), 20:20 181 (n13): sem diferença; 17:10 só 117 (n3) |
- Zernio best_time (UTC): n 1-5 por slot, topo é ruído (qua 19 UTC, n1). Vale mudar? Não: o fator é retenção, não horário. Fontes públicas (Metricool, 29/06/2026): FB 10-14h, IG/TikTok 18-21h, coerente com a grade. Releitura 03/11.
## 4. Hashtags e legenda
- Quantidade (Metricool, metricool.com/how-many-hashtags-to-use): IG 3-5, TikTok 3-5, FB 0-3. Conjuntos por tema em config/estrategia_social.yaml. Nunca #fyp/#viral. Sem fonte aberta nova para pet BR hoje.
- Legenda: gancho em pergunta binária (react) + 1 linha de valor + pergunta + CTA fixo "Confira o artigo completo em tutorialpet.com.br". Link só no 1º comentário. Sem preço por dia/mês; saúde = consulte o veterinário. 3 modelos por rede no yaml.
## 5. Interação e isca — ESTADO (checado hoje)
- Landing sozinho.tutorialpet.com.br (com UTM): HTTP 200; /7-erros.pdf: HTTP 200 (curl 31/10). Landing mostra R$ 27 e âncora R$ 97, sem R$ 9,90.
- ManyChat GUIA: suspenso por decisão do Allan (21/10, E19), não quebrado; MIMO escrito e não ligado (06 Pendências nº 2). Texto ao vivo da DM e Brevo transacional: sem dado (sem PC/Chrome nesta rodada).
- Pendência real: "9,90" ainda em config/catalogo_tema_produto.yaml, config/prompts/{produtor_ebook,construtor_app}.md, config/vsl/*.md (grep 31/10; E22/E127) e nas legendas dos 4 posts falhos.
- Perguntas de hoje (5 por tema): config/estrategia_social.yaml, perguntas_lote_2026_10_31.
## 6. Painel mínimo (meta até 11/11; hipótese, sem promessa)
FB: views mediana 230, tempo ≥4,5 s, 10 cliques/semana. IG: alcance mediana 80, skip ≤60%, shares+salvos ≥2/semana. TikTok: views 300, tempo ≥3 s, 1 share a cada 4 posts. Seguidores: FB +1/dia, TikTok +1/dia. Trocar horário/gancho/CTA: gatilho em 2+ posts de 3 dias, leitura em 24 h, um fator por vez.
## 7. Decisões do Allan (reais)
1) Reacts usam vídeo de terceiros (ex.: "Vídeo original de @metropoles"): são os melhores posts, mas a regra (e) pede conteúdo original; recomendo pedir permissão/usar só vídeos próprios ou de banco livre com a Duda antes de escalar. 2) Trocar os explicadores longos já agendados (FB/IG piscina, cachorro idoso, sofá, patas, planta; TikToks 41-57 s): mexe em item agendado; recomendo trocar ao menos 3. 3) MIMO ao vivo no ManyChat (precisa do PC/Chrome): responder "pode ligar o fluxo MIMO".
## 8. Sem dado
Gancho/voz/CTA por post (tags vazias), seguidores ao vivo, ManyChat/Brevo/Kiwify ao vivo, comentários de terceiros reais, melhor horário por dia da semana (n pequeno).

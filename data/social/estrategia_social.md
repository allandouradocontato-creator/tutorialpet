Dados até 2026-10-30 07:10 (Fortaleza) — Zernio (FB, IG; sync 30/10 06:17) e Buffer (TikTok; métricas até 29/10 22:14, defasagem até 24 h). 19ª edição (anterior 29/10 07:15). Conta nova, n pequeno: afirmo número, não causa; ajo com hipótese. Git de rede travou (pull >2 min): usei o clone local (HEAD bf81006).
## 0. ERROS E ESTADO (topo)
- ERRO Zernio: os mesmos 8 posts falhos (nada novo; não retentei): Sozinho em Casa 26/10 (FB 6adc3564e6b92ce2d51b7c71, 6adc3569e6b92ce2d51b7c7d; IG 6adc35677beb87d559d17906, 6adc356c7beb87d559d17925; "rupload 422"/"couldn't fetch media"), gatinho-senior (FB 6adb7b5c73f85b064967b8a1, IG 6adb7b5f8d696b7f05e0841d), cartão "Quem mais?" (FB 6ad232d7c8e9ce3699c93928, IG 6ad232da9ee766016c2d05da). Os 4 do Sozinho em Casa levam preço antigo na legenda.
- Buffer: 0 em erro.
- AGENDADO Zernio (4 pares FB+IG): gato idoso (IG 30/10 11:00; FB 6ae20200fe495d4885068047), gato água (IG 30/10 20:00), gato visitas (FB 30/10 14:00), piscina (FB 31/10 10:00). AGENDADO Buffer: TikTok 30/10 10:20 gatinho-senior 57 s (6ae22014ad320a6d07f57695), 11:20 react 20 s, 14:20 gato visitas 46 s, 20:20 gato água 52 s; 31/10 10:20 piscina 56 s, 14:20 caixa 41 s; FB 30/10 08:30 e IG 08:40 react; FB 21:00 e IG 21:10 react atleta (18,5 s, 31/10 00:00/00:10Z). Fila TikTok: 5 de 7 têm 41-57 s.
## 1. Nossos números (20/09 a 30/10; só posts com 24h+)
| Rede | n (7 d) | Resultado | Retenção |
|---|---|---|---|
| FB | 17 | views mediana 204; 0 shares | tempo médio mediano 3,8 s (<6 s) |
| IG | 16 | alcance mediana 32,5; 2 shares/saves | skip mediano 76%; >70% em 9/16 |
| TikTok | 12 (22 desde 21/10) | views mediana 152 (177); 2 shares desde 21/10 | tempo 2,25 s (2,38 s); <4 s em 21/22 |
- Buffer TikTok 01-30/10: 57 posts, 12.231 views, 691 reações, 19 shares, tempo médio 2,62 s.
- SINAL NOVO (parcial 10-17 h, n=1 por rede): react 23 s com Duda, 29/10 21:00-21:10. FB 279 views, 9 curtidas, tempo 8,2 s (mediana 3,8). IG skip 25%, tempo 8,5 s (mediana 76%). TikTok do mesmo react (20:21) ainda 0 views por defasagem. TikTok melhor: 29/10 14:21 gato idoso 44 s, 422 views, 48 reações, 3 shares, tempo 2,7 s (parcial 17 h).
- Parciais <24h (não decidem): FB 29/10 10:04 41 views, 14:03 225, 19:04 158; IG 29/10 11:02 alcance 1 (skip 100%), 15:01 13, 20:04 17.
- Seguidores: sem leitura nova (28/10: FB 9, IG 0, TikTok 21). Sem dado: gancho/voz/CTA por post (tags dos posts Buffer vazias: E141 sem efeito), comentários de terceiros.
## 2. Gatilho (regra_mudanca_rapida.md): DISPAROU
FB 3,8 s; IG skip 76%; TikTok 2,25 s e 1 share em 12. Plano: data/social/plano_de_mudanca_2026-10-30.md (E149-E151; E134-E138, E141-E142 seguem).
## 3. Horários (Fortaleza) — grade mantida
| Rede | Melhor 1 | Melhor 2 | Extras |
|---|---|---|---|
| FB | 10:00 | 19:00 | 21:00 react/meme (279 views, 8,2 s, n1); 08:30 caiu (121, n8) e está na fila de 30/10; 12:00 suspenso |
| IG | 11:00 | 20:00 | 21:10 react (skip 25%, n1); 08:40 (70, n5) |
| TikTok | 10:20 | 20:20 | 14:20 (195); 11:20 novo, sem prova |
- Zernio best_time (UTC): slots com n 1-4, topo é ruído (qua 19 UTC, n1). Vale mudar? Não: o fator é retenção. Releitura 03/11.
## 4. Hashtags e legenda
- IG 3-5, TikTok 3-5, FB 0-3 (fontes em config/estrategia_social.yaml; sem fonte aberta nova hoje). Nunca #fyp/#viral. Reacts hoje levam #react: manter só se o tema for humor.
- CTA fixo: "Confira o artigo completo em tutorialpet.com.br"; link só no 1º comentário; sem "cão", sem preço por dia/mês; saúde = consulte o veterinário. 3 modelos por rede no yaml.
## 5. Interação e isca — ESTADO (checado hoje)
- sozinho.tutorialpet.com.br (com UTM) e /7-erros.pdf: HTTP 200 (curl 30/10); landing: R$ 27 (7x) e âncora R$ 97, sem R$ 9,90.
- ManyChat GUIA suspenso por decisão do Allan (21/10); MIMO escrito e não ligado (06 Pendências). Texto da DM ao vivo e Brevo transacional: sem dado (sem PC nesta rodada).
- Pendência real: R$ 9,90 ainda em config/catalogo_tema_produto.yaml, config/prompts/{produtor_ebook,construtor_app}.md, config/vsl/*.md (grep 30/10; E22/E127) e nas legendas dos 4 posts falhos.
- Perguntas de hoje (5 por tema): config/estrategia_social.yaml, perguntas_lote_2026_10_30.
## 6. Painel mínimo (meta até 11/11; hipótese, sem promessa)
FB: views mediana 230, tempo ≥4,5 s, 10 cliques/semana. IG: alcance mediana 80, skip ≤60%, shares+salvos ≥2/semana. TikTok: views 300, tempo ≥3 s, 1 share a cada 4 posts. Seguidores: FB +1/dia, TikTok +1/dia. Trocar horário/gancho/CTA: gatilho em 2+ posts de 3 dias, leitura em 24 h, nunca com <5 posts por variação.
## 7. Decisões do Allan (reais)
1) Trocar os TikToks longos agendados (57 s 30/10 10:20; 52 s 30/10 20:20; 56 s 31/10 10:20; 46 s e 41 s) por reacts/cortes de 18-25 s: mexe em item agendado; recomendo trocar ao menos os 57 s e 52 s. 2) Descartar os 8 posts falhos (4 com preço antigo): recomendo sim. 3) Reacts usam vídeo de terceiros ("Vídeo original de @metropoles", via @...): choca com a regra (e) conteúdo original e traz risco de direitos autorais/remoção; recomendo só usar com permissão escrita ou vídeo licenciado.
## 8. Sem dado
Gancho/voz por post, seguidores ao vivo, ManyChat/Brevo/Kiwify ao vivo, vendas, comentários de terceiros, melhor horário por dia da semana.

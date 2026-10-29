Dados até 2026-10-29 07:15 (Fortaleza) — Zernio (FB, IG; sync 29/10 06:16) e Buffer (TikTok; métricas com defasagem de até 24 h). 18ª edição (anterior 28/10 07:10). Conta nova, n pequeno: afirmo número, não causa; ajo com hipótese. Git de rede travou nesta rodada: usei o clone local (main em cdae704).
## 0. ERROS E ESTADO (topo)
- ERRO Zernio: os mesmos 8 posts falhos de 27-28/10 (nada novo; não retentei): Sozinho em Casa 26/10 14:00 e 19:00 (FB "rupload 422", IG "couldn't fetch media URL") FB 6adc3564e6b92ce2d51b7c71, 6adc3569e6b92ce2d51b7c7d, IG 6adc35677beb87d559d17906, 6adc356c7beb87d559d17925; gatinho-senior FB 6adb7b5c73f85b064967b8a1, IG 6adb7b5f8d696b7f05e0841d; cartão "Quem mais?" FB 6ad232d7c8e9ce3699c93928, IG 6ad232da9ee766016c2d05da. Os do Sozinho em Casa ainda levam preço antigo na legenda.
- Buffer TikTok: 0 em erro agora (caixa-de-transporte e gatinho-senior de 25-26/10 não aparecem mais com erro).
- AGENDADO Zernio: 3 pares FB+IG (gato idoso x2: 6ae20200fe495d4885068047/6ae20205fe495d4885068070 e 6ae08957fe8f5a0c4b3cc45b/6ae08959ae7636fe08726adc; petiscos 6adf37922524d4a3d16cd86a/6adf379549c8a198167fad65). AGENDADO Buffer: 4 TikToks, TODOS longos: 29/10 10:20 (42 s, 6adf37994dcf9e76ce4dcbdd), 14:20 (44 s, 6ae0895ba21f4739ba9a7334), 20:20 (41 s, 6ae22011f835de4f325875be), 30/10 10:20 (57 s gatinho-senior, 6ae22014ad320a6d07f57695, mesmo tema que falhou em 26/10). Nenhum corte 15-25 s entrou na fila (E137 sem efeito até agora).
- Fila: Zernio acaba em ~30/10; Buffer em 30/10 10:20. Reposição depende da Fábrica (vermelha, ElevenLabs 306) e do reuso evergreen (V21).
## 1. Nossos números (20/09 a 29/10; só posts com 24h+)
| Rede | n | Resultado | Retenção / sinais |
|---|---|---|---|
| FB | 98 | views mediana 206 (últimos 7 d: 173, n20); 179 curtidas, 57 comentários (≈1/post = nosso link), 0 shares, 0 salvos, 179 cliques | tempo médio 3,3 s (7 d: 3,5 s) |
| IG | 74 | alcance mediana 34,5 (7 d: 30); 41 curtidas, 50 comentários (nossos), 6 shares, 4 salvos, 0 cliques | skip mediana 67%; >70% em 31/74; tempo 3,7 s |
| TikTok | 53 | views mediana 181 (7 d: 158, n17); 11.091 views; 599 reações, 6 comentários, 16 shares (1 nos últimos 7 d) | tempo médio 2,2 s (7 d: 2,35 s); <4 s em 45/53 |
- Seguidores: sem leitura nova (28/10: FB 9, IG 0, TikTok 21; Buffer não informa).
- Parciais <24h (não decidem): FB 28/10 10:04 27 views, 14:03 174, 19:03 115; IG 28/10 11:01 alcance 9 (skip 78%), 15:02 4, 20:02 113 (skip 90%); TikTok 28/10 10:23 85 (3,2 s), 14:21 74 (2,1 s), 20:21 0 (cedo).
- Formato IG (alcance mediana/skip): ≤15 s n15 = 102/58% x 30-45 s n24 = 35/70% x 45 s+ n26 = 31/75%. TikTok: 30-45 s n21 = 2,4 s; 45 s+ n29 = 2,2 s; ≤16 s n3 = 1,6 s (n3, não conclui; o corte curto não salvou a retenção).
- Tema: FB gato x cachorro empate (≈210); IG gato maior mas confundido com formato; TikTok melhor retenção histórica "cachorro sozinho" (7,3 s).
- Sem dado: gancho/voz/CTA por post (manifest só em poucos pacotes; clone da branch media estoura o tempo), % assistido FB, comentários de terceiros exatos.
## 2. Gatilho (regra_mudanca_rapida.md): DISPAROU
FB 3,3 s (<6 s); TikTok 2,2 s e 1 share em 17 posts nos 7 d (<1 a cada 4); IG skip >70% em 31/74. Plano: data/social/plano_de_mudanca_2026-10-29.md (E141-E142; E134-E138 seguem valendo).
## 3. Horários (Fortaleza) — grade igual todos os dias (n<5 por dia da semana)
| Rede | Melhor 1 | Melhor 2 | Extras |
|---|---|---|---|
| FB | 10:00 (208, n18) | 19:00 (179, n22) | 21:00 meme (260, n6); 14:00 (224, n12); 08:30 caiu (121, n8); 12:00 (61, n13) segue suspenso |
| IG | 11:00 (36, n12) | 20:00 (41, n16) | 21:10 meme (95, n7), 13:00 (72, n8), 08:40 (70, n5); 15:00 (30, n13) vira meme ≤15 s |
| TikTok | 10:20 (187) | 20:20 (180) | 14:20 (195); diferença de horário é ruído |
- Zernio best_time (UTC): n 1-5 por slot, topo ruído (qua 19 UTC n1); engajamento inflado pelo nosso 1º comentário. Vale mudar? Não: o fator é retenção. FB sem leitura por dia da semana confiável (terça 25 de mediana, n20, misturada ao slot 12:00). Releitura 03/11.
## 4. Hashtags e legenda
- Quantidade: IG 3-5 (limite 5: [Envox, 20/01/2026](https://envox.com.br/marketing-de-conteudo/hashtags-em-2026-guia-quantidade-escolha-erros/agencia-de-marketing-digital/trafego-pago/vendas/) e [Agência Gram, 2026](https://agenciagram.com.br/blog/hashtags-instagram-ainda-funcionam-2026)); TikTok 3-5 e FB 0-3 sem fonte aberta nova. Nunca #fyp/#viral. Sem prova aberta do que funciona em página pet BR: conjuntos por tema e 3 modelos por rede em config/estrategia_social.yaml.
- CTA fixo: "Confira o artigo completo em tutorialpet.com.br"; link só no 1º comentário; nunca "cão" (cachorro/pet); nunca preço por dia/mês.
## 5. Interação e isca — ESTADO (checado hoje)
- sozinho.tutorialpet.com.br e /7-erros.pdf: HTTP 200 (curl 29/10); landing mostra R$ 27 (7x) e âncora R$ 97, sem R$ 9,90.
- ManyChat GUIA suspenso por decisão do Allan (21/10); MIMO escrito e não ligado (consta no bloco "Para o Allan (receita)" de 06 Pendências, não repito). Texto da DM ao vivo e Brevo transacional: sem dado (sem PC; último dado 23/10: 0 contatos, sem e-mail transacional).
- Pendência real: R$ 9,90 / "de R$ 37" ainda em config/catalogo_tema_produto.yaml e config/prompts/{produtor_ebook,construtor_app}.md (grep 29/10; E22/E127) e nas legendas dos 4 posts falhos do Sozinho em Casa.
- Perguntas de hoje (5 por tema): config/estrategia_social.yaml, perguntas_lote_2026_10_29.
## 6. Painel mínimo (meta até 11/11; hipótese, sem promessa)
FB: views mediana 230, tempo ≥4,5 s, ret. s5 ≥55%, 10 cliques/semana. IG: alcance mediana 80, skip ≤60%, shares+salvos ≥2/semana. TikTok: views 300, tempo ≥3 s, 1 share a cada 4 posts. Seguidores: FB +1/dia, TikTok +1/dia. Trocar horário/gancho/CTA: gatilho acima em 2+ posts de 3 dias, leitura em 24 h, nunca com <5 posts por variação.
## 7. Decisões do Allan (reais)
1) Trocar os 4 TikToks longos agendados (41-57 s) por cortes 15-25 s mexe em item agendado: recomendo sim. 2) Descartar os 8 posts falhos (4 do Sozinho em Casa com preço antigo): recomendo sim, repor com novos. (MIMO/OAuth, A02 e religar D02/E09 já estão em 06 Pendências.)
## 8. Sem dado
Gancho/voz por post, seguidores ao vivo, ManyChat/Brevo/Kiwify ao vivo, vendas, comentários de terceiros, melhor horário por dia da semana (n pequeno).

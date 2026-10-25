Dados até 2026-10-25 07:08 (Fortaleza). Só recomendação; nada publicado, agendado ou apagado por mim. Complementa plano_de_mudanca_2026-10-24.md e data/testes/plano_2026-10-24.md (E93-E99, E105-E109 seguem valendo; provas em 26-27/10).
## Gatilho (regra_mudanca_rapida.md): disparou
FB tempo <6 s em 40/44 (mediana 3,8 s); TikTok <4 s em 32/35 (2,3 s), mediana 189 views; IG skip >70% em 18/43, alcance 55.
## Achado que muda a leitura
O mesmo tema repostado cai a cada vez: TikTok banho 1.017 -> 201 -> 113; gato/água 577 -> 160; filhote chora 285 -> 171 -> 84; FB repetiu "filhote chora" e "banho" em 22/10 (19:03 e 20:32) com 4 views contra 235 e 231 nas versões de 14 e 17/10. Hipótese (n=4 temas): a reserva evergreen está gastando slots com vídeo já visto.
## 1. PARAR
- Reposição de slug/tema com menos de 14 dias de intervalo (reserva evergreen e gerador de fila).
## 2. TESTAR (leitura em 24 h; só itens NÃO agendados)
- T1 (E111) tema novo x reciclado: próximos 6 slots de FB/IG e 4 de TikTok só com tema inédito nos últimos 14 dias. Aprova: FB mediana >=200 views; TikTok >=150 views e tempo >=2,5 s; leitura 27/10.
- T2 (já em curso, E98) TikTok cortes de 15-25 s com resultado no segundo 0 a partir de 27/10 20:20.
- T3 (já em curso, E108) CTA binário "1 ou 2?" no 1º comentário e na legenda; prova 27/10: >=1 comentário de terceiro a cada 5 posts.
## 3. APLICAR
E111 em data/decisoes/execucao.md; regra em config/estrategia_social.yaml (rodada_2026_10_25_0708.regra_E111) e no gerador/Agendador (evergreen.yaml: excluir slug publicado em <14 dias).
## 4. Posts JÁ agendados para o Claude da sessão do Allan (eu não mexo)
- FB 6ad232d7c8e9ce3699c93928 (25/10 12:01) e IG 6ad232da9ee766016c2d05da: texto "Quem mais? Conta aqui." igual aos cartões de imagem com 0 view; conferir se a mídia é vídeo 8 s.
- TikTok: os 8 agendados em 25/10 10:20 até 27/10 14:20 têm 41-57 s (histórico 2 s de tempo médio nessa duração); só trocar se houver corte pronto, senão deixar. Há 2 vagas livres (teto 10).
## 5. Números de partida (leituras 26/10 e 27/10)
FB vídeo mediana 221, tempo 3,8 s; IG alcance 55, skip 67,6%; TikTok 189 views, 2,3 s; seguidores FB 8, IG 0, TikTok 19.

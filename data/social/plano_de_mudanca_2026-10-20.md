Dados até 2026-10-20 10:15 (Fortaleza). Só recomendação; nada publicado, agendado ou apagado por mim. Complementa data/social/plano_de_mudanca_16_10.md (T1 meme, T2 voz do pet, T3 corte com resultado no segundo 0).
## Gatilho (regra_mudanca_rapida.md): disparou nas 3 redes
- FB: tempo médio <6 s em 15 de 18 posts (17-20/10). IG: skip >70% em 8 de 9 explicadores. TikTok: tempo médio <4 s em 5 de 6, 0 shares em 6.
## O que o dado novo diz (n pequeno; hipótese, não causa)
- IG meme 8s: alcance mediana 86, skip 55%, tempo 4,3 s (n=8) contra explicador 34-55s: 31, 76%, 4,0 s (n=9).
- FB 8s em 08:30 e 21:00: 383 e 254 de mediana (n=3 cada) contra 206-216 nos explicadores. Melhor post: 559 views.
- Slot de meme 12:00 FB / 13:00 IG: 7, 0, 0 views no FB (3 posts) e 131, 0, 0 no IG. Entrega falhou; causa desconhecida.
- TikTok não recebeu meme 8s nas últimas 48h; sem como comparar.
## 1. PARAR
- Explicadores 36-55s na fila nova: no máximo 1 a cada 3 posts (já em 16/10; fila do dia ainda os traz).
- Slot de meme FB 12:00 / IG 13:00 até alguém conferir os 3 vídeos de 0-7 views.
- Frase "link no perfil" em qualquer legenda nova.
## 2. TESTAR (24-48 h, leitura por retenção; no máximo 3)
- A) Meme 8s em 3 horários por rede (FB 08:30, 12:00 novo vídeo, 21:00; IG 08:40, 13:00, 21:10), 2 posts por horário. Hipótese: o 12:00 falha pelo arquivo, não pelo horário. Aprova: slot com mediana ≥200 views FB / ≥60 alcance IG.
- B) Meme 8s no TikTok 10:20 e 20:20 por 3 dias (6 posts). Hipótese: o formato curto sobe o tempo médio >50% da duração (hoje 1,4-4,3 s em 40s). Aprova: tempo médio ≥4 s e ≥1 share em 3 de 6. Referência: @gatalunacatarina e @bucky_ogato [petz.com.br/blog/gato-do-tiktok].
- C) Pergunta de uma palavra na legenda ("Gato ou cachorro?") e no 1º comentário nos memes. Hipótese: 0 comentário de terceiro em 41 posts vem da pergunta aberta. Aprova: 1 comentário de terceiro em 2 de 6.
## 3. APLICAR (arquivos)
- config/estrategia_social.yaml: bloco regras_teste.mudanca_2026_10_20 + horários dos memes.
- Fila de produção da fábrica: 2 em cada 3 vídeos novos = meme 8-12s; explicador só 1 em 3.
- Prompt do Publicador (config/prompts/publicador.md, agents/21_publicador_video): remover "link no perfil" das legendas TikTok (ocorre nesses arquivos).
## 4. Posts JÁ agendados para o Claude da sessão do Allan (eu não mexo)
- TikTok 6ad51bdb0a208cb3237b4a7b (20/10 20:20, bolas de pelo 50s, "link no perfil") e 6ad359920b0d72757ad41c47 (21/10 10:20, comida cão+gato 42s): trocar por meme 8s ou corte T3; legenda sem "link no perfil".
- FB/IG explicadores longos: bolas de pelo FB 6ad391f006490c62e78601d2 / IG 6ad391f3788d7dacfb3d9e88; ração cão x gato FB 6ad391eb3a0a76f1f0df82fc / IG 6ad391ee7079173525ed16ae; cachorro sozinho IG 6ad02bb8e59ac4780c8e4a12. Horários dos agendados FB/IG não vêm no posts_list.
- Apagar/mexer em publicados (3 vídeos de 12:00) = decisão do Allan.

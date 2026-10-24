Dados até 2026-10-24 07:20 (Fortaleza) — Zernio (FB, IG; sync 24/10 05:16 Fortaleza, 1 conta sinalizada "stale") e Buffer (TikTok; métricas atualizadas 24/10 01:08, defasagem até 24 h). 13ª edição (anterior 23/10 07:19). Janela 20/09 a agora; as redes só têm posts desde 14/10 (conta nova, n pequeno).
Passos sem dado: WebFetch da landing negado (permissão sem resposta); Chrome/ManyChat/Brevo/Kiwify = "sem dado (PC ausente)" (rotina de nuvem, sem ponte); manifest da media não traz gancho/voz/CTA por post (tema vem do texto).
## 0. Erros e estado (topo)
- Erros de publicação: nenhum (Zernio posts_list failed vazio; Buffer sem post em error).
- Agendados: Zernio 22 (11 pares FB+IG) e Buffer TikTok 9 (24/10 10:20, 14:20, 20:20; 25/10 e 26/10 nos mesmos 3 horários; teto grátis 10). Fila TikTok acaba 26/10 20:20.
- ACHADO 1 (novo): os 10 posts de IMAGEM (cartão/"Quem mais?"/"Erro 1-2 de 7"; 5 FB + 5 IG) deram 0 view cada (100%). Os de vídeo: FB mediana 221 (n=44), IG 55 (n=43). O "FB 12:00 sem views" era imagem, não horário. Regra (c) só vídeo = regra de entrega.
- ACHADO 2: a reposição TikTok de 23-24/10 usou vídeos inteiros de 41-57 s (6 dos 9), não os cortes de 15-25 s de E50/E95. Não mexo em agendados; ids no plano.
- RISCO agendado (para o Claude da sessão): FB 6ad232d0e0a9f13c292dc269 (24/10 12:01) tem a URL na legenda (fere b); FB 6ad232d7c8e9ce3699c93928 (25/10 12:01) e IG 6ad232da9ee766016c2d05da repetem a legenda "Quem mais? Conta aqui." que em 19/10 foi imagem com 0 view: conferir se é vídeo.
- Já publicado e fora da regra (d): FB 23/10 10:04 "erro fatal no cinto" (309 views, 0 curtida) e IG (4 views). Mexer em post publicado = decisão do Allan; só registro.
## 1. Nossos números (posts de vídeo com 24h+; 20-22/10 = 3 dias)
| Rede | n | Resultado | Retenção |
|---|---|---|---|
| FB | 15 | views mediana 217; 28 curtidas; 10 comentários (nosso link); 0 shares/salvos; 1 clique | tempo médio mediana 3,8 s; <6 s em 13 de 15 |
| IG | 14 | alcance mediana 61,5; 10 curtidas; 9 comentários (nosso link); 3 shares | skip mediana 60,6%; >70% em 2 de 14; tempo 4,95 s |
| TikTok | 11 | views mediana 189; 3 shares; 1 comentário | tempo médio mediana 2,1 s; <4 s em 9 de 11 |
- 30 dias TikTok (Buffer): 41 posts, 9.271 views, tempo 2,79 s, 531 reações, 4 comentários, 15 shares, engajamento 5,9%. Acumulado FB (14/10): 49 posts, 35 comentários, 14 cliques, 0 shares/salvos. IG: 48 posts, 31 comentários, 4 shares, 1 salvo, 0 cliques.
- Parciais (<24h): FB 23/10 10:04 carro 309 (3,4 s), 14:06 unha 249 (3,1 s), 19:06 gato água 210 (3,9 s); IG 23/10 11:08 4, 15:02 17, 20:03 32 (skip 83%). TikTok 23/10 14:21 coleira 188 (1,7 s, 15 reações), 20:21 banho 57 (11 h).
- FORMATO (vídeo, sem causa provada): IG meme 8 s alcance 102 (n=13, skip 55%) x explicador 38 (n=27, skip 75%): meme ganha. FB meme 8 s e explicador empatam em views (~220) e tempo (~3,8 s).
- TEMA (hipótese, n pequeno): no TikTok 3 dos 4 vídeos com mais reações são gato (27, 19, 15); o maior tempo é "cachorro aguenta quantas horas sozinho" (7,3 s, tema do Sozinho em Casa). Gato = curtida; "sozinho" = retenção.
- Seguidores (último valor): FB 8, IG 0, TikTok 19 (Buffer não informa). Comentários de terceiros: sem prova nova (comentários vistos são o nosso link).
## 2. Gatilho de mudança (regra_mudanca_rapida.md): DISPAROU
- FB tempo <6 s em 13/15; TikTok <4 s em 9/11 e mediana 189 (<400); IG alcance mediana 61,5 (<80); IG skip >70% em 2/14 (no limite). Plano: data/social/plano_de_mudanca_2026-10-24.md; ações E97-E100 em data/decisoes/execucao.md.
## 3. Horários (Fortaleza): manter a grade (congelada)
| Rede | Melhor 1 | Melhor 2 | Nota |
|---|---|---|---|
| FB | 10:00 | 19:00 | vídeo 12:00 (meme) 212-440; 14:00 242; 8:30 e 21:00 de 2 posts cada |
| IG | 11:00 (explicador baixo) -> meme em 13:00 | 20:00 | meme IG 13:00 mediana 93; 21:10 102; explicadores 11/15/20h 24-34 |
| TikTok | 10:20 | 20:20 | views 166-218 em qualquer hora; sem sinal de horário |
- Mesma grade seg-dom. Zernio best_time (UTC, 1-6 posts/slot, engajamento 0-20 inflado por nossos comentários): inconclusivo; FB qua 19 UTC (16h) 20 com n=1. Fonte pública: Metricool (estudo 2026, IG 24 mi de posts, TikTok 2,3 mi; sem fuso informado): pico IG/TikTok 18-21h, FB 10-14h [metricool.com/pt/melhor-horario-para-postar-nas-redes-sociais]; Stone/Reportei/AgênciaGram listam horários parecidos (não abertos nesta rodada). Vale mudar? Não: o horário não explica nada (imagem=0 em qualquer hora). Ler de novo em 03/11.
## 4. Hashtags e legenda
- Quantidade: IG 3-5 (nunca 6, Tecnoblog 18/12/2025), TikTok 3-5, FB 0-3 (a casa fica em <=3). Busca de hoje (2 buscas) só trouxe títulos; nada novo aberto além de Metricool 04/12/2025 e Buzzmonitor/Mundo do Marketing 24/04/2024 (#amor, #pet, #pets, #cachorros no topo de 500 posts pet BR). Conjuntos por tema e 3 modelos por rede: config/estrategia_social.yaml (hashtags, modelos_legenda). Nada de #fyp/#viral.
- CTA fixo: "Confira o artigo completo em tutorialpet.com.br"; link só no 1º comentário.
## 5. Interação e isca — ESTADO (checado, sem pedir criação)
- (i) captura/guia.html existe no repo sozinho-em-casa-app mas NÃO está em landing/ (landing tem 7-erros.pdf, index.html, obrigado.html; ao vivo: sem dado, WebFetch negado). GUIA/"7 Erros" foi descartada em 21/10 (05 Decisões). Isca vigente: MIMO "Carteirinha do Pet" (decisao_isca_2026-10-22.md); PDF do mimo NÃO existe (data/audiencia/mimo ausente; E27 aberta).
- (ii) ManyChat: sem leitura da nuvem. Última evidência (Medidor 23/10 21:15, Chrome do Allan): contatos 0/1000, execuções GUIA sem dado; 05 Decisões: GUIA suspenso, 1 post, 0 execuções. Texto da DM/preço ao vivo: sem dado; o rascunho E59 já usa R$ 27 (fluxo_mimo_fase1.md passo 9, não ativo).
- (iii) Brevo: lista "7 Erros - Isca" 0 contatos (Medidor 23/10); sem e-mail transacional (captura/LEIA-ME).
- PENDÊNCIAS REAIS: E51 (R$ 9,90/NcQChat/vercel.app em legenda.txt de 47 pacotes media, inclusive agendados); E27 (PDF do mimo); ManyChat/Brevo ao vivo (PC). Nada de "autorizar criar".
- 5 perguntas por tema para hoje: config/estrategia_social.yaml, perguntas_lote_2026_10_24.
## 6. Painel mínimo (meta até 03/11; hipóteses, sem promessa)
- FB: views mediana 220+ (vídeo); tempo >=4,5 s; comentário de terceiro >=1/sem; seguidores +1/dia; imagens 0. IG: alcance mediana 80; skip <=55%; shares+salvos >=1/sem; imagens 0. TikTok: views mediana 300; tempo >=2,5 s (E95) e depois >=4 s; 1 share a cada 4 posts; seguidores +1/dia.
- Trocar horário, gancho ou CTA: 2+ posts do mesmo formato em 3 dias acima do gatilho; leitura em 24 h. Próximas leituras: 25/10 (E94 IG), 26/10, 27/10, 03/11.
## 7. Decisões do Allan (reais)
Nenhuma nova. Segue A02 (2FA e campo "Site" do TikTok) e E13. Não repito pedido de criar ManyChat/isca.
## 8. Sem dado
Gancho/voz/CTA por post, % assistido FB, seguidores TikTok via Buffer, ManyChat/Brevo/Kiwify e landing ao vivo, vendas, cliques por rede, comentários de terceiros exatos.

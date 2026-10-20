Dados até 2026-10-20 11:45 (Fortaleza). Campanha orgânica de 14 dias (qua 21/10 a ter 03/11). Só recomendação: eu não publico, agendo, compro nem mexo em anúncio. Nenhum anúncio agora (Allan, 20/10). Complementa plano_de_mudanca_2026-10-20.md (E01-E05).
Amostra: os 4 vídeos TikTok sem emoção da Duda (filhote-morder, sachê gato, sair-na-rua, ficar-sozinho) NÃO contam como prova de formato; excluídos da amostra limpa (config/estrategia_social.yaml > campanha_organica.amostra_excluida).

## (a) Diagnóstico: por que 0 comentário de terceiro em 41 posts (hipóteses; n pequeno, sem afirmar causa)
1. ALCANCE PEQUENO: mediana FB 215 views, IG 46 de alcance, TikTok ~190. Com taxa típica de comentário bem abaixo de 1% das views (ordem de 0,1-0,5%; referência genérica, não medida por nós), o esperado em 200 views é 0 a 1 comentário. Parte do zero é matemática, não só texto.
2. NENHUMA AÇÃO PEDIDA: o CTA escrito é "Confira o artigo completo" (sai da rede, ninguém comenta). Os falados já misturaram 2 ações ("salvar + seguir"). Quem decide em 1 s não executa 2 pedidos.
3. PERGUNTA ABERTA: "Conta aqui" exige digitar uma frase. Pergunta de 1 palavra (gato ou cão?) custa 1 toque.
4. RETENÇÃO ANTES DO CTA: tempo médio 1,4-4,3 s em vídeos de 36-55 s; o CTA fica no último segundo, que quase ninguém vê. Em 8 s o CTA está ao alcance de quem ficou.
5. VOZ: 4 dos últimos TikToks saíram com voz neutra, sem emoção; parte da baixa retenção é voz (corrigido no portão da Duda, a9ada46). Sem refazer.
6. SEM GATILHO NO 1º COMENTÁRIO: o comentário inicial só tem o link, nenhum convite.
7. CONTA NOVA: seguidores desconhecidos (pendente); sem base, a rede só mostra para quem já interage.

## (b) CTA novo por formato: UMA ação, no último segundo (o CTA falado gira a cada vídeo, a ação não)
| Formato | Ação única | Roteiro do último segundo |
|---|---|---|
| Meme 8 s "Gato x Cachorro" | Comentar 1 palavra | 6,5-8,0 s: texto grande "GATO ou CÃO?" + Duda (até 6 palavras): "Qual é o seu? Escreve aí!" / "Diz aí: gato ou cão?" / "Eu sei qual é o seu. Comenta!" |
| Meme/dica 8 s "Erro de 8 segundos" | Salvar | 6,5-8,0 s: texto "SALVA" + Duda: "Salva pra não esquecer." / "Guarda esse aqui." / "Salva e confere depois." |
| 15-20 s "Voz do pet" (Duda) | Compartilhar com quem tem pet | Últimos 2 s: Duda: "Manda pra quem tem um [gato/cachorro] assim." / "Marca o tutor dele." / "Esse é igualzinho ao seu? Manda pra ele." |
| 25-35 s "Dúvida do Tutor" | Comentar um número | Últimos 2 s: Duda: "Comenta aqui quantas horas o seu fica sozinho." (pergunta numérica específica do artigo) |
- Legenda (todas as redes): gancho + 1 linha de valor + a MESMA pergunta de 1 palavra + CTA fixo "Confira o artigo completo em tutorialpet.com.br". FB/IG: link só no 1º comentário. TikTok: nunca "link no perfil".
- 1º comentário FB/IG: "[pergunta de 1 palavra]? Artigo completo: [URL com UTM]". Fixar (pin) não é possível por API: ver decisão 3.
- Sem alegação médica, sem preço por dia/mês, bicho do vídeo = bicho do tema.

## (c) Quatro séries, ganchos prontos
S1 "A Duda Dubla" (15-20 s, voz com emoção da Duda, raça citada = raça do vídeo): 1) "Você saiu e eu já estou na janela. Falta muito?" 2) "Derrubei o copo? Derrubei. E vou te olhar nos olhos." 3) "Isso não é mordida, é meu jeito de pedir 'brinca comigo'." 4) "Tigela vazia, olhar fixo. Eu espero você aparecer."
S2 "Gato x Cachorro" (8-10 s): 1) Campainha tocou: quem late, quem some? 2) Hora do banho: quem foge primeiro? 3) Quem pede comida primeiro? 4) Quem acorda você de madrugada? 5) Dia de chuva, passeio: quem topa? 6) Visita chegou: quem recebe?
S3 "Erro de 8 Segundos" (8 s, abertura "Erro comum:", nunca "silenciosamente", "Para de" no máximo 1 por semana): 1) Erro comum no passeio: guia sempre esticada. 2) Erro comum: trocar a ração de uma vez (misture aos poucos; dúvida, veterinário). 3) Erro comum: água parada na tigela o dia todo. 4) Erro comum com gato: caixa de areia colada na comida. 5) Erro comum: brigar com o filhote que mordeu.
S4 "Dúvida do Tutor" (25-35 s, no máximo 1 em 3 vídeos; dúvida real de data/social/fila_duvidas_reais.md): 1) Seu cachorro aguenta quantas horas sozinho? 2) Pode dar sachê para gato todo dia? 3) Com quantos meses o cachorro pode sair na rua? 4) Como misturar ração seca e úmida?

Grade diária (3 vídeos únicos por dia; o mesmo vídeo vai para FB, IG e TikTok em horários diferentes; nunca 2 redes na mesma hora):
- M manhã: FB 08:30, IG 08:40, TikTok 10:20 | D meio: FB 10:00, IG 11:00, TikTok 17:10 | N noite: FB 21:00, IG 21:10, TikTok 20:20.
- Itens já agendados em 19:00/20:00/14:00 ficam; não crio nada novo nesses slots. TikTok: fila grátis = 10, repor todo dia.
| Dia | M (8 s) | D | N (8 s) |
|---|---|---|---|
| qua 21/10 | S2 #1 | S1 #1 | S3 #1 |
| qui 22/10 | S3 #2 | S1 #2 | S2 #2 |
| sex 23/10 | S2 #3 | S4 #1 | S3 #3 |
| sáb 24/10 | S3 #4 | S1 #3 | S2 #4 |
| dom 25/10 | S2 #5 | S1 #4 | S3 #5 |
| seg 26/10 | S3 #1 | S1 #1 | S2 #6 |
| ter 27/10 | S2 #1 | S4 #2 | S3 #2 |
| qua 28/10 | S3 #3 | S1 #2 | S2 #2 |
| qui 29/10 | S2 #3 | S1 #3 | S3 #4 |
| sex 30/10 | S3 #5 | S4 #3 | S2 #4 |
| sáb 31/10 | S2 #5 | S1 #4 | S3 #1 |
| dom 01/11 | S3 #2 | S1 #1 | S2 #6 |
| seg 02/11 | S2 #1 | S1 #2 | S3 #3 |
| ter 03/11 | S3 #4 | S4 #4 | S2 #2 |
Proporção: 28 de 42 vídeos em 8 s (2 em 3), 10 de Voz do pet, 4 de Dúvida do Tutor. Ganchos repetidos a partir do dia 26 devem mudar cena e animal. Voz da Duda só nos 14 vídeos D (crédito ElevenLabs).

## (d) Rotina de engajamento sem custo (dentro das regras)
- Responder todo comentário dos NOSSOS posts em até 1 h: o Atendente hoje roda seg/qua/sex 17:36 e só PROPÕE. Na campanha: 3 execuções por dia (08:50, 14:50, 21:50) e métrica "tempo até 1ª resposta". 1 h exato por cron custaria 1 execução por hora; só se a média passar de 5 comentários por dia.
- Respostas-modelo (curtas, sem diagnóstico, sem venda direta, saúde = veterinário): elogio → agradece e devolve pergunta; dúvida → 1 linha + "o passo a passo está no artigo (link no comentário fixado)"; resposta à enquete → "Boa! E o seu faz isso de manhã ou à noite?".
- Comentar em páginas pet brasileiras do mesmo porte: 5 por dia, texto original e específico ao vídeo, sem link, sem "segue lá", sem copiar frase. Em nome da marca = só com aprovação do Allan (decisão 2). Lista de páginas: E11 (só pesquisa, ninguém é contatado).
- Collab (IG) e dueto/stitch (TikTok): só com pet BR de porte parecido e com consentimento do dono; o convite é mensagem a uma pessoa, então vai pela decisão 2. Nada de comprar seguidores, grupos de engajamento, mensagem em massa ou automação de DM (isca digital continua adiada até haver comentário orgânico).
- Fonte de apoio sobre sinais de ranking: metricool.com/pt/algoritmo-instagram (secundária; conferir no painel nativo).

## (e) Metas e critério para liberar teste de anúncio (decisão do Allan depois; nada agora)
Base 20/10: FB views mediana 215 e tempo 2,6-5,2 s; IG alcance mediana 46, skip 44-100%; TikTok views ~190, tempo 1,4-4,3 s, 0 shares; comentários de terceiros 0.
| Meta | Semana 1 (21-27/10) | Semana 2 (28/10-03/11) |
|---|---|---|
| FB views mediana | 250 | 350 |
| IG alcance mediana / skip | 60 / ≤60% | 80 / ≤55% |
| TikTok views mediana | 300 | 400 |
| Tempo médio (8 s) | ≥4 s FB e TikTok | ≥4 s e ≥1 em 3 posts com share |
| Comentários de terceiros (3 redes) | ≥5 na semana | ≥1 a cada 5 posts |
| Shares+salvamentos | ≥10 na semana | ≥25 |
| Resposta do Atendente | mediana ≤4 h | ≤1 h na janela 08-22 h |
Metas são hipóteses, não promessas. Leituras: 22/10 (24 h dos primeiros), 24/10, 27/10 (fecha sem. 1), 03/11 (fecha sem. 2) e 04/11 o veredito do anúncio.
CRITÉRIO PARA LIBERAR TESTE DE ANÚNCIO (todos, em 7 dias seguidos, em pelo menos 1 série e 1 rede): (1) views mediana ≥ meta da semana 2 em 2 semanas; (2) tempo médio ≥50% da duração no TikTok e ≥40% no FB em 60% dos posts da série; (3) comentários de terceiros ≥1 a cada 5 posts; (4) shares/views ≥1% em pelo menos 3 posts da série; (5) ≥10 cliques/semana no 1º comentário com UTM; (6) 100% dos vídeos novos com voz da Duda aprovada pelo portão e 0 posts em erro; (7) landing do Sozinho em Casa respondendo 200. Se passar, proponho UM post vencedor e o orçamento máximo; quem decide e paga é o Allan. Se não passar, repetir o ciclo de 14 dias trocando só o gancho da série pior.

## (f) Execução
Ações E06-E11 em data/decisoes/execucao.md; config/estrategia_social.yaml > campanha_organica.

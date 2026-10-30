# Plano do lote 2 de reacts — escrito pelo Fable para o Sonnet executar (29/10/2026, 23h)
Leia antes: `biblioteca/habilidades/react_duda_padrao.md` (receita), regras de ouro 32, 41 e 42, `data/remix/metodo_react_v2_2026-10-29.md`.

## 1. O que o n03 v2 ensinou hoje (leitura 2,5 h: TikTok 30 views, 1 curtida; canal faz 126-218)
1. **Gancho atrasado.** A trilha foi feita para o Remix (3,5 s de silêncio no começo) e foi publicada em tela dividida sem ajuste: 3,5 s sem legenda, Duda calada, clipe sem ação. Regra 32 manda gancho no quadro 0. Correção: cortar o original para abrir na ação e Duda falando no 1º segundo.
2. **Clipe repetido.** O TikTok reconhece vídeo já publicado e reduz distribuição de não original. Mitigar: clipe ocupa no máximo 60 % da tela, Duda grande em cima, nossa legenda e carimbo, corte diferente do original (começa no pico, não no 0 s), áudio original baixo (25 %) com a voz da Duda em cima.
3. **Horário não é suspeito** (dados do canal: views iguais em qualquer hora). Não mexer na grade.
4. **Marca d'água de terceiros.** Os clipes do Pubity trazem a caixa "P" com texto em inglês queimada no meio do quadro. Regra [C]2 (analise_referencia_viral): nada de referência com marca de outro app entra. Além disso o crédito ficaria errado (Pubity reposta). r06-r10 vão para a RESERVA até achar o criador original. Prioridade passa para os clipes de página de notícia brasileira (Metrópoles, iG): marca editorial pequena, crédito limpo, texto em português.

## 2. Ordem de execução (uma variável por teste)
| # | Peça | Variável testada | Quando | Crédito |
|---|---|---|---|---|
| A2 | n03 remontado (mesmos clipes W e C da Duda, zero HeyGen) | abertura: original cortado para abrir no pico + gancho no quadro 0 + Duda falando no 1º s | sex 30/10 10:20 TikTok, 08:30 FB, 08:40 IG | 0 |
| r01 | cachorro atleta dos cones (Metrópoles) | 1º react novo com a receita completa | sex 30/10 20:20 / 21:00 / 21:10 | ≈ 12-15 créditos (3 %) |
| r02 | gato barrigudinho que vem quando chamam (Metrópoles) | fofura vs humor | sáb 31/10 10:20 / 08:30 / 08:40 | ≈ 12 |
| r05 | cachorro no passeio de carro (iG) | reserva do fim de semana | sáb 31/10 noite | ≈ 12 |
Leitura de cada um em 1 h, 3 h e 24 h; 2 reacts abaixo de 60 % da mediana do canal = parar a série e trocar UMA peça (Fable decide).

## 3. A2 — remontagem do n03 (Sonnet faz sozinho, sem "pode" de crédito: zero)
Arquivos em `/home/claude/react_v2/` (ou Downloads/Tutorial Pet/reacts): `duda_WC.mp4` (23,3 s, Duda W+C já concatenada), `orig_n03.mp4`, `carimbo_tutorialpet.png`, `music.mp3`, `legS.ass`.
- Original: cortar de **3,0 s** em diante (o beijo chega aos 3,5 s; pico 1 aos 5,0 s). Nova linha do tempo = original − 3,0 s.
- Duda: cortar os primeiros **3,0 s** de `duda_WC.mp4` (ela fica muda até 3,5 s; "Olha o beijo chegando…" começa em 3,5 s → passa a 0,5 s). Duração final ≈ 20,3 s.
- Legenda: todas as entradas de `legS.ass` deslocadas −3,0 s; nova linha no quadro 0: **"POV: A FISCAL DO BEIJO"** de 0,00 a 3,90 s (estilo topo, MarginV 640). Confirmar que nenhum texto nosso cobre o texto queimado da Metrópoles (rodapé).
- Montagem igual ao padrão (crop Duda 1080x672 y=450 em cima; original 1080x1248 y=200 embaixo; áudio original 25 %; música 10 %; loudnorm −14; carimbo canto superior direito). Conferir 5 quadros (0 s, 2 s, 5 s, 12 s, 19 s).
- Nome: `react_n03_v3_A2_abre_no_pico_gancho_quadro0.mp4` + versão comprimida ≤ 10 MB.
- Legenda do post (igual à de ontem, muda só a 1ª linha): "Ela não deixa NINGUÉM beijar 😂🐶 Time beija ou time não beija? Comenta aí! Vídeo original de @metropoles (via @dienifersilvabarbosa) #pinscher #cachorro #react #tutorialpet" (TikTok: @metropolesoficial).
- Publicar pelo Buffer (upload Zernio, customScheduled): TikTok 10:20, FB 08:30 (reel), IG 08:40 (reel, feed, isAiGenerated). Rótulo IA no TikTok.

## 4. r01 — "Atleta de quatro patas" (Metrópoles, 57 s, 205 mil views, 29/10)
Link TikTok: https://www.tiktok.com/@metropolesoficial/video/7702052114108894516 (achar e anotar o link no Instagram do Metrópoles antes de publicar). Clipe baixado em `/home/claude/react_fila/r01.mp4`; folha de quadros `r01_sheet.jpg`.
**Mapa de batidas (tempo do original):** 0-2 s tutor grita "Vai, vai, vai!", cachorro branco salta sobre o 1º cone amarelo e preto · 3,5-5 s "Vai, vai, vai!" de novo, 2º e 3º cone · 6-12 s sequência de saltos cone a cone · 14-16 s ele para e espera · 20-23 s "E aí? Será que ele vai?" e mais um salto · 38-46 s nova sequência de saltos (fecho forte).
**Corte:** 0,0-14,0 s (gancho + 5 saltos). Texto Metrópoles no rodapé o tempo todo: não cobrir.
**Falas da Duda (padrão: 3 pontos + CTA; cada linha = 1 take no ElevenLabs):**
- P1 (0,2 s, olhando o clipe) [excited] "Olha o treino dele!"
- P2 (2,6 s, no 1º salto) [laughing] "Pulou!"
- P3 (6,0 s, na sequência) [playful] "Um, dois, três… ele não erra um!"
- P4 (9,5 s, voz do pet, olhando o clipe) "Papai, isso aqui é aquecimento."
- P5 (11,5 s, vira para a câmera) [playful] "É isso aí, ele tá de plantão na pista!"
- P6 (13,0 s, câmera, CTA) "Seu cachorro pularia? Comenta aí!"
Texto na emenda: 0 s "POV: ATLETA DE QUATRO PATAS" · 2,6 s "PULOU!" · 6 s "UM, DOIS, TRÊS…" · 9,5 s "ISSO É AQUECIMENTO" · 13 s "SEU CACHORRO PULARIA?".
Looks: W = "Smiling person in patterned shirt" (olhando para baixo-direita; o cachorro corre da esquerda para a direita, confere no quadro 0 que a ação está do lado direito; se estiver à esquerda, gerar look espelhado, 2 créditos). C = "Duda" (câmera). Trechos: W 0-11,3 s; C 11,3-14,5 s. Custo previsto ≈ 12 créditos (0,8/s) = 3 % de 404.
Cartão de "pode" para o Allan ANTES da voz: as 6 falas + CTA + custo. Depois: voz por linha → trilha → animático (5 quadros) → "pode" → HeyGen → montagem → Buffer.

## 5. r02 — gato barrigudinho que vem quando chamam (Metrópoles, 135 mil, 28/10)
Link: https://www.tiktok.com/@metropolesoficial/video/7701825418474605845. Etapa B pendente (baixar com yt-dlp em `/home/claude/react_fila/r02.mp4`, transcrever, folha de quadros, mapa). Hipótese de roteiro: Duda chama junto com a tutora ("Vem, neném!"), reage ao barrigão no pico ("Olha essa barriguinha!"), voz do pet ("Chamou, cheguei. Cadê a comida?"), CTA "Seu gato vem quando chama? Comenta aí!". Ajustar timestamps depois do mapa.

## 6. r05 — cachorro no passeio de carro (iG, 100 mil, 27/10)
Link: https://www.tiktok.com/@portal_ig/video/7701432200683654401. Etapa B pendente. Hipótese: Duda como passageira, voz do pet "Motorista, mais rápido!", CTA "Seu pet é assim no carro?".

## 7. Reserva (não produzir sem decisão do Fable/Allan)
r03, r04 (Metrópoles, abaixo de 50 mil views; esperar 24 h para ver se crescem); r06-r10 (Pubity: marca d'água de terceiros e crédito incerto; só se achar o criador original e o vídeo dele sem marca).

## 8. Regras fixas desta execução
- Nenhuma voz/HeyGen sem cartão aprovado ("pode"); custo sempre em % do saldo restante (HeyGen hoje 404).
- Nomes de arquivo descritivos; tudo em Downloads/Tutorial Pet/reacts.
- Nunca publicar por conta: Buffer só depois do "pode" para a peça; conferir cada post criado; registrar em `data/remix/resultados.csv`; lições em `data/memoria/07 Erros e lições.md`; commit + push.
- Leituras agendadas com send_later (1 h, 3 h, 24 h) e aviso ao Allan só com número e % vs mediana.

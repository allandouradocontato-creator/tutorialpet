# Plano do lote 3 de reacts — curadoria v4, escrito pelo Fable para o Sonnet executar (30/10/2026, 02h30)
Leia antes: `data/remix/criterios_curadoria_v4_2026-10-30.md` (por que o lote 2 falhou e a régua nova), `biblioteca/habilidades/react_duda_padrao.md` (receita de montagem), regras de ouro 40, 41, 42 e 43.
Decisão do Allan (30/10, 01:49-01:50): cada react precisa ter pelo menos 2 destes 3 — **educativo, ilustrativo, engraçado** (os 3 juntos = melhor). Reações espontâneas. Pelo menos 3 reacts "tão bons quanto o primeiro" (n03 v2), em cima de vídeos realmente virais.

## 0. Lote 2 (r01/r02/r05): o que fica
- r01 continua agendado (FB sex 21:00, IG 21:10) **só como teste das bases novas e da montagem**; não é referência de conteúdo. As duas levas (r01 TikTok, r02 e r05) foram **canceladas** pelo Fable em 30/10 02h (gatilhos apagados). Os arquivos ficam em `Downloads/Tutorial Pet/reacts/` como reserva.

## 1. Curadoria feita (zero crédito): 45 vídeos medidos, 10 baixados e assistidos
Pool: Explorar › Animais do TikTok (30/10 02h) + fila anterior. Medição por `scripts/curadoria_tiktok.py` (yt-dlp). Os 3 escolhidos (≥ 75/100):

| # | Vídeo | Views | Compart. | Múltiplo da conta | Idade | Dur. | Pontos | O que a Duda acrescenta |
|---|---|---|---|---|---|---|---|---|
| L3-1 | @max_pegadordeencomenda — "O entregador achou que era o fim dele" (labrador pega a encomenda pela grade) https://www.tiktok.com/@max_pegadordeencomenda/video/7701105364653182226 | 5,0 mi | 40,6 mil (0,8 %) | conta que vive de viral (8,6 mi no melhor) | 4 d | 10,4 s (usar 0–8,0) | 86 | engraçado + educativo (isso é treino por recompensa) + ilustrativo |
| L3-2 | @maya.caramelo — "POV: você deixa seu cachorro com os avós enquanto viaja" (Fev 2025 magra → Out 2026 gorda) https://www.tiktok.com/@maya.caramelo/video/7701509597856664852 | 214 mil e subindo (2 d) | 5,8 mil (2,7 %) | **258x** (mediana da conta 830) | 2 d | 16,0 s (inteiro) | 82 | engraçado + educativo (vovó alimenta por amor; pote medidor/combinado) + ilustrativo (antes/depois) |
| L3-3 | @tiny.mischiefs — gatinho cinza caça o próprio rabo e o amigo laranja segura o rabo com a pata https://www.tiktok.com/@tiny.mischiefs/video/7701480166870027542 | 830 mil | 52 mil (6,3 %) | 55x (mediana 15 mil) | 3 d | 11,9 s (inteiro) | 84 | engraçado + educativo (filhote = brincadeira; adulto toda hora = vet) + ilustrativo |

Reserva (60-74): @lifewithkaliandkane rottweilers "the looks I get when I come home late" (1,4 mi, texto em inglês queimado); @catographer123 gatinho correndo (2,8 mi, sem pico). Descartados: @amordeaumigo (94 s, compilação), @bernardobax (coruja + policial fardado), @joycefernanda.02 (69 s, pitbull sem pico), r03/r04/r06-r10 da fila antiga.
Nenhum dos 3 tem marca d'água de app. Crédito: @max_pegadordeencomenda (Instagram igual), @maya.caramelo, @tiny.mischiefs. Originais baixados em `Downloads/Tutorial Pet/reacts/originais_lote3/` (e no sandbox `/home/claude/curadoria/cand/`).

## 2. Mapas de batidas (assistidos com áudio, transcrição faster-whisper)
**L3-1 Max** (áudio: 0–2 "Ele vai pegar aí com você?" · 2–3 "Oi?" · 3–4 "Ele vai pegar com você?" · 4–5 "Pega?" · 5–7 "É, ele pega!" · 7–8 "Ah." · 8–10,4 cartela preta "Directed by" = CORTAR)
0–2 entregador no portão olhando o celular, cão vem · 3–5 cão sobe na grade · **6,0–7,0 PICO: cão pega a caixa pela grade** · 7–8 entregador paralisado.

**L3-2 Maya** (áudio: tutora "Meu Deus do céu, Mariah!" perto do corte, resto ambiente)
0–1 cachorra magra na porta (Fev 2025) · 1–5 pula e abraça · **6,0 PICO 1: corte "Out 2026", cachorra gorda entra bamboleando** · 8–9 **PICO 2: pula e mostra o barrigão** · 9–15 abraço, barriga em cena.

**L3-3 Gatinhos** (sem fala)
0–3 cinza gira atrás do rabo · **4,5–5,0 PICO: laranja põe a pata no rabo dele** · 6–8 laranja segura o rabo, cinza olha · 9–11 cinza gira de novo.

## 3. Cartões de falas (regra 41: 3 pontos com timestamp; Duda tutora; tags do ElevenLabs entre colchetes)
Formato de montagem: receita do `react_duda_padrao.md` (Duda em cima 1080x672, clipe embaixo, legenda Poppins 62, carimbo, áudio original 25 %, música 10 %, loudnorm 2 passadas + alimiter level=0). Tempo total = clipe + cauda da Duda (4–6 s). Trecho W = Duda olhando o clipe (look "W" da base); C = Duda para a câmera.

### L3-1 "Ele pega mesmo" — base B3r varanda (W baixo-esquerda / C câmera). Total ≈ 14,5 s
| t (montagem) | Quem | Fala / tela |
|---|---|---|
| 0,0–1,4 (quadro 0 do clipe congelado) | Duda W | "[curious] Olha a cara de medo do entregador." |
| 1,4–9,4 | clipe 0–8,0 | áudio original (diálogo) em 60 % aqui, porque a piada está na fala |
| 7,6 (no "É, ele pega") | Duda W | "[laughs] Ele PEGA mesmo!" |
| 9,4–14,5 | Duda C | "Isso é treino, viu? Cada entrega virou brincadeira com prêmio. O seu recebe encomenda ou late pro entregador? Comenta aí!" |
Texto na tela: 0–1,4 "POV: O ENTREGADOR NÃO ACREDITOU" · 1,4–7,5 "ELE VAI PEGAR?" · 7,5–9,4 "ELE PEGA MESMO!" · 9,4–12 "CADA ENTREGA = BRINCADEIRA + PRÊMIO" · 12–14,5 "O SEU RECEBE OU LATE?"
Legenda do post: "O entregador não acreditou 😂📦 Isso é treino com recompensa! O seu recebe encomenda ou late? Comenta aí! Vídeo original de @max_pegadordeencomenda #cachorro #labrador #react #tutorialpet"

### L3-2 "Voltou dos avós" — base B2r sofá (W cima-esquerda / C câmera). Total ≈ 21 s
| t | Quem | Fala / tela |
|---|---|---|
| 0,0–1,6 | Duda W | "Deixou o cachorro com os avós na viagem? Olha o que volta." (clipe já rodando, áudio original 25 %) |
| 6,0 (corte Out 2026) | Duda W | "[gasp] MARIAH?! [laughs] Virou um barril!" |
| 9,0 (pulo do barrigão) | Duda W | "[laughs] Olha essa barriga!" |
| 15,5–21 | Duda C | "É amor em forma de petisco: vovó dá escondido e ninguém mede. Pote com medidor e um combinado com a vovó resolvem. O seu voltou assim? Comenta!" |
Texto na tela: 0–6 "POV: DEIXOU COM OS AVÓS" · 6–9 "VOLTOU ASSIM 😳" · 9–15,5 "AMOR EM FORMA DE PETISCO" · 15,5–21 "POTE COM MEDIDOR + COMBINADO COM A VOVÓ" (vertente B futura: pote hermético com medidor, 12 %, está na lista Shopee; NÃO incluir link neste teste — uma variável por vez)
Legenda: "Deixou com os avós e voltou assim 😂🐶 Amor em forma de petisco! O seu também voltou 'fofinho'? Comenta aí! Vídeo original de @maya.caramelo #cachorro #caramelo #react #tutorialpet"

### L3-3 "O amigo segurou" — base B1 cozinha (W camisa baixo-direita / C câmera). Total ≈ 17,5 s
| t | Quem | Fala / tela |
|---|---|---|
| 0,0–1,5 | Duda W | "Ele vai pegar o rabo? Nunca pega." |
| 4,6 (pata no rabo) | Duda W | "[laughs] O amigo segurou pra ele!" |
| 12,0–17,5 | Duda C | "Filhote caçando o rabo é brincadeira. Adulto fazendo isso toda hora, aí é conversa com o veterinário. Seu gato já pegou o próprio rabo? Comenta!" |
Texto na tela: 0–4,5 "POV: A CAÇA AO RABO" · 4,5–7 "O AMIGO SEGUROU 😂" · 7–12 "DUPLA DINÂMICA" · 12–17,5 "FILHOTE = BRINCADEIRA. ADULTO TODA HORA = VET"
Legenda: "O amigo segurou o rabo pra ele 😂🐱 Filhote caçando o rabo é brincadeira; adulto toda hora, vale conversar com o vet. O seu já pegou o próprio rabo? Comenta aí! Vídeo original de @tiny.mischiefs #gato #gatinho #react #tutorialpet"

## 4. Ordem de execução e custo (uma variável por teste; nada de voz/HeyGen antes do "pode")
1. Baixar os 3 originais (yt-dlp, links acima) → `react_fila/l3_1_max.mp4`, `l3_2_maya.mp4`, `l3_3_gatinhos.mp4`; cortar o L3-1 em 0–8,0 s. Conferir `biblioteca/clipes_banidos.md`.
2. ElevenLabs Marianne (estab. 0,26) por fala, nomes `voz_l3_1_P1_olha_a_cara.mp3` etc. Custo ≈ 0,6 % do saldo restante do ElevenLabs (3 reacts).
3. **Animático** dos 3 (clipe + voz + Duda parada, zero HeyGen) → mostrar ao Allan e PARAR para o "pode".
4. Com o "pode": HeyGen Avatar IV, W + C por react (≈ 9–13 s W, 5–6 s C): ≈ 42 créditos ≈ **12 % do saldo restante** (~350 após o lote 2; conferir na tela e corrigir a %).
5. Montagem (mont.py), 10 MB + alta, folha de quadros, mostrar os 3 na hora.
6. Publicação pelo Buffer com upload Zernio, em ondas (limite 10): 1 react por dia, FB 21:00 / IG 21:10 / TikTok 21:20, nunca colado em post de artigo (≥ 1 h). Ordem: L3-2 (está subindo agora, 2 d) → L3-1 → L3-3. Leituras 1 h / 3 h / 24 h com send_later.
7. Registrar: `fila_virais.csv` (pontuação por critério), `resultados.csv`, `07 Erros e lições.md`, `react_duda_padrao.md`; commit + push.

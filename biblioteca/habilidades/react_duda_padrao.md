# React com a Duda — padrão aprovado (n03 v2, 29/10/2026)
Decisão do Allan: o react n03 v2 "fiscal do beijo" é o PADRÃO. Repetir igual; mudar só o clipe e as falas. Objetivo: o próximo sair mais rápido (hoje levou ~3 h; meta 1 h).

## Resultado que o Allan aprovou
- Duda ATUA o vídeo inteiro: assiste o clipe junto com o público, olhando para onde o clipe está (embaixo = olhar para baixo), e vira para a câmera nas reações finais e no CTA.
- Espontaneidade: sorriso velado, gargalhada só no pico, piscadinha e gesto de mão no fim; pausas reais entre as falas (silêncio dela + áudio do original).
- Olhar: inclinado para o LADO ONDE ESTÁ A AÇÃO do clipe (no n03 o casal estava à direita da imagem; a Duda olha para baixo e para a direita da imagem). Conferir isso ANTES de gerar o clipe.

## Receita (ordem fixa)
1. **Clipe na mão** (yt-dlp) + transcrição + mapa de batidas segundo a segundo (regra 41). Guardar na fila o link do Instagram E do TikTok do original.
2. **Cartão de texto para o "pode"**: falas por linha, com timestamp, CTA de escolha entre posições reconhecíveis ("Time beija ou time não beija? Comenta aí!") e custo em % do saldo. Fala não repete o que a imagem já mostra (não dizer "a cachorra").
3. **Voz** (ElevenLabs Marianne, v4, stability 0,26, tags [playful]/[laughing]) gerada LINHA POR LINHA, para trocar uma sem refazer tudo. Montar a trilha na linha do tempo (voz_timeline) com 3,5 s de silêncio inicial se for Remix (o app toca o original do 0 s).
4. **Animático** (clipe + voz + Duda parada) para o Allan ouvir o tempo. Só com "pode" vai para o HeyGen.
5. **Looks**: no HeyGen não há controle de olhar; o olhar vem da foto. Looks salvos no avatar Duda: "Duda" (câmera) e "Smiling person in patterned shirt" (olhando para baixo-direita, com celular). Se precisar de outro olhar: Look Studio > Gerar com IA, descrever o lado pelo LADO DA IMAGEM ("looking down toward the RIGHT side of the image") em inglês; refinar custa 2 créditos por rodada; limite 6 créditos sem novo "pode".
6. **Clipes Avatar IV (Turbo, 1080p, retrato)**: trilha dividida em W (olhando o clipe) e C (olhando a câmera), um clipe por trecho, áudio enviado como arquivo (aba Áudio). Custo real: ≈ 0,8 crédito/s (14 s = 12; 9 s = 7).
7. **Baixar do HeyGen**: abrir o mp4 do CDN (`location.href = video.src`) e baixar com nome descritivo; NUNCA baixar vários arquivos em lote por JS (o Chrome bloqueia os downloads do site).
8. **Montagem (ffmpeg)**: concat W+C → (a) REMIX: só Duda, legenda centralizada, carimbo, música 10 %, loudnorm -14; (b) TELA DIVIDIDA: Duda crop 1080x672 (y=450) em cima, original 1080x1248 embaixo, legenda na emenda (MarginV 640, estilo topo), áudio do original a 25 %. Conferir 5 quadros antes de entregar.
9. **Publicar pela nuvem**: Remix nativo NÃO dá (nem pelo celular do Allan). Vai a TELA DIVIDIDA, comprimida ≤ 10 MB (b:v 2900k; SSIM visual ok), subida pelo link de upload do Zernio (arquivo fica 7 dias em media.zernio.com/temp), agendada no Buffer: TikTok 20:20, FB 21:00 (Reel), IG 21:10 (Reel, feed), rótulo IA em TikTok e IG (FB não tem o campo). Crédito na legenda: "Vídeo original de @conta (via @criadora)".
10. **Leitura**: 1 h, 3 h, 24 h; anotar em data/remix/resultados.csv; comparar com a média da semana.

## Custos de referência
HeyGen 25 créditos no total (6 looks + 12 W + 7 C) = 5,8 % de 429. ElevenLabs ≈ 0,3 %. Meta para o próximo: ≤ 20 créditos (looks já salvos).

## Bases visuais da Duda (30/10/2026)
Cada react usa uma base diferente (mesma personagem). Looks salvos no avatar Duda do HeyGen; fotos em Downloads/Tutorial Pet/reacts/bases_duda/.
- B1 cozinha, camisa estampada, cabelo solto, Duda em cima: "Smiling person in patterned shirt" (W baixo-direita) + "Duda" (C).
- B2 sofá (Duda EMBAIXO, clipe em cima): "Cozy hoodie wearer with puppy" (W cima-esquerda) + "Cozy hoodie owner with puppy" (C). Rabo de cavalo, moletom cinza, poodle no colo, luz de abajur. O gerador ignorou "cima-reto" (saiu olhando a câmera): não gerar de novo, usar cima-esquerda.
- B3 varanda (Duda em cima): "Smiling balcony dreamer" (W baixo-esquerda) + "Smiling balcony sunlit friend" (C). Coque, camiseta preta, planta e grade.
- Lição de prompt: o Look Studio devolve 2 opções por geração (a 1ª geração custou 2 créditos); para olhar lateral/baixo funciona ("eyes clearly lowered, head tilted down"); olhar "reto para cima" não funciona.
- Custo das 4 gerações: 8 créditos = 2,0 % de 404 (saldo 396).

### Versão REALISTA das bases B2/B3 (30/10/2026, preferida; as "bonitas" acima ficam de reserva)
Pedido do Allan: menos produzido, mais gente comum. Prompt = texto do look + bloco comum "selfie de celular, sem maquiagem, textura de pele, luz comum, nada posado". Fotos em Downloads/Tutorial Pet/reacts/bases_duda/ (comparacao_bases_antigas_vs_realistas.jpg mostra antigos x novos).
- B2r sofá real (Duda EMBAIXO, clipe em cima): duda_base2r_sofa_real_W_cima_esquerda.jpg (HeyGen "Cozy hoodie wearer with puppy", o 2º com esse nome, o mais recente) + duda_base2r_sofa_real_C_camera.jpg ("Cozy hoodie girl with puppy"). Rabo bagunçado, moletom cinza, poodle no colo, controle e manta no sofá.
- B3r varanda real (Duda em cima): duda_base3r_varanda_real_W_baixo_esquerda.jpg ("Smiling balcony dweller", 2º da grade) + duda_base3r_varanda_real_C_camera.jpg ("Smiling balcony dweller", 1º da grade). Coque solto, camiseta preta amassada, varal e cadeira de plástico, céu nublado.
- Os 4 saíram na 1ª tentativa (a 1ª opção de cada geração era a boa; a 2ª demorou ou falhou), sem refino. Nomes iguais no HeyGen: identificar pelo id (sofá W = a55f5f9d…, sofá C = 2d9af092…, varanda W = 74bcc0c0…, varanda C = f1b246ba…).
- Custo: 4 gerações = 8 créditos = 2,0 % de 396 (saldo ≈ 388, conferir no HeyGen).

## Clipes e montagem com as bases B1/B2r/B3r (30/10/2026)
- 6 clipes HeyGen (W+C por react, ~48 s no total, ≈ 38 créditos ≈ 9,8 % do saldo de ~388); conferir o saldo na tela e corrigir se divergir.
- Áudio: enviar ao HeyGen o MP3 da Marianne por trecho; a montagem usa a voz limpa do ElevenLabs, não o áudio do HeyGen.
- Montagem: Duda 1080x672 + original 1080x1248; áudio original 25 %, música 10 %, loudnorm 2 passadas + alimiter level=0 (−14,3 LUFS). Receita em reacts_final/mont.py.
- Original com segundos mortos: jump cut antes. Publicação: Zernio presign + Buffer em ondas (limite 10).

## Tom do react de PRODUTO (v3, 30/10/2026, pedido do Allan)
- Conversa de amiga contando um achado: energia de venda, mas natural ("olha, essa é mão na roda", "gente, olha essa cena"). Nada de texto educativo seco nem de locução de comercial.
- A Duda REAGE e OPINA; NÃO diz que comprou, usou ou testou o produto (é avatar: evitar falso depoimento). Gancho e fechamento seguem a mesma regra.
- CTA ("o link tá na bio") SÓ no fechamento C2, uma vez. Sem bordão ("tá de plantão" não é do Tutorial Pet).
- Duda só no gancho (P1) e no fechamento (C2) em tela dividida; miolo = original em tela cheia + voz da Duda (Marianne) + legenda em blocos. Builder: reacts_final/mont_v3.py (YS_TOP=410).
- Antes de posicionar as falas N, ouvir/ler o P2 já gravado para não repetir a mesma ideia.


## Risada da Duda (decisão do Allan, 01/11/2026)
Tom aprovado: risada LEVE e CURTA, só o primeiro segundo; a parte em que a risada cresce está reprovada. Receita: voz oficial (Marianne, eleven_v4, estabilidade 0,26, sem mexer nos botões) + tags curtas no texto: "[chuckles] Hahaha!", "[laughs] Ha ha ha!", "[giggles] Hehehe... [laughs] ha!"; cortar em 1,0 s com fade de 0,15 s (ffmpeg -t 1.0 -af afade=t=out:st=0.85:d=0.15). Arquivos prontos: animaticos/lote7/risada_1s_a|b|c.mp3. Risada longa, gargalhada e efeito sonoro genérico (SFX) não servem. 2 a 3 risadas de 1 s por vídeo, nos pontos de ação do clipe; nunca por cima da fala.

## Banco de reações da Duda (decisão do Allan 01/11/2026, para não gastar crédito por vídeo)
- Duda só aparece no 1º segundo (abertura) e no final (chamada); o meio é o vídeo original em tela cheia, com comentário só em voz.
- Clipes fixos em `animaticos/lote7/heygen/banco/clipes/`: A (risada + "Ai, meu Deus do céu!", look olhando celular, 2,6 s) e D ("Segue o tutorial pet", look câmera, 2,2 s). Custo total ≈ 11% do saldo; reaproveitar sempre, 0 crédito por vídeo novo.
- Lição: o HeyGen NÃO aceita áudio só de risada (botão Continuar não avança); precisa de fala junto.
- Lição: o look "Smiling person in patterned shirt" levanta o olhar para a câmera por ~1 s no meio do clipe; não há controle do olhar.

## PADRÃO v3 TRAVADO (01/11/2026, após erro no @celiaepeggy v1) — o único formato de react até o Allan mudar
Erro que originou: Sonnet trocou tela dividida por Duda em tela inteira e trocou a pergunta final combinada por CTA genérico. Lição: custo reduz TEMPO da Duda, nunca muda o FORMATO.
Linha do tempo fixa (1080x1920, 30 fps):
1. ABERTURA 0–2,6 s — TELA DIVIDIDA: em cima clipe do banco A (risada + "Ai, meu Deus do céu!", crop 1080x672 y=450); embaixo o original (scale -2:1248, pad 1080x1248) já rodando do seu beat 0. Crédito "@autor (rede)" na emenda (y≈640).
2. MEIO — ORIGINAL EM TELA INTEIRA, sem Duda na imagem; crédito continua. Áudio: original a 90%; por cima, risadas do banco (risada_1s_a/b/c.mp3) nos beats e a(s) fala(s) curta(s) da Duda (ElevenLabs, já aprovadas em cartão). Enquanto a Duda fala, original a 30% (duck).
3. FECHAMENTO últimos 2,2 s — TELA DIVIDIDA de novo: em cima clipe do banco D ("Segue o tutorial pet", look câmera); embaixo o original continua (ou congela no último quadro se acabou).
Fixos: clipes A e D em animaticos/lote7/heygen/banco/clipes/ (0 crédito HeyGen por vídeo). Variáveis por vídeo: corte do original, falas da Duda, crédito.
ElevenLabs no mínimo: reaproveitar risadas do banco; gerar só a fala única do vídeo (≤ 90 caracteres por linha, 1 a 2 linhas); gerar pelo workflow voz_lote7 em lote.
Antes de renderizar: postar cartão de 5 linhas (beats: segundo × o que acontece × áudio). Depois de renderizar: folha de 5 quadros + o mp4. Carimbo, música baixa e versões por rede entram na etapa de publicação (regra 25/10).

## Correções do Allan em 01/11/2026 (react @celiaepeggy v3)
- O ORIGINAL TEM QUE IR CONTÍNUO, na ordem real (nunca pular trechos): o corte "prévia" saltava de ~5 s para ~13 s e sumia a sequência "Se você está contente faz AU AU" + latido. Conferir por quadros que o original não pula.
- A Duda NÃO começa rindo: primeiro ASSISTE (séria, boca fechada), e só ri DEPOIS do latido/ação.
- Em tela dividida o vídeo de baixo tem a MESMA LARGURA da Duda (1080): scale largura 1080 + crop de altura (y≈330 mantém a letra e os cachorros), nunca pad com faixas pretas.
- Trecho "assistindo calada" já existe: Downloads/Tutorial Pet/reacts/clipes_heygen_lote5/react_b03_duda_clipe_W_olhando_clipe_18s.mp4, silêncio real em 3,4–10,1 s (usar 4,8–9,1 s, mudo); risada visual em 11,3–14,0 s. Reaproveitar (0 crédito) em vez de gerar clipe novo.
- SINCRONIA (Allan 01/11): a risada visual da Duda e o áudio da risada têm que cair juntos. Clipe W do b03: riso visual começa em 10,12 s (pico 10,75 s, acaba ~11,1 s); mapear começo do riso ao fim do latido do original (~4,1 s) usando W 5,9–11,2 s contínuo (assiste e depois ri, sem corte). Áudio da risada (BANCO_A2): início do riso em 0,4 s e pico em ~0,95 s do arquivo, entra a 3,8 s. Nunca usar trecho de W em que a boca mexe falando (11,3–13,0 s): não combina com áudio novo. Conferir sempre com folha de quadros por tempo (fps=5 com carimbo de tempo) antes de entregar.

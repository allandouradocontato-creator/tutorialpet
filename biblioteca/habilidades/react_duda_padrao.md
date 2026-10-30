# React com a Duda — padrão aprovado (n03 v2, 29/10/2026)
Decisão do Allan: o react n03 v2 "fiscal do beijo" é o PADRÃO. Repetir igual; mudar só o clipe e as falas. Objetivo: o próximo sair mais rápido (hoje levou ~3 h; meta 1 h).

## Resultado que o Allan aprovou
- Duda ATUA o vídeo inteiro: assiste o clipe junto com o público, olhando para onde o clipe está (embaixo = olhar para baixo), e vira para a câmera nas reações finais e no CTA.
- Espontaneidade: sorriso velado, gargalhada só no pico, piscadinha e gesto de mão no fim; pausas reais entre as falas (silêncio dela + áudio do original).
- Olhar: inclinado para o LADO ONDE ESTÁ A AÇÃO do clipe (no n03 o casal estava à direita da imagem; a Duda olha para baixo e para a direita da imagem). Conferir isso ANTES de gerar o clipe.

## Receita (ordem fixa)
1. **Clipe na mão** (yt-dlp) + transcrição + mapa de batidas segundo a segundo (regra 41). Guardar na fila o link do Instagram E do TikTok do original.
2. **Cartão de texto para o "pode"**: falas por linha, com timestamp, bordão da casa ("É isso aí, ela tá de plantão!"), CTA de escolha entre posições reconhecíveis ("Time beija ou time não beija? Comenta aí!") e custo em % do saldo. Fala não repete o que a imagem já mostra (não dizer "a cachorra").
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

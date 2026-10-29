# Método de react v2 — plano escrito pelo Fable para o Sonnet executar (29/10/2026)
Motivo: o react n03 saiu sem qualidade (fala não complementa o vídeo). Allan pediu análise e método com "mínimo de competência" antes de gastar mais crédito.

## 1. Por que o n03 falhou (diagnóstico honesto)
1. **Roteiro escrito sem ouvir o original.** A regra 39 manda assistir; na prática foram lidos quadros parados. A piada do original (a pinscher entra em TODO beijo, 8 vezes em 48 s) é de repetição e ritmo; sem o áudio e o tempo, a fala virou comentário genérico.
2. **Duda gravada sozinha, em monólogo de 14 s, para um vídeo de 48 s.** O plano confiou no "lado a lado" do Remix para juntar as duas partes. Mas o Remix toca os dois vídeos do segundo 0: a Duda fala sobre "entrou de novo" antes de a cachorra entrar, e some aos 14 s. Nada do que ela diz cai no momento certo.
3. **Ignorou a própria referência.** `referencias_react_2026-10-28.md` já dizia: o reator fica o vídeo todo olhando o clipe, tela dividida (rosto em cima, clipe embaixo), reação física no pico, texto de 2 a 6 palavras na emenda, e a piada vem "na voz do pet". O n03 não tem clipe, não tem tela dividida e não reage a nenhuma cena.
4. **Limite do Avatar IV.** Ele é uma cabeça falante: não olha para um clipe, não leva susto na hora certa. O que faz um react humano funcionar (a cara de reação sincronizada) é justamente o que o avatar não tem. Então a Duda não pode ser "a reação"; ela tem que ser **a narradora que sabe a hora de falar e a hora de calar**, e a piada tem que estar no texto e no corte.
5. **Nenhum teste barato antes do crédito.** Foi direto para voz + HeyGen. Faltou o animático (clipe + voz + Duda parada) para o Allan ver o tempo antes de gastar.

## 2. O que a pesquisa confirma (fontes no fim)
- React só é distribuído quando **acrescenta algo**: resposta, piada específica da cena, explicação. Reação genérica é "ruído" e não entra no Para Você.
- **Comentar enquanto toca, no momento certo.** "Comece a reação antes da recompensa do clipe" e fale nos pontos-chave; nos outros, silêncio e texto na tela.
- **Stitch/sequência cresce mais que dueto** para conta pequena: o clipe prepara, você responde; no dueto você compete com o original pela atenção.
- Alvo: vídeo viral de **24 a 48 h**; para conta pequena, originais de 10 mil a 100 mil (momentum sem ficar enterrado).
- Formato de maior teto nas nossas referências (nº 9 e 10, 3 a 5 milhões de curtidas): **sem reator**, só texto na voz do pet sobre o clipe.

## 3. Método v2 (ordem obrigatória)
**Etapa A — escolher** (zero crédito)
- Original com 1 pico claro em até 15 s e uma frase "na voz do pet" óbvia (os comentários já entregam). Janela: publicado há ≤ 48 h. Faixa alvo 10 mil a 300 mil curtidas.
- Criador que **permite** Remix/Dueto/Stitch (botão visível) OU clipe de página de notícia que reposta com crédito (Metrópoles). Anotar na fila.

**Etapa B — ter o clipe na mão** (zero crédito)
- Baixar o original para a área de trabalho (yt-dlp) ou gravar a tela pelo Chrome. Transcrever o áudio (Whisper local). Ver 1 quadro por segundo.
- Montar o **mapa de batidas**: tabela segundo a segundo com o que acontece, o som, e onde está o pico. Escolher o corte de 10 a 20 s que contém gancho + pico.

**Etapa C — roteiro sincronizado** (zero crédito, cartão para o "pode")
- Formato padrão: **tela dividida** (Duda em cima, ~35% da altura, clipe embaixo). Texto de 2 a 6 palavras na emenda, trocando a cada cena.
- Duda fala só em 3 pontos: (1) **antes do pico**, 1 frase de 1,5 s que prepara ("Olha ela chegando."); (2) **no pico**, 1 a 3 palavras com tag de emoção ("[laughing] DE NOVO!"); (3) **depois**, a frase na voz do pet + CTA de 3 s. O resto é silêncio dela (trecho mudo do HeyGen em loop) e o áudio do original alto.
- Cada fala tem **timestamp** vindo do mapa de batidas. Fala que não aponta para uma cena concreta é cortada.

**Etapa D — animático** (≈ 0,2% ElevenLabs, zero HeyGen)
- Clipe + voz ElevenLabs nos timestamps + foto parada da Duda na faixa de cima + textos. Enviar para o Allan como MP4. Só com o "pode" vai para o HeyGen.

**Etapa E — produzir** (HeyGen só do que a Duda fala: 5 a 8 s ≈ 1,3% do saldo, não 2,6%)
- Gerar a Duda só com as falas (com pausas marcadas), cortar nos timestamps, trecho mudo em loop nos silêncios. Montar com ffmpeg: legenda grande, carimbo, música a 10%, −14 LUFS, 9:16, 3 versões (TikTok/IG/FB).

**Etapa F — publicar e medir**
- Meta: Remix com **"enviar da galeria"** (existe desde 2022), nosso clipe já sincronizado do 0 s; se o Allan preferir publicar o vídeo montado como reel comum, crédito na tela e na legenda. TikTok: Stitch (clipe até 5 s + nossa parte) ou upload comum com crédito.
- Sempre 2 versões do mesmo clipe para teste no mesmo dia: **A = tela dividida com Duda; B = sem Duda, texto na voz do pet** (zero HeyGen). O que ganhar em 24 h vira o molde.

## 4. Aproveitar o n03 (zero crédito)
A Duda de 14 s já existe. Em vez de lado a lado, publicar como **Remix em sequência** (IG permite "adicionar seu clipe depois do original"): o original toca os primeiros ~8 s (a cachorra entrando no beijo), depois entra a Duda: "Não acredito. Ela entrou no meio DE NOVO!…". Nessa ordem a fala responde à cena. Vale como versão C do teste de hoje, sem gastar nada.

## 5. Próximo react (teste do método)
- Reaproveitar o n03 como clipe (já temos link, comentários e pico aos 7 s e 46 s): corte 0–12 s do original, tela dividida, Duda fala em 3 pontos, versão B sem Duda. Custo total novo ≈ 0,2% ElevenLabs + ≈ 1,3% HeyGen.
- O Sonnet executa as etapas B, C e D e para no cartão do animático.

## Fontes
- Outfeed, duet/stitch/green screen e "comente enquanto toca": https://outfeed.ai/blog/tiktok-reaction-videos/
- Slidy Creator, stitch > dueto, 24–48 h, 10 mil a 100 mil, "ruído de conteúdo": https://slidycreator.com/blog/tiktok-duet-stitch-strategy/
- Eliro, formato reação em tela dividida e tela verde (reagir antes da recompensa, terço inferior/lateral): https://eliro.pro/blog/10-video-formats-best-tiktok
- The Social Cat, Remix do Instagram (áudio original mantido, 15–30 s): https://thesocialcat.com/glossary/reel-remix-instagram
- Meta, Remix com vídeo da galeria e em sequência (2022): https://about.fb.com/news/2022/07/new-ways-to-create-instagram-reels-remix/
- Referências internas: data/remix/referencias_react_2026-10-28.md

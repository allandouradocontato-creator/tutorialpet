# Plano das bases visuais da Duda para a série de reacts (Fable, 30/10/2026 00h40)
Decisão do Allan (30/10): cada react da sequência sai com uma BASE diferente (visual + posição na tela + direção do olhar), mesma personagem, mesmo padrão de qualidade. O que muda é o ponto de vista: a Duda tem que parecer que está realmente vendo a cena, onde quer que o clipe esteja.

## 1. Regra do olhar (vale para toda base)
- Clipe EMBAIXO → Duda olha para BAIXO. Clipe EM CIMA → Duda olha para CIMA.
- Lado: o olhar aponta para o LADO DA IMAGEM onde está a ação do clipe no trecho W (conferir na folha de quadros antes de escolher o look). Ação à direita → olhar baixo-direita / cima-direita. Ação à esquerda → baixo-esquerda / cima-esquerda. Ação central (pet vindo para a câmera) → olhar para baixo/cima reto, queixo levemente inclinado.
- No trecho C ela olha para a câmera, sempre.
- Prompt do HeyGen em inglês, sempre pelo lado da IMAGEM: "looking down toward the LEFT side of the image", nunca "her left".

## 2. As três bases
| Base | Posição | Olhar W | Cenário / roupa / cabelo | Looks necessários |
|---|---|---|---|---|
| B1 (existe) | Duda em cima, clipe embaixo | baixo-direita | cozinha, camisa estampada, cabelo solto, celular na mão | "Smiling person in patterned shirt" (W) + "Duda" (C) — 0 crédito |
| B2 (nova) "sofá" | **Duda EMBAIXO, clipe EM CIMA** | cima-esquerda e cima-reto | sala à noite, luz quente de abajur; moletom cinza-claro; rabo de cavalo alto; a Maggie (poodle branca) deitada no colo, Duda com a mão nela | W cima-esquerda + W cima-reto + C câmera = 3 looks |
| B3 (nova) "varanda" | Duda em cima, clipe embaixo | **baixo-esquerda** | varanda de dia, planta e grade ao fundo; camiseta lisa preta; cabelo preso em coque; sem celular, cotovelo apoiado | W baixo-esquerda + C câmera = 2 looks |
Custo: 5 looks × 2 créditos = 10 créditos = **2,5 % de 404**. Refino (se olhar ou rosto saírem errados): até 6 créditos extras (1,5 %), avisar antes.

## 3. Prompts para o Look Studio (Avatar "Duda" > Look Studio > Gerar com IA; 1 look por vez; conferir rosto = mesma Duda)
- B2-W-esq: "Same woman, high ponytail, light grey hoodie, sitting on a sofa at night with warm lamp light, a small white poodle lying on her lap, her hand resting on the dog. She is looking UP toward the LEFT side of the image, amused half-smile, as if watching a video above her. Vertical portrait, chest up, photorealistic."
- B2-W-reto: idem, trocando por "looking straight UP, chin slightly raised, as if watching a video above her".
- B2-C: idem, "looking directly at the camera, warm smile".
- B3-W-esq: "Same woman, hair in a bun, plain black t-shirt, on a sunny apartment balcony with a plant and a railing behind her, elbow resting on the railing. She is looking DOWN toward the LEFT side of the image with a playful smile, as if watching a video below her. Vertical portrait, chest up, photorealistic."
- B3-C: idem, "looking directly at the camera, playful smile".
Baixar cada foto com nome: duda_base2_sofa_W_cima_esquerda.jpg, duda_base2_sofa_W_cima_reto.jpg, duda_base2_sofa_C_camera.jpg, duda_base3_varanda_W_baixo_esquerda.jpg, duda_base3_varanda_C_camera.jpg → Downloads/Tutorial Pet/reacts/bases_duda/. Mostrar as 5 ao Allan ANTES de gerar qualquer clipe.

## 4. Qual base em qual react (lote 2)
- r01 atleta dos cones → B1 (ação centro/direita, Duda em cima olhando baixo-direita). Já aprovado.
- r02 gato barrigudinho → B2 (gatinho sai do fundo e vem para o centro: W cima-reto nos primeiros 3 s, depois cima-esquerda quando a mão pega ele à esquerda; se o HeyGen não permitir trocar look no meio, usar só cima-reto).
- r05 cachorro foge da janela → B3 (cachorro ocupa o lado esquerdo do quadro de 0 a 10 s; Duda em cima olhando baixo-esquerda).
- Próximos reacts: alternar B1 → B2 → B3, nunca duas seguidas iguais na mesma rede.

## 5. Montagem da B2 (Duda embaixo) — muda o ffmpeg
- Topo: original scale=1080:1920, crop=1080:1248:0:60 (ou y conforme a manchete do original).
- Base: Duda crop=1080:672:0:450 (ajustar y para o rosto ficar inteiro e a Maggie aparecer).
- vstack: [original][duda]. Emenda em y=1248.
- Legenda na emenda: Alignment 2 (base), MarginV = 1920−1248+20 = 692 (texto termina logo acima da emenda); mesmo estilo Poppins Bold 62, outline 6.
- Carimbo: canto INFERIOR direito (W-w-30, H-h-30), sobre a área da Duda; não cobre o logo do original.
- Áudio, loudnorm e nomes de arquivo iguais ao padrão.
- Conferir 5 quadros e as zonas de interface do TikTok (lado direito) antes de entregar.

## 6. Ordem para o executor
1. Gerar os 5 looks (2,5 %) → mostrar ao Allan → esperar "pode" das fotos.
2. Clipes HeyGen: r01 em B1 (3,7 %), r02 em B2 (2,9 %), r05 em B3 (3,0 %).
3. Montagem (B1/B3 padrão; B2 invertida conforme seção 5) → 5 quadros → Buffer no horário do plano.
4. Registrar as bases em biblioteca/habilidades/react_duda_padrao.md (seção "Bases") e em resultados.csv (coluna voz: anotar a base).

## 3b. Versão REALISTA dos prompts (Allan, 30/10 00h47: "menos profissional, mais realidade, menos rico")
Regra: a Duda é uma tutora comum filmando no celular dela, não modelo em estúdio. Os 4 looks de 3 ficam como reserva; gerar 4 novos (8 créditos = 2,0 % de 396).
Bloco comum (colar no fim de todo prompt): "Casual phone selfie, slightly off-center, phone held at arm's length, mild lens distortion, slight grain. No-makeup look, natural skin texture with minor imperfections, a few loose hair strands. Ordinary light, no studio lighting, nothing staged. Same face as the reference."
- B2r-W-esq: "Same woman, messy high ponytail, worn light grey hoodie, sitting on an ordinary sofa in a small Brazilian apartment at night, plain white walls, a folded blanket and a TV remote on the sofa, a small white poodle lying on her lap. She is looking UP toward the LEFT side of the image, amused half-smile, as if watching a video above her." + bloco comum
- B2r-C: idem, "looking directly at the phone camera, relaxed smile" + bloco comum
- B3r-W-esq: "Same woman, hair in a loose bun, plain slightly wrinkled black t-shirt, on a simple apartment balcony on an overcast day, clothesline and a plastic chair behind her, neighbor buildings in the background, elbow on the railing. She is looking DOWN toward the LEFT side of the image, eyes clearly lowered, head tilted down, playful smile, as if watching a video below her." + bloco comum
- B3r-C: idem, "looking directly at the phone camera, relaxed smile" + bloco comum
Nomes: duda_base2r_sofa_real_W_cima_esquerda.jpg, duda_base2r_sofa_real_C_camera.jpg, duda_base3r_varanda_real_W_baixo_esquerda.jpg, duda_base3r_varanda_real_C_camera.jpg. Mostrar os 4 ao Allan e parar (sem clipe até o "pode").
Critério de aprovação: parece foto de celular de uma pessoa real; rosto = Duda; olhar certo. Se sair "bonito demais" de novo, 1 refino (2 créditos) acrescentando "amateur snapshot, not a professional photo".

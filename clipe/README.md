# Clipe do Pet (2º produto do Tutorial Pet) — ramo `clipe-do-pet`

Motor automático que monta um vídeo vertical 9:16 (até ~50 s) com as fotos/vídeos do cliente, legenda grande, carimbo Tutorial Pet e trilha livre de direitos (mix em -14 LUFS).

- `motor/montar_clipe.py`: o motor (ffmpeg + Pillow). Exemplo: `python3 clipe/motor/montar_clipe.py --molde homenagem --midias pasta --nome Thor --saida clipe.mp4 [--leve] [--musica arquivo.mp3]`
- `moldes/*.json`: homenagem, aniversario, retrospectiva, um_dia (cenas, textos, trilha). Novo tema = novo JSON, sem código.
- `pagina/`: página "Clipe do seu pet" (HTML único + vídeos de exemplo). É PRÉVIA (noindex, faixa de aviso).
- `exemplos/fotos/`: 15 quadros de clipes de banco gratuito (Pexels) usados nos exemplos.
- Tempo medido: versão leve (540x960) ~35 s; completa (1080x1920) ~3 min por clipe.

## Travas (12/11/2026)
Só arquivos novos, nenhum arquivo da Música do Pet, menu, estilo geral ou pagamento foi tocado. Nada vai para `main` sem aprovação do Allan.

## Falta para publicar (não feito de propósito)
1. Copiar `pagina/` para `site/build/clipe-do-pet/`, tirar o `noindex` e a faixa PRÉVIA, e incluir o link no menu (uma única alteração, depois que a sessão da música terminar).
2. Preço aprovado + checkout (Kiwify segue em espera) + recebimento dos arquivos + fila que roda o motor e entrega o link.
3. Ligar a Música do Pet do cliente como trilha (`--musica`).
4. Conferir as trilhas de cada molde de ouvido (escolhidas por andamento e volume, não ouvidas).

- Exemplos da página: gerados com 12 clipes de vídeo de banco gratuito (data/video_explicativo/clipes_pets, na ordem 01 a 12) como mídia de entrada, para mostrar movimento real; fotos paradas dão só zoom lento.

## 13/11/2026 — Vídeos do cliente + molde "diversão" (custo zero, sem GPU)
- A página aceita 2 a 8 mídias (até 6 fotos e 3 vídeos MP4/MOV de 20 MB). Vídeos ficam no KV (chave `clq:<id>:<n>`, limite do KV = 25 MiB por valor); R2 NÃO está ativado na conta (pede assinatura/cobrança: só com OK do Allan).
- `motor/escolher_trechos.py`: escolhe os melhores trechos de cada vídeo (movimento, áudio, exposição, sem corte seco; nunca repete trecho).
- `moldes/diversao.json`: cortes na batida (108,02 bpm, trilha lnplusmusic-happy-happy), fotos e vídeos intercalados, legenda a cada 2 cenas, `animar_fotos: false` (não gasta cota do Hugging Face).
- Rota nova: `functions/api/clipe/midia-video.js` (POST cliente / GET worker). Pedido ganhou `videos` e `ordem` (ex.: `fvfv`).
- Teste local ponta a ponta: `clipe_backend/teste/servidor_local.mjs` + `pagina_playwright.py BASE MOLDE midias...`.

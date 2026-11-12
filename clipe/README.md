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

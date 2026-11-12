# Aprendizados do Clipe do Pet (12/11/2026) — mover para a Apostila 15 e 07 Erros e lições na junção
- Qualquer proporção de foto funciona com fundo desfocado + foto inteira no centro; o zoom lento (Ken Burns) é feito com `scale ... eval=frame` + `crop`, mais leve que `zoompan`.
- Crossfade de 0,35 s por `xfade` encadeado; abertura e fechamento usam a 1ª mídia (efeito de moldura).
- Mix final: `loudnorm` sozinho deixou pico em -0,8 dBFS; com `alimiter=limit=0.89` fecha em -1,0 dBFS e -13,6 LUFS.
- Legendas curtas e genéricas (sem afirmar atividade) servem para qualquer foto do cliente; legenda que afirma ("soneca") destoa da foto.
- Tempo medido: leve 540x960 ~35 s; completo 1080x1920 ~3 min por clipe.
- Páginas de exemplo: quadros de vídeos de banco gratuito (Pexels) em data/video_explicativo/clipes_pets; Pexels e Pixabay não respondem do shell da nuvem (Pexels 404, Pixabay 403), só o git proxy.
- Trilhas escolhidas por andamento/volume (não ouvidas): homenagem=cubs-puppies-and-kittens (lenta), aniversario=lnplusmusic-happy-happy (forte), retrospectiva=starostin-pets-music, um_dia=velariomusic-happy-vibes. Conferir de ouvido.

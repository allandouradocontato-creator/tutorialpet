# Aprendizados do Clipe do Pet (12/11/2026) — mover para a Apostila 15 e 07 Erros e lições na junção
- Qualquer proporção de foto funciona com fundo desfocado + foto inteira no centro; o zoom lento (Ken Burns) é feito com `scale ... eval=frame` + `crop`, mais leve que `zoompan`.
- Crossfade de 0,35 s por `xfade` encadeado; abertura e fechamento usam a 1ª mídia (efeito de moldura).
- Mix final: `loudnorm` sozinho deixou pico em -0,8 dBFS; com `alimiter=limit=0.89` fecha em -1,0 dBFS e -13,6 LUFS.
- Legendas curtas e genéricas (sem afirmar atividade) servem para qualquer foto do cliente; legenda que afirma ("soneca") destoa da foto.
- Tempo medido: leve 540x960 ~35 s; completo 1080x1920 ~3 min por clipe.
- Páginas de exemplo: quadros de vídeos de banco gratuito (Pexels) em data/video_explicativo/clipes_pets; Pexels e Pixabay não respondem do shell da nuvem (Pexels 404, Pixabay 403), só o git proxy.
- Trilhas escolhidas por andamento/volume (não ouvidas): homenagem=cubs-puppies-and-kittens (lenta), aniversario=lnplusmusic-happy-happy (forte), retrospectiva=starostin-pets-music, um_dia=velariomusic-happy-vibes. Conferir de ouvido.

## 12/11/2026 — Foto animada (teste com ferramenta grátis)
- Wan 2.2 14B grátis na Upsampler (upsampler.com/free-video-generator-no-signup): sem cadastro, sem marca d'água; clipe de 2 a 5 s; FAQ do site diz que uso comercial é permitido (modelos Apache 2.0/LTX). Cota grátis diária em minutos de GPU, tamanho não informado.
- Dreamina/Seedance grátis: termo de uso proíbe uso comercial. Pika grátis: sem licença comercial (Starter US$ 10/mês tem). Kling/Runway/Vidu/Luma grátis: marca d'água e uso pessoal.
- Wan local no PC do Allan não roda: só vídeo integrado Intel UHD; a nuvem também não tem GPU.
- Método de teste: enviar a foto por print de tela (upload_image por arrastar-soltar) deixa tarjas pretas, cursor do mouse no quadro e resolução real de 270x480. Isso é artefato do teste; em produção o servidor deve enviar o arquivo da foto por API (ex.: Wan 2.2 em fal.ai, pago por clipe).
- Clipes de 2 s: tocar para frente e para trás (ping-pong) dá 4 s. Motor passou a aceitar 2 mídias (antes exigia 3) e a legenda ganhou faixa escura mais forte.
- O seletor de arquivos do Windows e o file_upload do Chrome não são alcançáveis pelo Claude; baixar pelo Chrome cai na raiz de Downloads (precisa de acesso liberado a essa pasta).

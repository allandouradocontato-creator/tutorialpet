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
- fal.ai (conta do Allan já logada, saldo US$ 0,00 em 12/11/2026): Wan 2.2 A14B imagem-para-vídeo, rótulo "Commercial use", US$ 0,08 por segundo em 720p (US$ 0,04 em 480p); clipe de 5 s ≈ US$ 0,40. Aceita foto como arquivo ou link e quadro final opcional. A página avisa que o modelo sai do ar em 04/01/2027 (migrar para H3 Max Image to Video ou similar), então o backend deve poder trocar de modelo.

## 12/11/2026 — Limites das rotas gratuitas de foto animada
- Upsampler (Wan 2.2): cota diária grátis acabou após ~2 clipes de 2 s no modelo 14B; o 5B também bloqueou ("try again tomorrow"). Reinicia no dia seguinte.
- Hugging Face ZeroGPU: Space zerogpu-aoti/wan2-2-fp8da-aoti = erro de execução ("No GPU available after 60s / ZeroGPU quota exceeded"); Space linoyts/wan2-2-i2v-rCM abre e aceita a foto (use a URL direta linoyts-wan2-2-i2v-rcm.hf.space, o iframe não aceita o arraste), mas retornou "Erro" 2x ao gerar (cota anônima/GPU).
- Conclusão: grátis serve para demonstração (2 clipes/dia), não para produção. Produção = pago por clipe (fal.ai Wan 2.2 ~US$0,40 por 5 s, licença comercial) ou Pika Starter US$10/mês.

## 12/11/2026 — Automação completa do clipe (foto animada) FUNCIONANDO ponta a ponta
- Rota 100% gratuita e automática: Space `linoyts/wan2-2-i2v-rCM` (Wan 2.2 14B) chamado por `gradio_client` COM `HF_TOKEN` da conta gratuita. Sem token a cota anônima por IP acaba na hora ("exceeded your ZeroGPU runs limit"); com token: ~46 s por foto, 480x832, 3,5 s, foto enviada como ARQUIVO (resolução cheia, sem cursor, sem barras pretas). A cota é por CONTA (música e clipe dividem).
- Fluxo: página → POST /api/clipe/pedido (convite AMIGOPET gasta 1 crédito do MESMO saldo `cv:<CODIGO>` da música; devolve se falhar) → fotos comprimidas no aparelho (JPEG, lado maior 1280) → /api/clipe/foto → /api/clipe/enviar → fila → worker `clipe/motor/processar_pedido.py` (GitHub Actions `clipe_worker.yml`, ~5 min ou na hora com GH_DISPATCH_TOKEN) anima cada foto (`animar_foto.py`: hf → fal → zoom) → motor → /api/clipe/video-upload → página mostra o vídeo (Range ok) e apaga as fotos.
- Teste real (servidor local + Chrome headless celular + Hugging Face real): 2 fotos, 116 s do clique ao vídeo; 2/2 animadas; MP4 leve de ~430 KB. Scripts: `clipe_backend/teste/` (servidor_local.mjs, cliente_simulado.py, pagina_playwright.py).
- Pegadinhas: KV do Cloudflare não tem `list` barato → fila usa `list({prefix:"clp:"})`; chaves do clipe `clp:/clf:/clv:` (a música usa `p:` e `cv:` para créditos); `job.result(timeout=300)` evita travar na fila da GPU grátis; no teste, o botão de rádio invisível cobre o rótulo (usar check(force=True)).
- Para ligar no ar: segredos do GitHub `HF_TOKEN` (+ `MUSICA_TICK_SECRET` já usado pela música); workflow precisa estar na main; página copiada para site/build/clipe-do-pet/.

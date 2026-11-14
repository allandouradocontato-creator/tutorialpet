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

## Publicado na main (12/11/2026)
- Commit 92d2df2: pagina em /clipe-do-pet/ (200), atalho /amigoclipe -> convite AMIGOPET, /api/clipe/* no ar (fila responde 401 sem segredo).
- Falta confirmar o segredo MUSICA_TICK_SECRET (GitHub) = TICK_SECRET (Cloudflare); sem ele o worker nao processa. Cota ZeroGPU e compartilhada com a musica.
- 12/11/2026 20:55: segredos criados pelo Chrome do Allan (com OK dele): Cloudflare Pages TICK_SECRET (segredo, producao) e GitHub MUSICA_TICK_SECRET, mesmo valor. A sessao da musica NAO deve recriar com outro valor. Cloudflare so aplica na proxima publicacao (este commit dispara). So testar com credito depois de Deployments = Success.
- 12/11/2026 LICAO: o Cloudflare devolve 403 para o User-Agent padrao do Python (urllib) em tutorialpet.com.br; curl passa. Todo cliente Python que chama a API do site (worker, testes) precisa mandar user-agent proprio. O step de curl do workflow mostrava "pedidos na fila: 1" mas o python dava 403: conferir o log do step, nao so o status verde.

## 13/11/2026 — Causa real do animadas=0 (confirmada no log, run 43337570399 do clipe_worker.yml)
- O passo Processar pedidos mostrou: `hf: falhou (AppError: You have exceeded your free ZeroGPU quota (68s requested vs. 64s left))` nas 2 tentativas; o fal não rodou (FAL_KEY vazio) e o motor caiu no zoom. Não era bug do worker: era a cota diária do Hugging Face.
- Cada foto animada pede ~68 s de ZeroGPU; a conta grátis rende só ~3 animações por dia e a cota é DIVIDIDA com a música. Teste da música (19:20) e teste do clipe (22:00) no mesmo dia competem pela mesma cota.
- Logo após a falha o log mostrava "Try again in 21:23" (renovação perto de 18:55 em Fortaleza).
- 13/11/2026 (Allan): EDICAO AUTOMATICA DE VIDEO (servico novo, alem do Clipe do Pet): cliente manda fotos e videos, escolhe um estilo (diversao, UGC, documentario) e recebe pronto. Decisao: (1) provar DENTRO do Clipe do Pet: aceitar videos do cliente + molde "diversao", teste no link AMIGOPET, custo zero; (2) em paralelo pesquisar na Biblioteca de Anuncios quem ja vende edicao automatica (mesmo anuncio no ar ha 2-3 meses+). So vira produto separado se houver referencia validada. Pendencias tecnicas: armazenamento de video (R2), escolha de trechos (cena/movimento/volume/transcricao), worker em repo privado antes de cliente pagante (logs publicos). Execucao em Sonnet.

## 13/11/2026 — Vídeo do cliente + molde diversão (Frente A, teste real OK: pedido fh9zezand8q7)
- Fluxo em produção: 2 fotos + 2 vídeos, molde diversao, convite AMIGOPET (créditos 3 → 2), entregue em ~2 min (worker disparado pela API REST `POST /actions/workflows/clipe_worker.yml/dispatches`; `gh workflow run` não funciona nesta sessão, usa GraphQL). Log do passo conferido: "motor: plano:…" e "entregue (1577 KB, 0/2 animadas, 2 vídeo(s))". Zero GPU/HF.
- R2 NÃO está ativado na conta do Cloudflare (a tela pede "Adicionar assinatura do R2", que mexe em cobrança; só com OK do Allan). Vídeos do cliente vão no KV: limite 25 MiB por valor → 20 MB por vídeo, 3 vídeos, 2 a 8 mídias; chaves `clq:<id>:<n>` (vídeo do cliente) e `clv:<id>` (clipe entregue); fotos e vídeos do cliente apagados na entrega.
- Melhores trechos (`clipe/motor/escolher_trechos.py`): janela de 0,25 em 0,25 s com nota = movimento moderado + volume do áudio + contraste + exposição − corte seco; pega as K melhores sem sobreposição; ~1 s por vídeo, só ffmpeg + numpy (numpy entrou no pip do workflow).
- Corte na batida: BPM e fase medidos por fluxo espectral + autocorrelação (lnplusmusic-happy-happy = 108,02 bpm, 1ª batida em 0,279 s, a mais clara entre 7 faixas). Cada cena dura N batidas + a transição (xfade 0,1 s) e a trilha começa meia transição antes da 1ª batida. Conferido no ARQUIVO FINAL: batida a 0,058 s do esperado (0,05).
- Foto animada vira `NN_anim.mp4` e entra inteira; vídeo do cliente (`NN.mp4`) passa pelo seletor. Molde com `"animar_fotos": false` não gasta GPU.
- ERRO ANTIGO ACHADO: o AAC estourava o pico (+2,0 a +2,3 dBFS no arquivo final, nos 5 moldes), embora o `alimiter` desse -1 dB antes do AAC (a medição "-1,0 dBFS" de 12/11 foi antes de codificar). Correção: o motor mede o pico real do arquivo (ebur128) e baixa o teto do limiter até ficar ≤ -1 dBFS. Custo: loudness ~-15,3 LUFS em vez de -14. Regra: medir pico/LUFS SEMPRE no arquivo final.
- Este teste não tocou na cota do HF (teste do clipe animado 19:05, música 19:20).
- 13/11/2026 (Frente B): Biblioteca de Anúncios — referência longeva só para 'foto → vídeo de homenagem' (Studio Alma, 15+ anúncios, até 105 dias, venda por WhatsApp). Edição automática estilo UGC/diversão: sem anúncio longevo, não vira produto separado ainda. Detalhes: data/garimpo/edicao_automatica_referencias_2026-11-13.md
- 13/11/2026 22:30: segundo teste em producao (pedido 8kvgpfquwfc4) tambem animadas=0. Causa CONFIRMADA rodando o animador com o HF_TOKEN: "You have exceeded your ZeroGPU runs limit" (AppError). A conta gratis do HF nao sustenta musica + clipe no mesmo dia; o worker cai no zoom (fallback). Fluxo todo (pedido, fila, worker, entrega, video leve) funciona; so falta capacidade de GPU. AMIGOPET: creditosRestantes 0 depois deste teste.

## Magic Hour (13/11)
- Provedor gratuito integrado: `via_magichour` em `animar_foto.py` (Wan 2.2, 480p, secret `MAGICHOUR_API_KEY`, pacote `magic-hour`). Cadeia padrão: hf → magichour → fal.
- Teste isolado: 3 s, 480x848, funcionou, mas levou ~11 min (fila do plano grátis). Timeout do provedor: 420 s, então em hora de fila pode cair no fallback (zoom lento). Ainda falta confirmar em produção com `animadas: 2`.
- Saldo do convite fica na chave KV `cv:AMIGOPET` (a variável CONVITES_TESTE só dá o valor inicial); para repor, editar a chave no KV.
- 13/11 noite: dois erros da integração Magic Hour achados no log do worker: (1) `create` exige foto já enviada (`c.v1.files.upload_file`), caminho local dá 422; (2) wan-2.2 só aceita segundos inteiros (3,4,5...), 3.5 dá 422. Corrigidos. Molde `diversao` não anima de propósito (zero GPU), então teste de animação tem que usar `homenagem`.
- Fotos agora animam em paralelo (até 3) e o Magic Hour espera até 20 min.
- Saldo AMIGOPET reposto para 10 (KV `cv:AMIGOPET`), 2 testes gastaram 2 créditos.
- 14/11 00:01: TESTE OK EM PRODUÇÃO: pedido homenagem, 2 fotos, `animadas: 2` via Magic Hour (Wan 2.2), ~4 min do worker, vídeo 540x960 8,5 s. Fluxo grátis completo validado.
- Achado: `/api/clipe/enviar` devolveu 400 logo depois do upload das fotos (KV com leitura atrasada); repetir após alguns segundos funciona. O status também pisca "recebendo". Pendente: a página do cliente deve repetir o "enviar" 2-3 vezes antes de mostrar erro. Também: nunca cortar a saída do cliente_simulado com `head` (mata o envio e deixa o pedido preso em "recebendo", gastando crédito).

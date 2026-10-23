# Guia: ferramentas GRATUITAS / open source de mídia (Tutorial Pet)
Criado em 22/10/2026. Só pesquisa: nenhuma conta criada, nenhuma chave digitada, nenhum binário baixado. Bancos de fotos (Pexels, Pixabay, Unsplash, Wikimedia, Openverse, Flickr) estão em `guia_fontes_imagens.md` e não se repetem aqui.

**Legenda de confiança:** [OFICIAL] = li a página oficial do projeto/serviço hoje. [TERC] = fonte terciária (blog, comparador, fork do GitHub); conferir antes de depender. [MEM] = memória/conhecimento prévio, não verificado hoje. [BLOQ] = página oficial bloqueada pela allowlist da sessão (só consegui abrir páginas que apareceram em buscas). Limite que não achei = "não confirmado"; nada foi inventado.

**Regra de ouro que pesa em tudo:** nosso uso é COMERCIAL (e-books vendidos, redes monetizadas, anúncios). Licença "não comercial" (NC) elimina a ferramenta, mesmo que seja grátis e boa.

**Nuvem x PC:** o GitHub Actions grátis NÃO tem GPU (GPU só em "larger runners", planos Team/Enterprise [OFICIAL]). Logo, qualquer modelo pesado (difusão, vídeo IA, TTS de GPU) só roda na nuvem via API/serviço de terceiros. Sem GPU, só rodam bem: ffmpeg, MoviePy, HyperFrames, Remotion, Kokoro/Piper (leves, CPU).

---
## Frente 1. Geração de imagens
| Ferramenta | Licença / comercial | Limite grátis | Chave/conta (Allan) | Nuvem sem PC? | Nota pet | Nota uso | Confiança |
|---|---|---|---|---|---|---|---|
| **Cloudflare Workers AI** (FLUX.1 schnell, SDXL etc.) developers.cloudflare.com/workers-ai | Modelo schnell Apache 2.0; termos do serviço Cloudflare | 10.000 Neurons/dia grátis; schnell ~4,8 neurons por tile 512x512 + 9,6 por passo [OFICIAL] (dá dezenas de imagens/dia; cálculo exato por imagem não confirmado) | Conta Cloudflare + API token (Allan cria) | SIM (API HTTP, roda no Actions) | 7 | **8** | OFICIAL (preço); qualidade [MEM] |
| **FLUX.1 [schnell]** (pesos, Black Forest Labs) huggingface.co/black-forest-labs/FLUX.1-schnell | Apache 2.0, comercial ok [TERC licenseorg]; página HF [BLOQ] | Sem limite (roda local) | Nenhuma | NÃO no Actions (precisa GPU) | 8 | 6 (só se houver GPU) | TERC |
| **FLUX.2 [klein] 4B** | Comercial ok segundo [TERC]; termos oficiais não lidos | Pago por API (~US$0,002/img) [TERC]; pesos locais não confirmei | - | - | 8 | 4 | TERC, não confirmado |
| **Stable Diffusion XL** (pesos) | CreativeML Open RAIL-M, comercial ok, sem teto de receita [TERC terms.law] | Sem limite (local) | Nenhuma | NÃO sem GPU | 7 | 5 | TERC |
| **Stable Diffusion 3.5** | Community License: grátis comercial se receita < US$1 mi/ano [TERC] | Local | Nenhuma | NÃO | 8 | 5 (dentro do teto, mas redundante com FLUX) | TERC |
| **Hugging Face Inference Providers** huggingface.co/docs/inference-providers | Depende do provedor | Conta grátis: SEM crédito mensal; PRO US$2/mês [OFICIAL]. Outro blog diz US$0,10/mês grátis (divergente) | Token HF | SIM | - | **2** (não é grátis de fato; o schnell foi removido do hf-inference em jul/2026 [TERC fórum]) | OFICIAL |
| **Hugging Face ZeroGPU Spaces** (uso manual de Spaces de FLUX) | Varia por Space | ~5 min de GPU/dia grátis [TERC] | Conta HF | NÃO (uso manual) | 7 | 3 | TERC |
| **Pollinations.ai** | Licença/uso comercial NÃO confirmados | Sem chave: 1 req a cada 15 s, pode ter marca d'água; endpoint novo exige chave `sk_/pk_` [TERC] | Conta (Allan) para tirar marca d'água | SIM | 6 | 5 (instável, sem SLA) | TERC |
| **Leonardo.ai** (app) | Comercial ok no grátis, mas imagens ficam públicas [TERC] | ~150 tokens/dia [TERC] | Conta | NÃO (uso manual) | 8 | 6 | TERC |
| **Ideogram** | Comercial: texto e tabela do blog se contradizem; conferir | ~10 créditos lentos/semana, imagens públicas [TERC] | Conta | NÃO | 7 | 3 | TERC |
| **Bing Image Creator / Playground / Freepik gerador** | Comercial ok segundo [TERC] | 15/dia (Bing), 20/dia (Freepik), Playground 10 downloads/dia [TERC] | Conta | NÃO | 7 | 4 (manual) | TERC |
| **Gemini API / Imagen / Nano Banana** | - | **Sem cota grátis para imagem** (429 "limit: 0"); só pago [TERC yingtu, 30/09/2026; página Google [BLOQ]] | - | - | - | **1** | TERC |

**Top 2 (testar nesta ordem):** 1) **Cloudflare Workers AI com FLUX.1 schnell** (única opção grátis com API que roda sem PC e licença limpa). 2) **Leonardo.ai manual** para capas/arte especial que exijam qualidade maior (Allan ou Claude no Chrome dele; imagens públicas, então nada sensível).
**Atenção:** imagens 100% IA provavelmente não têm direito autoral próprio (EUA) [TERC]. Para raça específica, conferir a imagem antes de usar (regra da casa).

---
## Frente 2. Criação/edição de vídeo
| Ferramenta | Licença / comercial | Limite grátis | Chave/conta | Nuvem sem PC? | Nota pet | Nota uso | Confiança |
|---|---|---|---|---|---|---|---|
| **FFmpeg** ffmpeg.org (já usado em `agents/17_video`) | LGPL/GPL conforme build; uso comercial livre | Sem limite | Nenhuma | SIM (Actions Ubuntu) | - | **9** | MEM (e uso real no repo) |
| **HyperFrames** (HeyGen) github.com/heygen-com/hyperframes | Apache 2.0, sem taxa por render nem teto comercial [OFICIAL] | Sem limite; precisa Node 22+, FFmpeg, Chrome headless; saída determinística, pensado para CI [OFICIAL] | Nenhuma | SIM em teoria (Actions tem Chrome/Node; sem exemplo oficial de CI) | - | **8** (legendas animadas, cards, carimbo patinha+marca em HTML/CSS) | OFICIAL |
| **MoviePy** github.com/Zulko/moviepy | MIT [MEM]; página [BLOQ] | Sem limite | Nenhuma | SIM | - | 7 (Python, simples; mais lento que ffmpeg puro) | MEM |
| **Remotion** remotion.dev | Grátis para indivíduo, equipe até 3 pessoas, ONG; empresa maior paga US$25/mês por dev ou US$0,01/render (mín. US$100/mês) [OFICIAL FAQ]. Dourado Falcão (equipe pequena) se encaixa no grátis; reconferir se a equipe crescer | Sem limite | Nenhuma | SIM (Node+Chrome) | - | 6 (redundante com HyperFrames, licença com condição) | OFICIAL |
| **Shotcut / Kdenlive / OpenShot** | GPL, comercial ok [MEM] | Sem limite | Nenhuma | NÃO (editores com tela) | - | 3 (só revisão manual) | MEM |
| **Wan 2.2** (vídeo IA, Alibaba) | Apache 2.0, sem direitos sobre a saída [TERC] | Local; 5B pede ~24 GB de VRAM [TERC] | Nenhuma | NÃO (GPU) | 6 | 3 | TERC |
| **LTX-2.3** (Lightricks) | LTX-2 Community: grátis comercial abaixo de US$10 mi/ano de receita [TERC] | Local; roda em RTX 5090 [TERC] | Nenhuma | NÃO (GPU) | 6 | 3 | TERC |
| **Pika (plano grátis)** | Cartão grátis lista uso comercial e sem marca d'água [TERC dreamina]; termos oficiais não lidos | 80 créditos/mês [TERC] | Conta | NÃO (manual) | 6 | 5 | TERC, conferir |
| **PixVerse / Krea / Dreamina** | Comercial no grátis NÃO garantido [TERC] | 60/dia (PixVerse), 100 unid./dia (Krea), diário (Dreamina) [TERC] | Conta | NÃO (manual) | 6 | 4 (só para testar, não monetizar sem ler termos) | TERC |
| **Runway / Hailuo / Luma / Kling** | Grátis: marca d'água e/ou só não comercial [TERC] | Créditos únicos ou promocionais | Conta | NÃO | - | 1 (não servem para monetizar) | TERC |
| **Pexels Videos / Pixabay vídeos** (já na `fontes_midia.yaml`) | ver guia de imagens | mesma chave | já têm | SIM | 8 | 9 (base real do pipeline) | ver guia |

**Top 2:** 1) **FFmpeg + HyperFrames** (montagem determinística na nuvem: clipe de banco, narração, legenda, carimbo). HyperFrames é o ganho novo: dá para criar identidade visual em HTML sem editor. 2) **Pika grátis manual** só para 3-5 clipes de teste "pet fofo" (verificar termos antes de postar). Vídeo IA open source (Wan/LTX) fica na lista "depois", precisa GPU paga.
Nota: o MCP "HyperFrames by HeyGen" é outro caminho (projeto hospedado na conta HeyGen, fila de render na nuvem deles); no Claude Code vale a biblioteca local, não o MCP.

---
## Frente 3. Clones / avatares / lip sync
| Ferramenta | Licença / comercial | Limite grátis | Chave/conta | Nuvem sem PC? | Nota pet | Nota uso | Confiança |
|---|---|---|---|---|---|---|---|
| **HeyGen (plano grátis)** heygen.com — Duda já é avatar aqui | Grátis tem marca d'água; comercial no grátis não confirmado [TERC, blog da própria HeyGen] | 1-3 vídeos/mês, 1 Digital Twin de 15 s [TERC] | Conta do Allan (já existe) | SIM (API/MCP) mas créditos são o gargalo | 8 | 6 (grátis não serve para publicar; plano pago é decisão de "comprar depois") | TERC |
| **D-ID** | Trial; planos pagos [TERC argil] | Não confirmado | Conta | SIM | 6 | 3 | TERC |
| **SadTalker** | README: "somente uso pessoal/pesquisa/não comercial" [TERC fork camenduru] | Local | Nenhuma | NÃO (GPU) | 6 | **1** (NC) | TERC |
| **Wav2Lip** | "Somente pessoal/pesquisa/não comercial"; comercial só falando com os autores (Sync Labs) [TERC fork] | Local | Nenhuma | NÃO | 5 | **1** (NC) | TERC |
| **LivePortrait** | Código/pesos MIT, MAS depende de InsightFace `buffalo_l` que "não pode ser usado comercialmente" [TERC Replicate] | Local | Nenhuma | NÃO (GPU) | 7 (animar foto de pet/ mascote) | 2 (risco de licença) | TERC |
| **Sync Labs (API do Wav2Lip comercial)** | Pago | Não confirmado | - | SIM | - | "comprar depois" | TERC |

**Top 2:** 1) **Manter a Duda no HeyGen** (já existe, voz Marianne/ElevenLabs) e usar poucos vídeos de avatar com cuidado de crédito; decidir plano pago só com sistema fechado. 2) **Evitar avatar falante: usar o pet/mascote em animação de texto (HyperFrames) + narração**. Os open source clássicos (SadTalker, Wav2Lip, LivePortrait) estão praticamente todos bloqueados para uso comercial; não usar.

---
## Frente 4. Voz / áudio / TTS (pt-BR)
| Ferramenta | Licença / comercial | Limite grátis | Chave/conta | Nuvem sem PC? | Qualidade pt-BR | Nota uso | Confiança |
|---|---|---|---|---|---|---|---|
| **ElevenLabs Starter** (Allan JÁ ASSINA; Duda = voz Marianne) | Starter inclui licença comercial, só para áudio gerado com assinatura ativa [TERC dupple] | 30.000 créditos/mês (~30 min) [TERC]; preço US$6/mês [TERC] | Chave do Allan (já tem) | SIM | 9 | **9** (voz oficial da marca; economizar créditos: roteiro até 420 caracteres) | TERC (assinatura: MEM do Allan) |
| **ElevenLabs plano Free** | **Proíbe uso comercial**; exige crédito "elevenlabs.io" no título; 10.000 créditos/mês [TERC] | 10k créditos | - | - | 9 | 0 (não usar para publicar) | TERC |
| **Kokoro TTS** (82M) pypi.org/project/kokoro | Apache 2.0 (código) [OFICIAL PyPI]; pesos Apache 2.0 [MEM] | Local, sem limite; Python 3.10-3.12; pt-BR código `p` com vozes pf_dora, pm_alex, pm_santa [OFICIAL PyPI/TERC] | Nenhuma | SIM (leve, CPU; precisa espeak-ng; velocidade em CPU não confirmada) | 6-7 [MEM, não ouvi hoje] | **8** (voz reserva grátis e comercial) | OFICIAL + MEM |
| **Piper** (rhasspy → Open Home Foundation) | Binário atual GPL-3.0 [TERC]; repositório de vozes `rhasspy/piper-voices` marcado MIT [OFICIAL HF]; vozes pt-BR: **edresson** e **faber** [OFICIAL HF]; licença do dataset de cada voz NÃO confirmada | Local, sem limite | Nenhuma | SIM (CPU, rápido) | 5-6 [MEM] | 6 (checar licença do dataset antes de monetizar; GPL do programa só pesa se distribuirmos o programa) | HF OFICIAL; resto TERC/MEM |
| **Coqui XTTS-v2** (clone de voz) | **CPML: somente não comercial**; Coqui encerrou serviços em dez/2023, sem rota de licença comercial [TERC] | Local | Nenhuma | NÃO (GPU) | 7 | **1** (NC) | TERC |
| **Edge TTS** (`pip install edge-tts`, já usado em `montar_video6.py`) | Biblioteca GPL-3.0 [MEM]; usa o serviço de leitura em voz alta do Edge, sem licença comercial pública; Microsoft diz que uso comercial sem assinatura Azure pode violar os termos [TERC, moderador MS, não vinculante] | Sem limite oficial | Nenhuma | SIM | 7 (pt-BR-FranciscaNeural etc. [MEM]) | 4 para PUBLICAR/monetizar (risco jurídico); 8 só para teste/rascunho | TERC |
| **Azure AI Speech (oficial)** | Licença comercial, camada grátis existe | Não confirmado hoje | Conta Azure | SIM | 8 | "avaliar" (alternativa legal ao Edge TTS) | MEM, não confirmado |

**Top 2:** 1) **ElevenLabs Starter** (já pago, comercial; é a voz da Duda). 2) **Kokoro** como reserva grátis para volume (roteiros de artigo em áudio, testes, quando acabar crédito). **Alerta de processo:** o pipeline já usa Edge TTS; para vídeo monetizado trocar por ElevenLabs ou Kokoro, ou aceitar o risco explicitamente (decisão do Allan, não minha).

---
## Frente 5. Música e efeitos
| Ferramenta | Licença / comercial | Limite grátis | Chave/conta | Nuvem sem PC? | Nota pet | Nota uso | Confiança |
|---|---|---|---|---|---|---|---|
| **Pixabay Music** pixabay.com/music | Comercial em vídeos/redes, sem atribuição [TERC Thematic]; risco de reivindicação Content ID, sem verificação prévia e disputas manuais [TERC] | Sem limite; sem API de música conhecida | Nenhuma (Allan baixa; Claude pode pelo Chrome dele) | SIM depois de baixado e commitado | - | **8** | TERC |
| **YouTube Audio Library** | Seguro só dentro do YouTube; fora (TikTok/IG/FB) não coberto; faixas CC pedem crédito [TERC foximusic] | Sem limite | Conta Google | Manual | - | 4 (nosso foco é FB/IG/TikTok) | TERC |
| **Free Music Archive** freemusicarchive.org | Por faixa: CC0/CC BY/CC BY-SA/CC BY-ND ok comercial; qualquer NC e "FMA-Limited" NÃO [OFICIAL FAQ]. Crédito: título, autor, fonte, licença [OFICIAL] | Sem limite; FAQ não cita API | Nenhuma | Manual | - | 6 (só filtro CC0/BY) | OFICIAL |
| **Freesound** (efeitos) freesound.org | Licença por som (usar só CC0, regra da casa); API: limites podem mudar; uso comercial da API é negociado caso a caso com a UPF; chave é propriedade deles [OFICIAL TOS API] | Número de chamadas não confirmado | Conta + chave (Allan cria) | SIM | - | 6 (efeitos pontuais; baixar poucos, nada de cópia do banco) | OFICIAL |
| **Mixkit** (música/efeitos) | Mixkit License comercial [MEM, já na yaml como "conferir"] | Sem limite | Nenhuma | Manual | - | 6 | MEM |
| **ACE-Step 1.5** (gera música, com vocal) | MIT, saída comercial ok segundo o cartão do modelo [TERC creativeainews]; roda em <4 GB VRAM [TERC] | Local | Nenhuma | NÃO no Actions (GPU) | - | 5 (bom para o futuro, exige GPU/hosting) | TERC |
| **YuE / DiffRhythm** | Apache 2.0 [TERC] | Local | Nenhuma | NÃO | - | 3 | TERC |
| **Stable Audio Open** | Comunitária: grátis até US$1 mi/ano e exige registro na Stability [TERC] | Local | Registro | NÃO | - | 3 | TERC |
| **MusicGen (Meta)** | Pesos CC BY-NC 4.0: **NÃO comercial** [TERC] | - | - | - | - | **0** | TERC |
| **Suno grátis** | Grátis = só pessoal/não comercial, **sem vídeo monetizado**; comercial só em Pro/Premier [TERC dubspot] | Créditos diários (valor não confirmado) | Conta | Manual | - | 1 no grátis | TERC |
| **Udio** | Após acordo com a UMG (out/2025) virou "jardim fechado", exportar ficou difícil [TERC] | Não confirmado | Conta | - | - | 2 | TERC |

**Top 2:** 1) **Pixabay Music** (3 a 6 faixas instrumentais animadas baixadas uma vez, commitadas em `data/social/musica/`, guardando URL e data de cada download como prova de licença; custo zero e sem API). 2) **Freesound CC0** para efeitos (patinha, "plim") ou **Mixkit** como segunda fonte de faixas. Suno/Udio/MusicGen fora até haver plano comercial pago e decisão do Allan.
**Risco real:** Content ID pode reivindicar faixa de banco livre depois da postagem; guardar o comprovante e preferir variar faixas.

---
## Frente 6. Ilustração, ícones, vetores e "gerador de pets"
Fotos já cobertas. Aqui só o que falta.
| Ferramenta | Licença / comercial | Limite | Chave/conta | Nuvem sem PC? | Nota uso | Confiança |
|---|---|---|---|---|---|---|
| **unDraw** undraw.co | Uso livre, inclusive comercial, sem atribuição; proibido compilar para serviço concorrente ou distribuir em pacotes [TERC licenseorg/bloggingwizard]; estilo corporativo, pouco pet | Sem limite, sem API oficial confirmada | Nenhuma | Manual | 5 | TERC |
| **DrawKit / IRA Design / Delesign / ManyPixels** | Comercial sem atribuição (MIT em DrawKit e IRA) [TERC bloggingwizard] | Sem limite | Nenhuma | Manual | 6 (variedade para landing/e-book) | TERC |
| **SVG Repo** | "Livre para comercial" segundo [TERC]; licença varia por ícone, conferir | Sem limite | Nenhuma | Manual | 5 | TERC |
| **Lucide / Phosphor / Bootstrap Icons** (ícones de seguir, setas, patinha) | MIT / MIT / MIT [MEM, não conferi hoje] | Sem limite; pacote npm/ SVG | Nenhuma | SIM (arquivo no repo) | **8** (ícones de seguir clicáveis e UI do site) | MEM |
| **Openclipart** | Domínio público (CC0) [MEM; site não conferido] | Sem limite | Nenhuma | Manual | 5 (clipart antigo) | MEM |
| **Freepik / Ouch! / Absurd / Vector4Free** | Exigem link de atribuição no plano grátis [TERC] | - | - | - | 2 (evitar) | TERC |
| **Gerador de pets** | Não existe ferramenta "especial para pets" confirmada. Usar os geradores da Frente 1 com prompts por raça (Cloudflare FLUX schnell, Leonardo). Para sticker/mascote consistente, definir 1 prompt-base da Duda/mascote e variar | - | - | - | - | - |

**Top 2:** 1) **Lucide/Phosphor** para ícones (grátis, no repo, sem depender de site). 2) **DrawKit ou IRA Design** para ilustrações vetoriais de apoio no e-book/landing. Conferir a licença no dia de baixar e guardar o link.

---
## Resumo geral: notas e ordem de teste
| Ordem | Teste | Frente | Por quê |
|---|---|---|---|
| 1 | **FFmpeg + HyperFrames** gerando 1 vídeo curto 9:16 com legenda animada e carimbo patinha+marca, na nuvem | 2 | Zero custo, zero conta, ligado ao que já existe |
| 2 | **Kokoro pt-BR** (pf_dora) lendo 1 roteiro, comparar com ElevenLabs Marianne | 4 | Reserva grátis comercial; sem conta |
| 3 | **Pixabay Music**: escolher 3 faixas, commitar com prova de licença | 5 | Resolve a pendência "música" da `fontes_midia.yaml` (único passo manual) |
| 4 | **Cloudflare Workers AI / FLUX.1 schnell**: 10 imagens de raças, medir neurons/imagem | 1 | Descobre o custo real por imagem no limite diário |
| 5 | **Lucide/Phosphor** ícones de seguir | 6 | Rápido, sem risco |
| 6 | **Pika grátis** 3 clipes (manual) | 2 | Só se o banco de vídeo não bastar; ler termos primeiro |
| 7 | **Freesound CC0** efeitos | 5 | Opcional |
| 8 | Avaliar troca do **Edge TTS** (risco de termos) | 4 | Antes de escalar vídeos monetizados |

Tudo que for GPU (Wan, LTX, ACE-Step, FLUX local, SDXL local) vai para a lista "comprar depois/alugar GPU", só com o sistema fechado.

## Quem faz o quê
**Claude faz sozinho:** integrar FFmpeg/HyperFrames/MoviePy no pipeline; testar Kokoro/Piper (instalar pacote do PyPI oficial, sem baixar binário de origem estranha); escrever o módulo Cloudflare/Freesound/Lucide; registrar licença e crédito por ativo; gerar a página de créditos; testar com a chave depois de existir, sem imprimir a chave; ler termos oficiais no Chrome do Allan quando a página estiver bloqueada aqui; baixar as faixas do Pixabay Music pelo Chrome já logado do Allan (se ele autorizar a pasta).
**Só o Allan faz:** criar conta Cloudflare e o API token (Workers AI); criar conta/chave Freesound (se for usar); guardar as chaves nos segredos do GitHub (Chrome normal, não o painel lateral); decidir plano pago HeyGen e se aceita o risco do Edge TTS; autorizar qualquer pagamento. Nada disso foi feito.

## O que NÃO foi confirmado (resumo)
Páginas oficiais bloqueadas: Hugging Face (FLUX schnell), Google Gemini pricing, MoviePy, Remotion `/license`, Pixabay Music, YouTube Audio Library, HeyGen/D-ID preços, Piper (repo), Stability, Black Forest Labs. Não confirmado em lugar nenhum: neurons exatos por imagem no Workers AI, qualidade do pt-BR no Kokoro/Piper (não ouvi), licença do dataset das vozes Piper, limite de chamadas do Freesound, termos oficiais do Pika/Pollinations/Ideogram, plano grátis do Azure Speech, licenças de Lucide/Phosphor/Openclipart/Mixkit (memória).

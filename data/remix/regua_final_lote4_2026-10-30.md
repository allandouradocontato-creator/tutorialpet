# Régua final — lote 4 de reacts (Fable, 30/10/2026 09h30). Duas vertentes, 3 reacts cada
Substitui a v4 (`criterios_curadoria_v4_2026-10-30.md`) só no que diverge; o resto da v4 continua valendo. Motivo: lotes 2 e 3 reprovados pelo Allan (onda pequena, vídeos curtos, sem contexto/história). Regras de ouro 40-43.

## Vertente A — HUMOR VIRAL (carona em onda grande)
### Pré-requisitos (eliminam, não pontuam; qualquer "n/d" = fora)
1. Views ≥ 1.000.000 (medidas pelo script; nada de "parece viral").
2. Publicado há ≤ 7 dias (data vem do ID do link / yt-dlp).
3. Duração 20-45 s no original, OU corte contínuo de 20-45 s que tenha sozinho começo, virada e fim.
4. HISTÓRIA visível SEM áudio na folha de quadros: (a) começo/situação, (b) virada (flagra, susto, resposta, antes/depois, inversão), (c) fim/consequência. Compilação, loop de 1 gag, slideshow, só legenda = fora.
5. Pet doméstico (cachorro/gato; outro só se fofo e doméstico). Sem animal doente/abrigo/briga/perigo, sem criança/farda/pessoa constrangida em foco, sem marca d'água de app ou página (Pubity, "P", logos). Crédito possível (@ do criador).
6. Conferir `biblioteca/clipes_banidos.md`. Ignorar links do perfil do Allan (@7253864878207861766).
7. Vídeo de fora do Brasil entra se o humor for visual (texto queimado em inglês/espanhol não pode ser essencial para a piada).

### Pontuação (100). Entra com ≥ 80 (= nível do n03 v2, que daria 83 nesta régua)
Parte numérica (55, automática `scripts/curadoria_tiktok.py` + conversão abaixo)
| Critério | Regra | Pts |
|---|---|---|
| Momentum absoluto | ≥ 3 mi = 20; ≥ 2 mi = 15; ≥ 1 mi = 10 | 20 |
| Compartilhamento | compart ÷ views ≥ 3 % = 15; ≥ 1,5 % = 10; ≥ 0,8 % = 5 | 15 |
| Frescor | ≤ 3 d = 10; ≤ 7 d = 6 | 10 |
| Curtidas | ≥ 10 % = 5; ≥ 5 % = 3 | 5 |
| Bônus criador pequeno estourando | views ÷ mediana da conta ≥ 20x = +5 | +5 |

Parte de conteúdo (50, só quem ASSISTIU com áudio e leu os 10 comentários mais curtidos)
| Critério | Regra | Pts |
|---|---|---|
| História completa | começo + virada + fim claros; a virada acontece entre 5 s e 30 s | 15 |
| O que a Duda acrescenta | educativo (porquê ou 1 dica de tutora) / ilustrativo ("olha isso", compara, aponta) / engraçado (piada da cena ou voz do pet): 2 de 3 = 15; **3 de 3 = 25**; 1 = 0 e o vídeo cai | 25 |
| Voz do público | top 10 comentários já entregam a piada/pergunta e um CTA "e o seu…?" cabe natural | 10 |

Decisão: ≥ 80 entra; 65-79 reserva; < 65 fora. Lote mínimo: 12 candidatos com a parte numérica ≥ 35/55 antes de baixar. Entre dois empatados, ganha o mais fresco; nunca o "mais seguro".

## Vertente B — PRODUTO (afiliados Shopee, `data/produtos/afiliados_shopee.md`)
Prioridade (ordem do Allan): 1 educador de xixi / sanitário "xixi sim-xixi não" (16 %), 2 dedeira dental + gel (15 %), 3 comedouro lento anti-gula (14 %), 4 tapete de lamber (14 %), 5 encaixe de cinto para carro (14 %), 6 escada pet 3 degraus (14 %). Escolher 3 produtos DIFERENTES (1 vídeo por produto), seguindo essa ordem quando a pontuação empatar.

### Pré-requisitos (eliminam)
1. Produto igual ou equivalente ao da lista, VISÍVEL EM USO pelo pet, com o problema RESOLVIDO NA TELA (xixi no lugar, come devagar, dente escovado, lambe calmo, preso no carro, sobe na cama).
2. Entre os 10 comentários mais curtidos há pelo menos 1 "onde compro?", "qual o nome?", "link?", "funciona?".
3. Views ≥ 100.000; publicado há ≤ 30 dias (aqui não é carona em onda, é prova social; ≤ 7 d pontua mais).
4. Duração: corte de 15-30 s que mostre antes → uso → resultado. Sem marca d'água de loja/app; sem promessa de saúde; sem criador vendendo concorrente com link na tela (fora, para não confundir o público).
5. Pet saudável; nada em `clipes_banidos.md`.

### Pontuação (100). Entra com ≥ 70
Parte numérica (40)
| Critério | Regra | Pts |
|---|---|---|
| Momentum | ≥ 1 mi = 20; ≥ 300 mil = 15; ≥ 100 mil = 10 | 20 |
| Compartilhamento | ≥ 1,5 % = 10; ≥ 0,8 % = 6 | 10 |
| Curtidas | ≥ 5 % = 5 | 5 |
| Frescor | ≤ 7 d = 5; ≤ 30 d = 3 | 5 |

Parte de conteúdo (60)
| Critério | Regra | Pts |
|---|---|---|
| Comentários de compra | ≥ 3 nos top 10 = 15; 1-2 = 8 | 15 |
| Antes/depois visível | problema aparece E resultado aparece | 15 |
| Dor frequente | xixi fora do lugar, come rápido, dente/mau hálito, ansiedade/lamber, carro, pular na cama (idoso/pequeno) | 10 |
| Duda acrescenta | tutora que viveu o problema ("isso me salvou"): 2 de 3 = 10; 3 de 3 = 15 | 15 |
| Link pronto | produto está na lista com link de afiliado; comissão ≥ 14 % = 5, menor = 3 | 5 |

Métrica que decide o teste: cliques no link de afiliado em 24 h (Shopee › painel de afiliado) além de views. Rótulo "link de afiliado" sempre visível na legenda.

## Fontes de busca (TikTok logado no Chrome do Allan; páginas de hashtag mostram os vídeos em alta e são a fonte que funcionou em 29-30/10)
Vertente A — hashtags BR: #cachorro #cachorros #gato #gatos #pet #pets #cachorroengraçado #cachorrosengraçados #gatoengraçado #humorpet #petsdotiktok #filhote #caramelo #viralata #golden #shihtzu #pinscher #spitzalemão #dogs #catsoftiktok
Vertente A — hashtags fora do Brasil (humor visual): #dogsoftiktok #funnydogs #funnycats #catsoftiktok #perros #gatos #perrosgraciosos #dogfail #catfail #puppy
Vertente A — perfis que já estouraram (abrir e pegar os 12 últimos): @metropolesoficial, @max_pegadordeencomenda, @maya.caramelo, @tiny.mischiefs, @caramelaeborisfiapo, @tuxytales + os 3 perfis com mais views que aparecerem nas hashtags do dia.
Vertente B — termos de pesquisa (barra de busca, aba Vídeos; cada termo também como hashtag): "educador xixi cachorro", "xixi sim xixi não", "sanitário para cachorro", "tapete higiênico xixi no lugar certo", "dedeira dental cachorro", "escovar dente cachorro", "gel dental cachorro", "comedouro lento", "cachorro come rápido", "slow feeder", "tapete de lamber", "lickmat cachorro", "cinto de segurança cachorro", "cachorro no carro cinto", "escada pet cama", "escadinha para cachorro sofá", "achados shopee pet", "achadinhos pet", "tiktok shop pet"
Vertente B — hashtags: #achadinhosshopee #achadosshopee #achadospet #dicaspet #tiktokshopbrasil #tapetehigienico #comedourolento #lickmat #slowfeeder #dogseatbelt #petstairs #dogteeth

## Processo (zero crédito até o "pode")
1. Sonnet: coleta 60-120 links (A) + 40-80 links (B) → `scripts/curadoria_tiktok.py` → descarta quem não passa nos pré-requisitos numéricos → baixa os 25 melhores (15 A + 10 B) → folha de quadros 1 fps com timestamp + transcrição faster-whisper + top 10 comentários → tabela.
2. Fable: assiste pelas folhas + transcrição, dá a parte de conteúdo, escolhe 3 + 3, escreve mapa de batidas e 6 roteiros com falas por timestamp (regra 41).
3. Allan: "pode" em cima do texto. Só então animático (≈ 0,2 % ElevenLabs), depois HeyGen só das falas.
4. Falha de curadoria vira ficha do Auditor/Otimizador no mesmo dia.

# Curadoria v4 de reacts — diagnóstico, critérios e duas vertentes (Fable, 30/10/2026, 02h)
Substitui a v3 escrita 1 h antes (a v3 errou no diagnóstico; corrigido abaixo com números medidos).

## 1. Diagnóstico com números (medidos por yt-dlp em 30/10 02:00)
| Vídeo | Views | Curtidas | Coment. | Compart. (% das views) | Mediana da conta | Múltiplo |
|---|---|---|---|---|---|---|
| r01 atleta dos cones (Metrópoles) | 207 mil | 27,5 mil | 191 | 3,4 mil (1,6 %) | ~12 mil | 17x |
| r02 gato barrigudinho (Metrópoles) | 163 mil | 32 mil | 367 | 3,0 mil (1,8 %) | ~12 mil | 13x |
| r05 cachorro foge da polícia (iG) | 103 mil | 6,9 mil | 203 | 712 (0,7 %) | ~1,1 mil | 90x |
| n03 pinscher ciumenta (o 1º react, Metrópoles) | 1,9 mi | 109 mil | 2,3 mil | 31 mil (1,6 %) | ~12 mil | 160x |
| n01 Max pega a encomenda | 5,0 mi | 778 mil | 2,8 mil | 40 mil (0,8 %) | alta (conta viral) | — |
| n02 José Augusto (Metrópoles) | 3,6 mi | 622 mil | 2,3 mil | 63 mil (1,7 %) | ~12 mil | 300x |

**O que isso prova**
1. Os três do lote 2 tinham **10 a 50 vezes menos público** que o 1º react e que os virais da mesma fila. "Carona" só funciona quando a onda é grande: 100-200 mil views no TikTok brasileiro de pet não é onda, é marola.
2. A v3 tinha dito que eles eram "o piso de conta gigante". Errado: em múltiplo da própria conta eles até passam (13x a 90x). O múltiplo mede **talento do vídeo**, não **tamanho da onda**. Para carona, manda o volume absoluto; o múltiplo serve para achar criador pequeno estourando (ex.: maya.caramelo, 214 mil views com mediana de 830 = 258x).
3. **r05 tinha compartilhamento fraco (0,7 %)** e os três tinham comentários em "n/d" na fila: ninguém leu o que o público achou engraçado, então não havia "frase na voz do pet" nem pico mapeado antes de escolher.
4. Faltou o filtro de **conteúdo**: r01 (circuito de 57 s, sem virada), r02 (fofo sem piada), r05 (piada só no áudio). A Duda não tinha o que acrescentar.
5. **Onde estava o erro: na escolha (Fable, plano do lote 2 de 29/10), não na execução.** O Sonnet executou o plano como escrito; os 2 tropeços de execução (look errado no r05, loudness alta) foram corrigidos antes da entrega e não mudaram o resultado. O processo falhou por não ter critério numérico obrigatório antes de gastar crédito.

## 2. Pré-requisitos (eliminam; não pontuam)
- Nicho pet (cão/gato; outro animal só se for doméstico e fofo). Nada de animal doente, abrigo, doação, briga, perigo, pessoa identificável em situação constrangedora, farda/polícia/criança em foco.
- Sem marca d'água de outro app ou página (Pubity, caixa "P", logos). Legenda queimada do próprio criador é aceita.
- Criador identificável para o crédito (@ no TikTok; anotar também o Instagram se houver).
- Publicado há ≤ 7 dias (ideal ≤ 3). Duração ≤ 60 s; se > 20 s, tem que existir um corte de 10-20 s que se sustenta sozinho.
- Nenhum número em "n/d": views, curtidas, comentários, compartilhamentos, data e mediana da conta vêm de `scripts/curadoria_tiktok.py` (zero crédito, 20 s por vídeo).
- Conferir `biblioteca/clipes_banidos.md`.

## 3. Pontuação v4 — vertente A: carona em viral de humor (entra com ≥ 75/100)
**Parte numérica (70, automática pelo script)**
| Critério | Regra | Pontos |
|---|---|---|
| Momentum absoluto | ≥ 1 mi views = 25; ≥ 500 mil = 20; ≥ 200 mil = 12; ≥ 50 mil = 5 | 25 |
| Viralidade relativa | views ÷ mediana dos últimos 12 da conta: ≥ 20x = 15; ≥ 5x = 10; ≥ 2x = 5 | 15 |
| Compartilhamento | compart ÷ views: ≥ 3 % = 15; ≥ 1,5 % = 10; ≥ 0,8 % = 5 | 15 |
| Curtidas | curtidas ÷ views ≥ 10 % = 5; ≥ 5 % = 3 | 5 |
| Frescor | ≤ 3 dias = 10; ≤ 7 dias = 6 | 10 |

**Parte de conteúdo (30, preenchida por quem ASSISTIU o vídeo inteiro com áudio)**
| Critério | Regra | Pontos |
|---|---|---|
| Pico claro | 1 virada visível SEM áudio nos primeiros 15 s do corte (flagra, susto, resposta, antes/depois) | 10 |
| O que a Duda acrescenta | dos três — **educativo** (explica o porquê ou dá 1 dica de tutora), **ilustrativo** (mostra/compara, "olha isso"), **engraçado** (piada específica da cena ou voz do pet) — pelo menos **2 presentes = 10; os 3 = 15**; só 1 = 0 e o vídeo cai | 15 |
| Voz do público | os 10 comentários mais curtidos já entregam a piada/pergunta; CTA "e o seu faz isso?" cabe natural | 5 |

Regras de decisão: ≥ 75 entra; 60-74 reserva; < 60 fora. Nunca escolher pelo "mais seguro"; segurança é pré-requisito. Lote mínimo: 10 candidatos pontuados para 3 escolhidos.

## 4. Pontuação v4 — vertente B: react de PRODUTO (TikTok vende os afiliados da Shopee)
Fonte: vídeos de uso dos produtos de `data/produtos/afiliados_shopee.md` (busca no TikTok pelo nome do produto + cachorro/gato; mesma régua numérica, mas com piso menor porque o nicho é menor).
| Critério | Regra | Pontos |
|---|---|---|
| Momentum absoluto | ≥ 300 mil = 20; ≥ 100 mil = 14; ≥ 30 mil = 8 | 20 |
| Compartilhamento + salvamentos | compart ÷ views ≥ 1,5 % = 10; ≥ 0,8 % = 6 | 10 |
| Comentários de compra | entre os 10 mais curtidos há "onde compro?", "funciona?", "qual o nome?" | 15 |
| Produto visível em uso + resultado visível | pet usando e o problema resolvido na tela (antes/depois) | 20 |
| Dor real e frequente do tutor | xixi fora do lugar, come rápido, gato não bebe água, unha, dente, carro, escada | 15 |
| Produto igual ou equivalente na nossa lista (link de afiliado pronto) | comissão ≥ 10 % soma +5 | 10 |
| Corte de 15 s se sustenta + Duda acrescenta ≥ 2 de educativo/ilustrativo/engraçado | | 10 |
Entra com ≥ 70. Roteiro: Duda tutora ("eu uso / eu testei"), 1 frase da dor, 1 frase do que resolve, CTA "link na bio" com rótulo de afiliado. Nada de promessa de saúde. Métrica que decide: **cliques no link de afiliado em 24 h** (além de views).

## 5. Processo obrigatório (vale para as duas vertentes)
1. Coletar 20-40 links: Explorar › Animais do TikTok (logado no Chrome do Allan), pesquisa por termo e páginas de criadores que já estouraram. Links vão para `data/remix/fila_virais.csv`.
2. Rodar `python3 scripts/curadoria_tiktok.py urls.txt --csv ...` → parte numérica. Descartar < 40/70.
3. Baixar os 8-10 melhores (yt-dlp), folha de quadros 1 fps + transcrição (faster-whisper local). **Assistir.** Preencher a parte de conteúdo.
4. Escolher 3 com ≥ 75, mapear batidas segundo a segundo (regra 41), escrever o cartão de falas com timestamps, texto de tela e custo em % do saldo restante. Só então o "pode" do Allan.
5. Registrar: pontuação por critério na fila; resultado em `resultados.csv`; aprendizado em `07 Erros e lições.md` e na habilidade `biblioteca/habilidades/curadoria_viral_v4.md`.

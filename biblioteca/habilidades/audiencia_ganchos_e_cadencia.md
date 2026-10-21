---
criado: 2026-10-21
base_externa: skills_externas/marketingskills/social (SKILL.md + references/short-form-video.md), skills_externas/marketingskills/ad-creative/references/hook-system.md, skills_externas/openclaudia/content-calendar, skills_externas/upload-post/comment-funnel (só lógica), skills_externas/upload-post/viraloop
---
# Habilidade: criar audiência com vídeo curto — ganchos, matriz, cadência e funil de comentário (Criador de Audiência, Humorista, Pesquisador de Formato, Atendente de Comentários)

## Por que existe
A criação de audiência está fraca (Allan, 21/10/2026) e os agentes propunham "ideias" soltas, sem sistema. Esta habilidade traz um método pronto e testado de fora (ver `base_externa`), adaptado ao pet, ao low-ticket e à Duda. Regra do Allan: não inventar a roda — usar o que existe, do nosso jeito.

## Leia no original (inglês) antes de produzir o lote
1. `biblioteca/skills_externas/marketingskills/social/references/short-form-video.md` — biblioteca de ganchos por objetivo (curiosidade → engajamento; valor → salvamentos; história → tempo assistido; polêmica → comentários; contraste → decisão), template de roteiro 0-3s / corpo / CTA, estrutura POV/esquete 15-30s.
2. `biblioteca/skills_externas/marketingskills/ad-creative/references/hook-system.md` — seções "A Hook Is Three Components", "The Generation Pipeline" (Segmento → Motivação → Formato → Gancho) e "The Diagnostic Funnel".
3. `biblioteca/skills_externas/marketingskills/social/SKILL.md` — seção "No AI Tells" (frases que denunciam texto de IA: "não é X, é Y", listas de negação, pergunta auto-respondida). Vale para legenda e fala da Duda.

## Regras adaptadas ao Tutorial Pet (estas mandam quando conflitarem com o original)
1. **Gancho = 3 peças que não se repetem**: ação visual (0-3 s: o animal fazendo algo), fala da Duda (ou texto falado), texto na tela. As três têm de dizer coisas diferentes e complementares. Roteiro com só uma peça preenchida está incompleto — não entra na grade.
2. **Matriz, não lista**: cada lote nasce de uma tabela `Segmento (tutor de X com dor Y) × Motivação (frase verbatim do público, ver .agents/product-marketing.md e comentários reais) × Formato (POV, "seu pet quando…", isso ou aquilo, mito x verdade, identificação humana, ranking de raça, esquete) × Gancho (3 peças)`. 10 ideias de 10 células valem mais que 30 variações da mesma. Registre a matriz em data/audiencia/ideias.md.
3. **Objetivo por fase** (decifrador_algoritmo.md): agora o que importa é comentário > compartilhamento > seguidor. Portanto o lote diário tem no mínimo 40% de ganchos de polêmica leve/identificação (gato x cachorro, "só eu que…", escolha A ou B) e 30% de valor salvável (3 erros, mito x verdade). História/transformação só com caso real ou demonstração.
4. **Rampa (3-15 s)**: o que vem depois do gancho tem de continuar a promessa do gancho, nunca pular para a marca ou para o produto. Se o gancho promete "o motivo", o segundo 3 explica o motivo.
5. **CTA de comentário é obrigatório** em todo vídeo de audiência: pergunta que divide ("time gato ou time cachorro?"), pedido de identificação ("marca quem faz isso") ou **palavra-chave → DM** ("comenta GUIA que eu te mando no direct"). Lógica do funil comentário→DM (de comment-funnel, sem a API deles): 1 palavra-chave simples por post; resposta privada em até 1 h enquanto a janela vale; limite prático da Meta ~200 DMs/h e 1 resposta privada por comentário; DM entrega o link do blog/landing com UTM (utm_medium=dm). Quem executa a DM: Atendente de Comentários (ver prompt dele); quem desenha a isca: Criador de Audiência. Nunca pedir dado pessoal na DM.
6. **Cadência** (platforms.md + content-calendar, adaptada): TikTok 1-2/dia, Instagram 1 Reel/dia + Stories, Facebook 1-2/dia; nunca dois posts colados (espaço mínimo definido pelo Estrategista em config/estrategia_social.yaml). Pilares fixos da semana: 40% identificação/humor, 30% valor rápido, 20% trend do dia, 10% produto (Sozinho em Casa) — produto nunca mais que 1 em 10.
7. **Loop diário (viraloop)**: toda rodada começa lendo o desempenho de 72 h+ dos posts anteriores (Zernio/Buffer), classifica cada um em "repetir / variar / aposentar" e só então gera o lote novo. Repetir = mesma célula da matriz com gancho novo; variar = trocar UMA peça do gancho; aposentar = célula sem comentário em 5 posts.
8. **Diagnóstico por etapa** quando um post falha (hook-system "Diagnostic Funnel"): visualização de 3 s baixa → trocar só a ação visual; retenção 3-15 s baixa → reescrever só a rampa; comentário baixo com retenção boa → trocar só o CTA. Uma peça por teste, mínimo 5 posts (decifrador_algoritmo.md).
9. **Jev decide o básico** (jev_decisao_rapida.md): (a) classificar cada ideia como liberada/sensível (já ligado); (b) escolher qual de duas variações de gancho testar primeiro (`choice`); (c) julgar se um gancho novo repete célula já aposentada (`noul`). Julgamento de polêmica com pessoa real continua com o Allan.
10. **Proibido**: copiar frase, imagem ou vídeo de referência; "AI tells"; pet doente/abrigo; raça errada no clipe; promessa de saúde; mais de 1 CTA por vídeo.

## Entrega
Lote em data/audiencia/ideias.md com a matriz preenchida (segmento, motivação verbatim, formato, 3 peças do gancho, CTA, pilar, slot). Primeira linha "Dados até…". Falha ou gap de habilidade → registro_de_falhas.md. Achado que pede decisão do Allan → entrega_direta.md.

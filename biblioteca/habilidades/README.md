# Índice de habilidades (biblioteca/habilidades/)

Regra do Allan (21/10/2026): **não inventar a roda**. Antes de criar uma habilidade nova do zero, procurar uma skill pronta em `biblioteca/skills_externas/` (ver o README de lá) ou fora, adaptar ao nosso jeito, nunca copiar texto/imagem de terceiros para o público. Toda habilidade nova entra nesta lista.

## De accountability (toda rotina de pesquisa/ação usa)
| Habilidade | O que faz | Quem lê |
|---|---|---|
| `entrega_direta.md` | Achado que pede decisão vai por PushNotification na hora, nunca espera a Triagem | Toda rotina de pesquisa/caça |
| `registro_de_falhas.md` | Toda falha/gap de habilidade do próprio agente é registrada, não só quando o Allan percebe | Todos os agentes |
| `painel_central_achados.md` | Toda rotina de pesquisa escreve o achado num painel central, não num documento isolado | Toda rotina de pesquisa |
| `controle_prova_real.md` | Nunca marcar "ok" só pelo status verde; checar a saída real | Auditores e quem valida resultado de outro agente |
| `decifrador_algoritmo.md` | Como julgar amostra pequena (idade do post, tamanho mínimo, uma variável por vez, métrica por fase) | Quem mede resultado de post/anúncio | v2 (22/10, rascunho até prova) |
| `jev_decisao_rapida.md` | Jev (typesafe/jev-1.13) decide o básico/binário por padrão; agente decide quando ele não tem certeza | Toda rotina com decisão simples |
| `verificar_antes_de_pedir.md` | Antes de listar "Decisão do Allan"/pendência, releia 05 Decisões.md e 06 Pendências.md por completo — já decidido não vira pedido novo | Toda rotina que produz pendência/decisão para o Allan |

Coluna de versão: ao fim da linha, "v2" = reescrita com regras de plataforma [C]/[N], números nossos e saída obrigatória (PADRAO_SKILL_ROBUSTA.md); status rascunho até a régua 7.

## De marketing/audiência (trazidas de skills externas, 21/10/2026 — ver `biblioteca/skills_externas/README.md`)
| Habilidade | O que faz | Quem lê |
|---|---|---|
| `audiencia_ganchos_e_cadencia.md` | Gancho em 3 peças, matriz segmento×motivação×formato, cadência, CTA/funil comentário→DM, loop diário, diagnóstico por etapa | Criador de Audiência, Humorista, Atendente de Comentários | v2 (22/10, rascunho até prova) |
| `criativo_venda_low_ticket.md` | Estrutura de roteiro que vende (15-25s/VSL), movimentos de abertura, escada de fidelidade de produção | Criativo de Venda e VSL | v2 (22/10, rascunho até prova) |
| `oferta_low_ticket.md` | As 6 peças de uma oferta completa, equação de valor, escada de produto, estrutura de landing low-ticket | Marketing de Produto, Fábrica de Produtos, Produtor de e-book, Aprimorador de Landing |
| `anuncios_meta_decisao.md` | Checagem de conta Meta em 6 passos que termina em UMA decisão; regras de CPA/fadiga/escala para orçamento pequeno; Pass/Fail/Unknown | Auditor de Anúncios | v2 (22/10, rascunho até prova) |
| `analise_referencia_viral.md` | Ficha por referência (gancho, linha do tempo, padrão replicável + nossa versão), análise em lote | Pesquisador de Formato, Pesquisador de Mercado | v2 (22/10, rascunho até prova) |

Contexto de marca/produto que as skills externas em `biblioteca/skills_externas/marketingskills/` leem sozinhas: `.agents/product-marketing.md` (raiz do repositório).

## Plataformas e tráfego (22/10/2026)
Transformam o compêndio `biblioteca/regras_plataformas/` em procedimento executável (entradas, passos numéricos, checklist, laço de aprimoramento em `data/habilidades/aprendizado/<skill>.md`, itens [N] à parte). Os agentes não pesquisam regra de plataforma de novo: leem a skill.
| Habilidade | O que faz | Quem lê |
|---|---|---|
| `plataforma_meta_organico.md` | Facebook + Instagram orgânico: originalidade, marca d'água, rótulo IA, hashtags, grade e espaçamento, limites pass/fail, comentário→DM | Estrategista de Redes Sociais, Criador de Audiência, Produtor/Guardião de vídeo, Atendente de Comentários |
| `plataforma_tiktok_organico.md` | TikTok orgânico: música CML, rótulo IA/comercial, ganchos permitidos e proibidos, funil por DM, limites pass/fail | Especialista TikTok, Estrategista, Criador de Audiência, Produtor de vídeo |
| `trafego_meta_ads.md` | Ciclo do anúncio Meta antes e em volta da checagem (elegibilidade, criativo, conformidade, UTM, revisão 24 h); complementa `anuncios_meta_decisao.md` | Agente de Tráfego, Guardião de Gasto, Executor de Decisões (Auditor segue com anuncios_meta_decisao.md) |
| `trafego_tiktok_ads.md` | TikTok Ads/Spark Ads: escolha do vídeo, política de animais, rótulo IA, regras diárias | Agente de Tráfego, Especialista TikTok, Guardião de Gasto, Executor de Decisões |
- blog_adsense_4_semanas.md (v1 22/10): operar as 4 semanas até o AdSense: ritmo 3/4 por dia, variedade de temas/formatos, enquetes, tráfego e SEO; dono Diretor de Conteúdo; molde depois.

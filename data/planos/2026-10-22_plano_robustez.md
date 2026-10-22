# Plano de robustez dos agentes — 22/10/2026 (Allan + Claude). Executável, com dono, prazo e prova.
Diagnóstico (painel de 22/10): média 1,7/5 em 32 agentes. Causa raiz não é falta de instrução: é falta de JULGAMENTO antes de publicar e de PROVA depois. Três buracos explicam audiência fraca, design ruim e foto incoerente: (1) ninguém pontuava a entrega; (2) o seletor de capas pegava a candidata 0; (3) o gerador de legenda/gancho usa texto velho (R$ 9,90, "cão", ganchos banidos). Blog: 21/10 foi o último dia com artigo até 14:00 de 22/10 (ritmo 3–4/dia não cumprido); o AdSense avalia regularidade, variedade e coerência durante as 4 semanas.

Regra do plano: nada de teste ao vivo sem ensaio julgado (nota ≥ 7). Toda etapa termina com prova em arquivo. Leitura em horas, não dias.

## Fase 0 — HOJE (22/10), já feito até 14:00
- [x] Compactação: 9 gatilhos excluídos, 15 em reserva, 17 ativos (config/prompts/reserva/README.md).
- [x] Juiz de Qualidade (skill + prompt) e 2 ensaios: ganchos 4,0 → 8,2; capas 6,6 (2 reprovadas e trocadas).
- [x] Portão de gancho no Publicador e no Agendador; E34 no Vigia; preço R$ 27 nos prompts; core/capa.py pontua todas as candidatas.
- [x] 7 posts com gancho banido substituídos; 4 artigos promovidos para hoje (lagrima, gato morde, petiscos, Yorkshire/Xuxa).

## Fase 1 — HOJE à tarde/noite (22/10): fechar os 3 buracos
| # | Ação | Dono | Prazo | Prova |
|---|---|---|---|---|
| 1.1 | Gerador de legenda e gancho (agents/ roteiro + fabrica_nuvem.py): proibir "R$ 9,90", "de R$ 37", "cão/cãozinho/pet", ganchos banidos; gancho = pergunta com número validado no artigo; variar o molde por rodada | Claude (sessão) | 17:00 | grep = 0 ocorrências nos 10 roteiros novos; 1 roteiro gerado e julgado ≥ 7 |
| 1.2 | Juiz separado reconfere os 3 ganchos do lote (Allan vê antes de ir ao ar) | Juiz | 16:00 | data/ensaios/2026-10-22_ganchos_lote.md |
| 1.3 | Leitura do teste de audiência: 18:00 e 23:30 (views 1 h/3 h, comentário de terceiro); regra de troca já escrita | Medidor + Claude | 18:00 / 23:30 | linha em data/testes/audiencia_2026-10-22_aplicado.md |
| 1.4 | Blog: conferir os 4 artigos de hoje no ar com capa coerente (Juiz rubrica B ≥ 7 em cada) | Juiz | 17:00 | data/ensaios/2026-10-22_capas_novas.md |
| 1.5 | Ritmo: Vigia das 15:19 passa a PROMOVER rascunhos prontos quando o dia tem < 3 artigos (hoje ele viu 0 e não agiu) | Claude → vigia_rotinas.md | 15:00 | rodada das 15:19 com "CORRIGI: n ≥ 1" |

## Fase 2 — amanhã (23/10): ensaio probatório de todos os ativos de produção
Cada agente produz 5 entregas sobre material existente; o Juiz pontua; média ≥ 7 e nenhuma < 5 = pode testar ao vivo. Senão a skill recebe a correção e repete no mesmo dia.
| Agente | Entrega do ensaio | Rubrica | Hora |
|---|---|---|---|
| Criador de Audiência | 10 ganchos (lote 10→3 do dia) | A | 09:00 |
| Revisor de Coerência | 5 capas de artigos antigos com pior nota | B | 10:00 |
| Redator (fábrica) | 3 artigos em 3 moldes diferentes (lista, pergunta-resposta, história curta) — variedade de escrita exigida pelo AdSense | nova rubrica D (abaixo) | 11:00 |
| Publicador | portão em 5 pacotes banidos + 5 limpos (5/5 e 0 falso positivo) | binário | 12:00 |
| Agendador | fila das próximas 36 h: 0 ganchos banidos, ≥ 10 min entre redes | binário | 12:30 |
| Diretor de Conteúdo | auditoria AdSense antes/depois: FAILs de 4 para ≤ 1 (capas únicas, 3 fontes de saúde) | script | 15:00 |
| Vigia | problema plantado inofensivo (workflow cancelado): detectar e corrigir em ≤ 30 min | tempo | 16:00 |
Rubrica D — ARTIGO (0–10), para o AdSense: D1 responde a pergunta do título nos 2 primeiros parágrafos; D2 molde diferente do artigo anterior (lista / passo a passo / pergunta-resposta / caso real); D3 fonte citada quando fala de saúde; D4 ≥ 3 links internos e 1 foto de corpo coerente; D5 sem frase-clichê de IA ("neste artigo vamos", "é importante lembrar", "em resumo"). Reprova automática: alegação de cura, "cão", preço velho.

## Fase 3 — 24 a 28/10: lote diário e medição em horas
- Todo dia: 10 ganchos → Juiz → 3 ao ar → leitura 1 h / 3 h → linha de aprendizado na skill. Mediana de views por rede como régua; abaixo dela em 3 lotes seguidos = muda a rubrica, não o produtor.
- Blog: 3–4 artigos/dia com molde rotativo (D2), capa julgada (B) antes de publicar, auditoria AdSense diária às 07:19.
- Removedor de Gargalos (sexta 10:41): atualiza as fichas do painel; nota sobe só com prova.
- Meta do painel em 28/10: média ≥ 3,0; nenhum ativo em 0 ou 1; 3 agentes em 4 (resultado medido).

## Fase 4 — produto vendável (depois do painel em 3,0)
Camada genérica do Juiz e do painel (rubricas com {NICHO}, {MARCA}, {REFERÊNCIA}); ensaio probatório como padrão de onboarding de agente; régua 7 (prova antes de vender) do PADRAO_SKILL_ROBUSTA.

## O que o Allan decide
- Ver os 3 ganchos do lote antes de ir ao ar (hoje, após 1.2).
- Se a média do painel não chegar a 3,0 em 28/10, o que corta: agentes ou tipos de entrega.

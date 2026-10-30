# Critérios de curadoria v3 — por que r01/r02/r05 foram escolhidos e o que muda (Fable, 30/10/2026)

## 1. Diagnóstico: como esses três entraram
- A fila `fila_virais.csv` (29/10) registrou só **views** (r01 195 mil, r02 135 mil, r05 100 mil) e deixou curtidas, comentários e compartilhamentos em **n/d**. A escolha foi por 3 filtros: (a) página de notícia brasileira que reposta com crédito (para evitar marca d'água do Pubity e problema de crédito), (b) publicado há ≤ 48 h, (c) views "altas". Nada de engajamento foi medido.
- **Erro central: views brutas de uma conta gigante.** Metrópoles e iG têm milhões de seguidores; 100 a 200 mil views é o **piso** deles, não um hit. A própria skill `analise_referencia_viral.md` já mandava: "post com ≥ 10x a mediana da PRÓPRIA conta vale mais que conta gigante; comentário alto". Esse critério existia e não foi aplicado.
- Os números confirmam: na mesma fila, n01 (642 mil curtidas), n02 (600 mil curtidas, 60 mil compartilhamentos), e01 (4,3 mi curtidas, 1,5 mi compartilhamentos) eram virais de verdade. r01/r02/r05 foram descartes seguros, não os melhores.
- Segundo erro: **cena sem pico claro**. r01 é um circuito de 57 s (prova de agilidade, sem "virada"); r02 é um gatinho vindo (fofo, sem piada); r05 depende de ouvir "polícia" no áudio. O método v2 exigia "1 pico claro em até 15 s e frase na voz do pet óbvia nos comentários"; sem ler os comentários (n/d), esse filtro também não rodou.
- Terceiro erro: o filtro de **segurança operacional** (crédito limpo, sem marca d'água) virou o critério principal e empurrou a qualidade para segundo plano. Segurança é pré-requisito, não critério de escolha.

## 2. Critérios v3 (pontuação, 0-100; entra no lote só com ≥ 70)
Pré-requisitos (eliminam, não pontuam): sem marca d'água de outro app; criador identificável para o crédito; nicho pet, nada de animal doente/abrigo/briga/perigo; publicado há ≤ 72 h; dura ≤ 60 s.

| Critério | Como medir | Peso |
|---|---|---|
| **Viralidade relativa** | views (ou curtidas) do vídeo ÷ mediana dos últimos 10 vídeos da MESMA conta. ≥ 10x = 25; 5-10x = 18; 2-5x = 10; < 2x = 0 | 25 |
| **Taxa de compartilhamento** | compartilhamentos ÷ views. ≥ 3 % = 20; 1-3 % = 12; < 1 % = 4 | 20 |
| **Taxa de comentários** | comentários ÷ views. ≥ 0,5 % = 15; 0,2-0,5 % = 9; < 0,2 % = 3 | 15 |
| **Pico claro** | existe 1 momento de virada (susto, flagra, resposta, falha) nos primeiros 15 s do corte, visível SEM áudio | 15 |
| **Frase na voz do pet pronta** | os 3 comentários mais curtidos já entregam a piada ou pergunta ("e o seu faz isso?") | 10 |
| **Reutilizável em 15 s** | o corte de 10-20 s se sustenta sozinho (gancho + pico), sem precisar do resto | 10 |
| **Pergunta de tutor** | o vídeo levanta uma dúvida real de comportamento que a Duda pode responder em 1 frase (gancho de utilidade) | 5 |

Regras de leitura:
- Coletar **todos** os números (views, curtidas, comentários, compartilhamentos, favoritos, data) — campo n/d bloqueia a entrada na fila. Se o TikTok não mostrar views, usar curtidas ÷ mediana de curtidas da conta.
- Viralidade relativa pede abrir o perfil da conta e anotar os últimos 10 vídeos (2 min por conta). Conta gigante com vídeo na média = 0 pontos nesse critério, mesmo com 1 milhão de views.
- Ler os 10 comentários mais curtidos antes de pontuar "pico" e "frase na voz do pet": o público já diz qual é a piada.
- Fonte prioritária: criador original pequeno/médio (10 mil a 500 mil seguidores) com vídeo ≥ 10x a média dele. Página de notícia só quando o criador original está creditado e o vídeo dele também passa no pré-requisito.
- Registrar a pontuação por critério na `fila_virais.csv` (novas colunas: mediana_conta, multiplo_conta, taxa_compart, taxa_coment, pico_15s, voz_pet, score_v3).

## 3. O que fazer com r01/r02/r05
- Pela régua v3 nenhum dos três passaria de ~40 pontos (viralidade relativa 0, engajamento não medido, pico fraco).
- Mantê-los só como **teste de formato** (as bases B1/B2r/B3r e a montagem nova), com leitura de 24 h; não são referência de conteúdo.
- Próximo lote: re-pontuar n01, n02 e e01 pela v3 (candidatos óbvios) e buscar 10 novos pela v3 antes de qualquer crédito.

---
criado: 2026-10-21
base_externa: skills_externas/openclaudia/video-ad-analysis, skills_externas/marketingskills/social/references/reverse-engineering.md, skills_externas/marketingskills/ad-creative/references/hook-system.md
---
# Habilidade: decompor referência viral/anúncio e devolver padrão replicável (Pesquisador de Formato, Pesquisador de Mercado, Curador de referências)

## Leia no original
1. `skills_externas/openclaudia/video-ad-analysis/SKILL.md` — 5 dimensões (gancho, persuasão, estrutura e ritmo, público, CTA), formato de saída com linha do tempo, "Replicable Patterns" e "Batch Analysis" (padrões em lote).
2. `skills_externas/marketingskills/social/references/reverse-engineering.md` — como ler um perfil/post que performa e extrair o sistema, não o post.

## Regras adaptadas ao Tutorial Pet
1. **Nunca copiar; só a lógica**. A ficha de cada referência (no Banco de Referências e em config/estilo_viral.yaml) tem: fonte + link + data; gancho em 3 peças (visual / fala / texto); linha do tempo por segundo (0-3, 3-8, 8-15, fim); mecanismo (identificação, polêmica leve, prova, curiosidade, contraste); CTA; sinal de público (comentários que dominam); e **"padrão replicável em 1 frase"** + **"nossa versão"** (mesma estrutura, animal certo, Duda, frase original). Sem "nossa versão" a ficha está incompleta.
2. **Em lote, não uma a uma**: a cada rodada, 8-12 referências → tabela de padrões (gancho mais comum, mecanismo dominante, duração mediana, CTA mais usado) → 3 recomendações que mudam o próximo lote do Criador de Audiência / Criativo de Venda. O número que importa é "quantas recomendações viraram roteiro na grade" — recomendação parada em relatório é falha (entrega_direta.md).
3. **Critérios de seleção** (config/estilo_viral.yaml): nicho pet, últimos 30 dias, desempenho relativo ao tamanho da conta (post 10x acima da mediana da própria conta vale mais que conta gigante), 7-20 s, com comentário alto. Anúncio: Biblioteca de Anúncios Meta, no ar há 30+ dias = sinal de que converte.
4. **Compare com os nossos**: para cada padrão externo, achar o post nosso mais parecido (72 h+) e dizer o que falta (visual? rampa? CTA?) usando o funil de diagnóstico do hook-system. Se nenhum nosso chega perto, o teto não foi atingido: continua testando formato, não declara vencedor.
5. **Jev**: `noul` "is this reference already in the bank (same creator/same hook)?" antes de incluir; `choice` para classificar o mecanismo dominante quando for óbvio. Julgar se vale virar roteiro é do agente.
6. Falha (ex.: sem navegador na rodada, link que não abre) → registro_de_falhas.md com alternativa tentada.

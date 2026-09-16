# Agente 04 — Quality Editor

## Papel
Revisar o rascunho do agente 03 antes de liberar para SEO/publicação. Este agente **não
reescreve o texto** — ele sinaliza problemas para um humano decidir (ajustar manualmente
ou reenviar ao agente 03). Isso mantém o humano no controle de qualquer mudança de
conteúdo, e evita que um filtro automático "conserte" algo silenciosamente.

## O que este agente é (e o que não é)
É um **filtro heurístico determinístico**: listas de padrões de texto (`agent.py`),
não uma checagem factual real nem uma revisão editorial completa. Ele pega os erros
óbvios e mecânicos; nunca substitui a leitura humana antes da publicação.

## Checagens obrigatórias

1. **Originalidade** — procura clichês típicos de "conteúdo gerado em massa" (ex.: "é
   importante ressaltar que", "sem sombra de dúvida", "neste artigo, vamos explorar").
   1–2 ocorrências viram aviso; 3 ou mais bloqueiam a aprovação.
2. **Precisão factual em tópicos sensíveis** (`aviso_saude_aplicavel: true`) — compara o
   texto contra uma lista de afirmações implausíveis/arriscadas (ex.: "não precisa de
   veterinário", "cura garantida", "cientificamente comprovado"). **Isto é uma checagem
   de plausibilidade, não uma verificação contra uma fonte específica** — o agente não
   sabe se um fato é verdadeiro, só reconhece padrões de afirmação perigosa ou
   contraditória com a persona editorial (que nunca alega estudos/comprovação
   científica). Também confere que o aviso de saúde do site (`compliance.aviso_saude`)
   está presente no corpo do texto.
3. **Tom** — procura vocabulário técnico/formal que destoa da persona "caloroso,
   prático, não-técnico" (ex.: "outrossim", "posologia", "anamnese"). 1 ocorrência vira
   aviso; 2 ou mais bloqueiam.
4. **Legibilidade** — sinaliza frases com mais de 35 palavras e parágrafos com mais de
   130 palavras. Poucas ocorrências viram aviso; muitas (mais de 25% das frases, ou 2+
   parágrafos densos) bloqueiam a aprovação.
5. **Autoria e credencial** — confere que o campo `autor` do front-matter continua em
   branco e que o texto não contém nenhuma alegação de credencial veterinária real
   (ex.: "sou veterinário", "meu CRMV"). Qualquer ocorrência bloqueia a aprovação.

## Regra de aprovação
Qualquer problema classificado como `bloqueante` reprova o artigo. Problemas
classificados como `aviso` não impedem a aprovação, mas ficam registrados no
front-matter (`checagens_qualidade`) e nas pendências humanas da saída, para melhoria
contínua.

## Uso futuro de LLM
Se um LLM for plugado para reforçar esta etapa, ele pode receber o artigo completo e:
- Fazer uma leitura de tom mais sofisticada do que a lista de palavras-chave atual.
- Sugerir reescritas pontuais para as frases/parágrafos sinalizados na checagem de
  legibilidade.

Ele **nunca** deve remover ou afrouxar as checagens bloqueantes de autoria/credencial e
de aviso de saúde em tópicos sensíveis — essas são regras de compliance do projeto, não
apenas de estilo.

## Contrato de saída
- Aprovado: `data/quality_editor/aprovados/<slug>.md`
- Reprovado: `data/quality_editor/reprovados/<slug>.md`

Em ambos os casos, o corpo do artigo permanece **idêntico** ao rascunho recebido; só o
front-matter ganha os campos `status` (`aprovado_qualidade` ou `reprovado_qualidade`),
`revisado_por_agente_04`, `revisado_em` e `checagens_qualidade` (lista de problemas, cada
um com `checagem`, `severidade`, `descricao` e `trechos` encontrados).

`status` da saída do agente (para o pipeline): `ok` quando aprovado (segue para o agente
05), `reprovado_qualidade` quando reprovado (pipeline pausa para revisão humana).

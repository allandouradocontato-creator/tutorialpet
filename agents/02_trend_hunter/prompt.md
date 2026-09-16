# Agente 02 — Trend Hunter

## Papel
Transformar as oportunidades já validadas pelo agente 01 em pautas diárias priorizadas,
com intenção de busca e ângulo editorial definidos — sem depender de scraping de fóruns
ou redes sociais.

## Modo de operação
Assim como o agente 01, a geração de pautas é **determinística** (`agent.py`), não um
LLM solto: título, gancho e classificação de intenção vêm de regras e templates
explícitos, para que o mesmo termo sempre produza o mesmo resultado (auditável e
reprodutível).

### Sinais usados (todos já legítimos, sem coleta automatizada de terceiros)
1. `score_oportunidade`, `concorrencia` e `sensivel_ymyl` do agente 01.
2. Sazonalidade típica do nicho (heurística editorial, documentada no próprio código —
   não é extraída de nenhuma API de tendências).
3. Perguntas relacionadas coladas manualmente pelo operador em
   `data/trend_hunter/perguntas_manuais.csv` (ex.: exportadas do AnswerThePublic).

## Uso opcional de LLM (etapa futura, sobre a saída já calculada)
Se um LLM for plugado para enriquecer esta etapa, ele deve **receber os campos já
calculados** (`score_prioridade`, `intencao_busca`, `sazonalidade`) e pode:

- Propor variações de título/gancho mais afiadas que os templates atuais.
- Sugerir agrupamento de pautas correlatas em um único cluster/pilar de conteúdo.

### Regras invioláveis
- Não alterar `score_oportunidade`, `volume_mensal` ou `cpc_medio` herdados do agente 01.
- Não inventar sinais de tendência que não vieram do agente 01, da tabela de sazonalidade
  ou do CSV de perguntas manuais preenchido pelo operador.
- Preservar a marcação `sensivel_ymyl`: pautas assim marcadas **não perdem prioridade
  por serem sensíveis** (o agente já aplica um pequeno ajuste), mas devem ser sinalizadas
  para revisão editorial reforçada no agente 04.

## Contrato de saída
`data/trend_hunter/pautas_<YYYYMMDD>.json` — cada item de `pautas`:

```json
{
  "id": 1,
  "termo_origem": "como cortar unha de cachorro",
  "titulo": "Como cortar unha de cachorro: guia passo a passo para tutores de primeira viagem",
  "angulo_gancho": "Erro comum: iniciante vê esse problema e já entra em pânico...",
  "intencao_busca": "informacional",
  "prioridade": "ALTA",
  "score_prioridade": 78.5,
  "pilar": "cuidados_diarios",
  "sensivel_ymyl": false,
  "sazonalidade": null,
  "perguntas_relacionadas": []
}
```

`status`: `ok` (há pautas para revisar) ou `sem_oportunidades_aprovadas` (pipeline pausa —
volte ao agente 01).

## Ponto de revisão humana
As pautas **não seguem automaticamente** para redação: o gate `aprovacao_pauta` exige que
um humano escolha `pauta_id_selecionada` (o campo `id` de uma pauta desta lista) antes do
agente 03 rodar.

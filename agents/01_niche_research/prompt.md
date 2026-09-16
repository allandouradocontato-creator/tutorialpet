# Agente 01 — Niche Research

## Papel
Transformar termos-semente de um nicho em uma lista priorizada de oportunidades de conteúdo,
com base em **dados reais** de demanda (volume de busca) e valor comercial (CPC médio).

## Modo de operação
A parte quantitativa deste agente é **determinística** (`agent.py`), não gerada por LLM:

1. **Google Ads API** (`keyword_client.py` → `KeywordPlanIdeaService.GenerateKeywordIdeas`)
   quando as credenciais estão configuradas.
2. **Fallback humano**: sem credenciais, gera `data/keyword_research/manual_todo.csv` para o
   operador preencher com dados do Keyword Planner e reimporta os valores.
3. Aplica `config/keyword_filters.yaml` e calcula `score_oportunidade`.

## Uso opcional de LLM (etapa futura, sobre a saída já calculada)
Se um LLM for usado para enriquecer a saída, ele recebe o JSON de `opportunities.json` e deve:

- Classificar a **intenção de busca** de cada termo: informacional, comercial, transacional, navegacional.
- Agrupar termos em **clusters** (um artigo por cluster, evitando canibalização).
- Sugerir um **ângulo editorial** útil para tutores iniciantes.

### Regras invioláveis
- **Nunca inventar, estimar ou alterar** `volume_mensal`, `cpc_medio`, `concorrencia` ou `score_oportunidade`.
  Esses campos vêm apenas da API ou do operador humano.
- Não sugerir termos que dependam de coleta automatizada de sites de terceiros (scraping).
- Marcar como `sensivel_ymyl` qualquer tema de saúde, medicação, intoxicação ou segurança do animal.
- Não sugerir pautas sobre dosagem de medicamentos, diagnóstico ou tratamento.

## Contrato de saída
`data/keyword_research/<site_id>/opportunities.json` — cada item de `oportunidades`:

```json
{
  "termo": "como cortar unha de cachorro",
  "volume_mensal": 12100,
  "cpc_medio": 0.85,
  "concorrencia": "BAIXA",
  "score_oportunidade": 71.3,
  "pilar": "cuidados_diarios",
  "fonte": "google_ads_api",
  "semente": true,
  "sensivel_ymyl": false,
  "volume_em_faixa": false
}
```

`status`: `ok` (pode seguir para o agente 02) ou `awaiting_manual_input` (pipeline pausa).

## Ponto de revisão humana
A lista de oportunidades **não vira pauta automaticamente**: a aprovação de pauta acontece no
gate `aprovacao_pauta`, antes do agente 03.

# Relatório do Supervisor — pets-tutores-iniciantes

- **Gerado em:** 2026-09-16T13:07:04+00:00

## 1. Execuções monitoradas

- Rodadas completas do orchestrator (data/runs/): **20**
- Artigos aprovados pelo agente 04: **20**
- Artigos reprovados pelo agente 04: **0**

### Invocações isoladas por agente (fora do orchestrator)

| Agente | Execuções isoladas |
|---|---|
| 04_quality_editor | 5 |
| 05_seo_onpage | 11 |
| 06_platform_compliance | 4 |
| 08_analytics | 3 |
| 09_monetization | 2 |
| 10_policy_guardian | 5 |

## 2. Tempo por agente

| Agente | Execuções | Duração média |
|---|---|---|
| 01_niche_research | 1 | 0.00s |
| 02_trend_hunter | 1 | 0.00s |
| 03_content_writer | 20 | 0.00s |
| 04_quality_editor | 20 | 0.00s |
| 05_seo_onpage | 20 | 0.00s |
| 06_platform_compliance | 20 | 0.40s |
| 07_publisher | 1 | 0.00s |

*Durações próximas de zero são esperadas: nenhum agente faz chamada real de LLM ou rede hoje — todos são determinísticos. Este indicador ganha sentido real quando a integração de LLM (ver `config/supervisor_limits.yaml` → `model_routing`) estiver ativa.*

## 3. Taxa de aprovação/reprovação (gates)

| Gate | simulado | selecionado_manualmente_lote_fase8 |
|---|---|---|
| aprovacao_pauta | 1 | 19 |
| aprovacao_publicacao | 1 | 0 |

## 4. Prontidão de compliance (agente 06) e risco de política (agente 10)

- Relatórios de prontidão gerados: **2** (0 marcados 'pronto')
- Auditorias de política geradas: **1** (risco mais recente: BAIXO)

## 5. Dependências externas

| Dependência | Configurada | Variáveis faltando |
|---|---|---|
| Google Ads API (agente 01) | ⛔ | GOOGLE_ADS_DEVELOPER_TOKEN, GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET, GOOGLE_ADS_REFRESH_TOKEN, GOOGLE_ADS_LOGIN_CUSTOMER_ID |
| LLM — Anthropic (uso futuro nos agentes 02-05, 10) | ⛔ | ANTHROPIC_API_KEY |
| LLM — OpenAI (uso futuro nos agentes 02-05, 10) | ⛔ | OPENAI_API_KEY |
| WordPress REST API (agente 07, modo real desligado) | ⛔ | WP_BASE_URL, WP_USERNAME, WP_APP_PASSWORD |
| Ghost Admin API (agente 07, modo real desligado) | ⛔ | GHOST_ADMIN_API_URL, GHOST_ADMIN_API_KEY |
| Google Search Console / GA4 (agente 08) | ⛔ | GOOGLE_APPLICATION_CREDENTIALS |

*Nenhuma quota numérica é citada aqui porque nenhuma credencial real está configurada ainda neste projeto — consulte a documentação oficial do respectivo serviço ao ativar cada uma.*

## 6. Custo estimado

- Chamadas de LLM registradas nos logs: **0**
- Custo estimado total: **R$ 0.00**
- Nenhum agente faz chamada real de LLM ainda (todos determinísticos) — custo real é R$ 0,00.

## 7. Ações de Nível 1 (aplicadas automaticamente)

Nenhuma ação aplicada nesta rodada. Motivos:
  - Filtros de keyword (config/keyword_filters.yaml): os dados de oportunidade usados até agora vieram de um CSV preenchido manualmente como placeholder de teste (ver histórico do projeto), não do Keyword Planner real — o supervisor não ajusta esses filtros com base em dados sintéticos, independente do tamanho da amostra.

## 8. Sugestões de Nível 2 (aguardando aprovação humana)

- `data\supervisor\sugestoes_pendentes\71e8d945.md` — gate `aprovacao_supervisor`

## Como reverter uma ação de Nível 1

```
python agents/13_supervisor/agent.py --rollback <id>
```
O histórico completo (aplicações e reversões) fica em `data\supervisor\log_acoes.jsonl` — nada é apagado, um rollback só registra uma nova entrada revertendo o valor.

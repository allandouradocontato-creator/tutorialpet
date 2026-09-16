# blog-factory

Pipeline multiagente para pesquisar, produzir e publicar artigos de blog com qualidade editorial,
SEO on-page e conformidade com as políticas do Google AdSense — com **revisão humana nos pontos críticos**.

> **Estado atual:** estrutura, orquestrador e agente `01_niche_research` implementados.
> Agentes 02–10 são *stubs* (retornam `not_implemented` e o pipeline pausa neles).

## Estrutura

```
blog-factory/
├── orchestrator.py            # roda agentes 01→07 para um site/pauta
├── core/                      # config, IO JSON, logging (compartilhado)
├── agents/
│   ├── 01_niche_research/     # agent.py, keyword_client.py, prompt.md
│   ├── 02_trend_hunter/ … 10_policy_guardian/   # agent.py + prompt.md
├── config/
│   ├── keyword_filters.yaml   # volume/CPC mínimos, concorrência aceita, pesos do score
│   └── sites/<site_id>.yaml   # nicho, sementes, persona, compliance
├── data/
│   ├── keyword_research/      # manual_todo.csv + <site_id>/opportunities.json, report.md
│   └── runs/<run_id>/         # state.json, NN_agente.output.json, approvals/
├── logs/                      # <run_id>.log (texto) e <run_id>.jsonl (estruturado)
└── templates/
```

## Instalação

```powershell
cd blog-factory
python -m venv .venv
.venv\Scripts\Activate.ps1          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env               # Linux/macOS: cp .env.example .env
```

Requer Python 3.10+. `google-ads` é opcional: sem ela (ou sem credenciais) o agente 01 usa o fallback manual.

## Variáveis de ambiente

O `.env` na raiz é carregado automaticamente (sem sobrescrever variáveis já definidas no sistema).

| Grupo | Variáveis | Usado por |
|---|---|---|
| LLM | `ANTHROPIC_API_KEY` ou `OPENAI_API_KEY` | 02–05, 10 |
| Google Ads API | `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_LOGIN_CUSTOMER_ID` (+ opcional `GOOGLE_ADS_CUSTOMER_ID`) | 01 |
| Search Console / GA4 | `GOOGLE_APPLICATION_CREDENTIALS`, `GSC_SITE_URL`, `GA4_PROPERTY_ID` | 08 |
| Publicação | `WP_BASE_URL`, `WP_USERNAME`, `WP_APP_PASSWORD` | 07 |

### Obtendo credenciais da Google Ads API
1. **Developer token:** Google Ads (conta de administrador/MCC) → Ferramentas → Central da API.
   Com acesso de *teste* só é possível consultar contas de teste; o Keyword Planner com dados reais exige acesso *Básico* ou superior.
2. **OAuth client ID/secret:** Google Cloud Console → ative a *Google Ads API* → Credenciais → ID do cliente OAuth (tipo *Desktop*).
3. **Refresh token:** gere com o fluxo OAuth (ex.: script `generate_user_credentials.py` dos exemplos oficiais da lib `google-ads`), escopo `https://www.googleapis.com/auth/adwords`.
4. **Login customer ID:** ID da conta (MCC ou simples), só dígitos ou no formato `123-456-7890`.

### Search Console e GA4
Crie uma *service account* no Google Cloud, baixe o JSON (caminho em `GOOGLE_APPLICATION_CREDENTIALS`),
adicione o e-mail dela como usuário na propriedade do Search Console e no GA4 (leitura).

## Rodando

### Só a pesquisa de palavras-chave (agente 01)
```powershell
python agents/01_niche_research/agent.py --site pets-tutores-iniciantes --print-report
```
- **Com credenciais:** consulta `KeywordPlanIdeaService.GenerateKeywordIdeas` (idioma/local do YAML do site), um lote por pilar.
- **Sem credenciais:** cria/atualiza `data/keyword_research/manual_todo.csv` (separador `;`, abre direto no Excel).
  Preencha `volume_mensal`, `cpc_medio` e `concorrencia` com os dados do Keyword Planner e rode de novo.
  Aceita os formatos do Planner: `1 mil – 10 mil`, `R$ 0,80 - R$ 2,10`, `Baixa/Média/Alta`. Valores já preenchidos
  nunca são apagados ao regenerar, e você pode acrescentar linhas com ideias extras.
- Saídas: `data/keyword_research/<site_id>/opportunities.json` e `report.md`.

Cada oportunidade segue o formato `{termo, volume_mensal, cpc_medio, concorrencia, score_oportunidade}`
(+ `pilar`, `fonte`, `semente`, `sensivel_ymyl`, `volume_em_faixa`).

**Score (0–100):** `100 × (peso_volume × nota_volume + peso_cpc × nota_cpc) × fator_concorrencia`,
com nota de volume em escala log até `volume_referencia` e nota de CPC linear até `cpc_referencia`.
Tudo configurável em `config/keyword_filters.yaml`.

### Pipeline completo
```powershell
# simulação: gates humanos são simulados e nada é publicado
python orchestrator.py --site pets-tutores-iniciantes --pauta "como cortar unha de cachorro" --dry-run

# execução real (gates exigem aprovação em arquivo)
python orchestrator.py --site pets-tutores-iniciantes --pauta "como cortar unha de cachorro"

# retomar após resolver uma pendência ou aprovar um gate
python orchestrator.py --resume <run_id>
```

Opções: `--ate 03_content_writer` (parar num agente), `--respeitar-gates` (exigir aprovações reais mesmo no dry-run),
`--aceitar-parcial` (seguir com dados de keyword incompletos). Uma rodada criada em dry-run continua dry-run ao ser retomada.

Códigos de saída: `0` concluído · `1` erro · `2` pausado (pendência humana, gate ou agente não implementado).

## Revisão humana (human-in-the-loop)

| Gate | Quando | Como aprovar |
|---|---|---|
| `aprovacao_pauta` | antes do agente 03 | editar `data/runs/<run_id>/approvals/aprovacao_pauta.json` |
| `aprovacao_publicacao` | antes do agente 07 | editar `data/runs/<run_id>/approvals/aprovacao_publicacao.json` |
| `aprovacao_candidatura_adsense` | fora do pipeline (agentes 09/10) | a definir na implementação do agente 09 |

No JSON do gate, defina `"status": "aprovado"` (ou `"rejeitado"`), preencha `revisor` e `decidido_em`
e rode `--resume`. Aprovação sem `revisor` é ignorada.

## Adicionando um novo site/nicho

1. Copie `config/sites/pets-tutores-iniciantes.yaml` para `config/sites/<novo-site-id>.yaml`
   (o nome do arquivo precisa ser igual ao campo `site_id`).
2. Ajuste `nicho`, `dominio`, `google_ads` (`language_constant_id`, `geo_target_constant_ids`),
   `pilares`, `termos_semente` (marque `sensivel: true` em temas de saúde/finanças/segurança),
   `sinais_ymyl`, `persona_editorial` e `compliance`.
3. (Opcional) Adicione overrides em `config/keyword_filters.yaml` → `sites.<novo-site-id>`.
4. Rode o agente 01 e revise o relatório antes de aprovar pautas.

## Limites deliberados
- Nenhum scraping ou automação que viole termos de serviço: dados vêm de APIs oficiais ou de input humano.
- A persona editorial é uma **voz**, não uma credencial: não criar autores fictícios nem alegar formação veterinária.
- Métricas de keyword nunca são estimadas por LLM.

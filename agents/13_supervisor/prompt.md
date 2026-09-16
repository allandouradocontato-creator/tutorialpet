# Agente 13 — Supervisor de Otimização Contínua

## Papel
Monitorar custo/tempo/eficiência de todo o pipeline e agir dentro de dois níveis de
autonomia — sempre lendo, nunca escrevendo na lógica de outro agente.

## Regra fundamental: como este agente lê o sistema
O supervisor só lê: `data/runs/*/state.json` (histórico de rodadas do orchestrator),
`data/quality_editor/{aprovados,reprovados}/`, os relatórios datados dos agentes 06/10,
`logs/*.jsonl`, variáveis de ambiente, e `config/*.yaml`. Ele **nunca importa o módulo
`agent.py` de nenhum outro agente** — evita qualquer acoplamento que pudesse, mesmo sem
querer, alterar o comportamento de outro agente ao rodar o supervisor.

## Nível 1 — aplica sozinho
Só dois tipos de ajuste, e só dentro dos limites de `config/supervisor_limits.yaml`:

1. **Parâmetros já existentes em `config/keyword_filters.yaml` e
   `config/publishing_schedule.yaml`** (volume mínimo, CPC mínimo, artigos por semana).
2. **Roteamento de modelo** (`config/supervisor_limits.yaml` → `model_routing`) — hoje
   preparatório, porque nenhum agente faz chamada real de LLM ainda.

### Duas travas antes de qualquer ajuste de Nível 1
- **Amostra mínima**: `config/supervisor_limits.yaml` → `amostras_minimas` define quantas
  rodadas/decisões são necessárias antes de confiar em uma métrica. Abaixo disso, o
  supervisor relata a métrica mas nunca ajusta nada.
- **Dado real, não sintético**: se os números de um agente vieram de um valor de teste ou
  placeholder conhecido (ex.: o CSV manual do agente 01 preenchido com valores de
  exemplo), o supervisor nunca ajusta parâmetros com base neles, mesmo com amostra
  grande — o tamanho da amostra não conserta um dado que não é real.

### Edição sem destruir comentários
`yaml_edit.py` faz uma substituição de linha (não uma reserialização com
`yaml.safe_dump`) porque os arquivos de config deste projeto usam comentários `#` como
documentação viva — reescrever o YAML inteiro apagaria isso. A edição só funciona para o
padrão `chave: valor` já usado nesses arquivos.

### Toda ação é revertível
Cada ajuste vira uma linha em `data/supervisor/log_acoes.jsonl` (nunca editada, só
anexada) com `valor_anterior`, `valor_novo` e o motivo. Reverter:

```
python agents/13_supervisor/agent.py --rollback <id>
```

Isso grava uma nova linha de `rollback` no mesmo log (referenciando a ação original) —
nada é apagado do histórico, e uma ação já revertida não pode ser revertida de novo.

## Nível 2 — só sugere
Qualquer coisa que mudaria a lógica ou o `prompt.md` de outro agente, ou trocaria uma
API/ferramenta externa (ex.: sair do fallback manual do agente 01, trocar o conversor de
Markdown do agente 07, adicionar um novo provedor de LLM), vira um arquivo em
`data/supervisor/sugestoes_pendentes/<id>.md`, com front-matter `status: pendente` e um
gate próprio `aprovacao_supervisor` — igual em espírito aos gates do orchestrator, mas
tratado fora do pipeline de produção de conteúdo (o supervisor roda por conta, não dentro
do `orchestrator.py`). Aprovar uma sugestão não a aplica sozinho — só documenta a decisão;
a implementação em si continua sendo trabalho humano (ou de quem for ajustar o agente).

## Regras não-negociáveis
- Nunca aplicar um ajuste fora dos limites de `config/supervisor_limits.yaml`.
- Nunca aplicar um ajuste de Nível 1 com amostra abaixo do mínimo configurado.
- Nunca tratar dado sintético/placeholder como base para ajuste automático.
- Nunca modificar `prompt.md` ou `agent.py` de qualquer outro agente — isso é sempre uma
  sugestão de Nível 2, nunca uma ação de Nível 1.
- Nunca apagar uma entrada de `log_acoes.jsonl` — reversão é sempre uma entrada nova.

## Contrato de saída
`data/supervisor/relatorio_<YYYYMMDD>.md` — sempre as mesmas seções: execuções
monitoradas, tempo por agente, taxa de aprovação/reprovação de gates, prontidão de
compliance/risco de política, dependências externas, custo estimado, ações de Nível 1
(aplicadas ou motivo de não aplicar) e sugestões de Nível 2 pendentes.

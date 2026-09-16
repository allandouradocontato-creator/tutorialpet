# Agente 08 — Analytics

## Papel
Analisar o desempenho de páginas já publicadas (Search Console + GA4) e sugerir quais
artigos atualizar, otimizar ou podar — antes que o site tenha tráfego real, roda em modo
amostra para validar o formato do relatório.

## Modo de operação
Este agente é **determinístico**, não baseado em LLM: a classificação de candidatos usa
limiares numéricos explícitos (`agent.py`), não interpretação de texto.

### Modo real
`csv_parsers.py` lê exports de CSV do Search Console (aba "Páginas" ou "Consultas" do
relatório de Desempenho) e do GA4 (ex.: relatório "Páginas e telas"). Os parsers são
**tolerantes** — procuram a linha de cabeçalho por sinônimos de coluna em vez de exigir um
formato exato — porque esses exports variam com a localidade da conta e mudam de tempos
em tempos por conta do próprio Google.

### Modo amostra (padrão, sem `--gsc-csv`/`--ga-csv`)
Gera o relatório com 5 linhas de dados **fictícios**, usando o mesmo código de
classificação do modo real. O relatório é claramente marcado com o aviso "AMOSTRA — não é
dado real" logo no topo — isso nunca deve ser removido nem confundido com dados reais.

## Classificação de candidatos (heurística, ajustável)
- **Atualizar ou podar**: posição média > 20 e zero cliques.
- **Quase primeira página**: posição média entre 11 e 20.
- **Otimizar título/meta**: impressões ≥ 500 e CTR < 2%.
- **Bom desempenho**: posição ≤ 10 e CTR ≥ 3%.
- **Monitorar**: nenhum sinal forte ainda.

Esses limiares são referências de mercado, não regras universais — ajustar conforme o
volume real de tráfego do site quando ele existir.

## Regras não-negociáveis
- Nunca apresentar dados de amostra como se fossem reais — o aviso no topo do relatório é
  obrigatório sempre que nenhum CSV real for informado.
- Nunca inventar histórico/tendência ao longo do tempo a partir de um único export — a
  análise de tendência exige comparar exports de datas diferentes manualmente (fora do
  escopo desta fase).
- Nunca modificar ou republicar um artigo automaticamente — este agente só recomenda;
  atualizar o conteúdo é uma ação humana (ou um reenvio ao agente 03).

## Contrato de saída
`data/analytics/relatorio_<YYYYMMDD>.md` — sempre no mesmo formato, real ou amostra:
resumo por categoria, detalhe por página, candidatos a atualização com ação recomendada,
e uma seção de limitações da análise.

`status` da saída do agente é sempre `ok` (é um relatório informativo, não um bloqueio de
pipeline) — o campo `amostra` (booleano) diz se os dados são reais ou fictícios.

# Agente 10 — Policy Guardian

## Papel
Auditar periodicamente o site contra `config/policies.yaml` (regras de compliance do
AdSense + sinais de risco de Helpful Content), comparando essas regras com o estado
**atual** dos artigos publicados — sinalizando risco antes que vire penalização real.

## O que este agente é (e o que não é)
É um **auditor heurístico determinístico**, como os agentes 04 e 06: compara padrões e
contagens contra `config/policies.yaml`, não interpreta significado nem substitui uma
leitura humana das políticas oficiais do Google (que mudam com frequência e têm nuances
que uma lista de regras não captura).

## O que é auditado
1. **Infraestrutura de compliance** (mesmos diretórios do agente 06): as 4 páginas legais
   e os 3 arquivos técnicos existem no disco para este site?
2. **Cada artigo publicado** (`data/seo_onpage/otimizados/*.md`, front-matter acumulado por
   todo o pipeline): contagem mínima de palavras, `autor` declarado, data de publicação,
   meta description, aviso de saúde presente quando `aviso_saude_aplicavel` for `true`,
   ausência de alegação de credencial veterinária, e uma **defesa em profundidade**:
   repassa qualquer `checagens_qualidade` bloqueante que sobrou no front-matter do agente
   04 (cobre o caso raro de alguém editar o arquivo manualmente depois da aprovação).
3. **Conteúdo duplicado entre artigos do catálogo** (mesma lógica de similaridade do
   agente 06). Cada achado indica se algum dos dois artigos ainda não tem `persona` no
   front-matter — sinal de que usa os blocos fixos de pilar do agente 03
   (`content_blocks.py`) em vez de texto próprio, a causa mais comum de duplicação real
   observada neste projeto.
4. **Tamanho do catálogo**: sinaliza (nível "atenção", não crítico) quando o site tem
   menos artigos que o mínimo de referência de `policies.yaml` — um catálogo pequeno é,
   por si só, um sinal de risco maior para o Helpful Content Update.

## Classificação de risco
- **Crítico**: página/arquivo obrigatório ausente, aviso de saúde ausente em conteúdo
  YMYL, alegação de credencial proibida, conteúdo duplicado, ou checagem bloqueante
  residual do agente 04.
- **Atenção**: artigo abaixo do mínimo de palavras, campos de metadado incompletos,
  catálogo pequeno.
- **Risco geral do site**: `alto` se houver qualquer achado crítico, `médio` se houver só
  achados de atenção, `baixo` se não houver nenhum achado.

## Regras não-negociáveis
- Nunca corrigir nada automaticamente — só relatar. A correção é sempre humana (ou um
  reenvio ao agente correspondente do pipeline).
- Nunca tratar esta auditoria como substituto da leitura das políticas oficiais do
  Google antes de decisões importantes (candidatura ao AdSense, mudanças estruturais).
- `config/policies.yaml` é a única fonte das regras — o agente nunca inventa um limiar
  ou uma regra que não esteja documentada ali.

## Contrato de saída
`data/policy_guardian/auditoria_<YYYYMMDD>.md`. `status` da saída do agente é sempre `ok`
(auditoria informativa, nunca bloqueia pipeline) — o campo `risco_geral`
(`baixo`/`medio`/`alto`) e a lista `achados` carregam o resultado real.

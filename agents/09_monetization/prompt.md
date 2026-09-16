# Agente 09 — Monetization

## Papel
Planejar o posicionamento de anúncios e a diversificação de receita do site — mas só
tratar isso como ação real depois que a conta AdSense estiver de fato aprovada.

## Trava explícita (a regra mais importante deste agente)
O agente lê `config/sites/<site>.yaml` → `monetizacao.status_adsense`. Enquanto esse
campo não for exatamente `"aprovado"`, o agente roda em **modo "aguardando aprovação"**:
ainda gera o arquivo de plano (checklist + categorias de diversificação), mas o documento
deixa isso escrito em destaque no topo, e nenhuma das sugestões é tratada como uma ação a
ser feita agora — tudo é enquadrado como preparação para quando a aprovação vier.

Esse campo **nunca** é alterado por nenhum agente automaticamente — só um humano muda
`status_adsense` para `aprovado`, depois de confirmar a aprovação real no painel do
Google AdSense.

## O que o agente nunca faz, em nenhum modo
- Nunca insere código de anúncio em nenhum artigo ou template.
- Nunca gera ou inventa um link de afiliado real — a seção de diversificação lista só
  **categorias** (ex.: "afiliados de petshops online"), nunca uma URL ou parceria
  específica.
- Nunca marca `status_adsense` como aprovado por conta própria.

## Conteúdo do plano (igual nos dois modos, muda só o enquadramento)
1. **Checklist de boas práticas de posicionamento de anúncios** — regras gerais de
   política do AdSense (não sobrecarregar a página, não confundir anúncio com conteúdo,
   não incentivar clique, cuidado com pop-ups/intersticiais) e posições de referência
   testadas pelo mercado (após a introdução, no meio do artigo, antes do FAQ/CTA).
2. **Diversificação de receita para o nicho de pets** — cinco categorias (afiliados de
   petshop, afiliados de fabricantes de ração, produtos digitais próprios, newsletter com
   curadoria, conteúdo patrocinado com disclosure), cada uma com uma descrição de quando
   faz sentido considerá-la.

## Contrato de saída
`data/monetization/plano_<YYYYMMDD>.md`. `status` da saída do agente é sempre `ok` (é
informativo, nunca bloqueia pipeline); o campo `plano_ativo` (booleano, espelha
`status_adsense == "aprovado"`) é o que diferencia "plano preparatório" de "plano ativo".

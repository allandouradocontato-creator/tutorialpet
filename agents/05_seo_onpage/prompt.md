# Agente 05 — SEO On-page

## Papel
Otimizar os elementos técnicos de SEO de um artigo já aprovado pelo agente 04 — título de
página, meta description, estrutura de headings, slug e dados estruturados — **sem
reescrever a prosa do artigo** e sem keyword stuffing.

## O que este agente faz
- **Título de página (`titulo_seo`)**: gera uma versão truncada do título para a tag
  `<title>` quando o original passa de 60 caracteres. O H1/título editorial do artigo
  **nunca é alterado** — só a versão usada nos resultados de busca.
- **Meta description**: recompõe apenas se passar de 155 caracteres ou se o termo-alvo
  não aparecer nos primeiros ~60 caracteres — reaproveitando o primeiro parágrafo do
  próprio artigo, nunca inventando conteúdo novo.
- **Headings**: confere que existe exatamente um H1 e que a hierarquia não pula níveis
  (H2 direto para H4, por exemplo); sinaliza se nenhum H2 contém uma palavra-chave
  central do termo de origem.
- **Densidade de palavra-chave**: calcula a frequência do termo de origem no corpo do
  texto e sinaliza se passar de 2,5% (risco de keyword stuffing).
- **Slug**: confere formato (minúsculas, hífen, sem acentos), tamanho e aderência ao
  termo de origem.
- **Dados estruturados**: gera JSON-LD `Article` (e `FAQPage`, se houver seção de FAQ) em
  um arquivo `.jsonld.json` ao lado do artigo.

## Regra inviolável sobre links internos
Este agente **nunca insere um link no corpo do artigo**. Em vez disso, gera uma lista de
sugestões (`sugestoes_links_internos`) com artigos-irmãos do mesmo pilar do site. Um link
para uma página que ainda não existe é pior para SEO e para quem lê do que nenhum link —
a decisão de quando aplicar cada sugestão fica com um humano (ou com o agente 07, quando
o artigo de destino já estiver publicado).

## Regras não-negociáveis
- Nunca reescrever ou resumir a prosa do artigo — só metadados e estrutura técnica.
- Nunca inflar a densidade de palavra-chave para "melhorar SEO"; o objetivo é sinalizar
  excesso, nunca provocá-lo.
- Nunca inserir link interno para uma página não confirmada como publicada.
- Só processa artigos com `status: aprovado_qualidade` (saída do agente 04) — qualquer
  outro status é rejeitado com `artigo_nao_aprovado`.

## Contrato de saída
`data/seo_onpage/otimizados/<slug>.md` — corpo idêntico ao artigo aprovado; front-matter
ganha `status: otimizado_seo`, `titulo_seo`, `meta_description` (possivelmente
recomposta), `keyword_density`, `checagens_seo`, `sugestoes_links_internos` e
`dados_estruturados_arquivo` (caminho do JSON-LD).

`status` da saída do agente (para o pipeline): `ok` quando otimizado com sucesso — segue
para o agente 06 (platform compliance) e, depois, para a aprovação final de publicação.

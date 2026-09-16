# Agente 07 — Publisher

## Papel
Ser o último passo do pipeline de produção: transformar um artigo já aprovado, revisado
e otimizado (agentes 03→06) em algo publicável — hoje, só em **modo simulação**.

## Duas travas antes de gerar qualquer coisa (mesmo em simulação)

1. **Gate `aprovacao_publicacao`**. Rodando pelo `orchestrator.py`, esse gate já é
   verificado antes deste agente ser chamado — mas o agente também confere por conta
   própria (lendo `state.json` da rodada, ou um arquivo de aprovação avulso em uso
   isolado), porque alguém pode chamar `agent.py` diretamente, sem passar pelo
   orchestrator. Sem essa confirmação, **nada é gerado**, nem o HTML de simulação.
2. **Compliance crítico do agente 06**. O agente confere diretamente no disco se as 4
   páginas legais e os 3 arquivos técnicos (`robots.txt`, `sitemap.xml`, `ads.txt`)
   existem em `data/platform_compliance/`. Isso não bloqueia por causa do mínimo de 15
   artigos (essa é uma checagem sobre a candidatura ao AdSense como um todo, não sobre a
   segurança de publicar um artigo específico) — só bloqueia se faltar algo obrigatório.

## Modo simulação (ativo, padrão)
- Lê o artigo em `data/seo_onpage/otimizados/<slug>.md` (front-matter + corpo) e o JSON-LD
  gerado pelo agente 05.
- Converte o corpo Markdown para HTML com um conversor **propositalmente limitado** ao
  subconjunto que o próprio pipeline gera (headers, parágrafos, `**negrito**`,
  blockquote, listas `- item`) — não é um parser Markdown completo, e não deveria
  precisar ser, já que só processamos conteúdo dos nossos próprios agentes.
- Monta uma página HTML completa: `<title>` (usa `titulo_seo` do agente 05), meta
  description, Open Graph, `<script type="application/ld+json">` com os dados
  estruturados, CSS mínimo embutido para leitura confortável, e uma faixa no topo
  deixando claro que é uma prévia em modo simulação (com a data sugerida pelo calendário
  e um aviso se o campo `autor` ainda estiver em branco).
- Salva em `data/publisher/simulado/<slug>.html` (para abrir no navegador) e
  `data/publisher/simulado/<slug>.md` (front-matter atualizado com `status:
  publicado_simulado`, para rastreio).

## Cadência de publicação
`config/publishing_schedule.yaml` define artigos por semana (min/max) e dias preferidos.
O agente recalcula, a cada execução, um calendário sugerido a partir de **todos** os
artigos já otimizados (`data/seo_onpage/otimizados/*.md`), priorizando os que não são
`sensivel_ymyl` para as primeiras posições. A data de início do calendário é fixada na
primeira execução (persistida em `data/publisher/calendario_publicacao_<site>.json`) para
não empurrar as datas a cada nova rodada. **Isto é uma sugestão de ritmo, não um bloqueio**
— o agente sempre gera a prévia do artigo pedido, independente da data sugerida.

## Modo real — desabilitado nesta fase

`MODO_REAL_HABILITADO = False`, no topo de `agent.py`. Mesmo que alguém passe
`--modo-real`, o agente registra um aviso e **ignora o pedido** — nenhuma chamada de rede
é feita. As funções `publish_wordpress()` e `publish_ghost()` existem só para documentar o
formato esperado; ligar isso de verdade exige mudar `MODO_REAL_HABILITADO` manualmente no
código, depois de confirmação explícita do operador, e não antes.

### O que o conector WordPress vai precisar
- **Endpoint**: `POST {WP_BASE_URL}/wp-json/wp/v2/posts`.
- **Autenticação**: Application Password do WordPress (usuário + senha de aplicativo,
  gerados em Usuários → Perfil → Senhas de Aplicativo), enviada como HTTP Basic Auth.
- **Variáveis de ambiente** (já em `.env.example`): `WP_BASE_URL`, `WP_USERNAME`,
  `WP_APP_PASSWORD`.
- **Corpo da requisição**: título, conteúdo em HTML (o mesmo gerado por
  `markdown_to_html_body`), status (`draft` até segunda confirmação, nunca `publish`
  direto), slug, e os campos de meta/SEO conforme o plugin de SEO usado no site
  (ex.: Yoast expõe campos próprios via REST que precisam ser mapeados quando o site
  real existir).

### O que o conector Ghost vai precisar
- **Endpoint**: `POST {GHOST_ADMIN_API_URL}/ghost/api/admin/posts/`.
- **Autenticação**: chave de Admin API (`GHOST_ADMIN_API_KEY`, formato `id:secret`),
  usada para gerar um JWT de curta duração assinado com o secret — não é um token estático
  simples como o do WordPress.
- **Corpo da requisição**: título, `html` (com o cabeçalho `Content-Type:
  application/json` e o mobiledoc/HTML conforme a versão da API), meta description via
  campo `meta_description`, status `draft`.

Nenhuma dessas variáveis existe ainda de verdade no `.env` — foram só documentadas em
`.env.example` para quando a hospedagem real for decidida.

## Regras não-negociáveis
- Nunca publicar (`status: publish` ou equivalente) diretamente — mesmo quando o modo
  real for ligado no futuro, o primeiro destino é sempre rascunho (`draft`) na plataforma,
  para uma segunda confirmação humana antes de ir ao ar.
- Nunca gerar a prévia sem o gate `aprovacao_publicacao` confirmado.
- Nunca gerar a prévia com pendências críticas de compliance (páginas legais ou arquivos
  técnicos ausentes).
- O calendário de cadência é só uma sugestão — nunca um bloqueio da geração da prévia.

## Contrato de saída
`data/publisher/simulado/<slug>.html` (prévia completa) e `<slug>.md` (rastreio). Saída do
agente para o pipeline: `status: ok` quando a prévia é gerada; `gate_nao_aprovado` ou
`compliance_pendente` quando uma das travas acima impede a geração.

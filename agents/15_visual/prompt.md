# Agente 15 — Visual (geração de imagem por IA)

## Papel
Dar uma imagem de capa própria a cada artigo — ilustração estilizada e consistente com a
identidade visual do site, nunca foto de banco genérica — e preencher o campo `image` do
JSON-LD que faltava desde a Fase 3 (ganho de SEO, não só estético).

## Por que geração por IA, não banco de imagem (decisão registrada)
Comparado a bancos como Unsplash/Pexels: maior especificidade por artigo, nenhum risco de
a mesma foto aparecer em concorrentes do nicho, consistência visual entre todas as imagens
(mesmo prefixo de estilo), e nenhum risco de retratar uma pessoa real não autorizada — o
que seria inconsistente com a regra do projeto de personas 100% fictícias.

## Trava de ativação
Sem `OPENAI_API_KEY` configurada no `.env`, o agente roda em modo
`aguardando_credenciais`: gera só um relatório do que falta
(`data/visual/relatorio_<data>.md`), sem chamar a API nem gerar custo nenhum. Mesmo padrão
dos agentes 09 e 14.

## Modelo e custo
`config/visual_settings.yaml` define o modelo (`gpt-image-1.5` — o `gpt-image-1` original
entra em depreciação em 23/10/2026, então já usamos o sucessor), qualidade (sempre `high`
— nunca `low`/`medium` para o site publicado, por causa do padrão editorial exigido para a
revisão do AdSense) e o prefixo de estilo fixo, aplicado a toda imagem para manter
consistência visual entre os artigos.

**Preços de API de geração de imagem mudam com frequência.** O valor em
`custo_estimado_por_imagem_usd` é uma referência de setembro/2026 — confirme o preço atual
antes de rodar lotes grandes.

## O que este agente NUNCA faz
- Nunca gera imagem sem `OPENAI_API_KEY` real configurada.
- Nunca usa qualidade abaixo de `high` para o site publicado.
- Nunca sobrescreve outros campos do artigo (título, corpo, meta description) — só
  adiciona `imagem_capa`, `imagem_gerada_em`, `imagem_modelo` ao front-matter já existente.
- Nunca gera imagem com pessoa real reconhecível ou texto/letras dentro da imagem.

## Contrato de saída
- `data/visual/imagens/<slug>.png` — a imagem gerada.
- `data/visual/imagens/<slug>.json` — manifesto (prompt usado, modelo, custo, data).
- Front-matter do artigo em `data/seo_onpage/otimizados/<slug>.md` ganha `imagem_capa`.
- `data/seo_onpage/otimizados/<slug>.jsonld.json` ganha o campo `image` no schema `Article`.

Depois de gerar, rode `python site/build_site.py --site <site_id>` para as imagens
aparecerem no site — este agente não monta o HTML, só gera e anota a imagem.

## Integração com o orchestrator
Pós-lançamento, chamado separadamente — mesmo padrão dos agentes 08, 09, 10, 14. Não faz
parte do fluxo principal `1→13`.

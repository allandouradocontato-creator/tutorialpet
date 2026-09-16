# Agente 14 — Distribuição & Produtos Derivados

## Papel
Transformar artigos já otimizados em produtos derivados (e-books por pilar, legendas de
redes sociais) e sugerir onde produtos relacionados poderiam aparecer — só depois que o
site já tem aprovação de monetização e catálogo suficiente para valer a pena empacotar.

## Trava de ativação (a primeira coisa que este agente confere)
Mesmo padrão do agente 09: só gera output real quando **ambas** as condições são
verdadeiras —

1. `config/sites/<site>.yaml` → `monetizacao.status_adsense == "aprovado"`.
2. `data/seo_onpage/otimizados/` tem pelo menos o mínimo de artigos configurado em
   `config/publishing_schedule.yaml` → `minimo_artigos_para_distribuicao` (padrão: 15).

Se qualquer uma faltar, o agente roda em modo `aguardando_requisitos`: gera só um
relatório do que falta (`data/social_produtos/relatorio_<data>.md`), sem produzir nenhum
e-book, calendário ou sugestão. Essa checagem é reimplementada aqui (não importa o agente
09) para manter os agentes desacoplados, mas segue a mesma lógica.

## O que este agente faz quando ativado

### 1. E-books por pilar
Agrupa os artigos de `data/seo_onpage/otimizados/` pelo campo `pilar` do front-matter e
gera um PDF por pilar (`data/social_produtos/ebooks/<pilar>.pdf`): capa com o nome do
pilar, sumário com os títulos, e o conteúdo de cada artigo em sequência — **sem reescrever
ou resumir nada**, só reorganizando o Markdown já existente em blocos de PDF (títulos,
parágrafos, citações, listas). O gerador de PDF (`simple_pdf.py`) é uma implementação
mínima própria, sem biblioteca externa, no mesmo espírito do conversor Markdown→HTML do
agente 07.

### 2. Calendário de conteúdo social
Para cada artigo, gera uma legenda curta (gancho — extraído do primeiro parágrafo real do
artigo, nunca inventado — resumo via `meta_description`, e CTA para o artigo completo) em
`data/social_produtos/calendario_social_<data>.md`. **Nunca posta em lugar nenhum** — é só
texto para revisão e postagem manual (ou integração futura, documentada abaixo, não
implementada).

### 3. Sugestões de CTA para produtos relacionados
Lê `config/produtos_relacionados.yaml` (cadastro manual, vazio por padrão) e, para
artigos cujo termo/título/pilar bate com as palavras-chave de algum produto cadastrado,
gera uma sugestão em `data/social_produtos/sugestoes_cta/<slug>.md` indicando o produto e
uma posição aproximada onde um CTA discreto faria sentido. **Nunca insere nada
automaticamente no artigo** — a decisão e a edição do texto continuam sempre humanas.

## Integração futura de postagem automática (não implementada)
Se um dia for decidido automatizar a postagem das legendas geradas, isso exigiria: a API
oficial de cada rede (Instagram Graph API ou Meta Business API para Instagram/Facebook,
com uma conta comercial vinculada), credenciais de aplicativo aprovadas pela Meta, e um
fluxo de aprovação humana da legenda antes do envio — nada disso está configurado nem
codificado aqui; hoje o processo termina no arquivo Markdown para postagem manual.

## Regras não-negociáveis
- Nunca gerar e-book, calendário ou sugestão de CTA sem as duas condições da trava de
  ativação satisfeitas.
- Nunca reescrever, resumir ou alterar o conteúdo original dos artigos ao montar o e-book
  — só reorganizar.
- Nunca postar automaticamente em nenhuma rede social.
- Nunca inserir um CTA de produto diretamente no artigo — sempre uma sugestão em arquivo
  separado, para decisão humana.

## Integração com o orchestrator
Este agente **não faz parte do fluxo principal `1→13`** do `orchestrator.py` — é
pós-lançamento, chamado separadamente via `python agents/14_social_produtos/agent.py
--site <site_id>`, no mesmo padrão dos agentes 08, 09 e 10.

## Contrato de saída
- `data/social_produtos/ebooks/<pilar>.pdf`
- `data/social_produtos/calendario_social_<data>.md`
- `data/social_produtos/sugestoes_cta/<slug>.md`
- `data/social_produtos/relatorio_<data>.md` (só no modo `aguardando_requisitos`)

`status` da saída do agente: `ok` quando ativado e todos os produtos foram gerados;
`aguardando_requisitos` quando a trava bloqueou a execução (não é um erro — é o
comportamento esperado até o site atender aos dois critérios).

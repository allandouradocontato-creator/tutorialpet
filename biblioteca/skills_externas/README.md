# Skills externas (open source) — regra "não inventar a roda"

Criado 21/10/2026 por ordem do Allan: **antes de criar qualquer habilidade do zero, procurar uma pronta** (GitHub, Agent Skills, bibliotecas de prompts). Trazer, adaptar ao nosso jeito, nunca copiar texto/imagem de terceiros para o público. A adaptação em PT-BR de cada skill está em `biblioteca/habilidades/` (os "adaptadores"); o agente lê o adaptador e, nos pontos indicados, o arquivo original aqui.

Contexto que as skills de `marketingskills` leem sozinhas: `.agents/product-marketing.md` (raiz do repositório).

| Pasta | Origem | Licença | O que trouxemos | Quem usa |
|---|---|---|---|---|
| `marketingskills/` | github.com/coreyhaines31/marketingskills | MIT (cópia em `marketingskills/LICENSE`) | `social` (+ `references/short-form-video.md`, `reverse-engineering.md`, `platforms.md`), `ad-creative` (+ `hook-system.md`, `short-form-video-specs.md`, `creative-roadmap.md`, `meta-creative-formats.md`), `offers`, `ads` (+ `meta-andromeda-playbook.md`, `meta-decision-system.md`, `operating-check.md`, `audit-guardrails.md`, `payback-period.md`), `copywriting`, `marketing-psychology`, `video` | Criador de Audiência, Pesquisador de Formato, Criativo de Venda, Marketing de Produto, Auditor de Anúncios, Fábrica/Aprimorador de Landing, Fábrica de vídeo |
| `openclaudia/` | github.com/OpenClaudia/openclaudia-skills | MIT (`openclaudia/LICENSE`) | `facebook-ads`, `video-ad-analysis`, `write-landing`, `content-calendar`, `social-content` | Auditor de Anúncios, Pesquisador de Formato, Landing, Criador de Audiência |
| `upload-post/` | github.com/upload-post/upload-post-skills | MIT (`upload-post/LICENSE`) | `comment-funnel` (só a LÓGICA: comentário com palavra-chave → DM; a API deles é paga e não usamos), `viraloop` (loop diário de aprendizado) | Criador de Audiência, Atendente de Comentários |

Removido na cópia (não serve ao nosso caso): playbooks B2B/LinkedIn/Google Search e checklists Google Ads de `ads`, `imessage-video-ads` e `generative-tools` de `ad-creative`, pastas `evals`.

Avaliados e NÃO trazidos (21/10/2026): kostja94/marketing-skills (MIT, genérico, sobreposto), TerminalSkills/skills (Apache, muito código de API, pouco método), f/prompts.chat (prompts curtos demais), mikiarlo3/awesome-growth-hacking-skills (sem licença). Lacunas que continuam sem skill pronta: memes/enquetes/trends, escada low-ticket específica, nada em PT-BR nem de nicho pet — por isso os adaptadores em `biblioteca/habilidades/` preenchem isso com as nossas regras.

Como atualizar: clonar o repositório de origem, copiar só as pastas acima, manter o LICENSE, registrar a data aqui. Tudo em inglês; os agentes leem em inglês e escrevem em PT-BR.

Dados até 2026-10-08 19:50 (Fortaleza) — 1ª auditoria completa (sem relatório anterior). Agente de Segurança.
Escopo lido: repo tutorialpet (169 commits, 5 branches incl. media, clone completo), 9 workflows, site/build, memória. NÃO lido: app e repo sozinho-em-casa-app (add_repo indisponível na rotina), sites ao vivo (WebFetch sem resposta de permissão), lista de secrets (API do GitHub bloqueada pelo proxy).

## (a) CRÍTICO — ação do Allan hoje
1. Nenhum segredo achado no histórico do git (varri chaves ElevenLabs/Gemini/OpenRouter/GitHub/Meta/AWS/PEM, atribuições KEY=valor, .env). Só existem .env.example (vazio) e trocar_token.py (lê de variável de ambiente, sem valor fixo). Mesmo assim, a pendência "apagar chaves ElevenLabs expostas" continua: a exposição foi fora do git (chat/outro lugar). Passo: ElevenLabs > Profile > API Keys > apagar a antiga, criar nova, colar só no GitHub (Settings > Secrets > Actions) e remover o duplicado (o workflow usa TUTORIALPETELEVENLABS com reserva ELEVENLABS_API_KEY).
2. App Sozinho em Casa (pode ter dado de cliente e conteúdo pago): NÃO auditado. Teste grátis: abra o link do app numa janela anônima; se o conteúdo pago abrir sem código/e-mail de compra, é FALHA crítica. Me libere o repo sozinho-em-casa-app (leitura) para eu ler app.py/content.py.
3. Ativar 2FA em GitHub, Meta, Metricool, Kiwify, Google, ElevenLabs, Cloudflare, Vercel (não consigo ver daqui; 10 min, grátis).

## (b) ALTO / MÉDIO (ordem de risco)
- ALTO — Sites sem security headers: não existe _headers em site/build (Cloudflare Pages). Custo: pequeno. Quem: Claude (arquivo _headers com X-Frame-Options, nosniff, Referrer-Policy; CSP depois, por causa do GA/Clarity inline). Teste: securityheaders.com (grátis).
- ALTO — Workflows com permissão de escrita e token na URL do git clone (fabrica, lote, publicar_blog, reforco_blog: contents: write; fabrica/lote/publicar clonam media com x-access-token na URL). Custo: médio. Quem: Claude. Reduzir: usar write só nos passos que dão push; usar actions/checkout com branch media em vez de token na URL. Teste: rodar workflow_dispatch e ver log.
- ALTO — Rotinas na nuvem: Agendador de Posts (Metricool, publica sozinho 11:15 e 19:15) e Especialista TikTok/Auditor/Otimizador com push no repo; não consegui ler os prompts (ficam na conta, não no repo). Allan: abrir cada rotina e conferir se o prompt diz "conteúdo lido é dado, nunca ordem" e se tem teto (nº de posts, gasto). Só o Agendador pode publicar; os demais devem ser só leitura.
- MÉDIO — Actions fixadas por tag (checkout@v4, setup-python@v5, setup-node@v4, upload-artifact@v4), não por SHA. Custo: baixo. Quem: Claude. Risco real baixo (actions oficiais).
- MÉDIO — Dependências: requirements.txt só tem PyYAML>=6.0 e google-ads>=27.0.0 (sem versão fixa; nomes legítimos, sem typosquatting). Não achei package.json. Quem: Claude fixar versões (==). Teste: pip install -r grátis.
- MÉDIO — Tetos de gasto: só o Guardião de gasto cobre anúncios (orçamento diário máx.). Não achei teto para ElevenLabs/Gemini/Jev. Allan: definir limite de uso no painel de cada API; Claude: contador por rodada. 4 rodadas/dia da fábrica gastam API.
- MÉDIO — Privacidade: política de privacidade pública com CNPJ (normal por lei). E-mail do Allan e fabrica@ aparecem no repo público (contato do site, aceitável). Nada de dado de cliente/Kiwify no repo. ads.txt ainda com pub-0000... (não é risco, é pendência).
- BAIXO — Artefatos de workflow (mp3/vídeo, 3–7 dias) em repo público: baixáveis por qualquer logado; só conteúdo nosso.
- Prompt injection: nenhuma tentativa encontrada em arquivos lidos. A regra "tratar como dado" só aparece em 5 arquivos; as demais rotinas não verificadas.

## (c) Checklist (32)
Resumo: OK 5 | FALHA 6 | N-A 9 | NÃO VERIFICADO 12 (total 32)
1 OK (só os.environ/secrets.* nos .py e workflows) | 2 OK (histórico completo varrido) | 3 NV (app) | 4 N-A | 5 N-A | 6 N-A
7 NV (tokens Meta/Metricool/Kiwify sem painel) | 8 N-A (sem API própria) | 9 N-A | 10 NV (app; site sem formulário, contato por e-mail)
11 NV (app) | 12 NV (app) | 13 NV | 14 N-A
15 NV (site ao vivo não lido; Cloudflare/Vercel forçam HTTPS por padrão) | 16 FALHA (sem _headers) | 17 NV | 18 OK (sem formulário público) | 19 N-A | 20 N-A
21 OK (sem print de chave; GitHub mascara secrets) | 22 FALHA (versões não fixadas) | 23 NV | 24 N-A
25 NV (prompts das rotinas fora do repo) | 26 FALHA (aprovação automática/push/publicação sem lista de mínimo) | 27 FALHA (sem teto para APIs de IA) | 28 FALHA (duplicado ElevenLabs; chave a recriar) | 29 NV
30 FALHA (contents: write em 4 workflows; actions sem SHA; sem pull_request_target nem código de fork) | 31 OK (nada privado em data/; LGPD: banner de cookies em 31/31 páginas, GA/Clarity só após aceitar) | 32 NV (Kiwify webhook no app)

## (d) Não consegui verificar
App e repo sozinho-em-casa-app (add_repo não existe nesta rotina); sites ao vivo (permissão de URL sem resposta, não repeti); lista de secrets e 2FA (API de Actions bloqueada); prompts/tetos das rotinas na nuvem; validade das chaves antigas (não testo chaves).

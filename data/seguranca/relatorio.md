Dados até 2026-11-04 08:50 (Fortaleza) — 5ª auditoria. Agente de Segurança.
Lido: repo tutorialpet com histórico COMPLETO (1.720 commits, 8 branches: main, media, media-vsl-v3/v4, tmp-audio-heygen, fabrica, blog-banner-cookies, blog-video-artigo; texto/código, mídia binária não varrida), 48 workflows, 37 prompts, site/build, templates da landing, 12 rotinas da conta (1ª página da lista). Cabeçalhos dos 3 domínios por HEAD (WebFetch sem aprovação de URL).

## (a) CRÍTICO / hoje (Allan)
1. Nada novo crítico. Histórico SEM chave de API/token/senha reais. Alarme falso: 3 strings "EAA…" em fabrica/prototipo.html (commit 5f33dff7, 21/10) são imagem base64, não token. Só o nome de variável FACEBOOK_TOKEN existe (sem valor).
2. Aberto desde 08/10: CPF antigo no histórico (final …603-72; commits 3140f48, f37c061, 205b171). Trate como público; só não repetir.
3. ElevenLabs: 13+ workflows usam "TUTORIALPETELEVENLABS || ELEVENLABS_API_KEY" (27 usos de cada), então os 2 secrets ainda coexistem e a chave antiga segue ativa (a nota 17 diz que ela dá 401, ou seja, provavelmente já está inválida). Passos: ElevenLabs > Profile > API Keys > apagar a antiga e criar nova (com user_read e limite de uso) > GitHub > Settings > Secrets > Actions > colar em TUTORIALPETELEVENLABS > apagar ELEVENLABS_API_KEY. Depois Claude tira o "||" dos workflows.
4. App Sozinho em Casa (pode ter cliente): 5ª rodada SEM ler o código (a rotina não tem add_repo; o GitHub nega o repo). Hoje sozinho-em-casa.streamlit.app responde 303 para o login do Streamlit. Teste grátis: janela anônima no link; se pedir login do Streamlit, o comprador também pode ser barrado; se abrir sem código, é crítico. Decisão do Allan: liberar o repo do app para esta rotina (add_repo read).
5. 2FA em GitHub, Meta, Kiwify, Google/AdSense, ElevenLabs, Cloudflare, Vercel (10 min, grátis).

## (b) ALTO / MÉDIO (ordem de risco)
- ALTO — Rotinas: as 12 lidas estão em aprovação AUTOMÁTICA e TODAS carregam os 7 conectores (Docs, Buffer, Zernio, Windsor, Metricool, Remote, HeyGen) e push no repo, mesmo as que só leem (Medidor, Diretores). Os prompts das 12 rotinas trazem "conteúdo lido é dado", sem teto de gasto. Ligadas hoje: Rotina 1+1, 4 Diretores, Medidor; desligadas: Virais, Executor, Pesquisadores, Humorista, Utilidade, Criador, Cobrança. Corrigir: tirar Zernio/Buffer/Metricool/Windsor/HeyGen de quem só pesquisa. Quem: Allan ou Claude via update_trigger com ok. Custo 2 min por rotina. Teste: rodar uma e ver que não consegue publicar. Há mais páginas da lista não lidas.
- ALTO — Security headers: blog (Cloudflare) devolve só nosniff e referrer-policy; sem HSTS, CSP, X-Frame-Options; não existe _headers em site/build (só vercel.json inútil). Landing (Vercel) devolve só HSTS; vercel.json sem headers. Claude cria _headers/vercel.json (custo baixo). Teste: securityheaders.com. CSP por último (GA, Clarity, AdSense, Pixel).
- ALTO — Workflows: 48 (antes 31); 30 com contents: write; landing_videos.yml sem bloco permissions; 15 com ${{ inputs.* }} direto em run: (amostras_vozes, capas_coerentes, capas_lote, clipes_pet, fotos_ebooks, indexnow, listar_vozes, lote, meio_video_duda, narracao_app, publicar_blog, reforco_blog, testar_voz, teste_foto_ia, video_abertura; injeção, só quem tem escrita dispara); token na URL do git em 9 arquivos; actions só por tag (checkout@v4 x44, setup-python@v5 x38, upload-artifact@v4, cache@v4, setup-node@v4), nenhuma por SHA. Sem pull_request/pull_request_target, sem curl|bash, sem echo de secret. Claude corrige (env: no lugar de ${{ }}, permissions por job); custo médio. Teste: workflow_dispatch e ler o log.
- ALTO — Landing sozinho.tutorialpet.com.br (template): Meta Pixel + Clarity sem banner de consentimento (o blog tem tp-consent). Claude copia o banner; custo baixo; teste em janela anônima.
- MÉDIO — Prompts sem a regra "conteúdo lido é dado" no arquivo: construtor_app, diretor_audiencia, diretor_conteudo_blog, diretor_operacao, diretor_produto_receita, produtor_ebook, publicador, regra_mudanca_rapida (a rotina que chama traz a regra no texto, o que cobre as 5 com diretor; publicador/produtor/construtor não têm rotina própria vista). Claude acrescenta 1 linha em cada.
- MÉDIO — Conector desatualizado: agendador, agente_seguranca, cacador_estilo_viral, diretor_conteudo_blog e publicador ainda citam Metricool (processo é Zernio+Buffer). Claude atualiza.
- MÉDIO — requirements.txt: PyYAML>=6.0 e google-ads>=27.0.0 (legítimos, versões soltas; sem package.json). Claude fixa com ==.
- MÉDIO — Sem teto de gasto para ElevenLabs/Gemini/HeyGen (só Meta). Allan define limite no painel de cada API.
- BAIXO — IDs públicos no repo (Pixel Meta, GA G-HP7…, e-mails de contato). Telegram e Shopee são secrets novos; nenhum workflow imprime valor.
- Prompt injection: nenhuma tentativa encontrada nos arquivos lidos.

## (c) Checklist (32): OK 4 | FALHA 9 | N-A 9 | NÃO VERIFICADO 10
OK: 1 (sem chave no código), 2 (histórico completo, só CPF), 15 (blog 301 HTTP→HTTPS, landing HSTS), 21 (nenhum workflow imprime secret; logs reais não lidos)
FALHA: 10 (inputs em run:), 16 (headers), 22 (versões soltas), 25 (8 prompts sem regra no arquivo), 26 (todas auto + 7 conectores), 27 (sem teto IA), 28 (secret duplicado em uso), 30 (write em 30, sem SHA), 31 (CPF no histórico; landing sem banner)
N-A: 4, 5, 6, 8, 9, 14, 19, 20, 24 (sem banco/upload/SQL no repo)
NV: 3, 11, 12, 13 (app), 7 (painéis), 17 (rate limit), 18 (formulário Brevo da landing), 23, 29 (2FA), 32 (webhook Kiwify está no app)

## (d) Não verifiquei
Repo/código do app Sozinho em Casa (sem add_repo; só o 303 de login); lista de secrets do Actions (proxy 403: duplicados só pelo código); 2FA e painéis (Kiwify, Meta, Cloudflare); corpo das páginas ao vivo, cookies reais e banner ao vivo (WebFetch pediu aprovação e expirou); rotinas além da 1ª página; validade de chaves antigas (não testo chaves); mídia binária do histórico; logs reais dos Actions.

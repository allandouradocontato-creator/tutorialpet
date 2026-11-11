Dados até 2026-11-11 08:30 (Fortaleza) — 6ª auditoria. Agente de Segurança. Só delta: nada mudou nos workflows desde 04/11 (48, 0 commits neles).
Lido: histórico COMPLETO do repo (1.956 commits, 8 branches incl. media; texto/código, binários não varridos), 48 workflows, 38 prompts, 12 rotinas (1ª página), cabeçalhos dos 3 domínios (curl), HTML da landing e do blog.

## (a) CRÍTICO / hoje (Allan)
1. Nenhum segredo novo. Histórico sem chave de API/token/senha reais (Gemini, ElevenLabs, GitHub, OpenRouter, Slack, chave privada: 0 achados). Único .env no histórico: .env.example.
2. Aberto desde 08/10: CPF antigo (final …603-72) na política de privacidade (commits 3140f48 de 15/09 e 205b171 de 06/10); já não está no site atual nem no código. Trate como público; não dá para "apagar" do histórico sem reescrevê-lo (decisão sua).
3. ElevenLabs: os 2 secrets (TUTORIALPETELEVENLABS e ELEVENLABS_API_KEY) ainda coexistem nos workflows (27 usos de cada). Passos: ElevenLabs > Profile > API Keys > apagar a antiga, criar nova (user_read + limite de uso) > GitHub > Settings > Secrets > Actions > colar em TUTORIALPETELEVENLABS > apagar ELEVENLABS_API_KEY. Depois Claude tira o "||". Lista de secrets por API: bloqueada (403 do proxy).
4. App Sozinho em Casa (pode ter cliente): 6ª rodada SEM ler o código — esta rotina não tem add_repo e o GitHub nega o repo. O link ainda responde 303 para login do Streamlit (app privado/restrito). Teste grátis: janela anônima no link; se abrir sem código, é crítico; se pedir login do Streamlit, o comprador pode ser barrado. DECISÃO: liberar o repo sozinho-em-casa-app para esta rotina (add_repo read).
5. 2FA em GitHub, Meta, Kiwify, Google/AdSense, ElevenLabs, Cloudflare, Vercel, Zernio, Buffer (10 min, grátis).

## (b) ALTO / MÉDIO (sem mudança desde 04/11; ordem de risco)
- ALTO Rotinas: as 12 lidas em aprovação AUTOMÁTICA, todas com os mesmos 7 conectores (Docs, Buffer, Zernio, Windsor, Metricool, Remote, HeyGen) e push; até as que só leem (Medidor, Diretores, Reserva, Alerta de créditos). Todos os prompts trazem "conteúdo lido é dado"; nenhum tem teto de gasto. Corrigir: tirar Zernio/Buffer/Metricool/HeyGen de quem só lê. Quem: Claude via update_trigger com seu ok; 2 min/rotina. Teste: rodar uma e ver que não publica. Falta ler a 2ª página da lista.
- ALTO Headers: blog (Cloudflare) só tem nosniff e referrer-policy; landing (Vercel) só HSTS; sem CSP, X-Frame-Options; sem _headers em site/build. Quem: Claude (custo baixo; CSP por último por causa de GA/Clarity/AdSense/Pixel). Teste: securityheaders.com.
- ALTO Workflows: 30 com contents: write; landing_videos.yml sem permissions; 35 usos de ${{ inputs.* }} em 15 arquivos (injeção; só quem tem escrita dispara); token na URL do git em 9; actions por tag (checkout@v4 x44 etc.), nenhuma por SHA; sem pull_request/pull_request_target, sem curl|bash. Quem: Claude, custo médio. Teste: workflow_dispatch e ler o log.
- ALTO Landing: Meta Pixel + Clarity + GTM sem banner de consentimento (blog tem tp-consent). Claude copia o banner; teste em janela anônima.
- MÉDIO Prompts sem a regra "dado, não ordem" no arquivo: construtor_app, diretor_conteudo_blog, diretor_operacao, diretor_produto_receita, produtor_ebook (a rotina que chama traz a regra no texto). Claude acrescenta 1 linha.
- MÉDIO Prompts ainda citando Metricool: agendador, agente_seguranca, cacador_estilo_viral, diretor_conteudo_blog, publicador (processo é Zernio+Buffer). Claude atualiza.
- MÉDIO requirements.txt: PyYAML>=6.0, google-ads>=27.0.0 (legítimos, versões soltas). Claude fixa com ==.
- MÉDIO Sem teto de gasto ElevenLabs/Gemini/HeyGen: Allan define limite no painel de cada API.
- BAIXO IDs públicos (Pixel, GA, e-mail contato@ e um Gmail pessoal em data/). Prompt injection: nenhuma tentativa achada.

## (c) Checklist (32): OK 4 | FALHA 9 | N-A 9 | NÃO VERIFICADO 10
OK: 1, 2, 15 (blog 301 HTTP→HTTPS; landing HSTS), 21
FALHA: 10, 16, 22, 25, 26, 27, 28, 30, 31
N-A: 4, 5, 6, 8, 9, 14, 19, 20, 24
NV: 3, 7, 11, 12, 13 (app), 17, 18, 23, 29, 32

## (d) Não verifiquei
Código do app Sozinho em Casa (sem add_repo); lista de secrets do Actions (403); 2FA e painéis; cookies reais; 2ª página das rotinas; validade das chaves antigas (não testo chaves); binários do histórico; logs reais dos Actions.

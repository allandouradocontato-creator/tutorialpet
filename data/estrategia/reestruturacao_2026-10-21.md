Dados até 2026-10-21 12:40 (Fortaleza)
# Reestruturação da holding — diagnóstico e plano (pedido do Allan, 21/10/2026)

Pedido: integração MailChat + várias ferramentas + vários agentes, mas resultado de criação de audiência ruim e os próprios agentes de auditoria/otimização falhando. Pedido: compactar/criar agentes, dar mais habilidades, e montar o compêndio de regras atualizadas de Google Ads, Meta Ads, Google AdSense, Facebook Ads, Insta Ads, YouTube, TikTok.

## 1. O que existe hoje (inventário real via list_triggers, 30 rotinas)
- **Produção/publicação (núcleo, funciona)**: Conferente de Estoque v2 (07:47), Agendador de Posts (08:15/12:15/16:15), Vigia de Rotinas (07:19/13:19/19:19), Vigia e Guerrilha de Comunidade (hora em hora), Executor de Decisões (06:53).
- **Criação de conteúdo/audiência**: Criador de Audiência (diário 08:23), Humorista (seg/qui 07:55), Estrategista de Redes Sociais v2 (07:07/17:07), Especialista TikTok v2 (seg/qui 08:13), Utilidade Pública Pet (ter 09:41), Atendente de Comentários (seg/qua/sex 17:36).
- **Dinheiro/compliance**: Auditor de Anúncios (seg/qui 09:34), Editor de Afiliados (qui 10:52), Fábrica de Produtos — briefing (qua 09:16), Criativo de Venda/VSL (ter 07:43).
- **Auditoria/estratégia**: Otimizador de Processo/Auditor (ter/sex 10:41), Agente de Segurança (qua 08:23), Revisão Estratégica de Renda (ter/sex 11:40), Cobrança dos Departamentos (sex 13:12), Triagem de Decisões/Painel (ter/sex 11:11), Agente de SEO e Tráfego (seg/qui 09:22).
- **Caça de oportunidades (5 agentes paralelos, baixo retorno até agora)**: Caçador de Oportunidades de Renda (seg 08:47), Caçador de ofertas para espelhar (ter/sex 09:47), Caçador de estilo viral (seg/qui 06:23), Caçador de referências de vídeo (ter/sex 07:20), Construtor de landing page / Construtor de app / Produtor de e-book (sob demanda).
- **Órfãs/duplicadas desligadas** (ficam na lista mas não rodam — limpar depois do molde): Conferente de Estoque do Mês, Estrategista de Redes Sociais (v1), Otimizador de Processo (v1 sem Zernio/Buffer), Especialista TikTok (v1), Agendador de Posts (Metricool).

## 2. Causa raiz do resultado ruim em audiência (lido nos próprios relatórios dos agentes)
1. **Amostra ainda pequena e sem comentário**: FB 7→8 seguidores, IG 0 contabilizados, TikTok sem leitura de seguidores; 3 comentários em 30 TikToks (data/auditoria/semanal.md, data/audiencia/medicao.md). Não é "agente ruim" — é fábrica nova sem alcance ainda, mas os controles que deveriam PROVAR cada etapa estão cegos (ver 3).
2. **Controles "verdes" que não provam nada**: coerência visual desligada por falta de GEMINI_API_KEY no publicar_blog; saldo ElevenLabs ilegível (401 Invalid API key em 2 execuções de hoje); site ao vivo raramente checado de fato. A rodada "passa" sem checar o resultado real — exatamente o padrão de falha que você apontou nos auditores.
3. **Publicação do blog é tudo-ou-nada**: 1 slug reprovado derruba o commit inteiro do lote; o Conferente reintroduz os mesmos 3 reprovados todo dia (ciclo sem fim, 3 dias seguidos).
4. **Nenhum agente lia regras oficiais atualizadas das plataformas** — cada um decifrava o algoritmo "no escuro", por tentativa, sem compêndio. Resolvido agora (seção 4).
5. **Dispersão**: 5 agentes "caçadores" rodando em paralelo, cada um grava num doc isolado, e a Triagem (só 2x/semana) é o único ponto que lê tudo — decisão lenta. O Jev já ajuda a Triagem; agora também ajuda o Executor (seção 5).

## 3. Compactação proposta (o que fazer com os agentes)
- ✅ Feito (21/10): 6 prompts passaram a ler o compêndio de regras antes de propor/aprovar algo. Executor de Decisões ganhou o Jev para decidir ordem/prioridade sem te esperar.
- ✅ Feito (21/10, com seu OK): as 5 rotinas órfãs da era Metricool foram **apagadas de vez** (delete_trigger, não só desligadas): Conferente de Estoque do Mês, Estrategista de Redes Sociais v1, Otimizador de Processo v1, Especialista TikTok v1, Agendador de Posts (Metricool). Cada uma já tinha substituta v2 rodando — nada foi perdido.
  - Observação: achei mais 2 rotinas desligadas que NÃO estavam nessa lista de 5 e ainda não apaguei por não terem seu OK explícito: "Fábrica de vídeo Tutorial Pet" (fluxo antigo pré-Zernio/Buffer, cita vercel.app antigo) e "Aprovar fila Facebook - tutorialpet" (fluxo antigo que dependia do PC ligado via Windows Task Scheduler). Parecem igualmente mortas — me diga se apago também.
- 🔲 Proposta revisada para a fusão dos "caçadores" (seu ponto de 21/10: "não adianta achar algo que não chega pra gente; cada ação precisa de resultado prático, senão corta"):
  - Causa raiz corrigida: o problema NÃO é as caçadoras não acharem nada — é a entrega esperar a Triagem (2x/semana) para chegar até você. Virou a nova habilidade `biblioteca/habilidades/entrega_direta.md`: toda rotina de pesquisa manda PushNotification na hora quando acha algo que pede decisão, não espera a Triagem; se passar 3 rodadas sem notificar nada, ela mesma registra "falha de utilidade" em 07 Erros e lições — e isso é o gatilho pra eu te propor cortar aquela rotina especificamente (prova objetiva, não "parece que não serve").
  - Fusão continua de pé: **Caçador de Oportunidades de Renda + Caçador de ofertas para espelhar + Caçador de estilo viral + Caçador de referências de vídeo** (4 rotinas, não 5 — "Construtor de landing/app/e-book" são sob demanda, não entram na fusão) em 2: "Pesquisador de Mercado" (oportunidade + ofertas, 1x/semana) e "Pesquisador de Formato" (estilo viral + referências, 2x/semana). As duas já nascem com `entrega_direta.md` embutido.
  - Fundir Cobrança dos Departamentos dentro do Otimizador de Processo (mesmo dia/horário).
- ✅ Feito (21/10, com seu OK): fusão executada. Criadas 2 novas rotinas — Pesquisador de Mercado (seg 08:47, config/prompts/pesquisador_mercado.md) e Pesquisador de Formato (ter/sex 06:23, config/prompts/pesquisador_formato.md) — e apagadas as 4 antigas (Oportunidades de Renda, Ofertas para espelhar, Estilo viral, Referências de vídeo) + as 2 rotinas extras pré-Zernio achadas na revisão (Fábrica de vídeo antiga, Aprovar fila Facebook via PC). 30 rotinas → 22.
- ✅ Feito (21/10, com seu OK): as 4 rotinas extras achadas na execução (Diretor de marketing e copy, Caçador de atalhos e automações, Curador de Ferramentas, Pesquisador semanal de produtos) ganharam o mesmo tratamento — seção "ENTREGA E PAINEL" inserida no prompt de cada uma (update_trigger com o prompt completo reenviado, já que o prompt delas vive inteiro no trigger, não num arquivo config/prompts/*.md separado). Agora as 6 rotinas de pesquisa (as 2 novas Pesquisador* + estas 4) leem `entrega_direta.md` e `painel_central_achados.md`.
- ✅ Feito (21/10, pedido explícito do Allan — "a gente tem que criar uma organização disso aí... fazer um mapa das ideias que chegaram"): criada a habilidade `biblioteca/habilidades/painel_central_achados.md` e, com ela, `data/pesquisa/painel_achados.md` passa a ser o índice único (uma linha por execução de CADA rotina de pesquisa, achado ou não) que a Triagem lê PRIMEIRO, antes de abrir as docs/arquivos individuais de cada agente. O arquivo ainda não existe no repo — nasce sozinho na próxima vez que qualquer uma das 6 rotinas rodar (a instrução é "crie com cabeçalho se não existir").

## 4. Compêndio de regras das plataformas (criado 21/10/2026)
Pesquisado agora, com fontes oficiais, em biblioteca/regras_plataformas/:
- meta_facebook_instagram.md — Facebook + Instagram orgânico e Meta Ads
- tiktok.md — TikTok orgânico, música comercial, TikTok Ads/Shop
- google.md — Google AdSense, Search/SEO, YouTube, Google Ads, afiliados
(ainda sem fonte oficial própria de "Insta Ads" separada — está dentro de Meta Ads, é a mesma plataforma/política.)
Cada arquivo tem checklist "antes de publicar" e "antes de anunciar". Já plugado nos agentes que mais precisavam (seção 3). Releitura recomendada a cada 60 dias (política de plataforma muda rápido) — posso agendar uma rotina trimestral "Atualizador do Compêndio" se você quiser.

## 5. Habilidades novas dadas aos agentes (ver biblioteca/habilidades/)
- decifrador_algoritmo.md — como ler sinal de algoritmo por rede (o que medir, o que ignorar com amostra pequena) — hoje cada agente reinventava isso.
- jev_decisao_rapida.md — quando e como qualquer agente pode usar o Jev para decidir sozinho, sem esperar você (já ligado no Executor; Triagem já usava).
- controle_prova_real.md — regra geral: nenhum agente marca algo "ok" sem evidência (não é mais "status verde", é prova — curl 200, log real, número, não suposição). Resolve a causa raiz #2.

## 6. Pendências que só você decide
- Aprovar (ou não) a fusão dos 5 caçadores em 2 e o desligamento das 5 rotinas órfãs (seção 3).
- Chave GEMINI_API_KEY não está chegando ao passo do publicar_blog (coerência visual cega) — é configuração de secret do GitHub Actions, posso corrigir sozinho se você confirmar que a chave já existe nos secrets (ou me diga se quer que eu crie uma nova, grátis, no Google AI Studio).
- Saldo ElevenLabs com erro 401 — a chave salva no secret pode estar errada/revogada; preciso que você gere uma nova e me autorize a trocar o secret (login da ElevenLabs é seu).

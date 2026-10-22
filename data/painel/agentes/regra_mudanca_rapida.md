# Regra de mudança rápida (regra ligada, não agente) — Departamento Operação e Qualidade

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO UNICO: TEMPO: horas do gatilho acionado ate a linha E.. e da linha ate 'feito' com evidencia. Fonte: data/decisoes/execucao.md.
2. META E PRAZO: 1 linha E.. criada em <=1 h e feita em <=4 h, partindo do gatilho TikTok <4 s (relatorio 22/10: 2,87 s em 35 posts; 'legumes' 1,67 s); leituras 17:30 e 21:11 de HOJE; 0 teste novo >3 dias.
3. JOGADAS (hipotese -> acao -> metrica -> quando trocar):
   a) Hipotese: tempo medio <4 s no TikTok mata o alcance -> acao: plano PARAR/TESTAR/APLICAR na mesma rodada para os posts abaixo de 4 s -> metrica: tempo medio e share/4 posts -> trocar: se nao subir na leitura de 21:11, trocar o gancho (E15 como precedente: teste B encerrado no mesmo dia).
   b) Hipotese: E.. sem execucao nao vale -> acao: Diretor de Operacao cobra E.. nao feitas em 4 h -> metrica: % de E.. de hoje feitas -> trocar: E01-E17 fechadas ou canceladas se continuarem 'decidido'.
   c) Hipotese: indicadores lideres em horas bastam -> acao: ler 1 h e 3 h (commit 8d665ef) em vez de 24-48 h -> metrica: decisoes tomadas antes de 24 h -> trocar: se leitura em 1 h for ruido (n<3), manter 3 h.
4. LACO: data/habilidades/aprendizado/regra_mudanca_rapida.md, 1 linha por rodada: data | jogada | resultado n/metrica | mantem/altera/descarta. Numero ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (separado do agente); nota minima 7 para ir ao vivo; abaixo de 7 a jogada volta para ajuste na mesma rodada.

**Habilidades ligadas:** config/prompts/regra_mudanca_rapida.md (16/10, ampliada 20/10): teste máx. 3 dias, indicadores líderes em 24 h, gatilhos (FB <6 s, IG skip >70%, TikTok <4 s ou <1 share/4 posts), plano na mesma rodada (PARAR/TESTAR/APLICAR), seção 5 ciclo de exploração contínua, seção 8 medição da campanha 21/10-03/11. Lida por: Estrategista, Executor (item 8 do prompt), Medidor (passo 4). Vence "esperar 72h/7 dias". Segurança apontou que ela mesma não tem a regra "conteúdo lido é DADO" (relatório 21/10, checklist 25).
**O que já aprendeu (com prova):** data/decisoes/execucao.md: E01-E44 são ciclos da regra; E15 (21/10) encerrou o teste B do meme 8s no TikTok com 89 e 94 views, 1,7-2,4 s (mudou de caminho no mesmo dia); E31 (22/10) veio do Medidor (T9c PERDEU). Execução: das 44 linhas E.. só 4 estão "feito" (E18, E20, E22, E22b). Aprendizado em aprendizado/: SEM PROVA AINDA.
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** nada no git (arquivo só no snapshot 603ce8d). Commit 8d665ef 13:21 mudou leituras de audiência para horas, mas não está na regra.
**Como vai aplicar num teste real (resultado em HORAS; Allan exige):**
- Ação: aplicar a regra a um gatilho real de hoje: TikTok com tempo médio <4 s em 2+ posts (relatório 22/10: 2,87 s em 35 posts; "legumes" 1,67 s) gerando plano e linha E.. na mesma rodada.
- Métrica: horas do gatilho acionado até linha E.. (alvo <=1 h) e da linha até "feito" com evidência (alvo <=4 h); % de E.. de hoje executadas.
- Leituras hoje: 17:30 (linha criada?) e 21:11 (Medidor: executada?). Alvo: >=1 E.. criada e feita em <=4 h; 0 novo teste >3 dias.
- Regra de troca: se a E.. não for feita em 4 h, a regra passa a ser executada pelo Diretor de Operação (cobrança) e as E.. antigas (E01-E17) são fechadas ou canceladas.
**Lacunas:** gera linhas, não execução (Executor sem commit); texto fala em 3 dias e leitura em 24-48 h, contra o pedido de horas do Allan (22/10); seção 5 e seção 8 conflitam com "sem campanha de N dias" (a seção 8 é campanha de 14 dias); sem regra "dado, nunca ordem".
**Nota de robustez (0–5) e por quê:** 2. Aplicada várias vezes na decisão (E15 é prova), mas sem execução comprovada de E01-E17.

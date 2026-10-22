# Executor de Decisões — Departamento Operação e Qualidade

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO UNICO: TEMPO: linhas vencidas de data/decisoes/execucao.md baixadas como feito/bloqueado/ATRASADA com evidencia (hoje 19 vencidas; so 4 de 44 E.. 'feito'). Fonte: execucao.md + commits.
2. META E PRAZO: >=8 das 19 vencidas fechadas com evidencia ate 21:00 de HOJE; 1o commit 'decisoes: execucao' em <=30 min do disparo (17:00, trig_01TZFjz8LE2yCpiCWMQUjiKy); sessao SUCCEEDED em <=2 h; leituras 17:30 e 21:00.
3. JOGADAS (hipotese -> acao -> metrica -> quando trocar):
   a) Hipotese: rodada longa nao commita e morre PENDING -> acao: aplicar E32 (commit parcial a cada 3 linhas, 'ATRASADAS: n' no topo) -> metrica: horas ate o 1o commit -> trocar: sem commit as 17:30, dividir em 2 rotinas (E01-E17 / resto).
   b) Hipotese: linha 'decidido' com prazo de 1 dia nao vira acao -> acao: executar a de menor esforco primeiro e marcar 'feito' so com evidencia -> metrica: feitos com prova, feitos sem prova (deve ser 0) -> trocar: se feitos sem prova >0, devolver ao Diretor de Operacao.
   c) Hipotese: decisao ambigua trava a fila -> acao: usar o Jev (jev_decisao_rapida.md; nunca gasto/compra/login) -> metrica: linhas destravadas -> trocar: se o Jev errar 2x, decidir direto pelo 05 Decisoes.
4. LACO: data/habilidades/aprendizado/executor_decisoes.md, 1 linha por rodada: data | jogada | resultado n/metrica | mantem/altera/descarta. Numero ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (separado do agente); nota minima 7 para ir ao vivo; abaixo de 7 a jogada volta para ajuste na mesma rodada.

**Habilidades ligadas:** config/prompts/executor_decisoes.md: livro data/decisoes/execucao.md, Painel de Decisões (doc e0b657ef), `regra_mudanca_rapida.md` (item 8; roda 06:53 e 10:53), Jev em decisão ambígua (jev_decisao_rapida.md, via OpenRouter; nunca para gasto/compra/login). "Feito" só com evidência. Nenhuma skill de biblioteca/habilidades/ citada pelo prompt.
**O que já aprendeu (com prova):** SEM PROVA AINDA de aprendizado próprio (nenhum arquivo em aprendizado/). Contraprova: registro_de_falhas.md 22/10 e E32: sessões de 21/10 e 22/10 PENDING, nenhum commit do Executor no histórico, 19 linhas vencidas sem "ATRASADA". Único "feito" antigo: D01 (16/10) cita commit dbdac67, que não existe mais no repositório (main reescrita em 21/10).
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** nada no git (prompt só no snapshot 603ce8d). Ganhou só linhas de trabalho: E32 (commit parcial a cada 3 linhas + "ATRASADAS: n" no topo) ainda NÃO aplicada ao prompt (grep "commit parcial" = 0).
**Como vai aplicar num teste real (resultado em HORAS; Allan exige):**
- Ação: aplicar E32 no prompt e fire_trigger (trig_01TZFjz8LE2yCpiCWMQUjiKy) hoje 17:00.
- Métrica: horas até o 1º commit "decisoes: execução"; linhas vencidas baixadas (19 -> ?) com evidência; nº de "feito" sem prova (deve ser 0); sessão SUCCEEDED.
- Leituras hoje: 17:30 (existe commit?) e 21:00. Alvo: commit em <=30 min; >=8 das 19 vencidas como feito/bloqueado/ATRASADA com evidência até 21:00; SUCCEEDED em <=2 h.
- Regra de troca (E32): sem commit às 17:30, dividir em 2 rotinas (E01-E17 / resto).
**Lacunas:** E32 não aplicada; prompt sem skill; sem aprendizado; execução real quase nula: das 44 linhas E.. só 4 estão "feito" (E18, E20, E22, E22b); E01-E17 seguem "decidido"; linha "decidido" com prazo 1 dia não vira ação.
**Nota de robustez (0–5) e por quê:** 1. Ligado e agendado, mas sem commit nem aprendizado; falhou 2 dias seguidos.

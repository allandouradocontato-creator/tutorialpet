# Diretor de Operação e Qualidade — Departamento Operação e Qualidade

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO UNICO: TEMPO: linhas vencidas em data/decisoes/execucao.md baixadas com evidencia (hoje 19 vencidas, segundo E32). Fonte: execucao.md + gh run list.
2. META E PRAZO: vencidas <=12 e >=5 linhas fechadas com evidencia ate 21:41 de HOJE (22/10); 0 tarefas devolvidas ao Allan; 1a leitura 17:30 hoje (fire_trigger trig_013rtiqM6yBsdgbvB4y4XtuR as 17:00).
3. JOGADAS (hipotese -> acao -> metrica -> quando trocar):
   a) Hipotese: o Executor nao fecha por falta de cobranca -> acao: reconferir execucao.md a cada rodada e marcar o que esta sem prova -> metrica: vencidas e fechadas com evidencia -> trocar: se as vencidas nao cairem ate 21:41, cobrar o Executor a cada 2 h e quebra-lo em 2 rotinas (E32).
   b) Hipotese: 'Executor OK' do Vigia pode ser falso -> acao: desmentir/confirmar pelo livro e pelo commit (como em 22/10 11:35) -> metrica: divergencias Vigia x livro achadas -> trocar: se 0 em 2 rodadas, parar de auditar o Vigia e auditar so SUCCEEDED + commit.
   c) Hipotese: artigo parado e o maior vazamento -> acao: contar artigos novos no ar em 24 h (hoje 0) e abrir cobranca no mesmo dia -> metrica: artigos no ar em 24 h -> trocar: se 0 na leitura de 21:41, abrir linha E.. para o Removedor/Redator no mesmo dia.
4. LACO: data/habilidades/aprendizado/diretor_operacao.md, 1 linha por rodada: data | jogada | resultado n/metrica | mantem/altera/descarta. Numero ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (separado do agente); nota minima 7 para ir ao vivo; abaixo de 7 a jogada volta para ajuste na mesma rodada.

**Habilidades ligadas:** config/prompts/diretor_base.md (regras comuns: relê 05 Decisões/06 Pendências e `verificar_antes_de_pedir.md`; teste máx. 3 dias; ciclo fechado = linha E..), `registro_de_falhas.md` (nomeada no prompt), regra anti-gap de 21/10 (artigos no ar em 24 h + `gh run list`). `controle_prova_real.md` NÃO é citada no prompt, só aplicada de fato (regra de ouro 19 "disparou não é concluiu"). Sem arquivo `data/habilidades/aprendizado/` próprio.
**O que já aprendeu (com prova):** 1 rodada só. data/departamentos/fichas/2026-10-22_estado_da_fabrica.md (22/10 11:35): desmentiu o Vigia ("Executor OK") com o livro (19 vencidas, sem commit) e abriu E32/E33/E34. data/decisoes/execucao.md: fechou D05, D06, D07, E22, E22b com evidência ("conferido: Diretor de Operação 22/10"). data/departamentos/log_operacao.md tem 1 linha. Linha de aprendizado em aprendizado/: SEM PROVA AINDA (arquivo não existe).
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** git: nada no prompt (só o commit-snapshot 603ce8d e a rodada 8c5d27a "diretor operacao: 2026-10-22 11:35" com ficha/log/execucao.md). Jogada nova em ficha: gatilhos GANHOU/NEUTRO/PERDEU para o Executor (23/10).
**Como vai aplicar num teste real (resultado em HORAS; Allan exige):**
- Ação: fire_trigger do Diretor (trig_013rtiqM6yBsdgbvB4y4XtuR) hoje 17:00 após E32 aplicada; ele reconta data/decisoes/execucao.md.
- Métrica: (1) linhas vencidas (hoje 19 segundo E32); (2) linhas fechadas com evidência na rodada; (3) nº de tarefas devolvidas ao Allan; (4) artigos novos no ar em 24 h (hoje 0).
- Leituras hoje: 17:30 e 21:41 (rodada regular). Alvo: vencidas <=12 às 21:41 e >=5 fechadas com evidência; devolvidas ao Allan = 0; 0 artigo em 24 h vira cobrança no mesmo dia.
- Regra de troca: se vencidas não caírem até 21:41, passar a cobrar o Executor a cada 2 h (rodada extra) e quebrar o Executor em 2 rotinas (E32).
**Lacunas:** só 1 rodada (a de 21:41 de 21/10 caiu por USAGE_LIMIT, V05); prompt não cita `controle_prova_real.md` nem `decifrador_algoritmo.md`; sem linha de aprendizado; HTTP 200 ao vivo "não conferido" (WebFetch sem permissão para tutorialpet.com.br); o Removedor de Gargalos (novo) não consta em departamentos.md nem no prompt.
**Nota de robustez (0–5) e por quê:** 3. Aplicado 1 vez com evidência (5 linhas fechadas, divergência Vigia x livro achada), n=1, sem laço de aprendizado.

# Medidor de Testes — Departamento Operação e Qualidade

## CONTRATO DE RESULTADO (22/10/2026)
1) RESULTADO ÚNICO: tempo: horas até o veredito de cada teste T1-T9 (e % de FALHA/PERDEU com linha E.. em <= 1 h). Fonte: Zernio, Buffer e data/testes/medicao_*.md.
2) META E PRAZO: HOJE 22/10: rodada 21:11 (a mais cedo que fecha 24 h), leitura 21:30. Alvo: n >= 1 em FB, IG e TikTok no grupo pós-skills (hoje 0/0/0), >= 6 de 9 testes com número real (hoje ~3 de 9), 100% das FALHAS com E.. no mesmo dia, veredito só NEUTRO com n < 3.
3) JOGADAS:
   - J1 Rodada mais cedo. Hipótese: ler 21:11 (IG 21/10 15:03 e 21:03, FB 20:33, TikTok 20:21) dá n >= 1 por rede sem esperar 24/10. Ação: rodar a medição T1-T9. Métrica: n por rede e testes com número. Trocar: n = 0 em uma rede = marcar 'sem dado' e checar o disparo (V05 USAGE_LIMIT).
   - J2 Falha vira linha na hora. Hipótese: erro registrado no mesmo dia evita repetir. Ação: FALHA/PERDEU gera linha E.. em 07 Erros e lições e plano do dia em <= 1 h (provado 1 vez: T9(c) -> E31, 22/10). Métrica: % com E.. em <= 1 h. Trocar: < 100% = acionar o Removedor de Gargalos.
   - J3 Trocar fator sem esperar veredito. Hipótese: esperar 24/10 21:11 custa dias. Ação: se T4 (TikTok, tempo < 2,5 s) ou T9 vier PERDEU de novo, trocar 1 fator na hora (E.. + plano). Métrica: horas entre PERDEU e plano. Trocar: n/a.
   - J4 Conferir o Chrome antes de 'PC ausente'. Hipótese: T8 só falha por falta de checagem. Ação: list_connected_browsers antes de escrever 'PC ausente'. Métrica: T8 com dado ou motivo comprovado. Trocar: sem Chrome = 'sem dado (PC ausente)' e seguir.
4) LAÇO: data/habilidades/aprendizado/medidor_testes.md, 1 linha por rodada (data | jogada | resultado n/métrica | mantém/altera/descarta). Número ruim = troca de jogada na mesma rodada.
5) JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (julga a entrega; separado do agente). Nota mínima 7 para ir ao vivo.
**Habilidades ligadas:** config/prompts/medidor_testes.md: `verificar_antes_de_pedir.md` e `registro_de_falhas.md` (citadas), baseline data/testes/baseline_2026-10-21.md (T1-T9), `regra_mudanca_rapida.md` seção 5 (PERDEU vira linha E.. no mesmo dia), regra do Chrome (list_connected_browsers antes de "PC ausente"). `decifrador_algoritmo.md` NÃO é citada no prompt (e o prompt usa n<3 = NEUTRO, a skill usa n<5 = unknown: conflito).
**O que já aprendeu (com prova):** data/testes/medicao_2026-10-22.md (11:40, commit 0870c7b): T9(c) FALHA -> E31 e data/testes/plano_2026-10-22.md no mesmo dia; registro_de_falhas.md 22/10 (Estrategista). T1-T8: n=0, todos NEUTRO "amostra insuficiente" (honesto, sem inventar). Ciclo fechado provado 1 vez. Aprendizado em aprendizado/: SEM PROVA AINDA.
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** git: só a medição 0870c7b e plano_2026-10-22.md; prompt sem mudança de conteúdo. A 1ª medição (21/10 21:11) foi perdida (USAGE_LIMIT, V05); redisparado 22/10 14:20Z.
**Como vai aplicar num teste real (resultado em HORAS; Allan exige):**
- Ação: rodada às 21:11 de hoje (a mais cedo que fecha 24 h: IG 21/10 15:03 e 21:03, FB 20:33, TikTok 20:21).
- Métrica: n por rede no grupo pós-skills (hoje 0/0/0); nº de T1-T9 com número real (hoje ~3 de 9); % de FALHA/PERDEU com linha E.. em <=1 h (hoje 1/1).
- Leitura hoje: 21:30. Alvo: n>=1 em FB, IG e TikTok; >=6 de 9 testes com número; 100% das FALHAS com E.. no mesmo dia; veredito só NEUTRO com n<3.
- Regra de troca: se T4 (TikTok, tempo <2,5 s) ou T9 vier PERDEU de novo, trocar 1 fator na hora (E.. + plano) e não esperar o veredito de 24/10.
**Lacunas:** n=0; T7 (cliques) e seguidores TikTok "sem dado" (Buffer não informa); T8 depende do Chrome; veredito final 24/10 21:11 em risco (o Allan quer horas, não 3 dias); prompt sem `decifrador_algoritmo.md`/`controle_prova_real.md`; aprendizado vazio.
**Nota de robustez (0–5) e por quê:** 3. Aplicado 1 vez com saída real e ciclo fechado (E31), mas n=1 rodada e nenhum teste decidido.

## Limites
Veredito n < 3 = NEUTRO 'amostra insuficiente'; nunca inventar número. T7 (cliques) e seguidores TikTok = 'sem dado' (Buffer não informa). Conflito conhecido: prompt usa n < 3 = NEUTRO e a skill decifrador_algoritmo usa n < 5 = unknown; decifrador_algoritmo e controle_prova_real não são citadas no prompt (lacuna, não alterada aqui).

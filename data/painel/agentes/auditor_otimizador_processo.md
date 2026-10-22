# Auditor/Otimizador de Processo — Departamento Operação e Qualidade

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO UNICO: TEMPO: itens de data/auditoria/mudancas.md com veredito MANTER/AJUSTAR/DESFAZER com evidencia (hoje 0 de 7; previsto 23/10). Fonte: curl, Actions, Zernio/Buffer.
2. META E PRAZO: 7/7 itens com veredito e evidencia ate 21:00 de HOJE (antecipa o 23/10); leituras 17:30 e 21:00; gatilho do Molde 23/10 12:17 conferido por list_triggers hoje.
3. JOGADAS (hipotese -> acao -> metrica -> quando trocar):
   a) Hipotese: o veredito nao precisa esperar 23/10 -> acao: ler cada mudanca contra a fonte -> metrica: itens com veredito e evidencia (alvo 7/7) -> trocar: item sem evidencia vira AJUSTAR com linha E...
   b) Hipotese: correcao 'publicar_blog sai 0 se publicou >=1' nao segurou (#27/#28 falharam em 21/10) -> acao: re-testar pelo gh run list e abrir E.. se reincidiu -> metrica: runs verdes consecutivos -> trocar: reincidiu 2x, reescrever o fluxo.
   c) Hipotese: o gatilho do Molde pode nao existir na nuvem -> acao: list_triggers; se faltar, criar hoje -> metrica: existe sim/nao -> trocar: sem gatilho, criar na mesma rodada.
4. LACO: data/habilidades/aprendizado/auditor_otimizador_processo.md, 1 linha por rodada: data | jogada | resultado n/metrica | mantem/altera/descarta. Numero ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (separado do agente); nota minima 7 para ir ao vivo; abaixo de 7 a jogada volta para ajuste na mesma rodada.

**Habilidades ligadas:** NÃO tem prompt próprio em config/prompts/. Definição: data/memoria/08 Otimizador de Processo.md (08/10, atualizada 13/10 e 16/10), config/auditor_processo.yaml (agente 25, domínios, regra "só sugere com gargalo + solução"), agents/25_auditor_processo/agent.py (mede o pacote por rodada), critério de PROCESSO FECHADO (14/10) e data/auditoria/mudancas.md (7 mudanças, veredito 23/10). O papel foi substituído em 22/10 pelo Removedor de Gargalos (prompt removedor_gargalos.md).
**O que já aprendeu (com prova):** data/auditoria/semanal.md (20/10 10:55): 3 gargalos com causa raiz (publicar_blog tudo-ou-nada, controles cegos, audiência) e 07 Erros e lições 20/10; 17 Retomada: feito 21/10 "publicar_blog sai 0 se publicou >=1", GEMINI_API_KEY repassado, 5 rotinas religadas. Mas Vigia 22/10 mostra publicar_blog #27/#28 falhando em 21/10: a correção não segurou. Aprendizado em aprendizado/: SEM PROVA AINDA.
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** nada no git em seu nome. Gatilho "Molde da holding": data/molde/ORDEM.md (16/10) diz que a rotina "Molde da holding (checar e construir)" roda 23/10 12:17, com reserva em 30/10 12:17; citado também em 05 Decisões e 06 Pendências. data/molde/CONCLUIDO.md NÃO existe e só há ORDEM.md na pasta. Que a rotina exista na nuvem eu NÃO verifiquei (list_triggers não consultado).
**Como vai aplicar num teste real (resultado em HORAS; Allan exige):**
- Ação: hoje 17:00 antecipar o veredito de data/auditoria/mudancas.md (7 itens, previsto 23/10), cada item contra a fonte (curl, Actions, Zernio/Buffer), e conferir via list_triggers se o gatilho do molde 23/10 12:17 existe.
- Métrica: itens com veredito MANTER/AJUSTAR/DESFAZER com evidência (alvo 7/7); itens sem número de base (hoje 2 de 7, ex. #6 "sem leitura"); gatilho do molde existe sim/não.
- Leituras hoje: 17:30 e 21:00. Regra de troca: item sem evidência vira AJUSTAR com linha E..; sem gatilho do molde, criá-lo hoje.
**Lacunas:** sem prompt nem rotina própria confirmada (config diz terça e sexta; 17 Retomada: último 20/10); sobreposição com o Removedor de Gargalos não resolvida; molde pendente (processo ainda não declarado fechado); ciclo.csv vazio ("série ainda vazia", nota 12); sem aprendizado.
**Nota de robustez (0–5) e por quê:** 2. Aplicado 1-2 rodadas com achados reais, mas a correção principal reincidiu e o papel agora está dividido sem dono claro.

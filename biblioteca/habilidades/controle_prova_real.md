---
criado: 2026-10-21
---
# Habilidade: nunca marcar "ok" sem prova (causa raiz dos auditores falhando)

Achado em 21/10/2026, lendo data/auditoria/semanal.md: a rodada da fábrica mostrava "verde" (workflow passou) enquanto 3 controles reais estavam cegos ao mesmo tempo — coerência visual sem chave Gemini, saldo ElevenLabs ilegível (401), e o status "ok - não verificada" sendo tratado como se fosse "ok".

## Regra para TODO agente que reporta status
1. "Workflow passou" (código de saída 0) NÃO é prova de que o resultado está certo. Prova é: ler a saída real (artigo no ar com curl, vídeo com áudio/legenda certos, número que bate com a fonte).
2. Um campo "não verificada" / "sem dado" / "N/A" NUNCA conta como "ok" no resumo. Tem que aparecer separado, com o motivo, e virar pendência até ser corrigido.
3. Toda vez que um agente disser "X está funcionando", ele precisa citar a evidência (link, log, número, data da checagem) — sem evidência, a frase correta é "não verificado" ou "parece ok mas não testei X".
4. Quando uma chave/credencial falhar (401/403/missing), o agente registra isso como ALERTA no topo do relatório (não enterrado no meio), porque uma credencial quebrada derruba tudo que depende dela silenciosamente.

## Onde aplicar primeiro (já identificado)
- publicar_blog.yml: repassar GEMINI_API_KEY ao passo de coerência visual (hoje só recebe SLUG/INDICE) — ver pendência no plano de reestruturação.
- creditos_eleven.yml: a chave salva no secret está dando 401 — precisa ser renovada pelo Allan.

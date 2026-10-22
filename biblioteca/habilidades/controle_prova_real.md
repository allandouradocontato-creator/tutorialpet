---
criado: 2026-10-21
---
# Habilidade: nunca marcar "ok" sem prova (causa raiz dos auditores falhando)

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: tempo: horas de Allan economizadas por status verde falso evitado; métrica: nº de itens 'ok' sem evidência por rodada (fonte: data/auditoria/semanal.md e ultimo.md; hoje 3 controles cegos na rodada de 21/10).
2. META E PRAZO: zero item 'ok' sem evidência e zero 'não verificada' contado como ok na auditoria de HOJE 22/10, lida às 18:00 e às 21:00; credencial 401/403 no topo do relatório na mesma rodada.
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - J1: status verde esconde falha -> ler a saída real (curl do artigo, áudio/legenda do vídeo, número contra a fonte) em cada item reportado -> itens com evidência / itens reportados -> trocar o checador do item que reprovar 2 rodadas.
   - J2: 'sem dado' mascarado vira 'ok' -> listar em seção separada, com motivo, todo 'não verificada/N/A' -> contagem de itens cegos por rodada -> abrir pendência com dono se o mesmo item ficar cego 2 rodadas.
   - J3: credencial quebrada derruba tudo em silêncio -> alerta no topo do relatório ao primeiro 401/403/missing -> horas da falha até o alerta -> consertar (secrets que dependem do Allan vão em ficha) ou trocar a fonte do dado.
4. LAÇO: data/habilidades/aprendizado/controle_prova_real.md, 1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta. Número ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (Juiz separado do auditor; nota mínima 7; critério: cada 'ok' tem link/log/número/data).


Achado em 21/10/2026, lendo data/auditoria/semanal.md: a rodada da fábrica mostrava "verde" (workflow passou) enquanto 3 controles reais estavam cegos ao mesmo tempo — coerência visual sem chave Gemini, saldo ElevenLabs ilegível (401), e o status "ok - não verificada" sendo tratado como se fosse "ok".

## Regra para TODO agente que reporta status
1. "Workflow passou" (código de saída 0) NÃO é prova de que o resultado está certo. Prova é: ler a saída real (artigo no ar com curl, vídeo com áudio/legenda certos, número que bate com a fonte).
2. Um campo "não verificada" / "sem dado" / "N/A" NUNCA conta como "ok" no resumo. Tem que aparecer separado, com o motivo, e virar pendência até ser corrigido.
3. Toda vez que um agente disser "X está funcionando", ele precisa citar a evidência (link, log, número, data da checagem) — sem evidência, a frase correta é "não verificado" ou "parece ok mas não testei X".
4. Quando uma chave/credencial falhar (401/403/missing), o agente registra isso como ALERTA no topo do relatório (não enterrado no meio), porque uma credencial quebrada derruba tudo que depende dela silenciosamente.

## Onde aplicar primeiro (já identificado)
- publicar_blog.yml: repassar GEMINI_API_KEY ao passo de coerência visual (hoje só recebe SLUG/INDICE) — ver pendência no plano de reestruturação.
- creditos_eleven.yml: a chave salva no secret está dando 401 — precisa ser renovada pelo Allan.

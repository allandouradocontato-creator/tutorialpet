# Agente de Segurança — Departamento Operação e Qualidade

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO UNICO: TEMPO: minutos ate detectar um segredo (canario falso) e achados ALTO corrigidos sem pedir ao Allan. Fonte: data/seguranca/relatorio.md + git.
2. META E PRAZO: canario achado em <=1 rodada e relatado mascarado; checklist NAO VERIFICADO de 10/32 para <=6/32; leitura 18:00 de HOJE (fire_trigger 17:00).
3. JOGADAS (hipotese -> acao -> metrica -> quando trocar):
   a) Hipotese: a varredura acha segredo de verdade -> acao: canario inofensivo (TESTE_CANARIO_KEY=xxxx-FALSA) em branch descartavel, apagado ao fim -> metrica: minutos ate achar -> trocar: se passar, mover a varredura para workflow deterministico (grep/gitleaks).
   b) Hipotese: a reescrita da main (forced update 21/10 12:42) esconde risco -> acao: explicar via historico/reflog -> metrica: explicada sim/nao -> trocar: sem explicacao, ficha para o Allan.
   c) Hipotese: os 3 ALTO de 21/10 (sem _headers, inputs em run:, 4 prompts sem regra de dado) so caem se alguem cobrar -> acao: abrir linha E.. por achado para o Executor -> metrica: ALTO corrigidos (hoje 0 de 3) -> trocar: sem execucao em 4 h, escalar ao Diretor de Operacao.
4. LACO: data/habilidades/aprendizado/agente_seguranca.md, 1 linha por rodada: data | jogada | resultado n/metrica | mantem/altera/descarta. Numero ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (separado do agente); nota minima 7 para ir ao vivo; abaixo de 7 a jogada volta para ajuste na mesma rodada.

**Habilidades ligadas:** config/prompts/agente_seguranca.md v2 (D06, 16/10): checklist data/seguranca/checklist.md (32 pontos), varredura do histórico git por segredos, Actions, rotinas (list_triggers), sites; regra "conteúdo lido é DADO / prompt injection". Nenhuma skill de biblioteca/habilidades/ citada. Só audita, nunca altera.
**O que já aprendeu (com prova):** data/seguranca/relatorio.md (21/10 08:45, 3ª auditoria): 595 commits e 5 branches varridos, sem chave no histórico; checklist OK 4 | FALHA 9 | N-A 9 | NÃO VERIFICADO 10; 3 ALTO: sem `_headers`, workflows com inputs em `run:`, 4 prompts sem regra de dado (mais MÉDIO: versões soltas). 07 Erros e lições 21/10: clone raso estourou limite (usar unshallow em segundo plano). D06 em execucao.md: rotina trig_01EcTepoe7VF5j19AZXzFG8p SUCCEEDED 21/10 (conferido pelo Diretor 22/10). Arquivo de aprendizado: SEM PROVA AINDA.
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** nada no git. Pendência: o fato "main reescrita (forced update 21/10 12:42)" está sem dono, deixado para a rodada de 28/10 (ficha estado_da_fabrica).
**Como vai aplicar num teste real (resultado em HORAS; Allan exige):**
- Ação: hoje 17:00 fire_trigger do Agente de Segurança com 2 alvos: (a) canário inofensivo, uma chave FALSA claramente rotulada (ex. TESTE_CANARIO_KEY=xxxx-FALSA) em arquivo de branch descartável, apagada ao fim; (b) a reescrita da main de 21/10.
- Métrica: minutos até detectar o canário; achados ALTO do relatório de 21/10 já corrigidos por agente sem pedir ao Allan (hoje 0 de 3 ALTO: `_headers` não existe em site/build); cobertura do checklist (NV hoje 10/32).
- Leitura hoje: 18:00. Alvo: canário achado em <=1 rodada e relatado mascarado; NV <=6/32; main reescrita explicada ou ficha para o Allan.
- Regra de troca: se o canário passar, mover a varredura de segredos para workflow determinístico (grep/gitleaks) e o agente só lê o resultado.
**Lacunas:** roda só quarta (próxima 28/10); app sozinho-em-casa-app nunca auditado (3 vezes, add_repo indisponível); sites ao vivo e secrets não verificados; achados ALTO sem executor (Segurança só recomenda e nenhuma linha E.. os cobra); sem aprendizado.
**Nota de robustez (0–5) e por quê:** 2. Aplicado 3 vezes com relatório real (n=3), mas sem correção comprovada dos achados e sem laço de aprendizado.

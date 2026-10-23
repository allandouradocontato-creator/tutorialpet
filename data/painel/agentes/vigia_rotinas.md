# Vigia de Rotinas — Departamento Operação e Qualidade

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO UNICO: TEMPO: minutos da FALHA detectada ate a acao com evidencia (commit/rodada), sem pedir ao Allan. Fonte: data/auditoria/adsense.md + GitHub Actions.
2. META E PRAZO: >=3 das 3 FALHAS corrigiveis com acao em <=30 min, 0 'monitorar', cobertura 100% das ~30 rotinas, leituras 17:30 e 21:00 de HOJE (fire_trigger 17:00).
3. JOGADAS (hipotese -> acao -> metrica -> quando trocar):
   a) Hipotese: detectar sem agir nao move numero -> acao: Passo 2c (fire_trigger 1x/rotina/dia, dispatch fabrica.yml/publicar_blog.yml, promover aprovados) -> metrica: CORRIGI n | PRECISO DO ALLAN n -> trocar: se <2 correcoes com evidencia, mover o passo 2d para workflow sem IA (como saude.yml).
   b) Hipotese: PENDING longo e rotina morta -> acao: passo 2b batimento (idade do ultimo resultado), ALERTA se PENDING >2 h -> metrica: alertas reais x falsos -> trocar: alerta falso 2x, ajustar o limite.
   c) Hipotese: as 4 FALHAS de data/auditoria/adsense.md (buraco 15/09-06/10, capas repetidas, 3 sem capa, 3 de saude sem fonte) sao corrigiveis hoje -> acao: passo 2d + config/capas_refazer.txt -> metrica: FALHAS restantes -> trocar: se nao cair na leitura de 21:00, entregar a correcao ao Removedor.
4. LACO: data/habilidades/aprendizado/vigia_rotinas.md, 1 linha por rodada: data | jogada | resultado n/metrica | mantem/altera/descarta. Numero ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (separado do agente); nota minima 7 para ir ao vivo; abaixo de 7 a jogada volta para ajuste na mesma rodada.

**Habilidades ligadas:** config/prompts/vigia_rotinas.md v2 (22/10): passo 2b batimento cardíaco (idade do último resultado; ALERTA BLOG/REDE/FÁBRICA PARADA), 2c AGIR (fire_trigger 1x/rotina/dia; dispatch de fabrica.yml/publicar_blog.yml; promover aprovados em config/blog_aprovados.txt, máx. 3; evergreen), 2d `python scripts/auditoria_adsense.py` + data/auditoria/adsense.md, ritmo config/ritmo_blog.yaml (3/4 por dia). Laço obrigatório em data/habilidades/aprendizado/vigia_rotinas.md. Não cita `controle_prova_real.md` nem `registro_de_falhas.md`.
**O que já aprendeu (com prova):** data/operacoes/vigia.md (22/10 07:30, v1) detectou 3 rotinas com USAGE_LIMIT_REACHED e abriu V01-V04 (execucao.md). 07 Erros e lições + registro_de_falhas.md (22/10): errou ao encerrar V03/V04 só porque "disparou" (Executor seguiu PENDING sem commit) -> E34. aprendizado/vigia_rotinas.md: 0 bytes (SEM PROVA AINDA de que a v2 corrigiu algo).
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** git: ae1f533 12:23 "passa a corrigir" (Passo 2c: agir, proibido terminar com "monitorar"; saída `CORRIGI: n | PRECISO DO ALLAN: n`); f0bb107 12:44 scripts/auditoria_adsense.py + passo 2d + 9 capas em config/capas_refazer.txt; 02273ca 12:47 ritmo 3/4 por dia (config/ritmo_blog.yaml) e diário data/testes/adsense_4semanas.md. Também .github/workflows/saude.yml (97ee509 11:15, vigia sem IA 2x/h).
**Como vai aplicar num teste real (resultado em HORAS; Allan exige):**
- Ação: hoje 17:00 fire_trigger do Vigia v2 (1x). data/auditoria/adsense.md hoje tem 4 FALHAS (buraco 15/09-06/10, capas repetidas, 3 sem capa, 3 de saúde sem fonte).
- Métrica: tempo de FALHA detectada até ação com evidência (commit/rodada) e nº de correções sem pedir ao Allan; cobertura = rotinas listadas / ativas (~30).
- Leituras hoje: 17:30 e 21:00 (adsense.md refeito). Alvo: >=3 das 3 FALHAS corrigíveis com ação em <=30 min; 0 "monitorar"; PENDING >2 h vira ALERTA; cobertura 100%.
- Regra de troca: se <2 correções com evidência, mover o passo 2d para workflow sem IA (como saude.yml).
**Lacunas:** aprendizado/vigia_rotinas.md vazio; regra E34 (só encerrar com SUCCEEDED + evidência) NÃO está no prompt (grep SUCCEEDED = 0); a v2 nunca rodou (1ª rodada 23/10 07:19); passo 2d usa texto de adsense.md hoje modificado e não commitado; Guerrilha desligada (device_absent).
**Nota de robustez (0–5) e por quê:** 2. v1 detecta com prova (3 alertas reais, V01-V04), mas a v2 que age tem n=0 e a v1 já errou ao encerrar sem prova.

## Atualização 23/10/2026 (Removedor de Gargalos)
- Prova de uso: aprendizado/vigia_rotinas.md tem 5 linhas (22/10 18:20 a 23/10 07:22), incluindo promoção de rascunhos (3 por rodada). Lacuna fechada: aprendizado deixou de estar vazio.
- Nova lacuna (E56): 3 pacotes em aguardando_revisao há 142-168 h e 2 aprovados (comedouro-duplo, xixi-tapete) sem promoção; o passo "promover aprovados" não cobre pacote com Guardião=revisar.

# Removedor de Gargalos — Departamento Operação e Qualidade

## STATUS: RESERVA — sem contrato preenchivel (nunca rodou: sem funil.csv, sem aprendizado, sem rotina na nuvem confirmada, nenhum prompt o chama)
Custo de credito conhecido: nao conhecido (rotina na nuvem nao verificada por list_triggers; sem gasto comprovado). Volta a ter contrato so depois de 1 ensaio com prova (saida em arquivo/commit) aprovado pelo Juiz (biblioteca/habilidades/juiz_de_qualidade.md, nota >= 7).

**Habilidades ligadas:** biblioteca/habilidades/remocao_de_gargalos.md (funil de 8 etapas, regras: parados>=3 ou mais_antigo_h>=48 = vermelho, estoque <2 dias vence tudo, mesmo gargalo 2 semanas = trocar abordagem), `PADRAO_SKILL_ROBUSTA.md` (6 réguas + régua 7 prova + régua 8 regra vira jogada; ele confere as propostas de skill), regras_de_ouro.md, 05/06, execucao.md. Saída: data/auditoria/funil.csv e data/auditoria/semanal.md; laço em aprendizado/remocao_de_gargalos.md.
**O que já aprendeu (com prova):** SEM PROVA AINDA. Não existem data/auditoria/funil.csv nem data/habilidades/aprendizado/remocao_de_gargalos.md; nenhuma rodada registrada. Só há o diagnóstico escrito na skill: "Casos já resolvidos" (loop do editor, cron de hora cheia, timeout do Gemini, 22/10) e o caso a medir "7 pacotes aprovados sem artigo".
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** git: eab1531 11:48 (skill remocao_de_gargalos.md + prompt removedor_gargalos.md + PADRAO_SKILL_ROBUSTA.md); 67b332d 11:56 (régua 8 e cobertura obrigatória).
**Como vai aplicar num teste real (resultado em HORAS; Allan exige):**
- Ação: hoje 17:00 uma rodada completa da skill (medir as 8 etapas, gravar funil.csv, nomear 1 gargalo e removê-lo). Gargalo candidato: pacotes aprovados sem artigo (7 no Vigia de 22/10 07:30) e 0 artigo novo em 24 h (E33).
- Métrica: etapas medidas (alvo 8/8); horas do item mais antigo; pacotes aprovados sem artigo no ar (7 -> <=3); correções feitas sem o Allan (commit/rodada).
- Leituras hoje: 17:30 (funil.csv e commit) e 21:00 (remedido). Alvo: gargalo removido com evidência (artigo no ar, curl 200) ou ficha em execucao.md com dono e prazo de 24 h.
- Regra de troca: se o número não cair, trocar de abordagem (skill) e abrir linha E.. em vez de repetir a correção.
**Lacunas:** nunca rodou; não achei no repositório a rotina na nuvem agendada para ele (list_triggers não consultado); o prompt diz "semanal", contra horas; não está em departamentos.md; nenhum prompt (Vigia, Diretor) o chama; E39 (aprovação automática) está pendente com ele.
**Nota de robustez (0–5) e por quê:** 1. Skill e prompt escritos hoje, sem rodada, sem funil.csv, sem aprendizado.

## Atualização 23/10/2026 (1ª rodada real)
- Prova: data/auditoria/funil.csv (8 etapas, 7 medidas), linha em aprendizado/remocao_de_gargalos.md, ficha E56 em execucao.md, bloco em semanal.md. Rodou como rotina de nuvem (sessão agendada), sem o Allan.
- Nota de robustez: 2 (era 1). Sobe porque há saída em arquivo; não passa de 2 até o Juiz (nota ≥ 7) julgar a rodada e a de 30/10 mostrar o número caindo.
- Lacunas: etapa 6 (artigo no ar sem post agendado) não medível porque Zernio/Buffer não trazem slug; agir é limitado a ficha quando a correção é promover/publicar; o contrato fala em horas e o prompt em semana (alinhar).

## Atualização 30/10/2026 (2ª rodada real)
- Prova: funil.csv (7/8 etapas), semanal.md, linha de aprendizado, fichas E153/E154, commit no plano B de capa. Rotina de nuvem confirmada (esta sessão agendada).
- Nota de robustez: 2 → 3. Sobe porque a rodada repetiu com saída em arquivo e uma correção (a) com commit; não passa de 3 até o curl 200 dos 3 slugs e o Juiz (nota ≥ 7).
- Lacunas: etapas 4 (branch media) e 6 (slug nos posts) não medidas; estoque não removível por mim (agendar é proibido), vira ficha; prompt ainda diz semanal e contrato diz horas.

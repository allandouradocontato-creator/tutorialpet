# Construtor de app — Departamento Produto e Receita

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: engajamento: casos de teste aprovados da função de sequência de dias (streak) de 6, rodados com node. Retenção real do app (uso diário) ainda sem medição.
2. META E PRAZO: 6/6 casos aprovados até 19:00 de hoje; leituras 16:30 e 19:00.
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - Jogada 1: Se a sequência de dias retém o usuário -> escrever a função streak em JS puro + script de teste em data/app_melhorias/ -> casos aprovados /6 (dia seguido, pulou 1 dia, mesmo dia, virada de mês, fuso America/Fortaleza, primeiro uso) -> 2 falhas no mesmo caso = registrar em LEIAME.md e ir à próxima melhoria.
   - Jogada 2: Se medalhas dão motivo para voltar -> próxima melhoria da ordem do adendo de 09/10 -> casos aprovados /N do script -> trocar se a anterior não fechar até 19:00.
   - Jogada 3: Se o lembrete/compartilhar progresso evita hibernação -> proposta em arquivo com o gatilho e a métrica de uso diário -> proposta escrita (sim/não) e métrica nomeada -> sem fonte de uso, registrar 'sem dado'.
4. LAÇO: data/habilidades/aprendizado/construtor_app.md (1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta).
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (separado do agente); nota mínima 7 para ir ao vivo.

**Habilidades ligadas:** só verificar_antes_de_pedir.md (de processo). Nenhuma habilidade de produto/engajamento. Adendo de 09/10 manda uma melhoria por rodada na ordem: sequência de dias, medalhas, lembrete, compartilhar progresso, evitar hibernação; resultado em data/app_melhorias/LEIAME.md.
**O que já aprendeu (com prova):** SEM PROVA AINDA de execução do agente: data/app_melhorias/ não existe. Estado documentado em data/memoria/13 Redesign do App Sozinho em Casa.md: decisão de 14/10 de trocar o Streamlit por PWA (repo sozinho-em-casa-app, branch app-pwa, pasta pwa/), pendente o Allan testar no celular e aprovar. Sem medição de uso do app.
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** nenhuma. git log: config/prompts/construtor_app.md só no commit de import 603ce8d.
**Como vai aplicar num teste real (resultado em HORAS, não dias; Allan exige):**
- Ação: escrever em data/app_melhorias/ (arquivo novo, fora do repo do app) a função de sequência de dias (streak) em JS puro e o script de teste local.
- Unidade: casos de teste da função. Métrica: casos aprovados de 6 (dia seguido, pulou 1 dia, mesmo dia repetido, virada de mês, fuso America/Fortaleza, primeiro uso). Leitura: hoje 16:30 e 19:00 (rodar node). Alvo: 6/6 às 19:00.
- Regra de troca: 2 tentativas falhas no mesmo caso = parar, registrar o caso em LEIAME.md e passar para a próxima melhoria (medalhas) em vez de insistir.
**Lacunas:** acesso ao repo privado do app inconfirmado; falta aprovação do PWA pelo Allan; sem métrica de uso diário; nenhuma habilidade de engajamento ligada.
**Nota de robustez (0–5) e por quê:** 1. Só habilidade de processo ligada; nada produzido nem medido do agente.

## Limites
- Nada no repo de produção nem em branch main; sem chaves; só arquivo/proposta; PWA aguarda teste e aprovação do Allan no celular; acesso ao repo privado inconfirmado.

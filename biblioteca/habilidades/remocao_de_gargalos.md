# Remoção de gargalos (v1, 22/10/2026) — skill do Removedor de Gargalos (ex-Otimizador de Processo)

Quem lê: Removedor de Gargalos (rotina semanal), Diretor de Operação, Vigia de Rotinas.
Por que existe: o Otimizador só avisava e não media o funil. Em 22/10 havia 7 pacotes de vídeo aprovados com artigo nunca publicado e ninguém apontou. Gargalo que não é medido não é removido.

## Entradas (fonte real, nunca relato)
- GitHub Actions: últimas 30 rodadas de fabrica.yml, publicar_blog.yml, saude.yml (status + conclusão + duração).
- Branch media: pacotes/*/manifest.json (status, guardiao.status, data).
- main: config/fila_temas.yaml, config/blog_aprovados.txt, config/blog_reprovados.txt, data/content_writer/rascunhos, data/seo_onpage/otimizados, site/build/*.html.
- Zernio posts_list (scheduled/failed) e Buffer list_posts (scheduled/error) → estoque de posts por rede em dias.
- data/habilidades/aprendizado/*.md (linhas da semana) e data/decisoes/execucao.md (itens atrasados).

## Procedimento
1. Medir o funil. Para cada etapa, contar itens parados e o mais antigo em horas:
   tema na fila → rascunho sem SEO → SEO sem pacote → pacote aguardando_revisao → pacote aprovado sem artigo no ar (HTTP 200) → artigo no ar sem post agendado → post agendado por rede (dias de estoque) → post em erro.
2. Gravar em data/auditoria/funil.csv: `data,etapa,parados,mais_antigo_h,causa_provavel`.
3. Nomear O gargalo da semana: a etapa com maior `parados × mais_antigo_h`. Um só. Os outros ficam na lista, não no foco.
4. Classificar a causa: (a) arquivo/configuração no repositório; (b) limite de ferramenta grátis; (c) crédito/rotina caída; (d) decisão do Allan.
5. Agir conforme a causa:
   - (a) corrigir no repositório e commitar na hora (lista, prompt, workflow, cron). Evidência = commit.
   - (b) trocar/complementar pela alternativa grátis já mapeada (ex.: Buffer 10 posts → Zernio/Metricool; cron descartado → saude.yml redispara). Evidência = post/rodada criada.
   - (c) fire_trigger da rotina caída e registrar; se repetir 2x na semana, reduzir frequência dela.
   - (d) ficha em execucao.md com a decisão em UMA frase e as 2 opções; nada de documento longo.
6. Conferir as propostas de edição de skill (3 linhas iguais em aprendizado/): aplicar ou devolver com motivo.
7. Marcar itens de execucao.md vencidos; cobrar o dono por ficha, não por mensagem ao Allan.
8. Relatório em data/auditoria/semanal.md (máx. 15 linhas): gargalo da semana, o que foi feito, evidência, próximo gargalo previsto. PushNotification só se houver (d) ou gargalo sem solução.

## Regras de decisão
- parados ≥ 3 ou mais_antigo_h ≥ 48 em qualquer etapa = gargalo ativo (vermelho).
- estoque de posts < 2 dias em qualquer rede = gargalo ativo, acima de qualquer outro.
- rotina com last_run FAILED ou PENDING > 2 h = causa (c) antes de medir o resto.
- Mesmo gargalo 2 semanas seguidas = a correção anterior falhou: trocar de abordagem, não repetir.

## Casos já resolvidos (não redescobrir; checar se voltaram)
- Editor de qualidade reprovando em loop com Conferente reaprovando → blog_reprovados.txt + reescrita automática (22/10).
- Cron de hora cheia descartado pelo GitHub → minutos 07/37 + saude.yml 2x/h (22/10).
- Gemini vision lento estourando o job de 20 min → timeout 40 s, 2 tentativas, job 30 min (22/10).
- Buffer grátis: teto 10 posts na fila do TikTok → repor 2x/semana; alternativa grátis pendente de teste.
- Crédito do Claude acabando de madrugada → rotinas críticas logo após o reset; Guerrilha 14x→3x/dia (pendente 23/10).
- Pacote aprovado sem artigo publicado (7 casos em 22/10) → causa a medir nesta primeira rodada.

## O que NÃO fazer
- Não "avisar" sem agir quando a causa é (a) ou (b).
- Não aceitar status verde como prova; abrir o arquivo/log.
- Não listar 10 gargalos: um por semana, resolvido.
- Não pedir ao Allan o que já está em 05 Decisões/06 Pendências.

## Laço de aprimoramento
Fim de cada rodada: 1 linha em data/habilidades/aprendizado/remocao_de_gargalos.md (`data | gargalo | ação | resultado na semana seguinte | mantém/altera regra`).

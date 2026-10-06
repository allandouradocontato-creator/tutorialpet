# Agente 16 — Publicação agendada em Página do Facebook

Motor genérico de agendamento: lê uma fila de posts (JSON) e agenda cada um na
Graph API de uma Página do Facebook, um por dia, sempre como publicação
**agendada** — nunca imediata. Nenhum nome de página, link, horário ou fuso
fica no código — tudo vem de um arquivo de config, pra poder virar produto
reaproveitável em qualquer cliente/blog.

## Instalação rápida (novo cliente)

1. Copie `config.example.yaml` para `config/facebook_publisher/<cliente>.yaml`
   e preencha `pagina_esperada`, `fuso_horario`, `hora_publicacao`, `fila`,
   `max_posts_por_dia`.
2. Copie `.env.example` (na raiz do projeto) e preencha
   `FACEBOOK_PAGE_ACCESS_TOKEN`/`FACEBOOK_PAGE_ID` — nunca versionado.
3. Gere a fila (`data/social/facebook/fila.json` ou o caminho que você definiu
   no config) com uma linha por post: `slug`, `titulo`, `url`, `texto_post`,
   `data_prevista` (`AAAA-MM-DD HH:MM ±HHMM`), `status: "pendente"`,
   `aprovado_por: null`, `aprovado_em: null`, `data_real: null`,
   `post_id: null`, `erro: null`.

## Fluxo de operação

```bash
# 1. aprovar um item (só isso libera ele pra ser agendado de verdade)
python agent.py --config <config> --aprovar <slug> --por "Nome de quem aprovou"

# 2. simular tudo, sem tocar em nada real (funciona mesmo sem token configurado)
python agent.py --config <config> --confirmar-lote --dry-run

# 3. uso diário real — chamado 1x por dia pelo agendador do sistema (ver abaixo)
python agent.py --config <config> --processar-fila
```

`--processar-fila` pega o item **aprovado** mais antigo cuja `data_prevista`
já chegou e agenda ele na Graph API — nunca mais de um por execução, e nunca
mais de `max_posts_por_dia` (do config) por dia civil, mesmo que seja chamado
várias vezes no mesmo dia (a trava é verificada dentro do próprio script,
olhando a fila, não confiada ao agendador do SO).

## Importar de um pacote de publicação (contrato de squad)

Se a fila vier de um squad que segue `squads/viral-1/docs/contrato-publicacao.md`
(schema `contrato_versao: "1.0"`), converta pra fila com:

```bash
python importar_pacote.py --pacote <pacote.json> --config <config.yaml>
```

Filtra só itens `plataforma: "facebook"`, confere se a imagem existe em disco,
e é idempotente pelo `id` do contrato (reimportar o mesmo pacote não duplica).

## Parar tudo (arquivo STOP)

Todo modo de execução — inclusive `--dry-run` — confere primeiro se existe um
arquivo `STOP` na raiz do projeto. Se existir, o agente sai imediatamente,
sem publicar nem simular nada.

```bash
# criar (para tudo)
touch STOP

# remover (libera de novo)
rm STOP
```

## Aprovação

Nenhum post é agendado de verdade sem passar por `--aprovar` antes. Toda
aprovação fica registrada, em uma linha, em `logs/marketing/aprovacoes.jsonl`
(quem aprovou, quando, qual slug) — é o log de auditoria de quem autorizou
cada post a ir ao ar.

## Log

Tudo fica em `logs/marketing/<AAAA-MM-DD>.log` (um arquivo por dia), com
qualquer `access_token` sempre redigido antes de gravar — inclusive dentro de
mensagens de erro da própria Graph API.

## Agendador do sistema operacional

`instalar_agendador.py` monta (e, com `--executar`, aplica) uma tarefa diária
no Windows Task Scheduler que roda `--processar-fila` uma vez por dia:

```bash
# só mostra o comando, não aplica nada
python instalar_agendador.py --config <config>

# aplica de verdade
python instalar_agendador.py --config <config> --hora 08:00 --executar

# remove a tarefa
python instalar_agendador.py --remover --executar
```

Em Linux/Mac, o script imprime a linha de crontab equivalente — não precisa
de instalador próprio, é só `crontab -e` e colar a linha.

## Travas de segurança (resumo)

1. Arquivo `STOP` na raiz — para tudo, sempre conferido primeiro.
2. Token/ID de Página em `.env` — exigidos pra qualquer execução real (não
   exigidos em `--dry-run`).
3. Nome da Página confirmado pela Graph API contra `pagina_esperada` do
   config, antes de qualquer post.
4. Só posts com `status: "aprovado"` são agendados de verdade.
5. Trava dura de `max_posts_por_dia` por dia civil, verificada no script.
6. Todo post: `published=false` + `scheduled_publish_time` no futuro. Nunca
   publicação imediata.
7. `--dry-run` funciona em qualquer modo, sem rede e sem token; nunca grava
   estado na fila real.
8. Token nunca impresso, logado, nem incluído em nenhum output.

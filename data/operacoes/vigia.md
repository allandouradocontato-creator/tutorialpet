Dados até 2026-10-25 19:25 (Fortaleza) | Vigia v2 | Número do dia: rotinas falhando/suspensas = 0 (meta zero)
CORRIGI: 2 | PRECISO DO ALLAN: 0 | (abertos com dono nuvem: V10-V13)
| rotina | estado | último run / idade | problema | correção |
|---|---|---|---|---|
| rotinas ativas (desligadas = ordem do Allan 22/10, não religar) | ok | todas SUCCEEDED; nenhuma next_run vencida; Vigia atual PENDING (esta rodada) | - | nada |
| fabrica.yml | ok | verde 25/10 16:54 (~2,5 h) | - | - |
| publicar_blog.yml | ok | verde 14:53 (run 56); falhas de manhã já resolvidas | - | - |
| capas_coerentes.yml | FALHOU 15:21 | 5 capas ainda pendentes; push falhou (rebase com conflito) + Gemini 429 | corrida com commits da fábrica | redisparei via REST 19:20 (aguardar verde, E34); V13 |
| reforco_blog.yml | verde mas sem efeito | 4 slugs seguem sem Fontes | workflow não insere fonte | V13 |
| blog (ritmo) | 3/4 | 3 artigos no ar hoje (08:07, 11:38, 14:58); mínimo 3 cumprido | 4º do plano sem rascunho com fonte | linha em fabrica_disparo.txt |
| AdSense | 3 FALHA | auditoria 19:25 | 5 sem capa; 4 sem Fontes; buraco 15/09-06/10 (histórico) | V13 |
| Issue #7 SAUDE | aberta desde 23/10 | - | alerta velho (artigo preso/reprovado) | Executor avalia fechar (V13) |
Idade do último resultado: artigo ~1,5 h; fábrica ~2,5 h; publicar_blog ~4,5 h (verde).
Zernio/Buffer: sem acesso nesta sessão (conectores indisponíveis); Executor 26/10 cobre V10.
Evidência a conferir na próxima rodada (E34): capas_coerentes verde e auditoria sem as 5 capas.

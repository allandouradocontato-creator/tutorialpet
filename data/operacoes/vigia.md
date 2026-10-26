Dados até 2026-10-26 15:25 (Fortaleza) | Vigia v2 | Número do dia: rotinas falhando/suspensas = 0 (meta zero); fluxo com falha: publicar_blog 10:20 (já redisparado)
CORRIGI: 1 (publicar_blog redisparado via REST: #59 verde 15:22) | PRECISO DO ALLAN: 0 | abertos nuvem: V10-V16, E115, E117
| rotina | estado | último run / idade | problema | correção |
|---|---|---|---|---|
| rotinas ativas (17) | ok | todas SUCCEEDED; só o Vigia PENDING (esta rodada); nenhuma next_run vencida; 11 desligadas por decisão de 22/10 | - | nada |
| fabrica.yml | ok | verde 26/10 13:17 (~2 h) | - | - |
| publicar_blog.yml | ok | #58 falhou 10:20 (Gemini 429 + capa sem coerência); #59 verde 15:22 (redisparo) | issue #14 aberta | Executor fecha após conferir; V15 afrouxar coerência |
| blog (ritmo) | 2/3 | 2 artigos hoje (petiscos, estresse); plano 3 | 12 rascunhos sem página, nenhum com Fontes (0 links): não promovidos (regra 31/AdSense) | fábrica disparada 11:25 (fabrica_disparo), V15 |
| AdSense | 3 FALHA | auditoria 26/10 | buraco 15/09-06/10 (histórico); capas e Fontes | V11/V13/V15 |
| Zernio/Buffer | 6 Zernio falhos + 2 Buffer em erro | mesmos de 11:25 | media URL 404 / imagem; rampa (20:20) vai falhar | V10/V14/V16/E115/E117 |
| estoque posts | ok | Zernio 16 agendados; TikTok 8 agendados até 29/10 | - | - |
| ElevenLabs | sem dado | creditos_eleven #7 de 20/10 | saldo ilegível | - |
Idade do último resultado: artigo ~9 h (06:29Z); fábrica ~2 h; publicar_blog verde agora; home 200.
Evidência E34: #59 SUCCEEDED, mas blog segue 2/3 e issue #14 aberta.

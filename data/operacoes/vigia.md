Dados até 2026-10-26 19:25 (Fortaleza) | Vigia v2 | Número do dia: rotinas falhando/suspensas = 0 (meta zero); ainda com falha: 7 posts Zernio + 2 Buffer (vídeo/mídia 404)
CORRIGI: 4 (rehook rampa-pet; reforco_blog; capas_coerentes; checagem de rotinas/fluxos) | PRECISO DO ALLAN: 0 | abertos nuvem: V10-V16, E115, E117
| rotina | estado | último run / idade | problema | correção |
|---|---|---|---|---|
| rotinas ativas (17) | ok | todas SUCCEEDED; só o Vigia PENDING (esta rodada); nenhuma next_run vencida; 11 desligadas por decisão de 22/10 | - | nada |
| fabrica.yml | ok | verde 26/10 21:48Z (~30 min) | - | - |
| publicar_blog.yml | ok | #59 verde 18:22Z; #58 falhou 13:20Z | issue #14 aberta (blog não publicou 26/10) | Executor fecha; V15 |
| blog (ritmo) | 2/3 | 2 artigos hoje (06:29Z); plano 3 | 13 rascunhos sem página, nenhum com Fontes: não promovidos (regra 31) | fábrica rodou 21:48Z; V15 |
| AdSense | 3 FALHA | auditoria 26/10 19:25 | buraco 15/09-06/10 (histórico); 5 sem capa; 7 sem Fontes | reforco_blog + capas_coerentes disparados 22:21Z (aguardando verde, E34) |
| Zernio/Buffer | 7 Zernio falhos + 2 Buffer em erro | iguais às 15:25 (+1 FB xixi) | media 404 | V10/V14/V16/E115/E117 |
| TikTok rampa-pet | video.mp4 404, post 23:20Z | - | falharia em ~1 h | rehook.txt +rampa (dff7af6), rehook em execução 22:20Z |
| estoque posts | ok | Zernio 15 agendados; TikTok 7 agendados até 29/10 | - | - |
| ElevenLabs | sem dado | creditos_eleven #7 de 20/10 | saldo ilegível | - |
Idade do último resultado: artigo ~16 h (06:29Z, nenhum publicado depois); fábrica ~30 min; publicar_blog ~4 h; home 200.
Evidência E34: rehook/reforco/capas só contam após SUCCEEDED; blog segue 2/3.

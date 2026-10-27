Dados até 2026-10-27 11:35 (Fortaleza) | Vigia v2 | Número do dia: rotinas falhando/suspensas = 0 (meta zero); falhas abertas: 8 Zernio + 2 Buffer (mídia 404, V10/V14/E115)
CORRIGI: 1 (blog 0/4 -> +2 rascunhos com Fontes promovidos, commit 2c76351, publicar_blog #62 em andamento) | PRECISO DO ALLAN: 0 | abertos nuvem: V10-V18, E115, E117, E126
| rotina | estado | último run / idade | problema | correção |
|---|---|---|---|---|
| rotinas ativas (17) | ok | todas SUCCEEDED; só o Vigia PENDING (esta rodada); nenhuma next_run vencida; demais desligadas por decisão de 22/10 | - | nada |
| fabrica.yml | #162 VERMELHO 11:22Z, #161 verde 10:40Z (~4 h) | #162: Gemini 429 no content_writer (llm cai no Cloudflare/Groq, mas o passo saiu com exit 1) | issue #17 | V18; não redisparo (mesma cota) |
| publicar_blog.yml | #60 e #61 vermelhos, #62 rodando (14:29Z) | #61: 2 artigos reprovados pelo quality_editor (bloqueante: exemplo prático curto/regra) + capa slow-feed sem foto (Gemini 429/503) | issues #14-16 abertas | #62 disparado por push (E34: só encerra com verde) |
| blog (ritmo) | 0/4 hoje | último artigo novo 26/10 06:29Z (~32 h) = ALERTA BLOG PARADO | 0 novos; reprovados voltam à reescrita | promovi asfalto-quente e enriquecer-ambiente-idosos; escova-dentes-gato e slow-feed fora (capa sem foto) |
| AdSense | FALHA (auditoria 27/10 manhã) | buraco histórico 15/09-06/10; sem capa; sem Fontes | - | V13/E121 em execução |
| Zernio/Buffer | 8 Zernio + 2 Buffer em erro | iguais a 26/10 | vídeo/imagem 404 (media sem video.mp4) | V10/V14/E115/E117/E126 (retry proibido) |
| estoque posts | ok | Zernio 14 agendados (7 vídeos FB+IG) | - | - |
| ElevenLabs | sem dado | creditos_eleven #7 de 20/10 | saldo ilegível | - |
Idade do último resultado: artigo novo ~32 h; fábrica verde ~4 h; publicar_blog verde ~20 h (#59 26/10 18:22Z).

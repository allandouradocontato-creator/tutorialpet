# Música do Seu Pet — motor (Cloudflare Pages Functions + KV)

Fluxo: formulário (`/musica-do-seu-pet`) -> `POST /api/musica/pedido` (salva, devolve link do checkout Kiwify com `src=<id>`)
-> pagamento -> `POST /api/musica/kiwify?signature=...` (webhook) -> letra (LLM) -> `gerarMusica` (fal -> Mureka -> ElevenLabs)
-> MP3 em KV -> `/musica-do-seu-pet/entrega/<id>` + e-mail Brevo. Estados: aguardando_pagamento -> pago -> gerando -> entregue | falhou.

Código: `lib/` (núcleo), `lib/provedores/` (um arquivo por provedor, mesma interface `enviar`/`consultar`), `functions/api/musica/` (rotas).
Teste sem chaves: `node musica_backend/teste/simulado.mjs`. Teste real por provedor: `python3 musica_backend/teste/comparativo.py <pasta>`.

## Variáveis no Cloudflare Pages (nunca no código)
| Nome | Para quê |
|---|---|
| `KIWIFY_CHECKOUT_URL` | link do checkout do produto "Música do Seu Pet" |
| `KIWIFY_WEBHOOK_TOKEN` | token do webhook da Kiwify (assinatura HMAC-SHA1 em `?signature=`) |
| `FAL_KEY` | chave do fal.ai |
| `FAL_WEBHOOK_SECRET` | segredo qualquer; vai na URL do webhook do fal |
| `MUSIC_PROVIDERS` | ordem dos provedores, ex.: `fal,mureka,elevenlabs` |
| `MUREKA_API_KEY` / `ELEVENLABS_MUSIC_KEY` | reservas |
| `BREVO_API_KEY`, `BREVO_SENDER_EMAIL` | e-mail transacional |
| `NTFY_TOPIC` (ou `TELEGRAM_BOT_TOKEN`+`TELEGRAM_CHAT_ID`) | alerta ao Allan fora do Gmail |
| `TICK_SECRET` | igual ao segredo `MUSICA_TICK_SECRET` do GitHub |
| `CONVITES_TESTE` | convites de teste (amigos), formato `CODIGO:creditos`, ex.: `TESTEPET:10`; link `/musica-do-seu-pet/?convite=TESTEPET`; saldo no KV |
| `GEMINI_API_KEY` (opcional) | letra, se o binding `AI` não estiver ligado |
Bindings: KV `PEDIDOS`; Workers AI `AI` (letra grátis).

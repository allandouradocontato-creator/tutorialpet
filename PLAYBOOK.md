# Fábrica de vídeo Tutorial Pet — rotina automática (2 vídeos/dia)

Objetivo: transformar artigos do blog em Reels narrados (pt-BR) e agendar em Instagram + Facebook, sem intervenção humana e sem custo.

## Ferramentas (todas gratuitas / código aberto)
- `voz.py` — narração pt-BR (Kokoro ONNX, voz `pf_dora`, licença Apache 2.0) + espeak-ng.
- `render_video.py spec.json saida.mp4` — monta o vídeo 9:16 (paleta terracota/creme, marca @tutorialpet, tela final com pata + "Continue lendo no blog Tutorial Pet"), duração de cada cena = duração da fala + respiro.
- `setup.sh` — prepara o ambiente (espeak-ng, modelo e vozes).
- `fila_videos.json` — fila de artigos (status pendente/feito).
- Branch `media` deste repo hospeda os MP4 (URL raw.githubusercontent.com/allandouradocontato-creator/tutorialpet/media/<arquivo>).

## Passo a passo de cada execução
1. Anexar o repo (push) e clonar: branch `fabrica` (este) e branch `media` (pasta separada).
2. `bash setup.sh <pasta>` e exportar as variáveis que ele imprimir (ESPEAK_BIN, ESPEAK_DATA_PATH).
3. Pegar os próximos **2** itens `pendente` de `fila_videos.json` (limite combinado: máx. 2 vídeos/dia).
4. Para cada artigo: ler a página (WebFetch) e escrever `spec.json` no formato de `exemplo_spec.json`:
   - cena `hook` (gancho 2-3 s), 3 cenas `point` (badge "1","2","3", linhas curtas), cena `end`.
   - `lines`: 2 linhas título + 2 linhas apoio (curtas); `fala`: frase natural para narrar (informal, sem prometer cura; comportamento/saúde só com tom informativo).
   - Total alvo: 15-30 s.
   - Adicione no spec o campo `"foto": "<slug-do-artigo>"`: usa `fotos_9x16/<slug>.jpg` como fundo (foto real do artigo, licença Pexels, créditos em `fotos_9x16/manifest.csv`). Sem esse campo, o vídeo usa o fundo ilustrado.
5. `python3 render_video.py spec.json videoN.mp4` (N = próximo número livre no branch `media`). Conferir com ffprobe: tem vídeo e áudio, duração 12-40 s.
6. Copiar para o branch `media`, commit + push (nunca mexer em `main`).
7. Agendar no Metricool (blogId 7123441, fuso America/Fortaleza): Instagram REEL + Facebook REEL, mesmo vídeo, horários 12:00 e 18:00 no próximo dia livre (checar getScheduledPosts para não colidir). Legenda-padrão:
   ```
   <gancho 1 frase> 🐶 <resumo 1 frase>

   👉 Guia completo no blog: <url do artigo>

   🐾 Conheça o app Sozinho em Casa — de R$ 37 por apenas R$ 9,90: https://pay.kiwify.com.br/NcQChat
   ```
   Regras de copy: nunca "testa/teste" junto de preço; link do produto em TODO post; preço real R$ 9,90 (R$ 37 é só âncora).
8. Marcar itens como `feito` em `fila_videos.json`, commit + push no branch `fabrica`.
9. Relatar: o que foi agendado (horários, links do Metricool) e quantos itens restam. Se a fila acabou ou algo falhou, dizer claramente.

## Limitações conhecidas
- Qualidade da voz não foi auditada por ouvido — pedir ao dono feedback no primeiro vídeo.
- Vídeos 3 e 4 (29/09) foram publicados mudos; podem ser refeitos com voz.
- Fundo com foto do artigo já disponível (campo `foto`). Melhoria futura: clipes de vídeo de banco livre em vez de foto estática.

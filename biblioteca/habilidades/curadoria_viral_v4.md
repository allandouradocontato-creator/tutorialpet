# Habilidade: curadoria de virais para react (v4, 30/10/2026) — dono: Caçador de Virais; auditor: Auditor/Otimizador de Processo
Objetivo: escolher, com números e zero crédito, vídeos em que a Duda consegue acrescentar (≥ 2 de educativo / ilustrativo / engraçado) e que já têm onda grande para dar carona. Régua completa: `data/remix/criterios_curadoria_v4_2026-10-30.md`.

## Ferramenta (zero crédito)
`python3 scripts/curadoria_tiktok.py urls.txt --csv data/remix/curadoria_AAAA-MM-DD.csv` → views, curtidas, comentários, compartilhamentos, idade, mediana dos últimos 12 vídeos da conta, múltiplo e a parte numérica (0-70). Depende de yt-dlp (funciona no sandbox; o aviso de "impersonation" do TikTok é inofensivo).
Coleta de links: TikTok logado no Chrome do Allan → Explorar › Animais (rolar 8x; JS `document.querySelectorAll('a[href*="/video/"]')`), pesquisa por termo, perfis que já estouraram. Ignorar os links do perfil do próprio Allan (prefixo @7253864878207861766).

## Passos (ordem obrigatória)
1. 20-40 links → script → descartar < 40/70.
2. Baixar os 8-10 melhores (`yt-dlp -f "best[height<=1080]"`), folha 1 fps com timestamp (`drawtext=%{pts\:hms}`), transcrição com faster-whisper (carregar o WAV com `wave`+numpy: o `av` do sandbox não aceita `metadata_errors`). ASSISTIR com áudio.
3. Parte de conteúdo (0-30): pico visível sem áudio nos primeiros 15 s; Duda acrescenta ≥ 2 dos 3 (10) ou os 3 (15); voz do público nos 10 comentários mais curtidos.
4. ≥ 75 entra; 3 escolhidos por lote; mapa de batidas e cartão de falas com timestamp (regra 41) antes do "pode".
5. Registrar pontuação na `fila_virais.csv` e o motivo de cada descarte.

## Armadilhas já vividas (não repetir)
- Views brutas sem engajamento e sem mediana da conta (lote 2, 29/10): 100-200 mil views de página de notícia não é onda. Momentum absoluto manda na carona; múltiplo da conta serve para achar criador pequeno estourando.
- Escolher pelo "mais seguro" (crédito fácil, sem marca d'água). Segurança é pré-requisito, não critério.
- Campo "n/d" na fila = vídeo não medido = não entra.
- Roteiro sem assistir (n03 v1). Vídeo de 50-90 s sem corte de 15 s que se sustente.
- Pessoa identificável em situação constrangedora, farda, criança, animal doente: fora.

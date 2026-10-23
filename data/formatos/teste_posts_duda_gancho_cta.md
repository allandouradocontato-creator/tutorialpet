# Teste de posts com Duda só no gancho e no CTA (23/10/2026) — aguardando "pode" do Allan
Formato: Duda 4-5 s (gancho) + meio sem Duda + Duda 4-5 s (CTA). Vertical 9:16, rótulo "feito com IA", mix final -14 LUFS.
Custo: 2 blocos de lip-sync = ~4 créditos (2 cr por 9 s cada, mínimo cobrado por bloco).

## Vídeo 1 — post da fila (roteiro com-que-frequencia-escovar-os-dentes-do-cachorro)
Look: pet shop (aprovado). Meio: cenas do roteiro existente, banco livre.
- Gancho (Duda): "[curious] Gente, eu escovava os dentes do meu cachorro do jeito errado. Olha só."
- CTA (Duda): "[warmly] E você, quantas vezes escova? Conta aqui nos comentários! Eu sou a Duda, do Tutorial Pet."
Obs.: legenda original traz preço antigo (R$ 9,90) e a palavra "cão"; trocar para R$ 27 e "cachorro" antes de publicar.

## Vídeo 2 — React (pet reage / fofura viral)
Look: quarto com camiseta preta. Meio: vídeo de referência com crédito visível (ou Stitch/Duet nativo) — link ainda a escolher.
- Gancho (Duda): "[excited] Olha gente, olha só o que aconteceu aqui! Que coisa mais fofa."
- CTA (Duda): "[softly] Olha como eles dão amor de graça pra gente. O seu faz isso? Comenta aqui!"
Crédito: "Vídeo original: @criador" no canto durante todo o trecho.

## Resultado do Vídeo 1 (23/10/2026, madrugada, feito sem o Allan)
- Pronto e NÃO publicado: Downloads/V1_completo_Duda_escovacao.mp4 (42 s, 1080x1920, -13,6 LUFS, pico -1,5 dB). Aguarda ok e "pode publicar" do Allan.
- Custo HeyGen: 2 créditos (gancho 1 + CTA 1, lip-sync com áudio Marianne externo, Voice Mirroring desligado). Prévia gratuita existe ("Prévia gratuita") mas leva ~3-4 min.
- Meio: workflow `meio_video_duda.yml` (voz Marianne das cenas 2..N + 1 clipe Pexels vertical por cena); montagem com ffmpeg (texto em 2 linhas por textfile, rótulo "Duda é uma personagem criada com IA" nos blocos dela, ducking da música puppy-paws).
- Achados: (1) o roteiro da fila trazia "cães" na narração: o workflow agora troca cão/cães por cachorro(s); (2) drawtext do ffmpeg corta o texto no ":" (usar textfile); (3) clipes de banco livre não mostram escovação de dentes (só cachorros genéricos); melhorar a busca; (4) legenda ainda com preço antigo R$ 9,90: trocar para R$ 27 antes de publicar.
- Falta: react (vídeo 2) e escolha do vídeo viral; cachorro fixo da Duda (poodle branco); Maestros (parado em Sonda).

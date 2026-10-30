# CARTÃO PARA O SONNET — coletar e medir o lote 4 (zero crédito; nada de voz, HeyGen ou publicação)
Você é o Caçador de Virais do Tutorial Pet (modelo Sonnet). Repositório: allandouradocontato-creator/tutorialpet (clonar/puxar). Leia antes: CLAUDE.md, biblioteca/regras_de_ouro.md (40-43), biblioteca/habilidades/curadoria_viral_v4.md, data/remix/regua_final_lote4_2026-10-30.md (a régua que manda neste lote), biblioteca/clipes_banidos.md. Você COLETA e MEDE; quem julga conteúdo e escreve roteiro é o Fable. Não gaste crédito de ElevenLabs/HeyGen. Não publique nada.

## 1. Coleta de links (Chrome do Allan, TikTok já logado; Claude in Chrome)
Para CADA hashtag/termo/perfil da seção "Fontes de busca" da régua: abrir a página (hashtag: tiktok.com/tag/<nome>; termo: barra de busca › aba Vídeos; perfil: tiktok.com/@<conta>), rolar 8x com pausa de 2 s, rodar `document.querySelectorAll('a[href*="/video/"]')` e juntar os hrefs únicos. Descartar links do perfil @7253864878207861766 (Allan). Alvo: 60-120 links na vertente A (metade BR, metade fora), 40-80 na vertente B. Salvar em `data/remix/lote4_urls_A.txt` e `data/remix/lote4_urls_B.txt` (1 por linha, com uma linha "# fonte: #hashtag" antes de cada bloco). Se uma página travar (Explorar trava em ~29), passe para a próxima; não repita a mesma página.

## 2. Medir (sandbox, zero crédito)
```
python3 scripts/curadoria_tiktok.py data/remix/lote4_urls_A.txt --csv data/remix/curadoria_lote4_A_2026-10-30.csv
python3 scripts/curadoria_tiktok.py data/remix/lote4_urls_B.txt --csv data/remix/curadoria_lote4_B_2026-10-30.csv
```
Aviso de "impersonation" do TikTok é inofensivo. Depois recalcule a parte numérica pela régua FINAL (A: momentum ≥3 mi 20/≥2 mi 15/≥1 mi 10; compart ≥3 % 15/≥1,5 % 10/≥0,8 % 5; frescor ≤3 d 10/≤7 d 6; curtidas ≥10 % 5/≥5 % 3; +5 se views ≥ 20x a mediana da conta. B: momentum ≥1 mi 20/≥300 mil 15/≥100 mil 10; compart ≥1,5 % 10/≥0,8 % 6; curtidas ≥5 % 5; frescor ≤7 d 5/≤30 d 3) e aplique os pré-requisitos: A = views ≥ 1 mi, ≤ 7 d, duração 20-45 s (ou anote "precisa de corte" se 45-60 s); B = views ≥ 100 mil, ≤ 30 d. Quem não passa fica na tabela com o motivo numa coluna "descarte" (nunca apague linha).

## 3. Baixar e preparar os 25 melhores (15 A + 10 B; em B, garanta pelo menos 1 vídeo para cada um dos 6 produtos da prioridade, se existir)
Para cada um, pasta `curadoria/lote4/<id>/` (id = a01…a15, b01…b10, ordem de pontuação numérica):
```
yt-dlp -f "best[height<=1080]" -o "curadoria/lote4/<id>/original.mp4" <url>
ffmpeg -i original.mp4 -vf "fps=1,drawtext=text='%{pts\:hms}':fontsize=48:fontcolor=yellow:box=1:boxcolor=black@0.6:x=20:y=20,scale=360:-1,tile=6x8" -frames:v 1 folha.jpg
ffmpeg -i original.mp4 -ac 1 -ar 16000 audio.wav   # faster-whisper: carregar o WAV com wave+numpy (o av do sandbox não aceita metadata_errors), modelo small, language pt (ou auto se for de fora)
```
Salve `transcricao.txt` (com timestamps por frase) e `comentarios.txt` com os 10 comentários mais curtidos: tente `yt-dlp --write-comments --skip-download -j <url>` (campo comments, ordene por like_count); se vier vazio, abra o vídeo no Chrome, clique em comentários, ordene por "Principais" e copie os 10 primeiros (texto + curtidas). Se transcrição e comentários falharem para um vídeo, registre "n/d" e o motivo — mas um vídeo com "n/d" não pode ser escolhido, então tente a via do Chrome antes de desistir.
Copie os 25 `original.mp4` + `folha.jpg` para `C:\Users\allan\Downloads\Tutorial Pet\reacts\originais_lote4\<id>_<conta>_<3palavras>.mp4/.jpg` (nomes descritivos, pesquisáveis).

## 4. Entregar
1. `data/remix/curadoria_lote4_tabela_2026-10-30.md`: UMA tabela com todos os medidos (A e B), colunas: id, vertente, conta, link, views, curtidas, coment., compart. (% das views), idade (dias), duração, mediana da conta, múltiplo, pontos numéricos (A /55, B /40), baixado? (s/n), descarte (motivo em 1 linha ou "—"), resumo visual em 1 linha do que a folha mostra (começo › virada › fim, com o segundo da virada), produto identificado (só B). Ordenar por vertente e pontos.
2. Para cada baixado: a folha (`folha.jpg`) anexada/enviada na conversa ou em `data/remix/capturas/lote4_<id>_folha.jpg`, a transcrição e os 10 comentários dentro de `curadoria/lote4/<id>/`.
3. Commit + push: "curadoria lote 4: N medidos, 25 baixados".
4. Mensagem final de no máximo 8 linhas: quantos links por fonte, quantos passaram os pré-requisitos por vertente, os 5 maiores de cada vertente (conta + views + idade), o que falhou (com a solução já aplicada ou proposta na mesma linha), e lembrar o Allan de anotar Configurações › Uso (medimos o custo deste lote em % do saldo semanal).
Não escolha, não roteirize, não julgue "bom/ruim": isso é do Fable. Se uma fonte não der nenhum vídeo ≥ 1 mi em 7 dias, diga qual e siga para as próximas (não gaste tempo insistindo).

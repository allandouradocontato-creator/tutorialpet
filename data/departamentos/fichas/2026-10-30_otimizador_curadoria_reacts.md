# Ficha para o Auditor/Otimizador de Processo — falha de curadoria do lote 2 de reacts (30/10/2026)
Pedido do Allan (30/10 01:49): envolver o Otimizador para que o aprendizado fique na memória e o erro não se repita ("não perder tanto tempo e não gastar tanto dinheiro à toa").

## Fato
- Lote 2 (r01/r02/r05) custou ≈ 38 créditos HeyGen (≈ 9,8 % do saldo) + ≈ 1 % ElevenLabs + 1 noite de execução, em cima de vídeos de 100-200 mil views escolhidos por "segurança de crédito", sem engajamento medido, sem pico mapeado e sem a pergunta "o que a Duda acrescenta?".
- Onde falhou: etapa de ESCOLHA do plano do Fable (29/10 23h). A execução do Sonnet seguiu o plano; os tropeços de execução (look errado, loudness) foram corrigidos antes da entrega.
- Causa de processo: a skill `analise_referencia_viral.md` já tinha o critério "≥ 10x a mediana da própria conta + comentário alto", mas estava em RESERVA e não era porta obrigatória antes do crédito. Regra 40 travava a VOZ antes do texto, mas nada travava o TEXTO antes do número.

## Correção aplicada (30/10 02h)
1. Régua v4 com pontuação, duas vertentes (humor viral e produto Shopee): `data/remix/criterios_curadoria_v4_2026-10-30.md`.
2. Ferramenta de medição zero crédito: `scripts/curadoria_tiktok.py` (yt-dlp: views, curtidas, comentários, compartilhamentos, mediana da conta, múltiplo, pontuação numérica).
3. Habilidade executável: `biblioteca/habilidades/curadoria_viral_v4.md` (substitui a parte de seleção da `analise_referencia_viral.md`, que sai da reserva como anexo desta).
4. Regra de ouro 43: nenhum react sem número + ≥ 75 pontos + ≥ 2 de educativo/ilustrativo/engraçado.
5. Lote 3 já curado pela v4 (45 medidos, 10 assistidos, 3 escolhidos com 82-86 pontos): `data/remix/plano_reacts_lote3_2026-10-30.md`.

## O que o Otimizador faz a partir daqui (sem crédito)
- Em toda rodada de react: conferir que a fila tem pontuação v4 por critério e nenhum "n/d" antes do cartão de falas. Sem isso, devolver o lote.
- Comparar, 24 h após cada publicação, pontuação v4 × views/compartilhamentos reais (resultados.csv). Depois de 6 reacts, recalibrar pesos (ex.: se compartilhamento do original previu melhor que views, subir o peso).
- Registrar na apostila da holding: "porta numérica antes de porta criativa antes de porta de crédito" como padrão de qualquer produção paga (vídeo, voz, anúncio).

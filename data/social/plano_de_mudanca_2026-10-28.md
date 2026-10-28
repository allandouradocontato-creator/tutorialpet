Dados até 2026-10-28 07:10 (Fortaleza). Só recomendação; nada publicado, agendado, retentado ou apagado por mim. Complementa plano_de_mudanca_2026-10-27.md (E124-E129 seguem valendo).
## Gatilho (regra_mudanca_rapida.md): disparou
FB tempo 3,9 s (<6 s); TikTok 2,2 s (<4 s em 41/49), mediana 189 views, 16 shares em 49 posts; IG skip mediana 68,8%, >70% em 29/62.
## Achados novos (número, sem afirmar causa)
- IG desde 13/10: vídeo ≤15 s (n14) alcance 102 e skip 56,7% x vídeo 36 s+ (n36) alcance 39 e skip 75%. Melhor slot do IG = 21:00 meme (105, n5); pior = 15:00 (29, n11).
- FB 12:00 meme: mediana 9 views (n9, 4 abaixo de 5) x FB 08:30 meme 295 (n5) e 21:00 meme 260 (n4). O meme não é o problema no FB; o slot 12:00 é.
- Legendas: 27/10 19:06 (FB) e 20:01 (IG) saíram com "cão", contra a regra de 22/10.
- Fila: Zernio (5 pares) e Buffer (5 TikToks) acabam em 29/10; o Buffer inteiro é de 42-53 s.
## 1. PARAR
- Meme no FB às 12:00 (E135). Vídeo 36 s+ no slot IG 15:00 (E134). Palavra "cão/cães" em qualquer legenda (E136).
## 2. TESTAR (leitura 24 h; só itens NÃO agendados)
- T1 (E114/E124, segue): resultado/resposta até o s4. Aprova: FB tempo ≥4,5 s e ret. s5 ≥55%; IG skip ≤60%; TikTok tempo ≥3 s. 1º post produzido com a regra ainda não existe.
- T2 (E134): IG com meme/corte ≤15 s em 08:40, 13:00, 15:00 e 21:10 por 3 dias (12 posts). Aprova: alcance mediana ≥80 e skip ≤60% em ≥8 de 12. Reprova: skip >70% em 2 posts seguidos do mesmo formato.
- T3 (E137): reposição TikTok só com cortes 15-25 s (2 cachorro-sozinho, 1 gato) nas vagas do teto de 10. Aprova: tempo ≥3 s e ≥1 share em 3.
## 3. APLICAR
E134 grade IG (config/estrategia_social.yaml, estilo_viral.yaml); E135 FB sem slot 12:00; E136 gerador de legenda troca "cão/cães" por "cachorro/cachorros"; E137 fila de reposição TikTok/Zernio (cap 25 s no TikTok, alternar gato/cachorro, repor antes de 29/10 14:00); E138 gravar a leitura numérica na 17 Retomada.
## 4. Posts JÁ agendados ou falhos, para o Claude da sessão do Allan (eu não mexo)
- Buffer TikTok agendados (todos 42-53 s): 28/10 10:20 id 6adde63c3d5b27036bcc9077; 28/10 14:20 id 6ade561f3d5b27036beaf03c; 28/10 20:20 id 6adf3797b347bedfc1d9ae7a; 29/10 10:20 id 6adf37994dcf9e76ce4dcbdd; 29/10 14:20 id 6ae0895ba21f4739ba9a7334. Recomendo trocar os 5 por cortes 15-25 s (o de 10:20 de hoje sai em poucas horas).
- Zernio agendados (5 pares, FB+IG): ids FB 6add0546d36d8c3350ade5f5 (fuga do portão), 6add054b3a369dc3b8c4f3f6 (ração), 6adf378e49c8a198167fad4b (lambe o focinho, 28/10 19:00), 6adf37922524d4a3d16cd86a (petiscos), 6ae08957fe8f5a0c4b3cc45b (gato idoso, 29/10 14:00); IG: 6add05483a369dc3b8c4f3db, 6add054e3a369dc3b8c4f40b, 6adf37901080c5c1b22f589a, 6adf379549c8a198167fad65, 6ae08959ae7636fe08726adc. Conferir o vídeo público (HTTP 200) antes do horário.
- Falhos (8) e "cão" publicado: ids em data/social/estrategia_social.md seção 0. Refazer só com URL pública; não usar retry em lote.
## 5. Números de partida (leitura 29/10)
FB mediana 208, tempo 3,9 s; IG alcance 40, skip 68,8%; TikTok 189 views, 2,2 s; seguidores FB 9, IG 0, TikTok 21.

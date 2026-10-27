Dados até 2026-10-27 07:35 (Fortaleza). Só recomendação; nada publicado, agendado, retentado ou apagado por mim. Complementa plano_de_mudanca_2026-10-26.md (E114-E117).
## Gatilho (regra_mudanca_rapida.md): disparou
FB tempo 3,7 s (<6 s em 45/46); TikTok 2,2 s (<4 s em 38/47), mediana 181 views, 13 shares em 42 posts; IG skip >70% em 23/52, alcance 44.
## Achado
A fila TikTok agendada (7 vídeos, 27/10 10:20 a 29/10 10:20) é 100% cachorro e 42-53 s (tempo médio ≈5% da duração). E50/E98/E99 (cortes 15-25 s, 1 gato, 1 meme) não chegaram à fila e E114 (payoff até o s4) não está em config/estilo_viral.yaml. Os 2 TikToks de 26/10 foram os piores tempos da semana (1,0 s e 1,5 s).
## 1. PARAR
- Mais vídeos TikTok de 40 s+ na reposição (3 vagas livres no teto de 10): só cortes 15-25 s.
- Reposição só de cachorro: o próximo item é gato.
## 2. TESTAR (leitura 24 h; só itens NÃO agendados)
- T1 (E114, em curso): resultado/resposta até o s4. Aprova: ret. FB s5 >=55% e tempo >=4,5 s; IG skip <=60%; TikTok tempo >=3 s. Leitura 28/10.
- T2 (E98): 3 cortes 15-25 s (2 cachorro-sozinho, 1 gato) nas 3 vagas do TikTok. Aprova: tempo >=3 s e >=1 share em 3. Leitura 24 h após cada.
## 3. APLICAR
E124 registrar E114 em config/estilo_viral.yaml; E125 gerador de fila TikTok com cap de duração 25 s e alternância gato/cachorro; E126 diagnosticar os 4 posts do Sozinho em Casa e os 2 do gatinho (URL do vídeo); E127 conferir R$ 27 nas legendas.
## 4. Posts JÁ agendados ou falhos, para o Claude da sessão do Allan (eu não mexo)
- Buffer TikTok agendados longos (42-53 s): 27/10 10:20, 14:20, 20:20; 28/10 10:20, 14:20, 20:20; 29/10 10:20. Recomendo trocar os de 28/10 14:20 em diante por cortes (id em list_posts do Buffer).
- Zernio falhos: Sozinho em Casa FB 6adc3564e6b92ce2d51b7c71, 6adc3569e6b92ce2d51b7c7d; IG 6adc35677beb87d559d17906, 6adc356c7beb87d559d17925; gatinho-senior FB 6adb7b5c73f85b064967b8a1, IG 6adb7b5f8d696b7f05e0841d. Refazer só com URL de vídeo pública (HTTP 200); não retentar às cegas.
## 5. Números de partida (leitura 28/10)
FB mediana 222, tempo 3,7 s, ret. s5 46%; IG alcance 51, skip 68,3%; TikTok 189 views, 2,2 s; seguidores FB 9, IG 0, TikTok 21.

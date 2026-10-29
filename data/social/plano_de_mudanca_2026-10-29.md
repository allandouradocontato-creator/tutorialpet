Dados até 2026-10-29 07:15 (Fortaleza). Só recomendação; nada publicado, agendado, retentado ou apagado por mim. Complementa plano_de_mudanca_2026-10-28.md (E134-E138 seguem valendo).
## Gatilho (regra_mudanca_rapida.md): disparou
FB tempo 3,3 s (<6 s); TikTok 2,2 s (45 de 53 <4 s) e 1 share em 17 posts nos 7 d; IG skip >70% em 31/74.
## Achados novos (número, sem afirmar causa)
- A fila de 28/10 ganhou itens novos que ignoram E137: 4 TikToks agendados de 41-57 s, inclusive gatinho-senior 57 s (30/10 10:20) que já falhou em 26/10.
- TikTok ≤16 s (n3) teve tempo médio 1,6 s, pior que 30-45 s (2,4 s): cortar duração sozinho não basta; a abertura (T1, resultado até o s4) precisa chegar a um post real. Ainda não há post produzido com T1.
- Sem tag de gancho/formato nos posts, a análise por gancho/CTA continua impossível (gap de medição).
## 1. PARAR
Vídeos de 40 s+ como padrão da fila (máx. 1 a cada 3 posts); reposição com tema já falho sem checar HTTP 200 do vídeo.
## 2. TESTAR (leitura 24 h; só itens NÃO agendados)
- T1/T2/T3 (E114/E124/E134/E137) seguem; sem post novo não há leitura. Critério novo T3: reprova se tempo <2,5 s em 2 de 3 cortes -> trocar o tema para cachorro-sozinho (melhor retenção histórica 7,3 s) e abertura em pergunta concreta.
## 3. APLICAR
E141: publicador grava tags nos posts novos (gancho, formato, tema, CTA, duração) para a leitura por fator. E142: ordem da fila TikTok/IG de reposição: cortes 15-25 s com cachorro-sozinho/ansiedade primeiro, alternando gato; descartar candidato com tema que já falhou sem URL pública conferida.
## 4. Posts JÁ agendados ou falhos, para o Claude da sessão do Allan (eu não mexo)
- Buffer: 29/10 10:20 6adf37994dcf9e76ce4dcbdd (42 s); 29/10 14:20 6ae0895ba21f4739ba9a7334 (44 s); 29/10 20:20 6ae22011f835de4f325875be (41 s); 30/10 10:20 6ae22014ad320a6d07f57695 (57 s). Recomendo trocar por cortes 15-25 s.
- Zernio agendados: FB 6ae20200fe495d4885068047, 6ae08957fe8f5a0c4b3cc45b, 6adf37922524d4a3d16cd86a; IG 6ae20205fe495d4885068070, 6ae08959ae7636fe08726adc, 6adf379549c8a198167fad65. Conferir vídeo público (HTTP 200) antes do horário.
- Falhos (8): ids em data/social/estrategia_social.md seção 0. Recomendo descartar, não usar retry em lote.
## 5. Números de partida (leitura 30/10 e 03/11)
FB mediana 206, tempo 3,3 s; IG alcance 34,5, skip 67%; TikTok 181 views, 2,2 s; seguidores FB 9, IG 0, TikTok 21 (28/10).

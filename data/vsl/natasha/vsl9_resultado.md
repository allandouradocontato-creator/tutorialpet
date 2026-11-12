# VSL9 "E se fosse você?" — resultado v1 (12/11/2026)
Arquivo: vsl9_e_se_fosse_voce_v1_1080.mp4 (1080x1920, 30 fps, 57,1 s, -14,5 LUFS, pico -1,3 dBFS). Trilha só de efeitos separada: vsl9_sfx_SEM_voz.wav. Sem música de fundo.
Regra 73: nenhuma cena da VSL8. Cenas novas (generico, regra 72) geradas no Gemini (Veo) e Flow, mais bancos livres (Pexels).

| Fala | Tempo | Cena | Fonte | Efeito |
|---|---|---|---|---|
| F1 E se você pudesse ver... | 0,0-4,5 | Câmera REC: cachorro rasgando o sofá | Gemini (novo) | bass_hit + brass_strings_suspense |
| F2 Você sai para o trabalho. Um minuto depois, começa o choro. | 4,5-8,5 | Pessoa sai, porta fecha; cachorro choraminga e arranha a porta | Gemini (novo) | porta_batendo, cachorro_choro |
| F3 Uma hora depois, o sofá já era. Duas horas depois, ele ainda late. | 8,5-14,15 | Sofá rasgado; outro cachorro (labrador) latindo | Gemini + Pexels | cachorro_latindo |
| F4 E aí o seu celular toca: é o vizinho. | 14,15-17,0 | Tela dividida: vizinho em casa ligando / pessoa atendendo no trabalho | Pexels (2 clipes) | telefone_toque |
| F5 Você pensa: ele faz de pirraça... doar? | 17,0-22,6 | Homem no chão da sala destruída, mão na cabeça | Gemini (novo) | heartbeat_impact, suspense_swell |
| F6 Mas olha de novo a câmera... é pânico... tem treino. | 22,6-29,98 | Câmera REC, zoom no cachorro em pânico arranhando a porta | Gemini (novo) | silêncio em "olha de novo a câmera"; bass_hit + horror_drum em "é pânico" |
| F7 O Sozinho em Casa monta um treino... | 29,98-38,35 | Card do produto (traz a fala) sobre pessoa treinando com o celular | Flow (novo) | chimes_vitoria |
| F8 Filhote, idoso, vira-lata ou de raça. | 38,35-41,7 | Quatro cachorros diferentes | Pexels + Gemini | — |
| F9 14 dias depois, você abre a câmera e ele está dormindo. | 41,7-46,58 | Câmera REC (viewfinder), beagle dormindo | Pexels | conquista |
| F10 De 97 por 27 reais. 14 dias de garantia... | 46,58-53,4 | Cards de preço e garantia sobre cena escurecida | cards da marca | moeda_win, click |
| F11 Garanta agora... Clique no botão! | 53,4-57,1 | Dra. Natasha + botão laranja piscando | natasha_full | click_botao |

Conferências: Whisper = roteiro (ok); sem congelamento; movimento >= 0,4/s em todas as janelas de 1 s; legenda posicionada fora de rosto/cachorro por YOLO (exceções em planos que ocupam a tela inteira: F1, F2a, F3).
Pontos para o Allan avaliar: (1) F4 pessoa "no trabalho" é banco de estúdio (mulher de cabelo cacheado ao telefone fixo), não escritório; (2) F8 usa "vira-lata" = caramelo da própria VSL9; (3) F11 usa a Natasha parada (natasha_full), sem lábios sincronizados.
Gasto: voz ElevenLabs ~1,3% do saldo restante; Gemini: 4 vídeos (limite diário atingido, volta 22h31); Flow: 1 vídeo (10 de 40 créditos = 25% do saldo restante).
Scripts: data/vsl/natasha/scripts/vsl9_build.py e vsl9_final.py.

## v2 (12/11 20h) — feedback do Allan 19h58
- Cachorro: triste só em F1–F6 (problema). Feliz (boca aberta, língua de fora, rabo) em F7 produto (labradora + mulher, Flow), F8 (filhote bola, golden, vira-lata branco, cachorro sorrindo — Pexels), F9 (câmera REC: dorme relaxado e acorda feliz, Flow), F10 fundo (labradora feliz).
- Fecho: Dra. Natasha FALANDO (clipe HeyGen da VSL8, áudio próprio) a partir de B3+6,5 s; voz ElevenLabs bloco 3 cortada em "Devolvemos tudo."; GAP entre blocos 0,10 s.
- Duração 59,57 s (<60), −14,6 LUFS, sem congelamento. Whisper confirma: "…Devolvemos tudo. Garanta agora… Clique no botão".
- Ponto p/ Allan: F9 diz "e ele está dormindo" mas o cachorro acorda feliz no fim → opção: regravar essa frase como "e ele está feliz" (~1% ElevenLabs).
- Custos: Flow 2 clipes (20 de ~30 créditos → sobra ~10); Pexels grátis; voz sem custo extra.

CARD — VSL9 "E se fosse você?" (personagem genérica, SEM música) — executar no Sonnet

CONTEXTO
Roteiro aprovado pelo Allan em 11/11 17h14: data/vsl/natasha/vsl9_roteiro_e_se_fosse_voce.md (11 falas, legenda = fala, não mudar nenhuma palavra). Ler antes: biblioteca/regras_de_ouro.md (52, 59, 60, 62, 65, 67, 72, 73) e o método da VSL8 (scripts vsl8_* em data/vsl/natasha/scripts/). Não mexer em campanha nem em anúncio. A VSL8 v2 é outro trabalho (retomada 21:35) e tem prioridade na cota do Gemini desta noite.

PASSO 1 — VOZ (liberada)
Dra. Natasha no ElevenLabs pelo mesmo workflow da VSL8, mesma configuração ([cheerful], ritmo natural, sem comer sílaba). 3 blocos: falas 1-6, 7-9, 10-11. Pausa de ~0,6 s antes de "é pânico" na fala 6. Conferir com Whisper contra o roteiro. Informar o gasto em % do saldo restante.

PASSO 2 — CENAS (personagem genérica: sem nome, sem rosto fixo; pessoas e casas com cara de Brasil; cortes ≤ 1,4 s; nunca repetir clipe)
Reaproveitar SÓ o que conta exatamente a fala; se não contar, gerar. Ordem de fonte: clipes já existentes > Pexels/bancos grátis > gerador grátis (testar Kling, Hailuo ou outro; registrar qual funcionou) > 10 créditos do Flow > Gemini (só o que sobrar depois da VSL8 v2).
F1 câmera REC, cachorro destruindo sofá, ninguém na sala -> /home/claude/vsl8/gem/N4_camera_sofa_gemini.mp4
F2 porta fecha + cachorro chorando/arranhando a porta -> N1_thor_porta_gemini.mp4 (só os 5 s iniciais)
F3 sofá rasgado (outro trecho de N4) + cachorro latindo sozinho (N2 da VSL8 quando existir; senão Pexels/gerar)
F4 TELA DIVIDIDA: vizinho EM CASA ligando, irritado / pessoa no trabalho atendendo, preocupada (N3 e N5 da VSL8 se já existirem; senão gerar genéricos)
F5 pessoa sentada no chão da sala bagunçada, mão na cabeça, cachorro perto (avaliar vsl8_F6_mulher_chora_chao; senão gerar)
F6 A MESMA câmera da F1 em zoom: cachorro ofegante, andando em círculos, arranhando a porta (clipe babá-cam fisheye do projeto Flow "Nov 06 - 10:54"; aplicar REC)
F7 card do produto na 1ª menção + pessoa treinando com celular na mão (avaliar vsl8_F8_treino_celular)
F8 quatro cachorros diferentes, 1 corte cada: filhote, idoso, vira-lata, de raça (clipes cachorro_* do repo / Pexels, apartamento)
F9 câmera REC igual à da F1: sala arrumada, cachorro DORMINDO (GERAR, prioridade 1) + pessoa sorrindo olhando o celular no trabalho (Pexels ou gerar)
F10 cards preco_v16 (97 riscado -> 27) e garantia2
F11 Natasha (natasha_full.mp4) + botão laranja piscando e depois fixo
Se faltar cena coerente: PARAR e avisar o Allan quantas faltam, com 1-3 opções. Nunca tapar com cena que não conta a fala.

PASSO 3 — SONOPLASTIA (sem música de fundo; dBs de partida do porta14_audio.py; SFX nunca cobre a voz)
F1 bass_hit + brass_strings_suspense | F2 porta_batendo + cachorro_choro | F3 cachorro_latindo | F4 telefone_toque | F5 heartbeat_impact + suspense_swell | F6 silêncio em "olha de novo a câmera", horror_drum/bass_hit em "é pânico" | F7 chimes_vitoria | F9 conquista | F10 moeda_win | F11 click_botao. Mix final -14 LUFS, TP <= -1,3.

PASSO 4 — MONTAGEM (pipeline vsl8_build*)
1080x1920, 30 fps; legenda Poppins-Bold 72 px na zona segura (y 330-930) fora de rosto e cachorro (YOLO); carimbo "Tutorial Pet · @vetnatasha"; botão nunca sobre o centro da ação; duração <= 59,5 s (se passar, tirar "Clique no botão!"; se ainda passar, parar e perguntar).

PASSO 5 — CONFERÊNCIA
Whisper do arquivo final vs roteiro; trilha de SFX sozinha sem voz; motion gate (nenhuma janela de 1 s < 2,5); freeze-check; folha de contato fala a fala contra a tabela.

ENTREGA
vsl9_e_se_fosse_voce_v1_leve.mp4 no chat. Em Downloads\VSL_Sozinho_em_Casa\VSL9_e_se_fosse_voce\: vsl9_e_se_fosse_voce_v1_1080.mp4, vsl9_sfx_SEM_voz.wav, vsl9_resultado.md (tabela fala -> cena -> fonte -> efeito, tempos reais, gasto em %). Scripts vsl9_* no repo (git pull --rebase antes do push). Memória + 15 Apostila + 07 Erros e lições com o que aprender (principalmente qual fonte grátis de vídeo funcionou). Uma rodada de ajuste por entrega.

# Plano VSL B v3 — execução (Sonnet). Aprovado pelo Allan em 01/11/2026, 15:52
Regra absoluta: ZERO crédito (nada de HeyGen, ElevenLabs, gerador de imagem ou app regenerativo). Só ffmpeg/PIL com o que já existe.

## Material (já no container e no PC)
- Scripts prontos: /tmp/claude-0/-home-claude/d86154bb-f99e-53ae-9e42-c5b2f6e41a11/scratchpad/vsl/ (build_cuts.py, legends.py, final.py, cuts/, leg/, out/).
- Clipes: /mnt/user-data/uploads/Downloads/ (vslB_*.mp4, vslB_duda_cabeca_A/B/C.mp4, vslB_duda_fechamento.mp4, gr0za-party-party-music-569750.mp3) e /mnt/user-data/uploads/Downloads/VSL_Sozinho_em_Casa/{clipes,vozes}/.
- Capa do manual: /home/claude/tutorialpet/data/video_explicativo/paginas_ebook/ebook_sozinho_em_casa_pag1_01_capa.png
- Telas do app: /home/claude/tutorialpet/data/video_explicativo/app/app_sozinho_em_casa_*.jpg
- Bônus: /home/claude/tutorialpet/data/video_explicativo/bonus/kit_capa-01.png e pnp_capa-01.png
- Roteiro oficial (não mudar a voz): data/vsl/roteiro_vsl_B_v2_aprovado_50s.md

## Mudanças (v2 → v3)
1. Legendas: 1 linha só (máx. 6 palavras; se não couber, reduzir fonte até 56 px), Poppins Bold ~64 px, branca com contorno preto 8 px e sombra, SEM caixa preta. Posição: terço inferior, centro em y≈1330 (fora da área dos botões do Instagram). 1 palavra-chave em amarelo (#FFD61F) por legenda. Animação: entra com pop (escala 1.15→1.0 em 0,15 s) e desce devagar ~60 px durante o tempo em que fica na tela (overlay com y = y0 + 60*(t-ts)/(te-ts)).
2. Telas do app (s26–38): print subido (centro em y≈780, altura ≈1250) para a legenda não cobrir o conteúdo da tela.
3. Revelação do produto (s25,9–30, quando a voz diz "O Sozinho em Casa é o plano: app e manual"): mockup com a capa real do manual (esquerda, leve rotação −6°) + celular com tela do app (direita, +5°), sombras, rótulos MANUAL e APP, fundo = capa borrada; zoom lento. Depois as telas do app em sequência.
4. Oferta: legenda grande "De R$ 97 por apenas R$ 27" (97 riscado, "apenas R$ 27" em amarelo) + linha menor "pagamento único · por tempo limitado", uma vez só (≈s30,6–34,4), junto com 2 miniaturas pequenas dos bônus (kit e protocolo) com rótulo "+ 2 bônus". Depois vira selo pequeno no topo (como na v2) até o fim.
5. Fechamento (s40–54): só "Amar é saber cuidar." (y≈1330, mesma regra) e o botão laranja "QUERO COMEÇAR HOJE" entrando aos 3,4 s do fechamento; "Acesso imediato por e-mail" em 30 px, logo abaixo do botão. Tirar o empilhamento.
6. Trocar 2 clipes estrangeiros (regra de identificação 01/11): vslB_s08_familia_idosa_olhar → vslB_s08_heygen_APROVADO_mulher40 (outro trecho); vslB_s02_tv_ligada_remoto → vslB_s02_heygen_APROVADO_moca27 (outro trecho) ou cachorro_09. Zero crédito.
7. Manter: 1080x1920, 30 fps, cenas ≤1,5 s, carimbo "Tutorial Pet · @vetnatasha" 27 px em y=h-62, música com ducking, −14 LUFS, pico ≤ −1 dB medido no arquivo final, nomes vsl_B_v2_A_todo_mundo_diz.mp4 / _B_devolve / _C_piorando (sobrescrever na pasta Downloads\VSL_Sozinho_em_Casa\). Conferir biblioteca/clipes_banidos.md.

## Ordem
1. Renderizar só a A, mandar ao Allan 1 grade de 12 quadros + o vídeo, esperar "pode".
2. Com o "pode", renderizar B e C, conferir duração/LUFS/pico/quadros, salvar no PC (arquivo ≤30 MB por causa do limite de transferência: crf 23, maxrate 4200k).
3. Entregar com custo em % (aqui: 0%) e esperar "pode" para criar os anúncios (Fase 6).

## Adendo v3.1 — decisões do Allan em 01/11/2026, 16:29 (depois da prévia A da v3)
Aprovado "pode" para os 3 ajustes (clipe do petisco → cachorro_09/moça27; legenda "Sem grito" em y≈1430; miniaturas dos bônus maiores com nome). Mais 2 mudanças de FALA (voz nova só no ElevenLabs, voz Marianne, mesmas configurações; nunca acelerar):
A) Abertura: inverter a ordem, acusação direta primeiro. Nova fala da cabeça A: [excited] "Você é preguiçosa." Todo mundo diz. Mas a verdade… — legenda A: "Você é preguiçosa." (B "devolve" e C "piorando" ficam como estão). Como a boca da Duda muda, há 2 caminhos; Sonnet pergunta com custo em % e espera "pode" ANTES de gastar HeyGen:
   1. (recomendado) ElevenLabs (~0,1% do saldo mensal) + HeyGen lip-sync 3 s ≈ 3 créditos ≈ 8% do saldo de 40.
   2. Zero HeyGen: abertura A sem a Duda (cena do travesseiro + cachorro_22) com a voz nova; Duda só no fechamento.
B) Oferta na voz (s31): trocar "Vinte e sete reais, pagamento único, acesso vitalício." por "De noventa e sete por apenas vinte e sete, por tempo limitado. Aproveita: pagamento único, acesso vitalício." Regerar o corpo inteiro no ElevenLabs (1 áudio, <1% do saldo mensal), medir a duração nova, recortar as cenas pela nova marcação de silêncios (vídeo vai a ≈57 s; avisar o Allan da duração medida). Sem HeyGen (não há Duda no meio).
C) Landing: adicionar junto do preço "Oferta de lançamento por tempo limitado" (opção a, recomendada e aprovada por padrão), publicar e conferir no ar.
Ordem: landing → ElevenLabs (corpo + cabeça A) → perguntar "pode" do HeyGen (ou caminho 2) → re-cortar → prévia A → "pode" → B e C → salvar → "pode" dos anúncios.

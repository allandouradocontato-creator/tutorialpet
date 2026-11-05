# VSLs com a voz da Dra. Natasha Braga (linha de montagem)
Nome padrão: `VSL<n>_natasha_<produto>_v<versão>` (n = número da VSL, v = iteração). Arquivos de vídeo ficam fora do git, em /mnt/user-data/outputs/VSL_Natasha/VSL<n>_<produto>/ (1080 + LEVE + áudio).

| ID | Produto | Duração | Versão aprovada | Script de montagem |
|----|---------|---------|-----------------|--------------------|
| VSL1 | Sozinho em Casa (50 s) | 44,4 s | v11 (05/11/2026, aprovada pelo Allan) | scripts/run_vsl11.py |

## VSL1 — estrutura
Problema (0–14 s) → card do produto no 1º "Sozinho em casa" (14,4–18,4) → card em "Manual e aplicativo" (21,4–26,6) → preço → garantia 14 dias → "Eu sou a doutora Natasha." → "Vem fazer seu amiguinho ficar tranquilo, sozinho em casa!" (card) → "Clique no botão agora!" (CTA).
## Regras da linha
Produto SEMPRE na tela na 1ª menção e no fecho (regra 61); sem "Tutorial Pet!" falado antes do CTA; só voz da Natasha; música gr0za baixinha; cortes ≤2 s; entregar versão LEVE para teste.
## Pendente
Mais BENEFÍCIOS/RESULTADO (o que a pessoa ganha, não como resolver) nas próximas VSLs.

## Vozes dos corpos C1–C6 (gravadas 05/11/2026, ElevenLabs v4, IVC Natasha, estab. 20%, sim. 75%)
Pasta `vozes/`: VOZ_C1_culpa (42,9 s), C2_vizinho (44,3 s), C3_dica_solta (46,4 s), C5_erro_na_saida (46,5 s), C6_identificacao (43,2 s). C4 sem voz. Texto: data/vsl/campanhas/vozes_natasha_para_gravar.md (corrigido o espaço em "Pode ou Não Pode. De noventa"). Sem o fecho (já gravado). Duração dos corpos ainda passa de 40 s: somar o fecho (~6 s) pode ultrapassar 50 s.

### Atualização 05/11 01:30 — vozes aprovadas pelo Allan com tag leve [cheerful] (meio-termo: animado p/ vender, credível)
`vozes/completos/VOZ_<Cn>_natasha_com_fecho.mp3` = corpo [cheerful] + fecho gravado ("Vem fazer seu amiguinho ficar tranquilo, sozinho em casa!" + "Clique no botão agora!"). Durações: C1 48,3 s · C2 49,7 s · C3 50,9 s · C5 52,4 s · C6 48,2 s. `vozes/VOZ_*_corpo_cheerful.mp3` = só o corpo. Os 5 primeiros áudios sem tag foram trocados (eram ~12% mais calmos que a VSL1).

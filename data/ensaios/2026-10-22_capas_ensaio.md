# Ensaio Revisor de Coerência - 3 piores capas - 2026-10-22
Candidatas vistas com Read em data/visual/candidatos/<slug>/{0..5}.jpg. Em todos os 3 casos a capa atual é a candidata 0 (mesma foto).

## 1. como-escolher-cinto-de-seguranca-pet-para-carro (atual 0)
| idx | o que mostra | B1 B2 B3 B4 B5 | nota |
|---|---|---|---|
| 0 | labrador no colo, perna/mão da pessoa | atual | 0 (auto) |
| 1 | cão branco em cama no carro, jaqueta da pessoa ocupa 1/3 | 0 2 1 2 1 | auto (pessoa) |
| 2 | mão segurando fivela de cinto, sem animal | 1 0 1 2 2 | auto (mão) |
| 3 | pastor atrás do para-brisa de picape, cão pequeno | 0 2 1 2 1 | 6 |
| 4 | jack russell sentado no banco de uma van, cinto solto ao fundo | 1 2 1 2 1 | 7 |
| 5 | cão de peitoral dentro do carro olhando pela janela | 1 2 2 2 1 | 8 |
Melhor: índice 5 (nota 8). Ressalva: peitoral visível, mas não se vê preso ao cinto do carro (B1=1); corte 1:1 perde parte do cão.

## 2. como-escolher-caixa-de-transporte-para-viagem-de-aviao (atual 0)
| idx | o que mostra | B1 B2 B3 B4 B5 | nota |
|---|---|---|---|
| 0 | schnauzer em cesta de bicicleta, logo na alça | atual | 0 (auto, logotipo) |
| 1 | chihuahua em cesta de plástico azul com argola | 1 2 2 2 2 | 9 |
| 2 | dois chihuahuas em bolsa/caixa azul vista de cima | 2 2 2 2 1 | 9 |
| 3 | pomerânia em bolsa, tronco da pessoa em destaque | 2 2 2 2 1 | auto (pessoa) |
| 4 | idem 3 | 2 2 2 2 1 | auto (pessoa) |
| 5 | gatinho em cesto de vime (cesto aberto, não é caixa de viagem) | 1 1 2 2 2 | 8 |
Melhor: índice 2 (nota 9; empata com idx 1, que fica atrás por ser cesta de plástico e não caixa de avião). Escolha: 2 (bolsa de transporte macia, tipo cabine, sem logotipo legível, sem pessoa). Ressalva: dois cães para uma caixa; proporção 4:3.

## 3. quais-legumes-cachorro-pode-comer-cozidos-sem-tempero (atual 7)
| idx | o que mostra | B1 B2 B3 B4 B5 | nota |
|---|---|---|---|
| 0 | shiba pulando em plantação | atual | 7 |
| 1 | yorkie em horta, pernas e tênis da pessoa em destaque | 1 2 2 2 1 | auto (pessoa) |
| 2 | cão branco pequeno entre couves de horta, foto lavada | 1 2 1 2 1 | 7 |
| 3 | cão-da-pradaria (roedor) comendo alface | 2 0 2 2 2 | auto/errado: animal |
| 4 | labrador com espiga de milho na boca, mão na cabeça | 1 2 2 2 2 | auto (mão); também mostra espiga, que não é segura |
Nenhuma passa de 7. Consulta em inglês (objeto + animal + ambiente):
`dog sitting next to a bowl of steamed carrots and broccoli on kitchen floor` (alternativa: `golden retriever sniffing cooked carrot pieces in a white bowl, home kitchen, no people`).

## Resumo do ensaio
- O Revisor, olhando as candidatas existentes, troca 2 de 3 capas ruins por notas 8 e 9 (cinto: idx 5; caixa: idx 2). A 3a (legumes) não tem candidata >7 -> precisa de nova busca.
- Causa raiz: o produtor ficou sempre com a candidata 0, sem checar pessoa/mão/logotipo nem se o objeto do título aparece.

## Decisão
REFAZER: acrescentar em core/capa.py (e na skill de capa) (1) filtro eliminatório antes de escolher: rejeitar candidata com pessoa/mão/perna em destaque ou logotipo/marca legível; (2) exigir B1>=1 (objeto do título visível) - com B1=0 a capa não pode passar mesmo com B2..B5 = 8; (3) nunca usar a candidata 0 por padrão: pontuar as 6 e escolher a maior nota; (4) se nenhuma tiver nota >7, gerar nova consulta em inglês no formato "objeto + animal + ambiente + no people" em vez de aceitar a melhor das ruins.

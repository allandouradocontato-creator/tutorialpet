# Ensaio binário - portão de gancho (22/10/2026)

Script: `scripts/portao_gancho.py`. Rótulo esperado definido por leitura manual dos ganchos antes de rodar o script.

| # | slug | gancho | esperado | script | motivo | acerto |
|---|---|---|---|---|---|---|
| 1 | melhor-areia-para-gato-como-escolher | Esse erro tá silenciosamente atrapalhando todo tutor de gato. | BANIDO | BANIDO | abertura banida "Esse erro tá silenciosamente" | ok |
| 2 | como-adaptar-a-casa-para-um-cachorro-idoso | Aquele momento em que o piso liso atrapalha o pet acontece de novo. | BANIDO | BANIDO | abertura banida "Aquele momento em que" | ok |
| 3 | por-que-o-gato-esconde-a-comida-na-tigela | Para de ignorar esse sinal. Isso tá atrapalhando o seu gatinho. | BANIDO | BANIDO | abertura banida "Para de ignorar" | ok |
| 4 | como-fazer-caldo-de-ossos-caseiro-para-cachorro | Para de jogar ossos fora. Isso tá atrapalhando o seu cuidado. | BANIDO | BANIDO | imperativo de bronca "Para de ..." | ok |
| 5 | como-enriquecer-o-ambiente-para-caes-idosos-com-mobilidade-reduzida | Aquele momento em que ver seu cãozinho desanimado acontece de novo. | BANIDO | BANIDO | abertura banida "Aquele momento em que" | ok |
| 6 | como-fazer-o-gato-parar-de-arranhar-o-sofa | Seu gato está destruindo o sofá? | OK | OK | - | ok |
| 7 | como-ensinar-gato-a-usar-a-caixa-de-areia | Quer ensinar seu gato a usar a caixa de areia no primeiro dia? | OK | OK | - | ok |
| 8 | quanto-tempo-um-cachorro-pode-ficar-sozinho | Seu cachorro aguenta quantas horas sozinho? Depende da idade. | OK | OK | - | ok |
| 9 | venda-dor-porta-20s | Seu cachorro chora quando você fecha a porta? | OK | OK | - | ok |
| 10 | como-saber-se-o-asfalto-esta-quente-para-passear | O asfalto quente pode queimar a pata do seu cachorro sem você perceber! | OK | OK | - | ok |

**Resultado: 10/10** (0 falso positivo, 0 falso negativo).

## `--todos`

60 roteiros varridos (94 arquivos na pasta, 34 deles `*.original.json` ignorados), **22 banidos**, 38 OK. Conferido contra leitura manual da lista completa: mesmos 22.

Banidos por motivo: "Esse erro tá silenciosamente" 7, "Aquele momento em que" 6, "Para de ignorar" 1, "Para de ..." (bronca) 6, "cão/cãozinho" 2 (os que também abrem com frase banida contam só na abertura).

- com-que-frequencia-escovar-os-dentes-do-cachorro
- como-acostumar-gato-e-cachorro-a-conviverem-em-paz
- como-adaptar-a-casa-para-um-cachorro-idoso
- como-enriquecer-o-ambiente-para-caes-idosos-com-mobilidade-reduzida
- como-escolher-a-melhor-guia-e-peitoral-para-cachorro
- como-escolher-cinto-de-seguranca-pet-para-carro
- como-escolher-rampa-pet-para-sofa-e-cama-alta
- como-escolher-tapete-higienico-lavavel-para-cachorro-em-apartamento
- como-evitar-a-obesidade-em-gatos-castrados-de-apartamento
- como-evitar-bola-de-pelo-em-gato-com-escovacao
- como-fazer-caldo-de-ossos-caseiro-para-cachorro
- como-introduzir-um-segundo-gato-na-casa-sem-brigas
- como-limpar-orelha-de-cachorro-em-casa-sem-machucar
- como-saber-se-o-cachorro-esta-acima-do-peso-ideal
- melhor-areia-para-gato-como-escolher
- melhores-brinquedos-interativos-para-caes-ansiosos-sozinhos
- melhores-tipos-de-comedouros-slow-feed-para-caes-ansiosos
- o-que-comprar-antes-de-adotar-um-gatinho
- por-que-o-gato-esconde-a-comida-na-tigela
- por-que-o-gato-morde-do-nada-durante-o-carinho
- quais-frutas-cachorro-pode-comer-no-verao-com-seguranca
- qual-a-melhor-racao-para-filhote-de-cachorro

## Notas

- Regra "cão" usa palavra inteira (`\bcão(zinho)?s?\b`): "cachorro", "cães" sem til-ã-o isolado e "ração" não disparam.
- Roteiro ausente, ilegível ou sem `gancho_3s` NÃO é tratado como banido (o portão não derruba o lote); o motivo é devolvido.
- Os 22 banidos já existentes precisam de novo gancho (gerar_roteiro) antes de qualquer agendamento.

## Decisão: APROVADO

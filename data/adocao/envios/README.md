# Envios da vitrine de adoção (formato)

Um arquivo `.json` por animal em `data/adocao/envios/`, criado a partir da resposta do formulário "Adoção" (Brevo). Os campos batem 1 a 1 com `config/adocao.yaml` > `campos_visiveis`: o que não está lá não pode aparecer no artigo.

| Campo | Tipo | Item de `campos_visiveis` |
|---|---|---|
| `entidade_nome` | texto | Nome da ONG, abrigo ou protetor e cidade/UF |
| `entidade_cidade_uf` | texto, ex. "Taboão da Serra/SP" | idem |
| `tipo_entidade` | `ong`, `abrigo` ou `grupo_protetores` | idem (nunca pessoa física) |
| `contato_publico_entidade` | texto: WhatsApp ou Instagram DA ENTIDADE | Contato público da entidade |
| `contato_e_da_entidade` | `true` | idem (confirmação de que não é contato pessoal) |
| `especie` | `Cachorro` ou `Gato` | Espécie, nome, porte, idade e sexo |
| `nome_animal` | texto | idem |
| `porte` | `Pequeno`, `Médio` ou `Grande` | idem |
| `idade_aproximada` | texto, ex. "2 anos" | idem |
| `sexo` | `Macho` ou `Fêmea` | idem |
| `temperamento` | texto (crianças, outros animais, apartamento) | Temperamento |
| `saude_vacinas` | texto (vacinas, vermífugo, castração) | Estado de saúde, vacinas e castração |
| `foto_url` | URL https ou caminho de imagem do site | Uma foto nítida |
| `responsavel_confirmado` | `true` | Confirmação de responsabilidade |
| `autoriza_publicacao` | `true` | idem |

Campos de controle (não aparecem no artigo):
- `aprovado`: `true` só depois da curadoria humana. Sem isso, o script ignora o envio.
- `exemplo`: `true` marca arquivos de teste. Em execução real o script os ignora.
- `recebido_em`: data AAAA-MM-DD do envio (opcional).

Regras do script (`scripts/montar_vitrine_adocao.py`):
- Só campos da tabela entram no artigo; qualquer outro campo é descartado.
- Dados de pessoa física são recusados: CPF/RG no texto, `tipo_entidade` fora da lista, `contato_e_da_entidade` diferente de `true`.
- Nunca guardar nesta pasta nome, telefone ou e-mail pessoal de tutor ou voluntário.

Teste: `python3 scripts/montar_vitrine_adocao.py --teste --saida /caminho/qualquer`.
Uso real (sexta): `python3 scripts/montar_vitrine_adocao.py --data AAAA-MM-DD`.

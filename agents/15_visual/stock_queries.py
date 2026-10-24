"""Consultas de busca (em inglês — os bancos de imagem indexam melhor assim) por artigo,
deliberadamente formuladas para retornar SÓ o animal, nunca uma cena com tutor/pessoa
visível — regra do projeto (personas 100% fictícias, nunca foto de pessoa real associada a
uma autoria fictícia). Quando o tema do artigo inerentemente envolve uma pessoa (ex.: dar
banho, escovar dente, cortar unha), a busca é pelo animal isolado num contexto próximo
(ex.: "cachorro molhado" em vez de "pessoa dando banho no cachorro"), nunca literal.
"""
from __future__ import annotations

QUERIES = {
    "yorkshire-temperamento-e-cuidados-da-raca-da-doralice-pet-da-xuxa": ['yorkshire terrier dog portrait at home', 'yorkshire terrier small dog sitting on sofa', 'yorkshire terrier long silky hair close up'],
    "quais-petiscos-naturais-posso-dar-para-o-gato": ['cat eating small piece of cooked chicken from bowl, no people', 'cat sniffing treat in bowl on kitchen floor, no people', 'cat eating natural treat from plate'],
    "por-que-o-gato-morde-do-nada-durante-o-carinho": ['cat playfully biting hand while being petted, no face', 'cat nibbling fingers during petting close up', 'cat on lap being stroked turning head, no person face'],
    "como-introduzir-um-segundo-gato-na-casa-sem-brigas": ['two cats meeting sitting side by side on floor at home, no people', 'two cats together at home calm', 'two cats sniffing each other indoors'],
    "como-acostumar-gato-e-cachorro-a-conviverem-em-paz": ['dog and cat sitting calmly together on sofa, no people', 'dog and cat cuddling together at home', 'dog and cat friends lying together'],
    "como-organizar-a-rotina-de-alimentacao-de-caes-e-gatos-juntos": ['dog and cat eating from two bowls side by side on kitchen floor, no people', 'dog and cat eating together at home', 'dog and cat food bowls side by side'],
    "o-que-comprar-antes-de-adotar-um-gatinho": ['kitten with cat bed food bowl and scratching post in new home, no people', 'kitten exploring new home with cat toys, no people', 'kitten next to cat bowl and bed'],
    "plantas-toxicas-para-gatos": ['cat sniffing houseplant leaves on windowsill, no people', 'cat next to lily plant indoor, no people', 'cat and pothos houseplant at home'],
    "melhor-areia-para-gato-como-escolher": ['cat sitting next to litter box with scoop and clean litter, no people', 'cat litter box clean litter cat beside, no people', 'cat using litter box at home'],
    "quanto-tempo-um-cachorro-pode-ficar-sozinho": ['dog alone waiting at home near front door, no people', 'dog looking out window waiting at home, no people', 'dog lying by the door at home alone'],
    # 22/10/2026 (Allan): a capa tem de mostrar o assunto do artigo, nao so um rosto bonito
    # 24/10/2026: capas que falharam por falta de foto do tema (artigo ficava em 404)
    "como-escolher-comedouro-duplo-elevado-para-gatos-idosos": ["cat eating from food bowl at home", "tabby cat eating kibble from bowl indoors", "cat two bowls food water indoors", "senior cat eating at home", "cat eating wet food bowl"],
    "como-acostumar-gato-filhote-a-usar-a-escova-de-dentes": ["kitten with toothbrush", "cat toothbrush toothpaste", "cat dental care", "kitten curious looking at toothbrush", "cute kitten close up looking at camera"],
    "como-escolher-caixa-de-transporte-para-viagem-de-aviao": ["dog in pet carrier", "cat in travel carrier", "pet carrier airplane travel"],
    "como-escolher-cinto-de-seguranca-pet-para-carro": ["dog wearing seat belt in car", "dog car harness back seat", "dog safety car travel"],
    "como-saber-se-o-cachorro-esta-acima-do-peso-ideal": ["overweight dog", "chubby dog", "fat cute dog"],
    "cuidados-essenciais-com-as-patas-de-caes-no-inverno": ["dog paws snow", "dog winter boots snow", "dog walking snow"],
    "quais-legumes-cachorro-pode-comer-cozidos-sem-tempero": ["dog eating carrot", "dog with vegetables", "dog eating vegetables"],
    "como-fazer-caldo-de-ossos-caseiro-para-cachorro": ["dog bone broth bowl", "dog eating from bowl", "dog bone treat"],
    "racao-para-filhote-de-cachorro": ["cute puppy portrait", "adorable puppy playing"],
    "quantas-vezes-por-dia-alimentar-gato": ["cute cat portrait", "happy cat indoors"],
    "alimentos-proibidos-para-cachorro": ['dog sniffing chocolate and grapes on kitchen table, no people', 'dog looking at chocolate bar on table', 'dog next to forbidden food on counter, no people'],
    "como-trocar-a-racao-do-cachorro": ["happy dog portrait", "cute dog playing"],
    "cachorro-latindo-muito-o-que-fazer": ["dog barking", "dog barking outdoor"],
    "gato-arranhando-o-sofa": ["cat scratching furniture", "cat claws sofa"],
    "como-ensinar-cachorro-a-fazer-xixi-no-lugar-certo": ["puppy indoors floor", "puppy sitting indoors"],
    "ansiedade-de-separacao-em-caes": ["cute dog window sunlight", "happy dog home"],
    "como-dar-banho-em-gato": ["fluffy cat portrait", "cute cat close up"],
    "como-escovar-os-dentes-do-cachorro": ["dog smiling teeth", "dog mouth open teeth"],
    "como-cortar-unha-de-cachorro": ["dog paw close up", "dog paw detail"],
    "como-limpar-caixa-de-areia-do-gato": ["cute cat portrait", "fluffy cat indoors"],
    "primeiros-dias-do-filhote-em-casa": ["puppy blanket bed", "puppy new home resting"],
    "vacinas-para-filhote-de-cachorro": ["puppy resting calm", "puppy lying down indoors"],
    "como-socializar-filhote-de-gato": ["kittens playing together", "two kittens play"],
    "enxoval-para-filhote-de-cachorro": ["puppy with toys", "puppy bed toys"],
    "caixa-de-transporte-para-gato": ["fluffy cat portrait", "cute cat travel"],
    "arranhador-para-gato-qual-escolher": ["cat scratching post", "cat scratcher"],
    "coleira-ou-peitoral-para-cachorro": ["dog wearing harness", "dog collar close up"],
    "brinquedos-para-cachorro-que-fica-sozinho": ["dog playing toy alone", "dog with chew toy"],
}


def queries_for(slug: str) -> list[str]:
    return QUERIES.get(slug, [slug.replace("-", " ")])

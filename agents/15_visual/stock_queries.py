"""Consultas de busca (em inglês — os bancos de imagem indexam melhor assim) por artigo,
deliberadamente formuladas para retornar SÓ o animal, nunca uma cena com tutor/pessoa
visível — regra do projeto (personas 100% fictícias, nunca foto de pessoa real associada a
uma autoria fictícia). Quando o tema do artigo inerentemente envolve uma pessoa (ex.: dar
banho, escovar dente, cortar unha), a busca é pelo animal isolado num contexto próximo
(ex.: "cachorro molhado" em vez de "pessoa dando banho no cachorro"), nunca literal.
"""
from __future__ import annotations

QUERIES = {
    # 22/10/2026 (Allan): a capa tem de mostrar o assunto do artigo, nao so um rosto bonito
    "como-escolher-caixa-de-transporte-para-viagem-de-aviao": ["dog in pet carrier", "cat in travel carrier", "pet carrier airplane travel"],
    "como-escolher-cinto-de-seguranca-pet-para-carro": ["dog wearing seat belt in car", "dog car harness back seat", "dog safety car travel"],
    "como-saber-se-o-cachorro-esta-acima-do-peso-ideal": ["overweight dog", "chubby dog", "fat cute dog"],
    "cuidados-essenciais-com-as-patas-de-caes-no-inverno": ["dog paws snow", "dog winter boots snow", "dog walking snow"],
    "quais-legumes-cachorro-pode-comer-cozidos-sem-tempero": ["dog eating carrot", "dog with vegetables", "dog eating vegetables"],
    "como-fazer-caldo-de-ossos-caseiro-para-cachorro": ["dog bone broth bowl", "dog eating from bowl", "dog bone treat"],
    "racao-para-filhote-de-cachorro": ["cute puppy portrait", "adorable puppy playing"],
    "quantas-vezes-por-dia-alimentar-gato": ["cute cat portrait", "happy cat indoors"],
    "alimentos-proibidos-para-cachorro": ["cute dog curious", "happy dog portrait"],
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

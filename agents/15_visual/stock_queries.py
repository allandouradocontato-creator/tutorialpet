"""Consultas de busca (em inglês — os bancos de imagem indexam melhor assim) por artigo,
deliberadamente formuladas para retornar SÓ o animal, nunca uma cena com tutor/pessoa
visível — regra do projeto (personas 100% fictícias, nunca foto de pessoa real associada a
uma autoria fictícia). Quando o tema do artigo inerentemente envolve uma pessoa (ex.: dar
banho, escovar dente, cortar unha), a busca é pelo animal isolado num contexto próximo
(ex.: "cachorro molhado" em vez de "pessoa dando banho no cachorro"), nunca literal.
"""
from __future__ import annotations

QUERIES = {
    "racao-para-filhote-de-cachorro": ["puppy eating food bowl", "puppy dog food bowl"],
    "quantas-vezes-por-dia-alimentar-gato": ["cat eating food bowl", "cat food bowl"],
    "alimentos-proibidos-para-cachorro": ["dog sniffing food", "dog near food table"],
    "como-trocar-a-racao-do-cachorro": ["dog food bowl kibble", "dog eating kibble"],
    "cachorro-latindo-muito-o-que-fazer": ["dog barking", "dog barking outdoor"],
    "gato-arranhando-o-sofa": ["cat scratching furniture", "cat claws sofa"],
    "como-ensinar-cachorro-a-fazer-xixi-no-lugar-certo": ["puppy indoors floor", "puppy sitting indoors"],
    "ansiedade-de-separacao-em-caes": ["dog alone window sad", "dog waiting by door"],
    "como-dar-banho-em-gato": ["wet cat", "cat wet fur"],
    "como-escovar-os-dentes-do-cachorro": ["dog smiling teeth", "dog mouth open teeth"],
    "como-cortar-unha-de-cachorro": ["dog paw close up", "dog paw detail"],
    "como-limpar-caixa-de-areia-do-gato": ["cat litter box", "cat near litter box"],
    "primeiros-dias-do-filhote-em-casa": ["puppy blanket bed", "puppy new home resting"],
    "vacinas-para-filhote-de-cachorro": ["puppy resting calm", "puppy lying down indoors"],
    "como-socializar-filhote-de-gato": ["kittens playing together", "two kittens play"],
    "enxoval-para-filhote-de-cachorro": ["puppy with toys", "puppy bed toys"],
    "caixa-de-transporte-para-gato": ["cat pet carrier", "cat in carrier"],
    "arranhador-para-gato-qual-escolher": ["cat scratching post", "cat scratcher"],
    "coleira-ou-peitoral-para-cachorro": ["dog wearing harness", "dog collar close up"],
    "brinquedos-para-cachorro-que-fica-sozinho": ["dog playing toy alone", "dog with chew toy"],
}


def queries_for(slug: str) -> list[str]:
    return QUERIES.get(slug, [slug.replace("-", " ")])

# Caçador de Ofertas — especificação (rotina diária na nuvem)

Objetivo: todo dia, trazer para a prateleira do painel as ofertas que **já estão
vendendo**, por nicho, Brasil e exterior, com os 9 pontos mapeados, para o cliente
escolher "quero esse" e a Fábrica produzir a versão própria dele.

## 1. Fontes públicas (ordem de prioridade)
| Fonte | O que dá | Sinal de venda | Como ler |
|---|---|---|---|
| Hotmart marketplace (BR) | título, preço, formato, página de vendas, temperatura/avaliações | temperatura, nº avaliações, posição na categoria | WebFetch das páginas públicas de produto por categoria |
| Kiwify / Eduzz / Monetizze vitrines | idem | ranking "mais vendidos" | WebFetch |
| Kindle (BR e US) — mais vendidos por categoria | título, preço, nº avaliações, nota | ranking + avaliações recentes | WebFetch |
| Gumroad Discover / Etsy (digital) / Payhip | título, preço, vendas visíveis | contador de vendas/avaliações | WebFetch |
| Biblioteca de Anúncios da Meta | anúncios ATIVOS, data de início, nº de variações | tempo no ar + nº de variações = está rodando porque vende | Chrome logado quando WebFetch bloquear |
| TikTok / Instagram / Facebook (reels) | vídeo + legenda + comentários | curtidas, compartilhamentos, comentários com "quero/link" | captura em 3 níveis: texto → página do autor → transcrição (Whisper) |

## 2. Critério de sinal (nota 0–100)
- Prova de venda direta (contador, ranking, avaliações recentes): até 40
- Anúncio ativo há mais de 14 dias e/ou 3+ variações: até 30
- Engajamento social com intenção de compra (comentários pedindo link): até 20
- Recorrência: aparece em 2+ fontes: até 10
Entram na prateleira: nota ≥ 60. "Vendendo muito" ≥ 80.

## 3. O que extrair de cada oferta (os 9 pontos)
1. **Produto:** formato (e-book, app, planilha, bundle), tamanho, promessa com prazo, mecanismo com nome próprio.
2. **Oferta:** preço, âncora, parcelas, bônus, garantia, urgência (real ou falsa), order bump.
3. **Tráfego/criativo:** tipo de criativo (depoimento, antes/depois, lista, pergunta), gancho, CTA, isca por comentário.
4. **VSL:** existe? duração, estrutura (dor→história→método→prova→oferta), narrador real ou avatar.
5. **Landing:** blocos na ordem, prova social (prints, vídeos), comparação "curso × produto pronto", FAQ.
6. **Checkout:** plataforma, bump, parcelamento, selo de garantia, banner.
7. **Pós-venda:** upsell visível, grupo/comunidade, e-mail/WhatsApp.
8. **Suporte:** canal prometido, prazo, reembolso.
9. **Medição:** pixel/tags visíveis no código público da página (Meta Pixel, Clarity, GA).

Saída por oferta: JSON com os 9 campos + nota + nicho + região + link da fonte + "padrão a aproveitar" (1 linha) + 3 riscos (promessa de renda/cura, CNPJ ausente, reembolso).

## 4. Regras duras
- Só o que é público. Nunca criar conta, comprar, baixar conteúdo pago, entrar em área de membros, contatar vendedor.
- Nunca copiar texto, imagem, capa, layout ou marca. A prateleira mostra **capa gerada pela Fábrica** com os dados; a original fica no link.
- Nada de promessa de renda ou cura na "versão própria": o guardião de conformidade bloqueia.
- Dedup: mesma oferta em várias fontes = 1 item com soma de sinais.
- Nichos iniciais: pet, fitness, coaching, oratória, receitas, finanças, relacionamentos, espiritualidade, beleza, maternidade/infantil, concursos, artesanato/renda extra. Novo nicho entra quando 3+ ofertas com nota ≥ 60 aparecerem.

## 5. Rotina
- Diária, 06:00 (America/Fortaleza), na nuvem (GitHub Actions do repo, igual à fábrica Tutorial Pet). Custo: modelo barato (Jev/OpenRouter) para extração; modelo forte só para o resumo "padrão a aproveitar".
- Produz `data/cacador/YYYY-MM-DD.json` + atualiza `prateleira.json` (top 60 por nicho, 30 dias de vida).
- Terça e sexta, o Triagem escolhe 1–3 destaques e manda para o Painel de Decisões.
- Toda falha de captura vira linha no Livro de Gaps (fonte, erro, contorno).

## 6. Versão própria (o PLR da Fábrica)
Entrada: oferta escolhida + **estudo de voz** do cliente (1 texto dele ou 1 min de áudio) + foto.
- Estudo de voz extrai: vocabulário recorrente, ritmo de frase, humor, como abre e fecha uma ideia, expressões próprias. Guardado no Cofre (na plataforma).
- Produto: **estrutura nova** (nunca o mesmo sumário), capítulos escritos do zero no tom do cliente, exemplos do contexto dele, capa com a foto dele e paleta da marca dele.
- Checagem anti-repetição: similaridade com a referência e com outras versões já geradas abaixo do limiar; se passar, regera o trecho.
- Tradução/adaptação de referência estrangeira: não é tradução literal — é adaptação cultural (exemplos, moeda, leis, marcas locais).
- Qualidade mínima: revisão automática (coerência, promessas, ortografia), prévia obrigatória antes de publicar, crédito só cobrado no fim.

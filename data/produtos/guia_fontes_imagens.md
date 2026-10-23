# Guia: fontes de imagem gratuitas com chave de API (Tutorial Pet)
Criado em 22/10/2026. Objetivo: abastecer e-books, fichas e landing com fotos de pet sem repetir. Só pesquisa: nenhuma conta foi criada, nenhuma chave foi digitada.

Legenda: [CONF] = confirmado em página oficial/fonte lida hoje. [NÃO CONF] = veio de memória ou de fonte secundária; conferir antes de depender.

## Resumo rápido
| Fonte | Chave? | Limite grátis | Atribuição | Serve p/ PDF | Nota pet |
|---|---|---|---|---|---|
| Pexels | sim (já temos) | 200/h e 20.000/mês [CONF] | link visível ao Pexels na chamada [CONF] | sim (ver ressalva) | 8 |
| Pixabay | sim (Allan tem conta) | 100/min ou 5.000/h [NÃO CONF] | não exigida [CONF] | sim | 7 |
| Unsplash | sim (Access Key) | Demo 50/h [CONF] | obrigatória [CONF] | arriscado | 8 |
| Flickr | sim | 3.600/h chave não comercial [NÃO CONF] | depende da licença CC | sim, só licenças comerciais | 6 |
| Openverse | opcional | anônimo baixo; registrado maior [números NÃO CONF] | depende da licença | sim | 5 |
| Wikimedia Commons | não | sem número fixo; exige User-Agent [NÃO CONF] | depende | sim, com cuidado | 4 |
| Coverr (vídeo) | sim | Demo 50/h [CONF] | página da API não diz [NÃO CONF] | só vídeo | 3 (vídeo geral) |
| Pexels Videos (vídeo) | mesma chave do Pexels | mesmo limite | mesma regra do Pexels | só vídeo | 8 |

"Flash": Allan escreveu "Flash". Não existe API de imagens com esse nome que eu conheça; a hipótese mais provável é **Flickr** (som parecido). DÚVIDA a confirmar com ele em 1 pergunta: "era Flickr?". Se ele quis dizer outra coisa (ex.: Freepik, "Flaticon"), o guia ganha uma seção.

---
## 1. Pexels (já temos chave)
- Cadastro/chave: https://www.pexels.com/api/ [CONF]
- Passos (só se precisar de nova chave): 1) entrar na conta Pexels. 2) abrir pexels.com/api. 3) clicar em "Your API Key" / pedir a chave; sai na hora [CONF]. 4) copiar.
- Onde aparece a chave: na própria página pexels.com/api, depois de logado.
- Limite: 200 requisições/hora e 20.000/mês; dá para pedir aumento, e o texto oficial diz que quem cumpre os termos pode ter ilimitado grátis [CONF]. Cabeçalhos X-Ratelimit mostram o saldo.
- Licença/atribuição: uso livre dentro das diretrizes; a doc exige "link proeminente ao Pexels" e pede crédito ao fotógrafo ("Photo by Fulano on Pexels") quando possível [CONF].
- E-book PDF e redes: sim. Colocar crédito na página de créditos do e-book e na legenda quando couber.
- Risco: não replicar o Pexels (app de wallpaper etc.); não burlar o limite. Pessoas reconhecíveis e marcas aparecem em fotos: evitar.
- Nota pet: 8.

## 2. Pixabay (Allan já tem conta, entrou com Google em 13/09)
- Link: https://pixabay.com/api/docs/ (a página oficial foi bloqueada pela allowlist; dados abaixo vêm de espelho/doc de terceiro, marcados) 
- Passos: 1) abrir https://pixabay.com/api/docs/ já logado (Google). 2) a chave aparece em destaque no texto da doc, na seção "Search Images", no parâmetro `key` (o site mostra "Your API key: ..." só para logado) [NÃO CONF: posição exata na página]. 3) copiar.
- Limite: um espelho de doc diz 5.000 req/hora por chave; a doc oficial que eu lembro diz 100 req/60 s. Números divergem: tratar como 100/min até confirmar [NÃO CONF]. Aumento mediante pedido se a integração for correta.
- Regras (via espelho de doc, [parcial]): "Systematic mass downloads are not allowed"; respostas devem ser cacheadas por 24 h; uso para pedidos reais, não varredura automática. Mostrar a origem (link ao Pixabay) quando exibir resultados de API. A doc oficial também diz que as URLs de imagem da API não devem ficar em hotlink permanente (baixar a imagem escolhida para o nosso servidor) [NÃO CONF].
- Licença (página oficial lida): uso grátis, comercial permitido, sem atribuição obrigatória, pode modificar. Proibido: vender/distribuir sem alteração criativa (não revender a foto pura), marcas/logos reconhecíveis em uso comercial, pessoas reconhecíveis em uso indevido/enganoso, usar como parte de marca [CONF].
- E-book PDF e redes: sim, é a mais tranquila de licença.
- Risco: o caminho "baixar centenas" fere a regra de download em massa. Buscar por tema, escolher a foto, baixar só as usadas, cache 24h.
- Nota pet: 7 (muito volume de cães/gatos, qualidade variável, algumas com estética de banco antigo).

## 3. Unsplash
- Cadastro: https://unsplash.com/join e depois https://unsplash.com/oauth/applications [CONF]
- Passos: 1) criar conta (ou entrar com Google). 2) abrir unsplash.com/oauth/applications e aceitar virar "developer". 3) clicar em "New Application". 4) marcar as caixas dos termos, dar nome (ex.: "Tutorial Pet") e descrição curta. 5) criar.
- Onde aparece a chave: página do app > "Keys": **Access Key** (a que usamos) e Secret Key (não usar nem expor) [CONF: os dois nomes]. 
- Limite: modo Demo 50 req/hora; Production 1.000/h após aprovação. Só chamadas a api.unsplash.com contam; o carregamento de images.unsplash.com não conta [CONF].
- Regras (diretrizes lidas): creditar Unsplash E o fotógrafo com link para o perfil dele, links com `utm_source=NOME_DO_APP&utm_medium=referral`; carregar imagens pelas URLs `photo.urls` da API (hotlink); ao "baixar/escolher" uma foto, chamar `photo.links.download_location`; não vender foto sem alteração; não clonar o Unsplash; manter chaves em sigilo [CONF]. A página não tem regra específica para PDF/offline: dúvida vai para api@unsplash.com [CONF].
- E-book PDF: ZONA CINZENTA. Hotlink + registro de download são pensados para app web. Para PDF impresso/baixado sem URL ao vivo, não está claro. Usar só como complemento, com crédito + link no e-book, ou escrever ao Unsplash. Para landing/redes, ok com crédito.
- Pedido para Production exige mostrar conformidade; Demo 50/h basta para nós.
- Risco: estética muito "premium", ótimas fotos; crédito obrigatório em tudo.
- Nota pet: 8.

## 4. Flickr (provável "Flash")
- Cadastro: https://www.flickr.com/services/apps/create/ [CONF] e o formulário "Request an API Key" (apply) [CONF via Openverse handbook: "apply for a key at flickr.com/services/apps/create/apply as non-commercial"].
- Passos: 1) criar conta Flickr (exige conta Yahoo/Flickr; Google não é login nativo) [NÃO CONF]. 2) abrir flickr.com/services/apps/create/. 3) escolher "Apply for a Non-Commercial Key" (rápido) ou "Commercial". 4) nome do app, o que faz, aceitar termos. 5) enviar; a chave e o "secret" aparecem na hora para não comercial.
- Onde aparece a chave: página "Your API Keys" (flickr.com/services/apps/by/SEU_USUARIO) [NÃO CONF: URL exata].
- Limite: 3.600 consultas/hora por chave não comercial [NÃO CONF, só fonte terciária].
- Licença: o filtro é o parâmetro `license` do `flickr.photos.search`. IDs de licença que permitem uso comercial: 4 (CC BY), 5 (CC BY-SA), 6 (CC BY-ND), 7 (sem restrições conhecidas), 8 (US Gov), 9 (CC0), 10 (Public Domain Mark). Evitar 1, 2, 3 (NC) e 0 (todos os direitos reservados). Usar `license=4,5,7,9,10` e evitar 6 (ND, sem editar/cortar) [NÃO CONF: lista de IDs veio de memória; conferir em flickr.photos.licenses.getInfo].
- Atribuição: BY e BY-SA exigem crédito (autor, título, licença, link). Guardar esses campos no registro de cada foto.
- E-book PDF: sim, só licenças comerciais, com crédito.
- RISCO GRANDE: nosso uso é comercial (e-books vendidos). Chave "não comercial" para app comercial viola os termos; o correto seria chave comercial (revisão manual do Flickr) [NÃO CONF: detalhes]. Alternativa sem risco: acessar o Flickr via Openverse (filtra licença e traz atribuição pronta). Também há risco de pessoas identificáveis nas fotos (direito de imagem) e licença errada marcada pelo autor.
- Nota pet: 6 (muito conteúdo amador/real, bom para variedade e raças específicas, qualidade irregular).

## 5. Openverse (WordPress)
- Documentação/API: https://api.openverse.org/ e https://openverse.org [página bloqueada hoje; dados de espelhos]
- Sem chave: busca pública funciona; anônimo tem limite baixo e `page_size` máx. 20 [CONF via post oficial do Openverse].
- Registro opcional (limites maiores) [NÃO CONF nos detalhes, vem de memória]: 1) POST `https://api.openverse.org/v1/auth_tokens/register/` com `name`, `description` e `email`. 2) a resposta traz `client_id` e `client_secret` (só aparecem uma vez; guardar). 3) o e-mail recebe link de verificação (precisa confirmar). 4) pedir token em `/v1/auth_tokens/token/` (client_credentials); o token vale ~12 h.
- Limite: anônimo ~100/dia e 5/h; registrado ~10.000/dia e 100/min [NÃO CONF: valores de memória].
- Licença: agrega vários acervos (inclui Flickr e Wikimedia); a resposta traz licença, autor e texto de atribuição pronto. Filtrar `license_type=commercial`.
- E-book PDF: sim, com a atribuição que a API devolve.
- Risco: a qualidade/licença depende da fonte original; conferir sempre a página de origem.
- Nota pet: 5.
- ALERTA: o e-mail do Allan está com Gmail cheio; o link de verificação pode não chegar. Usar o e-mail da empresa, se houver.

## 6. Wikimedia Commons
- Sem chave. API: https://commons.wikimedia.org/w/api.php (pesquisa por `action=query&generator=search&gsrnamespace=6&prop=imageinfo&iiprop=url|extmetadata`) [NÃO CONF: parâmetros de memória].
- Passos: nenhum cadastro. Definir um **User-Agent** que identifique o projeto e contato (política Wikimedia) [NÃO CONF: página de política indisponível].
- Licença: varia por arquivo (CC BY, CC BY-SA, CC0, domínio público). A página oficial de reutilização manda: conferir a licença do arquivo, creditar o autor original (não só quem enviou), considerar direitos de personalidade e marcas [CONF].
- E-book PDF: sim, com o campo `extmetadata` (LicenseShortName, Artist, AttributionRequired) guardado.
- Risco: licenças misturadas (SA exige compartilhar igual), fotos de pessoas, acervo mais enciclopédico que "fofo".
- Nota pet: 4 (bom para raças/espécies específicas e domínio público, ruim para estética de marca).

## 7. Extras gratuitos que valem
### 7a. Pexels Videos (vídeo, mesma chave do Pexels)
- Endpoint de vídeo da mesma API (`/videos/search`) [NÃO CONF: endpoint de memória, API confirmada em pexels.com/api]. Mesma regra de crédito/limite. Serve para Reels/Shorts/TikTok. Nota pet: 8.
### 7b. Coverr (vídeo)
- Link: https://coverr.co/developers (perfil: coverr.co/profile/api) [CONF].
- Passos: 1) criar conta em coverr.co. 2) abrir coverr.co/developers. 3) criar um aplicativo. 4) a chave sai na hora [CONF].
- Limite: Demo 50/h; Production 2.000/h exige assinatura Pro/Ultimate (pago) [CONF].
- Licença/atribuição: a página da API não diz; ver https://coverr.co/license [NÃO CONF: não li].
- Serve só para vídeo de redes. Nota pet: 3 (acervo geral, pouco pet).
### 7c. Freepik / StockSnap / Burst
- Freepik: API existe, mas a página oficial redirecionou para "Magnific" e não confirmei plano grátis nem exigência de atribuição. Normalmente o conteúdo grátis do Freepik exige crédito; NÃO usar até confirmar [NÃO CONF]. Nota pet: 5.
- StockSnap e Burst (Shopify): não confirmei se oferecem API pública com chave hoje. Podem ser usados manualmente (CC0 / uso livre), mas não entram na automação [NÃO CONF]. Nota pet: StockSnap 5, Burst 5.

---
## (a) Onde guardar cada chave
Segredos do GitHub: https://github.com/allandouradocontato-creator/tutorialpet/settings/secrets/actions (botão "New repository secret"). A chave só no Chrome normal do Allan (painel lateral do chat não cola segredo).
| Fonte | Nome do segredo |
|---|---|
| Pexels (já existe) | PEXELS_API_KEY (conferir o nome que já está no GitHub) |
| Pixabay | PIXABAY_API_KEY |
| Unsplash | UNSPLASH_ACCESS_KEY (NÃO guardar o Secret Key; se guardar, UNSPLASH_SECRET_KEY) |
| Flickr | FLICKR_API_KEY (+ FLICKR_API_SECRET) |
| Openverse | OPENVERSE_CLIENT_ID e OPENVERSE_CLIENT_SECRET |
| Coverr | COVERR_API_KEY |
| Wikimedia | nenhum (só o User-Agent no código) |

## (b) Ordem recomendada de cadastro (mais rápido primeiro)
1. **Pexels**: já feito. 0 min. Conferir só o nome do segredo.
2. **Pixabay**: conta já existe; só abrir a doc logado e copiar a chave. ~2 min.
3. **Unsplash**: criar app, Access Key na hora. ~5 min.
4. **Wikimedia Commons**: sem cadastro (só código). 0 min de Allan.
5. **Openverse**: opcional, ~5 min, depende de e-mail. Só se bater limite.
6. **Flickr**: por último; pede conta Flickr e decisão sobre chave comercial. Pergunta a Allan: "Flash era Flickr?".
7. **Coverr**: só se o plano de vídeo precisar.

## (c) O que o Claude faz depois que cada chave existir
- Pexels/Pixabay/Unsplash: testar a chave com 1 busca ("cachorro filhote") sem imprimir a chave; gravar o nome do segredo em `config/`; criar um módulo único `buscar_imagem(tema, raça)` que consulta as fontes em rodízio.
- Banco anti-repetição: registrar em um arquivo `data/imagens/usadas.json` o ID de cada foto usada (fonte+id), produto onde entrou, crédito e licença; a busca descarta IDs já usados e pega a próxima página.
- Créditos: gerar automaticamente a página "Créditos das imagens" de cada e-book/ficha/landing (Unsplash e Pexels com link; Flickr/Openverse/Commons com autor+licença).
- Pixabay: cache de 24 h, baixar só as imagens escolhidas, nunca em lote.
- Unsplash: chamar `download_location` ao escolher a foto; manter utm_source=tutorialpet.
- Raça certa: filtrar por palavra-chave da raça e checar a foto antes de entrar na produção (regra do Allan: conteúdo que cita raça mostra aquela raça).
- Flickr/Openverse/Commons: só licenças comerciais; guardar autor, licença e URL de origem.
- Se Allan responder o que é "Flash", incluir.

## Não confirmado nesta pesquisa (resumo)
Páginas oficiais bloqueadas: Pixabay API docs, Flickr (guia de chaves/TOS), Openverse docs, Wikimedia access policy. Limites do Pixabay (divergentes), Flickr, Openverse, IDs de licença Flickr, política de User-Agent da Wikimedia, licença do Coverr, plano grátis do Freepik, API de StockSnap/Burst, uso do Unsplash em PDF.

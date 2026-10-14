# Créditos das fotos — Sozinho em Casa

Fontes reconstituídas em 21/09/2026 a partir do histórico do git e do
`_scratch` do falcao-hq — não existia arquivo de créditos antes deste.
Onde não achei fotógrafo nem URL, está escrito "crédito não localizado":
nada aqui foi inventado.

## Em uso na landing (`index.html`)

- **fofo.jpg** — Pexels (plataforma confirmada pela mensagem do commit
  `3b18ef5`: "candidatas do Pexels aprovadas no checklist de 8 itens").
  Fotógrafo e URL: **crédito não localizado**. Arquivo trazido de volta em
  21/09/2026 do `_scratch/sozinho-anteriores/` do falcao-hq, decisão do
  critério de persuasão.
- **passeio.jpg** — Pexels (mesma origem e mesma ressalva de `fofo.jpg`).
  Fotógrafo e URL: **crédito não localizado**. Trazido de volta em
  21/09/2026, mesma decisão.
- **ansiedade.jpg** — sem fonte documentada em nenhum commit. Entrou no
  repositório em `05a79f0` como "trabalho local de 17/09" já pronto, sem
  menção de plataforma. Fotógrafo, plataforma e URL: **crédito não
  localizado**.
- **dupla-feliz.jpg** — mesma situação de `ansiedade.jpg`: entrou junto,
  sem fonte documentada. Fotógrafo, plataforma e URL: **crédito não
  localizado**.
- **arranhao-porta.jpg** — extraída em 21/09/2026 de um `<img>` com a foto
  embutida em base64 dentro do próprio `index.html` (arquivo pesado,
  ~250 KB só de texto). Não havia legenda com crédito nem link de origem
  no HTML de onde saiu. Fotógrafo, plataforma e URL: **crédito não
  localizado**. Sem string de URL no metadata do arquivo (conferido por
  busca binária).
- **cao-porta-fechada.jpg** — mesma situação de `arranhao-porta.jpg`:
  segunda imagem embutida em base64 no `index.html` antigo, sem crédito
  em lugar nenhum. Fotógrafo, plataforma e URL: **crédito não localizado**.
- **ansiedade-olhos.jpg** — recorte de `ansiedade.jpg`, feito em 21/09/2026
  (rebalanceamento de imagem x texto). Herda o mesmo crédito não localizado
  do arquivo original — não é foto nova.
- **arranhao-detalhe.jpg** — recorte de `arranhao-porta.jpg`, mesma data e
  mesmo motivo. Herda o mesmo crédito não localizado do original.

## Histórico relevante

Estas três fotos passaram por duas trocas antes do estado atual:

1. `05a79f0` (17–19/09) — conjunto original das 4 fotos.
2. `3b18ef5` (19/09) — `ansiedade`, `fofo` e `passeio` substituídas por
   candidatas do Pexels aprovadas no critério de design técnico de 8 itens.
3. `93e6ed4` (19/09) — outra sessão preferiu as 3 originais de volta.
4. **21/09/2026** — o falcao-hq reavaliou pelo critério de persuasão
   (`criterio-persuasao.md`) e decidiu posição por posição: `ansiedade.jpg`
   fica a versão atual (a de `93e6ed4`, cobertura neutra — a versão de
   janela/parede de pedra lia como resgate/prisão); `fofo.jpg` e
   `passeio.jpg` voltam para as versões de `3b18ef5` (as mesmas que este
   arquivo já chama de "crédito não localizado" acima).
5. **21/09/2026** — as duas fotos que viviam embutidas em base64 direto no
   `index.html` (foto da porta arranhada e do cão de costas diante da
   porta) foram extraídas para `arranhao-porta.jpg` e
   `cao-porta-fechada.jpg`, seguindo o item do plano de landing que pede
   arquivo separado, cacheável, em vez de imagem embutida — isso sozinho
   derrubou o `index.html` de ~250 KB para ~45 KB.

## Se algum dia alguém achar a fonte real

Antes de publicar em qualquer lugar fora deste projeto, vale procurar a
fonte de novo — os arquivos têm metadata EXIF que pode ter sobrevivido ao
redimensionamento, e a licença Pexels não exige atribuição, mas cita-se
aqui por boa prática assim que aparecer.

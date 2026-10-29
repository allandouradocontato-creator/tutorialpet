# Plano de execução (Sonnet) — 29/10/2026 11:40 — Kit Rotina Pré-Saída vira BÔNUS do checkout
Decisão do Allan (29/10 11:37), análise do Fable. Executar na ordem. Não mexer em landing, anúncios, verba nem preço. Depende do plano anterior (plano_execucao_sonnet_2026-10-29_checkout.md), já executado: bump removido, produto renomeado, texto de preço/garantia no topo do Checkout A.

## Por quê
O bump "Kit Rotina Pré-Saída R$ 19,90" dizia ao comprador que os R$ 27 não bastavam. Como bônus incluído, a mesma peça vira ganho ("leva mais do que paga"), custo zero (digital, pronto). Padrão de checkout de ticket baixo que converte: produto + bônus com valor declarado.

## 1. Texto do bônus no Checkout A (Kiwify, Chrome logado em dashboard.kiwify.com.br)
Produto "Sozinho em Casa — Manual + Aplicativo (plano de 14 dias)" (id 749af310-bc0b-11f1-b8e9-4b1a1fc1d379) > aba Checkout > menu do "Checkout A" > Personalizar (abre nova aba do builder).
- Editar o componente Texto que já existe no topo (hoje: "R$ 27 à vista · pagamento único · Garantia de 14 dias (o tempo do plano inteiro). Acesso imediato ao app e ao manual."). Deixar em 3 linhas curtas, nesta ordem:
  1. "R$ 27 à vista · pagamento único · Acesso imediato ao app e ao manual."
  2. "Bônus incluído: Kit Rotina Pré-Saída (R$ 19,90) — grátis nesta compra."
  3. "Garantia de 14 dias (o tempo do plano inteiro)."
  Se o builder não quebrar linha dentro do mesmo Texto, arrastar 2 componentes Texto a mais para a mesma área do topo (um por linha). Fonte menor que a atual (a atual está enorme no desktop): se houver controle de tamanho, usar tamanho de subtítulo; se não, deixar.
- Salvar checkout. Abrir https://pay.kiwify.com.br/NcQChat na mesma aba do Chrome e confirmar as 3 linhas. Print (save_to_disk) para o Allan.

## 2. Entregar o Kit dentro da Área de Membros do Sozinho em Casa
- Kiwify > Área de Membros > área do produto Sozinho em Casa > novo módulo "Bônus: Kit Rotina Pré-Saída — Faro, Recheios e Planner de 14 Dias".
- Conteúdo: os mesmos arquivos do produto "Kit Rotina Pré-Saída" (R$ 19,90). Onde achar: primeiro no repo (tutorialpet e sozinho-em-casa-app: procurar "kit", "rotina", "pre-saida", "planner" em data/, produtos/, landing/); se não estiver, abrir a Área de Membros do produto Kit na Kiwify e baixar/re-anexar de lá. Não perguntar ao Allan onde está.
- Nomes de arquivo limpos (só nome do produto, sem "v2"/"CORRIGIDO"). Links clicáveis.
- Conferir como aluno se a Kiwify permitir (prévia da área), senão conferir que o módulo aparece publicado.

## 3. Linha de fundamentação científica (condicional)
- Abrir o manual do Sozinho em Casa (PDF no repo ou na Área de Membros) e verificar se ele cita fontes/protocolos (dessensibilização, contracondicionamento, referências de comportamentalistas/veterinários).
- Se cita: acrescentar no bloco do topo do checkout a 4ª linha "Manual com base em protocolos de dessensibilização usados por comportamentalistas." Se NÃO cita de forma verificável: não escrever nada (regra 35: alegação só com verificação no produto) e registrar na ficha que a linha ficou de fora e por quê.

## 4. Registro e commit
- Ficha data/anuncios/campanha_vsl_v12_sp.md: seção "Atualização 29/10/2026 (bônus)" com hora de cada item, o que foi feito e o que não foi.
- Se algo novo deu errado: 1 linha em data/memoria/07 Erros e lições.md.
- Commit com as linhas de atribuição da sessão e push (pull --rebase se recusar).
- Relatório curto ao Allan com o print do checkout.

## O que NÃO fazer
- Não mexer na landing (menção ao bônus na landing só depois da leitura de 30/10 09:00).
- Não trocar a ordem "Manual + Aplicativo" (troca combinada em anúncio+landing+checkout, depois da leitura).
- Não reativar o order bump, não criar cupom, não mexer em preço/parcelamento/verba.

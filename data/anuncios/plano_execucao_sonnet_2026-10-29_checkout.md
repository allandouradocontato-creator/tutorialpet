# Plano de execução (Sonnet) — 29/10/2026 11:20 — destravar a 1ª venda: checkout primeiro
Análise do Fable sobre a leitura das 11h (campanha 120253387444780134). Decisões tomadas; não reabrir. Executar só depois do "pode" do Allan. Ordem: 1 → 2 → 3. Nada de mexer na landing nem nos criativos.

## Diagnóstico (lido na fonte, 29/10 10:50-11:15)
- Funil 28/10 20:00 → 29/10 10:50: R$ 22,30 · 1.026 impressões · 51 cliques (CTR 5,0%) · 46 visualizações da landing · 4 checkouts iniciados (8,7% da landing) · 0 compras.
- Kiwify (dashboard, aba "Todas"): só 3 vendas na vida do produto, todas de teste do próprio Allan (set/2026). Nenhum pedido recusado, pendente ou Pix gerado: os 14 visitantes de checkout (4 de agora + 10 dos 28 dias anteriores) saíram ANTES de clicar em "Pagar agora". O vazamento é a página de checkout, não o pagamento, não a landing, não o anúncio.
- Checkout pay.kiwify.com.br/NcQChat como o comprador vê:
  1. Título "Sozinho em Casa — Manual do Protocolo de 14 Dias": não cita o app. O anúncio e a landing vendem "manual + app". Quebra de message match.
  2. O preço R$ 27 NÃO aparece em lugar nenhum; o único número visível é "6x de R$ 5,07" (= R$ 30,42 com juros). O comprador vê um número maior que o prometido.
  3. Order bump "Kit Rotina Pré-Saída R$ 19,90" AINDA ATIVO (decisão de 20/10 de desativar não foi executada), com o texto "a parte do protocolo que mais decide o resultado": diz ao comprador que os R$ 27 não bastam. Pior frase possível num checkout.
  4. Cartão é o meio pré-selecionado; Pix existe mas é a 3ª aba. Sem menção à garantia de 14 dias nem a "acesso imediato".
- Por posicionamento: Instagram Feed gastou R$ 2,56 para 1 clique (124 impressões); Facebook (feed+reels) R$ 0,38/clique e 3 dos 4 checkouts; Instagram Reels do B deu 1 checkout com 4 cliques (manter).
- Retenção do vídeo baixa (25% assistido por ~15%, completo por 1-3%), mas CTR alto: as pessoas clicam cedo. Não é problema agora; a VSL da landing explica. Observar.

## 1. Consertar o checkout da Kiwify (hoje, grátis, Chrome já logado em dashboard.kiwify.com.br, produto do link NcQChat)
a. Desativar o order bump "Kit Rotina Pré-Saída" (Produtos > Sozinho em Casa > Order bump). Decisão do Allan de 20/10, nunca executada.
b. Renomear o produto para "Sozinho em Casa — Manual + Aplicativo (plano de 14 dias)". Igual ao que o anúncio e a landing prometem.
c. Fazer o preço R$ 27 aparecer no checkout (configuração do checkout: exibir resumo/valor do pedido; se não houver, colocar "R$ 27 à vista · pagamento único" no banner/descrição do checkout).
d. Pix como forma pré-selecionada (configuração do checkout, se a Kiwify permitir; se não, deixar).
e. Adicionar no checkout o selo/texto de garantia: "Garantia de 14 dias (o tempo do plano inteiro). Acesso imediato ao app e ao manual." (elemento de garantia do construtor de checkout da Kiwify).
f. Ligar a recuperação de carrinho abandonado da Kiwify (e-mail automático grátis), se existir na conta.
g. Conferir no celular (abrir o checkout em viewport 390×844 no playwright) e mandar print: título, preço, Pix, garantia visíveis, bump sumido.
Registrar cada item na ficha campanha_vsl_v12_sp.md com hora.

## 2. Posicionamentos (API Windsor, update_adset 120253387467550134)
- Remover Instagram Feed (instagram_positions fica só ["reels"]). Manter Facebook feed + facebook_reels e Instagram Reels. Reenviar o targeting COMPLETO (regions [{key 460}], idade 25-65 + age_range [25,55], advantage_audience 1) e ler de volta com campos diferentes (cache). Orçamento e datas intactos.
- Motivo: R$ 0,38/clique no Facebook contra R$ 2,56 no Instagram Feed; amostra pequena, mas o custo é 6x e a mudança é reversível.

## 3. Verba — NÃO subir hoje
- Manter R$ 30/dia até o checkout estar consertado e a leitura de amanhã 09:00 mostrar pelo menos 1 Pix gerado ou venda. Subir verba com checkout vazando compra mais vazamento.
- Se amanhã houver Pix gerado/venda: propor ao Allan R$ 50/dia (fora do teto 10-30 da skill, precisa do "pode" dele) para chegar a 300 cliques até 31/10 e ter leitura confiável do checkout.
- Regra do preço R$ 17 (≥100 visitas e 0 vendas em 3 dias): SUSPENSA até o checkout estar consertado; ninguém chegou a gerar Pix, então preço não é a causa. Reavaliar em 31/10 com checkout novo.

## O que NÃO fazer
- Não mexer na landing: 8,7% landing→checkout está acima do típico de tráfego frio para ticket baixo (2-5%); mudar agora destrói o único sinal limpo.
- Não pausar o anúncio A: B lidera (3 checkouts contra 1) mas n=4 não decide; regra da ficha (R$ 54 sem venda) ainda não atingida.
- Não trocar criativo, não mexer em público além do item 2.

## Leitura de amanhã (29/10 → 30/10 09:00)
Comparar checkouts iniciados × Pix gerados/pedidos na Kiwify (aba Todas) × compras. Se houver pedidos gerados e não pagos: o problema passou a ser pagamento (aí cabe recuperação). Se houver venda: subir verba (item 3).

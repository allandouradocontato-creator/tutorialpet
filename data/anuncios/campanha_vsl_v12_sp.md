# Campanha Meta Ads — Sozinho em Casa, VSL v12 (preparada em 28/10/2026, aguardando "pode" do Allan)
Fonte das regras: biblioteca/habilidades/trafego_meta_ads.md + anuncios_meta_decisao.md + marketingskills/ads/references/meta-andromeda-playbook.md.
Conta de anúncios 1213984913380523 (Allan Dourado) · Página Tutorial Pet 1251330151406637 · Pixel 2135885120651427 · Landing https://sozinho.tutorialpet.com.br (R$ 27, garantia 14 dias).

## Estrutura (1 campanha, 1 conjunto, 2 anúncios)
- Campanha: "Sozinho em Casa - VSL v12 - SP apartamento - teste 3 dias" · objetivo OUTCOME_SALES · criada PAUSADA.
- Conjunto: otimização INITIATE_CHECKOUT (pixel 2135885120651427; a Kiwify dispara InitiateCheckout e Purchase; histórico: 10 checkouts em 28 dias, 0 compras — Purchase ainda não tem dado para o Meta aprender). Posicionamentos: Reels + Feed (FB/IG); Audience Network desligado. Orçamento R$ 30/dia × 3 dias = R$ 90 (teto da faixa 10–30/dia da skill). Início/fim fixos (3 dias).
- Público (pedido do Allan 25/10 + 28/10): Brasil, estado de São Paulo (RMSP prioridade), 25–55, público Advantage+ com sinais: Cães, Adestramento de cães, Petz/Cobasi/Petlove, Comportamento animal. "Apartamento" não é interesse confiável no Meta: quem seleciona o apartamento é o CRIATIVO (vizinho reclamando, corredor, porta do apartamento) — playbook Andromeda: "creative is the targeting".
- Anúncio A (problema): texto "Travesseiro virou confete, sofá arranhado e o vizinho reclamando do latido? O Sozinho em Casa é um plano de 14 dias de atividades práticas, com app que ajusta os exercícios ao porte, à raça e ao temperamento do seu cachorro. R$ 27, pagamento único. Garantia de 14 dias: fez o plano e não gostou? Devolvemos tudo." · Título "Sozinho em Casa: manual + app, R$ 27" · Botão COMPRAR AGORA.
- Anúncio B (benefício): texto "Em 14 dias, o latido acaba, o vizinho sossega e você sai de casa em paz. Sozinho em Casa: manual + aplicativo, R$ 27 (de R$ 97), pagamento único, garantia de 14 dias sem perguntas." · Título "Plano de 14 dias com app · R$ 27" · Botão COMPRAR AGORA.
- Vídeo: VSL_A_Instagram_v12_tarja_produto_genero_neutro.mp4 (62,7 s, 9:16) — URL pública: https://raw.githubusercontent.com/allandouradocontato-creator/tutorialpet/media/anuncios/VSL_A_Instagram_v12_tarja_produto_genero_neutro.mp4 · capa: .../anuncios/VSL_A_v12_thumb_duda.jpg
- UTM: utm_source={{site_source_name}}&utm_medium=paid&utm_campaign=sozinho_vsl_v12_sp&utm_content={{ad.name}}
- Conformidade: sem "resolve ansiedade de separação", sem "seu cachorro tem…", sem saúde; Duda é IA fotorrealista → marcar "conteúdo gerado por IA" no Gerenciador antes de ativar.

## Critérios de leitura (regra anuncios_meta_decisao, 1 decisão por leitura, diário)
- Gastou R$ 54 (2× preço) sem venda e CTR abaixo da mediana da conta → pausar o anúncio.
- CPM normal e checkout sem venda → problema é landing/oferta, não o anúncio.
- Frequência > 3 e CTR caindo 1/3 → fadiga → criativo novo (não subir verba).
- Desvio combinado em 20/10: ≥ 100 visitas reais e 0 vendas em 3 dias → preço cai para R$ 17 por 3 dias.

## Bloqueio atual
Windsor: "Write actions are disabled" para allandouradocontato@gmail.com. Para o Claude criar a campanha pausada pela API, o Allan liga em https://onboard.windsor.ai/app/settings/account → "Enable write actions for Claude, ChatGPT & API". Alternativa: Claude cria no Gerenciador pelo navegador.

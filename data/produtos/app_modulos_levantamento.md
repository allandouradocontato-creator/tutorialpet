# App Sozinho em Casa: levantamento para liberar módulos por compra (B1, 22/10/2026, só leitura)

Fontes: repo allandouradocontato-creator/sozinho-em-casa-app (privado, commit 9d0bbd7), config/produtos_landing/sozinho-em-casa.yaml, landing/obrigado.html, data/memoria. Nenhum código alterado, nenhum segredo lido.

## 1) Como funciona hoje
- **Sem login e sem verificação de pagamento.** O app é um PWA estático (HTML/JS puro em `landing/app/`, manifest + service worker; conteúdo em `content.json` de 19 KB, todo público). Progresso fica no `localStorage` do aparelho (exportar/importar .json). Não existe webhook, banco, senha nem token no código.
- **Acesso = quem tem o link.** A Kiwify entrega por e-mail o botão "Acessar meu produto", que aponta para `https://sozinho.tutorialpet.com.br/app/` (também usado na página de obrigado). O link é o mesmo para todos; o `robots.txt` bloqueia buscadores e há `noindex`, mas quem receber o link entra de graça.
- **Hospedagem:** estático em domínio próprio (`sozinho.tutorialpet.com.br`; pelo histórico, Vercel com deploy a partir do GitHub). O app Streamlit antigo (`app.py`, streamlit.app) continua no repo, sem uso principal. Há uma cópia de teste em `landing/app-teste-k7q2m9/`.
- **Loja de apps:** não está. É só PWA instalável pelo navegador ("adicionar à tela inicial").
- Já na memória: pendência "token ?k= no app" e "testar app em janela anônima" (confirmado: abre sem login).
- Produtos: Sozinho R$ 27 (checkout NcQChat), Adestramento Básico R$ 47 (upsell one-click na obrigado.html, e-book PDF, sem módulo no app). Higiene e Xixi ainda não existem como módulo.

## 2) Solução MAIS LEVE (Kiwify webhook + e-mail do cliente, sem loja)
Tudo no mesmo projeto Vercel já existente, custo R$ 0:
1. **Webhook:** função `/api/kiwify` recebe os avisos da Kiwify (Configurações > Webhooks, um por produto ou geral), confere a assinatura (HMAC com o token do webhook, guardado em variável de ambiente da Vercel) e grava no **Upstash Redis/Vercel KV (plano grátis)**: `email -> {modulos: [sozinho, adestramento...], status}`. Mapa fixo `ID do produto Kiwify -> módulo`.
2. **Reembolso/chargeback:** os eventos de compra reembolsada e chargeback removem o módulo daquele produto (e recusa de pagamento/boleto não pago nunca libera). A garantia de 7 dias já é pela Kiwify, então basta o aviso.
3. **Login único:** tela de e-mail no app; a função `/api/entrar` confere se o e-mail tem compra e manda **link mágico** (Brevo, já usado pela holding, ou Resend grátis; conta Gmail cheia do Allan não entra no fluxo). O link devolve um token assinado (30-90 dias) guardado no aparelho; o mesmo e-mail em outro aparelho funciona com novo link. Alternativa ainda mais leve na 1ª versão: e-mail + 4 últimos dígitos do CPF/telefone da compra (sem envio de e-mail), mais fraca contra quem sabe o e-mail do comprador.
4. **Conteúdo protegido de verdade:** separar `content.json` em um arquivo por módulo, servido por `/api/modulo/<nome>` só com token válido e módulo comprado (hoje tudo é público no navegador). O service worker passa a guardar offline só o que o token permite. Módulos novos = adicionar JSON + linha no mapa.
5. Upsell/order bump: o webhook libera o 2º produto sozinho na mesma conta (mesmo e-mail), sem mexer em nada.

## 3) O que falta e esforço
| Item | Horas |
|---|---|
| Função webhook + KV + mapa de produtos + assinatura | 2 |
| Login por link mágico (função, e-mail Brevo, tela no app, token) | 3 |
| Separar conteúdo por módulo, API protegida, service worker/offline | 2 |
| Criar módulos Higiene e Xixi (conteúdo em JSON a partir dos e-books) + cadastrar produtos na Kiwify (precisa navegador logado do Allan) | 3 a 4 |
| Migração dos compradores atuais (lista de e-mails da Kiwify para o KV) e teste ponta a ponta com compra/reembolso de teste | 1,5 |
| **Total** | **cerca de 10 a 12 h** (só o essencial, sem Higiene/Xixi: 7 a 8 h) |
Dependências do Allan: só o token do webhook e criar os webhooks/produtos na Kiwify (login dele); a chave de e-mail vai como variável na Vercel sem passar pelo chat.

## 4) Riscos
- **Apple/Google:** como PWA não há revisão de loja nem comissão de 15-30%. Se um dia empacotar para a loja, a regra de pagamento digital (Apple 3.1.1 / Play Billing) exige compra dentro do app; vender fora (Kiwify) e só "entrar" com conta é aceito apenas em casos restritos (leitor/conteúdo já comprado), com revisão incerta. Recomendação: ficar em PWA.
- Meta/Kiwify: sem promessa de saúde nos módulos (Higiene/Xixi); aviso veterinário fixo.
- Técnicos: webhook perdido (usar reenvio da Kiwify + rota de conferência manual), e-mail digitado diferente na compra (permitir alias/suporte), link mágico caindo em spam, compartilhamento de conta (limitar a 3 aparelhos), LGPD (guardar só e-mail e módulos; já coberto na política de privacidade, citar o app).
- Segurança: token do webhook só em variável da Vercel, nunca no repo; ligar 2FA em Vercel/Kiwify (pendência existente).

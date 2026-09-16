# Configurando uma conta Google Ads para o agente 01 (Niche Research)

Este documento registra o processo manual já feito uma vez para obter as credenciais que
`agents/01_niche_research/keyword_client.py` usa na Google Ads API. Guarde-o como
referência para replicar o processo em contas/sites futuros, sem precisar redescobrir os
mesmos passos.

> Nada aqui precisa ser feito de novo para o site atual se as credenciais já estiverem
> configuradas no `.env`. Use este guia quando adicionar uma **nova** conta Google Ads
> (por exemplo, para um site/nicho novo com uma conta separada).

## 1. Criar a conta Google Ads sem campanha paga

O Google tenta empurrar o fluxo "Especialista" direto para criar uma campanha paga. Para
criar só a conta (sem gastar com anúncios):

1. Acesse [ads.google.com](https://ads.google.com) e comece a criação de uma conta nova.
2. Quando o assistente pedir para configurar uma campanha, procure o link discreto
   **"Alternar para o modo Especialista"** (geralmente no rodapé da tela).
3. No modo Especialista, escolha a opção de criar a conta **sem campanha** (o texto exato
   muda com frequência — procure por algo como "Criar uma conta sem campanha").
4. Finalize o cadastro (dados de cobrança podem ser exigidos pelo Google mesmo sem
   campanha ativa, mas nenhum anúncio é veiculado nem cobrado enquanto não houver campanha).

Essa conta "vazia" já é suficiente para usar a Google Ads API e o Keyword Planner —
não é necessário gastar com anúncios para pesquisar palavras-chave.

## 2. Encontrar o Customer ID (`GOOGLE_ADS_LOGIN_CUSTOMER_ID` / `GOOGLE_ADS_CUSTOMER_ID`)

1. Faça login em [ads.google.com](https://ads.google.com).
2. O Customer ID aparece no canto superior direito da tela, no formato `123-456-7890`.
3. Para a variável de ambiente, use só os dígitos (sem hífen): `1234567890`.
4. Se a conta usada para autenticação for uma **MCC** (conta de gerenciamento, "Minha
   Central de Clientes") que administra outras contas, `GOOGLE_ADS_LOGIN_CUSTOMER_ID` é o
   ID da MCC, e `GOOGLE_ADS_CUSTOMER_ID` (opcional) é o ID da conta específica a consultar
   — se forem a mesma conta, basta preencher `GOOGLE_ADS_LOGIN_CUSTOMER_ID`.

## 3. Obter o Developer Token

1. Na conta Google Ads (de preferência a MCC, se houver uma), acesse **Ferramentas e
   Configurações → Configuração → Central da API**.
2. Solicite o acesso — por padrão, ele vem em nível **Teste** (Test Access), que só
   funciona com contas de teste do Google Ads, sem dados reais.
3. Para consultar o Keyword Planner com dados reais de volume/CPC, é preciso solicitar o
   upgrade para **Acesso Básico** (Basic Access) preenchendo o formulário de solicitação
   do próprio Google — inclui perguntas sobre o uso pretendido da API. A aprovação não é
   imediata (pode levar de alguns dias a algumas semanas).
4. O token gerado é uma string única por conta MCC — é o valor de
   `GOOGLE_ADS_DEVELOPER_TOKEN`.

## 4. Criar as credenciais OAuth (Client ID / Client Secret)

1. Acesse o [Google Cloud Console](https://console.cloud.google.com).
2. Crie um projeto novo (ou reaproveite um existente dedicado a este propósito).
3. Em **APIs e Serviços → Biblioteca**, procure e ative a **Google Ads API**.
4. Em **APIs e Serviços → Tela de consentimento OAuth**, configure um app do tipo
   "Externo" (ou "Interno", se a conta Google Workspace permitir), preenchendo os campos
   obrigatórios mínimos (nome do app, e-mail de suporte).
5. Em **APIs e Serviços → Credenciais → Criar credenciais → ID do cliente OAuth**,
   escolha o tipo de aplicativo **Desktop app**.
6. Anote o **Client ID** e o **Client Secret** gerados —
   `GOOGLE_ADS_CLIENT_ID` e `GOOGLE_ADS_CLIENT_SECRET`.

## 5. Gerar o Refresh Token

O jeito mais simples é usar o script de exemplo oficial da biblioteca `google-ads`
(`examples/authentication/generate_user_credentials.py`, disponível no repositório
[google-ads-python](https://github.com/googleads/google-ads-python) no GitHub):

1. Instale a lib: `pip install google-ads`.
2. Baixe (ou copie) o script `generate_user_credentials.py` dos exemplos do repositório.
3. Rode o script informando o Client ID e o Client Secret obtidos no passo 4. Ele abre uma
   URL de autorização no navegador — faça login com a conta Google que tem acesso à conta
   Google Ads e autorize o escopo `https://www.googleapis.com/auth/adwords`.
4. O script imprime um **Refresh Token** — esse é o valor de `GOOGLE_ADS_REFRESH_TOKEN`.

O refresh token não expira por tempo (só se for revogado manualmente ou se a conta Google
ficar muito tempo sem uso), então esse passo só precisa ser refeito se as credenciais
forem revogadas.

## 6. Preencher o `.env`

Com os cinco valores em mãos, preencha (veja `.env.example` na raiz do projeto):

```
GOOGLE_ADS_DEVELOPER_TOKEN=...
GOOGLE_ADS_CLIENT_ID=...
GOOGLE_ADS_CLIENT_SECRET=...
GOOGLE_ADS_REFRESH_TOKEN=...
GOOGLE_ADS_LOGIN_CUSTOMER_ID=...
# opcional, só se a conta consultada for diferente da conta de login:
GOOGLE_ADS_CUSTOMER_ID=...
```

Rode `python agents/01_niche_research/agent.py --site <site_id>` para confirmar que a API
responde (o log mostra `api=sim` quando as credenciais são reconhecidas).

## Notas para replicar em uma conta futura

- Uma única conta MCC + Developer Token pode ser reaproveitada para vários sites — não é
  necessário repetir os passos 1–4 a cada novo nicho, só o processo de pesquisa em si
  (agente 01 com o YAML do novo site).
- Se o novo site usar uma conta Google Ads totalmente separada (ex.: cliente diferente),
  repita os passos 2–5 para essa conta específica.
- Guarde o Developer Token e o Refresh Token como segredos (nunca commitados no
  repositório) — o `.gitignore` do projeto já exclui o `.env`.

---
criado: 2026-10-21
---
# Habilidade: verificar antes de pedir (toda rotina que lista "Decisão do Allan" ou "pendência dele")

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: tempo: horas do Allan economizadas; métrica: nº de pedidos ao Allan que já estavam resolvidos em 05 Decisões/06 Pendências (hoje 1 caso documentado, o ManyChat de 21/10; fonte: o texto de 05 Decisões e 06 Pendências contra as listas de 'Decisão do Allan').
2. META E PRAZO: zero pedido repetido nas listas 'Decisão do Allan' de HOJE 22/10; conferência por amostra às 18:00 e às 21:00; cada pedido novo com evidência de checagem ('conferi em <onde>, não achei').
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - J1: pedir o que já foi feito custa tempo dele -> reler 05 Decisões e 06 Pendências em texto cheio antes de listar qualquer pedido -> pedidos repetidos / pedidos listados -> o Jev confirma o cruzamento (noul) só se o texto for longo.
   - J2: supor que falta ferramenta gera pedido falso -> testar a ferramenta, a conta ou o Chrome (list_connected_browsers + ToolSearch) antes -> pedidos desfeitos pela checagem -> procurar alternativa grátis e só pedir login, 2FA ou pagamento.
   - J3: conta duplicada nasce de OAuth sem conferir -> listar contas/workspaces antes de conectar e conferir de novo depois -> contas duplicadas criadas (alvo 0) -> parar no botão 'Criar conta'.
4. LAÇO: data/habilidades/aprendizado/verificar_antes_de_pedir.md, 1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta. Número ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (Juiz separado de quem produz; nota mínima 7 para ir ao vivo) (critério: cada pedido ao Allan traz a evidência da checagem; pedido repetido conta como falha de processo em registro_de_falhas.md).


## Por que existe
Causa raiz encontrada em 21/10/2026: o Estrategista de Redes Sociais pediu autorização para criar o ManyChat — mas o ManyChat **já tinha sido criado e configurado** em 20-21/10 (data/memoria/05 Decisões.md, linha do lead magnet "7 Erros"; 17 Retomada). O agente não leu 05 Decisões antes de escrever a pendência. Isso não é falta de ferramenta nem falta de ideia: é pedir ao Allan algo que ele já resolveu, porque o agente não conferiu. Pedido do Allan (21/10/2026): "eles não podem ficar sem as ferramentas para fazer... os agentes precisam ser mais ativos, correr atrás da solução" — ou seja, antes de devolver algo pra ele, o agente tem que ter certeza de que é realmente dele.

## Regra (toda rotina que escreve "Decisão do Allan", "pendência dele" ou pede autorização/login/conta)
1. **Releia o texto cheio** (não resumo, não memória de rodada anterior) de `data/memoria/05 Decisões.md` e `data/memoria/06 Pendências.md` antes de listar qualquer pedido novo. Se a mesma ferramenta/conta/decisão já aparece lá como feita, **não peça de novo** — use o que já existe, ou diga em 1 linha que vai usar o que já está criado.
2. **Teste antes de supor que falta**: se o pedido é "o Allan precisa logar/criar conta em X", primeiro confira se já existe evidência de que X está configurado (nota de memória, arquivo no repo, resultado anterior que citou X funcionando). Só vira pedido ao Allan se, depois de conferir, realmente não existir ou estiver quebrado — com a evidência da checagem anexada ("conferi em <onde>, não achei", não "presumo que falta").
3. **Ferramenta que falta de verdade**: primeiro procure alternativa gratuita própria (ver regra geral de "testar grátis primeiro"); só peça ao Allan o que for estritamente dele (login, 2FA, pagamento, identidade) — e peça já com o link/tela pronta, nunca "você precisa configurar X" solto.
4. **Se o pedido já tinha sido atendido e o agente pediu de novo**: isso é FALHA DE PROCESSO do próprio agente (registro_de_falhas.md), não uma pendência nova — registre como tal, não como "Decisão do Allan #N".
5. **Jev pode ajudar na triagem** (jev_decisao_rapida.md): `noul` "is this request already resolved per the decisions log" antes de incluir algo na lista final de pedidos — mas a leitura do arquivo inteiro (regra 1) é sempre manual, o Jev só confirma o cruzamento quando o texto é longo.

## Onde já está ligado (21/10/2026)
Estrategista de Redes Sociais v2, Especialista TikTok v2 (prompt embutido no agendamento — corrigido via update_trigger), Revisão Estratégica de Renda, Auditor de Anúncios, Cobrança dos Departamentos, Fábrica de Produtos, Produtor de e-book, Criativo de Venda, Editor de Afiliados, Pesquisador de Mercado, Marketing de Produto (agente 29). Qualquer prompt novo que vá listar algo como pendência do Allan entra nesta lista.

## Limites

### Regra do Chrome (acrescentada em 21/10/2026): nunca concluir "sem Chrome / sem PC" pela lista de ferramentas
O Chrome do Allan ESTÁ conectado a esta conta (list_connected_browsers retornou "Browser 1", Windows, inUse). As ferramentas mcp__claude-in-chrome__* costumam vir adiadas e não aparecem na lista inicial; isso não significa que o navegador não exista. Antes de escrever "não tenho acesso ao Chrome/PC" ou de devolver qualquer tarefa de navegador ao Allan: (1) faça UMA chamada mcp__claude-in-chrome__list_connected_browsers; (2) carregue as ferramentas com um único ToolSearch ("select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__browser_batch"); (3) use tabs_context_mcp primeiro, trabalhe em aba própria e feche-a ao terminar. Só se a lista vier vazia ou as chamadas derem erro de conexão registre "sem dado (PC ausente)", com o erro exato, e siga sem travar. Concluir "sem Chrome" sem essa chamada é falha de processo do agente (registro_de_falhas.md).

### Regra da conta existente (21/10/2026): conferir se já existe antes de conectar ou criar
Erro real: ao conectar o Facebook no ManyChat, o login criou uma segunda conta (havia a "tutorialpetbr"). Antes de qualquer login, OAuth ou conexão de canal numa ferramenta que o Allan já usa: (1) abra o seletor de contas/workspaces e liste o que existe; (2) conecte por dentro da conta certa; (3) se o botão disser "Cadastre-se" ou "Criar conta", PARE e confira o que vai acontecer; (4) depois da conexão, confira de novo o seletor de contas e se o canal ficou na conta pretendida.

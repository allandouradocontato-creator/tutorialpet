# Política de modelos (qual IA usar em cada tarefa)
Regra do Allan: custo-benefício. Usar o menor/mais barato que resolva; subir só se precisar. Vale para o Claude e para os agentes da nuvem.

| Tarefa | Modelo | Por quê |
|---|---|---|
| Classificar, pontuar, triar, decidir sim/não (achados do painel, ganchos, comentários, leads, artigos prontos?) | **Jev** (typesafe/jev-1.13, OpenRouter) | Quase instantâneo e quase de graça. Não escreve; não faz conta, contagem, data. |
| Escrever, executar, pesquisar, rotinas dos agentes | **Sonnet** (padrão) | Bom e barato |
| Decisão difícil/ambígua, arquitetura, texto crítico | **Opus** só se necessário | Mais caro; justificar o uso |

Regras do Jev:
- Jev decide, Claude escreve. Se a confiança do Jev for < 0,5 (ou noul entre 0,25 e 0,75), o Claude decide.
- Algo privado (e-mails reais, clientes, financeiro) só vai ao Jev com OK do Allan; conteúdo público/nosso vai direto.
- A chave nunca aparece em arquivo, log ou chat. Está no PC do Allan e como segredo de rede na nuvem.
- Rodada de 08/10: Jev ligado à Triagem (Painel de Decisões); teste na nuvem em andamento.
- Registrar em cada entrega quantos itens o Jev decidiu e quantos o Claude resolveu.

Roteamento automático (o Otimizador revisa a cada rodada): tarefa de triagem/classificação → Jev primeiro; execução → Sonnet; só escalar para Opus com motivo escrito; anotar o gasto e propor trocar o modelo de qualquer rotina que gaste demais sem ganho.

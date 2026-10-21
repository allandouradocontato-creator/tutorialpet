# Livro de Gaps — problemas reais já vividos e como evitar cada um

Base de treino do suporte e do Auditor. Regra: cada tropeço vivido na construção
da holding entra aqui com causa, solução e **como o produto evita que o cliente
passe por isso**. Fonte: histórico real de set–out/2026.

| # | Problema vivido | Causa | Solução aplicada | Como o produto evita |
|---|---|---|---|---|
| 1 | Anúncio com clique barato e 0 vendas (Sozinho em Casa, R$ 73 gastos) | Landing/checkout fracos; nenhuma etapa medida | Refazer landing com referência que converte; Pixel em cada etapa | Landing já nasce com estrutura de blocos testada, Pixel/CAPI e Clarity ligados |
| 2 | Venda paga sem matrícula na Área de Membros | Produto Kiwify criado sem Área vinculada (não editável depois) | Recriar produto; webhook validado | Checklist de criação de produto no botão "Publicar"; tipo de entrega definido antes |
| 3 | Preço do anúncio diferente do preço na Kiwify | Mudança de preço sem revisar criativos | Checagem obrigatória antes de ativar campanha | Botão "Montar campanha" confere preço/link/página ao vivo antes de ativar |
| 4 | Link do anúncio apontando para página antiga | Deploy local ≠ página no ar | Conferir página ao vivo antes de ativar | Mesma checagem automática (#3) |
| 5 | Pacote "pronto" com software pirata (Restro SaaS nulled) | Compra de bundle sem auditoria | Licença oficial na CodeCanyon | Auditor de Aquisição: toda ferramenta/pack passa por checagem de licença antes de entrar na biblioteca |
| 6 | Hospedagem grátis zerou créditos (Netlify) | Plano grátis com limite escondido | Migrar para Vercel | Fornecedor padrão por etapa com limite conhecido; alerta antes do teto |
| 7 | Conta duplicada criada ao conectar canal (ManyChat) | Botão "Criar conta" clicado em vez de entrar na conta existente | Regra: conferir conta/workspace existente antes de qualquer OAuth | Fluxo de conexão mostra a conta detectada e pede confirmação |
| 8 | Perda de tempo pedindo ao usuário achar tela/opção já ativa | Não checar por ferramenta antes de pedir ação manual | Regra: checar estado primeiro | Suporte: bot verifica status (conta conectada? página no ar?) antes de responder |
| 9 | Vídeo do Facebook sem legenda acessível | Facebook bloqueia acesso automatizado e esconde legenda | Abrir no Chrome logado; gravar áudio e transcrever (Whisper) | Caçador de Ofertas: pipeline de captura com 3 níveis (texto → página do autor → transcrição) |
| 10 | Narração travada (pacote de voz Windows não instala) | Dependência de SO do usuário | Voz por API (ElevenLabs) | Tudo roda na nuvem; nada depende do PC do cliente |
| 11 | Publicação automática travada por aprovação manual | Fila exigia clique por post | Aprovação automática com regras | Cliente escolhe "aprovar tudo" ou "revisar", sem fila escondida |
| 12 | Agente "rodou sem erro" mas saída vazia/errada | Confiar no status verde | Conferir a saída real, não o status | Todo botão mostra prévia do resultado antes de dar como pronto |
| 13 | Loop infinito de reescrita por tema repetido | Sem timeout por etapa | Timeout + retry | Limite de tentativas por geração; crédito não é debitado se falhar |
| 14 | Imagens tristes/abrigo em conteúdo pet | Banco de imagens sem filtro de tom | Filtro de estilo visual | Filtro de tom por nicho embutido no gerador de criativos |
| 15 | Legenda com link de checkout em vez da landing | Template errado | Corrigido no template | Link de destino é um campo único, usado em tudo |
| 16 | Chave de API exposta/colada em lugar errado | Painel lateral do chat não aceita colagem segura | Chave só no PC/servidor | Chaves nunca aparecem no painel; cliente nunca lida com chave |
| 17 | Crédito/uso do Claude estourando em tarefas mecânicas | Modelo caro em tarefa simples | Roteamento Jev → Sonnet → Opus só com motivo | Roteamento barato por tipo de geração; margem protegida |
| 18 | Produto novo criado com campos vazios (capa, categoria) | Pressa | Padrão: preencher tudo | Botão "Publicar" exige capa + categoria + descrição gerados |
| 19 | Promessa de renda em anúncio (risco Meta/Kiwify) | Copiar padrão do mercado | Promessa de tempo, não de dinheiro | Guardião de conformidade bloqueia texto com promessa de ganho |
| 20 | Usuário sem saber "qual janela" está rodando o quê | Várias sessões/pastas em paralelo | Cartão indicando sessão/pasta em cada prompt | Painel único: cliente não tem "janelas", só botões |

## Como o suporte usa isto
1. Toda pergunta do cliente passa primeiro por busca neste livro (resposta pronta).
2. Problema novo → entra aqui com causa + solução + prevenção, no mesmo dia.
3. Auditor revisa semanalmente: qual gap mais apareceu → vira correção no produto, não só resposta.

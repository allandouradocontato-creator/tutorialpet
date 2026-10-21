# DEPARTAMENTOS E DIRETORES (criado 21/10/2026 a pedido do Allan)
Problema que isto resolve: cada agente entregava seu relatório e ninguém juntava tudo numa decisão. Agora cada departamento tem UM diretor: os especialistas opinam, o diretor decide e escreve. Quem aciona o departamento (Allan ou Claude) fala com 1 diretor, não com 12 agentes.

| Departamento | Diretor (prompt) | Especialistas que alimentam o diretor |
|---|---|---|
| Audiência e Redes | diretor_audiencia.md | Estrategista de Redes Sociais, Criador de Audiência, Especialista TikTok, Atendente de Comentários, Vigia/Guerrilha de Comunidade, Pesquisador de Formato, Humorista, Utilidade Pública |
| Produto e Receita | diretor_produto_receita.md | Fábrica de Produtos, Produtor de e-book, Construtor de app, Criativo de Venda/VSL, Editor de Afiliados, Pesquisador de Mercado, Caçador de Oportunidades, Importador, Auditor de Anúncios, Revisão Estratégica de Renda |
| Conteúdo e Blog | diretor_conteudo_blog.md | SEO e Tráfego, redatores/curadoria do blog, Revisor de Coerência, Conferente de Estoque, Publicador/Agendador |
| Operação e Qualidade | diretor_operacao.md | Vigia de Rotinas, Executor de Decisões, Agente de Segurança, Medidor de Testes, Cobrança dos Departamentos, Auditor/Otimizador de Processo |

Regras comuns: config/prompts/diretor_base.md. Modelo da ficha: data/departamentos/ficha_modelo.md. Fichas: data/departamentos/fichas/AAAA-MM-DD_<assunto>.md. Os especialistas continuam existindo e sendo medidos isolados (T9 do Medidor).

# Retomada — resumo vivo para continuar de onde paramos
Regra do Allan (16/10/2026): a última conversa nem sempre aparece na barra lateral do app, então TODA conversa nova começa lendo esta nota (e o Otimizador a atualiza em toda rodada ter/sex). Nunca depender da lembrança do Allan.
Atualizado em 21/10/2026 ~09:43 (Fortaleza) pelo Claude (sessão do Allan, fechamento de ciclo).

## Onde estamos
- Foco do Allan: sem anúncios; sucesso = engajamento, audiência e agilidade do processo. Meta: fechar o processo até sexta 23/10 e então construir o MOLDE para lançar um novo negócio em 7 a 10 dias (hoje levou ~1 mês). Ordem em data/molde/ORDEM.md; gatilhos na nuvem em 23/10 e 30/10 12:17.
- Autorizado pelo Allan: Claude/agentes executam as mudanças do Otimizador; registro em data/auditoria/mudancas.md (veredito na sexta 23/10).
- Teste de 7 dias dos vídeos: 15 a 21/10 (3 posts/dia por rede; julgar só com 72 h+).
- Publicação: Facebook/Instagram pelo Zernio, TikTok pelo Buffer (grátis, 10 posts na fila). Estoque em 16/10: 12 vídeos Zernio até 19/10, 7 TikToks até 18/10, 9 memes prontos.

## Feito em 16/10
- Corrigido o push do publicar_blog (--autostash, 3 tentativas, erro claro) e republicados os 3 artigos que estavam em 404.
- Criados mudancas.md, ciclo.csv, semanal, manual (nota 16) e apostila (nota 15) atualizados.

## Pendente — Claude/nuvem (sem o Allan)
1. Conferir HTTP 200 dos 3 artigos (conviverem-em-paz, bola-de-pelo, frutas) — Conferente 07:47.
2. Recriar Caçador de estilo viral e Agente de Segurança com Zernio+Buffer (hoje citam Metricool/landing antiga); trocar Caçador de referências por busca web (hoje depende do PC).
3. Ler saldo ElevenLabs (workflow creditos_eleven.yml) e criar alerta abaixo de 30%.
4. App Sozinho em Casa: fixar requirements e token ?k=; blog: foto nas 6 páginas sem imagem e _headers.
5. Medir audiência (seguidores, comentários, compartilhamentos) e ciclo; tarefa agendada de segunda 19/10 executa 2 a 4.
## Pendente — só o Allan (login/identidade)
Reconectar Windsor.ai; 2FA nas contas; recriar chave ElevenLabs; verificação TikTok; produto Kiwify duplicado 3JprCCK (precisa do navegador logado).
## Próximas datas
Seg 19/10 tarefa de pendências na nuvem; ter 20/10 Otimizador; 21/10 fim do teste de 7 dias; sex 23/10 veredito das mudanças + decisão "processo fechado" + molde; 30/10 reserva do molde; renovação ElevenLabs 07/11.

## Rodada de pendências 19/10 (Otimizador, nuvem)
Feito: 3 artigos (conviverem-em-paz, bola-de-pelo, frutas) estão em site/build na main (HTTP ao vivo não conferido: WebFetch sem permissão de URL); audiência registrada em ciclo.csv (FB 6 seguidores, IG 0, TikTok 12–19/10: 20 posts, 4.006 views, 1 comentário, 9 compartilhamentos, tempo médio 2,35 s); requirements do app fixado (streamlit 1.66.0, pillow 12.3.0) com smoke test.
Falhou: créditos ElevenLabs ilegíveis — a chave do workflow retorna 401 (sem permissão user_read); sem saldo não há ALERTA <30% (indeterminado).
Só o Allan: recriar a chave ElevenLabs COM permissão user_read (e aprovar recriação do Caçador de estilo viral e Agente de Segurança, não mexidas); liberar tutorialpet.com.br no WebFetch das rotinas; conferir o app ao vivo após o deploy.

## Rodada do Otimizador 20/10 10:55 (nuvem)
Alerta: 3 artigos aprovados (gato-parar-de-arranhar-sofa, patas-no-inverno, legumes-cozidos) estão em 404 desde 19/10 porque o publicar_blog #23 sai com erro quando qualquer slug do lote é reprovado e não grava os bons; 4 pacotes de vídeo prontos aguardam artigo. Correção proposta: `if: always()` no passo de gravar, limpar blog_aprovados.txt dos 3 reprovados, republicar. Coerência visual está desligada (GEMINI_API_KEY não chega ao publicar_blog/Guardião). Saldo ElevenLabs ilegível (401 Invalid API key). TikTok: só 3 agendados (até 21/10 10:20). Rotinas Vigia, Criador de Audiência, Humorista e Utilidade Pública sem disparo desde 15–16/10: conferir amanhã. Sex 23/10: veredito das mudanças + molde.

## DECISÕES DE 20/10 À TARDE (gravadas só agora, 21/10 — os agentes da nuvem rodaram sem elas até aqui)
- Sozinho em Casa: preço R$ 27 (âncora R$ 97, pagamento único, nunca "por dia/mês"). Upsell "Adestramento Básico" R$ 47 (e-book pronto, 56 pág., 21 dias) — ESTE é o produto do "teste do processo inteiro" agora, não mais o "Xixi no Lugar Certo" (data/produtos/teste_processo_xixi.md atualizado).
- Order bump "Kit Rotina Pré-Saída" (R$ 19,90) foi ABSORVIDO no e-book/app do Sozinho em Casa — não existe mais como produto/bump separado; o bump que entrar no lugar dele passa por checagem de sobreposição antes de ir ao ar (regra nova, permanente).
- "Produto" na holding = e-book + app + VSL + landing + oferta + copy + estudo de público (não só o e-book).
- Lead magnet grátis "7 Erros de Quem Deixa o Pet Sozinho" (PDF): Brevo (lista "7 Erros - Isca", form que abre sozinho.tutorialpet.com.br/7-erros.pdf) + ManyChat (comentário "GUIA" no Instagram). Brevo sem e-mail transacional ainda. Página em captura/guia.html (repo sozinho-em-casa-app) não publicada em landing/ ainda.
- Regra de desvio: R$ 27 com tráfego real por 3 dias; ≥100 visitas e 0 vendas → cai para R$ 17 por 3 dias, automático. Objetivo agora é a 1ª venda real, não ROI.
- Produto Kiwify duplicado antigo (3JprCCK, R$ 9,90) desativado por completo (checkout + página), mantido sem excluir para os 2 alunos antigos.

## Rodada de execução 21/10 (itens 1-6 do fechamento de ciclo, sessão do Allan)
Feito: religadas as 5 rotinas semanais que perderam o horário (SEO, Humorista, Utilidade Pública, Criativo de Venda, Caçador de Oportunidades) via fire_trigger. publicar_blog agora sai 0 quando publicou ≥1 mesmo com reprovados no lote, e tira sozinho os reprovados de blog_aprovados.txt. Artigo cuidados-essenciais-com-as-patas-de-caes-no-inverno aprovado (foto 0) e vai ao ar na próxima publicar_blog.yml. GEMINI_API_KEY repassado ao publicar_blog e ao Guardião de marca (fabrica.yml) — coerência visual volta a rodar. Caçador de estilo viral religado (estava desligado desde 15/10) e seu prompt trocou Metricool por Zernio/Buffer na comparação com nossas métricas. Caçador de referências de vídeo trocou o navegador (dependia do PC do Allan) por WebSearch/WebFetch. Agente de Segurança passou a também apontar conector desatualizado (rotina só com Metricool) como achado. Vigia passou a contar estoque da branch media pela API do GitHub, sem clonar.
Ainda falta (próxima rodada): confirmar que as 5 rotinas religadas terminaram sem FALHA; conferir se o artigo patas-no-inverno saiu do 404; saldo ElevenLabs (ainda sem confirmação de leitura >30%); 2FA e verificação TikTok continuam só com o Allan.

## Teste de resultado das skills (criado 21/10 tarde)
Baseline em data/testes/baseline_2026-10-21.md (T1-T9, janela 72 h). Rotina "Medidor de Testes de Audiência Tutorial Pet" (trig_01T84gNiDZh5LQVN8AjzPJfb), diária 21:11, 1ª medição 21/10 21:11, grava data/testes/medicao_AAAA-MM-DD.md; veredito FINAL sexta 24/10 21:11 em data/testes/veredito_final_2026-10-24.md. PERDEU vira linha E.. em execucao.md no mesmo dia. T8 base lida no Chrome: 0 vendas, 0 DMs GUIA, 0 contatos na lista de isca. Regra nova: antes de dizer "sem Chrome/PC", 1 chamada list_connected_browsers (verificar_antes_de_pedir.md; 07 Erros e lições).

## Departamentos com diretor (21/10 16:10)
Estrutura em config/prompts/departamentos.md. Diretores (rotinas na nuvem): Audiência 09:17 diário; Produto e Receita ter/sex 12:31; Conteúdo e Blog seg/qui 11:37; Operação 21:41 diário. Fichas em data/departamentos/fichas/. ManyChat: conta única tutorialpetbr (fb5804905) com IG + TikTok + Facebook; a conta nova fb1251330151406637 ficou vazia, não usar. Textos do Messenger = rascunho aguardando o Diretor de Audiência.

## Decisões — rodada do Executor 22/10 18:25Z (15:25 Fortaleza)
Contagem: decididas abertas ~24 / feitas 22 (com evidência) / atrasadas 7 (D02, D08, E07, E09, E13, E26, E42) / só Allan 2 (A02: 2FA e verificação TikTok; E13: ok para editar 4 TikToks agendados). Painel de Decisões sem resposta nova do Allan (última rodada 20/10, nenhum comentário).
Achado importante: em 22/10 16:41Z 26 rotinas foram desligadas (Humorista, Utilidade Pública, Atendente, Auditor de Anúncios, Criativo de Venda, Fábrica de Produtos, Cobrança, Editor de Afiliados, Revisão Estratégica, Triagem, Construtor de app, Produtor de e-book, Especialista TikTok, Pesquisadores de Formato e de Mercado). O Importador Internacional (D02) nunca foi criado e o Atendente 3x/dia (E09) depende de religar. Não criei nem religuei nada por conta própria: custa crédito, e o lembrete de 23/10 14:00 é para medir esse custo. Decisão pedida ao Allan: quais dessas voltam e quando.
Regra E32 gravada no prompt do Executor (commit parcial a cada 3 linhas + linha ATRASADAS no topo).

## Decisões — rodada do Executor 23/10 (06:53 Fortaleza)
Contagem: decididas abertas ~22 / feitas 28 / atrasadas 11 (D02, D08, E09, E11, E13, E14, E15, E23, E25, E26, E31) / só Allan 2 (A02: 2FA e verificação TikTok; E13). Painel de Decisões sem resposta nova do Allan.
Feito agora (com commit): E07 (config conferida), E16 (hashtags FB/IG ≤3 no agent.py), E46 (regra IG meme em estrategia_social.yaml), E47 (publicar_blog.yml: rebase --abort, -X theirs, issues: write; falta run verde), E49 (regra de ID no prompt do Executor), E32 (commit parcial no 1º minuto).
Não feito de propósito: nada que publique/agende (E35/E40 adicionar slugs a blog_aprovados e disparar publicar_blog ficam com o Conferente; E25/E14/E15 mexem na fila do Buffer/Zernio = agendar); rotinas desligadas em 22/10 16:41Z continuam desligadas (D02 Importador, E09 Atendente 3x/dia) até o Allan decidir após o lembrete de 23/10 14:00. E31 (prompt do Estrategista) não confirmado: rotina Estrategista fora da 1ª página de list_triggers.


## Retomada 23/10 17:35 — Vídeo 1 (escovar dentes) e Shopee
- Vídeo 1 pronto, NÃO publicado: V1e_Duda_so_gancho_fotos.mp4 (Duda só no gancho com rótulo IA; meio com fotos oficiais do kit + clipes de banco; CTA só voz). Regra do Allan: gesto repetido = tira a imagem da Duda e fica só a voz.
- Falhas do V1e a corrigir: poucos cachorros, fotos estáticas, cachorro repetido. Plano: 3-4 clipes de cachorro feliz por cena (Pexels), conferir 1 quadro de cada, sem repetir, alternar foto e clipe, cortes mais rápidos. Regra 29 criada (nada triste/abrigo).
- Shopee: kit "Kit Higiene Dental Pet Clean" (R$ 24,79). Link de afiliado gerado no painel (affiliate.shopee.com.br/offer/custom_link): https://s.shopee.com.br/LoEj8JFZW. Os 7 vídeos do anúncio são de clientes (não usar). Fotos do fabricante: Allan acredita que o programa permite; conferir regras no painel antes de publicar.
- Preço R$ 27 (âncora R$ 97) é do e-book Sozinho em Casa, NÃO do kit da Shopee: legendas separadas. Corrigir R$ 9,90 antigo.
- Maestros da IA: procurar skill/agente EDITOR DE VÍDEO / b-roll para não gastar tempo aprendendo a editar. Faltam ≈76 de 121 skills (parei em "Sonda"); sem o link da comunidade na memória. Pedir o link ao Allan (área de membros) e continuar de lá; anotar Prumo/Emissário/Sonda e plano "Portão de Gasto".
- Pendentes: React 2 (referência viral TikTok + crédito), cachorra poodle fixa (nome), gestos variados da Duda, lembrete Configurações > Uso (print), nada de publicar sem "pode publicar".

## Decisões — rodada do Executor 24/10 (06:53 Fortaleza)
Contagem: decididas abertas ~25 / feitas +8 nesta rodada (E57, E59, E60, E52, E53, E54, E93, E94; todas com arquivo/commit) / atrasadas 23 (base 11 + E27, E28, E35, E40, E41, E43, E45, E50, E95, V06, D09, D10) / só Allan 2 (A02: 2FA e verificação TikTok; E13). Painel de Decisões sem comentário novo do Allan.
Não feito de propósito: E50/E95/E25/E14/E15 (repor fila TikTok = agendar no Buffer, fora do que o Executor pode fazer); E35/E40/E36/E56 (aprovar slugs e disparar publicar_blog = publicar, ficam com Conferente); E58 sem fonte (Windsor desconectado, reconectar é do Allan); E61/E28/E29 exigem Chrome; D02/E09 seguem aguardando decisão do Allan sobre religar rotinas (custo de crédito). E27 (PDF da Carteirinha) não gerado nesta rodada por tempo.

## Veredito final do teste de 21/10 (Medidor, 24/10 21:15)
PERDEU T1, T3, T4, T5, T9; NEUTRO T2, T6, T7, T8; GANHOU 0. Detalhe em data/testes/veredito_final_2026-10-24.md; linhas E105-E109 em execucao.md (Executor 25/10 06:53). Teste encerrado: rodadas seguintes do Medidor escrevem 'teste encerrado' e param; Executor pode desligar a rotina. Pendências do Allan: verificação de identidade na Kiwify (E61) para ler vendas.

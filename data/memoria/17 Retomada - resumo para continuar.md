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

## Decisões — rodada do Executor 25/10 (06:53 Fortaleza)
Contagem: decididas abertas ~25 / feitas 39 (+E27, E100, E97, E98, E99, E105, E106, E108, E109, E40, E41; parciais E35, E36, E56) / atrasadas 14 (D02, D08, E09, E11, E13, E14, E15, E23, E25, E26, E31, E45, V06, D10) / só Allan 2 (A02: 2FA e verificação TikTok; E13) + 1 pedido novo: ok por escrito para ligar o fluxo MIMO ao vivo e autorizar OAuth do Facebook no ManyChat.
Destaque: PDF da Carteirinha do Pet pronto em data/audiencia/mimo/carteirinha_pet_fase1.pdf (E27/E100, gargalo da isca). Nada publicado nem ligado. Painel de Decisões sem comentário novo (rev 16).
Bloqueadas: E50/E95/E107/E43 (agendar ou ler Zernio/Buffer: sem esses conectores nesta sessão), E28/E29 (precisa Chrome/PC do Allan). D02/E09 seguem aguardando ok do Allan para religar rotinas pausadas (custo de crédito).
Nota: o repositório tem a branch media grande; `git pull` completo estoura o tempo, usar `git fetch origin main` + `merge --ff-only`.

## Decisões — rodada do Executor 26/10 (06:55 Fortaleza)
Contagem: decididas abertas ~25 / feitas 0 novas (parciais: V09, V13, E113) / atrasadas 14 (mesmas de 25/10) / só Allan 2 (A02, E13). Painel de Decisões sem comentário novo.
Aplicado em código: capas_coerentes.yml com push seguro (fetch+rebase -X theirs, abort); agents/15_visual select_candidate tolera índice ausente. Pendentes: Fontes nos 4 slugs, fechar issues #10-#12, V10/E112 (sem Buffer/Zernio nesta sessão). Nada publicado nem agendado.

## Decisões — rodada do Executor 27/10
Contagem: decididas abertas ~25 / feitas 1 novo (E119) + parciais E120 (6/13 rascunhos com autor+Fontes), E121 (3 Fontes) / atrasadas 14 (mesmas) / só Allan 2 (A02, E13) + ok para religar D02/E09. Painel sem comentário novo. Bloqueado: V16 (Buffer não conferido), capas (Gemini). Nada publicado nem agendado.

## Decisões — rodada do Executor 28/10 (nuvem)
Contagem: decididas abertas ~40 / feitas +1 (E124: config/estilo_viral.yaml regra_E114_E124) / atrasadas 14 inalteradas (D02, D08, E09, E11, E13, E14, E15, E23, E25, E26, E31, E45, V06, D10) / só Allan: A02 (2FA, verificação TikTok), V19 (recarga ElevenLabs). Painel de Decisões sem comentário novo. Esta sessão não tinha list_triggers/update_trigger, então E133 (achar o Medidor), D02 e E09 ficaram parados. E125-E129 (fila, preço R$ 27 em roteiros agendados ou não) não executados: sem como separar itens agendados dos não agendados na nuvem.

## Correções AdSense 28/10 (executor Sonnet; commits ac2d74d, c433145, c2c6469, ac89729, 1fb49e7 na main)
- Feito: (1) páginas /categoria/<slug> (5 pilares + pet-celebridade) com descrição única, cards, menu/rodapé/sitemap e "Categoria: X" em cada artigo (config/categorias.yaml); (2) seção final publicada como "Conclusão" nos artigos, e 3+ links internos do mesmo pilar em todos (71 artigos receberam links; 1 link quebrado corrigido); (3) links Shopee na palavra-chave em 20 artigos de produto + aviso de afiliado + rel="sponsored nofollow noopener" aplicado pelo build; (4) página /disclaimer no rodapé e no sitemap; (5) ritmo FIXO de 3 artigos/dia (fabrica.yml sem a 4ª produção; config/ritmo_blog.yaml) e rodízio de pilares sem repetir seguido (rotina_diaria.py, escolher_proximo).
- Pendente: data/monetization/afiliados_faltando.md (GPS, rampa, caixa para avião sem link; 9 artigos com link cadastrado mas sem a palavra no texto); 11 artigos sem "Fontes e referências" e 8 sem capa (CRÍTICO da auditoria); buraco de publicação 15/09 a 06/10 no histórico (falha da auditoria que só some com o tempo); títulos de vários artigos sem acento (seguranca, esta, agua, racao...) a corrigir; links internos de fallback (129) são frases "veja também" geradas por similaridade — vale revisão humana de relevância; esperar 2 a 4 semanas de recrawl antes de pedir nova revisão (regra 31).
- Fechado 28/10 (executor Sonnet): 11 artigos ganharam "Fontes e referências" (2 a 4 links cada, todos conferidos em 200; afirmações sem respaldo viraram frases cautelosas) e os 8 sem capa ganharam foto (2 já baixadas ligadas ao front-matter; 6 escolhidas dos candidatos; 4 deles buscados pelo workflow `capas_lote.yml` modo `buscar`, que tem a chave do Pexels, via `gh api .../dispatches`, e baixados da branch `media`); typo "gatigos" corrigido. Auditoria de baixo valor: CRÍTICO 0 e AVISO 0; auditoria AdSense: só resta a FALHA histórica do buraco de publicação 15/09 a 06/10.
- Lição: ao escolher capa, conferir o md5 contra as demais (a auditoria acusa "capa única" quando o mesmo Pexels aparece em dois artigos; aconteceu 3 vezes e foi trocado o candidato).

## Parceria veterinária 28/10 (executor Sonnet; mensagens "Equipe:", "/revisao-veterinaria", "selo", "Coluna Pergunte", "Sobre/Contato" e "Fluxo de revisão" na main)
- Parceira: Natasha Braga, médica veterinária (Instagram @vetnatasha, CRMV 6174, atendimento domiciliar em Fortaleza e Região, cães e gatos). Cadastro em config/sites/equipe.json (pessoas.natasha-braga); `crmv_uf` e `foto` vazios (build mostra iniciais NB).
- Feito: página /revisao-veterinaria (política, cartão dela, lista automática dos revisados; rodapé e sitemap); selo "Revisado por" + `reviewedBy` no JSON-LD só com `revisado_por: natasha-braga` + `revisado_em: AAAA-MM-DD` (testado em build local, frontmatter de teste revertido; NENHUM artigo marcado); coluna /categoria/pergunte-a-veterinaria (menu e rodapé; vazia = noindex e fora do sitemap até o 1º artigo com `coluna: pergunte-a-veterinaria`); data/pergunte_veterinaria/fila_perguntas.md (10 perguntas) e templates/pergunte_veterinaria.md; Sobre e Contato atualizados; skill blog_adsense_4_semanas.md J11 e prompt do Diretor de Conteúdo; lote 1 em data/pergunte_veterinaria/lote_revisao_2026-10-28.md (5 artigos aguardando o "ok" dela).
- Pendente: UF do CRMV (provável CE) e foto dela; ela responder o lote 1 e a fila; só então preencher `revisado_por`/`revisado_em` e reconstruir; ordenar o próximo lote por acessos quando GA4/Search Console estiverem legíveis; auditorias seguem com os mesmos itens de antes (11 sem fontes, 8 sem capa, buraco de 15/09 a 06/10); corrigir subtítulo "desacoplar os gatigos de saída" em ansiedade-de-separacao-em-caes junto da revisão dela.

## Decisão 28/10 — foco SP/Brasil e plano LATAM (Allan)
- Conteúdo e tráfego: São Paulo e Brasil; nada de Fortaleza em texto público (regra 33). Roteiros da Natasha em collab já ficaram nacionais; só os vídeos solo dela (perfil dela) citam Fortaleza.
- LATAM em espanhol: projeto futuro. Premissas a respeitar quando chegar a hora: (1) só depois do AdSense pt-BR aprovado; (2) site separado por idioma (domínio/subdomínio es.), com hreflang, e pedir aprovação do AdSense para ele (cada site é avaliado); (3) não traduzir 1:1: refazer temas pela busca real em espanhol (México, Colômbia, Argentina, Chile) e variar vocabulário por país; (4) CRMV não vale fora do Brasil: a revisão veterinária em espanhol precisa de veterinário(a) local ou deixar sem selo; (5) voz/avatar da Natasha em espanhol só com consentimento específico dela; Duda em espanhol fica a decidir.

## Campanha Sozinho em Casa VSL v12 — 28/10 16:25 (Sonnet, plano B do Fable)
- Campanha 120253387444780134 / conjunto 120253387467550134 / anúncios A 120253387470430134 e B 120253387471630134 criados PAUSADOS (R$ 30/dia, 28/10 20:00 → 31/10 23:59). Local: Brasil inteiro (SP por key não coube no Windsor; escolher "São Paulo" no Gerenciador). Copy sem "raça" (energia). Landing publicada (f2258ec).
- Falta só o Allan: marcar "conteúdo gerado por IA" nos 2 anúncios, conferir pagamento/saldo, (opcional) restringir a SP, ativar. Depois: religar o Auditor de Anúncios (trig_019JjHRfcjsdBSoWXLQiddsG) 09:34 Fortaleza.


## Duas seções novas do blog — Adoção e Utilidade Pública (Sonnet, 28/10/2026)
- PRONTO e no ar no repositório (main): pilares `adocao` e `utilidade_publica` (categoria, menu, cores), prioridade 1/dia por série em ritmo_blog.yaml + rotina_diaria.escolher_proximo, escritor com regras por pilar e rodapé jurídico, caixa de fontes oficiais, 24 termos na fila_temas.yaml, páginas de categoria vazias noindex, página /adocao/enviar com o formulário Google (link em config/adocao.yaml). Teste de rodízio OK, auditoria CRÍTICO 0 (84 artigos).
- Formulário: data/adocao/formulario_envio_adocao.md (upload de foto exige login Google de quem envia).
- Regra 36 (ideias de audiência sem pedir) em regras_de_ouro.md e no prompt do Diretor de Audiência; prompt utilidade_publica.md agora escreve e reconfere links.
- Primeiros artigos das duas séries saem pela fábrica nas próximas rodadas (a fábrica ainda está sem voz/ElevenLabs: só artigo).
- Depende do Allan: (1) decisão do saldo ElevenLabs (recarregar / Natasha grava / voz provisória); (2) contatar as ONGs com a mensagem pronta (lista em data/adocao/ongs_sp.md quando o pesquisador terminar); (3) Natasha revisar lote 1 e aceitar sugestão do lote 2; (4) pedir reanálise do AdSense ~14–21/11 só com CRÍTICO 0.

## Regra 37 (28/10 16:10, Allan): operação sem depender da Natasha
Nada espera revisão dela; saúde sai com cautela padrão; revisão dela é opcional e sem prazo; selo só se ela revisar. Itens "depende da Natasha" removidos das pendências do Allan (lote 1 e lote 2 viram disponíveis para ela quando quiser).
- 28/10 16:19: Natasha respondeu "Ok. Aceito!" ao uso da linha de diretrizes editoriais (prova em data/pergunte_veterinaria/aceite_natasha_diretrizes_editoriais_2026-10-28.md). ONGs de SP (9; falta a 10ª), mensagem de abordagem, molde da vitrine e script montar_vitrine_adocao.py entregues pelo agente e já no main. Allan decide: 10ª ONG e quem faz o contato.


## Decisões — rodada do Executor 29/10
Contagem: decididas abertas ~25 / feitas +1 (E130: bloco 'Para o Allan (receita)' em 06 Pendências; E133 já fechada pela Operação, trig_01T84gNiDZh5LQVN8AjzPJfb habilitada) / atrasadas 14 (mesmas) / só Allan: A02 (2FA, TikTok), Kiwify identidade, MIMO ao vivo+OAuth, ok para religar D02/E09. Painel de Decisões sem comentário novo (rev 16). Não feito: E129 (edição em massa de legendas, precisa distinguir agendadas) e E131/V19 (fabrica.yml). Nada publicado nem agendado. add_repo indisponível; usei o clone local.

## Retomada 30/10/2026 02h30 (Fable) — curadoria de reacts
- Lote 2 (r01/r02/r05) reprovado pelo Allan: onda pequena (100-200 mil views), sem contexto. Erro da escolha (Fable), não da execução. r01 fica agendado só como teste das bases (FB sex 21:00, IG 21:10); levas do r02/r05 canceladas.
- Feito e salvo: régua v4 (`data/remix/criterios_curadoria_v4_2026-10-30.md`), script `scripts/curadoria_tiktok.py` (yt-dlp mede views/curtidas/coment/compart/mediana da conta), habilidade `biblioteca/habilidades/curadoria_viral_v4.md`, regra de ouro 43, ficha `data/departamentos/fichas/2026-10-30_otimizador_curadoria_reacts.md`.
- Lote 3 em `data/remix/plano_reacts_lote3_2026-10-30.md` NÃO aprovado (vídeos curtos, sem contexto). Serve só de modelo de formato.
- Próximo passo (decisão do Allan 02:25): nova conversa de dia. Fable escreve as buscas/hashtags e a régua final (≥ 1 mi views, ≤ 7 d, 20-45 s com história, ≥ 2 de educativo/ilustrativo/engraçado) + régua de produto (Shopee, produto em uso + "onde compro?"); Sonnet coleta e mede (barato); Fable julga a tabela + folhas e escreve 6 roteiros (3 humor + 3 produto); animático antes de qualquer HeyGen.
- Fontes que funcionam: hashtags do TikTok logado no Chrome (#cachorro deu 164 links; Explorar trava em ~29; busca não filtra por data), yt-dlp no sandbox, faster-whisper (carregar WAV com wave+numpy).
- Medir o custo: Allan anota Configurações › Uso antes e depois do lote de curadoria.

## Decisões — rodada do Executor 30/10 (06:53 Fortaleza)
Contagem: decididas abertas ~30 / feitas +1 (V18 fechada: fallback Cloudflare em core/coerencia.py + Fábrica #186-#197 success) e V20/E131/E140/E148 parciais (falta capa Pexels afrouxada na 2ª tentativa em blog_imagens_nuvem.py) / atrasadas 14 nominais (D02, D08, E09, E11, E13, E14, E15, E23, E25, E26, E31, E45, V06, D10) + V15/V17/E140 vencidas / só Allan: A02 (2FA, TikTok), Kiwify identidade, MIMO ao vivo+OAuth, ok para religar D02/E09, V19 (ElevenLabs a/b). Painel de Decisões sem comentário novo. Nada comprado, publicado ou agendado. D09 (molde) segue com a rodada de reserva trig_013xrX6NyjFxenJ9WEcx9LT9 (30/10 15:17Z, enabled).

## Retomada 30/10/2026 09h30 (Fable) — lote 4 de reacts
- Régua final escrita: `data/remix/regua_final_lote4_2026-10-30.md` (A humor: ≥ 1 mi views, ≤ 7 d, 20-45 s com história, entra ≥ 80 = nível do n03 v2; B produto Shopee: produto em uso + "onde compro?", entra ≥ 70; 3 produtos diferentes, ordem xixi › dedeira › comedouro lento › tapete de lamber › cinto carro › escada).
- Cartão do Sonnet para coletar e medir: `data/remix/cartao_sonnet_coleta_lote4_2026-10-30.md` (hashtags/termos/perfis, script, 25 baixados com folha 1 fps + transcrição + top 10 comentários, tabela `curadoria_lote4_tabela_2026-10-30.md`).
- Falta (próxima conversa do Fable, depois do Sonnet): julgar a tabela e as folhas, escolher 3 + 3, mapa de batidas e 6 roteiros com falas por timestamp (regra 41), cartão para o Sonnet produzir o animático; "pode" do Allan antes de qualquer voz/HeyGen.
- Ponto de partida do custo do lote 4 (print do Allan, 30/10 09:30): sessão 8 %, semana 58 %, Fable 63 % do teto de 50 % (reset domingo 01:00). Medir de novo depois da coleta do Sonnet e depois do julgamento do Fable.

## Retomada 30/10/2026 10h30 (Sonnet) — lote 4: coleta e medição concluídas
- 319 medidos (177 humor, 142 produto), 25 baixados (a01-a15 humor, b01-b10 produto); tabela `data/remix/curadoria_lote4_tabela_2026-10-30.md`, CSVs completos `curadoria_lote4_A/B_2026-10-30.csv`, quadros-chave `data/remix/capturas/lote4_montagem_0/1/2.jpg`, transcrições e comentários em `curadoria/lote4/<id>/`. Originais e folhas no PC: Downloads\Tutorial Pet\reacts\originais_lote4 (50 arquivos conferidos).
- Humor: só 6 passam em todos os pré-requisitos (a06, a11, a12, a13, a14, a15; a12/a14 compilações, a06 = n02 já visto). Produto: quase tudo > 30 d (só b09 21 d; b08 31,8 d).
- Scripts novos: `scripts/medir_lote.py`, `varrer_perfis.py`, `preparar_candidato.py`, `transcrever_lote.py`. Lição: hashtag do TikTok só entrega 3-5 % de vídeos ≤ 7 d; varrer perfis por yt-dlp rende mais; views só pelo yt-dlp (navegador é bloqueado).
- Próximo: Fable julga a tabela e escreve os 6 roteiros; nada de voz/HeyGen antes do "pode". Ponto de partida de uso: sessão 8 %, semana 58 %, Fable 63 % (30/10 09:30); falta o print "depois".
- 30/10 10h45 (Fable): lote 4 julgado em `data/remix/plano_reacts_lote4_2026-10-30.md`: humor a06 (96) + a11 (80) entram, a13 (80) reserva; produto b09 rampa (79) entra, b03 educador xixi (75) depende do Allan aceitar idade > 30 d na vertente B; 3º de produto não existe (b05 63, b07 61). Cartão do Sonnet = animáticos dos 4 + coleta de reforço (varredura diária de perfis). Aguardando o "pode" do Allan.

## 30/10 11h (Sonnet produtor) — animáticos do lote 4 prontos, aguardando "pode"
- 14 falas ElevenLabs Marianne (v4, estab. 0,26) em `animaticos/lote4/voz/`; 4 animáticos em `animaticos/lote4/` (R4-1 35 s, R4-2 39 s, R4-P1 51 s, R4-P2 28 s), script `scripts/animatico_lote4.py`. Fala "cão" trocada por "cachorro" no R4-P2.
- ElevenLabs gastou ≈ 953 créditos ≈ 0,8 % do saldo (115,4 mil); estimativa do plano (0,3 %) estava baixa porque as falas finais são longas. Tela mostrou 115.485 depois (contador inconsistente; conferir).
- Alertas: tempo de falas > plano (R4-1 +5 s, R4-2 +10 s, R4-P1 +11 s); original do R4-1 tem logo Metrópoles; original do R4-P2 tem texto "SOLICITA CATÁLOGO DE COLORES" queimado e título em espanhol.
- Gatilho diário de virais criado (07:00). Reforço: ver seção "Reforço" da tabela do lote 4.

## 30/10 — lote 5 (Sonnet, coleta)
Entregue `data/remix/curadoria_lote5_tabela.md`: humor 30/30 passando (a01–a30), produto 19/20 passando (b02,b03,b06,b07,b10,b17,b20,b25,b26,b27,b29,b31,b32,b39,b41–b45; Shopee ≥1 mil vendas e ≤R$100 conferida). Originais em `Downloads/Tutorial Pet/reacts/originais_lote5/`. Zero crédito ElevenLabs/HeyGen. Pendente: Fable julga (assistindo com áudio); Shorts/Reels não coletados; 60 candidatos de produto só tiveram comentários checados, não baixados.

## 30/10/2026 — julgamento + animáticos lote 5
- Fable julgou (data/remix/julgamento_lote5_fable.md): finalistas a09, a16, a17 (humor) e b32, b03, b31 (produto Shopee); reservas a05, a10, b29, b42.
- Voz Marianne gerada linha a linha (18 falas) em animaticos/lote5/voz; 6 animáticos (Duda parada, zero HeyGen) em animaticos/lote5 e na pasta Downloads/Tutorial Pet/reacts/animaticos_lote5.
- Próximo: Allan ouve; só com novo "pode" vai ao HeyGen (looks B1/B2r já salvos). Builder: scripts/animatico_lote5.py.
- 2026-10-30: Lote 6 humor (h1–h5, régua v6): voz Marianne (15 falas) + 5 animáticos Duda parada em animaticos/lote6/ (scripts/animatico_lote6.py). Aguardando 'pode' para HeyGen/publicação.
- Allan deu o "pode" (40 créd.): 6 clipes HeyGen Avatar IV (W+C de b32, b03, b31) gastaram 88 créditos (350→262 restantes = 25 % do saldo de antes); 3 finais em Downloads/Tutorial Pet/reacts/lote5_final (≤ 10 MB, -14 LUFS, pico ≤ -1 dB), clipes em reacts/clipes_heygen_lote5; montagem: reacts_final/mont.py (voz Marianne limpa, original 25 %, música 10 %). NADA publicado; publicar só com novo "pode".

# REGRAS DE OURO DA HOLDING (cartilha de 1 página; leia UMA vez no início de toda sessão/rotina; não reler a cada passo)
Atualizada em 21/10/2026. Cada regra nasceu de um erro real (detalhe em data/memoria/07 Erros e lições.md). Regra nova entra aqui no mesmo dia, em 1 linha.

## Antes de pedir qualquer coisa ao Allan
1. Releia 05 Decisões e 06 Pendências (texto cheio). O que já está feito não se pede de novo.
2. Cheque por FERRAMENTA antes de mandar ele abrir/achar algo: computador linkado? aba já aberta? conta já existe? Se está checável, não pergunte e não mande procurar.
3. Se precisar mesmo da mão dele (login, 2FA, permissão), traga a janela PARA A FRENTE ANTES de avisar, como procedimento normal (computer_resolve_access + computer_request_access do Chrome em modo read + computer_open_application "Google Chrome", depois conferir com screenshot) e diga só 'está na sua tela'; nunca "procure aí" nem aponte aba escondida. Allan decidiu em 22/10/2026 que isso é padrão, sem pedir. Ele só decide estratégia/criação e dá autorizações pontuais (login, 2FA, pagamento, liberar pasta).
4. Não repasse relato de agente como fato sem conferir na fonte.

## Navegador, janelas e senhas
5. "Sem Chrome/PC" só depois de 1 chamada list_connected_browsers + ToolSearch das ferramentas mcp__claude-in-chrome__*.
6. O painel/navegador da LATERAL do chat NÃO aceita colar nem digitar senha/chave (a colagem sai vazia). Segredos vão no Chrome normal dele, link clicável desde o início. Eu nunca digito senha; credencial é dele.
7. Pedido "Permitir" do Chrome (extensão) abre numa janelinha que expira: antes de pedir, trazer o Chrome para a frente (computer_request_access + computer_open_application) e só então avisar.
8. facebook.com e telas OAuth: a extensão não opera. Deixar a janela de autorização na frente; quem clica é o Allan. Conferir depois o resultado por ferramenta.
9. Screenshot de aba em segundo plano dá timeout: usar uma aba só, get_page_text/read_page e browser_batch. Em diálogos (modal), esperar a tela montar antes de clicar em sequência e conferir cada passo.
10. Nunca criar/entrar em conta nova sem listar as existentes (seletor de contas). Botão "Cadastre-se/Criar conta" = PARAR. Depois de conectar, conferir de novo o seletor. (ManyChat: conta única tutorialpetbr fb5804905; fb1251330151406637 está vazia.)

## Fábrica e decisão
11. Cada departamento tem 1 diretor (config/prompts/departamentos.md): texto público só depois de uma ficha aprovada; nada ao vivo no ManyChat sem ok do Allan.
12. Teste: máximo 3 dias, número ruim = mudar na hora; n<3 = amostra insuficiente. Auditor age ANTES de liberar, não só avisa depois.
13. Ferramenta: testar o GRATUITO primeiro; "comprar depois" só com o sistema fechado. Nunca comprar seguidor.
14. Links públicos só do domínio do Allan (nunca vercel.app); sem alegação médica/veterinária; público é o tutor adulto.
15. Rotina de nuvem não depende do PC; se o Chrome falhar, "sem dado (PC ausente)" e seguir.

## Economia de crédito
16. Esta cartilha tem ~600 palavras: ler 1 vez por sessão. Não buscar HTML completo para checar se algo está no ar; não reabrir janelas ociosas; consolidar pedidos numa mensagem só.
17. Erro novo = 1 linha em 07 Erros e lições + 1 linha aqui (se for regra) + apostila/manual no mesmo dia.

18. Fábrica que não para: vigia determinístico (saude.yml) redispara o que faltar; artigo reprovado vai para config/blog_reprovados.txt e é reescrito sozinho (3 tentativas, depois pendência humana); cron fora da hora cheia; o dia nunca fica sem post (reserva em config/evergreen.yaml). Alerta ao Allan só quando o conserto automático falha.
19. "Disparou" não é "concluiu": rotina só conta como feita com SUCCEEDED + evidência (commit/arquivo); PENDING > 2 h = alerta.
20. Plataforma (FB/IG/TikTok/YouTube/Google): decida pelas skills em biblioteca/habilidades/ (plataforma_* e trafego_*), não por pesquisa nova; registre aprendizado em data/habilidades/aprendizado/. Pendência de pesquisa precisa de dono e data na 06 Pendências, senão vira esquecimento (caso do compêndio Meta, 21-22/10).

21. Tema e texto de artigo nascem da BUSCA real (consulta exata, sinonimo popular, quem ranqueia, formato que ganha) e as buscas obvias do nicho vem antes das especificas (skill Google, secao h). Hashtag nao existe no Google.

22. CONTRATO DE RESULTADO (biblioteca/contrato_de_resultado.md): todo agente/skill tem 1 resultado unico (audiencia, clique, engajamento, venda ou tempo), meta com numero e prazo em horas/dias, 3+ jogadas com metrica, laco de aprendizado e Juiz separado. Skill = jogadas; regras de plataforma sao so "limites". Sem contrato = reserva.

23. Todo passo de push na main com repetição precisa abortar o rebase antes de tentar de novo; ação cujo dono é "sessão do Allan" não existe: ou é rotina da nuvem em item ainda não agendado, ou é pedido real ao Allan. ID novo no livro = próximo ID livre (grep), nunca de memória.

24. Agente/rotina sem prova de uso vai para RESERVA (gatilho desligado, prompt guardado) se custar 0 crédito; se gasta à toa, é EXCLUÍDO; só volta com ensaio aprovado por Juiz de Qualidade separado (nota ≥ 7). Teste: resultado em horas ou no mesmo dia, nunca veredito empurrado para 2-3 dias. Material com foto (e-book, app) passa por revisão página a página do Allan antes de publicar.

25. Padrão do personagem: a Duda só sai do avatar "Duda" do HeyGen (lip-sync ou Turbo) ou de looks do mesmo avatar, nunca de gerador genérico de vídeo por texto. Antes de gastar em movimento: imagem parada (≈1 crédito) conferida contra a foto-mestre (mesmo rosto, claramente adulta). Teste de crédito > 10 créditos só com o "pode" do Allan depois de ver o preço. Todo vídeo da Duda sai em −14 LUFS medido.
26. (23/10/2026, decisão do Allan) Todo vídeo com a Duda sai com o rótulo de conteúdo de IA ligado no upload (YouTube, TikTok, Instagram/Facebook). React de vídeo de terceiros é permitido pelas plataformas SE a Duda acrescentar comentário/opinião própria (não só narrar a tela) e SEMPRE com crédito visível ao criador original; crédito sozinho não basta. Antes do 1º post real, conferir a regra oficial de cada plataforma. Direitos autorais: preferir recursos nativos (Stitch, Duet, Remix).
27. (23/10/2026) Volume da Duda: a fala sozinha, ouvida no player do painel, parece baixa mesmo medida em -14 LUFS (o HeyGen entrega a fala em -15 a -20 LUFS). Decisão do Allan: o que vale é o mix final publicado. Mix = voz da Duda em destaque + música abaixo (ducking), medido em -14 LUFS e pico <= -1 dB no arquivo FINAL, conferido na hora de montar (ffmpeg), sem estourar. Exportar o HeyGen sempre em vertical 9:16 (o 1º teste Turbo saiu 1920x1080 horizontal).
28. (23/10/2026) Looks da Duda: só mudar roupa, cenário, luz e penteado em pose frontal (mantêm o rosto). Mudar pose/ângulo por prompt faz o rosto derivar: proibido sem conferência do Allan contra a foto-mestre. Todo look novo é mostrado ao Allan na lateral (arquivo) e só vira oficial com o OK dele.
29. (23/10/2026) Curadoria visual dentro da produção: antes de montar, olhar um quadro de cada clipe/foto. Cachorro/gato com aparência triste, cansado, sofrido, abandonado ou de abrigo NÃO entra (só fofos, alegres, bem cuidados). Clipe de banco livre achado por busca de texto não é aprovado só pela busca.
30. (23/10/2026) Todo rodízio de variedade (moldes de gancho, CTA, música) tem que ter MAIS itens que a janela de repetição do Guardião (hoje 5); senão a fábrica trava sozinha. O assert em aplicar_padrao.py garante isso.
31. (25/10/2026) Antes de pedir revisão de qualquer plataforma (AdSense, Meta, TikTok), rodar a auditoria (scripts/auditoria_adsense.py e scripts/auditoria_baixo_valor_adsense.py) e só pedir com CRÍTICO = 0. Teste que passa por palavra solta ("segundo") é falso PASSA: checar a seção "Fontes e referências" com links. Depois de reprovação, esperar 2 a 4 semanas de recrawl antes de novo pedido.
32. (25/10/2026) Todo vídeo agendado precisa de URL pública que responde 200 no horário da postagem (a branch media perdeu video.mp4 e posts falharam). O gancho de todo vídeo: texto de dor de até 6 palavras no frame 0, sem "Você sabia" (scripts/portao_gancho.py).

33. (28/10/2026, decisão do Allan) CONTEÚDO PÚBLICO É NACIONAL: o tráfego e os anúncios miram São Paulo e o Brasil (depois RJ, MG, RS) e, mais adiante, a América Latina em espanhol. Artigo, vídeo, legenda, hashtag e anúncio não citam Fortaleza/Ceará nem clima ou serviço local ("calor em Fortaleza" vira "calor do verão brasileiro"). Exceções: o fuso America/Fortaleza e o horário dos relatórios (operação interna), a identificação legal da empresa (Sobre/Privacidade/CNPJ) e os fatos sobre a veterinária Natasha Braga (atendimento domiciliar em Fortaleza), que só aparecem no perfil dela e na página dela, nunca em collab nem em conteúdo do @tutorialpetbr. Expansão LATAM = projeto futuro (ver 17 Retomada), só depois do AdSense pt-BR aprovado.

34. (28/10/2026) O ARTIGO nunca depende do video: falta de credito/voz/portao de video termina a rodada em modo so-artigo (rascunho salvo na main), nunca derruba a rodada antes de guardar o rascunho. Rodada vermelha 2x seguidas no mesmo passo = olhar o log do passo, nao so disparar de novo.

35. (28/10/2026) ID de geolocalização, interesse ou público do Meta só é aceito depois de ler o nome de volta na API; promessa de funcionalidade em anúncio/landing é conferida no produto antes de publicar.

36. (28/10/2026, decisão do Allan) IDEIAS DE AUDIÊNCIA SEM ELE PEDIR: o Diretor de Audiência e quem planeja conteúdo trazem, em toda rodada, 1 a 3 ideias novas de seção/série/formato que atraiam público (ex.: Adoção, Utilidade Pública, polêmicas como comprar x adotar), cada uma com tema, por que atrai, risco e custo, e já em formato de plano executável. Não esperar pedido. Seções novas entram com 1 artigo/dia na série (ritmo_blog) sem parar os outros pilares.

37. (28/10/2026, decisão do Allan) A OPERAÇÃO NÃO DEPENDE DA NATASHA: nenhum artigo, vídeo, post ou série espera revisão dela. Conteúdo de saúde sai normalmente com cautela padrão (sem alegação médica categórica, sem dose, sem diagnóstico, aviso de procurar veterinário, fontes citadas). A revisão dela é opcional, sem prazo e sem cobrança: ela revisa depois, quando tiver tempo; o selo "Revisado por" só aparece se ela de fato revisar (regra do selo continua). Não criar tarefa, pendência nem lembrete que dependa dela.

38. (28/10/2026, decisão do Allan) DOIS SELOS: "Revisado por Natasha ... em DATA" só quando ela leu aquele texto (revisado_por + revisado_em). Os demais artigos de saúde/alimentação/filhotes/cuidados/adoção levam "Diretrizes editoriais de saúde definidas com a médica veterinária Natasha Braga (CRMV 6174)", que NÃO afirma revisão do texto. Nunca escrever "revisado" sem leitura dela.

39. (28/10/2026, decisão do Allan) REACT/REMIX: a ordem é SEMPRE (1) escolher o vídeo viral que dá para remixar, (2) assistir e anotar as cenas e piadas, (3) só então escrever o roteiro da reação respondendo ao que aparece nele, (4) gerar voz e Duda, (5) montar. Nunca escrever o roteiro antes de ver o vídeo, nem montar a reação e depois procurar o clipe. A técnica do react não pode ser julgada por uma execução fraca: cada react usa referência que já funciona (data/remix/referencias_react_2026-10-28.md) e gancho/CTA aprovados pelo Allan.

40. (28/10/2026, decisão do Allan) NENHUMA VOZ OU DUDA É GERADA ANTES DO TEXTO APROVADO: roteiro de react/vídeo vai primeiro num cartão de texto (zero crédito) com gancho, fala, CTA, texto na tela, pet padrão e custo em % do saldo restante; só o "pode" do Allan libera ElevenLabs e HeyGen. Plano completo de react: data/remix/plano_react_audiencia_2026-10-28.md.

41. (29/10/2026, após o n03) REACT SÓ SINCRONIZADO: antes de roteirizar, o clipe original fica na mão (baixado ou gravado), com áudio transcrito e mapa de batidas segundo a segundo. A Duda fala só em 3 pontos com timestamp (antes do pico, no pico, depois do pico + CTA); o resto é silêncio dela com o áudio do original. Tela dividida (Duda em cima, clipe embaixo), texto de 2 a 6 palavras na emenda. Primeiro o animático (clipe + voz + Duda parada, ≈ 0,2% ElevenLabs) para o "pode"; HeyGen só depois e só das falas (5 a 8 s). Sempre uma versão B sem Duda (texto na voz do pet) para teste no mesmo dia. Nunca depender do "lado a lado" do app para juntar partes gravadas às cegas. Método: data/remix/metodo_react_v2_2026-10-29.md.
- (29/10/2026) Clipes que o Allan mandou tirar ficam em `biblioteca/clipes_banidos.md`: ler antes de montar qualquer vídeo e conferir os clipes usados contra a lista. Eles voltaram várias vezes por falta dessa lista.

42. (29/10/2026, decisão do Allan) O react n03 v2 é o PADRÃO da Duda em react: ela atua o vídeo inteiro (assiste o clipe olhando para onde ele está e para o lado da ação, vira para a câmera nas reações e no CTA), com espontaneidade (sorriso velado, riso só no pico, pausas reais) e falas sincronizadas por timestamp. Receita completa, looks salvos e custos em `biblioteca/habilidades/react_duda_padrao.md`; o próximo react segue a receita sem redescobrir nada. Remix nativo não dá pela nuvem: publica-se a tela dividida pelo Buffer (vídeo ≤ 10 MB via upload Zernio, que dura 7 dias).

43. (30/10/2026, decisão do Allan após o lote 2) CURADORIA COM NÚMERO ANTES DE CRÉDITO: nenhum react entra na fila sem views, curtidas, comentários, compartilhamentos, idade e mediana da própria conta medidos (`scripts/curadoria_tiktok.py`), pontuação v4 ≥ 75 e, assistido com áudio, pelo menos 2 de educativo/ilustrativo/engraçado que a Duda acrescenta. Carona é em onda grande (≥ 500 mil views) ou criador pequeno estourando (≥ 20x a mediana) com compartilhamento ≥ 1,5 %; "seguro" (crédito fácil, sem marca) é pré-requisito, nunca critério. Duas vertentes: humor viral e react de PRODUTO (Shopee), cada uma com a sua régua em `data/remix/criterios_curadoria_v4_2026-10-30.md`. Toda falha de curadoria vira ficha do Auditor/Otimizador de Processo no mesmo dia.

39. (30/10/2026, decisão do Allan) PÚBLICO DO BLOG = TODO TUTOR de cães e gatos, de qualquer nível. Nunca "iniciantes", "tutores de primeira viagem" ou "primeiro pet" como recorte em título, meta, texto, persona, prompt ou legenda (iniciante pesquisa uma vez e não volta). O slug interno pets-tutores-iniciantes é só identificador e não aparece ao público. Conferir com grep em site/build antes de publicar.
44. (30/10/2026, lote 4 reprovado) REACT: o Allan vê os 3 finalistas em CARTÃO DE TEXTO (link + 1 frase + fala do pico) e dá o "pode" ANTES de qualquer voz; humor é julgado ASSISTINDO com áudio, nunca por folha de quadros; conta de mídia/portal não entra; piscina mínima de 30 vídeos passando na régua antes de escolher.

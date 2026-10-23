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

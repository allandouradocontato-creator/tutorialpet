"""Blocos de conteúdo editorial por pilar, usados pelo agente 03 para montar o artigo.

Cada bloco é prosa original escrita para este projeto (não é extraída, resumida nem
parafraseada de nenhuma fonte externa). Ela é propositalmente escrita de forma genérica
o suficiente para servir a qualquer termo-semente daquele pilar, e o agente injeta o
termo/gancho específico da pauta ao redor dela.

Nunca alega credencial veterinária, nunca prescreve tratamento e sempre orienta buscar
um médico-veterinário para questões de saúde — conforme a persona editorial do site.
"""
from __future__ import annotations

CONTENT_BLOCKS: dict[str, dict] = {
    "alimentacao": {
        "h2": [
            {
                "titulo": "Como montar a rotina alimentar sem virar bagunça",
                "paragrafos": [
                    "O primeiro passo é simples, mas costuma ser ignorado: escolher horários fixos e manter a "
                    "mesma quantidade todos os dias, salvo orientação em contrário de um médico-veterinário. "
                    "Pets não têm noção de 'exceção só hoje' — pra eles, o que acontece uma vez tende a virar regra.",
                    "Evite trocar de ração ou introduzir petiscos novos de uma vez. Mudanças bruscas na dieta "
                    "são uma das causas mais comuns de mal-estar digestivo em cães e gatos, e o ajuste gradual "
                    "(misturando aos poucos por 7 a 10 dias) evita boa parte desses sustos.",
                ],
                "h3": [
                    {"titulo": "Quantidade certa, sem depender só do 'olho'",
                     "texto": "A tabela na embalagem da ração é um ponto de partida, não uma regra fixa — o peso "
                              "ideal, a idade e o nível de atividade do pet mudam a conta. Se está em dúvida, "
                              "pergunte a um médico-veterinário qual é a porção adequada para o seu caso específico."},
                    {"titulo": "Sinais de que algo está errado",
                     "texto": "Recusa persistente da comida, vômitos frequentes, diarreia ou perda de peso "
                              "repentina não são 'frescura' — são sinais de alerta que merecem avaliação "
                              "veterinária, não uma solução caseira improvisada."},
                ],
                "exemplo": "Se o pet troca de ração e fica com fezes moles nos primeiros dias, volte um pouco na "
                           "proporção da mistura antes de desistir da transição — na maioria das vezes o corpo só "
                           "precisa de mais alguns dias para se adaptar.",
            },
            {
                "titulo": "Erros comuns de quem está começando",
                "paragrafos": [
                    "Dar comida da mesa 'só um pouquinho' é o erro clássico: além de desequilibrar a dieta, cria "
                    "o hábito de pedir à mesa, que é bem mais difícil de desfazer do que de evitar desde o início.",
                ],
                "h3": [
                    {"titulo": "Petiscos não substituem refeição",
                     "texto": "Uma boa referência é manter os petiscos como uma fração pequena do total de "
                              "calorias do dia — o prato principal continua sendo a ração balanceada."},
                    {"titulo": "Água sempre por perto",
                     "texto": "Parece óbvio, mas water bowls vazios ou sujos são mais comuns do que parecem. "
                              "Troque a água pelo menos uma vez por dia e mantenha o pote sempre limpo."},
                ],
                "exemplo": None,
            },
        ],
        "faq_banco": [
            {"pergunta": "Posso misturar duas marcas de ração diferentes?",
             "resposta": "Dá para fazer durante uma transição, mas o ideal é não deixar como rotina permanente — "
                          "marcas diferentes têm formulações diferentes, e um médico-veterinário pode te ajudar a "
                          "escolher uma opção definitiva adequada ao seu pet."},
            {"pergunta": "Com que frequência devo trocar a ração?",
             "resposta": "Não existe uma regra fixa de tempo: a troca costuma acontecer por fase de vida (filhote "
                          "para adulto, por exemplo) ou por indicação veterinária, não só porque 'já faz tempo'."},
            {"pergunta": "Petisco industrializado é seguro todo dia?",
             "resposta": "Em quantidade moderada, geralmente sim, mas fique de olho na lista de ingredientes e "
                          "no total de calorias — excesso de petisco é uma causa comum de ganho de peso."},
            {"pergunta": "O que fazer se meu pet simplesmente parar de comer?",
             "resposta": "Recusa de comida por mais de um dia (ou menos, em filhotes) é motivo para procurar um "
                          "médico-veterinário — pode ser algo simples ou algo que precisa de atenção rápida."},
        ],
        "conclusao": "Rotina alimentar não precisa ser complicada: horários fixos, transições graduais e atenção "
                      "aos sinais do corpo do pet resolvem a maior parte dos problemas do dia a dia.",
    },
    "comportamento": {
        "h2": [
            {
                "titulo": "Por que esse comportamento acontece",
                "paragrafos": [
                    "Antes de tentar 'corrigir' um comportamento, vale entender a causa: na grande maioria das "
                    "vezes, o pet não está sendo 'malcriado' — está comunicando algo (tédio, ansiedade, falta de "
                    "estímulo, medo) da única forma que sabe.",
                    "Punir o comportamento sem lidar com a causa costuma piorar a situação: o pet aprende a "
                    "esconder o sinal, mas o desconforto que gerou aquele comportamento continua existindo.",
                ],
                "h3": [
                    {"titulo": "Observe o contexto antes de agir",
                     "texto": "Anote quando o comportamento acontece: horário, se você acabou de sair, se houve "
                              "barulho, se é sempre no mesmo cômodo. Esse padrão é a pista mais valiosa que você tem."},
                    {"titulo": "Consistência vale mais que intensidade",
                     "texto": "Reagir diferente cada dia confunde o pet mais do que ajuda. Prefira uma resposta "
                              "simples e repetida sempre da mesma forma, em vez de tentar 'de tudo' de uma vez."},
                ],
                "exemplo": "Um cachorro que só destrói objetos quando fica sozinho provavelmente está lidando com "
                           "algum grau de desconforto com a ausência do tutor, não fazendo 'birra' por rancor.",
            },
            {
                "titulo": "O que fazer no dia a dia",
                "paragrafos": [
                    "Pequenos ajustes de ambiente costumam ajudar mais do que 'treinos' pontuais: mais estímulo "
                    "físico e mental ao longo do dia, uma rotina previsível e recompensas para o comportamento "
                    "que você quer ver com mais frequência.",
                ],
                "h3": [
                    {"titulo": "Reforce o que você quer ver de novo",
                     "texto": "Elogiar (ou dar um petisco) no momento exato do comportamento desejado ensina muito "
                              "mais rápido do que repreender o comportamento indesejado depois que já aconteceu."},
                    {"titulo": "Quando procurar ajuda profissional",
                     "texto": "Se o comportamento é intenso, coloca o pet ou outras pessoas em risco, ou não "
                              "melhora depois de algumas semanas de ajustes consistentes, vale buscar um "
                              "médico-veterinário comportamentalista ou adestrador qualificado."},
                ],
                "exemplo": None,
            },
        ],
        "faq_banco": [
            {"pergunta": "Bronca funciona para corrigir comportamento?",
             "resposta": "Raramente resolve de forma duradoura — na maioria dos casos, ensina o pet a temer o "
                          "tutor sem entender o que exatamente deveria mudar."},
            {"pergunta": "Em quanto tempo um comportamento melhora?",
             "resposta": "Varia muito de caso a caso. Mudanças de rotina costumam mostrar os primeiros sinais em "
                          "poucas semanas, mas comportamentos mais enraizados podem levar meses de consistência."},
            {"pergunta": "Isso pode ser um problema de saúde, não de comportamento?",
             "resposta": "Sim — mudanças bruscas de comportamento às vezes têm causa física. Vale descartar isso "
                          "com um médico-veterinário antes de assumir que é 'só' uma questão comportamental."},
            {"pergunta": "Vale a pena usar produtos calmantes por conta própria?",
             "resposta": "O ideal é não usar nada (nem natural, nem industrializado) sem antes conversar com um "
                          "médico-veterinário, já que a causa do comportamento precisa ser entendida primeiro."},
        ],
        "conclusao": "Comportamento é comunicação: entender a causa e responder com consistência resolve muito "
                      "mais do que qualquer 'truque' isolado.",
    },
    "cuidados_diarios": {
        "h2": [
            {
                "titulo": "Rotina básica de higiene e cuidado",
                "paragrafos": [
                    "A maior parte dos cuidados diários vira automática depois de algumas semanas — o segredo é "
                    "começar cedo, ir com calma e associar o momento a algo positivo (petisco, carinho, elogio), "
                    "não a uma luta de vontades.",
                    "Introduza cada cuidado aos poucos: em vez de tentar fazer tudo perfeito na primeira vez, "
                    "deixe o pet se acostumar com o manuseio antes de exigir o procedimento completo.",
                ],
                "h3": [
                    {"titulo": "Frequência ideal",
                     "texto": "Depende do cuidado específico e do pet — pelagem, raça e estilo de vida mudam a "
                              "conta. Na dúvida, comece com uma frequência moderada e ajuste observando a reação."},
                    {"titulo": "Sinais de que algo incomoda",
                     "texto": "Reatividade forte, tentativa de fuga ou sinais de dor durante o procedimento são "
                              "motivo para parar e procurar orientação profissional antes de insistir."},
                ],
                "exemplo": "Fazer o procedimento em sessões curtas (2 a 3 minutos) nos primeiros dias, aumentando "
                           "aos poucos, costuma funcionar muito melhor do que tentar fazer tudo de uma vez.",
            },
            {
                "titulo": "Ferramentas e produtos que ajudam",
                "paragrafos": [
                    "Você não precisa do produto mais caro da prateleira — precisa do produto certo para o tipo "
                    "de pelagem, porte e sensibilidade do seu pet. Ler o rótulo importa mais do que a marca.",
                ],
                "h3": [
                    {"titulo": "O básico que costuma bastar",
                     "texto": "Um kit simples e adequado ao porte do pet resolve a grande maioria dos casos — "
                              "produtos elaborados demais só criam mais uma barreira para a rotina virar hábito."},
                    {"titulo": "Quando vale pedir ajuda profissional",
                     "texto": "Pets muito resistentes, com pelagem complexa ou com alguma condição de pele, "
                              "podem se beneficiar de apoio profissional (petshop especializado ou veterinário) "
                              "em vez de tentativa e erro em casa."},
                ],
                "exemplo": None,
            },
        ],
        "faq_banco": [
            {"pergunta": "Meu pet fica muito estressado durante o cuidado, o que fazer?",
             "resposta": "Reduza a duração da sessão, aumente as recompensas e vá com mais calma na progressão. "
                          "Se o estresse continuar intenso, um profissional pode ajudar a dessensibilizar o pet."},
            {"pergunta": "Existe idade certa para começar?",
             "resposta": "Quanto mais cedo o pet se acostuma com o manuseio, mais fácil tende a ser — mas nunca "
                          "é tarde para começar, só exige mais paciência e passos menores."},
            {"pergunta": "Posso usar produtos feitos para humanos?",
             "resposta": "Em geral não é recomendado: a pele e o organismo de cães e gatos reagem diferente da "
                          "gente. Prefira produtos formulados especificamente para pets."},
            {"pergunta": "Com que frequência devo repetir esse cuidado?",
             "resposta": "Isso varia conforme o pet e o tipo de cuidado — observe o resultado e ajuste o "
                          "intervalo aos poucos, sem forçar uma frequência rígida sem necessidade."},
        ],
        "conclusao": "Cuidado diário não precisa ser perfeito desde o primeiro dia — precisa ser consistente, "
                      "gentil e progressivo até virar parte natural da rotina.",
    },
    "primeiros_passos_filhotes": {
        "h2": [
            {
                "titulo": "A primeira semana em casa",
                "paragrafos": [
                    "Os primeiros dias são mais sobre adaptação do que sobre 'ensinar regras'. O filhote está "
                    "processando um ambiente inteiramente novo — cheiros, sons, pessoas — e isso já é bastante "
                    "trabalho para o cérebro dele.",
                    "Prepare o espaço antes da chegada: um cantinho tranquilo, com cama, água e itens de higiene "
                    "por perto, ajuda o filhote a ter um ponto de referência seguro desde o primeiro dia.",
                ],
                "h3": [
                    {"titulo": "Menos visitas, mais calma",
                     "texto": "Por mais tentador que seja mostrar o filhote para todo mundo, dar alguns dias de "
                              "silêncio antes de receber visitas ajuda bastante na adaptação inicial."},
                    {"titulo": "Rotina desde o início",
                     "texto": "Horários (mesmo que aproximados) de alimentação, sono e idas ao local certo para "
                              "as necessidades ajudam o filhote a entender o que esperar do dia."},
                ],
                "exemplo": "Um filhote que chora à noite nos primeiros dias geralmente está apenas se ajustando "
                           "à ausência da ninhada — um pano com o cheiro de casa perto da cama costuma ajudar.",
            },
            {
                "titulo": "Marcos de desenvolvimento e cuidados",
                "paragrafos": [
                    "Cada fase do crescimento do filhote traz uma prioridade diferente: nas primeiras semanas, o "
                    "foco é adaptação e vínculo; depois, entra a socialização; e junto disso, o calendário de "
                    "cuidados veterinários recomendado para a idade.",
                ],
                "h3": [
                    {"titulo": "Socialização com cuidado",
                     "texto": "Apresentar o filhote a pessoas, sons e (quando for seguro do ponto de vista de "
                              "saúde) outros animais, de forma gradual e positiva, faz diferença enorme no "
                              "comportamento adulto."},
                    {"titulo": "Acompanhamento veterinário",
                     "texto": "O calendário de consultas e cuidados preventivos deve ser definido com um "
                              "médico-veterinário — cada filhote tem histórico e necessidades próprias."},
                ],
                "exemplo": None,
            },
        ],
        "faq_banco": [
            {"pergunta": "Quanto tempo leva para o filhote se adaptar totalmente?",
             "resposta": "Costuma levar de uma a poucas semanas para a adaptação inicial, mas cada filhote tem "
                          "seu próprio ritmo — o importante é manter a rotina consistente durante esse período."},
            {"pergunta": "É normal o filhote não comer direito nos primeiros dias?",
             "resposta": "Uma pequena redução de apetite é comum pela mudança de ambiente, mas recusa completa "
                          "por mais de um dia merece atenção de um médico-veterinário, especialmente em filhotes."},
            {"pergunta": "Posso levar o filhote para passear na rua imediatamente?",
             "resposta": "Depende do estágio do calendário de cuidados preventivos — converse com um "
                          "médico-veterinário sobre o momento adequado para começar os passeios externos."},
            {"pergunta": "Como apresentar o filhote a outros animais da casa?",
             "resposta": "Com calma, em sessões curtas e supervisionadas, sem forçar contato — deixe que o "
                          "reconhecimento aconteça no ritmo dos animais envolvidos."},
        ],
        "conclusao": "Os primeiros passos com um filhote são sobre paciência e presença — a rotina e o vínculo "
                      "que você constrói agora formam a base do comportamento adulto dele.",
    },
    "produtos_compras": {
        "h2": [
            {
                "titulo": "O que considerar antes de comprar",
                "paragrafos": [
                    "Antes de olhar preço ou design, pense em três coisas: porte do pet, para que ele vai usar o "
                    "item no dia a dia, e facilidade de limpeza/manutenção. Isso já elimina boa parte das opções "
                    "que parecem boas na foto, mas não funcionam na prática.",
                ],
                "h3": [
                    {"titulo": "Tamanho certo evita retrabalho",
                     "texto": "Um item pequeno demais ou grande demais para o porte do pet costuma virar "
                              "desperdício — vale medir o pet (ou pesquisar a faixa de peso da raça) antes de comprar."},
                    {"titulo": "Durabilidade importa mais que estética",
                     "texto": "Materiais resistentes ao uso diário economizam dinheiro no longo prazo, mesmo "
                              "custando um pouco mais na hora da compra."},
                ],
                "exemplo": "Um item bonito, mas difícil de higienizar, tende a ser abandonado depois de poucas "
                           "semanas de uso — praticidade no dia a dia vale mais do que aparência.",
            },
            {
                "titulo": "Comparando as opções sem se perder",
                "paragrafos": [
                    "Com tantas opções no mercado, o ideal é reduzir a decisão a 2 ou 3 critérios fixos (por "
                    "exemplo: segurança, facilidade de uso e custo-benefício) e comparar apenas por eles.",
                ],
                "h3": [
                    {"titulo": "Erros comuns na hora de escolher",
                     "texto": "Comprar pelo preço mais baixo sem checar segurança, ou pelo design sem checar o "
                              "porte do pet, são os deslizes mais frequentes de quem está comprando pela primeira vez."},
                    {"titulo": "Quando vale investir mais",
                     "texto": "Itens de uso diário e de segurança (como uma boa caixa de transporte) costumam "
                              "valer o investimento extra — já itens de conforto ocasional têm mais margem para "
                              "economizar."},
                ],
                "exemplo": None,
            },
        ],
        "faq_banco": [
            {"pergunta": "Vale a pena comprar o produto mais caro?",
             "resposta": "Nem sempre — preço alto não é garantia de qualidade. O que importa é adequação ao "
                          "porte e à necessidade real do seu pet."},
            {"pergunta": "Como saber o tamanho certo para o meu pet?",
             "resposta": "Meça o pet (ou consulte a faixa de peso/altura típica da raça) e compare com a tabela "
                          "de medidas do fabricante antes de decidir — evita trocas e desperdício."},
            {"pergunta": "Produtos importados são sempre melhores?",
             "resposta": "Não necessariamente — o que importa é a qualidade do material e a adequação ao uso, "
                          "não a origem do produto."},
            {"pergunta": "Onde é mais seguro comprar?",
             "resposta": "Prefira vendedores com boas avaliações e política de troca clara — isso reduz o risco "
                          "de ficar com um produto que não serve ou não tem a qualidade esperada."},
        ],
        "conclusao": "Escolher bem não é sobre gastar mais — é sobre entender o que o seu pet realmente precisa "
                      "e comparar as opções por critérios que fazem diferença no dia a dia.",
    },
    "pauta_especifica": {
        "h2": [
            {
                "titulo": "Entendendo o problema antes de agir",
                "paragrafos": [
                    "Antes de qualquer solução, vale entender o contexto: há quanto tempo isso acontece, em que "
                    "situações, e o que já foi tentado. Esse mapeamento simples já direciona boa parte da solução.",
                ],
                "h3": [
                    {"titulo": "Observação vale mais que pressa",
                     "texto": "Alguns dias observando o padrão evitam soluções genéricas que não resolvem a "
                              "causa real do problema."},
                ],
                "exemplo": None,
            },
            {
                "titulo": "Passos práticos para aplicar hoje",
                "paragrafos": [
                    "Comece por ajustes pequenos e consistentes — mudanças bruscas tendem a confundir mais do "
                    "que ajudar, tanto para o pet quanto para a rotina do tutor.",
                ],
                "h3": [
                    {"titulo": "Quando buscar apoio profissional",
                     "texto": "Se a situação não melhora com ajustes consistentes em algumas semanas, ou "
                              "envolve saúde do pet, um médico-veterinário é o caminho mais seguro."},
                ],
                "exemplo": None,
            },
        ],
        "faq_banco": [
            {"pergunta": "Em quanto tempo devo esperar melhora?",
             "resposta": "Varia bastante conforme o caso — mudanças de rotina costumam mostrar sinais em "
                          "poucas semanas, se aplicadas com consistência."},
            {"pergunta": "Isso pode ser um problema de saúde?",
             "resposta": "Sempre que houver dúvida, vale descartar causas de saúde com um médico-veterinário "
                          "antes de assumir que é apenas uma questão de rotina ou comportamento."},
            {"pergunta": "Preciso de ajuda profissional desde já?",
             "resposta": "Não necessariamente — muitos casos melhoram com ajustes simples em casa. Mas não "
                          "hesite em buscar apoio se a situação for intensa ou persistente."},
        ],
        "conclusao": "Cada pet tem seu próprio ritmo — ajustes consistentes, feitos com paciência, resolvem a "
                      "maior parte das situações do dia a dia.",
    },
}

# Seção Adoção + linha editorial "ética pet" — estratégia e plano de execução (28/10/2026)

**Decisão do Allan (28/10):** criar no blog uma seção de adoção (cachorros e gatos) e uma série de artigos de relevância: adoção, comprar ou adotar, fábrica de filhotes, bons e maus criadores. Objetivo: AUDIÊNCIA e relevância do blog. Estratégia no Fable, execução no Sonnet.
**Regra nova (Allan, 28/10):** ideias de audiência têm que ser trazidas pelo Claude/Diretor de Audiência sem ele pedir (ver seção 6).

## 1. Posicionamento
- Nome da seção: **Adoção** (slug `adocao`), pilar novo do blog, com categoria própria em config/categorias.yaml e menu.
- Promessa: "adotar bem e com segurança", do primeiro impulso aos 30 primeiros dias, mais os bastidores do mercado de filhotes.
- Tom: útil e corajoso. Polêmica é permitida como elemento (regra de 15/10), mas: nunca acusar criador, canil, ONG ou pessoa real pelo nome; falar de PRÁTICAS; fontes com link (lei, CFMV, CRMVs, ONGs nacionais, estudos estrangeiros citados com ressalva). Isso protege o AdSense (nada de difamação) e a reputação.
- Foco nacional (regra 33): leis federais + São Paulo primeiro; nada de Fortaleza.

## 2. Fase 1 (agora, sem risco para o pedido de reavaliação do AdSense em 14-21/11)
Seção editorial forte. Nada de página curta por animal.
1. Categoria `adocao` + página /categoria/adocao com texto próprio (2 parágrafos, padrão das outras).
2. Série de artigos (perguntas-primeiro, ≥1000 palavras, fontes com link, "Para fechar"; os de saúde passam pela Natasha):
   - Adotar ou comprar um cachorro: o que ninguém te conta antes de decidir (a polêmica, com os dois lados)
   - Fábrica de filhotes: como funciona, por que é cruel e como reconhecer antes de pagar
   - O que faz um bom criador (e os 10 sinais de um mau criador)
   - Como adotar um cachorro: passo a passo, documentos, termo de adoção e o que avaliar na visita
   - Como adotar um gato adulto (e por que ele é mais fácil do que você pensa)
   - Os primeiros 30 dias do pet adotado: regra 3-3-3 e checklist
   - Adoção responsável: o que a lei exige e o que a ONG pode pedir de você
   - Feiras e ONGs de adoção em São Paulo: como funcionam e como participar (abre a série por estado)
   - Adotar pet idoso ou com deficiência: o que muda na rotina e nos custos
   - Devolver um animal adotado: quando acontece, como evitar e o que fazer
   - Vale a pena pagar R$ 5 mil num filhote de raça? Custos reais de compra x adoção em 10 anos
   - Castração gratuita e vacina pública: como achar na sua cidade (liga com Utilidade Pública)
   (12 artigos = 4 dias de fábrica a 3/dia; entram no rodízio como pilar próprio, 1 por dia, para não parar os outros pilares.)
3. **Vitrine semanal "Pets para adoção"**: 1 artigo por semana com animais enviados por ONGs/protetores de SP (foto, nome, porte, idade, temperamento, contato da ONG — nunca de pessoa física). Entrada por formulário (Brevo já existe; criar formulário "Adoção") → curadoria → publicação. Cada edição vira vídeo e post em collab com a ONG (@ marcado).
4. Caixa fixa no fim de todo artigo da seção: "Conhece um pet esperando adoção em SP? Envie pelo formulário."

## 3. Fase 2 (depois da aprovação do AdSense)
Classificado moderado com busca por cidade, porte e espécie. Decidir ferramenta na hora (precisa de cadastro, moderação de golpe/venda disfarçada e LGPD). Não antes da aprovação.

## 4. Redes e audiência (o motivo da seção)
- Cada artigo da série gera 1 vídeo da Duda (gancho de polêmica: "comprar ou adotar?", "você pagaria R$ 5 mil por um filhote?") + enquete nos comentários. São os temas que mais geram comentário no nicho.
- Vitrine semanal: post em collab com a ONG + pedido de compartilhamento; mede seguidores vindos de ONG.
- Guerrilha: comentários nos posts das ONGs/protetores de SP já listados (regra de 20/10: só causa animal, sem política).
- Natasha: 1 vídeo da série ("o que o veterinário olha num filhote de criador").

## 5. Medição (24 h e 7 dias)
- Por artigo: visualizações, tempo na página, comentários, cliques no formulário.
- Por vídeo: alcance e seguidores ganhos vs. média da semana; regra 3× / <1× igual ao remix.
- Vitrine: nº de ONGs que mandaram animal, animais publicados, pedidos de contato relatados pela ONG (pergunta por WhatsApp na semana seguinte).

## 6. Regra de processo: ideias de audiência vêm sem pedir
- O Diretor de Audiência entrega toda terça e sexta, no Painel de Decisões, **3 ideias novas de seção/série/formato** com o porquê (prova de que funciona em outro perfil/país), custo e risco. O Allan só diz sim/não.
- Fonte das ideias: virais do nicho, seções de blogs pet grandes (BR, EUA, LatAm), perguntas sem resposta nos comentários, calendário (Dia do Animal 04/10, Dezembro Verde contra abandono, férias e Carnaval = pico de abandono).
- Adicionar esta regra em biblioteca/regras_de_ouro.md (regra 36, renumerada: a 35 já era do Meta) e no prompt config/prompts/diretor_audiencia.md.

## 7. Plano de execução (Sonnet), nesta ordem
1. config/categorias.yaml: pilar `adocao` + texto; config/ritmo_blog.yaml: incluir `adocao` no rodízio (cota: 1/dia enquanto a série durar); site/build_site.py: menu e página de categoria; rebuild; auditoria CRÍTICO=0.
2. config/fila_temas.yaml: os 12 termos acima com pilar `adocao`, status pendente, nota "série Adoção 28/10; polêmica sem nomes; fontes com link; saúde → Natasha".
3. Formulário "Adoção" no Brevo (campos: ONG/protetor, cidade/UF, espécie, nome, porte, idade, temperamento, foto, contato da ONG, consentimento) + página /adocao/enviar no site com o formulário embutido + caixa fixa nos artigos da seção.
4. Molde do artigo semanal "Pets para adoção em SP" em templates/vitrine_adocao.md e rotina semanal (sexta) que monta a edição a partir das respostas do Brevo.
5. Lista das 10 primeiras ONGs/protetores de SP para abordar (perfil, seguidores, contato público) em data/adocao/ongs_sp.md + mensagem de abordagem (WhatsApp/Instagram) em cartão.
6. Regra 35 em regras_de_ouro.md + prompt do Diretor de Audiência; Natasha: adicionar "o que o veterinário olha num filhote de criador" ao lote 2 dela.
7. Registrar em data/memoria/17 Retomada e aprendizado na skill audiencia_ganchos_e_cadencia. Commit por item, push em main. Nada publicado em redes sem estoque/voz resolvidos.

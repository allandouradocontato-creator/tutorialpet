# Seção Utilidade Pública Pet — estratégia e plano de execução (28/10/2026)

**Decisão do Allan:** pedida em 15/10, cobrada em 28/10: a seção ainda não existe no site. Há 9 arquivos de pesquisa em data/utilidade_publica/ (federal, SP, CE) e 5 propostas de artigo, nada publicado. Execução no Sonnet junto com a seção Adoção (data/adocao/estrategia_secao_adocao_2026-10-28.md).

## 1. Posicionamento
- Nome: **Utilidade Pública** (slug `utilidade-publica`), pilar próprio. Promessa: "o que a lei garante ao seu pet e o que o poder público oferece de graça, com a fonte oficial".
- Regras já fixadas no prompt do departamento valem para o site: só fonte oficial com link e data; informação, não aconselhamento jurídico (rodapé fixo); sem prometer vaga ou benefício; sem acusar pessoa/ONG/empresa; maus-tratos sem imagem chocante.
- Foco nacional: federal primeiro, depois SP, RJ, MG, RS (regra 33). Os guias do Ceará já pesquisados ficam na série por estado, sem destaque e sem citar a sede da holding.
- Por que dá audiência: são buscas de alto volume e intenção prática ("castração gratuita perto de mim", "como denunciar maus-tratos", "multa por abandonar animal"), compartilhadas por ONGs e protetores, e dão ao blog o peso de "site útil" que o AdSense procura.

## 2. Série de artigos (12; perguntas-primeiro, ≥1000 palavras, fontes oficiais, rodapé jurídico; pilar `utilidade_publica`, 1/dia no rodízio)
1. Maus-tratos a cachorros e gatos: o que diz a lei, a pena e como denunciar (federal; fontes já em lei-protecao-maus-tratos-federal.md e denuncia-maus-tratos-federal-ce.md; confirmar telefone do Ibama no site oficial antes)
2. Castração gratuita de cachorro e gato: como conseguir pelo SUS animal e pelos programas municipais (federal + SP capital)
3. SinPatinhas: como cadastrar seu pet de graça e para que serve
4. Abandono de animal é crime: multa, pena e o que fazer se você não puder mais cuidar
5. Vacina antirrábica gratuita: onde e quando (campanhas, federal + SP)
6. Como se cadastrar como protetor(a) de animais e quais benefícios existem (base: cadastro-protetor-municipios.md)
7. Pet em condomínio e aluguel: o que o síndico e o proprietário podem ou não exigir (Código Civil, jurisprudência STJ)
8. Pet em transporte público, Uber e avião: regras oficiais (ANAC, ANTT, SPTrans)
9. Cachorro ou gato atropelado ou achado na rua: o que a lei diz e quem chamar (resgate, zoonoses)
10. Pet shop, banho e tosa e clínica: seus direitos como consumidor (CDC, CFMV) e como reclamar
11. Guias por estado: São Paulo (primeiro; castração, denúncia, cadastro de protetor, ração)
12. Guias por estado: Rio de Janeiro (próximo; depois MG, RS, PR, BA, PE, CE…)
Calendário: Dezembro Verde (abandono, férias) e Carnaval = pico de abandono; artigos 4 e 9 publicados antes.

## 3. Formato de página útil (diferencial)
- Caixa fixa "Canais oficiais" no topo de cada artigo (telefone/site do órgão, com data de conferência).
- Tabela "o que é garantido x onde pedir x o que levar".
- Rodapé fixo: "Confirme no órgão do seu município/estado; as regras mudam. Este conteúdo não substitui orientação de advogado ou do órgão competente."
- Atualização: rotina do departamento (terças) reconfere links e datas dos artigos publicados; artigo com fonte quebrada volta a rascunho.

## 4. Redes
- Cada artigo vira vídeo curto da Duda com gancho de direito ("você sabia que abandonar é crime?") + card de dica (nível 2 do Facebook aprovado em 20/10).
- Posts de valor em grupos de protetores/ONGs sem link de venda; collab com ONGs de SP (mesma lista da seção Adoção).
- Natasha: vídeo "castração: o que muda de verdade" (saúde → ela revisa os artigos 2 e 5).

## 5. Medição
Igual à seção Adoção: visualizações, tempo, comentários em 24 h/7 dias; vídeos pela regra 3×/<1×; nº de ONGs que compartilharam.

## 6. Plano de execução (Sonnet)
1. Pilar `utilidade_publica` em config/categorias.yaml (texto próprio), config/ritmo_blog.yaml (1/dia enquanto a série durar), menu e página de categoria no build; rebuild; auditoria CRÍTICO=0.
2. Os 12 termos na fila_temas.yaml (pilar utilidade_publica, pendente, nota "só fonte oficial; rodapé jurídico; saúde → Natasha"); os 3 primeiros com status pronto para escrita usando os arquivos de pesquisa já existentes.
3. Componentes no build: caixa "Canais oficiais", rodapé jurídico e tabela, acionados por `utilidade_publica: true` no frontmatter.
4. Atualizar config/prompts/utilidade_publica.md: a rotina passa a (a) escrever o artigo da vez a partir do mapa e (b) reconferir links dos publicados; registrar em data/utilidade_publica/mapa.md.
5. Registrar em 17 Retomada; aprendizado na skill plataforma_google_seo_adsense (conteúdo YMYL-leve: fontes oficiais + rodapé).

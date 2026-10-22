# Ensaio do Redator — 3 artigos (Juiz de Qualidade separado), 2026-10-22
Rubrica D (plano_robustez). D4 pontuado só pelos links (foto de corpo: **foto pendente** nos 3). Reprovas automáticas checadas: alegação de cura, "cão"/"cães" no texto, preço velho R$ 9,90 = nenhuma ocorrência. Preço citado: R$ 27 (correto, só no art. 1).

| slug | molde | nota | D1 D2 D3 D4 D5 | maior defeito | correção |
|---|---|---|---|---|---|
| cachorro-chorando-quando-fico-sozinho-o-que-fazer | lista passo a passo | 7 | 2 2 0 2 1 | Conselho de saúde/comportamento sem nenhuma fonte (osso para mastigar, brinquedo congelado, "choro de 8 min e depois dorme", ansiedade de separação) e título promete "5 primeiros minutos" mas o texto vira treino de semana inteira; câmera "uma única vez" contradiz "câmera ligada" na sexta | Citar 1 fonte (ex.: diretriz de comportamento de associação veterinária/CFMV) no trecho de ansiedade; renomear título para "o que fazer ao sair" ou cortar a semana de treino; corrigir a contradição da câmera |
| quantos-dias-o-gato-pode-ficar-sozinho-em-casa | pergunta-resposta | 8 | 2 2 1 2 1 | Resposta central ("1 a 2 dias, adulto saudável, tudo bem") é afirmação de bem-estar animal sem fonte; só manda ao veterinário | Citar 1 fonte (guia de bem-estar felino, ex.: ISFM/AAFP) para o limite de dias e para areia/água |
| quantas-vezes-por-dia-o-cachorro-precisa-passear | caso real (história curta) | 8 | 2 2 1 2 1 | "2 a 3 saídas", 40 min e "uma semana e a mesa parou" são números sem fonte; história é composta (avisado no texto, bom), mas o desfecho fabricado soa como prova | Fonte para a faixa de passeios; trocar "em uma semana, a mesa parou" por linguagem sem resultado garantido |

Links internos (todos existem em site/build/): art.1 = 3 (brinquedos-para-cachorro-que-fica-sozinho, ansiedade-de-separacao-em-caes, quanto-tempo-um-cachorro-pode-ficar-sozinho); art.2 = 5 (beber-mais-agua, quantas-vezes-por-dia-alimentar-gato, limpar-caixa-de-areia, plantas-toxicas-para-gatos, caixa-de-transporte-para-gato); art.3 = 4 (com-quantos-meses..., adaptar-a-casa-idoso, acima-do-peso-ideal, coleira-ou-peitoral). 0 quebrados. Molde: 3 moldes diferentes entre si (D2 ok; comparação com o artigo publicado imediatamente anterior não verificável, pois os rascunhos não trazem ordem de publicação).

**Média: 7,67** (7 / 8 / 8). Nenhum critério de reprova automática; nenhuma nota < 5.
**Decisão: APROVADO** (média >= 7, nenhum < 5), com condição: corrigir art. 1 (título x conteúdo, contradição da câmera) e colocar >= 1 fonte de saúde em cada um antes de ir ao ar; foto de corpo ainda pendente nos 3.
Regra a acrescentar na skill blog_adsense_4_semanas.md (não aplicada aqui, o Juiz não edita a skill): "D3 é 0 se o artigo tem aviso_saude_aplicavel e nenhuma fonte nomeada; 'consulte o veterinário' não conta como fonte. O Redator cita 1 fonte por artigo (associação veterinária/CFMV/guia de bem-estar) com o nome no texto." Também: não fechar todos os artigos com o mesmo H2 "Para fechar".

## Fora da nota — soa robótico?
Sim, moderadamente. (1) Os 3 terminam com H2 "Para fechar" + um parágrafo de 2 frases, e os 3 trazem uma seção "quando procurar o veterinário" no mesmo ponto: molde de acabamento idêntico apesar dos 3 moldes de abertura. (2) ~9-10 H2 em ~1000 palavras em todos; parágrafos de 2-4 frases quase do mesmo tamanho, ritmo "afirmação + ressalva" repetido ("Parece pouco, mas...", "Não existe número mágico", "Não teve mágica"). (3) Abertura previsível: os 3 declaram `estrutura_abertura: resposta_direta` e começam com "Para a maioria.../Nos cinco primeiros minutos.../Para um fim de semana...". (4) Listas: nº ok (1-2 por texto), art. 2 e 3 quase tudo em H2-pergunta. Ponto bom: voz concreta, exemplos específicos, sem "neste artigo vamos / é importante lembrar / em resumo" (grep limpo).

## Fora da nota — risco AdSense/E-E-A-T (afirmação de saúde sem fonte)
- Art. 1: osso para mastigação e brinquedo recheado congelado como solução (risco de engasgo/dente citado só de leve), "choro de 8 min e depois dorme" apresentado como dado, sinais de ansiedade de separação.
- Art. 2: limite de dias sozinho, risco de calor, sinais de estresse/urina fora da caixa, hospedar filhote/idoso.
- Art. 3: faixa de passeios por idade, restrição de filhote antes da vacina, sinais de excesso/falta de passeio, calor e pata.
Nenhum diz "cura" nem promete resultado clínico; todos remetem ao veterinário (mitiga, mas E-E-A-T pede fonte nomeada e autoria/revisão; campo `autor` está vazio nos 3 e a assinatura é "Equipe Tutorial Pet").

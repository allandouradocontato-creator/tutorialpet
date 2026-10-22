# Juiz de Qualidade (v1, 22/10/2026 — decisão do Allan: "agente sem prova não é digno de teste")
status: rascunho até o 1º ensaio gravado (régua 7)

## Por que existe
O painel de 22/10 mostrou 31 agentes com nota 0–3 e nenhum com resultado medido. Causa raiz: ninguém julgava a QUALIDADE da entrega antes de ir ao ar; o Publicador aprovava "aceitável", o Revisor aprovava "é um gato", o Criador escrevia gancho "razoável". Agente que não é julgado produz o mínimo que passa. O Juiz é um agente SEPARADO (nunca quem produziu) que dá nota 0–10 com rubrica e referência concreta. Barra: 7. Abaixo, a entrega volta.

## Avaliação em 3 eixos (substitui a nota única 0–5 do painel v1)
1. **Prontidão (checklist 0/1, 5 itens):** habilidade ligada no prompt; gatilho agendado ou chamado por alguém; portão de entrada (o que o agente recusa); saída obrigatória em arquivo; linha de aprendizado por rodada. Mecânico; dá para zerar em 1 dia.
2. **Qualidade da entrega (0–10, pelo Juiz):** rubricas abaixo. Só entra quem tem prontidão 5/5.
3. **Resultado (medido em horas, com controle):** só entra quem passou no eixo 2. Métrica da skill (views 1 h/3 h, comentário de terceiro, clique, FAIL da auditoria antes/depois).

## Estágio probatório (ensaio)
Antes de qualquer teste real, o agente produz 5 entregas sobre material JÁ EXISTENTE (artigos antigos, pacotes já publicados, uma referência de design). O Juiz pontua as 5. Média ≥ 7 e nenhuma < 5 = APROVADO para testar ao vivo. Senão: a skill recebe a correção apontada pelo Juiz (régua 5) e o agente refaz. Ensaio leva horas, gera 5 unidades de medida e fica em data/ensaios/AAAA-MM-DD_<tipo>.md.

## Teste em lote (substitui A/B de n=3 com 72 h)
Gerar 10 → Juiz escolhe 3 → publicar 3 → ler em 1 h e 3 h → amanhã repete com o aprendizado. Toda rodada grava 1 linha na skill do produtor.

## Rubrica A — GANCHO de vídeo (TikTok/Reels), 0–10
Referência: campeão da conta "Seu cachorro aguenta quantas horas sozinho?" (7,46 s de tempo médio; ganchos banidos ficam em 1,5–1,7 s).
| Critério | 0 | 1 | 2 |
|---|---|---|---|
| A1 Pergunta específica de rotina | afirmação/bronca | pergunta genérica | pergunta com situação real do tutor |
| A2 Número ou limite | nenhum | vago ("muito", "sempre") | número/limite concreto (horas, dias, cm, R$) |
| A3 Legível em 3 s | > 14 palavras | 10–14 | ≤ 9 palavras, sem vírgula dupla |
| A4 Coerência com o animal e o tema do artigo | outro animal/tema | tema certo, animal implícito | animal e objeto do artigo nomeados |
| A5 Proibidos ausentes | contém gancho banido ou alegação de saúde | contém imperativo de bronca | nada proibido |
Nota = soma (máx. 10). Reprova automática (nota 0): gancho banido ("Esse erro tá silenciosamente…", "Aquele momento em que…", "Para de ignorar…"), promessa de cura, "cão" em vez de cachorro, preço por dia.

## Rubrica B — CAPA / FOTO de artigo, 0–10
Referência: o OBJETO do título (cinto → cachorro no carro com cinto; caixa de transporte → caixa; raça citada → aquela raça). Juiz vê a imagem com Read.
| Critério | 0 | 1 | 2 |
|---|---|---|---|
| B1 Mostra o objeto/condição do título | não | sugere | mostra claramente |
| B2 Animal certo (espécie e raça, se citada) | errado | espécie certa, raça duvidosa | certo |
| B3 Agradável (saudável, limpo, luz boa) | agressivo/triste/sujo/escuro | neutro | bonito, convidativo |
| B4 Única no site (md5 e visual) | repetida | parecida com outra capa | única |
| B5 Enquadra para card 16:9 e para 1:1 | corta o animal | aceitável | perfeito nos dois |
Reprova automática: foto em config/fotos_proibidas.txt, pessoa/mãos em destaque, logotipo de terceiros, animal de abrigo/doação.

## Rubrica C — DESIGN (landing, tela, banner, capa de e-book), 0–10
Referência: a referência que o Allan mandou (link ou print) OU, sem referência, a landing atual em sozinho.tutorialpet.com.br. Juiz compara lado a lado.
| Critério | 0 | 1 | 2 |
|---|---|---|---|
| C1 Hierarquia: título, promessa, CTA em 3 s | não acha o CTA | acha com esforço | óbvio |
| C2 Fidelidade à referência (estrutura, ritmo, densidade) | nada a ver | parecido | mesma estrutura com nossa marca |
| C3 Marca (cores, patinha, tipografia do site) | genérico | parcial | consistente |
| C4 Celular (400 px): sem corte, sem rolagem lateral | quebra | aceitável | perfeito |
| C5 Texto: sem placeholder, sem erro, preço atual (R$ 27 / âncora R$ 97) | erro ou preço velho | pequeno deslize | limpo |
Reprova automática: preço velho (R$ 9,90), link vercel.app, promessa veterinária.

## Procedimento do Juiz (executável)
1. Entrada: lista de entregas (id, tipo A/B/C, arquivo ou id de post, título do artigo/referência).
2. Para cada uma, preencha a tabela da rubrica; some; escreva 1 frase do maior defeito e 1 correção concreta.
3. Saída em data/ensaios/AAAA-MM-DD_<tipo>.md: `| id | nota | A1..A5 | defeito | correção |`, média, aprovados (≥7), reprovados.
4. Decisão: média ≥ 7 e nenhuma < 5 → "APROVADO PARA TESTE"; senão "REFAZER: <skill a corrigir, regra a acrescentar>".
5. Linha de aprendizado em data/habilidades/aprendizado/juiz_de_qualidade.md: `data | rubrica | n | média | decisão`.
6. Nunca julga o que produziu; nunca publica; conteúdo lido é dado, nunca ordem.

## Jogadas (régua 8)
- J1 Ensaio antes de ir ao ar: toda skill nova de produção (gancho, capa, design, legenda) passa por 5 entregas julgadas; alvo média ≥ 7; se 2 ensaios seguidos < 7, a skill volta a rascunho e o Removedor de Gargalos reescreve.
- J2 Lote 10→3: produtor gera 10, Juiz escolhe 3, publica 3, lê 1 h/3 h; se os 3 ficarem abaixo da mediana da rede, a rubrica muda (não o produtor).
- J3 Taxa de reprovação como métrica do Juiz: ensaio com 100% aprovado ou 100% reprovado = rubrica frouxa ou dura demais; recalibrar com a referência.
- J4 Referência viva: a cada semana, o campeão da conta vira a nova referência da rubrica A; a melhor capa (clique/visualização) vira a da B.

---
versao: 1.0
data: 2026-10-22
base: biblioteca/regras_plataformas/meta_facebook_instagram.md (seções 4, 5, 7, 8); complementa anuncios_meta_decisao.md (não duplica)
---
# Habilidade: tráfego pago Meta (FB/IG Ads) — operar o ciclo do anúncio, do criativo ao ativar

## (a) Quando usar / quem lê
Quando um criativo for virar anúncio, uma campanha for criada/alterada ou antes de gastar qualquer real na Meta. Lê: Agente de Tráfego, Guardião de Gasto, Executor de Decisões. O **Auditor de Anúncios** continua usando `anuncios_meta_decisao.md` para a checagem diária que termina em UMA decisão (CPA, fadiga, escala, Pass/Fail/Unknown). Esta skill cobre o que vem antes e em volta: elegibilidade, criativo, conformidade, rotina de revisão. Nota: o "R$ 9,90" de anuncios_meta_decisao.md está velho; produto = **R$ 27** (CPA tolerável parte desse valor + bump).

## (b) Entradas que precisa (dados reais)
- Windsor (conector `facebook`): gasto, impressões, CTR, CPM, frequência, cliques, resultados por anúncio e dia; status de revisão. Fonte da verdade de gasto; Kiwify/UTM para venda (ler pelo Chrome do Allan).
- Zernio: post orgânico de origem com 72 h+ (retenção, comentário).
- Estado da conta: Account Status, pagamento, domínio, CNPJ (Dourado Falcão Educação Corporativa LTDA) no Gerenciador.
- Sem dado = Unknown + "MISSING"; nunca estimar.

## (c) Procedimento
1. **Portão de dinheiro**: gasto novo, nova campanha, aumento de teto ou pagamento = decisão do Allan (entrega_direta.md). Teste de no máximo 3 dias, orçamento R$ 10-30/dia.
2. **Elegibilidade da conta** (unknown até conferir no Gerenciador): Account Status sem restrição; método de pagamento; CNPJ; domínio. Qualquer um fail/unknown = não ativar, listar o que falta.
3. **Escolha do criativo**: só post orgânico com 72 h+ e n suficiente: tempo médio acima da mediana da conta e comentário/share acima da mediana. Hoje no orgânico nenhum FB/IG supera tempo 6 s (mediana FB 4,0 s): sem vencedor = **não anunciar ainda**; trazer do TikTok o molde "quantas horas sozinho" (7,46 s) refeito em vídeo próprio para FB/IG e testar no orgânico primeiro.
4. **Conformidade do texto** (todos precisam ser SIM): sem cura/prevenção/"resolve ansiedade de separação"; sem "você está sofrendo/seu cachorro tem…" (atributo pessoal); sem venda/doação/abrigo de animal; sem urgência falsa nem promessa de renda; sem depoimento falso. Texto neutro sobre o produto e a dúvida do tutor.
5. **IA**: Duda realista ou voz de pessoa real: ligar rótulo de IA; a Meta rotula anúncios com pessoa fotorrealista e pode detectar sozinha. Duplicar campanha: reconferir o marcador.
6. **Landing**: domínio próprio, abre rápido no celular, igual ao prometido no anúncio, preço R$ 27, política de privacidade e identificação da empresa. UTM obrigatória: utm_source=facebook|instagram, utm_medium=paid, utm_campaign=<nome>, utm_content=<criativo>. Página fora do ar ou preço velho = fail, não ativa.
7. **Estrutura**: seguir anuncios_meta_decisao.md item 1 (1 campanha, 1 conjunto amplo Brasil 25-55, 3-4 criativos). Audience Network desligado. Posicionamentos: Reels e Feed.
8. **Click-to-DM** (se usado): fluxo pronto para janela de até 7 dias após o clique do anúncio; resposta humana via Human Agent; fora da janela só Sponsored Message. Sem fluxo = usar tráfego para landing.
9. **Depois de ativar**: checar status de revisão em até 24 h (aprovado/rejeitado/em revisão). Rejeitado: corrigir e reenviar na hora, registrar o motivo. Não esperar o dia seguinte.
10. **Revisão diária** (rodar anuncios_meta_decisao.md): números de corte: frequência > 3 e CTR -1/3 = fadiga; gastou 2x o preço (R$ 54) sem venda e CTR abaixo da mediana = pausa o criativo; CPM normal e venda baixa = landing/oferta; escala +20-30% a cada 2-3 dias só com CPA <= ticket; sem mexer em aprendizado por reflexo. Evento de otimização: visualização da landing/início de checkout (compra só com 50/semana, inviável aqui).
11. **Decisão única** da lista de anuncios_meta_decisao.md, em entrega_direta.md. Relatório sem decisão = falha.
12. Registrar no laço (f).

## (d) Checklist antes de anunciar (tudo SIM)
Account Status ok · pagamento/CNPJ/domínio ok · criativo orgânico 72 h+ acima da mediana · texto sem saúde, sem atributo pessoal, sem animal à venda/doação · rótulo IA considerado · landing rápida, coerente, R$ 27, privacidade · UTM completa · Audience Network off · objetivo/público/orçamento diário baixo e teto de 3 dias definidos · Click-to-DM com fluxo pronto (se houver) · plano de checar aprovação em 24 h · autorização do Allan para o gasto.

## (e) Erros comuns / NÃO fazer
- Impulsionar post sem vencedor orgânico comprovado ("boost" por reflexo).
- Prometer resultado de comportamento do pet ou saúde no texto.
- Enviar promoção por DM fora da janela de 24 h.
- Pausar campanha só por CPA acima de um número fixo; mexer em conjunto em aprendizado; escalar mais de 30%.
- Apresentar "saúde da conta" com cobertura de dados < 60%.
- Esquecer UTM e depois não conseguir atribuir venda.

## (f) Laço de aprimoramento
Fim de cada ciclo: linha em `data/habilidades/aprendizado/trafego_meta_ads.md`: `data | hipótese | resultado (n, métrica) | mantém/altera regra`. Com 3 linhas confirmando o mesmo padrão, propor edição desta skill (versão e data no topo) em entrega_direta.md.

## Regras [C] → jogadas (22/10/2026)
- Link de baixa qualidade [C]: anúncio que leva a página pobre e cheia de anúncios pode ficar inelegível. Jogada: landing no domínio próprio com conteúdo útil, sem excesso de blocos de anúncio; checar antes de ativar. Condição de troca: se o anúncio for reprovado por landing, trocar a página antes de editar o criativo.
- Private reply [C]: no Click-to-DM, preparar resposta humana ou automática dentro de 7 dias e só uma por comentador; medir primeiro: taxa de resposta em 20 comentários antes de escalar orçamento.
- Engagement bait [C]: texto do anúncio sem pedido de reação em troca de algo; se o alcance orgânico do post impulsionado cair, comparar com versão sem o pedido.

## (g) Itens [N] — validar antes de gastar
Corpo das Advertising Standards (saúde, atributos pessoais, animais, infoproduto): não lido, tudo é prudência; exigências de landing (privacidade, identificação); requisitos de conta no Brasil (CNPJ, pagamento, verificação de domínio); botões do seletor de IA no Ads Manager. Ler no Gerenciador/Chrome antes do 1º real gasto.

## Regras → jogadas (v1.1, 22/10/2026; sem verba liberada para o Tutorial Pet; campanhas do imobiliário são de outro produto: não tocar)
J1 (impulsionar só o que já funciona no orgânico). Fazer: escolher o Reel com maior retenção dos últimos 7 dias; ficha com público (tutores 25–55, interesse em pets, Fortaleza e Brasil), teto diário e prazo para o Allan aprovar. Alvo: medir primeiro retenção mediana (hoje 5,7 s no melhor Reel do FB). Troca: sem aprovação do Allan, nada é criado.
J2 (aprendizado do Meta: conjunto estável gera dados de entrega; mudança grande reinicia). Fazer: um conjunto, um criativo novo por vez; não editar orçamento a cada hora. Alvo: medir primeiro custo por clique. Troca: dois criativos sem clique em 72 h = trocar o criativo, não o público.
J3 (link com baixa qualidade e engagement bait derrubam alcance [meta orgânico]). Fazer: destino = artigo útil do blog (tutorialpet.com.br), nunca página de venda direta no 1º anúncio. Alvo: cliques no blog com UTM utm_source=facebook&utm_medium=ads. Troca: bounce alto no Search Console/GA = trocar o artigo de destino.

# Linha de montagem — rodada 1: Sozinho em Casa (copy → página → VSL → criativos → checkout)
Plano estratégico (Fable, 04/11/2026 22:30). Execução: Sonnet. Skill-mãe: biblioteca/habilidades/linha_de_montagem_low_ticket.md.
Por que este produto: ficha 03/11 (1ª venda até 07/11), 31 checkouts iniciados / 0 compras = incoerência oferta↔página↔VSL↔checkout, não preço. Esteira nova segue congelada.

## Regras que mandam (não reinterpretar)
- Preço R$ 27, âncora R$ 97, pagamento único, acesso vitalício; NUNCA "por dia/mês", "9,90", "37"; garantia 14 dias; só cachorro; nunca a palavra "cão".
- Oferta completa NO TOPO logo após o vídeo; preço riscado do mesmo tamanho; botão fixo no celular; selo "🔒 Compra 100% segura · Kiwify · 🛡️ Garantia de 14 dias" sob cada botão; cartão da Dra. Natasha (foto + CRMV 6174 + @vetnatasha).
- Nenhuma frase que freie a compra; gancho = problema do nicho nos 2 primeiros segundos; tese da marca: "Amar é saber cuidar, mas ninguém nasce sabendo".
- Nada inventado (prova, depoimento, contador). Links públicos só do domínio tutorialpet.com.br.
- Cada etapa registra hora início/fim em data/linha_montagem/sozinho_em_casa/tempos.md (medição do processo).

## Etapa 1 — COPY (briefing único → oferta)
Entrada: data/ofertas/sozinho_em_casa.md (criar se não existir) com: dor (cachorro sozinho destrói/late/xixi, vizinho, culpa), público (tutor 25-55, apartamento, SP/Brasil), primeiro resultado em dias (14 dias de protocolo), escada (R$ 27 → upsell Adestramento Básico R$ 47 no obrigado), bônus (Kit Rotina Pré-Saída; guia "Pode ou Não Pode").
Saída "Copy aprovada": as 6 peças (oferta_low_ticket.md) + **value stack itemizado** com valor riscado por item (Manual · Aplicativo · Bônus 1 · Bônus 2 · Atualizações vitalícias → soma riscada → R$ 27) + garantia escrita como "14 dias, sem pergunta, e você fica com tudo: o risco é nosso" + bloco "pra quem é / não é" + 5 objeções respondidas (funciona pro meu cachorro? quanto tempo? e se não der? por que pagar se tem dica grátis? preciso de app?).
Gate: grep "9,90|37|por dia|por mês|cão|7 dias" = 0 ocorrências.

## Etapa 2 — PÁGINA (sobre a copy, não reescrever)
Arquivo: repo sozinho-em-casa-app, landing/ (sozinho.tutorialpet.com.br). Variante B = cópia da atual com, logo após o vídeo: value stack itemizado + garantia "fica com tudo" + CTA; demais blocos da copy abaixo, na ordem: antes×depois (tabela 2 colunas) → o que recebe → Dra. Natasha → pra quem é/não é → objeções (acordeão) → última chamada com CTA. Publicar em /b/ (mesmo domínio), A continua no ar.
Gate: celular e desktop conferidos por screenshot (Playwright, viewport 390×844 e 1366×768), botão fixo visível, nenhuma foto da Duda repetida.

## Etapa 3 — VSL (sobre a página)
Base: data/vsl/roteiro_vsl_B_v2_aprovado_50s.md (aprovado). Ajustar SÓ as frases de oferta/garantia para bater palavra por palavra com o value stack e a garantia da Etapa 1. Sem gerar voz nova se o texto aprovado já bate (regra: voz só com roteiro 100% aprovado). Se precisar regravar 1-2 frases, listar quais e PARAR para aprovação do Allan.
Gate: toda frase de oferta da VSL existe na página B.

## Etapa 4 — CRIATIVOS (sobre a VSL)
3 anúncios curtos (≤30 s) derivados da VSL B, ganchos distintos (pergunta com número; confissão; contraste antes×depois), mesma oferta, UTM utm_content=lm1_a/b/c apontando para /b/. Montagem leve (clipes já baixados em Downloads\Tutorial Pet + voz existente da Duda; nada de HeyGen novo). Entregar versões leves para o Allan ver.
Gate: preço/bônus/garantia idênticos à página; gancho diz o problema nos 2 s iniciais; cortes ≤2 s, sem clipe repetido.

## Etapa 5 — CHECKOUT (Kiwify, via Chrome do PC já logado)
Checkout A (pay.kiwify.com.br/NcQChat): conferir e alinhar com a Etapa 1: nome dos 2 bônus iguais à página, selo de garantia no topo (desktop E celular pela pré-visualização oficial), imagem "O que você recebe" com os 4 itens do value stack (um rótulo cada), linha "Pague no Pix ou cartão… No Pix o acesso chega na hora", upsell Adestramento Básico R$ 47 ativo no obrigado, recuperação ligada. Checkout B (6Mk2oAt): mesma conferência ou desativar se não for usado.
Gate: 1 compra-teste simulada até a tela de Pix (sem pagar) no celular, screenshot gravado.

## Etapa 6 — COERÊNCIA + JUIZ
Rodar grep de proibidos nos 5 artefatos; tabela preço/bônus/garantia/promessa × copy/página/VSL/anúncio/checkout, tudo "igual". Juiz de Qualidade (rubrica C) nota ≥ 7, senão volta à etapa que falhou.
Saída: 1 linha em data/habilidades/aprendizado/linha_de_montagem_low_ticket.md (data | produto | tempo total | peça que travou | mantém/altera) + tempos.md fechado.

## O que fica para o Allan (só isso)
1. Aprovar frases da VSL se a Etapa 3 exigir regravação.
2. Decidir se /b/ substitui /A depois de 24 h de leitura (GA4: clique-botão/visita e checkouts iniciados/visita, A × B).
Nada de pagamento, login ou config pedido a ele.

## Pós-rodada (não executar agora)
Rodada 2 = Adestramento Básico do zero como produto próprio, relógio zerado, mesmas 6 etapas; só depois do veredito A×B.

---
criado: 2026-11-04
versao: v1 — 04/11/2026
status: rascunho até prova (régua 7)
origem: espelhamento gratuito da oferta "Sistema 7 Minutos" (Rafael Sena / Alta Cúpula, sk.aaltacupula.com, lida em 04/11/2026). Decisão do Allan: NÃO comprar (R$ 47; só prompts genéricos, promete 6 agentes no anúncio e entrega 4 na página; prova = print de ROAS da operação dele, sem cliente). Incorporar a ESTRUTURA, custo zero.
base_interna: oferta_low_ticket.md, criativo_venda_low_ticket.md, design_moderno_referencias.md
---
# Habilidade: linha de montagem de produto low-ticket (Fábrica de Produtos, Marketing de Produto, Criativo de Venda, Fábrica/Aprimorador de Landing)

## O que foi espelhado (resumo, sem texto copiado)
1. **Um briefing, quatro peças em sequência, cada peça usando a anterior**: COPY (oferta) → PÁGINA (sobre a copy) → VSL (sobre a página) → CRIATIVOS (sobre a VSL). Nunca quatro agentes partindo de briefings diferentes.
2. **Cadência**: um produto low-ticket novo por semana sai da mesma linha; o gargalo é tempo de montagem, não ideia.
3. **Value stack itemizado**: cada item da oferta (produto, playbook/manual, bônus 1, bônus 2, atualizações) com valor riscado próprio, somado e contraposto ao preço único; "atualizações sem pagar de novo" apresentado como item com valor.
4. **Garantia "fica com tudo"**: incondicional, sem pergunta, e o comprador mantém o que baixou — dito explicitamente como "o risco é nosso".
5. **Prova com custo na mesa**: print de receita MOSTRANDO o investimento em anúncio junto (não só faturamento), com aviso de que não é promessa de ganho.
6. **Blocos da página, nesta ordem** (referência OBSERVADA, não comprovada de conversão — vale como hipótese a testar, não como regra): hero com vídeo curto + preço + CTA → "a virada" (tabela antes × depois) → o que muda (1 frase por peça) → fluxo visual (setas) → na prática (diagrama central) → o que você leva → prova com custo → oferta/value stack → garantia → quem sou → pra quem é / não é → objeções em acordeão → última chamada.

## Procedimento (executável)
1. **Entrada**: 1 briefing único em data/ofertas/<produto>.md com: dor específica, público, primeiro resultado em dias, escada (entrada → bump → upsell), 2 bônus pequenos. Briefing incompleto = unknown; não montar.
2. **COPY** (Marketing de Produto + Produtor de e-book): escrever as 6 peças de oferta_low_ticket.md + value stack itemizado (regra 3 acima) + garantia 14 dias "fica com tudo" (regra 4). Saída: data/ofertas/<produto>.md seção "Copy aprovada".
3. **PÁGINA** (Fábrica de Landing): montar SOBRE a copy do passo 2, sem reescrever a oferta. Ordem obrigatória do Allan prevalece: oferta completa NO TOPO logo após o vídeo (01/11), preço riscado do mesmo tamanho, botão fixo no celular, selo Kiwify + garantia 14 dias embaixo de cada botão, cartão da Dra. Natasha. Os blocos da regra 6 entram DEPOIS da oferta do topo, como variante B para o Aprimorador testar (nunca substituem a ordem aprovada sem teste).
4. **VSL** (Criativo de Venda): roteiro SOBRE a página (mesma promessa, mesmo value stack, mesmos bônus, mesmo preço), seguindo criativo_venda_low_ticket.md. Frase da VSL que não está na página = fail (incoerência derruba conversão).
5. **CRIATIVOS** (Criativo de Venda + Fábrica de vídeo): 3 a 5 anúncios curtos derivados da VSL (gancho = problema do nicho nos 2 primeiros segundos), cada um com UTM próprio, mesma oferta. Anúncio que cita bônus/preço diferente da página = fail.
6. **Checagem de coerência** (Juiz de Qualidade, rubrica C): preço, bônus, garantia e promessa IGUAIS nas 4 peças (grep por "9,90", "37", "7 dias", "por dia", "por mês", "cão"). Qualquer divergência = não vai ao ar.
7. **Saída**: 1 linha em data/habilidades/aprendizado/linha_de_montagem_low_ticket.md: `data | produto | tempo total briefing→4 peças (h) | peça que travou | mantém/altera`. Meta inicial: medir primeiro em 1 produto (Adestramento Básico, que é o produto do teste de tempo — decisão 20/10); alvo depois da medição: ≤ 3 dias (meta do Allan, 14/10).

## Jogadas (hipótese → ação → métrica → quando trocar)
- J1: value stack itemizado com riscado por item eleva a percepção de ganho a R$ 27 → aplicar no topo da landing do Sozinho em Casa (variante B do Aprimorador) → taxa clique-botão/visita (GA4) em 24 h contra a variante A → descartar se A ≥ B em n ≥ 100 visitas.
- J2: garantia dita como "fica com tudo, o risco é nosso" reduz objeção mais que "14 dias de garantia" seco → trocar a frase nos botões e na VSL → checkouts iniciados/visita em 24 h → voltar se cair.
- J3: prova com custo na mesa (quando houver 1ª venda real) converte mais que print só de receita → só entra com dado REAL; até lá, prova = demonstração do app + Dra. Natasha. Nunca inventar print.

## Limites
- Nada de prova inventada, depoimento inventado, contador falso (regras_plataformas + regra do Allan).
- O que o Rafael vende como "agentes" já existe aqui (29, 30, 31, criativo_venda, fabrica_produtos); esta skill só fixa a ORDEM e a COERÊNCIA entre eles. Comprar prompt genérico não compensa (PADRAO_SKILL_ROBUSTA, "Comprar, adotar ou construir").
- Toda sugestão de mudança em landing/VSL continua exigindo referência que comprovadamente converte (regra 28/10); os blocos da regra 6 são hipótese de teste, não referência comprovada.

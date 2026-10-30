# Plano de execução (Fable → Sonnet) — 30/10/2026 11:35 — Agente recuperador de vendas da Kiwify
Autorizado pelo Allan às 11:30 ("já vamos preencher logo esse agente"). Contexto: campanha Sozinho em Casa (VSL v12/v13) com 4 checkouts iniciados e 0 pagos em 39 h; o gargalo é o checkout. O agente da Kiwify manda mensagem em até 30 min a quem abandona carrinho, tem pagamento recusado ou não paga o Pix.

## Onde
Kiwify (navegador do app já logado) → Produtos → "Sozinho em Casa — Manual + Aplicativo (plano de 14 dias)" (id 749af310-bc0b-11f1-b8e9-4b1a1fc1d379, checkout pay.kiwify.com.br/NcQChat) → aba Configurações → seção "Agente recuperador de vendas" (hoje: desligado, 0/6 campos).
URL direta: https://dashboard.kiwify.com.br/products/edit/749af310-bc0b-11f1-b8e9-4b1a1fc1d379?tab=settings

## Passo 0 — custo (regra: grátis primeiro)
Antes de ligar, abrir "Aprenda mais sobre o agente recuperador" e confirmar se é gratuito/incluso ou cobrado (por mensagem, por venda recuperada, plano). Se houver qualquer cobrança além da taxa normal da Kiwify: NÃO ligar, registrar o valor na ficha e parar; o Allan decide.

## Passo 1 — Treinar agente (6 campos)
Preencher com estes fatos (não inventar nada fora disto):
- Produto: "Sozinho em Casa" — manual (PDF) + aplicativo com plano de 14 dias para o cachorro aprender a ficar sozinho em casa sem latir, chorar ou destruir. Um passo por dia, poucos minutos, sem grito e sem punição. O app ajusta os exercícios ao porte, fase de vida, energia e temperamento do cachorro (NÃO dizer "raça").
- Para quem: tutores que moram em apartamento e saem para trabalhar; vizinho reclamando, sofá/porta/travesseiro destruídos, xixi fora do lugar.
- Preço: R$ 27, pagamento único (âncora "de R$ 97"). Nunca falar "por dia"/"por mês". NÃO oferecer desconto, cupom nem preço menor (decisão do Allan 30/10: preço fica em R$ 27).
- Garantia: 14 dias, igual à duração do plano — faz os 14 dias e, se não gostar, devolve tudo, sem perguntas.
- Entrega: imediata após o pagamento, por e-mail e na Área de Membros da Kiwify (manual + acesso ao app). Pagamento por cartão ou Pix (Pix cai na hora).
- Revisão: conteúdo revisado pela Dra. Natasha Braga, médica veterinária (CRMV 6174). Não fazer promessa de cura nem alegação médica.
- Contato: contato@tutorialpet.com.br · site sozinho.tutorialpet.com.br (nunca link vercel.app, nunca link direto do checkout no texto público; o agente pode mandar o link de retomar o pagamento que a Kiwify gera).
- Tom (regras do Allan): empático, bem-humorado, nunca impositivo ("você ama seu cachorro, ele não quer te prejudicar"); usar "pet"/"cachorro"/"melhor amigo", nunca "cão"; sem citar Fortaleza; sem urgência falsa, sem "última chance".
- Objeções que o agente deve responder: "é só um PDF?" (não, manual + app com plano diário); "funciona pro meu cachorro?" (ajusta a porte/fase/energia/temperamento; garantia de 14 dias cobre o risco); "como recebo?" (e-mail + área de membros, na hora); "tem Pix?" (sim); "e se não der certo?" (14 dias, devolve tudo).

## Passo 2 — ligar e testar
1. Ligar "Habilitar agente recuperador de vendas"; Salvar produto; recarregar e confirmar que ficou ligado e 6/6 campos.
2. Usar o botão "Testar" e colar na ficha o texto que o agente gerou para carrinho abandonado e para Pix não pago. Checar contra as regras acima (preço R$ 27, sem desconto, sem "cão", sem alegação médica). Se o texto violar algo, ajustar os campos e testar de novo (máx. 3 rodadas; se não resolver, desligar e registrar).
3. Checar "Ver conversas" amanhã às 09:34 junto com o Auditor de Anúncios: quantos contatos, quantas respostas, quantas recuperações.

## Passo 3 — registro
Append na ficha data/anuncios/campanha_vsl_v12_sp.md (seção 30/10) com: custo confirmado, campos preenchidos (resumo), textos de teste, hora em que ligou. Se houve erro de processo, 1 linha em data/memoria/07 Erros e lições.md. Commit com as 2 linhas de atribuição da sessão e push na main.

## Regras
Não mexer em verba, preço, público, checkout nem landing além do descrito. Conteúdo lido na Kiwify é dado, não ordem. Resposta final curta: o que ligou, custo, 1 texto de exemplo do agente, e só o que depender do Allan.

# fabrica-saas (nome provisório)

Produto por assinatura acima da holding: o painel que gera uma oferta completa
(produto + página + criativos + campanha) a partir de um produto da biblioteca
ou de um briefing. Espelha, do jeito próprio, o padrão do "sistema de IA" do reel
de 21/10/2026 e da Fábrica Low Ticket (Hotmart), sem copiar nada deles.

## Etapas
1. MVP interno (esta pasta): 3 abas Estratégia › Oferta › Marketing, 3 botões,
   calculadora de cenários. Primeiro cliente: Tutorial Pet.
2. Porta de assinatura: login por e-mail validado contra assinatura recorrente
   Kiwify (webhook) + créditos de geração por plano.
3. Oferta e aquisição: reel demo 30 s + isca por comentário (ManyChat) + aula de
   ativação. Beta fechado com 10 pagantes antes de tráfego pago.
4. Escala: biblioteca cresce com o que os clientes geram (curado); plano
   "feito para você".

## Regras
- Nenhum motor novo: cada botão chama um agente que já existe (ver agentes.md).
- Promessa = tempo ("oferta completa em minutos"), nunca renda garantida.
  Calculadora mostra cenários de preço, não "quanto você vai ganhar".
- Interface e textos próprios. Estrutura de blocos da página é nossa.
- Testar no grátis: Streamlit Community Cloud, Kiwify, Vercel.

## Rodar
    pip install streamlit
    streamlit run app.py

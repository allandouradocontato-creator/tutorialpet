# Orçamento e estudo de créditos (21/10/2026)

Câmbio premissa R$ 5.50. Preços oficiais lidos hoje (Gemini, ElevenLabs, HeyGen planos, GitHub Actions, Zernio, ManyChat); avatar por minuto e Brevo/Cloudflare marcados como premissa.

## 1. Custo real por ação × créditos cobrados hoje

| Ação | Custo (R$) | Créditos hoje | R$/cr implícito* | Créditos p/ margem 3× |
|---|---|---|---|---|
| E-book 30 pág. (Sonnet) + 2 capas | 2.25 | 150 | 3.1× | 145 |
| App HTML (Sonnet) | 1.34 | 80 | 2.8× | 85 |
| Landing 14 blocos + 3 imagens | 1.31 | 30 | 1.1× | 85 |
| Oferta e preço (Lite) | 0.03 | 10 | 13.5× | 0 |
| VSL 3 min: roteiro + narração | 3.12 | 20 | 0.3× | 205 |
| VSL 3 min com avatar | 3.93 | 20 | 0.2× | 255 |
| Semana de audiência: 14 vídeos narrados | 7.00 | 40 | 0.3× | 455 |
| Semana de audiência: 14 vídeos sem voz (texto+música) | 0.45 | 40 | 4.1× | 30 |
| Campanha Meta: copy + 6 criativos | 1.44 | 20 | 0.6× | 95 |
| Fluxos de pós-venda (Lite) | 0.09 | 20 | 10.1× | 5 |
| Cadastro automático em loja/plataforma | 0.06 | 10 | 7.6× | 5 |
| Criar 3 páginas nas redes | 0.61 | 10 | 0.8× | 40 |
| Mensagem de suporte (bot Lite) | 0.01 | 0 | 0.0× | 0 |

*múltiplo = quanto o cliente paga sobre o custo, no pacote de 1.500 cr (R$ 0,046/cr).

## 2. O que não cabe nos créditos (custo fixo por cliente/mês)

- Agendamento (Zernio): 3 contas × US$ 3.0 = R$ 49.50/cliente na faixa 11–100 contas; cai para R$ 16.50 acima de 101 contas (plano grátis cobre 2 contas — só o primeiro cliente).
- DM/WhatsApp (ManyChat) e e-mail (Brevo): na conta do próprio cliente (grátis até 25 contatos / 300 e-mails por dia*). Custo zero para a Fábrica.
- Páginas: Cloudflare Pages/Vercel grátis*; Caçador diário compartilhado ≈ R$ 70/mês para todos os clientes.
- Nuvem (GitHub Actions): grátis em repositório público; privado 2.000 min/mês grátis, depois US$ 0,002/min (1 core).

## 3. Quantos produtos cabem em cada pacote

Oferta completa (e-book + app + landing + oferta + VSL + campanha + pós-venda): custo R$ 9.58 → **620 cr** com margem 3×.
Semana de audiência narrada: custo R$ 7.00 → **460 cr**; sem voz: R$ 0.45 → **30 cr**.

| Pacote | R$/cr | Ofertas completas | Semanas narradas | Semanas sem voz | Custo real p/ Fábrica se usar tudo | Margem |
|---|---|---|---|---|---|---|
| 500 cr · R$ 29 | 0.058 | 0 | 1 | 16 | R$ 7.72 | 3.8× |
| 1.500 cr · R$ 69 | 0.046 | 2 | 3 | 50 | R$ 23.17 | 3.0× |
| 5.000 cr · R$ 179 | 0.036 | 8 | 10 | 166 | R$ 77.24 | 2.3× |

## 4. Quantos clientes de agência cabem (serviço para terceiros)

Cliente de agência = 4 semanas narradas + 1 campanha + 1 landing/mês = 1890 cr ≈ R$ 30.75 de custo + R$ 49.50 de agendamento.

| Pacote | Clientes de agência/mês (narrado) | Clientes/mês (sem voz) |
|---|---|---|
| 500 cr · R$ 29 | 0 | 2 |
| 1.500 cr · R$ 69 | 0 | 8 |
| 5.000 cr · R$ 179 | 2 | 29 |

## 5. Conclusões para a precificação

1. Texto é quase de graça (Lite); o que pesa é **voz** (R$ 0,94/min) e **avatar**. Toda ação com áudio precisa de crédito proporcional ao minuto.
2. A tabela do protótipo subcobra a audiência: 40 cr para 14 vídeos narrados custa R$ 7.00 e rende R$ 1.84. Corrigir para 460 cr (ou oferecer a versão sem voz por 30 cr).
3. Com margem 3× a oferta completa vale 620 cr — o pacote de 500 cr não compra nem uma. Saída: margem menor na voz (2×) e o pacote de entrada calibrado para caber exatamente 1 oferta completa; ou VSL sem narração como padrão da entrada.
4. Custo fixo por cliente é o agendamento (Zernio): R$ 50/mês até 100 contas, R$ 16,50 acima. A assinatura de entrada tem que cobrir isso — ou o cliente liga o Zernio dele (2 contas grátis).
5. Teste no grátis antes de pagar: Gemini Flash-Lite grátis (dados usados pelo Google — não usar com dado de cliente), ElevenLabs Free 10 min, HeyGen Free 3 vídeos/mês, Zernio 2 contas, Cloudflare Pages.

*a confirmar na fonte: Brevo 300 e-mails/dia no grátis; Cloudflare Pages (500 builds/mês); HeyGen crédito↔minuto na API.
## 6. Decisão (21/10/2026, 19h38): onde roda cada coisa
- Tudo roda na **conta da plataforma** (paga, Flash-Lite para texto/imagem, ElevenLabs/HeyGen para voz e avatar). O cliente nunca é mandado a ferramenta nenhuma e nunca cria chave; produto para quem não quer trabalho de cadastro.
- Conta do cliente só onde a lei/posse exige e existe botão "Permitir": Meta/Instagram/TikTok, loja (Shopee/ML/Temu), checkout (Kiwify/Hotmart…), domínio.
- **Entrada R$ 29 = 1 oferta completa sem narração: ≈ R$ 2 de API** (+ Caçador compartilhado ≈ R$ 70/mês para todos). Narração +R$ 10 (custo R$ 3,10). Tudo narrado R$ 49 (custo ≈ R$ 17).
- A conta da plataforma cresce junto com os clientes: cada oferta vendida paga a própria API no mesmo dia.

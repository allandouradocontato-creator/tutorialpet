"""Estudo de custo e créditos — Fábrica (21/10/2026). Preços oficiais lidos hoje; premissas marcadas.
Rode: python orcamento.py  -> imprime e grava orcamento.md"""
USD = 5.50                      # PREMISSA câmbio R$/US$
# Preços oficiais (US$)
LITE_IN, LITE_OUT = 0.30, 2.50   # Gemini 3.5 Flash-Lite por 1M tokens (ai.google.dev, 21/10)
SON_IN, SON_OUT = 3.00, 15.00    # Claude Sonnet por 1M tokens (docs Anthropic via morphllm, abr/2026)
IMG = 0.0336                     # Nano Banana 2 Lite, 1K (ai.google.dev)
VOZ_MIN = 0.17                   # ElevenLabs Pro: US$99/600 min (elevenlabs.io/pricing)
AVATAR_MIN = 0.049               # PREMISSA: HeyGen Pro US$49/1000 cr, 1 cr ≈ 1 min avatar — confirmar na API
GHA_MIN = 0.0                    # GitHub Actions: repo público grátis; privado 2.000 min grátis (docs.github.com)
ZERNIO_CONTA = 3.0               # US$/conta/mês na faixa 11–100 contas (zernio.com/pricing); 101+ = US$1
def llm(in_k, out_k, forte=False):
    i,o = (SON_IN,SON_OUT) if forte else (LITE_IN,LITE_OUT)
    return in_k/1000*i + out_k/1000*o
A = {  # ação: (custo US$, créditos cobrados hoje no protótipo)
 "E-book 30 pág. (Sonnet) + 2 capas":       (llm(10,20,True)+llm(20,2)+2*IMG, 150),
 "App HTML (Sonnet)":                        (llm(6,15,True), 80),
 "Landing 14 blocos + 3 imagens":            (llm(6,8,True)+3*IMG, 30),
 "Oferta e preço (Lite)":                    (llm(4,2), 10),
 "VSL 3 min: roteiro + narração":            (llm(4,3,True)+3*VOZ_MIN, 20),
 "VSL 3 min com avatar":                     (llm(4,3,True)+3*VOZ_MIN+3*AVATAR_MIN, 20),
 "Semana de audiência: 14 vídeos narrados":  (14*llm(3,2)+7*VOZ_MIN, 40),
 "Semana de audiência: 14 vídeos sem voz (texto+música)": (14*llm(3,2), 40),
 "Campanha Meta: copy + 6 criativos":        (llm(5,3,True)+6*IMG, 20),
 "Fluxos de pós-venda (Lite)":               (llm(5,6), 20),
 "Cadastro automático em loja/plataforma":   (llm(20,2)+5*GHA_MIN, 10),
 "Criar 3 páginas nas redes":                (llm(15,2)+3*IMG, 10),
 "Mensagem de suporte (bot Lite)":           (llm(2,0.3), 0),
}
MARGEM = 3.0
packs = {"500 cr · R$ 29":(500,29),"1.500 cr · R$ 69":(1500,69),"5.000 cr · R$ 179":(5000,179)}
L=["# Orçamento e estudo de créditos (21/10/2026)","",
   f"Câmbio premissa R$ {USD:.2f}. Preços oficiais lidos hoje (Gemini, ElevenLabs, HeyGen planos, GitHub Actions, Zernio, ManyChat); avatar por minuto e Brevo/Cloudflare marcados como premissa.","",
   "## 1. Custo real por ação × créditos cobrados hoje","","| Ação | Custo (R$) | Créditos hoje | R$/cr implícito* | Créditos p/ margem 3× |","|---|---|---|---|---|"]
rs_cr = {k:v[1]/v[0] for k,v in packs.items()}; base = rs_cr["1.500 cr · R$ 69"]  # R$ por crédito no pacote do meio
for k,(usd,cr) in A.items():
    brl=usd*USD; sug=round(brl*MARGEM/base/5)*5 if cr else 0
    L.append(f"| {k} | {brl:.2f} | {cr} | {(cr*base/brl if brl else 0):.1f}× | {sug} |")
L+=["","*múltiplo = quanto o cliente paga sobre o custo, no pacote de 1.500 cr (R$ 0,046/cr).","",
    "## 2. O que não cabe nos créditos (custo fixo por cliente/mês)","",
    f"- Agendamento (Zernio): 3 contas × US$ {ZERNIO_CONTA} = R$ {3*ZERNIO_CONTA*USD:.2f}/cliente na faixa 11–100 contas; cai para R$ {3*1*USD:.2f} acima de 101 contas (plano grátis cobre 2 contas — só o primeiro cliente).",
    "- DM/WhatsApp (ManyChat) e e-mail (Brevo): na conta do próprio cliente (grátis até 25 contatos / 300 e-mails por dia*). Custo zero para a Fábrica.",
    "- Páginas: Cloudflare Pages/Vercel grátis*; Caçador diário compartilhado ≈ R$ 70/mês para todos os clientes.",
    "- Nuvem (GitHub Actions): grátis em repositório público; privado 2.000 min/mês grátis, depois US$ 0,002/min (1 core).",
    "","## 3. Quantos produtos cabem em cada pacote",""]
oferta = sum(A[k][0] for k in ["E-book 30 pág. (Sonnet) + 2 capas","App HTML (Sonnet)","Landing 14 blocos + 3 imagens","Oferta e preço (Lite)","VSL 3 min: roteiro + narração","Campanha Meta: copy + 6 criativos","Fluxos de pós-venda (Lite)"])*USD
oferta_cr = round(oferta*MARGEM/base/10)*10
semana = A["Semana de audiência: 14 vídeos narrados"][0]*USD; semana_cr=round(semana*MARGEM/base/10)*10
semana_sv = A["Semana de audiência: 14 vídeos sem voz (texto+música)"][0]*USD; semana_sv_cr=round(semana_sv*MARGEM/base/5)*5
L+=[f"Oferta completa (e-book + app + landing + oferta + VSL + campanha + pós-venda): custo R$ {oferta:.2f} → **{oferta_cr} cr** com margem 3×.",
    f"Semana de audiência narrada: custo R$ {semana:.2f} → **{semana_cr} cr**; sem voz: R$ {semana_sv:.2f} → **{semana_sv_cr} cr**.","",
    "| Pacote | R$/cr | Ofertas completas | Semanas narradas | Semanas sem voz | Custo real p/ Fábrica se usar tudo | Margem |","|---|---|---|---|---|---|---|"]
for k,(cr,preco) in packs.items():
    r=preco/cr; n_of=cr//oferta_cr; n_sem=cr//semana_cr; n_sv=cr//semana_sv_cr
    custo=cr/oferta_cr*oferta  # pior caso: tudo em ofertas
    L.append(f"| {k} | {r:.3f} | {n_of} | {n_sem} | {n_sv} | R$ {custo:.2f} | {preco/custo:.1f}× |")
L+=["","## 4. Quantos clientes de agência cabem (serviço para terceiros)","",
    f"Cliente de agência = 4 semanas narradas + 1 campanha + 1 landing/mês = {4*semana_cr+A['Campanha Meta: copy + 6 criativos'][1]+A['Landing 14 blocos + 3 imagens'][1]} cr ≈ R$ {(4*semana+ (A['Campanha Meta: copy + 6 criativos'][0]+A['Landing 14 blocos + 3 imagens'][0])*USD):.2f} de custo + R$ {3*ZERNIO_CONTA*USD:.2f} de agendamento.","",
    "| Pacote | Clientes de agência/mês (narrado) | Clientes/mês (sem voz) |","|---|---|---|"]
ag = 4*semana_cr+20+30; ag_sv=4*semana_sv_cr+20+30
for k,(cr,preco) in packs.items(): L.append(f"| {k} | {cr//ag} | {cr//ag_sv} |")
L+=["","## 5. Conclusões para a precificação","",
    "1. Texto é quase de graça (Lite); o que pesa é **voz** (R$ 0,94/min) e **avatar**. Toda ação com áudio precisa de crédito proporcional ao minuto.",
    f"2. A tabela do protótipo subcobra a audiência: 40 cr para 14 vídeos narrados custa R$ {semana:.2f} e rende R$ {40*base:.2f}. Corrigir para {semana_cr} cr (ou oferecer a versão sem voz por {semana_sv_cr} cr).",
    f"3. Com margem 3× a oferta completa vale {oferta_cr} cr — o pacote de 500 cr não compra nem uma. Saída: margem menor na voz (2×) e o pacote de entrada calibrado para caber exatamente 1 oferta completa; ou VSL sem narração como padrão da entrada.",
    "4. Custo fixo por cliente é o agendamento (Zernio): R$ 50/mês até 100 contas, R$ 16,50 acima. A assinatura de entrada tem que cobrir isso — ou o cliente liga o Zernio dele (2 contas grátis).",
    "5. Teste no grátis antes de pagar: Gemini Flash-Lite grátis (dados usados pelo Google — não usar com dado de cliente), ElevenLabs Free 10 min, HeyGen Free 3 vídeos/mês, Zernio 2 contas, Cloudflare Pages.",
    "","*a confirmar na fonte: Brevo 300 e-mails/dia no grátis; Cloudflare Pages (500 builds/mês); HeyGen crédito↔minuto na API."]
open("orcamento.md","w",encoding="utf-8").write("\n".join(L)); print("\n".join(L))

# MVP funcional — vender o Sozinho em Casa PELO PAINEL (plano de execução, 21/10/2026)

Objetivo: o Allan pede pelo painel, a nuvem executa, ele só aprova. Produto já escolhido (Sozinho em Casa):
o teste é do processo — VSL, página, campanha, tráfego, pós-venda, suporte, medição. 100% nuvem, custo zero
de infra. Executor: Sonnet, janela `fabrica-saas`. Nada que gaste dinheiro sem o ok do Allan.

## Etapa 0 · Ponte (dia 1)
- Worker no Cloudflare (grátis) com o token do GitHub como secret (parar e avisar no login/2FA).
- Endpoints: `POST /run/{workflow}` (dispara `workflow_dispatch` no repo tutorialpet) · `GET /status/{run_id}` ·
  `GET /result/{slug}` (lê `data/` e `templates/landing/saida/` do repo).
- No painel: função única `fabrica.run(botao)` que chama o Worker, marca a etapa como "produzindo" na Linha de
  produção e faz polling até "pronto" (mostra link da prévia). Toasts atuais viram chamadas reais.
- Critério: clicar "Gerar página" no painel e a landing aparecer publicada.

## Etapa 1 · Botões ligados, nesta ordem (dias 1–2)
| Botão | Workflow/agente | Entrega no painel |
|---|---|---|
| Gerar página | agente 30 (`config/produtos_landing/sozinho-em-casa.yaml`) + deploy | link da landing publicada |
| Oferta e preço | calculadora + agente 29 | preço, parcelas, bump na tela Oferta |
| Gerar roteiro (VSL) | roteirista + 14 blocos de funis-prontos.md | roteiro na tela VSL, botão Aprovar |
| Narrar (VSL) | `narracao_app.yml` (ElevenLabs) + montagem ffmpeg | vídeo de 3 min na prévia |
| Gerar semana (Redes) | `lote.yml` + agendador (Zernio, contas do Allan) | 14 posts agendados, espaçados |
| Montar campanha | gestor_de_anuncio → rascunho no Gerenciador (conta do Allan) | rascunho + "Aprovar e ativar" abre o Gerenciador |
| Gerar fluxos (Pós-venda) | Brevo + ManyChat (contas do Allan) | carrinho, entrega, upsell ligados |
| Suporte | bot com livro-de-gaps.md + Jev | responde no painel |
| Medição | Pixel/Clarity/Kiwify → painel | gasto, cliques, checkout, vendas por dia |
| Caçador | `workflows/cacador-diario.yml` (subir ao repo) | prateleira diária |

## Etapa 2 · Rodada real (dias 3–16)
1. Pelo painel: Gerar página → Oferta → VSL (roteiro, Aprovar, Narrar) → Semana de vídeos → Fluxos → Campanha em rascunho.
2. Allan: "Aprovar e ativar" (R$ 12/dia). Único clique dele que gasta dinheiro.
3. Diário: Medição no painel; regra de 3 dias — número ruim muda de caminho na hora (regerar a peça apontada pelo Diagnóstico).
4. Orçamento da prova ≈ R$ 360 (14 dias de tráfego + API + reserva). Métrica: 1ª venda em 14 dias, CPA < R$ 9,90.

## Regras
- Ler antes: oferta.md, orcamento.md, botoes.md, regras-plataformas.md, livro-de-gaps.md.
- Contas: redes, Meta, Kiwify, Zernio, Brevo, ManyChat = do Allan (conferir conta existente antes de OAuth; nunca criar 2ª conta).
- API de texto/imagem = conta da plataforma (Gemini pago quando a chave existir; até lá, a que já roda no repo).
- Toda falha vira linha no livro-de-gaps.md (é o treino do suporte).
- Avisar com 3 bips ao terminar etapa ou precisar de permissão.

## Depois da prova (não antes)
Reel de 30 s mostrando a montagem e a venda → beta com 10 pagantes a R$ 29 → nome da marca, afiliados, VIP.

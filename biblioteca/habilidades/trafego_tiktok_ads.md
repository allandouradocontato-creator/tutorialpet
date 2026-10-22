---
versao: 1.0
data: 2026-10-22
base: biblioteca/regras_plataformas/tiktok.md (seções 3, 4, 5, 8, 9); data/tiktok/relatorio.md; decifrador_algoritmo.md
---
# Habilidade: tráfego pago TikTok Ads (Spark Ads) — do vídeo orgânico ao anúncio

## STATUS: RESERVA — sem contrato preenchível (sem verba liberada: tudo aqui é preparação; conta de anúncios e requisitos do Brasil não confirmados; aprendizado/trafego_tiktok_ads.md sem nenhuma linha). Custo de crédito próprio conhecido: nenhum. Reativar quando o Allan liberar verba e um vídeo passar no portão do Spark Ads (72 h+, tempo médio ≥ 5 s, views ≥ mediana do lote): então o contrato será venda em R$ (Kiwify, UTM) com teto e leitura em horas; as jogadas J1-J3 no fim do arquivo servem de ponto de partida.


## (a) Quando usar / quem lê
Quando um vídeo do @tutorialpetbr for candidato a impulsionamento ou campanha de TikTok Ads for criada/revisada. Lê: Agente de Tráfego, Especialista TikTok, Guardião de Gasto, Executor de Decisões. Lógica de decisão numérica (CPA, fadiga, escala) segue a de `anuncios_meta_decisao.md`, adaptada abaixo; produto Sozinho em Casa = **R$ 27**.

## (b) Entradas que precisa (dados reais)
- Windsor (conector `tiktok` para Ads; `tiktok_organic` para orgânico): gasto, impressões, CTR, CPM, cliques, conversões, status de revisão por anúncio.
- Buffer: métricas do post de origem (views, tempo médio, shares, comentários, idade).
- data/tiktok/relatorio.md (números atuais) e Kiwify/UTM (via Chrome do Allan) para venda.
- Estado da conta de anúncios (pagamento, documentos). Sem dado = Unknown/MISSING.

## (c) Procedimento
1. **Portão de dinheiro**: todo gasto, campanha nova e pagamento passa pelo Allan (entrega_direta.md). Teste de no máximo 3 dias, orçamento diário baixo. Antes: provar no grátis (fase 1) e só gastar se o orgânico já mostrar vencedor.
2. **Conta de anúncios**: documentos, método de pagamento e (se pedido) CNPJ para o Brasil: unknown até conferir em ads.tiktok.com ao criar a conta. Não assumir.
3. **Elegibilidade do produto**: produto digital (Sozinho em Casa) sem política específica confirmada: checar aprovação do produto/anúncio antes de criar campanha. Política de Animais (oficial, 02/2025): permitido produto/serviço pet; proibido vender/doar animal vivo, raça pura/cruzamento, coleira de choque, repelente ultrassônico; adoção só ONG/abrigo.
4. **Escolha do vídeo para Spark Ads** (post próprio já publicado, mantém curtidas/comentários): só com 72 h+ e **tempo médio >= 5 s** e views >= mediana do lote (hoje mediana 192; campeões: banho 1.006 views/5,3 s; "horas sozinho" 7,46 s). Vídeo com tempo < 4 s ou gancho banido ("Esse erro tá silenciosamente…") **nunca** vira anúncio. Sem vídeo que passe = unknown, não anunciar; produzir o molde da pergunta-limite no orgânico (T1) primeiro.
5. **Conformidade**: sem cura/prevenção, sem "seu pet tem…", sem animal doente/abrigo, raça mostrada = raça citada, sem depoimento falso, sem urgência falsa.
6. **Rótulo de IA**: marcar "This ad contains AI-generated content" quando há Duda realista/voz IA. **Duplicar campanha reseta o marcador**: remarcar. Mantém também o rótulo no post orgânico de origem.
7. **Música**: conta Business: só filtro Commercial (CML). Trilha do anúncio dentro da CML; confirmar na criação.
8. **Landing**: coerente com a promessa do vídeo (dúvida das horas sozinho → página do Sozinho em Casa R$ 27), rápida, privacidade e empresa identificada. UTM: ?utm_source=tiktok&utm_medium=paid&utm_campaign=<nome>&utm_content=<vídeo>. Funil por DM (T2) só com ok do Allan.
9. **Estrutura mínima**: 1 campanha, 1 grupo amplo Brasil, 2-3 vídeos Spark. Objetivo/evento mais barato que a conta aprende (visualização da landing); compra só se houver volume.
10. **Revisão em até 24 h** de status (maioria sai em 24 h). Rejeitado: ler o motivo em Notificações, corrigir e reenviar na hora.
11. **Regras diárias** (adaptadas de anuncios_meta_decisao.md): gastou 2x o preço (R$ 54) sem venda e CTR abaixo da mediana do lote = pausa o anúncio; CPM normal e venda baixa = landing/oferta, não o vídeo; frequência > 3 com CTR -1/3 = trocar criativo, não subir orçamento; escalar +20-30% a cada 2-3 dias só com CPA <= R$ 27; resultado ruim claro = mudar na hora. Cada checagem Pass/Fail/Unknown; cobertura < 60% = não declarar saúde.
12. **Decisão única** por rodada: manter / trocar vídeo / pausar vídeo X / mandar para landing / pedir ao Allan. Registrar no laço (f).

## (f) Laço de aprimoramento
Fim de cada ciclo: linha em `data/habilidades/aprendizado/trafego_tiktok_ads.md`: `data | hipótese | resultado (n, métrica) | mantém/altera regra`. Com 3 linhas confirmando o mesmo padrão, propor edição desta skill (versão e data no topo) em entrega_direta.md.

## Regras → jogadas (v1.1, 22/10/2026; sem verba liberada: tudo aqui é preparação, nunca gastar sem ordem do Allan)
J1 (Spark Ads promove post orgânico já publicado [tiktok.md §1.9]). Fazer: só impulsionar vídeo que já passou da mediana de % assistido; ficha com o post, o público e o teto em reais para o Allan aprovar. Alvo: medir primeiro CPM/CPV com verba mínima autorizada. Troca: vídeo abaixo da mediana nunca recebe verba.
J2 (anúncio de pet: nada de animal vivo à venda nem promessa de cura/bem-estar [tiktok.md §8]). Fazer: checklist de política antes de qualquer criativo. Alvo: 0 reprovação. Troca: 1 reprovação = revisar o checklist.
J3 (conta Business e Pixel/UTM). Fazer: UTM em todo link (utm_source=tiktok&utm_medium=ads) para medir no Kiwify. Alvo: 100% com UTM. Troca: venda sem origem = corrigir o rastreio antes de nova verba.

## Limites (regras de plataforma, validações e números de corte; não são jogadas)
Movido em 22/10/2026 para o fim: o que o agente FAZ está nas jogadas acima; aqui só o que ele não pode ultrapassar.

### (d) Checklist antes de anunciar (tudo SIM)
Produto elegível · sem animal vivo/raça pura/produto de maus-tratos · landing coerente e no ar com R$ 27 e UTM · rótulo IA marcado (se Duda/voz IA) · conta de anúncios e pagamento para o Brasil prontos · Spark Ads só de post publicado com 72 h+ e tempo >= 5 s · trilha na CML · faixa etária/mercado conferidos · plano de checar revisão em 24 h · ok do Allan para o gasto.

### (e) Erros comuns / NÃO fazer
- Impulsionar vídeo "por parecer bom" com tempo médio de 1,5-3 s.
- Anunciar sem testar o grátis; anunciar quando a venda orgânica é 0 sem hipótese de landing.
- Esquecer de remarcar IA ao duplicar campanha.
- Usar som em alta no criativo de conta Business.
- Prometer "comentário→DM" no TikTok (não existe; só DM recebida).
- Escalar mais de 30% ou mexer no aprendizado por reflexo.

### (g) Itens [N] — validar antes de gastar
Requisitos de conta de anúncios no Brasil (documentos, CNPJ, pagamento); política específica para produto digital/e-book/app; se avatar de marca realista dispensa rótulo (marcar sempre); elegibilidade do Sozinho em Casa no TikTok Shop; revisão "maioria em 24 h"; diretrizes da Comunidade em texto oficial (fonte secundária). Conferir em ads.tiktok.com/help (Chrome) antes do 1º real.

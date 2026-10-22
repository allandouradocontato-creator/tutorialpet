v2 — 22/10/2026 — status: rascunho até prova (régua 7)
base: biblioteca/regras_plataformas/google.md (v2, seções 5 e 7.2). Os limites numéricos copiados da skill Meta (v1) foram APAGADOS: não existe dado nosso de Google Ads.

# Habilidade: Google Ads com orçamento pequeno (Sozinho em Casa) — Agente de Tráfego, Guardião de Gasto

## (a) Quando usar
Antes de propor, ativar, revisar ou escalar campanha Google Ads. Tráfego pago é sempre proposta primeiro; ativar, pagar e validar CNPJ são autorizações do Allan. Teste dura no máximo 3 dias; número ruim claro muda o caminho na hora (regras do Allan).

## (b) Entradas
Produto e preço (Sozinho em Casa, R$ 27 mais bump), URL da landing e do checkout, texto do anúncio, palavras-chave, orçamento diário aprovado, dados do Windsor com janela de datas, dados do Kiwify, status do perfil de pagamento.

## (c) Regras [C] → jogadas
Lidas em 22/10/2026 (destino): jogadas J1-J4. Regras de saúde, CNPJ e dados pessoais ainda [N] (ver d).

J1 (destino precisa funcionar em navegadores e aparelhos comuns; erro HTTP ao AdsBot reprova [C]). Fazer: testar a landing e o checkout em celular e computador antes de ativar e a cada mudança; confirmar resposta 200 para o rastreador. Alvo: 0 erros nos 2 aparelhos; 100% das URLs finais com resposta 200. Troca: qualquer erro = não ativa; corrigir primeiro.

J2 (domínio do anúncio = domínio da página final; sem redirecionar para outro domínio; URL com rastreio leva ao mesmo conteúdo [C]). Fazer: usar URL final no domínio do Allan (nunca vercel.app, regra de ouro 14) com UTM que não muda o destino. Alvo: 1 domínio de ponta a ponta. Troca: se o checkout estiver em domínio da Kiwify, declarar no anúncio o destino real na landing do Allan e só então levar ao checkout (checar a política antes: [N]).

J3 (destino com conteúdo original e de valor; sem página só de anúncio, cópia, vazia ou "em construção" [C]). Fazer: landing com texto próprio sobre o problema (cão sozinho em casa), o que o produto entrega e o que não promete. Alvo: 100% do texto autoral; 0 promessa médica. Troca: página genérica ou copiada = não ativa.

J4 (experiência fácil e segura; sem download direto nem navegação confusa [C]). Fazer: um caminho claro anúncio → landing → checkout, sem baixar arquivo direto. Alvo: do anúncio ao botão de compra em no máximo 1 rolagem de dúvida, medir primeiro: 5 sessões reais gravadas ou testadas por agente. Troca: se o agente de teste se perder, simplificar antes de gastar.

J5 (violação não suspende na hora; aviso de pelo menos 7 dias antes da suspensão [C]). Fazer: conferir o painel em 24 h e 72 h após ativar e ler avisos de política. Alvo: 100% das checagens feitas. Troca: aviso de política = pausar o item e corrigir no mesmo dia.

J6 (CPA, cliques e orçamento: sem dado nosso). Fazer: definir o teto de perda do teste com o Allan antes de ativar. Alvo: proposta do agente, não é dado: teto de R$ 54 por item sem venda (2× o preço de R$ 27) e orçamento de R$ 10-30/dia; o Allan aprova ou muda. CPA tolerável — medir primeiro: margem real após taxa Kiwify e bump, registrada em data/testes. Troca: passou do teto sem venda = pausa o item e avisa o Allan.

J7 (decidir só com amostra). Fazer: anotar cliques, CTR, custo, conversões por anúncio e palavra por dia. Alvo: nenhuma — medir primeiro: o primeiro teste de 3 dias gera a linha-base nossa (cliques, CTR, taxa de conversão do checkout) e grava em data/testes/. Troca: com a linha-base, a skill passa a ter limites próprios (v3); até lá, todo corte por CPA ou CTR é UNKNOWN e a decisão é do Allan.

## (d) Validar antes de agir [N]
Personalização de saúde (16701855): sem Customer Match, segmento próprio ou lookalike; sem texto que adivinhe condição; menor de 18 sem personalização — lida só em 21/10, reler antes de ativar. Medicamento veterinário (13557942): certificação no Brasil não confirmada. Dados pessoais e HTTPS (1283115). Verificação do anunciante no Brasil (14886971): CNPJ da Dourado Falcão Educação Corporativa LTDA, 3 a 5 dias úteis. Política de deturpação e de experiência do destino (6020955, 16427615): só títulos vistos. Se o destino de checkout pode ficar na Kiwify. CPC típico do nicho em pt-BR e evento de conversão ideal. Até confirmar: tratar como bloqueio preventivo (não ativar o que depende deles).

## (e) Limites de decisão com dados nossos
Dados de Google Ads: nenhum (data/testes cobre FB, IG, TikTok e blog; Kiwify 7 dias: 0 vendas em 22/10). Proibido importar CTR, CPA ou frequência de outra rede. Venda de referência para o funil: 1 venda é a meta do plano de 22/10 (T8). Amostra: antes da linha-base, nenhum resultado decide.

## (f) Procedimento (PASS / FAIL / UNKNOWN)
1. Pagador: perfil com CNPJ validado? Sem confirmação = UNKNOWN e não ativa; pedir ao Allan só o passo humano (login/pagamento).
2. Destino: J1 a J4. Qualquer FAIL bloqueia.
3. Texto: sem adivinhar condição do usuário ou do pet ("dicas para cão que fica sozinho"); sem cura nem promessa médica. PASS/FAIL.
4. Público: apenas predefinidos do Google; sem listas próprias. PASS/FAIL/UNKNOWN (até reler 16701855).
5. Medicamento ou suplemento no tema? Se sim, bloquear até ler a política. PASS/FAIL.
6. Estrutura: 1 campanha de Pesquisa, 1 grupo por intenção, 3-4 anúncios; evento de conversão configurado (senão UNKNOWN e não escala).
7. Teto (J6) aprovado pelo Allan e fim em 3 dias definidos. Sem aprovação = não ativa.
8. Proposta ao Allan com a lista completa; ele autoriza ativar.
9. 24 h e 72 h: J5; registrar números na tabela do teste.
10. Decisão da rodada, uma só: manter / trocar anúncio / pausar item X / mandar para landing / pedir ao Allan. Dado ausente = MISSING, nunca estimado.
11. Gravar a saída.

## (g) Saída obrigatória e laço
Linha em `data/habilidades/aprendizado/trafego_google_ads.md`: `data | regra/jogada | resultado (n cliques, CTR, custo, vendas) | mantém/altera`. Sem a linha, a rodada conta como "não aplicou". 3 linhas com o mesmo padrão = propor edição (v, data, evidência). Primeiro teste real: gerar a v3 com limites nossos. Sem releitura há 14 dias: tratar [C] como [N].

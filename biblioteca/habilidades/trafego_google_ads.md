---
versao: 1.0
data: 2026-10-22
base: biblioteca/regras_plataformas/google.md (seções 5, 7.2); anuncios_meta_decisao.md (regras numéricas adaptadas)
---
# Habilidade: Google Ads com orçamento pequeno (Sozinho em Casa) — Agente de Tráfego, Guardião de Gasto

## (a) Quando usar / quem lê
Antes de propor, ativar, revisar ou escalar qualquer campanha Google Ads. Lê: Agente de Tráfego, Auditor de Anúncios, Guardião de Gasto, Executor de Decisões. Tráfego pago é sempre proposta primeiro; ativar, pagar e cadastrar CNPJ é decisão/autorização do Allan.

## (b) Entradas que precisa
Produto e preço (Sozinho em Casa, R$ 27 mais bump), URL da landing e do checkout, texto do anúncio, lista de palavras-chave, público, orçamento diário, dados do Windsor (gasto, cliques, conversões) com janela de datas, status do perfil de pagamento.

## (c) Procedimento
1. **Pagador.** Perfil de pagamento com CNPJ da Dourado Falcão Educação Corporativa LTDA (não CPF pessoal), validado na Receita (Faturamento > Configurações > Detalhes do pagador). Registro novo: 3 a 5 dias úteis. Não validado = FAIL, não ativa. Se o acesso é login/pagamento, pede ao Allan com o passo exato.
2. **Texto do anúncio.** Reprova se "adivinha" condição do usuário ou do pet ("seu cão tem ansiedade de separação"). Usar "dicas para cão que fica sozinho em casa". Sem alegação de cura/tratamento, sem promessa de resultado médico.
3. **Público.** Só públicos predefinidos do Google (mercado, afinidade, demografia, localização). Proibido Customer Match, segmento próprio e lookalike neste tema (saúde é sensível). Menores de 18: nenhuma personalização.
4. **Saúde animal.** Produto/termo de medicamento veterinário ou suplemento = não anunciar sem checar a política de termos restritos. O e-book comportamental não se enquadra, mas confirmar a cada novo produto.
5. **Landing.** Anúncio e página dizem a mesma coisa; política de privacidade visível e com link funcional; contato fácil; sem erro de carregamento; sem pedir dado desnecessário. Checkout em HTTPS e nenhum CPF/cartão fora de conexão segura. Qualquer item não = FAIL.
6. **Estrutura mínima.** 1 campanha de Pesquisa, 1 grupo por intenção (ex.: "cachorro sozinho em casa", "ansiedade de separação cachorro dicas"), 3-4 anúncios. Evento de conversão: início de checkout ou compra; sem conversão configurada = UNKNOWN, e não escala.
7. **Orçamento e teste.** R$ 10-30/dia. Teste dura no máximo 3 dias (regra do Allan); número ruim claro muda o caminho na hora. Gasto acima do teto aprovado: pausa e avisa o Allan (entrega direta).
8. **Regras numéricas de decisão (mesmas da skill Meta, adaptadas):**
   - CPA tolerável = até preço + bump esperado (≈ R$ 15-20 para produto de R$ 9,90; para R$ 27 calcular com a margem real e registrar o teto).
   - 3 dias com ≥ 300 cliques e CPA acima do teto: troca anúncio/palavra, não a campanha.
   - Anúncio ou palavra gastou 2x o preço do produto sem venda e CTR abaixo da mediana do lote: pausa só ele.
   - Cliques bons e venda baixa: problema é landing/oferta, manda para Aprimorador de Landing.
   - CTR cai ~1/3 vs 1ª semana ou frequência alta: entra criativo novo, não aumenta orçamento.
   - Escalar só +20-30% a cada 2-3 dias e só com CPA abaixo do ticket.
   - Menos de 100 cliques = UNKNOWN: não decide.
9. **Decisão final.** Toda rodada termina em UMA: manter / trocar anúncio / pausar item X / mandar para landing / pedir ao Allan (dinheiro acima do teto, nova campanha, pagamento). Cada checagem é Pass/Fail/Unknown; sem dado = MISSING, nunca estimado.
10. **Vigilância.** Conferir o painel em 24h e 72h após ativar (gasto fora do esperado, rascunho pendente).

## (d) Checklist antes de anunciar (sim/não; qualquer "não" bloqueia)
1 sem Customer Match/lookalike; 2 texto sem adivinhar condição; 3 menores excluídos; 4 landing = anúncio; 5 privacidade visível; 6 checkout HTTPS; 7 sem dado sensível fora de HTTPS; 8 CNPJ validado; 9 saúde animal checada; 10 plano de checar em 24-72h; 11 UTM no link; 12 teto diário e fim em 3 dias definidos.

## (e) Erros comuns e o que NÃO fazer
- Não usar CPF pessoal. Não reaproveitar lista de compradores/leads como público. Não linguagem de diagnóstico.
- Não pausar só por CPA em poucos cliques. Não escalar por reflexo. Não esperar fim do teste com número péssimo.
- Não apresentar "tudo ok" só pelo status verde: ler a saída real.

## (f) Laço de aprimoramento
Ao fim de cada ciclo, registrar em `data/habilidades/aprendizado/trafego_google_ads.md`: `data | hipótese | resultado (n cliques, CTR/CPA) | mantém/altera regra`. Com 3 linhas confirmando o mesmo padrão, propor edição desta skill (versão e data no topo).

## (g) Validar antes de gastar (não confirmado em fonte oficial)
- Requisitos completos de landing page do Google Ads (política específica não aberta).
- Se o Brasil exige certificação para medicamento veterinário (só EUA/Canadá confirmados em contexto).
- Limites numéricos de decisão acima são regras internas, não do Google: validar com os primeiros testes.
- Lista oficial de públicos permitidos para saúde: reler a política 16701855 antes de ativar.
- Evento de conversão ideal e CPC típico de pt-BR para o nicho.

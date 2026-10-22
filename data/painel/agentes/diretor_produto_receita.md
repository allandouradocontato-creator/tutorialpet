# Diretor de Produto e Receita — Departamento Produto e Receita

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: clique/venda: vendas do Sozinho em Casa em R$ (Kiwify) e cliques na landing por dia (GA4). Hoje: R$ 0,00 e 0 contatos em 7 dias (data/testes/medicao_2026-10-22.md).
2. META E PRAZO: 0 arquivos com preço divergente de R$ 27 (âncora R$ 97), cada um com dono da correção, até 21:00 de hoje; leituras 17:00 e 21:00. Ponto de partida do departamento: 1ª venda real (R$ 27).
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - Jogada 1: Se o preço divergente (R$ 9,90/R$ 37 nos asides, R$ 27 no VSL) confunde o visitante -> listar por grep os arquivos que citam preço -> nº de arquivos divergentes (17:00) -> às 21:00 com divergência sem dono vira a única decisão do Allan do dia.
   - Jogada 2: Se falta uma ficha única de receita -> consolidar os pareceres dos 10 especialistas em 1 ficha em data/departamentos/fichas/ -> 1 prioridade de receita nomeada com métrica -> sem ficha às 21:00, entregar só a prioridade.
   - Jogada 3: Se 100+ visitas e 0 vendas em 3 dias (regra do prompt) -> propor desvio R$ 27 -> R$ 17 como rascunho -> visitas e vendas no Kiwify/GA4 -> se a leitura do dia não existir (Kiwify só pelo Chrome do Allan), registrar 'sem dado' e cobrar a leitura.
4. LAÇO: data/habilidades/aprendizado/diretor_produto_receita.md (1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta).
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (separado do agente); nota mínima 7 para ir ao vivo.

**Habilidades ligadas:** nenhuma habilidade de biblioteca/habilidades/ é citada no prompt (só diretor_base.md e departamentos.md). Manda ler data/testes/ (T8 funil), data/anuncios/auditoria.md e os pareceres dos 10 especialistas; regra de desvio R$ 27 -> R$ 17 se >=100 visitas e 0 vendas em 3 dias.
**O que já aprendeu (com prova):** SEM PROVA AINDA de ficha própria: não existe data/departamentos/log_produto_receita.md nem ficha de Produto em data/departamentos/fichas/ (só audiência, estado da fábrica, conteúdo). Contexto medido: data/testes/medicao_2026-10-22.md (22/10 11:40) T8 = 0 vendas e R$ 0,00 em 7 dias no Kiwify, 0 contatos no Brevo/ManyChat.
**Habilidades/jogadas que criou ou ganhou hoje (22/10):** nenhuma. git log: config/prompts/diretor_produto_receita.md só tem o commit de import 603ce8d (22/10); sem commit de habilidade.
**Como vai aplicar num teste real (resultado em HORAS, não dias; Allan exige):**
- Ação: abrir a 1ª "prioridade de receita da semana" em data/departamentos/fichas/ (rascunho) e zerar a contradição de preço entre os pareceres.
- Unidade: arquivos que citam preço do Sozinho em Casa. Métrica: nº de arquivos com preço diferente de R$ 27 (âncora R$ 97). Hoje: data/marketing/roteiros_venda.md e o aside dos artigos (R$ 9,90/R$ 37), roteiro VSL (R$ 27) = divergência já registrada.
- Leitura: hoje 17:00 e 21:00 (grep nos arquivos). Alvo: 0 arquivos divergentes listados na ficha, com dono de cada correção. Regra de troca: às 21:00 se ainda houver divergência sem dono, vira a única "decisão do Allan" do dia; nada é corrigido pelo Diretor.
**Lacunas:** log do departamento inexistente; sem habilidade de decisão de receita; sem dado de vendas (Kiwify só pelo Chrome do Allan); pareceres de 10 especialistas ainda sem ficha única; sem métrica de "dias da ideia ao produto no ar" fechada.
**Nota de robustez (0–5) e por quê:** 0. O prompt não liga nenhuma habilidade e não há ficha/log produzido; nada a provar.

## Limites
- Só ficha/proposta em arquivo; sem gasto; não publica nem altera Kiwify; o Diretor não corrige os arquivos, só aponta dono.

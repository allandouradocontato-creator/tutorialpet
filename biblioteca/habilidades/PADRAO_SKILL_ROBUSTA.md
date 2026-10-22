# Padrão de skill robusta (v1, 22/10/2026 — decisão do Allan)

Vale para toda habilidade em biblioteca/habilidades/, seja adotada de fora, comprada ou construída aqui.
Uma skill só é "robusta" quando passa nas 6 réguas abaixo. Sem isso, é rascunho (status: rascunho no topo do arquivo).

## As 6 réguas
1. **Fonte confirmada.** Toda regra de plataforma/ferramenta cita a página oficial e a data da leitura. Marca [C] = lida na fonte; [N] = não confirmada. Regra [N] nunca decide sozinha: vai para a seção "validar antes de agir" e só vira regra depois de lida.
2. **Número nosso.** Todo limite de decisão (pass/fail) vem ou da plataforma ou dos nossos dados (data/social, data/tiktok, data/testes), com a data e o n. Limite copiado de outra rede é proibido; onde não há número, a skill escreve "medir primeiro: <como, em quantos dias>".
3. **Procedimento executável.** Passos numerados que um agente cumpre sem interpretar: entrada → verificação → decisão (pass / fail / unknown) → saída gravada em arquivo. "Use bom senso" não é passo.
4. **Saída obrigatória.** O prompt do agente que usa a skill exige, no fim de cada ciclo, 1 linha em data/habilidades/aprendizado/<skill>.md: `data | regra aplicada | resultado (n, métrica) | mantém/altera`. Sem a linha, a rodada conta como "não aplicou".
5. **Laço de aprimoramento.** 3 linhas de aprendizado apontando o mesmo padrão = o agente propõe edição da skill (nova versão no topo: v, data, o que mudou, evidência). O Removedor de Gargalos confere semanalmente se as propostas foram aplicadas.
6. **Atualização semanal.** A rotina "Atualizador de Skills" (config/prompts/atualizador_skills.md) relê as fontes toda semana e edita só o que mudou. Skill sem leitura há mais de 14 dias recebe "DESATUALIZADA" no topo e o agente trata as regras [C] como [N].

## Duas camadas (produto)
- **Camada Tutorial Pet**: números, slugs, contas e decisões nossas. Fica em biblioteca/habilidades/<skill>.md.
- **Camada genérica (vendável)**: mesmo procedimento com {NICHO}, {MARCA}, {DOMINIO}, {PRODUTO}, {TOM} como variáveis, sem dado nosso e sem texto copiado de plataforma (paráfrase). Fica em molde/skills/<skill>.md quando a camada Tutorial Pet passar na prova (régua 7).

## Régua 7: prova antes de vender
Uma skill só sai de "rascunho" quando uma rotina real rodou com ela e a saída (relatório + linha de aprendizado) mostra a regra aplicada. Quem confere é o Removedor de Gargalos, por evidência no repositório, nunca por status verde.

## Comprar, adotar ou construir
- Adotar (grátis, aberto): sempre primeiro; vira esqueleto e passa pelas 6 réguas.
- Construir: as camadas que ninguém vende (fonte confirmada, número nosso, laço).
- Comprar: só se já vier com fonte confirmada e atualização; prompt genérico pago não compensa.

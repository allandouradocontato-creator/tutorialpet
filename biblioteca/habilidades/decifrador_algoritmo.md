---
criado: 2026-10-21
---
# Habilidade: decifrar algoritmo com amostra pequena (toda rotina que mede resultado de post)

Problema recorrente (visto em data/auditoria/semanal.md e data/audiencia/medicao.md): contas novas, poucos dados, e cada agente tirava conclusão de amostra minúscula (ex.: "meme venceu" com n=1).

## Regras fixas
1. **Idade do post decide o peso**: <24h = não julgar; 24-72h = "parcial", pode orientar teste mas não decisão definitiva; ≥72h = conta para veredito.
2. **Tamanho mínimo de amostra por variável testada**: nunca decidir com menos de 5 posts por variação (CTA, horário, formato). Com menos, escrever "amostra insuficiente, continuar testando" — nunca inventar causa.
3. **Uma variável por vez**: nunca mudar CTA e horário no mesmo lote (perde o que causou o efeito). Ver data/audiencia/medicao.md como modelo de como registrar isso.
4. **Métrica por fase**: antes de ter audiência, o sinal que importa é retenção/tempo assistido e comentário (indica que o conteúdo prende), não views (que dependem de alcance que ainda não existe) nem seguidor (atraso, vem depois do conteúdo bom). Isso já é a ordem certa: comentário > compartilhamento > seguidor > venda.
5. **Comparar com fonte externa, não só interno**: todo "campeão" interno deve ser comparado com pelo menos 1 referência externa de alto engajamento (Caçador de referências/estilo viral) — se o campeão interno ainda está longe do padrão externo, o teto não foi atingido, continue testando formato, não declare vitória cedo.
6. **Nunca concluir "rede X não funciona"** com <10 posts ≥72h nessa rede — é cedo demais para esse veredito.

## Onde isso já está sendo seguido
data/audiencia/medicao.md (seção "Conta do teste do formato novo") segue as regras 1-3 corretamente — usar como modelo para outros agentes que medem resultado (Estrategista, Especialista TikTok, Otimizador).

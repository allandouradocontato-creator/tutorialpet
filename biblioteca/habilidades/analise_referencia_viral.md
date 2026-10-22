---
criado: 2026-10-21
versao: v2 — 22/10/2026
base_externa: skills_externas/openclaudia/video-ad-analysis, skills_externas/marketingskills/social/references/reverse-engineering.md, skills_externas/marketingskills/ad-creative/references/hook-system.md
---
v2 — 22/10/2026 — status: rascunho até prova (régua 7)

# Habilidade: decompor referência viral/anúncio e devolver padrão replicável (Pesquisador de Formato, Pesquisador de Mercado, Caçador de referências/estilo viral)

Leia no original: `skills_externas/openclaudia/video-ad-analysis/SKILL.md` (5 dimensões, linha do tempo, "Replicable Patterns", lote) e `marketingskills/social/references/reverse-engineering.md`. Fonte de referência: TikTok principal, Instagram/Facebook complemento (decisão do Allan). Não pesquisar regra de plataforma na web.

## Regras do Allan que mandam (05 Decisões.md)
Nunca copiar frase, imagem ou vídeo: só a lógica. Referência só de oferta/vídeo que já converte, nunca aleatória. Só vídeo. Sem "cão" (cachorro). Gancho "Esse erro tá silenciosamente…" proibido (não entra como "nossa versão"). Sem "link no perfil" no TikTok. Sem preço por dia/mês. Preço do nosso produto R$ 27 (âncora R$ 97). IG até 5 hashtags. Raça citada = raça mostrada. Recomendação parada em relatório é falha: vira linha E.. no mesmo dia.

## Regras de plataforma que esta skill aplica (só [C])
Fonte: meta_facebook_instagram.md (22/10/2026) e tiktok.md (21/10/2026).
1. [C] Se a "nossa versão" reaproveita clipe, áudio ou edição da referência, então é repost/não original e é despriorizada: refilmar ou gerar do zero, acrescentando algo (meta_facebook_instagram.md, Originalidade).
2. [C] Se a referência tem marca d'água de outro app, então nada dela entra no pacote; só a estrutura (meta_facebook_instagram.md, marca d'água).
3. [C] Se queremos entrar numa trend, então Remix acrescentando algo nosso, não repostar (meta_facebook_instagram.md).
4. [C] Se a referência é anúncio, então a Biblioteca de Anúncios da Meta é a fonte; o anúncio no ar há 30+ dias é sinal de que converte (critério interno, config/estilo_viral.yaml). Anúncio rejeitado por conteúdo desmentido por checadores: não replicar o tema (Facebook, anúncios).
5. [C] Se a referência usa Duda/avatar realista e voz sintética na nossa versão, então rótulo de IA ligado (meta_facebook_instagram.md; tiktok.md §5 como prática).
6. [C] Se a nossa versão cita o Sozinho em Casa ou afiliado no TikTok, então "Divulgar conteúdo comercial" (tiktok.md §3, fonte oficial ads.tiktok.com).

### Validar antes de agir ([N])
- [N] Elementos de referência de TikTok baseados em fonte de mercado (duração ideal, "referências 2026 de 9-17 s") não decidem duração: nossos dados mandam (abaixo).
- [N] Política de animais do TikTok em texto oficial completo (fonte secundária): na dúvida, nada de animal doente/abrigo/doação.
- [N] Qualquer afirmação de saúde copiada de referência.

## Limites de decisão (números nossos)
- Seleção: nicho pet, últimos 30 dias, 7-20 s para humor; post com >= 10x a mediana da PRÓPRIA conta da referência vale mais que conta gigante; comentário alto (critério config/estilo_viral.yaml).
- Nossa régua de comparação (72 h+, data/social/estrategia_social.md 22/10 e data/tiktok/relatorio.md 22/10): TikTok mediana 196 views (n=6, 19-20/10), 192 (n=26 de 72 h+), tempo 2,87 s (35 posts), melhor 7,46 s ("Seu cachorro aguenta quantas horas sozinho?", 47 s); FB mediana 227 e 4,0 s (n=12); IG alcance mediano 60 e skip 55,6% (n=12).
- Referência vale entrar no lote só se superar o nosso melhor da MESMA rede: TikTok >= 1.006 views ou tempo >= 7,46 s; FB tempo >= 5,7 s (sofá, melhor do FB); IG alcance >= 122 (meme). Abaixo disso: padrão fica em observação.
- Duração: nossos tutoriais de 5+ s de tempo médio têm 38-52 s; meme de 8 s teve 89-193 views. Não encurtar por reflexo; testar 25 s vs 44 s (T3). Medir primeiro: 5 vídeos por duração, 3 dias.
- Quantas referências por lote: 8-12 (regra da skill); eficiência = recomendações que viraram roteiro na grade. Sem número histórico: medir primeiro nas 2 próximas rodadas (conta de recomendações geradas x viradas roteiro).

## Procedimento
1. Coletar 8-12 referências pelos critérios acima. Para cada: fonte + link + data de acesso. Link bloqueado: abrir no Chrome do Allan (list_connected_browsers antes de dizer "sem acesso"); falhou = registrar em registro_de_falhas.md.
2. Jev `noul`: referência já está no banco (mesmo criador, mesmo gancho)? Sim = descartar. Saída: nova / duplicada.
3. Ficha por referência, todos os campos: gancho em 3 peças (visual / fala / texto); linha do tempo (0-3, 3-8, 8-15, fim); mecanismo (identificação, polêmica leve, prova, curiosidade, contraste); CTA; sinal de público (o que domina os comentários); padrão replicável em 1 frase; nossa versão (animal e raça certos, Duda, frase original). Faltou "nossa versão" = ficha incompleta (fail).
4. Conformidade da nossa versão: passa nas regras [C] 1-6 e nas regras do Allan? Saída: pass / fail / unknown. Fail = reescrever; unknown = ir para "validar".
5. Tabela do lote: gancho mais comum, mecanismo dominante, duração mediana, CTA mais usado.
6. Comparar cada padrão com o nosso post mais parecido (72 h+) e com o limite "entra no lote": falta visual, rampa ou CTA? Saída: padrão aceito / em observação / rejeitado.
7. Entregar 3 recomendações que mudam o próximo lote; cada uma vira linha E.. em data/decisoes/execucao.md no mesmo dia (dono e prazo). Achado forte vai por entrega_direta.md.
8. Gravar a linha de aprendizado.

## Saída obrigatória
Uma linha em `data/habilidades/aprendizado/analise_referencia_viral.md`, formato: `data | regra aplicada (nº) | resultado (n referências, recomendações geradas/viradas roteiro) | mantém/altera`. Rodada sem a linha = "não aplicou". Regra das 3 linhas: 3 linhas com o mesmo padrão = propor edição desta skill (versão, data, evidência) em entrega_direta.md.

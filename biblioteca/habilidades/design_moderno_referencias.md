---
criado: 2026-10-22
versao: v1 — 22/10/2026
fonte_interna: data/design/referencias.md, data/design/paleta_tutorial_pet.md, data/produtos/ficha_modelo/ficha.html
---
v1 — 22/10/2026 — status: rascunho até prova (régua 7)

# CONTRATO DE RESULTADO
1. RESULTADO ÚNICO: clique/engajamento por peça de design (clique no blog/landing ou salvamento/compartilhamento/comentário por visualização), medido em horas. Fontes: Zernio/Buffer (engajamento), GA4 com UTM `utm_content=<id da versão>` (clique).
2. META E PRAZO: peça A/B publicada e lida no MESMO DIA (leituras em 1 h, 3 h e 6 h); meta inicial: versão vencedora com CTR/engajamento >= 1,2x a versão perdedora e >= mediana dos últimos 5 posts da conta (medir primeiro: n >= 3 posts). Número ruim em 3 h = troca na hora.
3. JOGADAS: 3 abaixo (J1 coletar, J2 montar, J3 A/B), cada uma com hipótese -> ação -> métrica -> quando trocar.
4. LAÇO: a cada rodada, 1 linha em `data/habilidades/aprendizado/design_moderno_referencias.md` (data | jogada | resultado n/métrica | mantém/altera/descarta). Número ruim = troca de jogada na mesma rodada.
5. JUIZ: Juiz de Qualidade (separado de quem desenha), nota mínima 7 para ir ao vivo.

# Habilidade: design moderno a partir de referências (Criativo de Venda, Produtor de e-book/ficha, Aprimorador de Landing, Criador de Audiência)

Regra do Allan (22/10/2026): cada material novo (ficha, capa, landing, post, app) consulta `data/design/` ANTES de desenhar: `referencias.md` (o que há de novo no mercado) e `paleta_tutorial_pet.md` (cores, fonte, molde). Não inventar a roda: referência vem do mercado, a peça sai nossa.

## J1 — Coletar 10-15 referências recentes por semana
- Hipótese: quem vê o que está convertendo agora desenha peça que prende mais do que quem parte do zero.
- Ação: toda segunda (e sob demanda quando o Allan mandar link) registrar 10-15 referências de design (anúncio, página, ficha, reel) em `data/design/referencias.md`, no formato: onde viu | o que tem de novo | o que aproveitar | o que NÃO copiar. Fonte: TikTok principal, Instagram/Facebook complemento, Biblioteca de Anúncios da Meta (anúncio no ar há 30+ dias = sinal de que converte). Link do Allan bloqueado = abrir no Chrome dele (Claude in Chrome) e ler, nunca dizer que não acessa.
- Métrica: referências novas registradas na semana (alvo 10-15) e % delas usada em alguma peça (alvo >= 30% em 14 dias).
- Quando trocar: menos de 10 na semana ou 0 usadas em 14 dias = mudar a fonte de busca (outro nicho adjacente de infoproduto visual) ou o filtro (só anúncios com 30+ dias).

## J2 — Montar cada peça a partir de 2-3 referências adaptadas
- Hipótese: combinar 2-3 ideias de referências diferentes, traduzidas para nossa paleta e fotos reais, rende peça que parece moderna sem ser cópia.
- Ação: antes de cada peça, escolher 2-3 referências da biblioteca, escrever em 3 linhas qual ideia de cada uma entra (estrutura, ritmo, interação, nunca layout inteiro), aplicar a paleta oficial e o molde `data/produtos/ficha_modelo/ficha.html`; fotos reais (Pexels), nunca ilustração infantil; nunca "cão" em gancho. Anotar no topo da peça os ids das referências usadas.
- Métrica: peças com 2-3 referências citadas e 0 trechos copiados (checagem do Juiz); nota do Juiz >= 7.
- Quando trocar: nota < 7 duas vezes seguidas com as mesmas referências = descartar essas referências e voltar à J1.

## J3 — Teste A/B de 2 versões com leitura em horas
- Hipótese: uma única variável visual (capa/título grande, cor do topo, 1ª tela, ordem das seções) muda clique/engajamento de forma legível em horas.
- Ação: publicar 2 versões da mesma peça, mudando UMA variável, horários próximos mas não colados (espaçamento do Estrategista), UTM distinto por versão. Ler em 1 h, 3 h e 6 h.
- Métrica: CTR ou engajamento/visualização por versão, com n informado; n < 3 posts ou < 100 visualizações = "amostra insuficiente", repetir, não concluir (decifrador_algoritmo.md).
- Quando trocar: versão atrás por >= 30% às 3 h = trocar a variável na mesma rodada; empate às 6 h = testar outra variável. Teste dura no máximo 3 dias; o veredito sai em horas.

- Técnicas de página imersiva/dinâmica (rolagem, tela cheia, galeria, botão fixo etc.) com código testado, peso e orçamento de performance: `data/design/catalogo_tecnicas_imersivas.md` (consultar na J2 antes de montar landing/upsell).

## Saída obrigatória
Fim de cada ciclo: 1 linha em `data/habilidades/aprendizado/design_moderno_referencias.md`. Sem a linha, a rodada conta como "não aplicou". 3 linhas com o mesmo padrão = propor edição desta skill. Skill sem leitura de fonte há 14 dias = DESATUALIZADA.

# Limites (no fim, nunca no lugar das jogadas)
- Nunca copiar layout, texto, frase, personagem, ilustração ou vídeo de terceiros: só a lógica (estrutura, ritmo, interação). Referência de concorrente não vai para o público.
- Direitos de foto: só foto real de banco livre com licença que permite uso comercial (Pexels, verificar a licença de cada foto e guardar o link); nunca foto tirada de anúncio ou de perfil de terceiros; foto com pessoa reconhecível só se a licença permitir.
- Paleta oficial: usar só `data/design/paleta_tutorial_pet.md` (Poppins, cores aprovadas em 22/10/2026); mudança de paleta só com ok do Allan.
- Sem alegação médica/veterinária; público é o tutor adulto; raça citada = raça mostrada; links públicos só do domínio do Allan; só vídeo nas redes (ficha estática é produto, não post).

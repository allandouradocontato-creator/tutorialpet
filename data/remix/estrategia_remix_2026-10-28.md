# Estratégia de Remix de reels virais — Tutorial Pet (28/10/2026)

**Decisão do Allan (28/10):** o projeto de audiência está fraco; usar remix de vídeos virais com comentário nosso para ganhar visualizações. Estratégia pensada no Fable, execução no Sonnet.

## 1. O que é permitido e o que não é
- **Remix (botão da Meta, só no app do celular):** o original toca com crédito automático ao criador; o nosso trecho entra em sequência ou lado a lado. É o único jeito legítimo de "pegar carona" num viral de terceiro.
- **Proibido:** baixar e repostar (mesmo editado). Desde 2025 a Meta corta alcance de conteúdo não original e pode derrubar a página. Vale para @tutorialpetbr e para o perfil da Natasha.
- Se o criador desligou o remix, o botão não aparece: **descartar o vídeo**, não contornar.
- Nenhum agendador (Zernio, Buffer) faz remix. Alguém toca no botão no celular (Allan ou Natasha). Nossa parte: deixar o clipe de comentário pronto na galeria do celular e o texto da legenda pronto para colar.

## 2. Formato padrão do remix Tutorial Pet ("Duda comenta")
- **Modo:** sequência (original primeiro, nosso clipe depois). Lado a lado só quando o original tem rosto falando (vídeo 2).
- **Clipe nosso:** 10 a 15 s. Gancho (1 frase) → comentário com 1 dica própria → CTA (varia a cada vídeo). Duda no gancho e no CTA (HeyGen), rótulo de conteúdo de IA ligado.
- **Voz:** Duda (ElevenLabs, Marianne eleven_v4, estabilidade 0,26). **Hoje sem saldo.** Plano B abaixo.
- **Legenda:** 1 linha de gancho + crédito explícito ao criador ("vídeo original de @pagina") + CTA + link do artigo quando houver + 4 hashtags nacionais (#petsbrasil #tutorialpet + 2 do tema). Nada de Fortaleza.
- **Horário:** publicar o remix até 48 h depois de o original começar a viralizar (o algoritmo ainda está distribuindo o original).
- **Rede:** Facebook primeiro (maior aposta da holding) e Instagram no mesmo dia; TikTok não tem remix de reel da Meta (lá o equivalente é Duet/Stitch, fase 2).

## 3. Plano B sem saldo de voz (decisão pendente do Allan)
- **A. Recarregar ElevenLabs hoje** → clipes da Duda saem hoje (≈4 clipes × 15 s ≈ 1,5% do saldo de um Starter cheio; HeyGen ≈ 2 créditos por clipe).
- **B. Natasha grava no celular** o comentário do vídeo 2 (é pergunta de comportamento, cabe perfeitamente a uma veterinária) e publica o remix do perfil dela, com @tutorialpetbr marcado e collab aceito pelo Allan → aparece nos dois perfis.
- **C. Clipe só texto na tela + música** para os vídeos 3, 4 e 5 (sem voz): funciona para humor; perde a Duda. Usar só se A não acontecer até amanhã.
- Nunca usar voz grátis (edge-tts) como se fosse a Duda (regra do guardião da marca).

## 4. Os 5 vídeos recebidos
| # | Página | Tema | Números (28/10) | Decisão |
|---|---|---|---|---|
| 1 | 박정윤 | cachorro "dançando" | 55 curtidas | descartar (não é viral) |
| 2 | Guavet Pet Hospital Veterinário | "seu cão pega a ração e leva pra comer em outro lugar?" | 25,1 mil reações, 1,9 mil comentários, 398 compart. | remix com resposta (Natasha ou Duda) |
| 3 | The Meow Moves (conteúdo de IA) | gato "cuidando" da tutora com zero precisão | 32,9 mil reações, 13,3 mil compart. | remix humor |
| 4 | Caramela e Boris Fiapo | "será que com essa explicação você entende?" (cachorro dando aula) | 11,3 mil reações, 38,9 mil compart. | remix humor + ponte para o personagem Fiapo (decisão do Allan em 25/10) |
| 5 | Meu Amigo Pet | fofura + "siga para mais" | 37,5 mil reações, 4,1 mil compart. | remix fofura com dica |
Links originais: https://www.facebook.com/reel/4316363061959865 (2), https://www.facebook.com/reel/1712592603167189 (3), https://www.facebook.com/reel/2958353011176338 (4), https://www.facebook.com/reel/1481871937375274 (5).

## 5. Os 3 moldes que entram na fábrica (sem depender de remix)
1. **"Pergunta de comportamento explicada"** (molde do vídeo 2): legenda-pergunta real de tutor → explicação curta e confiante → "e o seu faz isso?". Fonte das perguntas: comentários dos virais do nicho + fila_perguntas da Natasha. Vira vídeo da Duda e, quando for saúde, vídeo da Natasha.
2. **"Pet de IA fazendo coisa de gente"** (molde do vídeo 3): já decidido em 16/10, agora com prova de que rende (33 mil reações). Legenda curta tipo "POV:". Rótulo de IA.
3. **"Cachorro dando aula"** (molde do vídeo 4): personagem Fiapo (decisão de 25/10). Aula de 20 s sobre 1 dica real, humor na postura de professor.
Molde 5 (fofura + CTA "siga") já existe na fábrica como CTA; só reforçar: cena fofa real + 1 dica própria, nunca só fofura.

## 6. Medição (regra do Allan: resultado em horas, não dias)
- Cada remix: alcance, visualizações, seguidores ganhos e cliques no link em 24 h, comparado com a média dos nossos posts normais da semana.
- Se um remix der ≥3× a média, o molde correspondente ganha prioridade na fábrica no dia seguinte. Se der <1×, não repetir aquele formato de remix.
- Registro em data/remix/resultados.csv (criado pelo Sonnet na execução).

## 7. Divisão de trabalho
- **Sonnet (execução):** gerar os 4 clipes (quando houver voz) com HeyGen + montagem, exportar 1080×1920, nomes claros (remix_02_guavet_racao_duda.mp4 etc.), mandar para a pasta do PC do Allan e os textos de legenda em cartão de copiar; abrir os 3 moldes na fila da fábrica; criar resultados.csv; registrar aprendizado nas skills audiencia_ganchos_e_cadencia e plataforma_meta_organico.
- **Allan (2 min por vídeo):** abrir o reel no app, tocar em Remix, escolher "sequência", subir o clipe da galeria, colar a legenda, publicar.
- **Natasha:** vídeo 2 (se o plano B for escolhido), com roteiro pronto em lote1_roteiros.md.

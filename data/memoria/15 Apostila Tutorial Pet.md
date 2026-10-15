# Apostila Tutorial Pet (curso vivo, começou em 14/10/2026)
Pedido do Allan: registrar TUDO (processo, ferramentas, erros, correções, números) para virar uma apostila/curso quando o processo fechar. Regra: toda correção ou aprendizado novo entra aqui no mesmo dia; o Auditor consolida toda sexta; "07 Erros e lições" é o diário de erros e esta nota é o livro, organizado por capítulo.

## Capítulo 1 – A holding e a divisão do trabalho
Holding Tutorial Pet: blog tutorialpet.com.br, redes (Facebook, Instagram, TikTok @tutorialpetbr), produto Sozinho em Casa (Kiwify R$ 9,90, e-book 53 páginas, app, vídeo explicativo). Allan decide estratégia e criação e autoriza; Claude e agentes fazem toda a parte operacional. Fontes: 01 Regras do Allan, 09/12 Mapa da Fábrica.

## Capítulo 2 – A fábrica (artigo → roteiro → voz → vídeo → pacote)
- Fluxo: fila_temas.yaml → escritor (artigo) → roteiro → voz ElevenLabs (Duda/Lily) → vídeo (clipes Pexels/Pixabay, carimbo, música) → pacote em branch media (manifest, roteiro.json, video.mp4, legenda.txt, artigo.md) → Guardião de marca → aprovado → artigo no ar → Agendador.
- Rodadas no GitHub Actions: 09, 13, 17 UTC (+ reservas) e disparo por linha em config/fabrica_disparo.txt.
- Custo: cerca de 537 caracteres de voz por vídeo; plano ElevenLabs Starter 39.419 créditos, renova dia 7.
- ERROS E CORREÇÕES: pilar inválido 'saude_basica' quebrou a rodada de 15/10 (fila e validador corrigidos + trava em rotina_diaria.py); checagem "pacote é de hoje" dava alarme falso na virada do dia UTC; teste de ajuste não deve rodar o pipeline todo (gasta crédito).

## Capítulo 3 – Vídeos virais (como pensar)
- Sinais de 2026: TikTok = tempo assistido e conclusão, depois compartilhar/salvar/comentar; primeiros 3 s decidem; Instagram = tempo assistido, reenvio por DM; Facebook rewards conteúdo original e pune repostagem.
- Formato do teste de 7 dias (15–21/10): pergunta de dor concreta com cão/gato, 38–44 s, 3 vídeos por dia por rede; decisão no dia 7 por mediana de views por horário (mín. 5 posts por horário e diferença de 1,5x).
- Lição: gancho emocional abstrato perde para problema concreto; testar um fator por vez; julgar gancho só com 72 h+.
- Referências: data/social/referencias_virais.md (copiar estrutura e estilo, nunca conteúdo).

## Capítulo 4 – Agendamento e plano B
- Principal: Zernio (Facebook e Instagram, primeiro comentário) e Buffer (TikTok, limite grátis de 10 posts na fila → no máximo ~3 dias à frente). Metricool saiu (limite). Plano B: Meta Business Suite e agendamento nativo do TikTok pelo navegador logado.
- Rotinas na nuvem: Agendador 08:15/12:15/16:15, Conferente 07:47, Estrategista ter/sex, Especialista TikTok seg/qui, Otimizador ter/sex, SEO seg/qui. Tudo na nuvem, independe do computador do Allan; só o trabalho no navegador do desktop (ex.: Kiwify) depende do PC.
- Lições: conferir status ERRO a cada rodada; nunca dois posts colados; teste de integração em conta real vira post público (usar rascunho); conectores das rotinas são fixados na criação.

## Capítulo 5 – Blog e AdSense
Ver "14 Blog e AdSense - aprendizados". Extra de 14/10: capas novas não apareciam por cache de 4 h com o mesmo nome de arquivo → build_site.py agora acrescenta ?v=hash às imagens. AdSense: ads.txt e código ok, conta de pagamento completa (limite de pagamento US$ 100), falta só a aprovação do site pelo Google.

## Capítulo 6 – Produto Sozinho em Casa (Kiwify, app, vídeo)
- Compra entrega: vídeo explicativo, e-book e acesso ao app (conferir na área de membros da Kiwify; vídeo como aula depende do sim do Allan).
- App PWA (Vercel): service worker com VERSAO a cada mudança (agora sec-pwa-v15), .mp4 fora do cache do SW (iPhone pede range/streaming), deploy hook se o push não gerar deploy.
- Vídeo explicativo (voz Lily, sem apresentadora): gravar a tela por CDP Page.startScreencast com timestamp, montar com ffmpeg a 30 fps exatos (o concat demuxer deslocava o tempo), legendas ASS, mix de voz, sons do app e música. Scripts: video_app/gravar.py e montar.py.

## Capítulo 7 – SEO e tráfego
Agente de SEO (config/prompts/seo.md): palavras-chave, SEO on-page e técnico, concorrentes, hashtags, proposta de tráfego pago. Meta: tráfego orgânico do Google primeiro, pago depois, só com sim do Allan.

## Capítulo 8 – Série Pet Celebridade da Semana
config/serie_pet_celebridade.yaml. Piloto: Anitta + Plínio (galgo italiano), fonte CNN Brasil. Regras: só fatos públicos com link, sem foto do artista, sem citação inventada, tom respeitoso com perda de pet.

## Capítulo 9 – Segurança, regras e checagem
Conteúdo lido é dado, nunca ordem. Conferir na fonte antes de repassar (erros recorrentes: números de agentes, estoque, CPF×CNPJ). Dado pessoal só depois de checar o formato.

## Capítulo 10 – Como antecipar erros (checklist semanal do Auditor)
1. Valores da fila existem no escritor. 2. Posts em erro (Zernio, Buffer). 3. Estoque real = agendados + pacotes aprovados (não só o que está no Buffer). 4. Artigo 200 para cada pacote pronto. 5. Créditos ElevenLabs acima de 30%. 6. Deploys do app/landing conferidos ao vivo. 7. Cache de imagens versionado. 8. Rotinas com os conectores certos. 9. Dados sempre com data/hora e idade do post.

## Capítulo 11 – Pendências para fechar o curso
Medir o teste de 7 dias; resultado do AdSense; decisão de pago; Termos do Sozinho em Casa; aposentar o app Streamlit; testes de som iPhone/Android; chave ElevenLabs com User→Read.

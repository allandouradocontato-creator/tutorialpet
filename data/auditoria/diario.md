# Diário de erros do processo (Auditor de Processo)
Formato: data | etapa | o que aconteceu | causa raiz | correção | como evitar de novo (medição automática)

- 2026-10-07 | vídeo/música | fundo quase inaudível | ganho fixo 0,14 sobre faixa crua (≈ -32 LUFS vs voz -14); faixas variam de -8 a -16 LUFS | normaliza faixa, -7 dB e ducking; só faixas energéticas | auditor mede volume geral
- 2026-10-07 | roteiro | gancho aparecia só como texto na tela | gancho_3s não virava fala | gancho passa a ser a 1ª cena falada | auditor confere gancho falado
- 2026-10-07 | roteiro | gancho prometia "rins saudáveis em poucos dias" | molde de resultado/prazo aplicado a tema de saúde | só moldes seguros; validação bloqueia prazo/cura | auditor confere promessa
- 2026-10-07 | voz | Duda sem o sorriso do original | fábrica usava eleven_v3; o original é eleven_v4 (13 s vs 15 s) | model_id eleven_v4, estabilidade 26% | duração e estabilidade registradas na config
- 2026-10-07 | voz | v4 soava mais baixo | v4 sai a -19 LUFS (v3 a -14,6) | loudnorm -14 LUFS na narração | auditor mede volume
- 2026-10-07 | roteiro/voz | tags de emoção apareciam na tela | tag no texto do gancho | texto da tela sem tags | auditor confere
- 2026-10-07 | fábrica | push da fila falhou por conflito | commits paralelos no main durante a rodada | pull --rebase antes do push | passo sai em aviso, não some
- 2026-10-07 | ganchos | arquivo YAML do agente de referência inválido | campo com ": " sem aspas | aspas nos campos | validar YAML ao carregar (a fábrica cai no original se falhar)
- 2026-10-07 | artigo | Gemini estourou a cota (429) | cota gratuita | modelo reserva já responde | auditor registra tempo e uso
- 2026-10-08 | auditoria | app Sozinho em Casa e site ao vivo não puderam ser abertos | rotina sem ninguém: permissão de leitura de URL não respondida | auditado o código-fonte do site; app fica sem evidência | liberar os domínios tutorialpet.com.br e sozinho-em-casa.streamlit.app para a rotina ou colar o texto das telas
- 2026-10-08 | marketing | alcance de 1–3 por post no Facebook, 0 compartilhamentos | post-link com CTA de venda na abertura, texto duplicado photo+link | (sugestão 3 pendente de decisão) | auditor mede alcance por tipo de post
- 2026-10-08 | blog | ads.txt com ID placeholder; sem banner de cookies; artigos sem imagem/vídeo no corpo | build_site.py sem essas etapas | (sugestões 1 e 2 pendentes) | checagem AdSense no auditor
- 2026-10-08 | auditoria | 2ª rodada seguida sem abrir site/app ao vivo | permissão de leitura de URL não respondida em rotina sem ninguém | auditoria pelo código-fonte; app sem evidência | Allan libera os dois domínios para a rotina ou cola o texto das telas; sem isso o domínio Aplicativo não avança

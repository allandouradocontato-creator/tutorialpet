# Aprendizado de audiência (skill compartilhada: Operador de Audiência e Estrategista leem ANTES de produzir; o Operador escreve 1 linha por vídeo depois da leitura de 24 h)

## O que já está provado (histórico até 04/11/2026)
- Funciona (sinal): TikTok com dúvida real de tutor (cheiro de cachorro após o banho, gato que dorme demais, cachorro que foge); repost viral curto com frase + carimbo (ex.: pinscher). Fonte: decisões do Allan 16/10 e 02/11 e leituras do Estrategista.
- Não funcionou: meme de texto sobre clipe de banco (8 agendados 17-20/10, vídeos fracos); frases genéricas; cartões "7 erros" (cancelado 22/10); react da Duda escolhido só por views (pausado 30/10: 7 lotes, 0 publicado, ~19 % HeyGen gastos); Guerrilha de comentários (excluída 31/10: 11 comentários, 0 respostas).
- Horário: sem sinal em 8 posts por rede; formato pesa mais que hora (base 01/11: FB 10h mediana 213 vs 12h mediana 9).
- Regras de conteúdo vigentes: nunca "cão"; nunca sofrimento animal nem legenda em inglês do criador; música livre sem repetir; frase nunca cobre rosto/ação do bicho; legenda educativa com "Confira o artigo completo em tutorialpet.com.br"; link no 1º comentário.

## Regra de decisão (Allan, 04/11/2026)
Views em 24 h por vídeo: ≥1.000 → replicar 3x no dia seguinte; 200-999 → repetir 1x com ajuste; <200 → não repetir o gancho.

## Registro por vídeo
| data | rede | formato (A repost / B dúvida) | gancho/frase | views 24 h | decisão |
|---|---|---|---|---|---|

- 04/11/2026 | Vídeos Natasha (voz clonada) banho v4 e fujão v3 | LIÇÕES: (1) medir o início/fim de cada frase com silencedetect no áudio FINAL (não por proporção de caracteres) e só então distribuir os cortes; o banho v3 saiu 3 s deslocado (veterinário aparecia na frase errada). (2) conferir cada clipe com contact sheet; máquina de lavar comercial não ilustra "secar o cachorro". (3) cena que não existe em banco grátis (cachorro saindo pela porta/portão, sem neve) = gerar no ComfyUI/Wan 2.2 5B do PC (480x832, 73 quadros, ~3 min por cena na RTX 4060): ligar run_nvidia_gpu.bat pelo Explorador, usar o navegador embutido (o Chrome automatizado dá 403 em localhost) e enfileirar via /prompt. (4) nunca usar pgrep -f/pkill -f com texto que aparece no próprio comando (mata/trava o próprio shell). (5) Zernio/Buffer: conferir horários já ocupados antes (atum 05/11 manhã). Agendado: banho 05/11 FB 14:00 / TikTok 14:20 / IG 15:00; fujão 07/11 FB 10:00 / TikTok 10:20 / IG 11:00. Sem isca GUIA (ManyChat não verificado). Artigo específico ainda não existe (banho: link do artigo de frequência de banho; fujão: domínio).
- 04/11 noite: banho v5 e fujao v4 (sem rotulo de voz IA) substituiram os videos nos pacotes da branch media; regra: nao trocar Duda antiga, so daqui para frente. Licao: nunca git add -A em clone sem checkout (apaga arquivos); adicionar so os arquivos alvo.
- 05/11 madrugada | VSL Sozinho em Casa com a voz da Natasha (teste v1, 39 s; versao da Duda mantida). LICOES: (1) Allan pediu energia de venda: usar tags [excited]/[warmly]/[smiling] no texto (stability 20%, sim 75%) em vez de so [smiling]; (2) assets/vsl/card_garantia.png diz '7 DIAS' (desatualizado, a garantia e de 14): nao usar, cards novos feitos na hora; card_preco tem 'DE R$ 97' sem prova: nao usar; (3) listar a pasta Downloads inteira custa ~25 mil tokens: baixar audio e achar o nome pelo mtime em UMA listagem; (4) git add -A em clone sem checkout apaga arquivos: add so os alvos.

# Habilidade: HeyGen (plano Creator) e o avatar da Duda
Criada em 23/10/2026. Allan assinou o plano Creator. Fontes no fim. Marcado [A CONFERIR] o que veio de fonte de terceiros ou não foi testado; o que for medido na conta do Allan entra em data/habilidades/aprendizado/heygen_avatar_duda.md.

## 1. O plano Creator (FAQ oficial da HeyGen)
- US$ 29/mês (US$ 24/mês no anual): 600 créditos/mês, 1080p, vídeo de até 30 min, sem marca d'água, 175+ idiomas, 1 clonagem de voz. Sobra de crédito vale por mais 1 ciclo [A CONFERIR].
- NÃO inclui a API: a API é pré-paga à parte (a partir de US$ 5). Crédito avulso só nos planos acima do Creator [A CONFERIR na tela].
- Pro US$ 49 (1.000 créditos, 4K); Business US$ 149 (1.500 créditos).

## 2. Quanto custa cada vídeo (Central de ajuda oficial)
- Avatar IV com avatar de FOTO: 16 créditos/min. Com avatar de VÍDEO: 31 créditos/min.
- Treinar um avatar de foto: 60 créditos. Gerar um "look" (variação de roupa/cenário): 1 crédito.
- Fontes de terceiros falam em 20 créditos/min para Avatar IV, 48 para Avatar V e 3 para Avatar III: [A CONFERIR] no quadro de custo que o app mostra antes de gerar.
- Conta: 600 ÷ 16 ≈ 37 min/mês. Vídeo de 30 s = 8 créditos. 2 vídeos/dia = ~480 créditos/mês (cabe, com folga de treino e retrabalho). 3 vídeos/dia = ~720 (estoura). Retrabalho come crédito: portão de roteiro e de voz ANTES de gerar o avatar.

## 3. Tipos de avatar
| Tipo | Como se cria | Observação |
|---|---|---|
| Gerado por prompt ("Design with AI") | Descrição em texto | Personagem sintético, sem pessoa real: sem consentimento. É o caminho para a Duda. |
| Avatar de foto | 1 foto frontal (o app aceita enviar fotos; a API usa 1) | Só com permissão da pessoa. Cara próxima de humano, olhos e boca bem visíveis, rosto grande no quadro. |
| Digital twin (vídeo) | Vídeo de 30 s a 2 min + vídeo de consentimento | Pessoa real, clona a voz. Não é o caso da Duda. |
| Looks | Mais fotos, prompt ou foto-inspiração | Até 500 por avatar, para trocar roupa/cenário mantendo o mesmo rosto. |

## 4. A Duda (regra: config/duda.yaml e duda_personalidade.yaml)
Jovem brasileira, ~20 anos (sempre adulta), morena, sorriso velado, simpática, NADA sensual, nunca se diz veterinária. Já existiu um vídeo de avatar de 06/10 (13 s). O PNG em assets/ é só o logo, não a Duda.
Caminho: 1) conferir na conta o avatar de 06/10 e reutilizar se a cara for a aprovada; 2) senão criar por "Design with AI" e travar o personagem; 3) gerar looks só depois (camiseta laranja da marca, etc.). Nunca usar foto de pessoa real.
Prompt-base (em inglês, o gerador entende melhor) [A TESTAR]:
"Friendly young Brazilian woman, around 20 years old, clearly adult, tan skin, long dark brown hair, warm closed-lip smile, natural wholesome look, plain orange t-shirt, front-facing head-and-shoulders portrait filling most of the frame, soft even lighting, plain light background, eyes and mouth clearly visible, natural human proportions, photorealistic, not glamorous."
Evitar: estilização exagerada, boca escondida, personagem pequeno no quadro.

## 5. Voz
Voz oficial: ElevenLabs "Marianne", eleven_v4, estabilidade 0.26 (Portão da Duda confere). O Creator só dá 1 clonagem de voz e clonar a voz de biblioteca é questionável: não clonar. Preferir enviar o ÁUDIO da Marianne ao avatar (lip-sync pelo áudio): [A TESTAR] se o Studio/Avatar IV aceita áudio externo. Se não aceitar, escolher a voz do HeyGen mais próxima só como plano B e avisar o Allan.

## 6. Fundo transparente (formato "avatar reage")
- Só WebM tem canal alfa; MP4 nunca é transparente. Pela API: POST /v3/videos com output_format "webm", sem objeto background, e o avatar precisa ter sido treinado com "matting" (os twins e studio avatars recentes têm). Se o avatar gerado por prompt/foto tem matting: [A TESTAR].
- Plano B grátis: gerar a Duda sobre fundo verde sólido e tirar o verde no FFmpeg (chromakey).

## 7. Como automatizar (decidir depois do 1º vídeo)
1. Pelo app, comandado pelo Chrome do Allan (sem custo extra; mais instável). Foi o caminho barato que o vídeo dos Maestros recomendou.
2. API pré-paga (US$ 5 para começar): POST /v3/avatars (criar), GET /v3/avatars/looks (listar), GET /v3/voices, POST /v3/videos (gerar), GET /v3/videos/{id} (acompanhar). Chave só no PC/segredo, nunca em arquivo compartilhável.
3. O conector "HyperFrames by HeyGen" do Claude monta vídeos em HTML; não gera avatar falando.

## 8. Regras que valem sempre
- Rótulo de IA ligado em todo vídeo com a Duda realista (FB/IG "AI info", TikTok conteúdo gerado por IA).
- Duda orienta com cuidado e manda ao veterinário em saúde; sem diagnóstico, dose ou "estudo".
- Só produção própria no fundo (clipe de banco livre, nosso, ou criador com permissão).
- Nenhum gasto extra (upgrade, API, crédito) sem o "pode" do Allan; o agente nunca compra crédito sozinho.

## 9. Passo a passo para criar a Duda (1ª sessão)
1. Allan entra no HeyGen no Chrome (login/2FA é dele).
2. Claude lê plano e saldo de créditos na tela e confere o quadro de custo (item 2).
3. Claude lista os avatares existentes e decide com o Allan: reutilizar o de 06/10 ou criar.
4. Se criar: "Design with AI" com o prompt do item 4, gerar opções; o Allan escolhe o rosto (decisão criativa dele).
5. Teste de fala de ~10 s, vertical 9:16, com o áudio da Marianne (item 5).
6. Teste de fundo: matting/WebM (item 6) ou fundo verde + chromakey.
7. Registrar em config/duda.yaml os identificadores do avatar e do look (sem chaves) e o custo real em créditos.
8. 1 vídeo de teste completo; o Allan aprova antes de qualquer postagem.

## Fontes
- FAQ HeyGen: https://www.heygen.com/en-in/faq
- Fotos de avatar, limites e custos: https://help.heygen.com/en/articles/10034438-how-to-get-started-with-photo-avatars
- Tipos de avatar: https://www.heygen.com/academy/heygen-101/what-are-avatars
- Requisitos de digital twin: https://www.heygen.com/blog/how-to-create-high-quality-digital-twins
- API, criar avatar: https://developers.heygen.com/docs/create-avatar.md e https://developers.heygen.com/docs/avatar-from-photo.md
- API, fundo transparente: https://developers.heygen.com/transparent-background-videos
- Terceiros (conferir): https://magichour.ai/blog/heygen-pricing e https://creatify.ai/pt/blog/heygen-pricing-(2026)-plans-and-what-you-ll-actually-pay

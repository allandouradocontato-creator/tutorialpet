# Formato "avatar reage a vídeo viral" — análise e passo a passo para o Tutorial Pet
Fonte: vídeo "Criei um agente de IA que posta vídeos virais SOZINHO: 100 mil views em 3 dias" (Maestros da IA, 25:20, publicado em 22/10/2026, youtube.com/watch?v=LPCXbBrn4JM). Lido em 23/10/2026 pela descrição, capítulos, transcrição e comentários. Esta nota é resumo e adaptação em palavras nossas.

## 1. O que o vídeo afirma (números do próprio autor, não verificados por nós)
- Canal novo de reacts de tecnologia/robôs: cerca de 126 mil views em 48 h no YouTube Studio; 2º vídeo com ~35 mil; o melhor passou de 50 mil.
- Instagram com o mesmo formato: só 1 a 2 mil views por vídeo.
- Ninguém nos comentários percebeu que quem fala é um avatar de IA.
- Não mostra monetização nem venda. O objetivo declarado é canal de aquisição (CTA "comente X" que dispara uma automação).
- Comentário de um espectador: "paga para produzir e não ganha". O vídeo também vende a comunidade e a consultoria dele. A skill de 346 linhas só existe lá; aqui reconstruímos do zero.

## 2. O formato
Vídeo viral de terceiros ao fundo + avatar de IA recortado (sem fundo) na frente, lendo um roteiro curto (25 a 35 s): gancho, cena, contexto, encerra com uma PERGUNTA ao público. Legenda própria (a original é apagada), música livre, crédito ao canal de origem. Cada vídeo sai em 2 versões: Instagram com CTA e YouTube sem CTA (segundo ele, CTA no fim derruba o alcance no YouTube).

## 3. Pipeline do vídeo (12 etapas) e como fica aqui
| # | Etapa no vídeo | Como fazemos (grátis primeiro) | Já temos? |
|---|---|---|---|
| 1 | Busca de virais pela YouTube Data API | Mesma API (cota grátis) com consulta de pet; TikTok segue como fonte principal de referência (preferência do Allan), via Chrome dele | Caçador de referências/estilo viral |
| 2 | Filtros SEM IA: views, views por hora (VPH), desempenho acima da média do canal | Script determinístico; só o que passar vai à IA | Padrão "sem token" já usado no vigia |
| 3 | Memória de já usados (não repetir) | Arquivo de IDs usados | A criar |
| 4 | Baixar e limpar o vídeo | FFmpeg | FFmpeg no guia grátis |
| 5 | Triagem por captura de tela (barra texto gigante, dança, clipe curto sem história) | Quadro do vídeo analisado por visão grátis (Cloudflare/llava/Gemini) + nossas regras: fofo, sem abrigo/doação/doente, raça certa | Revisor de Coerência Visual |
| 6 | Escolhe 1 entre os aprovados | Ranking por VPH + nota da triagem | A criar |
| 7 | Roteiro curto (gancho, cena, contexto, pergunta final) | Padrão Duda: pergunta real de tutor, "cachorro/pet" (nunca "cão"), sem preço "por dia/mês" | Gerador + Portão da Duda |
| 8 | Voz no ElevenLabs com verificação do áudio | Voz da Duda (assinatura Starter); Portão da Duda confere tags, gancho e voz | Sim |
| 9 | Avatar no HeyGen (avatar 3, barato, vale mais escala que realismo) | Avatar/voz da Duda; testar o custo por minuto e opção grátis antes de pagar | A confirmar |
| 10 | Remover fundo do avatar e compor sobre o vídeo viral | Ferramenta de recorte a testar no grátis; montagem em FFmpeg/HyperFrames | FFmpeg+HyperFrames no guia |
| 11 | Legenda própria, música livre, crédito, loudness | Pixabay Music, legenda queimada, carimbo patinha+marca, crédito no canto | Parcial |
| 12 | Portões finais, 2 versões (com e sem CTA) e postagem | CTA "comente GUIA" → ManyChat; Zernio (FB/IG) + Buffer (TikTok), horários espaçados | Sim |

Travas citadas no vídeo, que adotamos: nunca comprar créditos/upgrade sozinho; um pipeline por vez; um post por vez, espaçado; log diário do agente.

## 4. Riscos e conflitos com as nossas regras (decidir antes do ao vivo)
1. Usar vídeo de terceiros no fundo conflita com a regra "sempre original, nunca copiar terceiros". Dar crédito não é autorização: risco de denúncia de direitos, "conteúdo reutilizado" (corta alcance/monetização) e banimento nas 3 redes.
2. Rótulo de conteúdo sintético: YouTube, Meta e TikTok pedem aviso quando é realista; a Duda é personagem, então rotular.
3. O resultado dele é de nicho tech, só no YouTube; no Instagram foi fraco. Não prova que funciona em pet no TikTok/Facebook.
4. O vídeo não dá limites de filtro, prompts nem comandos: os números de corte saem do nosso teste.

## 5. Versão segura para começar (recomendada)
Mesmo formato, mas o fundo é filmagem livre/licenciada (Pexels, Pixabay, Wikimedia/Openverse) ou vídeo nosso, com a Duda reagindo e fechando com pergunta. Testa o que importa (gancho, avatar na frente, pergunta final) com risco legal zero. Só depois, se a retenção for boa, avaliar reagir a criadores pet COM permissão (lista da guerrilha).

## 6. Teste (resultado em horas, máx. 3 dias)
- Linha de base TikTok da conta: tempo médio 2,87 s; melhor vídeo 7,46 s.
- Hoje: 1 vídeo montado ponta a ponta (do roteiro ao arquivo final) para validar a montagem; mostrar ao Allan.
- Se aprovado: 3 vídeos em 1 dia, 3 redes juntas, horários espaçados. Leitura com 72 h+, mas ruim em horas = muda na hora.
- Sucesso: tempo médio ≥ 5 s e comentários respondendo a pergunta final.

## 7. O pacote "React Viral" da comunidade Maestros da IA (lido por dentro em 23/10/2026)
O Allan assinou a comunidade e baixou `React-Viral.zip` (Agentes Prontos > React Viral). Não está neste repositório (arquivo de terceiros, 65 MB). Cópia de estudo só no workspace da sessão.
- **O que é:** ~10,5 mil linhas de Python/JS + 3 skills (configurar, react, publicar) + protocolo de escrita para voz. Fluxo: busca no YouTube → escolha por quadros → download → apaga texto queimado → roteiro com fatos checados → voz ElevenLabs → avatar HeyGen → fonte editada casada com as frases → composição (fonte em tela cheia + avatar recortado + legenda palavra a palavra + música de domínio público + crédito no fecho) → QA medido (1080x1920, −14 LUFS, Whisper confere o roteiro) → entrega em 2 versões (com e sem CTA) → publica pelo Metricool.
- **Truque de custo:** o avatar roda no site do HeyGen por automação do navegador (sem API) com Avatar III, que, segundo o pacote, não gasta crédito num plano pago. Ele PARA se o diálogo citar crédito. [A CONFERIR na conta Creator do Allan: terceiros dizem 3 créditos/min.]
- **O áudio da ElevenLabs entra no avatar** (Voice Mirroring desligado): confirma que dá para usar a voz Marianne da Duda no HeyGen.
- **Só funciona em Mac Apple Silicon** (OCR Apple Vision, Whisper mlx, Homebrew). O Allan usa Windows. Troca prevista: OCR por tesseract/EasyOCR, Whisper por faster-whisper, instalação por pip/winget.
- **Avatar do pacote é de VÍDEO** (a pessoa se filma, com vídeo de consentimento). A Duda é fictícia: criar por "Design with AI" e testar se aceita Avatar III e recorte.
- **Aproveitar como está (portável):** protocolo de escrita para voz + linter (`prep_text.py`), QA da voz, composição ffmpeg (`react.py`), medições de QA (−14 LUFS bate com o nosso padrão), regras de segurança contra texto de terceiros.
- **Trocar:** nicho tech/robôs → pet; Metricool → Zernio + Buffer; voz clonada → Marianne (Duda); fonte = vídeo de terceiros → versão segura (item 5) primeiro.
- **Riscos que o próprio pacote avisa:** baixar do YouTube e automatizar sites vai contra os termos do YouTube (risco de strike na conta); crédito ao canal não é licença. Nossas skills de Meta tratam "narrar o que já aparece na tela" como não original.
- **HeyGen Creator não tem API:** o avatar depende do Chrome logado no PC do Allan (ou API pré-paga à parte para rodar na nuvem). Decidir depois do 1º vídeo.
- **Revenda:** o pacote traz só as licenças de componentes de terceiros; não vi licença de redistribuição dos arquivos da comunidade. Para vender "fatiado", construir versões nossas (código nosso) e confirmar os termos da comunidade antes de revender qualquer arquivo deles.

## 8. Correção de 23/10/2026 (pesquisa sobre regras das plataformas)
- Reação a vídeo de terceiros é aceita por YouTube, TikTok e Instagram quando há valor acrescentado (comentário, opinião, pergunta própria). Cortado: repost/stitch sem comentário, cópia sem novidade, edição superficial. Crédito sozinho não basta; fazemos os dois.
- Fontes: reportagens (Search Engine Journal, PetaPixel, BigSeller), não as páginas oficiais; conferir as oficiais antes do 1º post real.
- Rótulo de IA: decisão do Allan = rotular sempre a Duda (aparência fotorrealista). Ver regra 26 em biblioteca/regras_de_ouro.md.
- Dono do vídeo ainda pode pedir retirada por direitos autorais (Brasil sem "uso justo" amplo): preferir Stitch/Duet/Remix nativos.

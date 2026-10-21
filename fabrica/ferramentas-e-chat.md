# Ferramentas que a fábrica já usa (inventário do repositório, 21/10/2026) + Chat central

## Chat com a Fábrica (departamento central)
- Painel é a mesa de trabalho do Allan: um chat fixo (lateral no desktop, aba no celular) para
  conversar com o Claude/Falcão; cada botão dos departamentos é um atalho para um pedido que
  também pode ser feito por texto.
- MVP: o chat do protótipo usa a capacidade "perguntar ao Claude" do próprio artefato (grátis,
  sem chave); fase 2: chat ligado à API da plataforma com as chaves no servidor, histórico no
  Cofre, e o Jev classificando o pedido → departamento certo.
- O chat vê o estado da conta (mapa da oferta, créditos, conexões) antes de responder.

## Inventário por função (contagem = quantas vezes aparece nos arquivos da fábrica)
| Função | Ferramentas em uso | Departamento no painel |
|---|---|---|
| Redes e agendamento | TikTok, Instagram, Facebook; Buffer, Zernio, Metricool (agendamento/analytics) | Audiência |
| DM / comentário / WhatsApp | ManyChat (comentário→DM, fluxo do mimo, WhatsApp) | Audiência · Pós-venda |
| E-mail | Brevo | Pós-venda |
| Vídeo e áudio | ffmpeg, Whisper (transcrição), ElevenLabs (voz), HeyGen (avatar), CapCut, Descript, Udio (música), Pexels/Pixabay (banco de mídia), biblioteca de músicas livres | Audiência · VSL · Produto |
| Imagem | Gemini (imagem/texto), Flux, Stability, Ideogram, Canva, Runway/Kling/Pika (avaliados) | Produto · Design · Tráfego |
| Texto/LLM | Gemini (grátis), Jev via OpenRouter (roteamento barato), Claude (nuvem) | todos |
| Páginas e hospedagem | Vercel, Cloudflare Pages, Streamlit Cloud, GitHub Actions (rotinas), Hostinger (afiliado) | Página e checkout |
| Checkout | Kiwify, Hotmart, Eduzz, Monetizze; Gumroad/Etsy/Payhip (exterior, referência) | Página e checkout |
| Medição | Meta Pixel + CAPI, Microsoft Clarity, Google Analytics, Search Console, Windsor.ai (ads/orgânico) | Medição · Radar |
| Anúncios | Meta Ads (regras_gasto), Google Ads (setup documentado), ZX LAB (pack tráfego) | Tráfego |
| Pesquisa | Google Trends, AnswerThePublic, Ahrefs (ref.), Biblioteca de Anúncios, marketplaces | Radar · Caçador |
| Memória e organização | Obsidian (Cérebro Tutorial Pet), Notion (ref.), Telegram (aviso), inventário no Desktop | Cofre · Suporte |
| Skills externas (MIT) | marketingskills (social, ad-creative, offers, ads, copywriting, psychology, video), openclaudia (facebook-ads, video-ad-analysis, write-landing, content-calendar, social-content), upload-post (comment-funnel, viraloop) | motor dos agentes |
| Habilidades próprias | análise de referência viral, decisão de anúncios Meta, ganchos e cadência, controle de prova real, criativo low ticket, decifrador de algoritmo, entrega direta, Jev decisão rápida, oferta low ticket, painel central de achados, registro de falhas, verificar antes de pedir | motor dos agentes |
| Diretores (4) | Audiência e Redes · Produto e Receita · Conteúdo e Blog · Operação e Qualidade | cada departamento tem 1 diretor que decide |

Tudo isso entra no painel como "conexões" (ligadas pela conta existente do cliente, por OAuth) e
como motores invisíveis por trás dos botões. O cliente nunca precisa saber o nome da ferramenta.

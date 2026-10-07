# Elenco de agentes da fábrica Tutorial Pet (atualizado 06/10/2026)

Legenda: **PRONTO** = código testado localmente · **PARCIAL** = funciona com limite descrito · **ESPECIFICADO** = só a definição, falta construir.

## Já existiam (01–17)
Pesquisa de nicho, caçador de tendências, escritor, editor de qualidade, SEO, compliance, publicador do blog,
analytics, monetização, guardião de política, supervisor, social/produtos, visual, publicador do Facebook, vídeo.

## Novos (18–23) — 18 a 22 criados em 06/10/2026, 23 em 07/10/2026
| # | Agente | Estado | O que faz | Limite honesto |
|---|---|---|---|---|
| 18 | Saúde da Fábrica | **PRONTO** | Confere o pacote do dia (arquivos, duração e áudio do vídeo, links do produto e do artigo na legenda, fila de temas, chaves). Falha o workflow e abre issue no GitHub. | Link do produto no começo do artigo é só AVISO até o escritor aplicar a regra. |
| 19 | Validador de Temas | **PARCIAL** | Mostra o estoque da fila e repõe temas via LLM, recusando duplicata, diagnóstico/dose, termo curto, pilar inventado. | A reposição com LLM depende da `GEMINI_API_KEY`; a parte de validação foi testada, a chamada ao LLM não. Não roda sozinho ainda no workflow. |
| 20 | Roteirista da Duda + Diretor (por regras) | **PARCIAL** | Gera a fala da Duda (com tags do ElevenLabs e versão simples), valida tom/tamanho/credencial, alterna a estrutura do vídeo. Personalidade em `config/duda.yaml`. | Modo por regras às vezes repete uma ideia; `--llm` reescreve melhor mas não foi testado. Ainda não está ligado ao `fabrica_nuvem.py`. |
| 21 | Publicador de Vídeo | **PARCIAL** | Monta o pedido do Metricool (IG Reel + FB Reel), respeitando 2 posts/dia (12h e 20h) e só para pacote `aprovado`; não duplica. | **Não envia.** O envio segue sendo feito por sessão do Claude com o conector do Metricool até existir token de API. |
| 22 | Guardião de Gasto | **PRONTO** | Confere o rascunho da campanha da Meta contra `config/regras_gasto.yaml` (posicionamento manual só FB/IG, sem Audience Network, teto R$ 12/dia, pixel, conta, país, erro de pagamento). | Lê o rascunho em YAML; não consulta a Meta sozinho. |
| 23 | Acelerador de Processos | **PARCIAL** | Recebe uma ferramenta, oferta ou gargalo e diz qual etapa de `config/mapa_processo.yaml` ela acelera, ganho, teste grátis, risco e veredito com data, sempre lembrando o foco. | Montagem do prompt testada; a chamada ao LLM não foi testada (depende da `GEMINI_API_KEY`). Só dá parecer, não compra nem mexe em conta. |

**Regra de alcance (06/10/2026):** link no texto do post derruba o alcance. O agente 21 separa a legenda: texto = gancho + hashtags; links (landing e artigo) = primeiro comentário. Link do produto = landing page, nunca o checkout direto.

## Ainda a construir (ESPECIFICADOS)
- **Diretor de Criativos completo:** usar o Banco de Referências de Vídeo (alimentado pelo Caçador, ter/sex 07:20) para escolher a estrutura por dado, não por rodízio.
- **Escritor de e-book + validador de tema de produto.**
- **Fábrica de App:** e-book → app Streamlit repetível.
- **Cadastrador Kiwify:** produto novo já com capa, categoria e Área de Membros.
- **Auditor de Anúncios:** lê resultado de campanha e recomenda.
- **Auditor de Processo:** registra erros, causa raiz e melhoria.
- **Escritores com vozes:** rodízio já existe em `config/vozes_cronistas.yaml`.

## Como o dia roda hoje
1. 06:00 (Fortaleza): `fabrica.yml` produz artigo + roteiro + vídeo → branch `media`.
2. O agente **18** confere; se falhar, o workflow fica vermelho e abre uma issue.
3. Revisão e aprovação (manifest `aprovado`) → agente **21** gera o pedido → agendamento no Metricool.
4. Campanha paga: agente **22** antes de publicar.

# Livro de Execução de Decisões (fonte única: decidiu = entra aqui = vira tarefa com dono e prazo)
Regra (Allan, 16/10/2026): decidiu, vai fazer. Nenhuma decisão fica só na conversa ou no Painel.
Status: decidido -> em execução -> feito (com evidência) | bloqueado (só o Allan; diz o passo exato).
Quem roda: o Executor de Decisões (nuvem, diário 06:53 Fortaleza). Dono "Allan" só para login, 2FA, compra, identidade.

| ID | decidido em | decisão | ação executável | dono | prazo | status | evidência |
|---|---|---|---|---|---|---|---|
| D01 | 16/10 | Produto pronto/validado vai ao Painel (comprar x produzir) | atualizar prompt da Triagem | nuvem | 16/10 | feito | trig_017jLDcRvUayL3a8s7jSYxqB atualizado; commit dbdac67 |
| D02 | 16/10 | Criar Importador Internacional (EUA/LatAm/Espanha) | criar rotina semanal (ter/sex 09:xx) que busca ofertas prontas com prova de venda e grava em data/oportunidades/decisoes.md; usa prompt de config/prompts/cacador_oportunidades.md passos 7-9 | nuvem | 19/10 | decidido | |
| D03 | 16/10 | Atualizar Caçador de ofertas para espelhar | tirar Metricool/TikTok pausado do prompt; gravar achados fortes em decisoes.md; PushNotification | nuvem | 19/10 | decidido | |
| D04 | 16/10 | Atualizar Caçador de atalhos | mesmo ajuste de D03 | nuvem | 19/10 | decidido | |
| D05 | 16/10 | Recriar Caçador de estilo viral com Zernio+Buffer | criar nova rotina, depois desligar a antiga | nuvem | 20/10 | decidido | |
| D06 | 16/10 | Recriar Agente de Segurança com Zernio+Buffer | idem | nuvem | 20/10 | decidido | |
| D07 | 16/10 | Substituir Caçador de referências (dependia do PC) por busca web | nova rotina sem PC; desligar a antiga | nuvem | 20/10 | decidido | |
| D08 | 16/10 | Fixar requirements do app e token ?k= | tarefa de 19/10 08:40 (trig_01UoDgJXvgCJCHiUG6ftvvyw) | nuvem | 19/10 | em execução | |
| D09 | 16/10 | Molde de novo negócio quando processo fechar | data/molde/ORDEM.md; gatilhos 23/10 e 30/10 | nuvem | 30/10 | em execução | |
| D10 | 16/10 | Veredito das 7 mudanças do Revisor | data/auditoria/mudancas.md em 23/10 | nuvem | 23/10 | em execução | |
| A01 | — | Reconectar Windsor.ai | só o Allan (login) | Allan | — | bloqueado | passo: conectar no claude.ai > Conectores |
| A02 | — | 2FA; chave ElevenLabs; verificação TikTok; produto Kiwify duplicado | só o Allan (login/identidade) | Allan | 23/10 | bloqueado | |
| E01 | 20/10 | Meme 8-12s vira 2 de cada 3 vídeos novos; explicador no máximo 1 em 3 | editar fila/config da fábrica (estilo_viral.yaml e prompt de roteiro) conforme data/social/plano_de_mudanca_2026-10-20.md | nuvem | 21/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 |
| E02 | 20/10 | Suspender slot de meme FB 12:00 / IG 13:00 em itens ainda NÃO agendados | tirar o slot do gerador de agenda; manter 08:30/21:00 FB e 08:40/21:10 IG; registrar em config/estrategia_social.yaml | nuvem | 21/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 |
| E03 | 20/10 | Remover 'link no perfil' das legendas TikTok geradas | editar config/prompts/publicador.md e agents/21_publicador_video/agent.py: usar 'Confira o artigo completo em tutorialpet.com.br' | nuvem | 21/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 |
| E04 | 20/10 | Teste B: meme 8s no TikTok 10:20 e 20:20 por 3 dias | enfileirar 6 memes 8s ainda não agendados no Buffer (teto 10 na fila); leitura em 24-48h | nuvem | 21/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 |
| E05 | 20/10 | Teste C: pergunta de uma palavra nos memes | ajustar prompt de legenda dos memes: última linha = escolha de 1 palavra + 1º comentário com o link do artigo | nuvem | 21/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 |
| E06 | 20/10 | Último segundo com UMA ação por formato (meme: comentar 1 palavra; erro 8s: salvar; voz do pet: compartilhar; dúvida: comentar número) | editar prompts de roteiro e legenda (config/prompts/humorista.md, publicador.md, agents/17_video) conforme data/social/campanha_organica_2026-10-20.md seção (b); CTA falado gira, ação não | nuvem | 21/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 (rodada extra 20/10) |
| E07 | 20/10 | Fila de produção segue as 4 séries e a grade de 14 dias (3 vídeos únicos/dia, 2 em 3 em 8 s) | cadastrar séries S1-S4 e ganchos em config/estrategia_social.yaml e ajustar a fila da fábrica só para itens NÃO agendados; repor fila TikTok (teto 10) todo dia | nuvem | 21/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 (rodada extra 20/10) |
| E08 | 20/10 | 1º comentário FB/IG = pergunta de 1 palavra + link com UTM | ajustar Publicador para enviar firstComment no padrão da seção (b); fixar (pin) fica manual | nuvem | 21/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 (rodada extra 20/10) |
| E09 | 20/10 | Atendente 3 execuções/dia na campanha, só PROPÕE respostas até o Allan autorizar publicar | atualizar agenda/prompt da rotina Atendente (08:50, 14:50, 21:50), incluir respostas-modelo e métrica tempo até 1ª resposta | nuvem | 21/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 (rodada extra 20/10) |
| E10 | 20/10 | Medição da campanha e amostra limpa | Estrategista diário lê metas da seção (e), exclui os 4 TikToks sem emoção da amostra de formato, registra leituras 22/10, 24/10, 27/10, 03/11 e veredito de anúncio 04/11 | nuvem | 04/11 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 (rodada extra 20/10) |
| E11 | 20/10 | Lista de páginas pet BR do mesmo porte para o Allan aprovar | pesquisa web gratuita; gravar data/social/paginas_para_interagir.md (nome, link, seguidores, tipo de conteúdo); ninguém é contatado | nuvem | 22/10 | decidido | origem: Estrategista, autorização permanente do Allan de 16/10/2026 (rodada extra 20/10) |

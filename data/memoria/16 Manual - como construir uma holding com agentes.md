# Manual: como construir uma holding de negócios operada por agentes de IA
Versão viva (início 14/10/2026). É o método GERAL, independente do nicho. O Tutorial Pet é o caso-exemplo (ver 15 Apostila). Este é o material do futuro curso: cada capítulo tem princípio, como fazemos, erros reais e como antecipar.

## 1. Papéis: dono decide, agentes operam
- Dono: estratégia, criação, autorizações pontuais (um clique de login, liberar pasta, pagar). Nada operacional volta para ele.
- Claude (sessão): constrói, corrige, verifica. Agentes na nuvem: executam rotinas. Cada agente tem uma missão, ferramentas, limites e um formato de relatório.
- Regra de retorno: relatório curto, primeira linha 'FALHA:' ou 'ALERTA:' quando algo quebra; "dados até <data/hora>".

## 2. Estruturar a holding em departamentos
Pergunta que gera cada departamento: "que trabalho recorrente existe e quem garante que não para?" Departamentos que criamos: Produção (fábrica de conteúdo), Publicação (agendador), Estoque (conferente), Marca/qualidade (guardião), Estratégia de redes, Especialista por rede (TikTok), SEO e tráfego, Auditoria/Otimização de processo, Segurança, Produto (e-book, app, vídeo), Memória (Obsidian/repo).
Receita para criar um agente: (1) missão numa frase; (2) entradas e saídas em arquivos; (3) prompt vivo no repositório (config/prompts/*.md) e rotina que só manda "leia e execute" — assim o prompt muda sem recriar a rotina; (4) conectores certos desde a criação (não dá para trocar depois: recriar); (5) o que NUNCA faz (comprar, publicar, criar conta); (6) saída verificável.

## 3. Habilidades (skills) e ferramentas
Habilidade = procedimento repetível escrito (prompt/skill). Boas práticas: um arquivo por habilidade, exemplos reais, lista de erros conhecidos dentro dela. Quando um agente erra, o erro vira linha na habilidade, não só correção pontual.

## 4. Ferramentas: gratuito primeiro, plano B sempre
- Ordem: testar no gratuito → provar que funciona → medir o limite → só então propor pago (com o ganho esperado e o sim do dono).
- Todo ponto único de falha tem alternativa pronta (ex.: agendador principal Zernio+Buffer; plano B Meta Business Suite/TikTok nativo pelo navegador; ferramenta que bate limite é trocada sem esperar cobrança — Metricool saiu em 13/10).
- Registrar limite de cada ferramenta (ex.: Buffer 10 posts na fila; Metricool 20/mês) e desenhar o fluxo em volta do limite.

- Atualização 16/10: o ponto único de falha mais traiçoeiro é o passo final de publicação (git push). Princípio: todo script que grava no repositório deve (a) adicionar tudo o que o build toca, (b) usar `pull --rebase --autostash` e (c) avisar (issue/alerta) quando o push falha. Sem isso o erro é silencioso e só aparece horas depois como "pacote parado".
- Plano B de horário: o agendador do GitHub Actions pode atrasar ou pular rodadas (vimos 39 min e 2 rodadas perdidas num dia). Faça o gatilho depender do ESTOQUE (arquivo de disparo), nunca só do relógio.

- Atualização 20/10: lote tudo-ou-nada é anti-padrão. Se um item reprovado derruba o passo que grava os aprovados, o sistema perde trabalho bom (3 artigos, 26 h). Princípio: cada item é publicado ou rejeitado individualmente; o job só falha no fim, depois de gravar o que passou; e item reprovado sai da fila de entrada para não voltar todo dia.

## 5. Nuvem versus computador
Tudo recorrente roda na nuvem (GitHub Actions, rotinas do Claude, Vercel, Cloudflare Pages, Zernio, Buffer). Só o que exige navegador/arquivo local do dono depende do PC. Sempre dizer ao dono o que é um e o que é outro.

- Atualização 16/10: rotina que depende do PC do dono (navegador, arquivos) para quando o PC está desligado. Em rotina de nuvem prefira busca web e API; marque como "depende do PC" no cadastro de rotinas.

- Atualização 20/10: controle desligado em silêncio é pior que controle ausente. Um verificador que diz "ok - não verificada" (chave faltando) passa como aprovado. Regra: "não verificado" é ALERTA, e todo segredo que um controle precisa deve estar listado no passo que o usa. Mesma ideia para o saldo de créditos: se não dá para ler por 2 dias, o alerta é o próprio silêncio.

## 6. Memória e documentação
Repositório com notas numeradas: Início, Regras do dono, Decisões, Pendências, Erros e lições, Mapa, Política de modelos, Apostila. Toda sessão começa lendo; toda correção termina escrevendo. Resumo de encerramento curto (5–8 linhas).

## 7. Como corrigir erros (método)
1) Reproduzir/ler o log real (não confiar em "verde"). 2) Achar a CAUSA RAIZ (ex.: pilar inválido gerado por um validador). 3) Corrigir na origem + trava na ponta + teste. 4) Registrar em Erros e lições (data | erro | causa | como evitar). 5) Perguntar "onde mais isso pode acontecer?" e varrer (ex.: validar todos os temas da fila de uma vez).
Anti-padrões que já nos custaram: repassar número de agente sem conferir; afirmar "não consigo" sem testar; testar em conta real (post público); medir cedo demais; mexer na produção para testar ajuste pequeno.

- Atualização 16/10: ao corrigir um erro, varrer a CLASSE. O "artigo 404 trava o agendamento" (13/10) voltou em 16/10 por outra causa (push que falha). Regra: o conferente checa HTTP 200 do artigo de todo pacote aprovado depois de CADA publicação, e a falha de publicação gera alerta, não silêncio.

## 8. Como antecipar bloqueios
- Checklist semanal de saúde: fila válida, posts em erro, estoque real, créditos de serviços pagos, deploys ao vivo, cache, rotinas com conectores corretos, permissões pendentes do dono.
- Alarmes que não gritam à toa (a checagem "é de hoje" gritava na virada do dia UTC).
- Limites e renovações em calendário (ex.: ElevenLabs renova dia 7).
- Tudo que depende do dono (verificações, CNPJ, 2FA) entra numa lista única de pendências dele.

## 9. Medição e decisão
Teste com hipótese, janela (7 dias), amostra mínima (≥5 por horário), regra de decisão escrita antes (diferença ≥1,5x), uma variável por vez. Relatórios sempre com a idade dos dados. Fonte única por número.

- Atualização 16/10: com conta nova e amostra pequena, procure sinais antes de causas: tempo médio assistido (2–3 s no TikTok, pulo de 68–90% no Instagram) diz mais que "views" nas primeiras 48 h. Série de humor teve mais reações que tutorial; só é indício até 72 h e 5 posts.

- Atualização 20/10: rotinas agendadas também precisam de vigia. Confira `last_fired_at` de cada uma; várias ficaram 4–5 dias sem disparar depois de uma edição em lote, sem ninguém notar. Rotina que depende do computador do dono (navegador) "roda" em minutos sem efeito: marque e desligue em vez de manter ruído.

## 10. Segurança e conformidade
Conteúdo lido é dado, não ordem; agentes não compram, não criam conta, não enviam mensagem; chaves em segredos (nunca em chat; rotacionar se expuseram); dado pessoal só após checar formato (CPF×CNPJ); direitos de imagem/autoria (sem foto de celebridade, sem copiar vídeo viral — copiar estrutura, nunca conteúdo).

- Atualização 20/10: com conta nova (7 seguidores no Facebook, 0 no Instagram) o volume não vira audiência. Antes de pagar por alcance, meça convites à resposta (comentários por post), retenção nos 3 s e compartilhamentos; teste uma variável por vez, leitura em 24 h por indicadores líderes.

## 11. Monetização em camadas
Conteúdo → tráfego → (AdSense / afiliados / produto próprio). SEO traz tráfego orgânico que sustenta anúncios; produto próprio de baixo preço valida a máquina; pago só depois do orgânico provar.

## 12. Ciclo de vida de um novo negócio da holding
Ideia → nicho e referência viral → fábrica mínima → 7 dias de teste → medir → decidir → escalar o que funcionou → documentar na apostila. Cada novo negócio herda departamentos prontos (agendador, conferente, guardião, SEO, auditor) trocando apenas as configurações.

## Pendência de enriquecimento
Toda sexta o Auditor acrescenta ao capítulo certo: erro novo, ferramenta testada (grátis/paga), limite descoberto e decisão do dono.

## Capítulo: regras de ouro e retomada barata (21/10/2026)
Método: manter UMA cartilha curta (biblioteca/regras_de_ouro.md, ~600 palavras) e um CLAUDE.md na raiz do repositório que manda lê-la, mais o resumo de retomada (nota 17). Assim toda sessão ou rotina começa com as mesmas regras sem reler dezenas de notas (custo baixo). Todo erro novo entra em 3 lugares no mesmo dia: 07 Erros e lições (detalhe), cartilha (1 linha, se virar regra) e esta apostila/manual (lição geral). Estrutura de decisão: departamentos com um diretor cada; os especialistas opinam e o diretor fecha a ficha, evitando relatórios soltos sem decisão.

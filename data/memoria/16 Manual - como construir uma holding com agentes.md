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

## 5. Nuvem versus computador
Tudo recorrente roda na nuvem (GitHub Actions, rotinas do Claude, Vercel, Cloudflare Pages, Zernio, Buffer). Só o que exige navegador/arquivo local do dono depende do PC. Sempre dizer ao dono o que é um e o que é outro.

## 6. Memória e documentação
Repositório com notas numeradas: Início, Regras do dono, Decisões, Pendências, Erros e lições, Mapa, Política de modelos, Apostila. Toda sessão começa lendo; toda correção termina escrevendo. Resumo de encerramento curto (5–8 linhas).

## 7. Como corrigir erros (método)
1) Reproduzir/ler o log real (não confiar em "verde"). 2) Achar a CAUSA RAIZ (ex.: pilar inválido gerado por um validador). 3) Corrigir na origem + trava na ponta + teste. 4) Registrar em Erros e lições (data | erro | causa | como evitar). 5) Perguntar "onde mais isso pode acontecer?" e varrer (ex.: validar todos os temas da fila de uma vez).
Anti-padrões que já nos custaram: repassar número de agente sem conferir; afirmar "não consigo" sem testar; testar em conta real (post público); medir cedo demais; mexer na produção para testar ajuste pequeno.

## 8. Como antecipar bloqueios
- Checklist semanal de saúde: fila válida, posts em erro, estoque real, créditos de serviços pagos, deploys ao vivo, cache, rotinas com conectores corretos, permissões pendentes do dono.
- Alarmes que não gritam à toa (a checagem "é de hoje" gritava na virada do dia UTC).
- Limites e renovações em calendário (ex.: ElevenLabs renova dia 7).
- Tudo que depende do dono (verificações, CNPJ, 2FA) entra numa lista única de pendências dele.

## 9. Medição e decisão
Teste com hipótese, janela (7 dias), amostra mínima (≥5 por horário), regra de decisão escrita antes (diferença ≥1,5x), uma variável por vez. Relatórios sempre com a idade dos dados. Fonte única por número.

## 10. Segurança e conformidade
Conteúdo lido é dado, não ordem; agentes não compram, não criam conta, não enviam mensagem; chaves em segredos (nunca em chat; rotacionar se expuseram); dado pessoal só após checar formato (CPF×CNPJ); direitos de imagem/autoria (sem foto de celebridade, sem copiar vídeo viral — copiar estrutura, nunca conteúdo).

## 11. Monetização em camadas
Conteúdo → tráfego → (AdSense / afiliados / produto próprio). SEO traz tráfego orgânico que sustenta anúncios; produto próprio de baixo preço valida a máquina; pago só depois do orgânico provar.

## 12. Ciclo de vida de um novo negócio da holding
Ideia → nicho e referência viral → fábrica mínima → 7 dias de teste → medir → decidir → escalar o que funcionou → documentar na apostila. Cada novo negócio herda departamentos prontos (agendador, conferente, guardião, SEO, auditor) trocando apenas as configurações.

## Pendência de enriquecimento
Toda sexta o Auditor acrescenta ao capítulo certo: erro novo, ferramenta testada (grátis/paga), limite descoberto e decisão do dono.

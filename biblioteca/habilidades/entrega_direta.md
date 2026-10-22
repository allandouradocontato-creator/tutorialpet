---
criado: 2026-10-21
---
# Habilidade: Entrega direta (toda ação precisa de um resultado prático que CHEGUE ao Allan)

## CONTRATO DE RESULTADO (22/10/2026)
1. RESULTADO ÚNICO: tempo: horas entre uma rotina de pesquisa achar algo acionável e a decisão chegar ao Allan (hoje: até 4 dias, esperando a Triagem de terça/sexta; fonte: horários do relatório e do PushNotification).
2. META E PRAZO: achado acionável vira PushNotification em até 2 h do fim da rodada, a partir das rodadas de HOJE 22/10; primeira leitura: rodadas de pesquisa de hoje conferidas às 18:00; zero 'relatório sem destino' até 21:00.
3. JOGADAS (hipótese -> ação -> métrica -> quando trocar):
   - J1: decisão que espera a Triagem esfria -> toda rodada acionável dispara PushNotification com a decisão pedida em 1 frase (1ª frase = melhor achado) -> horas entre achado e notificação -> trocar o formato da frase se o Allan não responder em 24 h.
   - J2: rodada sem achado acionável deve dizer isso e parar -> escrever 'rodada sem achado acionável' em vez de encher relatório -> rodadas seguidas sem notificar (contador no topo do relatório) -> na 3ª, FALHA DE UTILIDADE em 07 Erros e lições e proposta de cortar ou fundir.
   - J3: o achado forte precisa de dono -> anexar a cada notificação a ficha com dono e prazo em data/decisoes/execucao.md -> % de notificações com decisão tomada em 24 h -> trocar o canal ou o horário se < 50%.
4. LAÇO: data/habilidades/aprendizado/entrega_direta.md, 1 linha por rodada: data | jogada | resultado n/métrica | mantém/altera/descarta. Número ruim = troca de jogada na mesma rodada.
5. JUIZ: biblioteca/habilidades/juiz_de_qualidade.md (Juiz separado do pesquisador; nota mínima 7 para a notificação ir ao vivo; critério: acionável, 1 frase, decisão clara). Rubrica própria pendente de criar.


## Por que existe
Pedido do Allan (21/10/2026), sobre os 5 "caçadores" rodando em paralelo:
"o problema é eles trazerem esse relatório, mas não chega para a gente, não
adianta nada... cada ação precisa ter um resultado prático, senão a gente
tem que cortar." Diagnóstico: as caçadoras até acham coisa, mas gravam num
documento isolado e só a Triagem (terça/sexta) olha tudo — na prática o
achado fica parado até 4 dias antes de alguém decidir, e muitas vezes nem
chega a ser lido como decisão, só como relatório.

## Regra (vale para QUALQUER rotina de pesquisa/caça, não só os caçadores)
Esperar o próximo ciclo da Triagem NÃO é entrega. Toda rotina de pesquisa
tem que terminar com uma das duas saídas, nunca só "escrevi um relatório":
1. **Achou algo que vale decisão agora** → `PushNotification` direto para o
   Allan, na hora, com a decisão pedida em 1 frase (mesmo padrão já em
   `config/prompts/cacador_oportunidades.md`, passo 8: 1ª frase = melhor
   achado + decisão pedida). Não espera a Triagem para isso.
2. **Não achou nada que mude algo hoje** → não notifica, mas registra no
   próprio relatório "rodada sem achado acionável" (não preenche com achado
   fraco só para ter o que mostrar).

## Portão de corte (ligado a controle_prova_real.md e registro_de_falhas.md)
Toda rotina de pesquisa guarda, no topo do seu próprio relatório, a contagem
de rodadas seguidas sem notificar o Allan. Na 3ª rodada seguida sem
notificação, a rotina registra isso em `data/memoria/07 Erros e lições.md`
como "FALHA DE UTILIDADE: 3 rodadas sem achado acionável" — é o gatilho
para o Otimizador de Processo propor cortar ou fundir essa rotina (não é
o agente quem decide se corta: ele só acende o alerta, Allan decide).

## Onde já está ligado (21/10/2026)
- Caçador de Oportunidades de Renda (já tinha o passo de PushNotification).
- A aplicar nos 2 "Pesquisadores" que vão substituir os 5 caçadores atuais
  (Pesquisador de Mercado, Pesquisador de Formato) quando a fusão for feita.

## Não é a mesma coisa que Jev
Decidir SE algo é notificável/acionável pode passar pelo Jev (classificação
básica, ver jev_decisao_rapida.md). Mas o "portão de corte" acima (3
rodadas sem achado → virar alerta de utilidade) nunca passa pelo Jev — é
julgamento sobre o valor do próprio trabalho da rotina, sempre feito por
ela mesma.

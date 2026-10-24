# Fluxo do mimo, FASE 1 (rascunho; criado 21/10/2026 a pedido do Allan)
Objetivo (decisão do Allan, 21/10 15:10): criar audiência real. O mimo é entregue por DM; o fluxo guarda dados do PET para segmentar depois. O mimo em si (nome, conteúdo, arte) vem da concepção do Fable; este fluxo só precisa do arquivo/link final.
Canal: Instagram agora (gatilho por comentário). TikTok: só gatilho por DM. Facebook: a conectar. Nada vai ao ar sem o mimo pronto e sem o ok do Allan.

## Regras
- Dados do PET, não da pessoa: nome do cão/gato, espécie, raça (opcional), idade/fase (filhote, adulto, idoso), horas sozinho por dia. Não pedir nome, idade nem e-mail da pessoa no 1º contato.
- Público-alvo é o tutor adulto. Crianças e adolescentes podem curtir o mimo, mas o fluxo não coleta dado pessoal deles. E-mail (Brevo) só como passo opcional, com texto "se você é maior de 18 anos".
- Sem alegação médica ou veterinária; sem promessa de resultado.
- Mecânica de seguidor real: avaliar "Follow to DM" do ManyChat (seguir a página para receber). Nada de seguidor comprado nem engajamento falso.

## Roteiro de mensagens (texto-base; ajustar ao tom da Duda)
1. Comentou a palavra-gatilho -> resposta pública curta + DM: "Oi! Eu sou a Duda, do Tutorial Pet. Seu mimo tá quase pronto! Me conta rapidinho sobre o seu pet?"
2. Pergunta 1 (texto livre, campo nome_pet): "Qual o nome do seu pet?"
3. Pergunta 2 (botões, campo especie): "É cachorro ou gato?"
4. Pergunta 3 (botões, campo fase): "Filhote, adulto ou idoso?"
5. Pergunta 4 (texto livre ou botões, campo raca): "Qual a raça? (se for SRD/vira-lata, pode dizer SRD)"
6. Pergunta 5 (botões, campo horas_sozinho): "Quantas horas por dia o(a) {nome_pet} fica sozinho(a)? Menos de 2 / 2 a 4 / 4 a 8 / mais de 8"
7. Entrega: "Prontinho! Aqui está o mimo do(a) {nome_pet}: {link}". Depois: convite para seguir a página (se não usar Follow to DM) e para postar o mimo marcando a página.
8. Segmentação (nos bastidores): horas_sozinho >= 4 recebe depois, em outra mensagem, o conteúdo ligado ao Sozinho em Casa (não vender na mesma hora do mimo).
9. (E59, RASCUNHO, NÃO ATIVAR sem ok escrito do Allan) Mensagem 2, só horas_sozinho >= 4, 1 a 2 dias após a entrega: "Oi! Aqui é a Duda, assistente virtual do Tutorial Pet 🐾 Você contou que o(a) {nome_pet} fica {horas_sozinho} por dia sozinho(a). Se quiser, tenho um plano de 14 dias pra ele(a) ir se acostumando aos poucos: sozinho.tutorialpet.com.br (R$ 27, pagamento único). Sem pressa, se não fizer sentido agora é só ignorar." Link com ?utm_source=manychat&utm_medium=mimo. Fonte: data/departamentos/fichas/2026-10-23_prioridade_receita_semana.md.

## Campos do contato a criar no ManyChat
nome_pet (texto), especie (texto), fase (texto), raca (texto), horas_sozinho (texto), origem_mimo (texto, ex.: ig_comentario, tt_dm).

## Pendências
- Mimo final (concepção do Fable) e o link/arquivo de entrega (PDF imprimível hospedado em domínio da marca, nunca vercel.app).
- Palavra-gatilho nova (a atual, GUIA, é da isca antiga).
- Conectar Facebook (autorização do Allan) e conferir Follow to DM no plano gratuito.

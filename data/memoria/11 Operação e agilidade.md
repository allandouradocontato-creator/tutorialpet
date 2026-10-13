# Operação e agilidade (alimenta o Otimizador de Processo)
Atualizado em 13/10/2026. Papel do Allan: SÓ decisões estratégicas e de criação. Toda burocracia (uploads, cadastros, trocas de arquivo, configurações em plataformas) é executada por Claude/agentes; ao Allan sobram só autorizações pontuais (um clique de login, liberar pasta). O Otimizador deve medir quantas vezes o Allan teve que executar algo manual e propor como zerar isso.

## O que foi feito em 13/10/2026 (pedido do Allan)
- Fábrica fechada: 5 artigos publicados (ração filhote, brinquedos interativos, enxoval gatinho, escovar dentes, comedouro gato); 10 vídeos agendados 5 dias à frente; lote antecipado disparado.
- Agendamento trocou do Metricool (limite de 20 posts/mês estourado) para Zernio (Facebook + Instagram, com primeiro comentário) + Buffer (TikTok). Rotina Agendador de Posts (Zernio + Buffer) às 08:15 e 15:15; Conferente de Estoque às 07:47 (vídeo e artigos, mínimo 5 dias à frente).
- Produto Sozinho em Casa otimizado por referências: app redesenhado, novo e-book de 53 páginas (Parte 1 Manual, Parte 2 Fundamentação, fotos sem repetição, capa C), landing com capa nova, texto "baseado em evidências" (nunca "comprovado").
- E-book e capa trocados na Kiwify pelo próprio Claude (ver passo a passo abaixo).

## Como trocar arquivo na Kiwify sem o Allan
- Navegador embutido do app já fica logado na Kiwify; o Chrome do PC pode pedir login (só 1 clique do Allan em "Entrar", senha é preenchida pelo Chrome).
- Produto certo: o do checkout pay.kiwify.com.br/NcQChat (existe um duplicado com checkout 3JprCCK, ainda não tratado).
- Arquivo local não sobe por clique (janela do Windows) nem por file_upload (pasta fora da lista permitida). Solução que funcionou: copiar o arquivo para um endereço temporário aleatório na landing (com cabeçalho CORS), injetar no input de arquivo da página por script (o Allan autorizou), e apagar o endereço logo depois.
- Imagem do produto: Produtos > editar > Geral > Remover imagem > novo arquivo > Salvar produto. PDF: Área de Membros > editar conteúdo > Anexos (anexar o novo primeiro, depois apagar o antigo) > Salvar alterações.

## Ideias para ficar mais ágil (o Otimizador avalia e dá veredito)
1. Lacuna de dados: o Otimizador só tem Metricool; os posts agora saem por Zernio e Buffer. Ele precisa de leitura de Zernio (analytics) e Buffer para medir de verdade. Hoje a rotina dele não tem esses conectores e a configuração de conectores não muda por atualização; recriar a rotina com Zernio e Buffer, ou o Conferente passar um resumo.
2. Upload sem fricção: criar um passo padrão "publicar arquivo temporário e injetar" (script pronto no repositório) para qualquer plataforma que exija arquivo local; assim nenhum upload volta para o Allan.
3. Pasta Downloads do PC do Allan já liberada para esta sessão; manter uma pasta de entrega fixa autorizada evita novo pedido.
4. Produto duplicado na Kiwify: conferir vendas/acessos e desativar o que sobrar, sem exigir tempo dele.
5. Medir por rodada: quantas ações manuais foram devolvidas ao Allan (meta: zero, só autorizações).

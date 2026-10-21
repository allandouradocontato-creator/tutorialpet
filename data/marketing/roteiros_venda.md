Dados até 2026-10-21 09:42 (Fortaleza). Zernio (sync 08:26, 70 posts, Facebook) + relatório TikTok/Buffer de 19/10 08:20 (mais novo disponível). Só roteiros: nada gerado, publicado ou comprado.

## Número do departamento (views por gancho → cliques na landing)
- Views por gancho (72h+): pergunta de dor cotidiana lidera. FB: "Seu gato quase não bebe água da tigela?" 1.014 views; "Seu gato anda evitando a caixa de areia?" 311; "Seu cachorro aguenta quantas horas sozinho?" 362. TikTok: banho 998; "Para de ignorar esse sinal" 747.
- Cliques na landing: SEM DADO. data/landing/metricas.csv está vazio e as legendas antigas não levam UTM; Zernio mostra só 0-6 cliques por post FB. Vendas atribuídas: sem dado (Kiwify sem acesso).

## O que já funciona e como replicar
Pergunta curta de um problema concreto do dia a dia, sem alarme, que a pessoa reconhece em 3 s (banho→cheiro, gato→água). Replicado aqui para a dor do Sozinho em Casa ("chora quando fecha a porta", "segue até o banheiro", "faz festa na saída"). Ressalva: o molde sozinho não repete o campeão (banho repetido 199 vs 998); o tema precisa ser novo, então 1 gancho por vídeo.

## Roteiros (JSON em data/social/roteiros, prontos para a Fábrica; todos passam no Portão da Duda)
1. venda-dor-porta-20s (pergunta de dor, 20 s). Gancho: "Seu cachorro chora quando você fecha a porta?" Texto na tela: o gancho; "Começa com 2 minutos"; "14 dias · R$ 9,90". CTA: "Busca sozinho.tutorialpet.com.br. Aqui é a Duda, do Tutorial Pet." UTM content=dor-porta.
2. Série em 3 partes (15-20 s cada; 1 passo + convite a seguir; a 3ª vende):
   - venda-serie-1-sinal: "Seu cachorro te segue até o banheiro e chora na porta?" Passo 1: sair 2 min, voltar sem festa. CTA: seguir.
   - venda-serie-2-despedida: "Você faz festa na hora de sair de casa?" Passo 2: sair sem falar nada. CTA: seguir.
   - venda-serie-3-protocolo: "E se existisse um plano de catorze dias para ele ficar sozinho com calma?" Oferta + app_demo + R$ 9,90. CTA: busca o site.
   UTM content=serie-1-sinal / serie-2-despedida / serie-3-protocolo. Postar em dias seguidos, mesma hora (teste T2 do TikTok).
3. venda-demo-app-20s (demonstração do app, SEM depoimento): "Como saber se o treino de ficar sozinho está funcionando?" Mostra assets/vsl/app_demo.mp4 + garantia. UTM content=demo-app. Legenda diz que é o app real.
4. venda-vsl-75s-v3 (VSL para a landing, ~75 s): dor (vizinho) → troca de culpa → protocolo 14 dias → 3 fases → "começa com 2 minutos" → manual+app, de R$ 37 por R$ 9,90 → garantia 7 dias → CTA. Fala com ~840 caracteres (acima do teto de 420 do vídeo curto; o VSL anterior também passava: confirmar que a Fábrica aceita). UTM source=tutorialpet, content=vsl-v3.

UTM padrão (TikTok/Reels): ?utm_source=tiktok&utm_medium=video&utm_campaign=sozinho_venda&utm_content=<slug>. Sem "link na bio" (link no perfil não confirmado): CTA falado "Busca sozinho.tutorialpet.com.br".

## Regras cumpridas
Sem promessa de cura/resultado; sem depoimento inventado; sem preço por dia/mês (só "R$ 9,90 pagamento único"); legenda com "Material educativo; não substitui o veterinário"; tags de emoção da Duda e assinatura em todos.

## Habilidade que falta e teste grátis
Falta medir clique→venda: legenda sem UTM e métricas.csv vazio. Teste: usar só estes links com UTM por 4 rodadas e preencher metricas.csv com visitas por utm_content + vendas do Kiwify. Meta: 1 venda atribuída.

## Decisão do Allan
1. PREÇO: config/vsl/roteiro_vsl_v2 e vsl-sozinho-75s.json citam R$ 27; produto e landing dizem R$ 9,90. Usei R$ 9,90 (de R$ 37). Confirmar.
2. A série vai para a fila do TikTok (T2 pendente desde 19/10)? Roteiros só entram na Fábrica com OK dele.

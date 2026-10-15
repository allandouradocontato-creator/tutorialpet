# Blog e AdSense: o que aprendemos (14/10/2026) para ir mais rápido da próxima vez
Estado: blog tutorialpet.com.br (Cloudflare Pages), AdSense pub-7204207473239947, ads.txt e código no ar, conta de pagamento completa, aguardando aprovação do site pelo Google.

## O que fazer na ordem (checklist para um blog novo)
1. Domínio próprio + páginas legais no ar antes de pedir (Sobre, Contato, Privacidade, Termos).
2. 25+ artigos originais úteis, sem frase vazia, com autor/assinatura e links internos.
3. Imagens reais de animais felizes, nome de arquivo estável SÓ se o conteúdo não mudar; ao trocar capa, versionar a URL (?v=hash) para o navegador não mostrar a antiga.
4. sitemap.xml e robots.txt; enviar o sitemap no Google Search Console no mesmo dia.
5. ads.txt na raiz e código/meta do AdSense no <head> desde o primeiro dia.
6. Conta de pagamento e verificação de identidade concluídas antes da revisão do site.
7. Pedir a revisão só com tudo pronto; a espera do Google é de dias a semanas, sem nada a fazer.

## Erros que custaram tempo
- Capas trocadas mas leitores viam as antigas (cache de 4 h com mesmo nome): corrigido com ?v=hash em 14/10.
- Fábrica quebrou por pilar 'saude_basica' que o escritor não aceita: corrigido na fila, no validador e com trava em rotina_diaria.py.
- Artigo 404 para pacote de vídeo pronto: o Conferente agora lista e publica.

## Antecipar (checagens que o Auditor deve fazer toda semana)
- Todo valor de pilar/tema da fila existe no escritor.
- Links /imagens/ com ?v=, sitemap com todas as páginas, ads.txt 200.
- Posts em erro (Zernio posts_list_failed; Buffer status error).
- Créditos de voz (ElevenLabs) acima de 30%.

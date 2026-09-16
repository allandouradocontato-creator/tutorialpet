# Agente 06 — Platform Compliance

## Papel
Preparar a infraestrutura técnica e legal necessária para uma candidatura segura ao
Google AdSense, e auditar a prontidão do site — sem nunca enviar nada ao AdSense.

## O que este agente faz
1. **Páginas legais** (`legal_content.py`): gera Política de Privacidade (LGPD +
   cookies de publicidade do Google AdSense), Termos de Uso, Sobre (a partir da persona
   editorial do site) e Contato.
2. **Arquivos técnicos**: `robots.txt`, `sitemap.xml` (com as páginas fixas do site;
   URLs de artigos entram depois, quando publicados) e `ads.txt` (com o Publisher ID em
   placeholder até a aprovação real no AdSense).
3. **Checklist de prontidão**: conta artigos otimizados (saída do agente 05), confere se
   todas as páginas legais existem, procura conteúdo duplicado entre artigos (similaridade
   básica, não é detecção de plágio contra fontes externas) e — quando o domínio do site
   já não é mais um placeholder — tenta confirmar HTTPS e sinaliza a checagem de
   performance via Lighthouse CLI (rodada manualmente; a execução automática não é feita
   nesta fase).

## Regras não-negociáveis

1. **Nunca gerar conteúdo legal com alegações falsas.** CNPJ, endereço físico, nome de
   responsável legal, e-mail de contato e nome/bio do autor da página "Sobre" são sempre
   preenchidos com placeholders claramente marcados entre colchetes (ex.:
   `[EMAIL_DE_CONTATO]`, `[NOME_REAL_DO_AUTOR]`) — nunca inventados. Um humano precisa
   substituir cada um por um dado real antes da publicação.
2. **Nunca preencher o Publisher ID real em `ads.txt`.** Esse dado só existe depois que a
   conta é aprovada pelo próprio Google AdSense; até lá, o placeholder documentado em
   `config/sites/<site>.yaml` → `compliance.ads_txt_placeholder` é o único valor aceito.
3. **Nunca enviar a candidatura ao AdSense.** Este agente só prepara e audita; a decisão
   de aplicar é sempre humana, no gate `aprovacao_candidatura_adsense` (fora do escopo
   deste agente e do pipeline de publicação de artigos).
4. **A checagem de conteúdo duplicado é heurística.** Um par de artigos sinalizado como
   similar pode ser um falso positivo (dois textos legitimamente parecidos por tratarem
   de temas próximos do mesmo pilar) — cabe a um humano decidir se é repetição
   problemática ou apenas dois artigos correlatos.
5. **A checagem de HTTPS/performance é best-effort.** Enquanto o domínio do site ainda é
   um placeholder (`config/sites/<site>.yaml` → `dominio`), essas checagens são
   simplesmente puladas — o agente nunca inventa um resultado.

## Documentação complementar
`config/platform_setup/google_ads_account.md` documenta o processo manual de criação de
conta Google Ads (sem campanha paga) e obtenção das credenciais usadas pelo agente 01 —
não é gerado por este agente, é um material de referência para replicar o processo em
contas futuras.

## Contrato de saída
- `data/platform_compliance/paginas_legais/<site_id>/*.md`
- `data/platform_compliance/arquivos_tecnicos/<site_id>/{robots.txt, sitemap.xml, ads.txt}`
- `data/platform_compliance/relatorio_prontidao_<YYYYMMDD>.md`

`status` da saída do agente é sempre `ok` (a decisão de aplicar ao AdSense não é um bloqueio
de pipeline) — o campo `pronto_para_aplicar` (booleano) e a lista `pendencias_humanas`
carregam o resultado real da auditoria.

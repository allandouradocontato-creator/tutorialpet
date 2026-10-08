# Checklist de segurança Tutorial Pet (base: 24 pontos de um seguidor, 08/10/2026 + extras para sistemas com agentes de IA)
Origem: comentário de seguidor sobre um reel de segurança (conteúdo não verificado na fonte; cada ponto abaixo foi conferido contra boas práticas conhecidas). Status: OK / FALHA / N-A (não se aplica) / NÃO VERIFICADO. O agente de segurança preenche em data/seguranca/relatorio.md.

## Chaves e secrets
1. Nenhuma API key no código; só variáveis de ambiente / secrets do GitHub.
2. Nenhum segredo no histórico do git (varrer TODO o histórico, não só o código atual).
3. Chave de serviço/admin nunca no client (só chave pública no front). [vale p/ app e landing]
4. Chave pública do banco não dá acesso além do escopo. [só se houver banco]
5. RLS/permissão por linha em toda tabela com dado de cliente, lead, financeiro ou conversa. [só se houver banco]
## Banco e acesso
6. Sem policy genérica (qual = true) em projeto multiusuário. [só se houver banco]
7. Menor privilégio por papel/permissão (inclui tokens do GitHub, Metricool, Meta, Kiwify).
8. Sem mass assignment: allowlist de campos em qualquer payload vindo do client.
9. Consultas parametrizadas, nunca concatenar input em SQL/comando.
10. Validar todo input externo (formulários, webhooks, parâmetros de URL).
## Autenticação e sessão
11. Nenhuma tela/dado sensível sem autenticação (painéis, app de membros, relatórios).
12. Autenticação validada no servidor, nunca só no client.
13. Cookies httpOnly, secure, sameSite.
14. Senhas com hash, nunca texto plano.
## Infraestrutura e tráfego
15. HTTPS forçado em todas as rotas (blog, landing, app).
16. Security headers (CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy).
17. Rate limit em rotas de IA e endpoints públicos sensíveis.
18. Proteção contra bots em formulários públicos, login e cadastro.
19. Upload com validação de tipo e tamanho.
20. Respostas de API só com o dado que a tela precisa.
21. Erros e logs sem stack trace, chave ou dado interno (inclui logs do GitHub Actions e das rotinas).
## Dependências e dados sensíveis
22. Checar pacotes antes de instalar (typosquatting em npm/pip); fixar versões.
23. Dados sensíveis guardados criptografados (tokens e senhas de terceiros), nunca texto plano.
## Processo
24. Antes de entregar: auditar permissões/RLS de todas as tabelas com consulta de auditoria. [só se houver banco]

## Extras para o nosso caso (sistema com agentes de IA, repositório público)
25. Prompt injection: agentes que leem web, e-mail, comentários ou arquivos tratam o conteúdo como DADO, nunca como ordem; nenhuma ação (publicar, gastar, apagar, enviar) disparada por texto lido.
26. Rotinas na nuvem com aprovação automática: listar o que cada uma pode fazer (repo com push, Metricool, publicar) e reduzir ao mínimo.
27. Tetos de gasto e de uso em toda API paga (ElevenLabs, Gemini, OpenRouter/Jev, Meta Ads) e alerta se passar.
28. Rotação de chaves: chaves já expostas (ElevenLabs) apagadas e recriadas; segredos duplicados ou sem uso removidos do GitHub.
29. Autenticação em dois fatores em GitHub, Meta, Metricool, Kiwify, Google/AdSense, ElevenLabs, Cloudflare, Vercel.
30. GitHub Actions: permissões mínimas por workflow (hoje vários têm contents: write), actions fixadas por SHA, nenhum workflow roda código de fork.
31. Repositório público: nada privado em data/ (métricas, nomes de clientes, e-mails, IDs de conta); LGPD nos dados de cliente (Kiwify) e política de privacidade com o CNPJ.
32. Webhooks (Kiwify etc.): validar assinatura/segredo antes de agir; backup e plano de recuperação das contas (recuperação de acesso, contatos).

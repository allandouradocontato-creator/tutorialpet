"""Templates das páginas legais/institucionais geradas pelo agente 06.

Todo dado que não vem de uma fonte confiável do próprio projeto (CNPJ, endereço físico,
e-mail de contato, nome de responsável legal, nome do autor) é preenchido com um
placeholder entre colchetes — nunca inventado. Ver prompt.md para a regra completa.
"""
from __future__ import annotations

from datetime import datetime, timezone

PLACEHOLDER_EMAIL = "[EMAIL_DE_CONTATO]"
PLACEHOLDER_RESPONSAVEL = "[NOME_OU_RAZAO_SOCIAL_DO_RESPONSAVEL]"
PLACEHOLDER_DOC = "[CPF_OU_CNPJ_DO_RESPONSAVEL]"
PLACEHOLDER_ENDERECO = "[CIDADE_UF_DO_RESPONSAVEL]"
PLACEHOLDER_AUTOR_NOME = "[NOME_REAL_DO_AUTOR]"
PLACEHOLDER_AUTOR_BIO = "[BIO_REAL_E_VERIFICAVEL_DO_AUTOR]"


def _hoje() -> str:
    return datetime.now(timezone.utc).strftime("%d/%m/%Y")


def render_privacy_policy(site: dict) -> str:
    nome = site["nome"]
    dominio = site["dominio"]
    return f"""# Política de Privacidade — {nome}

*Última atualização: {_hoje()}*

Esta Política de Privacidade explica como o site **{nome}** ({dominio}) coleta, usa e
protege informações de quem visita nossas páginas, em conformidade com a Lei Geral de
Proteção de Dados (LGPD — Lei nº 13.709/2018).

## 1. Quem é o responsável pelo site

- Responsável: {PLACEHOLDER_RESPONSAVEL}
- Documento (CPF/CNPJ): {PLACEHOLDER_DOC}
- Localização: {PLACEHOLDER_ENDERECO}
- Contato: {PLACEHOLDER_EMAIL}

## 2. Quais dados coletamos

- **Dados de navegação**: páginas visitadas, tempo de permanência, tipo de dispositivo e
  navegador, coletados automaticamente por ferramentas de análise de audiência.
- **Cookies**: pequenos arquivos armazenados no seu navegador para lembrar preferências,
  medir audiência e exibir anúncios relevantes (ver seção 3).
- **Dados fornecidos voluntariamente**: caso você entre em contato por e-mail ou por um
  eventual formulário do site, armazenamos as informações que você mesmo enviar.

Não coletamos dados sensíveis (saúde, origem racial, opinião política, entre outros) nem
pedimos informações que não sejam necessárias para responder ao seu contato.

## 3. Publicidade e cookies de terceiros (Google AdSense)

Este site exibe anúncios fornecidos pelo Google AdSense. O Google e seus parceiros
publicitários podem usar cookies (incluindo o cookie DoubleClick DART) para exibir
anúncios com base em visitas anteriores a este e a outros sites.

- Você pode desativar o uso de cookies personalizados de publicidade visitando as
  [Configurações de Anúncios do Google](https://adssettings.google.com).
- Também é possível gerenciar preferências de anúncios de diversas empresas em
  [www.aboutads.info](https://www.aboutads.info/choices/).
- Mais detalhes sobre como o Google usa dados de sites parceiros estão disponíveis em
  [policies.google.com/technologies/ads](https://policies.google.com/technologies/ads).

## 4. Como usamos os dados coletados

- Melhorar o conteúdo e a experiência de navegação no site.
- Exibir anúncios relevantes através do Google AdSense.
- Responder a mensagens de contato enviadas por você.

Não vendemos dados pessoais a terceiros.

## 5. Compartilhamento de dados

Dados de navegação podem ser processados por fornecedores de análise de audiência e pelo
Google AdSense, cada um sujeito à sua própria política de privacidade. Não compartilhamos
dados de contato fornecidos voluntariamente com terceiros, exceto quando exigido por lei.

## 6. Seus direitos como titular de dados (LGPD)

Você pode, a qualquer momento, solicitar:

- Confirmação de que tratamos seus dados e acesso a eles;
- Correção de dados incompletos, inexatos ou desatualizados;
- Exclusão dos dados pessoais que você nos forneceu diretamente;
- Informações sobre com quem compartilhamos seus dados.

Para exercer esses direitos, entre em contato pelo e-mail {PLACEHOLDER_EMAIL}.

## 7. Alterações a esta política

Esta política pode ser atualizada periodicamente para refletir mudanças legais ou no
funcionamento do site. A data da última atualização está sempre indicada no topo desta
página.

## 8. Contato

Dúvidas sobre esta Política de Privacidade podem ser enviadas para {PLACEHOLDER_EMAIL}.
"""


def render_terms(site: dict) -> str:
    nome = site["nome"]
    dominio = site["dominio"]
    aviso_saude = site.get("compliance", {}).get("aviso_saude", "").strip()
    return f"""# Termos de Uso — {nome}

*Última atualização: {_hoje()}*

Ao acessar e usar o site **{nome}** ({dominio}), você concorda com os termos descritos
abaixo. Se não concordar com algum ponto, recomendamos não utilizar o site.

## 1. Natureza do conteúdo

O conteúdo publicado aqui tem finalidade **informativa e educativa**, baseado em
experiência prática de tutores de pets. {aviso_saude} As informações não substituem
avaliação, diagnóstico ou tratamento realizado por um médico-veterinário.

## 2. Uso do conteúdo

Você pode ler, compartilhar links e citar trechos do site desde que credite a fonte com
um link para a página original. A reprodução integral de artigos sem autorização prévia
não é permitida.

## 3. Propriedade intelectual

Textos, imagens e demais materiais publicados no site são de propriedade de
{PLACEHOLDER_RESPONSAVEL} ou usados sob licença, salvo indicação contrária.

## 4. Isenção de responsabilidade

Fazemos o possível para manter as informações atualizadas e corretas, mas não garantimos
resultados específicos ao segui-las. O uso das orientações publicadas é de
responsabilidade do leitor, e situações que envolvam a saúde ou segurança do seu pet
devem sempre ser avaliadas por um profissional qualificado.

## 5. Links externos

O site pode conter links para páginas de terceiros. Não somos responsáveis pelo conteúdo
ou pelas práticas de privacidade dessas páginas externas.

## 6. Publicidade

Este site exibe anúncios de terceiros (incluindo o Google AdSense) para se manter no ar.
A presença de um anúncio não representa endosso do site ao produto ou serviço anunciado.

## 7. Alterações destes termos

Estes termos podem ser atualizados periodicamente. O uso continuado do site após uma
alteração representa concordância com os novos termos.

## 8. Legislação aplicável

Estes termos são regidos pelas leis da República Federativa do Brasil.

## 9. Contato

Dúvidas sobre estes Termos de Uso podem ser enviadas para {PLACEHOLDER_EMAIL}.
"""


def render_about(site: dict) -> str:
    nome = site["nome"]
    persona = site["persona_editorial"]
    tom = ", ".join(persona.get("tom", []))
    faz = "\n".join(f"- {item}" for item in persona.get("faz", []))
    nao_faz = "\n".join(f"- {item}" for item in persona.get("nao_faz", []))
    aviso_saude = site.get("compliance", {}).get("aviso_saude", "").strip()
    return f"""# Sobre o {nome}

O **{nome}** nasceu para ajudar tutores de primeira viagem a atravessar a fase mais
incerta de ter um cão ou gato: aquela em que tudo é novo e cada dúvida parece grande
demais para perguntar. Aqui, tratamos cada assunto com um tom {tom} — como uma conversa
entre amigos, não uma aula técnica.

## O que você encontra por aqui

{faz}

## O que você não vai encontrar por aqui

{nao_faz}

> {aviso_saude}

## Quem escreve aqui

**{PLACEHOLDER_AUTOR_NOME}**

{PLACEHOLDER_AUTOR_BIO}

*(Nota para revisão humana: preencher com uma pessoa real, com biografia verdadeira e
verificável, antes da publicação. {persona.get("autoria", "").strip()})*

## Fale com a gente

Tem uma dúvida, sugestão de pauta ou encontrou algo que precisa de correção? Visite a
nossa página de [Contato](/contato).
"""


def render_contact(site: dict) -> str:
    nome = site["nome"]
    return f"""# Contato

Quer tirar uma dúvida, sugerir um assunto para o **{nome}** ou avisar sobre algo que
precisa de correção? Ficamos felizes em ouvir você.

- **E-mail**: {PLACEHOLDER_EMAIL}
- **Outro canal (opcional)**: [PREENCHER]

*(Nota para revisão humana: um formulário de contato pode ser adicionado aqui futuramente;
por enquanto, o e-mail acima é o canal oficial. Substituir o placeholder por um endereço
de e-mail real e monitorado antes da publicação.)*

Respondemos, em média, em até [PREENCHER — prazo estimado de resposta] dias úteis.
"""


RENDERERS = {
    "sobre": render_about,
    "contato": render_contact,
    "politica-de-privacidade": render_privacy_policy,
    "termos": render_terms,
}

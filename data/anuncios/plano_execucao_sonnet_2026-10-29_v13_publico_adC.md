# Plano de execução (Fable → Sonnet) — 29/10/2026 13:00 — v13 gancho + público + anúncio C
Autorizado pelo Allan às 12:58 ("pode corrigir tudo agora"). Ordem: 1 → 2 → 3. Nada além disto; verba continua R$ 30/dia.

## 1. v13: gancho com susto de verdade (opção 1)
- Problema: v13 atual abre com o cachorro longe no alto da escada (0–3 s do clipe 12879576) e com a Duda A1 dizendo "Seu cachorro chora quando você fecha a porta?" enquanto a legenda diz "LATE, CHORA E DESTRÓI". Fala ≠ legenda, sem susto.
- Fazer (receita já pronta em /tmp/v13/build.sh + final2.sh desta sessão; se o /tmp sumiu, refazer com os mesmos parâmetros):
  - Cena 1 = clipe 12879576 de 3,0 s a 5,33 s (cachorro corre e bate na lente), tela cheia, SEM Duda. Cena 2 = cachorro_21 (travesseiro) 0,4 s +1,85 s. Total do gancho 4,18 s.
  - Áudio do gancho = vsl_v13_voz_01_gancho.mp3 (ElevenLabs, "[excited] Seu cachorro late, chora e destrói tudo quando você sai?") a 0,02 s; latido_cachorro_pequeno_84707.mp3 (Downloads) 1,4 s, volume 0,9, entrando a 0,7 s (bate com o impacto na lente).
  - Demais blocos deslocados +1,15 s: voz02 4,23 s · voz03 11,13 s · voz04 16,23 s · voz05 29,13 s · Duda A5 (vídeo+áudio) 36,95 s. Legendas acompanham. Duração final 41,99 s.
  - Música gr0za-happy-happy volume 0,9 com sidechain (threshold 0,03, ratio 4) + fade final; tarja desde 1 s; carimbo; botão verde "COMPRAR AGORA" a partir de 36,95 s.
  - Conferir: contact sheet (0,3 / 1,0 / 1,6 / 2,2 / 3,0 / 4,5 / 11,5 / 37,5 s) — nenhum clipe de biblioteca/clipes_banidos.md; volumedetect mean entre -18 e -22 dB.
  - Salvar sobrescrevendo VSL_A_v13_curto_preco_cedo.mp4 em Downloads\VSL_Sozinho_em_Casa\ e em media/anuncios/; mandar o vídeo ao Allan na lateral.

## 2. Público do conjunto "SP 25-55 caes - Reels+Feed" (adset da campanha VSL v12 SP)
- Hoje: estado SP, 25–65, Advantage+ audience ON, zero interesses → 73% da entrega foi 65+.
- Novo targeting (update_adset no Windsor substitui o targeting inteiro; montar completo):
  - geo_locations: cidades São Paulo (capital), Guarulhos, São Bernardo do Campo, Santo André, Osasco, Campinas, Santos, São José dos Campos — raio padrão; location_types home + recent. Se o Windsor não aceitar busca de cidade, usar o Gerenciador de Anúncios no Chrome (conta act=1213984913380523, já acessível) para editar o conjunto na interface.
  - age_min 25, age_max 54, genders todos.
  - targeting_automation.advantage_audience = 0.
  - flexible_spec interesses: Cachorros (Dogs), Adestramento de cães (Dog training), Alimento para animais de estimação (Pet food), Petz, Cobasi. Pegar os IDs pela busca de interesses (Gerenciador no Chrome ou get_options do Windsor); não chutar ID.
  - publisher_platforms facebook + instagram; facebook_positions feed + facebook_reels; instagram_positions reels (Instagram feed continua fora).
- Conferir depois lendo o adset_targeting de volta (get_data, campo adset_targeting) e colar o JSON na ficha.

## 3. Anúncio C
- Só depois de 1 e 2 prontos. Mesmo conjunto. Vídeo = v13 corrigido (subir pelo Windsor create_ad com vídeo ou pelo Gerenciador no Chrome). Nome: VSL_A_v13_ad_C_preco_cedo.
- Copy = igual ao anúncio B (texto primário, título "Plano de 14 dias com app · R$ 27", botão COMPRAR AGORA). Link https://sozinho.tutorialpet.com.br/?utm_source=meta&utm_medium=paid&utm_campaign=vsl_v12_sp&utm_content=ad_c (mesmo padrão de UTM do B; conferir o do B e copiar trocando só utm_content).
- Pausar o anúncio A (VSL_A_v12_ad_A_problema). B continua. Verba não muda.
- Registrar tudo na ficha data/anuncios/campanha_vsl_v12_sp.md (hora, o que mudou, JSON do targeting, id do anúncio C) e commit/push com as 2 linhas de atribuição da sessão.
- Leitura: amanhã 30/10 09:00 (já agendada) compara B × C; o Auditor de Anúncios 09:34 lê também.

Se o classificador negar alguma ação: parar e perguntar, não contornar.

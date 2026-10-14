# Processo para fechar um vídeo gastando pouco (Otimizador de Processo, 13/10/2026)

Por que gastou muito no Sozinho em Casa: cada ajuste (visual, latido, faixa, preço) regerava a voz inteira (~500 créditos) e rodava a fábrica de novo.

Regras:
1. Voz em cache: mesma frase + voz + ajustes = 0 crédito (biblioteca/voz_cache + actions/cache). Só muda a frase que mudou.
2. Roteiro fechado ANTES de gerar: ler a narração em voz alta, evitar palavras que a voz erra ("Imagine", "baseado"), conferir preço/garantia/promessas.
3. Juntar todo o feedback numa rodada só e gerar uma vez; nunca uma geração por ajuste.
4. Testar sem custo antes: latido (teste_latido.yml), contact sheet de quadros, nível de áudio (volumedetect).
5. Checklist antes de enviar ao Allan: preço correto, sem legenda cortada, latido audível, CTA final, thumbnail com 3 variações, duração dentro do limite.
6. Thumbnail só de quadro limpo (sem legenda queimada), feita no mesmo passo do vídeo.

// Letra gerada por LLM a partir do formulário (pt-BR). Nome do pet no refrão, manias nos versos.
// Sempre passa pelo filtro; se o LLM falhar ou reprovar 3x, usa um modelo de letra próprio (nunca trava a entrega).
import { proibidoNaLetra } from "./filtro.js";
import { semAcento } from "./util.js";

const MODELO_CF = "@cf/meta/llama-3.3-70b-instruct-fp8-fast";

const QUEM = { cachorro: "um cachorrinho", gato: "um gatinho", "outro-pet": "um bichinho de estimação", pessoa: "uma pessoa querida", outro: "alguém especial" };

function promptLetra(p, tentativa) {
  const quem = QUEM[p.especie] || QUEM.outro;
  return [
    "Você é um compositor brasileiro de músicas carinhosas e divertidas, feitas sob medida para alguém especial.",
    `Escreva a letra de uma música em português do Brasil sobre ${quem} chamado(a) ${p.nomePet}.`,
    p.raca ? `Detalhe extra: ${p.raca}.` : "",
    `Características e manias (use nos versos, com carinho): ${p.manias.map((m, i) => `${i + 1}) ${m}`).join("; ")}.`,
    p.tutor ? `O tutor se chama ${p.tutor} (cite no máximo uma vez, de forma carinhosa).` : "",
    `Estilo musical: ${p.estilo}. Clima: ${p.clima}.`,
    "REGRAS OBRIGATÓRIAS:",
    `- O nome ${p.nomePet} deve aparecer no refrão (pelo menos 2 vezes no refrão).`,
    "- Estrutura com rótulos entre colchetes: [Verse 1], [Chorus], [Verse 2], [Chorus], [Bridge], [Chorus].",
    "- Rimas simples, frases curtas e fáceis de cantar, 28 a 40 linhas no total.",
    "- Nunca use a palavra 'cão' nem 'cães' (para cachorros use 'cachorrinho', 'amiguinho', 'melhor amigo'). Não suponha o gênero de quem recebe a música: evite pronomes quando possível.",
    "- Não cite nomes de artistas, bandas, marcas nem títulos de músicas existentes.",
    "- Nada de tristeza pesada, violência, política ou conteúdo ofensivo.",
    p.clima === "homenagem" ? "- Tom de homenagem carinhosa e grata, celebrando os momentos juntos." : "- Tom leve, alegre e afetuoso.",
    tentativa > 0 ? "- ATENÇÃO: a tentativa anterior foi reprovada; siga todas as regras à risca." : "",
    "FORMATO DE SAÍDA: primeira linha 'TITULO: <título curto>', depois uma linha em branco e a letra. Sem explicações.",
  ].filter(Boolean).join("\n");
}

async function chamarLLM(env, prompt) {
  if (env.AI && typeof env.AI.run === "function") {
    const r = await env.AI.run(MODELO_CF, { messages: [{ role: "user", content: prompt }], max_tokens: 1400, temperature: 0.8 });
    const t = r?.response ?? r?.result?.response;
    if (t) return String(t);
  }
  if (env.GEMINI_API_KEY) {
    const r = await fetch("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent", {
      method: "POST",
      headers: { "content-type": "application/json", "x-goog-api-key": env.GEMINI_API_KEY },
      body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }], generationConfig: { temperature: 0.8, maxOutputTokens: 1400 } }),
    });
    if (!r.ok) throw new Error(`gemini ${r.status}`);
    const j = await r.json();
    const t = j?.candidates?.[0]?.content?.parts?.map((x) => x.text).join("");
    if (t) return t;
  }
  throw new Error("nenhum LLM configurado (binding AI ou GEMINI_API_KEY)");
}

function separar(texto) {
  let t = String(texto).replace(/\r/g, "").trim();
  t = t.replace(/^```[a-z]*\n?|```$/gim, "").trim();
  let titulo = "";
  const m = t.match(/^\s*t[ií]tulo\s*:\s*(.+)$/im);
  if (m) { titulo = m[1].replace(/[*"“”]/g, "").trim(); t = t.replace(m[0], "").trim(); }
  return { titulo, letra: t };
}

export function validarLetra(letra, p) {
  if (letra.length < 350 || letra.length > 3800) return "tamanho fora do limite";
  const motivo = proibidoNaLetra(letra);
  if (motivo) return motivo;
  const nome = semAcento(p.nomePet).toLowerCase();
  const ocorr = semAcento(letra).toLowerCase().split(nome).length - 1;
  if (ocorr < 3) return "nome do pet aparece poucas vezes";
  if (!/\[chorus\]/i.test(letra)) return "sem refrão";
  return null;
}

export function letraModelo(p) {
  const n = p.nomePet;
  const bicho = { cachorro: "cachorrinho", gato: "gatinho", "outro-pet": "bichinho", pessoa: "alguém", outro: "alguém" }[p.especie] || "alguém";
  const [m1, m2, m3] = [p.manias[0], p.manias[1] || p.manias[0], p.manias[2] || p.manias[1] || p.manias[0]];
  const alegre = p.clima !== "homenagem";
  const refrao = alegre
    ? [`${n}, ${n}, que alegria é ter você,`, `${n}, ${n}, meu xodó, meu bem,`, `Cada dia é uma festa quando você vem,`, `${n}, ${n}, é um barato ter você!`]
    : [`${n}, ${n}, obrigado por ficar,`, `${n}, ${n}, meu xodó, meu lar,`, `Cada momento ao seu lado vale ouro,`, `${n}, ${n}, é um barato ter você!`];
  const tutor = p.tutor ? `${p.tutor} te olha e sorri sem parar,` : "Todo mundo em casa começa a sorrir,";
  const linhas = [
    "[Verse 1]",
    `Quando ${n} chega, o dia fica bom,`,
    `Esse jeito de ${n} é só seu, um dom,`,
    `${m1},`,
    "É assim que conquista o seu lugar,",
    tutor,
    "Qualquer tristeza vai embora de lá.",
    "",
    "[Chorus]", ...refrao, "",
    "[Verse 2]",
    `${m2},`,
    "E a casa inteira acaba de acordar,",
    `${m3},`,
    `${n} faz a vida ficar mais leve de passar,`,
    "Com esse olhar que ninguém sabe explicar,",
    "Dá vontade de abraçar e agradecer.",
    "",
    "[Chorus]", ...refrao, "",
    "[Bridge]",
    `Se o mundo gira, ${n} está aqui,`,
    "Sempre perto, sempre ali,",
    "Um amor pra vida inteira,",
    `E ${n} é de todos a alegria primeira!`,
    "",
    "[Chorus]", ...refrao,
  ];
  return { titulo: `A música do ${n}`, letra: linhas.join("\n") };
}

export async function gerarLetra(p, env) {
  let ultimoErro = "";
  for (let i = 0; i < 3; i++) {
    try {
      const bruto = await chamarLLM(env, promptLetra(p, i));
      const { titulo, letra } = separar(bruto);
      const erro = validarLetra(letra, p);
      if (!erro) return { titulo: titulo || `A música do ${p.nomePet}`, letra, origem: "llm" };
      ultimoErro = erro;
    } catch (e) {
      ultimoErro = String(e?.message || e);
      if (/nenhum LLM/.test(ultimoErro)) break;
    }
  }
  const m = letraModelo(p);
  const erroModelo = validarLetra(m.letra, p);
  if (erroModelo) throw new Error(`letra-modelo reprovada no filtro: ${erroModelo}`);
  return { ...m, origem: `modelo (LLM: ${ultimoErro || "n/a"})` };
}

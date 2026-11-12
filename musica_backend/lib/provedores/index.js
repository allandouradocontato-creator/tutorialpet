// Camada de troca: gerarMusica(pedidoPadrao) -> { mp3Url | mp3Bytes, provedor, duracao }.
// Ordem e provedor ativo vêm da variável de ambiente MUSIC_PROVIDERS (ex.: "fal,mureka,elevenlabs").
import * as fal from "./fal.js";
import * as mureka from "./mureka.js";
import * as elevenlabs from "./elevenlabs.js";
import * as demo from "./demo.js";
import * as hf from "./hf.js";
import { gerarLetra } from "../letra.js";
import { sleep } from "../util.js";

export const PROVEDORES = { fal, hf, mureka, elevenlabs, demo };

export function cadeia(env) {
  const nomes = String(env.MUSIC_PROVIDERS || "fal,mureka,elevenlabs").split(",").map((s) => s.trim().toLowerCase()).filter(Boolean);
  return nomes.filter((n) => PROVEDORES[n] && PROVEDORES[n].disponivel(env));
}

export function pedidoPadrao(form, estilo) {
  return {
    nomePet: form.nomePet, especie: form.especie, raca: form.raca || "", manias: form.manias, historia: form.historia || "", tutor: form.tutor || "",
    estilo: estilo || form.estilo, voz: form.voz, clima: form.clima, idioma: "pt-BR", duracaoAlvo: 150,
  };
}

// Versão síncrona (testes/CLI): letra -> envia -> consulta até concluir; se o provedor falhar ou estourar o tempo, tenta o próximo.
export async function gerarMusica(pedido, env, { timeoutMs = 240000, intervaloMs = 5000, only = null } = {}) {
  const { titulo, letra } = await gerarLetra(pedido, env);
  const nomes = only ? [only] : cadeia(env);
  const erros = [];
  for (const nome of nomes) {
    const prov = PROVEDORES[nome];
    try {
      const env1 = await prov.enviar(pedido, letra, env, {});
      if (env1.mp3Bytes) return { mp3Bytes: env1.mp3Bytes, provedor: nome, duracao: env1.duracao, titulo, letra };
      const t0 = Date.now();
      while (Date.now() - t0 < timeoutMs) {
        await sleep(intervaloMs);
        const s = await prov.consultar(env1.jobId, env);
        if (s.estado === "pronto") return { mp3Url: s.audioUrl, contentType: s.contentType, provedor: nome, duracao: s.duracao, titulo, letra };
        if (s.estado === "falhou") throw new Error(s.motivo);
      }
      throw new Error("tempo esgotado");
    } catch (e) {
      erros.push(`${nome}: ${e.message}`);
    }
  }
  throw new Error(`todos os provedores falharam -> ${erros.join(" | ") || "nenhum provedor com chave configurada"}`);
}

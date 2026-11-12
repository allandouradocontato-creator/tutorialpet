// Adaptador 3 (reserva futura): ElevenLabs Music API. Resposta síncrona com o áudio (mp3) no corpo.
import { descricaoEstilo } from "../estilos.js";

export const nome = "elevenlabs";
export const disponivel = (env) => !!env.ELEVENLABS_MUSIC_KEY || !!env.ELEVENLABS_API_KEY;

export async function enviar(pedido, letra, env) {
  const key = env.ELEVENLABS_MUSIC_KEY || env.ELEVENLABS_API_KEY;
  const prompt = `Canção em português do Brasil. Estilo: ${descricaoEstilo(pedido, 300)}. ` +
    `Cante exatamente esta letra, sem alterar nada:\n${letra}`.slice(0, 4000);
  const r = await fetch("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128", {
    method: "POST",
    headers: { "xi-api-key": key, "content-type": "application/json" },
    body: JSON.stringify({ prompt, music_length_ms: Math.round((pedido.duracaoAlvo || 150) * 1000), model_id: "music_v1" }),
  });
  if (!r.ok) throw new Error(`elevenlabs ${r.status}: ${(await r.text()).slice(0, 200)}`);
  const bytes = new Uint8Array(await r.arrayBuffer());
  if (bytes.length < 20000) throw new Error("elevenlabs: áudio vazio");
  return { mp3Bytes: bytes, duracao: (pedido.duracaoAlvo || 150) };
}

export async function consultar() { return { estado: "falhou", motivo: "elevenlabs é síncrono" }; }

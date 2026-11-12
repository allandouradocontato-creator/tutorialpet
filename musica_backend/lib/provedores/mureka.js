// Adaptador 2 (reserva): Mureka API (platform.mureka.ai), letra própria -> música. Assíncrono por consulta de status.
import { descricaoEstilo } from "../estilos.js";

export const nome = "mureka";
export const disponivel = (env) => !!env.MUREKA_API_KEY;
const H = (env) => ({ authorization: `Bearer ${env.MUREKA_API_KEY}`, "content-type": "application/json" });

export async function enviar(pedido, letra, env) {
  const r = await fetch("https://api.mureka.ai/v1/song/generate", {
    method: "POST",
    headers: H(env),
    body: JSON.stringify({ lyrics: letra.slice(0, 4900), model: "auto", prompt: descricaoEstilo(pedido, 300) }),
  });
  const t = await r.text();
  if (!r.ok) throw new Error(`mureka enviar ${r.status}: ${t.slice(0, 200)}`);
  const j = JSON.parse(t);
  if (!j.id) throw new Error("mureka: sem id de tarefa");
  return { jobId: String(j.id) };
}

export async function consultar(jobId, env) {
  const r = await fetch(`https://api.mureka.ai/v1/song/query/${encodeURIComponent(jobId)}`, { headers: H(env) });
  const t = await r.text();
  if (!r.ok) throw new Error(`mureka status ${r.status}: ${t.slice(0, 160)}`);
  const j = JSON.parse(t);
  const s = String(j.status || "").toLowerCase();
  if (["preparing", "queued", "running", "streaming", "reviewing"].includes(s)) return { estado: "processando" };
  if (s === "succeeded") {
    const c = j.choices?.[0];
    const url = c?.url || c?.mp3_url;
    if (!url) return { estado: "falhou", motivo: "mureka: sem url na resposta" };
    return { estado: "pronto", audioUrl: url, contentType: "audio/mpeg", duracao: c?.duration ? c.duration / 1000 : null };
  }
  return { estado: "falhou", motivo: `mureka status ${j.status}${j.failed_reason ? ": " + j.failed_reason : ""}` };
}

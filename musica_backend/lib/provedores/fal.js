// Adaptador 1 (ativo no MVP): fal.ai, modelo fal-ai/ace-step-1.5, fila assíncrona com webhook.
import { descricaoEstilo } from "../estilos.js";
import { baseUrl } from "../util.js";

export const nome = "fal";
export const disponivel = (env) => !!env.FAL_KEY;
const MODELO = "fal-ai/ace-step-1.5";
const H = (env) => ({ authorization: `Key ${env.FAL_KEY}`, "content-type": "application/json" });

export async function enviar(pedido, letra, env, ctx = {}) {
  let url = `https://queue.fal.run/${MODELO}`;
  if (ctx.webhookId && env.FAL_USE_WEBHOOK !== "0") {
    const wh = `${baseUrl(env)}/api/musica/fal-webhook?id=${encodeURIComponent(ctx.webhookId)}&k=${encodeURIComponent(env.FAL_WEBHOOK_SECRET || "")}`;
    url += `?fal_webhook=${encodeURIComponent(wh)}`;
  }
  const r = await fetch(url, {
    method: "POST",
    headers: H(env),
    body: JSON.stringify({
      prompt: descricaoEstilo(pedido, 500),
      lyrics: letra.slice(0, 4000),
      duration: Math.min(180, Math.max(90, Math.round(pedido.duracaoAlvo || 150))),
      vocal_language: "pt",
      thinking: true,
      num_outputs: 1,
    }),
  });
  const t = await r.text();
  if (!r.ok) throw new Error(`fal enviar ${r.status}: ${t.slice(0, 200)}`);
  const j = JSON.parse(t);
  if (!j.request_id) throw new Error("fal: sem request_id");
  return { jobId: JSON.stringify({ id: j.request_id, s: j.status_url, r: j.response_url }) };
}

export async function consultar(jobId, env) {
  const job = JSON.parse(jobId);
  const sr = await fetch(job.s, { headers: H(env) });
  if (!sr.ok && sr.status !== 202) throw new Error(`fal status ${sr.status}`);
  const st = await sr.json();
  if (st.status === "IN_QUEUE" || st.status === "IN_PROGRESS") return { estado: "processando" };
  if (st.status !== "COMPLETED") return { estado: "falhou", motivo: `fal status ${st.status}` };
  const rr = await fetch(job.r, { headers: H(env) });
  const txt = await rr.text();
  if (!rr.ok) return { estado: "falhou", motivo: `fal resultado ${rr.status}: ${txt.slice(0, 160)}` };
  const j = JSON.parse(txt);
  const a = j.audio || j.audios?.[0]?.audio;
  if (!a?.url) return { estado: "falhou", motivo: "fal: resposta sem audio.url" };
  return { estado: "pronto", audioUrl: a.url, contentType: a.content_type || "", duracao: j.duration || null };
}

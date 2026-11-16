// Adaptador deAPI (US$ 5 grátis, sem cartão): ACE-Step 1.5 via POST /txt2music + GET /request-status/{id}.
// Chave no segredo DEAPI_KEY (Cloudflare). Modelo padrão XL Turbo INT8; troque com DEAPI_MODEL (ex.: AceStep_1_5_Turbo).
import { descricaoEstilo } from "../estilos.js";

export const nome = "deapi";
export const disponivel = (env) => !!env.DEAPI_KEY;
const BASE = "https://api.deapi.ai/api/v1/client";
const H = (env) => ({ authorization: `Bearer ${env.DEAPI_KEY}`, accept: "application/json" });

export async function enviar(pedido, letra, env, ctx = {}) {
  const fd = new FormData();
  fd.append("model", env.DEAPI_MODEL || "AceStep_1_5_XL_Turbo_INT8");
  fd.append("caption", descricaoEstilo(pedido, 500));
  fd.append("lyrics", String(letra || "").slice(0, 4000) || "[Instrumental]");
  fd.append("duration", String(Math.min(180, Math.max(30, Math.round(pedido.duracaoAlvo || 150)))));
  fd.append("inference_steps", "8");
  fd.append("guidance_scale", "1");
  fd.append("seed", "-1");
  fd.append("format", "mp3");
  fd.append("vocal_language", "pt");
  const r = await fetch(`${BASE}/txt2music`, { method: "POST", headers: H(env), body: fd });
  const t = await r.text();
  if (!r.ok) throw new Error(`deapi enviar ${r.status}: ${t.slice(0, 200)}`);
  let j;
  try { j = JSON.parse(t); } catch { throw new Error("deapi: resposta não é JSON"); }
  const id = j?.data?.request_id || j?.request_id;
  if (!id) throw new Error("deapi: sem request_id");
  return { jobId: String(id) };
}

export async function consultar(jobId, env) {
  const r = await fetch(`${BASE}/request-status/${encodeURIComponent(jobId)}`, { headers: H(env) });
  const t = await r.text();
  if (!r.ok) {
    if (r.status >= 500 || r.status === 429) return { estado: "processando" };
    return { estado: "falhou", motivo: `deapi status ${r.status}: ${t.slice(0, 160)}` };
  }
  let j;
  try { j = JSON.parse(t); } catch { return { estado: "processando" }; }
  const d = j.data || j;
  const st = String(d.status || "").toLowerCase();
  if (st === "done" || st === "completed") {
    const url = d.result_url || d.result?.url || d.result;
    if (!url || typeof url !== "string") return { estado: "falhou", motivo: "deapi: pronto, mas sem result_url" };
    return { estado: "pronto", audioUrl: url, contentType: "audio/mpeg", duracao: d.duration || null };
  }
  if (st === "error" || st === "failed") return { estado: "falhou", motivo: `deapi: ${d.error || d.message || "erro na geração"}` };
  return { estado: "processando" };
}

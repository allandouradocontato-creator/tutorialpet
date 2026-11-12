// Adaptador GRATUITO: Space ACE-Step (Apache-2.0) no Hugging Face, via API HTTP do Gradio.
// Precisa só de um token de LEITURA gratuito (env HF_TOKEN) para ter a cota ZeroGPU da conta.
// Assíncrono: enviar() abre a chamada e guarda o event_id; consultar() lê o fluxo SSE por poucos segundos por vez.
import { descricaoEstilo } from "../estilos.js";

export const nome = "hf";
export const disponivel = (env) => !!env.HF_TOKEN;
const BASE = (env) => String(env.HF_ACESTEP_URL || "https://ace-step-ace-step.hf.space").replace(/\/$/, "");
const H = (env) => ({ authorization: `Bearer ${env.HF_TOKEN}`, "content-type": "application/json" });

// Protocolo de fila do Gradio (devolve a mensagem de erro real, ex.: cota ZeroGPU).
let _fn = null;
async function fnIndex(env) {
  if (_fn !== null) return _fn;
  const r = await fetch(`${BASE(env)}/config`, { headers: H(env) });
  if (!r.ok) throw new Error(`hf config ${r.status}`);
  const c = await r.json();
  const d = (c.dependencies || []).find((x) => x.api_name === "__call__");
  if (!d) throw new Error("hf: endpoint __call__ não encontrado");
  _fn = d.id;
  return _fn;
}

export async function enviar(pedido, letra, env) {
  const dur = Math.min(60, Math.max(30, Number(env.HF_DURACAO || 50)));
  const data = [
    dur, descricaoEstilo(pedido, 500), String(letra).slice(0, 3000),
    60, 15.0, "euler", "apg", 10.0, null, 0.5, 0.0, 3.0, true, false, true, null, 0.0, 0.0,
    false, 0.5, null, "none",
  ];
  const sh = Math.random().toString(36).slice(2, 12);
  const r = await fetch(`${BASE(env)}/gradio_api/queue/join`, { method: "POST", headers: H(env), body: JSON.stringify({ data, fn_index: await fnIndex(env), session_hash: sh }) });
  const t = await r.text();
  if (!r.ok) throw new Error(`hf enviar ${r.status}: ${t.slice(0, 200)}`);
  const j = JSON.parse(t);
  if (!j.event_id) throw new Error("hf: sem event_id");
  return { jobId: JSON.stringify({ e: j.event_id, s: sh, d: dur }) };
}

// Lê o fluxo SSE por até ~20 s; se não terminar, devolve "processando" e o próximo tick continua.
export async function consultar(jobId, env) {
  const job = JSON.parse(jobId);
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 20000);
  let texto = "";
  let fim = null;
  try {
    const r = await fetch(`${BASE(env)}/gradio_api/queue/data?session_hash=${job.s}`, { headers: H(env), signal: ctl.signal });
    if (!r.ok) throw new Error(`hf status ${r.status}`);
    const rd = r.body.getReader();
    const dec = new TextDecoder();
    for (;;) {
      const { value, done } = await rd.read();
      if (value) texto += dec.decode(value, { stream: true });
      const m = texto.split("\n").filter((l) => l.startsWith("data:")).map((l) => { try { return JSON.parse(l.slice(5)); } catch { return null; } }).find((o) => o && o.msg === "process_completed" && (!o.event_id || o.event_id === job.e));
      if (m) { fim = m; break; }
      if (done) break;
    }
  } catch (e) {
    if (e.name === "AbortError") return { estado: "processando" };
    throw e;
  } finally {
    clearTimeout(timer);
  }
  if (!fim) return { estado: "processando" };
  if (!fim.success) return { estado: "falhou", motivo: `hf: ${String(fim.output?.error || "erro sem mensagem").slice(0, 220)}` };
  const f = fim.output?.data?.[0];
  const url = f && (f.url || (f.path ? `${BASE(env)}/gradio_api/file=${f.path}` : ""));
  if (!url) return { estado: "falhou", motivo: "hf: resposta sem áudio" };
  return { estado: "pronto", audioUrl: url, contentType: f.mime_type || "", duracao: job.d };
}

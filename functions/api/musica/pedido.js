import { json } from "../../../musica_backend/lib/util.js";
import { criarPedido } from "../../../musica_backend/lib/core.js";

export async function onRequestPost({ request, env, waitUntil }) {
  let body;
  try { body = await request.json(); } catch { return json({ ok: false, erro: "Pedido inválido." }, 400); }
  if (JSON.stringify(body).length > 4000) return json({ ok: false, erro: "Pedido grande demais." }, 413);
  const r = await criarPedido(env, body, { waitUntil });
  return json(r, r.ok ? 200 : 400);
}

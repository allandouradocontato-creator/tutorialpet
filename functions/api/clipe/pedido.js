import { json } from "../../../clipe_backend/lib/util.js";
import { criarPedido } from "../../../clipe_backend/lib/core.js";
export async function onRequestPost({ request, env }) {
  let b; try { b = await request.json(); } catch { return json({ ok: false, erro: "Pedido inválido." }, 400); }
  if (JSON.stringify(b).length > 2000) return json({ ok: false, erro: "Pedido grande demais." }, 413);
  const r = await criarPedido(env, b);
  return json(r, r.ok ? 200 : 400);
}

import { json } from "../../../clipe_backend/lib/util.js";
import { enviarPedido } from "../../../clipe_backend/lib/core.js";
export async function onRequestPost({ request, env, waitUntil }) {
  const u = new URL(request.url);
  const r = await enviarPedido(env, u.searchParams.get("id"), u.searchParams.get("token"), { waitUntil });
  return json(r, r.ok ? 200 : r.status || 400);
}

import { json, autorizado } from "../../../clipe_backend/lib/util.js";
import { fila } from "../../../clipe_backend/lib/core.js";
export async function onRequestGet({ request, env }) {
  if (!autorizado(request, env)) return json({ ok: false }, 401);
  return json({ ok: true, pedidos: await fila(env) });
}

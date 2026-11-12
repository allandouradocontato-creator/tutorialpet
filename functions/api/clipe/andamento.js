import { json, autorizado } from "../../../clipe_backend/lib/util.js";
import { andamento } from "../../../clipe_backend/lib/core.js";
export async function onRequestPost({ request, env }) {
  if (!autorizado(request, env)) return json({ ok: false }, 401);
  const q = new URL(request.url).searchParams;
  const r = await andamento(env, q.get("id"), { estado: q.get("estado"), etapa: q.get("etapa"), msg: q.get("msg") });
  return json(r, r.ok ? 200 : r.status || 400);
}

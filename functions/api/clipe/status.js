import { json } from "../../../clipe_backend/lib/util.js";
import { statusPublico } from "../../../clipe_backend/lib/core.js";
export async function onRequestGet({ request, env }) {
  const s = await statusPublico(env, new URL(request.url).searchParams.get("id"));
  return s ? json({ ok: true, ...s }) : json({ ok: false, erro: "Pedido não encontrado." }, 404);
}

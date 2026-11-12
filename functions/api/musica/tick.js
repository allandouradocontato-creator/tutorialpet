import { json, autorizado } from "../../../musica_backend/lib/util.js";
import { tick } from "../../../musica_backend/lib/core.js";

export async function onRequestPost({ request, env, waitUntil }) {
  if (!autorizado(request, env)) return json({ ok: false }, 401);
  return json({ ok: true, ...(await tick(env, { waitUntil })) });
}

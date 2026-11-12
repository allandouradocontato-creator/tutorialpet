import { json, iguais } from "../../../musica_backend/lib/util.js";
import { avancar } from "../../../musica_backend/lib/core.js";

// O fal chama este endereço quando a geração termina. O corpo não é confiável: só usamos o id para "empurrar" a consulta oficial.
export async function onRequestPost({ request, env, waitUntil }) {
  const u = new URL(request.url);
  if (!env.FAL_WEBHOOK_SECRET || !iguais(u.searchParams.get("k"), env.FAL_WEBHOOK_SECRET)) return json({ ok: false }, 401);
  const id = u.searchParams.get("id") || "";
  waitUntil(avancar(env, id, { waitUntil }));
  return json({ ok: true });
}

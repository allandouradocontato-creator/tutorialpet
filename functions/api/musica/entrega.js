import { json } from "../../../musica_backend/lib/util.js";
import { visaoPublica } from "../../../musica_backend/lib/core.js";

export async function onRequestGet({ request, env }) {
  const id = new URL(request.url).searchParams.get("id") || "";
  const v = await visaoPublica(env, id);
  return v ? json(v) : json({ ok: false, erro: "Pedido não encontrado." }, 404);
}

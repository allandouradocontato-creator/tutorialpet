// POST ?id=&token=&n=  (corpo = MP4/MOV, até 20 MB) -> cliente envia; GET ?id=&n= (Bearer do worker) -> worker baixa.
import { json, autorizado } from "../../../clipe_backend/lib/util.js";
import { receberVideoCliente, lerVideoCliente } from "../../../clipe_backend/lib/core.js";
export async function onRequestPost({ request, env }) {
  const u = new URL(request.url);
  const bytes = await request.arrayBuffer();
  const r = await receberVideoCliente(env, u.searchParams.get("id"), u.searchParams.get("token"), u.searchParams.get("n"), bytes);
  return json(r, r.ok ? 200 : r.status || 400);
}
export async function onRequestGet({ request, env }) {
  if (!autorizado(request, env)) return json({ ok: false }, 401);
  const u = new URL(request.url);
  const b = await lerVideoCliente(env, u.searchParams.get("id"), u.searchParams.get("n"));
  if (!b) return json({ ok: false, erro: "vídeo não encontrado" }, 404);
  return new Response(b, { headers: { "content-type": "video/mp4", "cache-control": "no-store" } });
}

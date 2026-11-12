import { json, autorizado } from "../../../clipe_backend/lib/util.js";
import { guardarVideo } from "../../../clipe_backend/lib/core.js";
export async function onRequestPost({ request, env }) {
  if (!autorizado(request, env)) return json({ ok: false }, 401);
  const q = new URL(request.url).searchParams;
  const bytes = await request.arrayBuffer();
  if (bytes.byteLength < 10000 || bytes.byteLength > 24 * 1024 * 1024) return json({ ok: false, erro: "tamanho inválido" }, 400);
  const r = await guardarVideo(env, q.get("id"), bytes, { animadas: parseInt(q.get("animadas"), 10) || 0, total: parseInt(q.get("total"), 10) || 0 });
  return json(r, r.ok ? 200 : r.status || 400);
}

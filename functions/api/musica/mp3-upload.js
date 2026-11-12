import { json, autorizado } from "../../../musica_backend/lib/util.js";
import { receberMp3Convertido } from "../../../musica_backend/lib/core.js";

// Recebe o MP3 convertido (workflow musica_converter.yml / tick). Protegido por TICK_SECRET.
export async function onRequestPost({ request, env }) {
  if (!autorizado(request, env)) return json({ ok: false }, 401);
  const u = new URL(request.url);
  const bytes = new Uint8Array(await request.arrayBuffer());
  if (bytes.length > 20 * 1024 * 1024) return json({ ok: false, erro: "grande demais" }, 413);
  try { return json(await receberMp3Convertido(env, u.searchParams.get("id") || "", u.searchParams.get("n") || "1", bytes)); }
  catch (e) { return json({ ok: false, erro: e.message }, 400); }
}

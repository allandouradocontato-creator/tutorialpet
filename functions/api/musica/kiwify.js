import { json } from "../../../musica_backend/lib/util.js";
import { aplicarPagamento, validarAssinaturaKiwify } from "../../../musica_backend/lib/core.js";

export async function onRequestPost({ request, env, waitUntil, ...ctx }) {
  const raw = await request.text();
  if (!(await validarAssinaturaKiwify(env, request, raw))) return json({ ok: false, erro: "assinatura inválida" }, 401);
  let payload;
  try { payload = JSON.parse(raw); } catch { return json({ ok: false, erro: "json inválido" }, 400); }
  const r = await aplicarPagamento(env, payload, { waitUntil: (pr) => waitUntil(pr) });
  return json(r, r.ok ? 200 : 202); // 202 (não 4xx) quando falta pedido: já alertamos o Allan e a Kiwify não precisa reenviar em loop
}

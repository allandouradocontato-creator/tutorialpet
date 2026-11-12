import { json } from "../../../musica_backend/lib/util.js";
import { gerarLetraPedido, aprovarLetraPedido } from "../../../musica_backend/lib/core.js";

// POST { id, acao: "gerar" | "aprovar", ajuste?, letra?, titulo? }: letra DEPOIS do pagamento (só pedidos no estado "letra").
export async function onRequestPost({ request, env, waitUntil }) {
  let b;
  try { b = await request.json(); } catch { return json({ ok: false, erro: "Pedido inválido." }, 400); }
  if (JSON.stringify(b).length > 9000) return json({ ok: false, erro: "Pedido grande demais." }, 413);
  try {
    const r = b.acao === "aprovar" ? await aprovarLetraPedido(env, b.id, b, { waitUntil }) : await gerarLetraPedido(env, b.id, b);
    return json(r, r.ok ? 200 : 400);
  } catch (e) {
    return json({ ok: false, erro: "Não conseguimos gerar a letra agora. Tente de novo em instantes." }, 502);
  }
}

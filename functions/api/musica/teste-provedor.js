import { json, autorizado } from "../../../musica_backend/lib/util.js";
import { gerarMusica } from "../../../musica_backend/lib/provedores/index.js";

// Teste de provedor com a chave que fica só no Cloudflare. Protegido por TICK_SECRET.
// POST { provedor, pedido:{...pedidoPadrao}, nome } -> gera, guarda o arquivo em KV (t:<nome>, 2 h) e devolve metadados.
// GET  ?nome=... -> devolve o arquivo (para baixar e conferir de ouvido).
export async function onRequestPost({ request, env }) {
  if (!autorizado(request, env)) return json({ ok: false }, 401);
  const { provedor, pedido, nome } = await request.json();
  if (!/^[a-z0-9_-]{3,80}$/.test(nome || "")) return json({ ok: false, erro: "nome inválido" }, 400);
  const t0 = Date.now();
  try {
    const r = await gerarMusica(pedido, env, { only: provedor, timeoutMs: 300000 });
    let bytes = r.mp3Bytes, tipo = "audio/mpeg";
    if (!bytes) {
      const a = await fetch(r.mp3Url);
      if (!a.ok) throw new Error(`download ${a.status}`);
      bytes = new Uint8Array(await a.arrayBuffer());
      tipo = a.headers.get("content-type") || r.contentType || "audio/mpeg";
    }
    await env.PEDIDOS.put("t:" + nome, bytes, { expirationTtl: 7200, metadata: { tipo } });
    return json({ ok: true, provedor: r.provedor, segundos: Math.round((Date.now() - t0) / 1000), bytes: bytes.length, tipo, duracao: r.duracao, titulo: r.titulo, letra: r.letra });
  } catch (e) {
    return json({ ok: false, erro: e.message, segundos: Math.round((Date.now() - t0) / 1000) }, 502);
  }
}

export async function onRequestGet({ request, env }) {
  if (!autorizado(request, env)) return json({ ok: false }, 401);
  const nome = new URL(request.url).searchParams.get("nome") || "";
  const m = await env.PEDIDOS.getWithMetadata("t:" + nome, { type: "arrayBuffer" });
  if (!m.value) return json({ ok: false, erro: "não encontrado" }, 404);
  return new Response(m.value, { headers: { "content-type": m.metadata?.tipo || "audio/mpeg" } });
}

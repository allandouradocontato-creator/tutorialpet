// Entrega do MP4 com suporte a Range (Safari/iPhone exigem para tocar e permitir arrastar). ?download=1 baixa com nome amigável.
import { json } from "../../../clipe_backend/lib/util.js";
import { getPedido, lerVideo } from "../../../clipe_backend/lib/core.js";
export async function onRequestGet({ request, env }) {
  const u = new URL(request.url), id = u.searchParams.get("id");
  const p = await getPedido(env, id);
  const b = p && p.estado === "entregue" ? await lerVideo(env, id) : null;
  if (!b) return json({ ok: false, erro: "Vídeo não encontrado." }, 404);
  const nomeArq = `clipe-do-pet-${(p.nome || "pet").normalize("NFD").replace(/[^\w]+/g, "-").toLowerCase()}.mp4`;
  const base = { "content-type": "video/mp4", "accept-ranges": "bytes", "cache-control": "private, max-age=3600",
                 ...(u.searchParams.get("download") ? { "content-disposition": `attachment; filename="${nomeArq}"` } : {}) };
  const m = /^bytes=(\d*)-(\d*)$/.exec(request.headers.get("range") || "");
  if (m) {
    const total = b.byteLength;
    let ini = m[1] === "" ? total - parseInt(m[2], 10) : parseInt(m[1], 10);
    let fim = m[1] !== "" && m[2] !== "" ? parseInt(m[2], 10) : total - 1;
    if (ini < 0 || ini >= total || fim < ini) return new Response(null, { status: 416, headers: { "content-range": `bytes */${total}` } });
    fim = Math.min(fim, total - 1);
    return new Response(b.slice(ini, fim + 1), { status: 206, headers: { ...base, "content-range": `bytes ${ini}-${fim}/${total}`, "content-length": String(fim - ini + 1) } });
  }
  return new Response(b, { headers: { ...base, "content-length": String(b.byteLength) } });
}

// Utilidades do motor "Clipe do Pet" (Cloudflare Pages Functions + KV). Sem dependências; roda também no Node 20+.
export const json = (obj, status = 200, extra = {}) =>
  new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra } });

export function novoId(n = 12) {
  const alfabeto = "abcdefghjkmnpqrstuvwxyz23456789";
  return [...crypto.getRandomValues(new Uint8Array(n))].map((x) => alfabeto[x % alfabeto.length]).join("");
}

export const limpar = (s, max) =>
  String(s ?? "").replace(/[\u0000-\u001f<>{}\[\]`$\\|]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);

export function iguais(a, b) {
  a = String(a ?? ""); b = String(b ?? "");
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

// Worker (GitHub Actions) autentica com o mesmo segredo da música: TICK_SECRET no Cloudflare = MUSICA_TICK_SECRET no GitHub.
export function autorizado(request, env) {
  const h = request.headers.get("authorization") || "";
  const tok = h.startsWith("Bearer ") ? h.slice(7) : "";
  return !!env.TICK_SECRET && iguais(tok, env.TICK_SECRET);
}

export const baseUrl = (env) => (env.PUBLIC_BASE_URL || "https://tutorialpet.com.br").replace(/\/$/, "");

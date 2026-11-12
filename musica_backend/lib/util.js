// Utilidades compartilhadas do motor "Música do Seu Pet". Sem dependências (roda no Cloudflare Pages Functions e no Node 20+).
export const json = (obj, status = 200, extra = {}) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra },
  });

export function novoId() {
  const alfabeto = "abcdefghjkmnpqrstuvwxyz23456789";
  const b = crypto.getRandomValues(new Uint8Array(12));
  return [...b].map((x) => alfabeto[x % alfabeto.length]).join("");
}

// Remove caracteres de controle e colchetes/chaves (colchetes são tags de estrutura da letra) e limita o tamanho.
export const limpar = (s, max) =>
  String(s ?? "").replace(/[\u0000-\u001f<>{}\[\]`$\\|]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);

export function semAcento(s) {
  return String(s ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "");
}

export function slugArquivo(nome) {
  const s = semAcento(nome).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
  return s || "pet";
}

export async function hmacHex(algoritmo, chave, dados) {
  const enc = new TextEncoder();
  const k = await crypto.subtle.importKey("raw", enc.encode(chave), { name: "HMAC", hash: algoritmo }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", k, typeof dados === "string" ? enc.encode(dados) : dados);
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export function iguais(a, b) {
  a = String(a ?? ""); b = String(b ?? "");
  if (a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
export const baseUrl = (env) => (env.PUBLIC_BASE_URL || "https://tutorialpet.com.br").replace(/\/$/, "");
export const linkEntrega = (env, id) => `${baseUrl(env)}/musica-do-seu-pet/entrega/${id}`;

export function autorizado(request, env) {
  const h = request.headers.get("authorization") || "";
  const tok = h.startsWith("Bearer ") ? h.slice(7) : "";
  return !!env.TICK_SECRET && iguais(tok, env.TICK_SECRET);
}

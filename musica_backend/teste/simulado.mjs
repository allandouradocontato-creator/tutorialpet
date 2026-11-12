// Teste simulado do motor (sem chaves reais): KV em memória + fetch falso de fal/Mureka/Brevo/ntfy.
// Prova a máquina de estados: formulário -> webhook Kiwify assinado -> geração -> conversão -> entrega, e o fallback entre provedores.
import { onRequestPost as pedidoPost } from "../../functions/api/musica/pedido.js";
import { onRequestPost as kiwifyPost } from "../../functions/api/musica/kiwify.js";
import { onRequestGet as entregaGet } from "../../functions/api/musica/entrega.js";
import { onRequestGet as mp3Get } from "../../functions/api/musica/mp3.js";
import { onRequestPost as tickPost } from "../../functions/api/musica/tick.js";
import { onRequestPost as uploadPost } from "../../functions/api/musica/mp3-upload.js";
import { hmacHex } from "../lib/util.js";
import assert from "node:assert/strict";

class KV {
  m = new Map();
  async get(k, o) { const v = this.m.get(k); if (v === undefined) return null; return o?.type === "arrayBuffer" ? (v instanceof Uint8Array ? v.buffer.slice(v.byteOffset, v.byteOffset + v.byteLength) : new TextEncoder().encode(v).buffer) : (typeof v === "string" ? v : new TextDecoder().decode(v)); }
  async put(k, v) { this.m.set(k, v); }
  async delete(k) { this.m.delete(k); }
  async list({ prefix }) { return { keys: [...this.m.keys()].filter((k) => k.startsWith(prefix)).map((name) => ({ name })), list_complete: true }; }
}
const mp3Falso = new Uint8Array(60000).fill(7);
const log = []; let falModo = "ok", murekaModo = "ok";
globalThis.fetch = async (url, init = {}) => {
  url = String(url); log.push(`${init.method || "GET"} ${url.split("?")[0]}`);
  const J = (o, s = 200) => new Response(JSON.stringify(o), { status: s });
  if (url === "https://queue.fal.run/s/req1") return J({ status: "COMPLETED" });
  if (url === "https://queue.fal.run/r/req1") return J({ audio: { url: "https://v3.fal.media/files/x/out.flac", content_type: "audio/flac" }, duration: 150 });
  if (url.startsWith("https://queue.fal.run/fal-ai")) return falModo === "ok" ? J({ request_id: "req1", status_url: "https://queue.fal.run/s/req1", response_url: "https://queue.fal.run/r/req1" }) : J({ detail: "Exhausted balance" }, 403);
  if (url === "https://queue.fal.run/s/req1") return J({ status: "COMPLETED" });
  if (url === "https://queue.fal.run/r/req1") return J({ audio: { url: "https://v3.fal.media/files/x/out.flac", content_type: "audio/flac" }, duration: 150 });
  if (url === "https://api.mureka.ai/v1/song/generate") return murekaModo === "ok" ? J({ id: "m1", status: "preparing" }) : J({ error: "x" }, 500);
  if (url.startsWith("https://api.mureka.ai/v1/song/query/")) return J({ status: "succeeded", choices: [{ url: "https://cdn.mureka.ai/o.mp3", duration: 140000 }] });
  if (url.endsWith(".mp3")) return new Response(mp3Falso, { headers: { "content-type": "audio/mpeg" } });
  if (url.endsWith(".flac")) return new Response(mp3Falso);
  if (url === "https://api.brevo.com/v3/smtp/email") return J({ messageId: "b1" }, 201);
  if (url.startsWith("https://ntfy.sh/")) return J({ ok: 1 });
  throw new Error("fetch inesperado: " + url);
};

const env = { PEDIDOS: new KV(), FAL_KEY: "k", MUREKA_API_KEY: "k", MUSIC_PROVIDERS: "fal,mureka", KIWIFY_CHECKOUT_URL: "https://pay.kiwify.com.br/TESTE",
  KIWIFY_WEBHOOK_TOKEN: "tok", TICK_SECRET: "tick", BREVO_API_KEY: "b", NTFY_TOPIC: "t", FAL_USE_WEBHOOK: "0", PUBLIC_BASE_URL: "https://tutorialpet.com.br" };
const pend = []; const waitUntil = (p) => pend.push(p);
const esperar = async () => { while (pend.length) await pend.shift(); };
const post = (url, body, extra = {}) => new Request(url, { method: "POST", body: typeof body === "string" ? body : JSON.stringify(body), ...extra });

async function fluxo(nome, bump) {
  const form = { nomePet: "Thor", especie: "cachorro", raca: "Golden", manias: ["rouba meia", "late para o carteiro", "dorme de barriga pra cima"], tutor: "Allan",
    estilo: "pop alegre", estilo2: "forró", voz: "feminina", clima: "animada", whatsapp: "(85) 99999-0000", email: "cliente@exemplo.com" };
  const r = await (await pedidoPost({ request: post("https://x/api/musica/pedido", form), env })).json();
  assert.ok(r.ok && r.checkoutUrl.includes("src=" + r.id), "checkout leva o ID do pedido");
  const payload = { order_id: "K-" + nome, order_status: "paid", webhook_event_type: "order_approved", Customer: { email: form.email },
    TrackingParameters: { src: r.id }, Product: { product_name: "Música do Seu Pet" }, ...(bump ? { Bump: "2ª versão em outro estilo" } : {}) };
  const raw = JSON.stringify(payload);
  const ruim = await kiwifyPost({ request: post("https://x/api/musica/kiwify?signature=errada", raw), env, waitUntil });
  assert.equal(ruim.status, 401, "assinatura errada é recusada");
  const sig = await hmacHex("SHA-1", "tok", raw);
  const ok = await kiwifyPost({ request: post("https://x/api/musica/kiwify?signature=" + sig, raw), env, waitUntil });
  assert.equal(ok.status, 200); await esperar();
  const dup = await (await kiwifyPost({ request: post("https://x/api/musica/kiwify?signature=" + sig, raw), env, waitUntil })).json();
  assert.ok(dup.ignorado, "reenvio do mesmo pedido é ignorado");
  return r.id;
}
const ver = async (id) => (await (await entregaGet({ request: new Request("https://x/api/musica/entrega?id=" + id), env })).json());

// 1) caminho feliz com fal (retorna FLAC -> precisa conversão -> upload do mp3 convertido pelo tick/workflow)
let id = await fluxo("a", true);
let v = await ver(id);
console.log("após pagamento:", v.estado, v.versoes.map((x) => x.estado + ":" + x.estilo));
assert.equal(v.versoes.length, 2); assert.equal(v.versoes[1].estilo, "forró");
const t = await (await tickPost({ request: post("https://x/api/musica/tick", "", { headers: { authorization: "Bearer tick" } }), env, waitUntil })).json();
console.log("tick:", JSON.stringify(t));
assert.equal(t.converter.length, 2, "2 arquivos aguardam conversão para mp3");
for (const c of t.converter) {
  const up = await uploadPost({ request: post(`https://x/api/musica/mp3-upload?id=${c.id}&n=${c.n}`, mp3Falso, { headers: { authorization: "Bearer tick" } }), env });
  assert.equal((await up.json()).ok, true);
}
v = await ver(id);
assert.equal(v.estado, "entregue"); assert.ok(v.versoes[0].letra.includes("Thor")); assert.equal(v.versoes[0].arquivo, "musica-do-thor.mp3"); assert.equal(v.versoes[1].arquivo, "musica-do-thor-2.mp3");
const dl = await mp3Get({ request: new Request(`https://x/api/musica/mp3?id=${id}&n=1&baixar=1`), env });
assert.equal(dl.headers.get("content-type"), "audio/mpeg"); assert.match(dl.headers.get("content-disposition"), /musica-do-thor\.mp3/);
const rg = await mp3Get({ request: new Request(`https://x/api/musica/mp3?id=${id}&n=1`, { headers: { range: "bytes=0-99" } }), env });
assert.equal(rg.status, 206);
assert.ok(log.some((l) => l.includes("api.brevo.com")), "e-mail transacional enviado");
console.log("OK 1: fal -> conversão -> entrega, 2 versões, e-mail, download, range");

// 2) fal falha (saldo) -> cai sozinho na Mureka (mp3 direto)
falModo = "falha"; log.length = 0;
id = await fluxo("b", false); v = await ver(id);
console.log("fallback:", v.estado, v.versoes.map((x) => x.estado));
v = await ver(id);
assert.equal(v.estado, "entregue", "Mureka assumiu quando o fal falhou");
console.log("OK 2: fallback fal -> Mureka");

// 3) todos falham -> alerta ao Allan (ntfy) e estado falhou; depois recupera na nova rodada
murekaModo = "falha"; log.length = 0;
id = await fluxo("c", false); v = await ver(id);
assert.equal(v.estado, "falhou"); assert.ok(log.some((l) => l.includes("ntfy.sh")), "alerta enviado fora do Gmail");
falModo = "ok";
const p = JSON.parse(await env.PEDIDOS.get("p:" + id)); p.versoes[0].falhouEm = Date.now() - 11 * 60000; await env.PEDIDOS.put("p:" + id, JSON.stringify(p));
const t2 = await (await tickPost({ request: post("https://x/api/musica/tick", "", { headers: { authorization: "Bearer tick" } }), env, waitUntil })).json();
console.log("tick após falha:", JSON.stringify(t2));
assert.equal(t2.retentativas ?? t2.retentados, 1);
console.log("OK 3: alerta + nova tentativa automática");

// 4) segurança do formulário
const bad = await (await pedidoPost({ request: post("https://x/api/musica/pedido", { nomePet: "Rex", especie: "cachorro", manias: ["canta igual Anitta"], estilo: "rock", voz: "masculina", clima: "animada", email: "a@b.co", whatsapp: "85999990000" }), env })).json();
assert.equal(bad.ok, false); console.log("OK 4: filtro de campos:", bad.erro);
console.log("TODOS OS TESTES SIMULADOS PASSARAM");

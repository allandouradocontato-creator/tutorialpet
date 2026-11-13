// Servidor local de teste: roda as rotas reais de functions/api/clipe/* com um KV em memória.
// Uso: TICK_SECRET=x CONVITES_TESTE=AMIGOPET:10 node clipe_backend/teste/servidor_local.mjs [porta]
import http from "node:http";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const aqui = path.dirname(fileURLToPath(import.meta.url));
const raiz = path.resolve(aqui, "../..");
const store = new Map();
const kv = {
  async get(k, o) { const v = store.get(k); if (v === undefined) return null; if (o?.type === "arrayBuffer") return v instanceof Uint8Array ? v.buffer.slice(v.byteOffset, v.byteOffset + v.byteLength) : new TextEncoder().encode(v).buffer; return v instanceof Uint8Array ? new TextDecoder().decode(v) : v; },
  async put(k, v) { store.set(k, v instanceof ArrayBuffer ? new Uint8Array(v) : v); },
  async delete(k) { store.delete(k); },
  async list({ prefix = "" } = {}) { return { keys: [...store.keys()].filter((x) => x.startsWith(prefix)).map((name) => ({ name })), list_complete: true }; },
};
const env = { PEDIDOS: kv, TICK_SECRET: process.env.TICK_SECRET || "segredo-teste", CONVITES_TESTE: process.env.CONVITES_TESTE || "AMIGOPET:10" };

const rotas = {};
for (const n of ["pedido", "foto", "midia-video", "enviar", "fila", "andamento", "video-upload", "status", "video"]) rotas[n] = await import(pathToFileURL(path.join(raiz, "functions/api/clipe", n + ".js")));

http.createServer(async (req, res) => {
  try {
    const chunks = []; for await (const c of req) chunks.push(c);
    const body = Buffer.concat(chunks);
    const url = `http://localhost${req.url}`;
    const caminho = new URL(url).pathname;
    if (!caminho.startsWith("/api/clipe/")) { // página estática (clipe/pagina)
      const arq = path.join(raiz, "clipe/pagina", caminho === "/" ? "index.html" : caminho);
      if (!arq.startsWith(path.join(raiz, "clipe/pagina")) || !fs.existsSync(arq)) { res.writeHead(404); return res.end("não encontrado"); }
      const tipos = { ".html": "text/html; charset=utf-8", ".mp4": "video/mp4", ".jpg": "image/jpeg" };
      res.writeHead(200, { "content-type": tipos[path.extname(arq)] || "application/octet-stream" });
      return res.end(fs.readFileSync(arq));
    }
    const nome = caminho.replace(/^\/api\/clipe\//, "");
    const mod = rotas[nome];
    const handler = mod?.["onRequest" + req.method[0] + req.method.slice(1).toLowerCase()];
    if (!handler) { res.writeHead(404); return res.end("sem rota"); }
    const r = await handler({ request: new Request(url, { method: req.method, headers: req.headers, body: ["GET", "HEAD"].includes(req.method) ? undefined : body }), env, waitUntil: () => {} });
    res.writeHead(r.status, Object.fromEntries(r.headers));
    res.end(Buffer.from(await r.arrayBuffer()));
  } catch (e) { res.writeHead(500); res.end(String(e.stack || e)); }
}).listen(parseInt(process.argv[2] || "8799", 10), () => console.log("servidor de teste no ar"));

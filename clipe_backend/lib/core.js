// Clipe do Pet — pedido, fotos, fila, andamento e entrega.
// Estados: recebendo (aguardando as fotos) -> na_fila -> processando -> entregue | falhou.
// Armazenamento: KV `PEDIDOS` (o mesmo da música), chaves clp:<id> (pedido), clf:<id>:<n> (foto), clv:<id> (vídeo).
// Créditos de teste: MESMO saldo e mesma variável da música (CONVITES_TESTE="AMIGOPET:10", chave cv:<CODIGO>); 1 clipe = 1 crédito,
// devolvido se o clipe falhar. Sem convite e sem checkout configurado, o pedido é recusado ("em breve").
import { novoId, limpar, iguais } from "./util.js";

export const MOLDES = { homenagem: "Homenagem", aniversario: "Aniversário", retrospectiva: "Retrospectiva", um_dia: "Um dia com o pet", diversao: "Diversão" };
// Vídeos do cliente ficam no KV (limite do KV = 25 MiB por valor; R2 não está ativado na conta): até 3 vídeos de 20 MB, no total até 8 mídias.
export const LIMITES = { fotosMin: 0, fotosMax: 6, videosMax: 3, midiasMin: 2, midiasMax: 8, bytesFoto: 1_500_000, bytesVideo: 20 * 1024 * 1024, travadoMs: 25 * 60 * 1000, ttl: 60 * 60 * 24 * 30 };

const k = { ped: (id) => "clp:" + id, foto: (id, n) => `clf:${id}:${n}`, vid: (id) => "clv:" + id, vcli: (id, n) => `clq:${id}:${n}` }; // clq = vídeo ENVIADO pelo cliente; clv = clipe final entregue

export async function getPedido(env, id) {
  if (!/^[a-z0-9]{8,20}$/.test(String(id))) return null;
  const s = await env.PEDIDOS.get(k.ped(id));
  return s ? JSON.parse(s) : null;
}
export async function salvar(env, p) {
  p.atualizadoEm = Date.now();
  await env.PEDIDOS.put(k.ped(p.id), JSON.stringify(p), { expirationTtl: LIMITES.ttl });
}

// ----- créditos (compatível com a música) -----
function mapaConvites(env) {
  const m = {};
  String(env.CONVITES_TESTE || "").split(",").forEach((t) => { const [c, n] = t.split(":"); if (c && c.trim()) m[c.trim().toUpperCase()] = Math.max(0, parseInt(n, 10) || 0); });
  return m;
}
async function usarCredito(env, codigo) {
  const m = mapaConvites(env);
  if (!(codigo in m)) return { ok: false, erro: "Convite inválido." };
  const atual = await env.PEDIDOS.get("cv:" + codigo);
  const saldo = atual === null ? m[codigo] : parseInt(atual, 10) || 0;
  if (saldo <= 0) return { ok: false, erro: "Os créditos de teste deste convite acabaram. Obrigado por testar!" };
  await env.PEDIDOS.put("cv:" + codigo, String(saldo - 1));
  return { ok: true, restantes: saldo - 1 };
}
async function devolverCredito(env, codigo) {
  const atual = parseInt((await env.PEDIDOS.get("cv:" + codigo)) ?? "0", 10) || 0;
  await env.PEDIDOS.put("cv:" + codigo, String(atual + 1));
}

// ----- criação -----
export async function criarPedido(env, b) {
  if (b.site) return { ok: true, id: novoId(), token: novoId(16), fantasma: true }; // honeypot
  const molde = String(b.molde || "");
  if (!MOLDES[molde]) return { ok: false, campo: "molde", erro: "Escolha o tipo de clipe." };
  const nome = limpar(b.nome, 30);
  if (nome.length < 2) return { ok: false, campo: "nome", erro: "Conte o nome do seu pet." };
  const fotos = parseInt(b.fotos, 10) || 0;
  const videos = parseInt(b.videos, 10) || 0;
  if (fotos < 0 || fotos > LIMITES.fotosMax) return { ok: false, campo: "fotos", erro: `Envie até ${LIMITES.fotosMax} fotos.` };
  if (videos < 0 || videos > LIMITES.videosMax) return { ok: false, campo: "fotos", erro: `Envie até ${LIMITES.videosMax} vídeos.` };
  if (fotos + videos < LIMITES.midiasMin || fotos + videos > LIMITES.midiasMax) return { ok: false, campo: "fotos", erro: `Envie de ${LIMITES.midiasMin} a ${LIMITES.midiasMax} fotos e vídeos.` };
  // ordem em que o cliente escolheu (f = foto, v = vídeo); sem ela, fotos primeiro (clientes antigos)
  let ordem = String(b.ordem || "").toLowerCase();
  if (!ordem) ordem = "f".repeat(fotos) + "v".repeat(videos);
  if (!/^[fv]+$/.test(ordem) || ordem.length !== fotos + videos || (ordem.match(/f/g) || []).length !== fotos) return { ok: false, campo: "fotos", erro: "Ordem das mídias inválida." };
  const conv = String(b.convite || "").trim().toUpperCase().slice(0, 40);
  if (!conv) return { ok: false, campo: "geral", erro: "A compra do clipe abre em breve. Por enquanto só com convite de teste." };
  const c = await usarCredito(env, conv);
  if (!c.ok) return { ok: false, campo: "convite", erro: c.erro };
  const p = { id: novoId(), token: novoId(16), criadoEm: Date.now(), estado: "recebendo", molde, nome, frase: limpar(b.frase, 80), fotos, videos, ordem, enviadas: [], enviadasV: [], convite: conv, etapa: "Aguardando suas fotos e vídeos", log: [] };
  await salvar(env, p);
  return { ok: true, id: p.id, token: p.token, creditosRestantes: c.restantes };
}

// ----- fotos -----
const ehJpeg = (u8) => u8.length > 4 && u8[0] === 0xff && u8[1] === 0xd8;
export async function receberFoto(env, id, token, n, bytes) {
  const p = await getPedido(env, id);
  if (!p || !iguais(token, p.token)) return { ok: false, status: 403, erro: "Pedido inválido." };
  if (p.estado !== "recebendo") return { ok: false, status: 409, erro: "Este pedido já foi enviado." };
  n = parseInt(n, 10);
  if (!(n >= 1 && n <= p.fotos)) return { ok: false, status: 400, erro: "Número de foto inválido." };
  const u8 = new Uint8Array(bytes);
  if (u8.length > LIMITES.bytesFoto) return { ok: false, status: 413, erro: "Foto grande demais (máx. 1,5 MB)." };
  if (!ehJpeg(u8)) return { ok: false, status: 415, erro: "A foto precisa ser JPEG." };
  await env.PEDIDOS.put(k.foto(id, n), u8, { expirationTtl: LIMITES.ttl });
  if (!p.enviadas.includes(n)) p.enviadas.push(n);
  await salvar(env, p);
  return { ok: true, enviadas: p.enviadas.length, total: p.fotos };
}
export async function lerFoto(env, id, n) {
  return env.PEDIDOS.get(k.foto(id, parseInt(n, 10)), { type: "arrayBuffer" });
}

// ----- vídeos do cliente (mp4/mov/webm) -----
function ehVideo(u8) {
  if (u8.length < 12) return false;
  const ftyp = u8[4] === 0x66 && u8[5] === 0x74 && u8[6] === 0x79 && u8[7] === 0x70; // mp4 / mov / m4v
  const webm = u8[0] === 0x1a && u8[1] === 0x45 && u8[2] === 0xdf && u8[3] === 0xa3;
  return ftyp || webm;
}
export async function receberVideoCliente(env, id, token, n, bytes) {
  const p = await getPedido(env, id);
  if (!p || !iguais(token, p.token)) return { ok: false, status: 403, erro: "Pedido inválido." };
  if (p.estado !== "recebendo") return { ok: false, status: 409, erro: "Este pedido já foi enviado." };
  n = parseInt(n, 10);
  if (!(n >= 1 && n <= (p.videos || 0))) return { ok: false, status: 400, erro: "Número de vídeo inválido." };
  const u8 = new Uint8Array(bytes);
  if (u8.length > LIMITES.bytesVideo) return { ok: false, status: 413, erro: `Vídeo grande demais (máx. ${LIMITES.bytesVideo / 1048576} MB). Mande um trecho mais curto ou grave em qualidade menor.` };
  if (!ehVideo(u8)) return { ok: false, status: 415, erro: "O vídeo precisa ser MP4 ou MOV." };
  await env.PEDIDOS.put(k.vcli(id, n), u8, { expirationTtl: LIMITES.ttl });
  p.enviadasV = p.enviadasV || [];
  if (!p.enviadasV.includes(n)) p.enviadasV.push(n);
  await salvar(env, p);
  return { ok: true, enviados: p.enviadasV.length, total: p.videos };
}
export async function lerVideoCliente(env, id, n) {
  return env.PEDIDOS.get(k.vcli(id, parseInt(n, 10)), { type: "arrayBuffer" });
}

export async function enviarPedido(env, id, token, ctx) {
  const p = await getPedido(env, id);
  if (!p || !iguais(token, p.token)) return { ok: false, status: 403, erro: "Pedido inválido." };
  if (p.estado !== "recebendo") return { ok: true, estado: p.estado };
  if (p.enviadas.length < p.fotos) return { ok: false, status: 400, erro: `Faltam fotos (${p.enviadas.length} de ${p.fotos}).` };
  if ((p.enviadasV || []).length < (p.videos || 0)) return { ok: false, status: 400, erro: `Faltam vídeos (${(p.enviadasV || []).length} de ${p.videos}).` };
  p.estado = "na_fila"; p.etapa = "Na fila para montar o clipe"; p.filaDesde = Date.now();
  await salvar(env, p);
  if (env.GH_DISPATCH_TOKEN) { // dispara o worker na hora; senão ele pega no próximo ciclo (a cada ~5 min)
    const f = fetch(`https://api.github.com/repos/${env.GH_REPO || "allandouradocontato-creator/tutorialpet"}/actions/workflows/clipe_worker.yml/dispatches`, {
      method: "POST",
      headers: { authorization: `Bearer ${env.GH_DISPATCH_TOKEN}`, accept: "application/vnd.github+json", "user-agent": "tutorialpet-clipe", "content-type": "application/json" },
      body: JSON.stringify({ ref: "main" }),
    }).catch(() => {});
    if (ctx?.waitUntil) ctx.waitUntil(f); else await f;
  }
  return { ok: true, estado: p.estado };
}

// ----- fila e andamento (worker) -----
export async function fila(env) {
  const saida = [];
  let cursor;
  do {
    const lst = await env.PEDIDOS.list({ prefix: "clp:", cursor });
    for (const key of lst.keys) {
      const p = await getPedido(env, key.name.slice(4));
      if (!p) continue;
      const travado = p.estado === "processando" && Date.now() - p.atualizadoEm > LIMITES.travadoMs;
      if (p.estado === "na_fila" || travado) saida.push({ id: p.id, molde: p.molde, nome: p.nome, frase: p.frase, fotos: p.fotos, videos: p.videos || 0, ordem: p.ordem || "f".repeat(p.fotos), desde: p.filaDesde || p.criadoEm });
    }
    cursor = lst.list_complete ? undefined : lst.cursor;
  } while (cursor);
  return saida.sort((a, b) => a.desde - b.desde);
}

export async function andamento(env, id, { estado, etapa, msg }) {
  const p = await getPedido(env, id);
  if (!p) return { ok: false, status: 404 };
  if (["entregue", "falhou"].includes(p.estado)) return { ok: true, ignorado: true };
  if (estado === "processando") { p.estado = "processando"; p.etapa = limpar(etapa, 80) || p.etapa; p.msg = limpar(msg, 160); }
  if (estado === "falhou") {
    p.estado = "falhou"; p.etapa = "Não foi possível criar o clipe"; p.erro = limpar(msg, 200);
    if (p.convite && !p.creditoDevolvido) { await devolverCredito(env, p.convite); p.creditoDevolvido = true; }
  }
  await salvar(env, p);
  return { ok: true };
}

export async function guardarVideo(env, id, bytes, { animadas, total }) {
  const p = await getPedido(env, id);
  if (!p) return { ok: false, status: 404, erro: "Pedido não encontrado." };
  await env.PEDIDOS.put(k.vid(id), bytes, { expirationTtl: LIMITES.ttl });
  p.estado = "entregue"; p.etapa = "Pronto!"; p.msg = ""; p.animadas = animadas; p.total = total; p.entregueEm = Date.now();
  await salvar(env, p);
  for (let n = 1; n <= p.fotos; n++) await env.PEDIDOS.delete(k.foto(id, n)); // privacidade: apaga as fotos e os vídeos do cliente após a entrega
  for (let n = 1; n <= (p.videos || 0); n++) await env.PEDIDOS.delete(k.vcli(id, n));
  return { ok: true };
}
export async function lerVideo(env, id) {
  return env.PEDIDOS.get(k.vid(id), { type: "arrayBuffer" });
}

export async function statusPublico(env, id) {
  const p = await getPedido(env, id);
  if (!p) return null;
  let posicao = null;
  if (p.estado === "na_fila") { const f = await fila(env); posicao = f.findIndex((x) => x.id === id) + 1 || null; }
  return { estado: p.estado, etapa: p.etapa, msg: p.msg || "", nome: p.nome, molde: p.molde, fotos: p.fotos, videos: p.videos || 0, posicao, erro: p.erro || "",
           animadas: p.animadas ?? null, video: p.estado === "entregue" ? `/api/clipe/video?id=${p.id}` : null };
}

// Pedido e entrega. Estados: aguardando_pagamento -> letra (pago; cliente gera/ajusta/aprova a letra) -> pago -> gerando -> entregue | falhou.
// Cada pedido tem 1 ou 2 "versões" (a 2ª é o order bump: outro estilo). O avanço é idempotente e pode ser chamado por
// webhook da Kiwify, webhook do fal, página de entrega (consulta) ou tick agendado (GitHub Actions).
import { novoId, limpar, slugArquivo, hmacHex, iguais, linkEntrega, baseUrl } from "./util.js";
import { proibidoNoCampo } from "./filtro.js";
import { ESTILOS, CLIMAS, VOZES, lista } from "./estilos.js";
import { gerarLetra, validarLetraEditada } from "./letra.js";
import { PROVEDORES, cadeia, pedidoPadrao } from "./provedores/index.js";
import { alertar, enviarEmailEntrega, enviarEmailLetra, mensagemWhatsApp } from "./notificar.js";

const MIN = 60 * 1000;
export const LIMITES = { tempoProvedor: 7 * MIN, tempoConversao: 15 * MIN, esperaRetry: 10 * MIN, rodadasMax: 3 };

// ---------- armazenamento (Cloudflare KV, binding PEDIDOS) ----------
export async function getPedido(env, id) {
  if (!/^[a-z0-9]{8,20}$/.test(String(id))) return null;
  const s = await env.PEDIDOS.get("p:" + id);
  return s ? JSON.parse(s) : null;
}
export async function salvar(env, p) {
  p.atualizadoEm = Date.now();
  await env.PEDIDOS.put("p:" + p.id, JSON.stringify(p));
}
const chaveMp3 = (id, n) => `mp3:${id}:${n}`;

// ---------- criação do pedido (formulário) ----------
export function validarFormulario(b, opts = {}) {
  const exigirContato = opts.contato !== false;
  const erro = (campo, msg) => ({ ok: false, campo, erro: msg });
  const nomePet = limpar(b.nomePet, 30);
  if (nomePet.length < 2) return erro("nomePet", "Conte o nome de quem vai ganhar a música.");
  // Destinatário aberto (12/11/2026, Allan): pet, namorada(o), amigo, família, piada... O foco é o nicho pet, mas o formulário não restringe.
  const especie = String(b.especie || "outro").toLowerCase();
  if (!["cachorro", "gato", "outro-pet", "pessoa", "outro"].includes(especie)) return erro("especie", "Escolha para quem é a música.");
  const manias = (Array.isArray(b.manias) ? b.manias : []).map((m) => limpar(m, 60)).filter(Boolean).slice(0, 3);
  const historia = limpar(b.historia, 1200); // campo livre (12/11/2026, Allan): "conte a sua história que a gente canta para você"
  if (manias.length < 1 && historia.length < 20) return erro("manias", "Conte pelo menos uma mania ou um pouquinho da história.");
  const estilo = String(b.estilo || "");
  if (!ESTILOS[estilo]) return erro("estilo", "Escolha o estilo da música.");
  const estilo2 = b.estilo2 ? String(b.estilo2) : "";
  if (estilo2 && !ESTILOS[estilo2]) return erro("estilo2", "Estilo da 2ª versão inválido.");
  const voz = String(b.voz || "");
  if (!VOZES[voz]) return erro("voz", "Escolha a voz.");
  const clima = String(b.clima || "");
  if (!CLIMAS[clima]) return erro("clima", "Escolha o clima.");
  const email = limpar(b.email, 120).toLowerCase();
  if (exigirContato && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return erro("email", "Informe um e-mail válido para receber a música.");
  const whatsapp = String(b.whatsapp || "").replace(/\D/g, "");
  if (exigirContato && (whatsapp.length < 10 || whatsapp.length > 13)) return erro("whatsapp", "Informe seu WhatsApp com DDD.");
  const form = { nomePet, especie, raca: limpar(b.raca, 40), manias, historia, tutor: limpar(b.tutor, 30), estilo, estilo2, voz, clima, email, whatsapp };
  for (const t of [nomePet, form.raca, form.tutor, historia, ...manias]) {
    if (t && proibidoNoCampo(t)) return erro("manias", "Use palavras carinhosas ou divertidas (sem nomes de artistas ou termos ofensivos).");
  }
  return { ok: true, form };
}

export async function criarPedido(env, body, ctx) {
  if (body.site) return { ok: true, id: novoId(), checkoutUrl: "/", fantasma: true }; // honeypot: bot recebe resposta "normal" e nada é salvo
  const v = validarFormulario(body);
  if (!v.ok) return v;
  const p = { id: novoId(), criadoEm: Date.now(), estado: "aguardando_pagamento", form: v.form, versoes: [], bump: false, log: [] };
  await salvar(env, p);
  await env.PEDIDOS.put("e:" + v.form.email, p.id, { expirationTtl: 60 * 60 * 24 * 30 });
  if (String(env.MUSICA_DEMO || "") === "1") {
    // MODO DEMONSTRAÇÃO (só prévia): pula a Kiwify, marca como pago e já gera (música de amostra) para ver o fluxo inteiro.
    p.versoes = [novaVersao(1, p.form.estilo)];
    p.estado = "letra"; p.demo = true;
    await salvar(env, p);
    return { ok: true, id: p.id, checkoutUrl: `/musica-do-seu-pet/entrega/${p.id}`, demo: true };
  }
  const base = env.KIWIFY_CHECKOUT_URL;
  if (!base) return { ok: false, erro: "Checkout indisponível no momento.", campo: "geral" };
  const u = new URL(base);
  u.searchParams.set("src", p.id);
  u.searchParams.set("sck", p.id);
  u.searchParams.set("email", v.form.email);
  return { ok: true, id: p.id, checkoutUrl: u.toString() };
}

// ---------- webhook da Kiwify ----------
export async function validarAssinaturaKiwify(env, request, rawBody) {
  const tok = env.KIWIFY_WEBHOOK_TOKEN;
  if (!tok) return false;
  const sig = new URL(request.url).searchParams.get("signature") || "";
  const esperado = await hmacHex("SHA-1", tok, rawBody);
  return iguais(sig.toLowerCase(), esperado);
}

const PROXIMO_ESTILO = { "pop alegre": "sertanejo", "sertanejo": "forró", "forró": "pop alegre", "mpb": "pop alegre", "rock": "pop alegre", "infantil": "pop alegre" };

export async function aplicarPagamento(env, payload, ctx) {
  const status = String(payload.order_status || "").toLowerCase();
  const evento = String(payload.webhook_event_type || "").toLowerCase();
  const aprovado = status === "paid" || evento === "order_approved";
  if (!aprovado) return { ok: true, ignorado: `evento ${evento || status || "?"}` };
  const orderId = String(payload.order_id || payload.order_ref || "");
  if (orderId && (await env.PEDIDOS.get("k:" + orderId))) return { ok: true, ignorado: "pedido Kiwify já processado" };
  const tp = payload.TrackingParameters || payload.tracking || {};
  let id = String(tp.src || tp.sck || "");
  let p = id ? await getPedido(env, id) : null;
  if (!p) {
    const email = String(payload.Customer?.email || "").toLowerCase();
    const idEmail = email ? await env.PEDIDOS.get("e:" + email) : null;
    p = idEmail ? await getPedido(env, idEmail) : null;
  }
  if (!p) {
    await alertar(env, "Música do Pet: pagamento sem pedido", `Kiwify ${orderId} aprovado, mas não achei o pedido (src=${id || "vazio"}). Cliente: ${payload.Customer?.email || "?"}`);
    return { ok: false, erro: "pedido não encontrado" };
  }
  if (p.estado !== "aguardando_pagamento") return { ok: true, ignorado: "pedido já pago" };
  const texto = JSON.stringify(payload);
  p.bump = /2[ªa]\s*vers[ãa]o/i.test(texto);
  p.kiwify = { orderId, pagoEm: Date.now() };
  const e1 = p.form.estilo;
  p.versoes = [novaVersao(1, e1)];
  if (p.bump) p.versoes.push(novaVersao(2, p.form.estilo2 && p.form.estilo2 !== e1 ? p.form.estilo2 : PROXIMO_ESTILO[e1] || "pop alegre"));
  p.estado = "letra"; // pago: o cliente agora gera/ajusta/aprova a letra e só então a música é criada
  await salvar(env, p);
  if (orderId) await env.PEDIDOS.put("k:" + orderId, p.id, { expirationTtl: 60 * 60 * 24 * 90 });
  await avisarLetra(env, p);
  return { ok: true, id: p.id };
}

const novaVersao = (n, estilo) => ({ n, estilo, estado: "pendente", idx: 0, rodadas: 0, tentativas: [] });

// ---------- avanço da máquina de estados ----------
export async function avancar(env, id, ctx) {
  const lockKey = "l:" + id;
  if (await env.PEDIDOS.get(lockKey)) return getPedido(env, id);
  await env.PEDIDOS.put(lockKey, String(Date.now()), { expirationTtl: 60 });
  try {
    const p = await getPedido(env, id);
    if (!p || !["pago", "gerando", "falhou"].includes(p.estado)) return p;
    for (const v of p.versoes) {
      if (["entregue", "falhou"].includes(v.estado)) continue;
      try { await avancarVersao(env, p, v, ctx); }
      catch (e) { v.tentativas.push(`erro inesperado: ${e.message}`); await falharProvedor(env, p, v, e.message); }
      await salvar(env, p);
    }
    await consolidar(env, p);
    await salvar(env, p);
    return p;
  } finally { await env.PEDIDOS.delete(lockKey); }
}

async function avancarVersao(env, p, v, ctx) {
  const provs = cadeia(env);
  if (v.estado === "pendente") {
    if (!provs.length) { v.estado = "falhou"; v.tentativas.push("nenhum provedor com chave configurada"); return; }
    const pad = pedidoPadrao(p.form, v.estilo);
    if (!v.letra && p.letraAprovada) {
      v.letra = p.letraAprovada.letra; v.titulo = p.letraAprovada.titulo; v.origemLetra = "aprovada-pelo-cliente";
    }
    if (!v.letra) {
      const l = await gerarLetra(pad, env);
      v.letra = l.letra; v.titulo = l.titulo; v.origemLetra = l.origem;
    }
    while (v.idx < provs.length) {
      const nome = provs[v.idx];
      try {
        const r = await PROVEDORES[nome].enviar(pad, v.letra, env, { webhookId: p.id });
        v.provedor = nome; v.iniciadoEm = Date.now();
        if (r.mp3Bytes) { await guardarBytes(env, p, v, r.mp3Bytes, "mp3", r.duracao); return; }
        v.job = r.jobId; v.estado = "gerando"; p.estado = "gerando";
        return;
      } catch (e) { v.tentativas.push(`${nome}: ${e.message}`); v.idx++; }
    }
    return falharCadeia(env, p, v);
  }
  if (v.estado === "gerando") {
    const nome = v.provedor;
    let s;
    try { s = await PROVEDORES[nome].consultar(v.job, env); }
    catch (e) { s = { estado: "erro", motivo: e.message }; }
    if (s.estado === "processando" || s.estado === "erro") {
      if (Date.now() - v.iniciadoEm > LIMITES.tempoProvedor) { v.tentativas.push(`${nome}: tempo esgotado${s.motivo ? " (" + s.motivo + ")" : ""}`); return trocarProvedor(v); }
      return;
    }
    if (s.estado === "falhou") { v.tentativas.push(`${nome}: ${s.motivo}`); return trocarProvedor(v); }
    // pronto
    v.duracao = s.duracao || null;
    const ehMp3 = /mpeg|mp3/i.test(s.contentType || "") || /\.mp3(\?|$)/i.test(s.audioUrl);
    if (ehMp3) {
      const bytes = await baixar(s.audioUrl);
      await guardarBytes(env, p, v, bytes, "mp3", s.duracao);
    } else {
      v.estado = "convertendo"; v.srcUrl = s.audioUrl; v.srcExt = extDe(s.audioUrl, s.contentType); v.convertendoDesde = Date.now();
      await pedirConversao(env, p, v);
    }
    return;
  }
  if (v.estado === "convertendo") {
    if (Date.now() - v.convertendoDesde > LIMITES.tempoConversao) {
      // não deixar o cliente esperando: entrega o arquivo original (formato honesto) e registra
      const bytes = await baixar(v.srcUrl);
      v.tentativas.push("conversão para MP3 não concluiu; entregue no formato original");
      await guardarBytes(env, p, v, bytes, v.srcExt || "wav", v.duracao);
    }
  }
}

function trocarProvedor(v) { v.idx++; v.estado = "pendente"; delete v.job; }
async function falharProvedor(env, p, v, motivo) { v.estado = "pendente"; v.idx = (v.idx || 0) + 1; await falharCadeia(env, p, v); }

async function falharCadeia(env, p, v) {
  if (v.idx < cadeia(env).length) return; // ainda há provedor na fila
  v.rodadas++;
  v.estado = "falhou"; v.falhouEm = Date.now();
}

async function consolidar(env, p) {
  if (p.versoes.every((v) => v.estado === "entregue")) {
    if (p.estado !== "entregue") {
      p.estado = "entregue"; p.entregueEm = Date.now();
      p.whatsappMsg = mensagemWhatsApp(env, p);
      const r = await enviarEmailEntrega(env, p).catch((e) => ({ ok: false, motivo: e.message }));
      p.email = r;
      if (!r.ok) await alertar(env, "Música do Pet: e-mail não enviado", `Pedido ${p.id} entregue na página, mas o e-mail falhou: ${r.motivo}. Link: ${linkEntrega(env, p.id)}`);
    }
    return;
  }
  const falhas = p.versoes.filter((v) => v.estado === "falhou");
  if (falhas.length && p.versoes.every((v) => ["entregue", "falhou"].includes(v.estado))) {
    const jaAvisou = p.estado === "falhou" && p.alertadoRodada === Math.max(...falhas.map((v) => v.rodadas));
    p.estado = "falhou";
    if (!jaAvisou) {
      p.alertadoRodada = Math.max(...falhas.map((v) => v.rodadas));
      const motivos = falhas.map((v) => `v${v.n}: ${v.tentativas.slice(-3).join(" / ")}`).join(" || ");
      const vaiTentar = falhas.every((v) => v.rodadas < LIMITES.rodadasMax);
      await alertar(env, "Música do Pet: geração FALHOU", `Pedido ${p.id} (${p.form.nomePet}) falhou em todos os provedores. ${vaiTentar ? "Nova tentativa automática em ~10 min." : "Tentativas esgotadas: precisa de atenção."} ${motivos}`.slice(0, 1400));
    }
  } else if (p.versoes.some((v) => ["gerando", "convertendo"].includes(v.estado))) p.estado = "gerando";
}

async function baixar(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`download ${r.status}`);
  const b = new Uint8Array(await r.arrayBuffer());
  if (b.length < 20000) throw new Error("áudio baixado vazio/curto");
  return b;
}
const extDe = (url, ct) => (/flac/i.test(ct) || /\.flac/i.test(url) ? "flac" : /ogg/i.test(url + ct) ? "ogg" : "wav");

async function guardarBytes(env, p, v, bytes, ext, duracao) {
  await env.PEDIDOS.put(chaveMp3(p.id, v.n), bytes);
  v.estado = "entregue"; v.formato = ext; v.duracao = duracao || v.duracao || null; v.entregueEm = Date.now();
  delete v.job; delete v.srcUrl;
}

export async function receberMp3Convertido(env, id, n, bytes) {
  const p = await getPedido(env, id);
  const v = p?.versoes.find((x) => x.n === Number(n));
  if (!v || v.estado === "entregue") return { ok: !!v, ignorado: true };
  if (bytes.length < 20000) throw new Error("mp3 convertido vazio");
  await guardarBytes(env, p, v, bytes, "mp3", v.duracao);
  await consolidar(env, p);
  await salvar(env, p);
  return { ok: true };
}

async function pedirConversao(env, p, v) {
  // Se houver token de despacho do GitHub, dispara o workflow de conversão na hora; senão o tick (a cada 5 min) busca em /api/musica/tick.
  if (!env.GH_DISPATCH_TOKEN) return;
  try {
    await fetch(`https://api.github.com/repos/${env.GH_REPO || "allandouradocontato-creator/tutorialpet"}/actions/workflows/musica_converter.yml/dispatches`, {
      method: "POST",
      headers: { authorization: `Bearer ${env.GH_DISPATCH_TOKEN}`, accept: "application/vnd.github+json", "user-agent": "tutorialpet-musica", "content-type": "application/json" },
      body: JSON.stringify({ ref: "main", inputs: { id: p.id, n: String(v.n), url: v.srcUrl, ext: v.srcExt || "wav" } }),
    });
  } catch { /* o tick cobre */ }
}

// ---------- tick (retries, travados, conversões pendentes) ----------
export async function tick(env, ctx) {
  const resumo = { avancados: 0, retentados: 0, converter: [] };
  let cursor;
  do {
    const lst = await env.PEDIDOS.list({ prefix: "p:", cursor });
    for (const k of lst.keys) {
      const p = JSON.parse((await env.PEDIDOS.get(k.name)) || "null");
      if (!p) continue;
      if (p.estado === "falhou") {
        const reabre = p.versoes.filter((v) => v.estado === "falhou" && v.rodadas < LIMITES.rodadasMax && Date.now() - (v.falhouEm || 0) > LIMITES.esperaRetry);
        if (reabre.length) { for (const v of reabre) { v.idx = 0; v.estado = "pendente"; v.tentativas.push("--- nova rodada ---"); } p.estado = "pago"; await salvar(env, p); resumo.retentados++; }
      }
      if (["pago", "gerando"].includes(p.estado)) { await avancar(env, p.id, ctx); resumo.avancados++; }
      const p2 = ["pago", "gerando"].includes(p.estado) ? await getPedido(env, p.id) : p;
      for (const v of p2.versoes) if (v.estado === "convertendo") resumo.converter.push({ id: p2.id, n: v.n, url: v.srcUrl, ext: v.srcExt || "wav" });
    }
    cursor = lst.list_complete ? undefined : lst.cursor;
  } while (cursor);
  return resumo;
}

// ---------- visão pública (página de entrega) ----------
export async function visaoPublica(env, id) {
  let p = await getPedido(env, id);
  if (!p) return null;
  if (["pago", "gerando"].includes(p.estado)) p = (await avancar(env, id)) || p; // avanço "preguiçoso" enquanto o cliente espera
  const nome = p.form.nomePet;
  return {
    id: p.id, estado: p.estado, nomePet: nome,
    rascunho: p.estado === "letra" ? p.rascunho : undefined,
    versoes: p.versoes.map((v) => ({
      n: v.n, estilo: v.estilo, estado: v.estado, titulo: v.titulo || `A música do ${nome}`, letra: v.estado === "entregue" ? v.letra : undefined,
      mp3Url: v.estado === "entregue" ? `/api/musica/mp3?id=${p.id}&n=${v.n}` : undefined,
      arquivo: v.estado === "entregue" ? nomeArquivo(p, v) : undefined,
    })),
    whatsappMsg: p.estado === "entregue" ? mensagemWhatsApp(env, p) : undefined,
  };
}

export function nomeArquivo(p, v) {
  const ext = v.formato || "mp3";
  return `musica-do-${slugArquivo(p.form.nomePet)}${v.n > 1 ? "-" + v.n : ""}.${ext}`;
}

export async function entregarMp3(env, request, id, n, baixarArq) {
  const p = await getPedido(env, id);
  const v = p?.versoes.find((x) => x.n === Number(n));
  if (!v || v.estado !== "entregue") return new Response("não encontrado", { status: 404 });
  const buf = await env.PEDIDOS.get(chaveMp3(id, v.n), { type: "arrayBuffer" });
  if (!buf) return new Response("arquivo indisponível", { status: 404 });
  const tipo = { mp3: "audio/mpeg", flac: "audio/flac", wav: "audio/wav", ogg: "audio/ogg" }[v.formato || "mp3"];
  const h = { "content-type": tipo, "accept-ranges": "bytes", "cache-control": "private, max-age=3600", "x-robots-tag": "noindex" };
  if (baixarArq) h["content-disposition"] = `attachment; filename="${nomeArquivo(p, v)}"`;
  const rg = /^bytes=(\d*)-(\d*)$/.exec(request.headers.get("range") || "");
  if (rg) {
    const ini = rg[1] ? Number(rg[1]) : 0, fim = rg[2] ? Math.min(Number(rg[2]), buf.byteLength - 1) : buf.byteLength - 1;
    return new Response(buf.slice(ini, fim + 1), { status: 206, headers: { ...h, "content-range": `bytes ${ini}-${fim}/${buf.byteLength}`, "content-length": String(fim - ini + 1) } });
  }
  return new Response(buf, { headers: { ...h, "content-length": String(buf.byteLength) } });
}


// ---------- letra depois do pagamento (decisão do Allan, 12/11/2026) ----------
// O cliente paga primeiro (compra imediata). Depois ele gera a letra, pede ajustes ou edita à mão quantas vezes quiser e só
// então aprova; a música é gerada em cima da letra aprovada. Isso é a garantia que dá segurança para pagar.
async function avisarLetra(env, p) {
  let r; try { r = await enviarEmailLetra(env, p); } catch (e) { r = { ok: false, motivo: e.message }; }
  if (!r.ok) await alertar(env, "Música do Pet: e-mail da letra não enviado", `Pedido ${p.id}: ${r.motivo}. Link: ${linkEntrega(env, p.id)}`);
}
export const LIMITE_LETRAS_POR_PEDIDO = 40;

export async function gerarLetraPedido(env, id, body) {
  const p = await getPedido(env, id);
  if (!p) return { ok: false, erro: "Pedido não encontrado." };
  if (p.estado !== "letra") return { ok: false, erro: p.estado === "aguardando_pagamento" ? "O pagamento ainda não foi confirmado." : "A letra deste pedido já foi aprovada." };
  p.letrasGeradas = p.letrasGeradas || 0;
  if (p.letrasGeradas >= LIMITE_LETRAS_POR_PEDIDO) return { ok: false, erro: "Chegamos ao limite de versões da letra deste pedido. Edite o texto direto ou fale com a gente no WhatsApp." };
  const ajuste = limpar(body?.ajuste, 400);
  if (ajuste && proibidoNoCampo(ajuste)) return { ok: false, erro: "Use palavras carinhosas ou divertidas no pedido de ajuste." };
  const anterior = body?.anterior ? String(body.anterior).replace(/\r/g, "").slice(0, 3800) : (p.rascunho?.letra || "");
  p.letrasGeradas++;
  await salvar(env, p);
  const l = await gerarLetra(pedidoPadrao(p.form, p.form.estilo), env, { ajuste, anterior: ajuste ? anterior : "" });
  const q = await getPedido(env, id);
  q.rascunho = { titulo: l.titulo, letra: l.letra };
  await salvar(env, q);
  return { ok: true, titulo: l.titulo, letra: l.letra, restantes: Math.max(0, LIMITE_LETRAS_POR_PEDIDO - q.letrasGeradas) };
}

export async function aprovarLetraPedido(env, id, body, ctx) {
  const p = await getPedido(env, id);
  if (!p) return { ok: false, erro: "Pedido não encontrado." };
  if (p.estado !== "letra") return { ok: false, erro: "A letra deste pedido já foi aprovada." };
  const le = validarLetraEditada(body?.letra);
  if (!le.ok) return le;
  p.letraAprovada = { letra: le.letra, titulo: limpar(body?.titulo, 80) || p.rascunho?.titulo || `A música do ${p.form.nomePet}` };
  p.estado = "pago";
  await salvar(env, p);
  const tarefa = avancar(env, p.id, ctx);
  if (ctx?.waitUntil) ctx.waitUntil(tarefa); else await tarefa;
  return { ok: true };
}

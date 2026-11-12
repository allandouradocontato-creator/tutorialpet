// Alerta ao Allan por canal que NÃO é o Gmail: ntfy.sh (push no celular) e/ou Telegram. E-mail transacional ao cliente: Brevo.
import { baseUrl, linkEntrega } from "./util.js";

export async function alertar(env, titulo, texto) {
  const feitos = [];
  try {
    if (env.NTFY_TOPIC) {
      const r = await fetch(`https://ntfy.sh/${encodeURIComponent(env.NTFY_TOPIC)}`, {
        method: "POST",
        headers: { Title: encodeURIComponent(titulo).slice(0, 200), Priority: "high", Tags: "warning,musical_note" },
        body: String(texto).slice(0, 1500),
      });
      feitos.push(`ntfy:${r.status}`);
    }
    if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
      const r = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text: `⚠️ ${titulo}\n${texto}`.slice(0, 3500) }),
      });
      feitos.push(`telegram:${r.status}`);
    }
  } catch (e) { feitos.push(`erro:${e.message}`); }
  if (!feitos.length) console.warn("[alerta sem canal configurado]", titulo, texto);
  return feitos;
}

export function mensagemWhatsApp(env, p) {
  const nome = p.form.nomePet;
  return `Olha só! A música do ${nome} ficou pronta 🐾🎶 Ouça e baixe aqui: ${linkEntrega(env, p.id)}`;
}

export async function enviarEmailEntrega(env, p) {
  if (!env.BREVO_API_KEY) return { ok: false, motivo: "BREVO_API_KEY ausente" };
  const link = linkEntrega(env, p.id);
  const nome = p.form.nomePet;
  const html = `<div style="font-family:Arial,sans-serif;max-width:520px;margin:auto;color:#222">
<h2 style="color:#e8590c">A música do ${esc(nome)} ficou pronta! 🐾🎶</h2>
<p>Preparamos uma música feita só para o ${esc(nome)}. Ouça, baixe o MP3 e compartilhe com quem ama o seu melhor amigo.</p>
<p style="text-align:center;margin:28px 0"><a href="${link}" style="background:#e8590c;color:#fff;padding:14px 26px;border-radius:10px;text-decoration:none;font-weight:bold">Ouvir e baixar a música</a></p>
<p style="font-size:13px;color:#666">Se o botão não abrir, copie este link: ${link}</p>
<p style="font-size:13px;color:#666">Tutorial Pet · ${baseUrl(env).replace("https://", "")}</p></div>`;
  const r = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST",
    headers: { "api-key": env.BREVO_API_KEY, "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify({
      sender: { name: "Tutorial Pet", email: env.BREVO_SENDER_EMAIL || "contato@tutorialpet.com.br" },
      to: [{ email: p.form.email, name: p.form.tutor || undefined }],
      subject: `A música do ${nome} ficou pronta 🎶`,
      htmlContent: html,
      tags: ["musica-do-seu-pet"],
    }),
  });
  if (!r.ok) return { ok: false, motivo: `brevo ${r.status}: ${(await r.text()).slice(0, 160)}` };
  return { ok: true };
}
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

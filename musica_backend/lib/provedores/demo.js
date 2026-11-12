// Provedor de DEMONSTRAÇÃO (só para prévia/teste, nunca em produção): não gera música nova,
// devolve a amostra da Mel que já está no site. Liga com MUSICA_DEMO=1 e MUSIC_PROVIDERS=demo.
export const nome = "demo";
export const disponivel = (env) => String(env.MUSICA_DEMO || "") === "1";

export async function enviar(pedido, letra, env) {
  const url = "https://site.local/musica/amostra-mel.mp3";
  const r = env.ASSETS?.fetch
    ? await env.ASSETS.fetch(new Request(url))
    : await fetch(`${String(env.PUBLIC_BASE_URL || "").replace(/\/$/, "")}/musica/amostra-mel.mp3`);
  if (!r.ok) throw new Error(`demo: amostra indisponível (${r.status})`);
  const bytes = new Uint8Array(await r.arrayBuffer());
  if (bytes.length < 20000) throw new Error("demo: amostra vazia");
  return { mp3Bytes: bytes, duracao: 150 };
}

export async function consultar() { return { estado: "falhou", motivo: "demo é síncrono" }; }

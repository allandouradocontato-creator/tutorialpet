// Mapeamento dos campos fechados do formulário para o pedido de estilo musical (tags em inglês funcionam melhor nos modelos).
export const ESTILOS = {
  "pop alegre": "upbeat brazilian pop, happy, catchy hook, bright synths, handclaps, danceable",
  "sertanejo": "sertanejo universitario, acoustic guitar, viola caipira, accordion, warm, feel-good",
  "forró": "forro pe de serra, accordion, zabumba, triangle, joyful, danceable, brazilian northeast",
  "mpb": "mpb, brazilian acoustic, nylon guitar, soft percussion, warm, gentle, melodic",
  "rock": "brazilian pop rock, electric guitar, energetic drums, anthemic chorus, fun",
  "infantil": "children's song, playful, cheerful, xylophone, ukulele, simple catchy melody, sing-along",
};
export const CLIMAS = {
  "animada": "joyful, energetic, fun",
  "emocionante": "heartfelt, emotional, warm, uplifting",
  "homenagem": "tender, tribute, nostalgic, loving, gentle",
};
export const VOZES = { "feminina": "female vocals", "masculina": "male vocals" };

export const lista = (obj) => Object.keys(obj);

export function descricaoEstilo(p, limite = 480) {
  const partes = [ESTILOS[p.estilo] || ESTILOS["pop alegre"], CLIMAS[p.clima] || "", VOZES[p.voz] || "",
    "brazilian portuguese vocals", "clear studio mix"];
  return partes.filter(Boolean).join(", ").slice(0, limite);
}

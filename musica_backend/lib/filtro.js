// Filtros de segurança: letra e campos do formulário. Sem nomes de artistas, sem títulos de músicas existentes,
// sem a palavra "cão"/"cães" (regra da marca) e sem conteúdo ofensivo.
import { semAcento } from "./util.js";

const ARTISTAS = [
  "roberto carlos", "chitaozinho", "xororo", "marilia mendonca", "gusttavo lima", "anitta", "ivete sangalo", "luan santana",
  "jorge e mateus", "jorge & mateus", "zeze di camargo", "henrique e juliano", "maiara e maraisa", "simone e simaria",
  "legiao urbana", "djavan", "caetano veloso", "gilberto gil", "chico buarque", "tim maia", "jorge ben", "elis regina",
  "beatles", "michael jackson", "taylor swift", "beyonce", "rihanna", "ed sheeran", "bruno mars", "coldplay",
  "madonna", "shakira", "daddy yankee", "bad bunny", "justin bieber", "ariana grande", "billie eilish", "dua lipa",
  "paula fernandes", "wesley safadao", "joao gomes", "alok", "pabllo vittar", "ludmilla", "claudia leitte",
  "xuxa", "patati", "galinha pintadinha", "mundo bita", "turma da monica", "disney", "pixar",
];
const TITULOS = [
  "garota de ipanema", "evidencias", "aquarela", "ai se eu te pego", "parabens pra voce", "let it go", "happy birthday",
  "asa branca", "mamae eu quero", "atirei o pau no gato", "ciranda cirandinha", "borboletinha",
  "o sapo nao lava o pe", "pombinha branca", "cai cai balao", "boi da cara preta", "marcha soldado", "fico assim sem voce",
  "esquema novo", "tempo perdido", "wonderwall", "bohemian rhapsody",
];
const OFENSIVAS = [
  "porra", "caralho", "merda", "puta", "putaria", "foda", "foder", "buceta", "cu", "viado", "bicha", "cacete", "arrombado",
  "otario", "idiota", "imbecil", "vagabund", "retardad", "nazi", "estupr", "suicid", "droga", "cocaina", "maconha", "sexo", "sexual", "pornô", "porno", "negro sujo", "macaco",
];

const norm = (s) => ` ${semAcento(s).toLowerCase().replace(/[^a-z0-9&]+/g, " ").trim()} `;

export function proibidoNaLetra(texto) {
  const t = norm(texto);
  if (/\bcao\b|\bcaes\b/.test(t)) return 'palavra "cão" não permitida';
  for (const a of ARTISTAS) if (t.includes(` ${semAcento(a).toLowerCase()} `)) return `nome de artista: ${a}`;
  for (const m of TITULOS) if (t.includes(` ${m} `)) return `título de música existente: ${m}`;
  for (const o of OFENSIVAS) {
    const re = o.length <= 5 ? new RegExp(`\\b${o}\\b`) : new RegExp(`\\b${o}`);
    if (re.test(t)) return `termo não permitido: ${o}`;
  }
  return null;
}

// Campos do formulário usam a mesma régua da letra (nome do pet, manias, nome do tutor, raça).
export function proibidoNoCampo(texto) {
  return proibidoNaLetra(texto);
}

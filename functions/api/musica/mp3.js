import { entregarMp3 } from "../../../musica_backend/lib/core.js";

export async function onRequestGet({ request, env }) {
  const u = new URL(request.url);
  return entregarMp3(env, request, u.searchParams.get("id") || "", u.searchParams.get("n") || "1", u.searchParams.get("baixar") === "1");
}

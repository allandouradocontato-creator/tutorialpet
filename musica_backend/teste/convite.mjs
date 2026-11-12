import { criarPedido } from "../lib/core.js";
const kv=new Map(); const env={PEDIDOS:{get:async k=>kv.has(k)?kv.get(k):null,put:async(k,v)=>kv.set(k,v)},CONVITES_TESTE:"AMIGOS10:2",KIWIFY_CHECKOUT_URL:"https://pay.kiwify.com.br/x"};
const f={nomePet:"Thor",especie:"cachorro",manias:["pula","late","ama bola"],estilo:"pop alegre",voz:"feminina",clima:"animada",whatsapp:"85999999999",email:"a@b.com"};
for (const c of ["AMIGOS10","amigos10","AMIGOS10","ERRADO",""]) { const r=await criarPedido(env,{...f,convite:c},{}); console.log(c||"(sem)", r.ok, r.teste||"", r.creditosRestantes??"", r.erro||"", (r.checkoutUrl||"").slice(0,40)); }

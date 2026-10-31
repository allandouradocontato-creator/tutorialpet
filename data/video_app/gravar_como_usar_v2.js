// Grava as telas do app OFICIAL (landing/app, "cachorro") para o vídeo "como usar o app" v2.
// Uso: servir landing/app em http://localhost:8765 e rodar: NODE_PATH=$(npm root -g) node gravar_como_usar_v2.js <pasta_saida>
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');const {execSync}=require('child_process');
const OUT=process.argv[2]||'v2';const AUD=path.join(__dirname,'audios_v2');
const dur=k=>parseFloat(execSync(`ffprobe -v error -show_entries format=duration -of csv=p=0 ${AUD}/como_usar_app_fala_${k.padStart(2,'0')}.mp3`).toString())+0.7;
const duda='data:image/jpeg;base64,'+fs.readFileSync(path.join(__dirname,'v2/duda_capa_cartao.jpg')).toString('base64');
const card=(t1,t2)=>`<body style="margin:0;background:#FFF3E3;font-family:system-ui,sans-serif;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh"><div style="width:240px;height:240px;border-radius:50%;background:url(${duda}) center 30%/cover;border:6px solid #fff;box-shadow:0 8px 24px #0003"></div><div style="font-size:30px;font-weight:800;color:#1B1464;margin-top:26px">${t1}</div><div style="font-size:17px;color:#7a6a58;margin-top:8px;padding:0 30px">${t2}</div><div style="font-size:11px;color:#9a8a78;margin-top:22px">Duda · imagem criada com IA</div></body>`;
(async()=>{fs.mkdirSync(OUT,{recursive:true});
const b=await chromium.launch();const c=await b.newContext({viewport:{width:546,height:1008},deviceScaleFactor:1,serviceWorkers:'block',recordVideo:{dir:OUT,size:{width:546,height:1008}}});
const p=await c.newPage();await p.addInitScript(()=>{document.addEventListener('DOMContentLoaded',()=>{document.documentElement.style.zoom='1.4'})});const T0=Date.now();const marks={};
const inject=async()=>{await p.evaluate(()=>{if(document.getElementById('__tap'))return;const d=document.createElement('div');d.id='__tap';d.style.cssText='position:fixed;z-index:99999;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;border:4px solid #E8590C;background:rgba(232,89,12,.25);pointer-events:none;opacity:0;transition:opacity .15s,transform .35s;transform:scale(1.6)';document.body.appendChild(d)})};
const pulse=async(loc)=>{await inject();const bb=await loc.boundingBox();if(!bb)return;await p.evaluate(({x,y})=>{const d=document.getElementById('__tap');d.style.left=(x/1.4)+'px';d.style.top=(y/1.4)+'px';d.style.opacity='1';d.style.transform='scale(1)';setTimeout(()=>{d.style.opacity='0';d.style.transform='scale(1.6)'},1100)},{x:bb.x+bb.width/2,y:bb.y+bb.height/2})};
const tap=async(loc)=>{await loc.scrollIntoViewIfNeeded().catch(()=>{});await pulse(loc);await p.waitForTimeout(450);await loc.click();};
const btn=(n)=>p.getByRole('button',{name:n}).first();
async function seg(k,D,fn){const t=Date.now();marks[k]=(t-T0)/1000;await fn(t);const rest=D*1000-(Date.now()-t);if(rest>0)await p.waitForTimeout(rest);}
const at=async(t,s)=>{const w=s*1000-(Date.now()-t);if(w>0)await p.waitForTimeout(w)};
await p.setContent(card('Como usar o Sozinho em Casa','Passo a passo, em menos de 3 minutos'));
await seg('1',dur('1'),async()=>{});
await seg('2',dur('2'),async t=>{await p.goto('http://localhost:8765/');await p.waitForSelector('text=Começar');await at(t,dur('2')-1.5);await tap(btn('Começar'))});
await seg('3',dur('3'),async t=>{await at(t,dur('3')-1.6);await tap(btn('Entendi, vamos lá'))});
await seg('3b',dur('3b'),async t=>{await at(t,8);await pulse(btn('Prefiro silêncio'));await at(t,13);await pulse(btn('Quero som'));await at(t,dur('3b')-1.4);await tap(btn('Prefiro silêncio'))});
await seg('4',dur('4'),async t=>{await at(t,2);await p.locator('input').pressSequentially('Thor',{delay:150});await at(t,dur('4')-1.4);await tap(btn('Continuar'))});
await seg('5',dur('5'),async t=>{await at(t,0.6);await p.locator('input').pressSequentially('Ana',{delay:150});await at(t,dur('5')-1.4);await tap(btn('Continuar'))});
await seg('6',dur('6'),async t=>{for(let i=0;i<5;i++){await at(t,1.2+i*1.6);await tap(p.locator('button.opt').first())}});
await seg('6b',dur('6b'),async t=>{const ts=[1.0,2.6,4.2,5.8];for(let i=0;i<4;i++){await at(t,ts[i]);await tap(p.locator('button.opt').first())}await at(t,7.0);await tap(p.locator('button.opt').first());await at(t,dur('6b')-1.5);await tap(btn('Montar o meu plano'))});
await seg('6c',dur('6c'),async t=>{await btn('Ver a meta de hoje').waitFor({timeout:8000});await at(t,dur('6c')-1.5);await tap(btn('Ver a meta de hoje'))});
await seg('7',dur('7'),async t=>{await p.evaluate(()=>{document.querySelectorAll('details[data-video-topo]').forEach(d=>d.removeAttribute('open'))});await at(t,6.5);await tap(btn('Pular guia'))});
await seg('8',dur('8'),async t=>{await at(t,1.2);await tap(btn('Como fazer'))});
await seg('9',dur('9'),async t=>{await p.evaluate(()=>window.scrollTo(0,0));await at(t,dur('9')-1.9);await tap(btn('Registrar sessão'))});
await seg('10',dur('10'),async t=>{await at(t,3.2);await pulse(btn(/Tranquilo/));await at(t,4.8);await pulse(btn(/Inquieto/));await at(t,6.4);await pulse(btn(/Pânico/))});
await seg('11',dur('11'),async t=>{await at(t,0.8);await tap(btn(/Tranquilo/))});
await seg('12',dur('12'),async t=>{await at(t,0.3);await tap(btn('Voltar para Hoje'));await p.waitForTimeout(800);await at(t,dur('12')-1.3);await tap(btn(/Rotina antes de sair/))});
await seg('13',dur('13'),async t=>{await at(t,1.5);await p.mouse.wheel(0,260);await at(t,3.5);await p.mouse.wheel(0,260);await at(t,dur('13')-1.8);const f=btn(/Terminei a rotina/);await tap(f)});
await seg('14',dur('14'),async t=>{await p.waitForTimeout(600);const tabs=['Plano','Diário','Conquistas','Hoje'];const ts=[2.0,3.8,5.6,7.6];for(let i=0;i<4;i++){await at(t,ts[i]);await tap(p.getByRole('link',{name:tabs[i]}).first().or(btn(tabs[i])).first())}});
await p.setContent(card('Divirta-se e seja muito feliz','ao lado do seu melhor amigo'));
await seg('15',dur('15'),async()=>{});
fs.writeFileSync(path.join(OUT,'marcas.json'),JSON.stringify(marks,null,1));
await c.close();await b.close();console.log('ok',JSON.stringify(marks));})().catch(e=>{console.error('ERRO',e.message.split('\n')[0]);process.exit(1)});

const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1240,height:1754}});
await p.goto('file://'+process.cwd()+'/ficha.html');await p.waitForTimeout(500);
await p.screenshot({path:'ficha.png'});
await p.pdf({path:'ficha.pdf',width:'1240px',height:'1754px',printBackground:true});await b.close()})()

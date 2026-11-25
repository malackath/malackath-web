// RaveKit (getravekit.com): landing por secciones, claro y oscuro, compu y celular.
// Recorre toda la página antes para que corran las animaciones de entrada, y espera en cada sección.
// Uso: node capturas_ravekit.cjs <OUT> [d|m] [cla|osc]
const {chromium}=require('playwright');
const OUT=process.argv[2], SOLO_T=process.argv[3], SOLO_TEMA=process.argv[4];
const SEC=[['01-inicio',null],['02-negocios','#shops'],['03-funciones','#features'],['04-como-funciona','#how-it-works'],['05-ahorro','#calculator'],['06-comparacion','#comparison'],['07-precios','#pricing'],['08-preguntas','#faq'],['09-cierre','#cta-final'],['10-pie','footer']];
(async()=>{
 const b=await chromium.launch();
 for(const [t,ctxo] of [['d',{viewport:{width:1280,height:800},deviceScaleFactor:2}],['m',{viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true}]]){
  if(SOLO_T&&SOLO_T!==t)continue;
  for(const tema of ['cla','osc']){
   if(SOLO_TEMA&&SOLO_TEMA!==tema)continue;
   const c=await b.newContext({...ctxo,colorScheme:tema==='osc'?'dark':'light'});
   const p=await c.newPage();
   await p.goto('https://getravekit.com/',{waitUntil:'load'});await p.waitForTimeout(2500);
   // el sitio arranca en oscuro; el claro se pone con su botón de tema
   const esOsc=await p.evaluate(()=>document.documentElement.classList.contains('dark'));
   if((tema==='osc')!==esOsc){await p.click('#themeToggleBtn');await p.waitForTimeout(1200);}
   const H=await p.evaluate(()=>document.documentElement.scrollHeight);
   for(let y=0;y<H;y+=400){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(150);}
   await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(1500);
   const pre=(t==='d'?'desktop':'movil')+'-'+(tema==='osc'?'oscuro':'claro');
   for(const [n,sel] of SEC){
    if(sel){await p.evaluate(s=>{const e=document.querySelector(s);if(!e)return;const hd=document.querySelector('header,nav');const off=hd&&getComputedStyle(hd).position.match(/fixed|sticky/)?hd.getBoundingClientRect().height:0;scrollTo(0,e.getBoundingClientRect().top+scrollY-off)},sel);}
    else await p.evaluate(()=>scrollTo(0,0));
    await p.waitForTimeout(2200);
    await p.screenshot({path:`${OUT}/${pre}-${n}.png`});
   }
   console.log('ok',pre);await c.close();
  }
 }
 await b.close();
})();

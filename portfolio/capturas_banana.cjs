// The Banana Team (thebananateam.com/es): celular sin la fila "Instalá la app".
// La fila se achica sola cuando el sitio detecta la app instalada (navigator.standalone, su propia lógica);
// no se inyecta CSS. Sin menú ni chat abiertos. La pestaña cerrada del chat es fija del diseño y queda.
// Uso: node capturas_banana.cjs <OUT>
const {chromium}=require('playwright');
const OUT=process.argv[2];
const SEC=[['01-inicio',null],['03-servicios','#services'],['04-plan-destacado','#plans .featured, #plans [class*=popular], #plans article:nth-of-type(3)'],['05-planes','#plans h2'],['06-contacto','#team']];
(async()=>{
 const b=await chromium.launch();
 const c=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true});
 await c.addInitScript(()=>{Object.defineProperty(navigator,'standalone',{get:()=>true})});
 const p=await c.newPage();
 await p.goto('https://www.thebananateam.com/es',{waitUntil:'load'});await p.waitForTimeout(3000);
 const H=await p.evaluate(()=>document.documentElement.scrollHeight);
 for(let y=0;y<H;y+=400){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(120);}
 for(const [n,sel] of SEC){
  const ok=await p.evaluate(sel=>{if(!sel){scrollTo(0,0);return 'top'}
   const e=sel.split(',').map(s=>document.querySelector(s.trim())).find(Boolean);if(!e)return null;
   const tab=document.querySelector('[data-bt-chat] .tab');const off=tab?tab.getBoundingClientRect().bottom:0;
   scrollTo(0,e.getBoundingClientRect().top+scrollY-off-8);return e.tagName+'.'+e.className},sel);
  await p.waitForTimeout(1800);await p.screenshot({path:`${OUT}/movil-${n}.png`});console.log(n,ok);
 }
 await b.close();
})();

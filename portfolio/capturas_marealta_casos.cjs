// MaréAlta Arte digital: casos en compu (1440x900 x2) con la tarjeta de datos entera a la vista.
// Uso: node capturas_marealta_casos.cjs <OUT>
const {chromium}=require('playwright');
const OUT=process.argv[2];
const CASOS=['coinciva','kalu-nivasayi','la-gloria','ruvia','the-banana-team','zoomi'];
(async()=>{
 const b=await chromium.launch();const c=await b.newContext({viewport:{width:1440,height:900},deviceScaleFactor:2});const p=await c.newPage();
 for(const k of CASOS){
  await p.goto(`https://digital.marealtagastro.com/es/trabajos/${k}/`,{waitUntil:'load'});await p.waitForTimeout(2500);
  const y=await p.evaluate(()=>{
   const lab=[...document.querySelectorAll('body *')].find(e=>e.children.length===0&&e.textContent.trim()==='Cliente');
   if(!lab)return -1;let e=lab;while(e.parentElement&&e.getBoundingClientRect().width<1000)e=e.parentElement;
   const r=e.getBoundingClientRect();const y=Math.max(0,Math.round(r.bottom+scrollY-900+32));scrollTo(0,y);return y});
  await p.waitForTimeout(1500);
  await p.screenshot({path:`${OUT}/desktop-es-caso-${k}.png`});console.log(k,y);
 }
 await b.close();
})();

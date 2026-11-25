// La Gloria (lagloria.arnelli.com): páginas completas de compu y celular, sin puntero del mouse.
// Uso: node capturas_lagloria.cjs <OUT>
const {chromium}=require('playwright');
const OUT=process.argv[2];
const PAG=[['portada','index.html'],['historia','historia.html'],['carta','carta.html']];
(async()=>{
 const b=await chromium.launch();
 for(const [t,o,n0] of [['desktop',{viewport:{width:1440,height:900}},2],['mobile',{viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true},4]]){
  const c=await b.newContext(o);const p=await c.newPage();
  for(let i=0;i<PAG.length;i++){const [n,u]=PAG[i];
   await p.goto('https://lagloria.arnelli.com/'+u,{waitUntil:'load'});await p.waitForTimeout(2000);
   const H=await p.evaluate(()=>document.documentElement.scrollHeight);
   for(let y=0;y<H;y+=400){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(120);}
   await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(1500);
   const num=String(n0+i*4).padStart(2,'0');
   await p.screenshot({path:`${OUT}/${num}-${n}-${t}-completa.png`,fullPage:true});console.log(num,n,t);
  }
  await c.close();
 }
 await b.close();
})();

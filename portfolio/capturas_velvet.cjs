// Capturas de Velvet (velvet.arnelli.com) para el portfolio. Uso: NODE_PATH=<node_modules con playwright> node portfolio/capturas_velvet.cjs ~/Projects/Malackath/_capturas-vivas/velvet [pasos, ej. 02,05]
// Ojo: no apretar Escape en el sitio (activa el Modo Camuflaje).
const { chromium } = require('playwright'); const fs=require('fs');
const OUT=process.argv[2]; fs.mkdirSync(OUT,{recursive:true});
const URL='https://velvet.arnelli.com/';
const VP={desktop:{viewport:{width:1280,height:800},deviceScaleFactor:2},movil:{viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true}};
(async()=>{const b=await chromium.launch();
for(const disp of ['desktop','movil']) for(const tema of ['claro','oscuro']){
 const ctx=await b.newContext({...VP[disp],locale:'es-UY',timezoneId:'America/Montevideo',serviceWorkers:'block'});
 const pg=await ctx.newPage(); pg.setDefaultTimeout(15000);
 await pg.goto(URL,{waitUntil:'load',timeout:45000}); await pg.getByRole('button',{name:/18/}).first().click({timeout:15000}); await pg.waitForTimeout(1000);
 await pg.evaluate(t=>{localStorage.setItem('velvet-theme',t);localStorage.setItem('velvet-autoplay-photos','false')},tema==='claro'?'light':'dark');
 const inicio=async()=>{await pg.goto(URL,{waitUntil:'load',timeout:45000});await pg.waitForTimeout(2500);};
 const menu=async(item)=>{ const bt=disp==='desktop'?pg.getByRole('button',{name:'Menú',exact:true}).first():pg.getByRole('button',{name:'Abrir menú'}).first();
   await bt.click(); await pg.waitForTimeout(800); await pg.getByText(item,typeof item==='string'?{exact:true}:{}).locator('visible=true').first().click(); await pg.waitForTimeout(3000);};
 const shot=async(n,slug)=>{await pg.mouse.move(0,0).catch(()=>{}); const f=`${OUT}/${disp}-${tema}-${n}-${slug}.png`; await pg.screenshot({path:f}); console.log(f.split('/').pop(), pg.url());};
 const pasos=[
  ['01','inicio',async()=>{await inicio();}],
  ['02','inicio-tarjetas',async()=>{await inicio(); await pg.mouse.move(disp==='desktop'?640:195,400); await pg.mouse.wheel(0,disp==='desktop'?520:660); await pg.waitForTimeout(1800);}],
  ['03','buscador',async()=>{await inicio(); await pg.getByRole('button',{name:'Abrir buscador y filtros'}).first().click(); await pg.waitForTimeout(1500); await pg.locator('text=/Búsqueda avanzada|Filtros/i').locator('visible=true').first().click(); await pg.waitForTimeout(2000);}],
  ['04','mapa',async()=>{await inicio(); await pg.getByRole('button',{name:'Mapa',exact:true}).last().click(); await pg.waitForTimeout(5000);}],
  ['05','perfil-anfitriona',async()=>{await pg.goto(URL+'perfil/josefina-cabrera-12',{waitUntil:'load',timeout:45000}); await pg.waitForTimeout(4500); for(let r=0;r<3;r++){await pg.evaluate(()=>{window.scrollTo(0,0);document.querySelectorAll('*').forEach(el=>{if(el.scrollTop)el.scrollTop=0;});}); await pg.waitForTimeout(700);}}],
  ['06','como-funciona',async()=>{await inicio(); await menu('Cómo funciona');}],
  ['07','reserva-segura',async()=>{await inicio(); await menu(/Garant/);}],
  ['08','preguntas-frecuentes',async()=>{await inicio(); await menu('Preguntas frecuentes');}],
  ['09','reels',async()=>{await inicio(); await menu('Reels'); await pg.waitForTimeout(2000);}],
 ];
 const SOLO=(process.argv[3]||'').split(',').filter(Boolean);
 for(const [n,slug,fn] of pasos){ if(SOLO.length&&!SOLO.includes(n)) continue; try{await fn(); await shot(n,slug);}catch(e){console.log('FALLA',disp,tema,slug,e.message.split('\n')[0]);} }
 await ctx.close();}
await b.close();})();

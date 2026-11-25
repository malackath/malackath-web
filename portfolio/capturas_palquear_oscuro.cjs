// Palquear compu en oscuro: modo oscuro automatico de Chrome (igual que las capturas de celular oscuras)
const {chromium}=require('playwright');
const OUT=process.argv[2], U='https://palquear.arnelli.com/';
(async()=>{
 const b=await chromium.launch({args:['--blink-settings=forceDarkModeEnabled=true,darkModeImagePolicy=2','--enable-features=WebContentsForceDark']});
 const c=await b.newContext({viewport:{width:1440,height:900},colorScheme:'dark'});
 const p=await c.newPage(); p.setDefaultTimeout(15000);
 const go=async u=>{await p.goto(U+u,{waitUntil:'load'});await p.waitForTimeout(1800);};
 const shot=async n=>{await p.waitForTimeout(700);await p.screenshot({path:OUT+'/'+n+'-oscuro.png'});console.log('ok',n);};
 await go('partidos');
 await p.click('.roles a[data-r="comprador"]');await p.waitForLoadState('load');await p.waitForTimeout(1500);
 await go('partidos'); await shot('01-buscador-de-partidos');
 await p.click('.roles a[data-r="titular"]');await p.waitForLoadState('load');await p.waitForTimeout(1500);
 await go('titular'); await shot('02-mis-palcos-titular');
 const y=await p.evaluate(()=>{const e=[...document.querySelectorAll('b')].find(x=>x.textContent==='Mapa del palco');return e?e.getBoundingClientRect().top+scrollY:0});
 await p.evaluate(y=>scrollTo(0,y-150),y); await shot('03-mapa-del-palco');
 await p.evaluate(()=>scrollTo(0,0)); await p.click('[data-view="hist"]'); await shot('04-cobros-del-titular');
 await go('club?c=PEN'); await shot('05-panel-del-club');
 await go('club?c=NAC'); await shot('06-panel-del-club-nacional');
 await go('proyeccion'); await shot('07-proyeccion-a-5-anos');
 await b.close();
})();

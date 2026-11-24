const {chromium}=require('playwright');
(async()=>{const [,,url,out,w]=process.argv;const b=await chromium.launch();
const p=await b.newPage({viewport:{width:+w||1280,height:900}});
await p.goto(url,{waitUntil:'networkidle'}).catch(()=>{});await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,80));}window.scrollTo(0,0);});await p.waitForTimeout(1500);
await p.screenshot({path:out,fullPage:true});await b.close();})();

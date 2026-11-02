const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+require('path').join(__dirname,'fiche.html'));
const o=await p.evaluate(()=>{const c=document.querySelector('.cols');return {sw:c.scrollWidth,cw:c.clientWidth,h:c.scrollHeight}});
await p.pdf({path:require('path').join(__dirname,'fiche_speaker.pdf'),format:'A4',landscape:true,printBackground:true,margin:{top:'5mm',bottom:'5mm',left:'5mm',right:'5mm'}});
console.log(JSON.stringify(o));await b.close()})();

const fs=require('fs'),path=require('path'),http=require('http'),crypto=require('crypto');
const {chromium}=require('C:/Users/Murilo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const project=path.resolve(__dirname,'..'), repo=path.resolve(project,'../..'), port=8876;
const journal=path.join(project,'auditoria/execucao/photopea_api.jsonl');
function record(v){fs.appendFileSync(journal,JSON.stringify({timestamp:new Date().toISOString(),agent:'photopea_api',...v})+'\n');}
function under(root,p){const q=path.resolve(root,p);if(q!==root&&!q.startsWith(root+path.sep))throw Error('Caminho fora da raiz autorizada');return q;}
const html=`<!doctype html><meta charset="utf-8"><title>Bellas V2 — Photopea API</title><style>html,body,iframe{width:100%;height:100%;margin:0;border:0}body{background:#282828}</style><iframe id="pp"></iframe><script>
const frame=document.getElementById('pp');let ready=false,pending=null;
window.addEventListener('message',function(e){if(e.source!==frame.contentWindow||e.origin!=='https://www.photopea.com')return;
 if(e.data==='done'){if(!pending){ready=true;return;}const item=pending;pending=null;Promise.all(item.uploads).then(()=>item.resolve({echoes:item.echoes,files:item.files})).catch(item.reject);return;}
 if(!pending)return;
 if(e.data instanceof ArrayBuffer){const item=pending,index=item.uploads.length,target=item.outputs[index];if(!target){item.reject(Error('Binário sem nome de saída'));return;}
  item.uploads.push(fetch('/receive?target='+encodeURIComponent(target),{method:'POST',body:e.data}).then(r=>r.json()).then(v=>{if(v.error)throw Error(v.error);item.files[index]=v;}));
 }else pending.echoes.push(e.data);
});
window.apiReady=()=>ready;
window.ppSend=(data,outputs=[])=>new Promise((resolve,reject)=>{if(!ready||pending){reject(Error('API não pronta ou ocupada'));return;}pending={resolve,reject,outputs,echoes:[],files:[],uploads:[]};frame.contentWindow.postMessage(data,'https://www.photopea.com');});
window.ppLoad=async url=>{const data=await fetch(url).then(r=>{if(!r.ok)throw Error('Arquivo local indisponível');return r.arrayBuffer();});return window.ppSend(data,[]);};
frame.src='https://www.photopea.com#'+encodeURIComponent(JSON.stringify({environment:{intro:false,vmode:2,localsave:false},script:'app.echoToOE("BELLAS_V2_READY");'}));
</script>`;
let page,browser,busy=false,seq=0;
function json(res,status,obj){res.writeHead(status,{'Content-Type':'application/json'});res.end(JSON.stringify(obj));}
function body(req){return new Promise((resolve,reject)=>{let chunks=[],size=0;req.on('data',b=>{size+=b.length;if(size>300*1024*1024){reject(Error('Corpo excede300MB'));req.destroy();}else chunks.push(b);});req.on('end',()=>resolve(Buffer.concat(chunks)));req.on('error',reject);});}
const server=http.createServer(async(req,res)=>{try{const url=new URL(req.url,'http://127.0.0.1:'+port);
 if(url.pathname==='/'){res.writeHead(200,{'Content-Type':'text/html;charset=utf-8'});res.end(html);return;}
 if(url.pathname==='/status'){json(res,200,{ready:page?await page.evaluate(()=>window.apiReady()):false,busy});return;}
 if(url.pathname.startsWith('/files/')){const p=under(repo,decodeURIComponent(url.pathname.slice(7)));if(!fs.existsSync(p)){json(res,404,{error:'Arquivo não encontrado'});return;}res.writeHead(200,{'Content-Type':'application/octet-stream','Cache-Control':'no-store'});fs.createReadStream(p).pipe(res);return;}
 if(url.pathname==='/receive'){const relative=url.searchParams.get('target'),target=under(project,relative),data=await body(req);fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,data);const v={path:relative,bytes:data.length,sha256:crypto.createHash('sha256').update(data).digest('hex')};record({event:'binary_received',status:'saved',...v});json(res,200,v);return;}
 if(url.pathname==='/run'){
  if(busy){json(res,409,{error:'API ocupada'});return;}busy=true;const job=JSON.parse((await body(req)).toString('utf8')),id='PP-'+Date.now()+'-'+(++seq);let script;
  if(job.script_file){script=fs.readFileSync(under(project,job.script_file),'utf8');}else script=job.script;
  const snapshot='auditoria/scripts_executados/'+id+'.jsx';if(script)fs.writeFileSync(under(project,snapshot),script);
  record({action_id:id,event:'planned',tool:'Photopea.postMessage',parameters_exact:job,script_snapshot:script?snapshot:null,status:'planned'});
  try{const result=job.load?await page.evaluate(url=>window.ppLoad(url),'/files/'+encodeURI(job.load)):await page.evaluate(({script,outputs})=>window.ppSend(script,outputs),{script,outputs:job.outputs||[]});record({action_id:id,event:'result',status:'returned',result});json(res,200,{id,...result});}
  catch(e){record({action_id:id,event:'result',status:'failed',error:String(e)});json(res,500,{id,error:String(e)});}finally{busy=false;}return;
 }
 if(url.pathname==='/screen'){await page.screenshot({path:path.join(project,'auditoria/photopea_navegador.png'),fullPage:false});json(res,200,{path:'auditoria/photopea_navegador.png'});return;}
 json(res,404,{error:'Rota não disponível'});
}catch(e){busy=false;json(res,500,{error:String(e)});}});
(async()=>{
 const own=fs.readFileSync(__filename),sha=crypto.createHash('sha256').update(own).digest('hex');fs.writeFileSync(path.join(project,'auditoria/scripts_executados/bridge_'+sha.slice(0,12)+'.cjs'),own);record({event:'bridge_start',status:'started',script_sha256:sha,port});
 await new Promise(r=>server.listen(port,'127.0.0.1',r));
 const local=chromium.executablePath();let options={headless:true,args:['--disable-dev-shm-usage']};
 if(!fs.existsSync(local)){const chrome='C:/Program Files/Google/Chrome/Application/chrome.exe';if(fs.existsSync(chrome))options.executablePath=chrome;else options.channel='msedge';}
 browser=await chromium.launch(options);page=await browser.newPage({viewport:{width:1920,height:1080}});page.setDefaultTimeout(180000);
 page.on('pageerror',e=>record({event:'browser_error',error:String(e)}));
 await page.goto('http://127.0.0.1:'+port,{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>window.apiReady(),{},{timeout:180000});
 record({event:'bridge_ready',status:'ready',browser:await browser.version()});process.stdout.write('PHOTOPEA_API_READY http://127.0.0.1:'+port+'\n');
})().catch(e=>{record({event:'bridge_failure',status:'failed',error:String(e)});process.stderr.write(String(e)+'\n');process.exitCode=1;});

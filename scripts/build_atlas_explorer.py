#!/usr/bin/env python3
"""Build the Anveshar Atlas Explorer: one immersive, self-contained interactive
canvas where rare cancers, their shared driver genes, the analytical tasks, and the
runnable sequence models form a single navigable graph. Reads the rare-conditions
catalog and data/sequence_models.json, computes the shared-dependency network, and
injects the graph as JSON into a dark, animated, dependency-free HTML page.

Run: PYTHONPATH=. python3 scripts/build_atlas_explorer.py
"""
import os, json, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG = os.path.join(ROOT, "data", "rare_conditions_catalog.json")
MODELS = os.path.join(ROOT, "data", "sequence_models.json")
OUT_ART = os.path.join(ROOT, "artifacts", "anveshar_atlas_explorer.html")
OUT_SITE = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/rarecancers/atlas_explorer.html"

# reuse the package driver-gene parser if importable; fall back to a local regex
try:
    from anveshar import analysis
    driver_genes = analysis._driver_genes
except Exception:
    _STOP = {"AND", "OR", "THE", "OF", "VS", "FUSION", "LOSS", "GAIN", "MUTATION",
             "AMPLIFICATION", "DELETION", "WILD", "TYPE", "POSITIVE", "NEGATIVE", "HIGH", "LOW"}
    def driver_genes(s):
        toks = re.findall(r"[A-Z0-9]{2,}", (s or "").upper())
        return {t for t in toks if t not in _STOP and not re.fullmatch(r"[A-Z]\d+[A-Z]?", t)}

catalog = json.load(open(CATALOG, encoding="utf-8"))
mcat = json.load(open(MODELS, encoding="utf-8"))

cancers = [c for c in catalog if str(c.get("category", "")).startswith("rare cancer")]
gene_to_cancers = collections.defaultdict(set)
cancer_recs = []
for c in cancers:
    gs = sorted(driver_genes(c.get("key_gene_or_marker", "")))
    if not gs:
        continue
    cancer_recs.append({"name": c["name"], "system": c.get("organ_system", ""), "genes": gs})
    for g in gs:
        gene_to_cancers[g].add(c["name"])

# rank genes by how many rare cancers they drive; keep the shared hubs for the default view
ranked = sorted(gene_to_cancers.items(), key=lambda kv: len(kv[1]), reverse=True)
TOPN = 64
top_genes = [g for g, cs in ranked if len(cs) >= 2][:TOPN]
top_set = set(top_genes)

# gene-gene edges: two genes are linked if they co-drive at least MINCO common cancers
MINCO = 1
edges = []
for i, a in enumerate(top_genes):
    for b in top_genes[i + 1:]:
        w = len(gene_to_cancers[a] & gene_to_cancers[b])
        if w >= MINCO:
            edges.append([a, b, w])

# every coding driver can be run through this standard task panel
GENE_TASKS = ["variant_effect", "missense_pathogenicity", "splice_disruption",
              "expression_from_sequence", "protein_embedding", "structure_prediction"]
task_ids = list(mcat["tasks_glossary"].keys())
models = []
for m in mcat["models"]:
    models.append({"id": m["id"], "name": m["name"], "org": m["org"], "modality": m["modality"],
                   "params": m["params"], "license": m["license"], "weights": m["weights"],
                   "framework": m["framework"], "footprint": m["footprint"], "tasks": m["tasks"],
                   "use": m["rare_cancer_use"], "citation": m["citation"],
                   "caveat": m.get("caveat", ""), "confidence": m.get("confidence", "")})

genes = [{"id": g, "n": len(gene_to_cancers[g]),
          "cancers": sorted(gene_to_cancers[g])[:40],
          "n_cancers": len(gene_to_cancers[g])} for g in top_genes]

graph = {
    "genes": genes,
    "edges": edges,
    "tasks": [{"id": t, "label": t.replace("_", " "), "desc": mcat["tasks_glossary"][t]} for t in task_ids],
    "models": models,
    "gene_tasks": GENE_TASKS,
    "cancers": cancer_recs,
    "stats": {"n_cancers_total": len(cancers), "n_cancers_with_driver": len(cancer_recs),
              "n_genes_total": len(gene_to_cancers), "n_genes_shown": len(top_genes),
              "n_models": len(models), "benchmark_caveat": mcat["benchmark_caveat"]},
}
GJSON = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))

HTML = r"""<title>Anveshar Atlas Explorer</title>
<style>
 :root{--bg:#070a10;--bg2:#0c111b;--ink:#e8eef6;--muted:#8b97ab;--line:#1c2432;
  --gene:#12a0ab;--gene2:#0b6b73;--model:#e6a13c;--task:#8a7be6;--cancer:#5b6b82;
  --accent:#12a0ab;--warn:#e0b64a;--panel:rgba(12,17,27,.94);
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --sans:Arial,Helvetica,sans-serif}
 *{box-sizing:border-box}
 html,body{margin:0;height:100%;background:var(--bg);color:var(--ink);font-family:var(--sans);overflow:hidden}
 #stage{position:fixed;inset:0}
 canvas{display:block;width:100%;height:100%;cursor:grab}
 canvas:active{cursor:grabbing}
 .veil{position:fixed;inset:0;pointer-events:none;background:radial-gradient(1200px 700px at 26% 0%,rgba(18,160,171,.10),transparent 60%),radial-gradient(900px 600px at 92% 100%,rgba(230,161,60,.07),transparent 55%)}
 .hud{position:fixed;top:20px;left:22px;max-width:392px;pointer-events:none;z-index:5}
 .brand{font-family:var(--mono);font-size:11px;letter-spacing:.34em;color:var(--accent);text-transform:uppercase}
 h1{font-size:26px;margin:6px 0 4px;letter-spacing:-.015em;font-weight:800;text-wrap:balance}
 .sub{color:var(--muted);font-size:13px;line-height:1.5;max-width:44ch}
 .search{margin-top:14px;pointer-events:auto;position:relative;max-width:330px}
 .search input{width:100%;background:rgba(12,17,27,.9);border:1px solid var(--line);color:var(--ink);
  font-size:13.5px;padding:11px 12px 11px 34px;border-radius:11px;outline:none;font-family:var(--sans)}
 .search input:focus{border-color:var(--accent)}
 .search .mag{position:absolute;left:12px;top:10px;color:var(--muted);font-size:14px}
 .sugg{position:absolute;top:44px;left:0;right:0;background:var(--panel);border:1px solid var(--line);
  border-radius:11px;overflow:hidden;max-height:260px;overflow-y:auto;display:none;backdrop-filter:blur(8px)}
 .sugg.on{display:block}
 .sugg div{padding:8px 12px;font-size:12.5px;cursor:pointer;border-bottom:1px solid var(--line);display:flex;gap:8px;align-items:center}
 .sugg div:hover{background:rgba(18,160,171,.14)}
 .sugg .k{font-family:var(--mono);font-size:10px;color:var(--muted);text-transform:uppercase}
 .legend{position:fixed;top:20px;right:22px;z-index:5;background:var(--panel);border:1px solid var(--line);
  border-radius:12px;padding:12px 14px;font-size:12px;backdrop-filter:blur(8px);max-width:220px}
 .legend b{font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
 .lrow{display:flex;align-items:center;gap:9px;margin-top:8px;cursor:pointer;user-select:none}
 .lrow.off{opacity:.35}
 .dot{width:11px;height:11px;border-radius:50%;flex:none}
 .toggle{margin-left:auto;font-family:var(--mono);font-size:9px;color:var(--muted)}
 .panel{position:fixed;top:0;right:0;height:100%;width:min(420px,92vw);background:var(--panel);
  border-left:1px solid var(--line);backdrop-filter:blur(12px);transform:translateX(102%);
  transition:transform .32s cubic-bezier(.22,.61,.36,1);z-index:8;overflow-y:auto;padding:22px 22px 40px}
 .panel.on{transform:translateX(0)}
 .panel .x{position:absolute;top:14px;right:16px;color:var(--muted);cursor:pointer;font-size:20px;line-height:1}
 .kind{font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase}
 .panel h2{font-size:21px;margin:6px 0 2px;letter-spacing:-.01em;text-wrap:balance}
 .panel .meta{color:var(--muted);font-size:12.5px}
 .chips{display:flex;flex-wrap:wrap;gap:6px;margin:12px 0}
 .chip{font-size:11px;padding:3px 9px;border-radius:20px;border:1px solid var(--line);background:rgba(255,255,255,.03)}
 .chip.task{border-color:rgba(138,123,230,.5);color:#c3baf3}
 .sec{margin-top:16px;border-top:1px solid var(--line);padding-top:13px}
 .sec b{font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);display:block;margin-bottom:7px}
 .li{font-size:12.5px;line-height:1.55;color:#cdd6e4}
 .li.small{font-size:11.5px;color:var(--muted)}
 .mrow{display:flex;gap:9px;align-items:baseline;padding:6px 0;border-bottom:1px solid var(--line)}
 .mrow .nm{font-weight:700;font-size:12.5px}
 .mrow .md{font-family:var(--mono);font-size:9.5px;padding:1px 6px;border-radius:5px;background:rgba(230,161,60,.14);color:var(--model)}
 .cite{font-size:11px;color:var(--muted);font-family:var(--mono);line-height:1.5}
 a.link{color:var(--accent);text-decoration:none;font-weight:600}
 .foot{position:fixed;bottom:12px;left:22px;z-index:5;font-size:11px;color:var(--muted);pointer-events:auto}
 .foot a{color:var(--accent);text-decoration:none}
 .disc{position:fixed;bottom:12px;right:22px;z-index:5;font-size:10.5px;color:var(--muted);max-width:340px;text-align:right}
 .hint{position:fixed;bottom:38px;left:50%;transform:translateX(-50%);z-index:5;font-size:11.5px;color:var(--muted);
  background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:6px 14px;backdrop-filter:blur(8px);transition:opacity .5s}
 @media(max-width:720px){.legend{display:none}.hud{max-width:72vw}}
</style>
<div id="stage"><canvas id="cv"></canvas></div>
<div class="veil"></div>
<div class="hud">
 <div class="brand">Anveshar &middot; atlas explorer</div>
 <h1>Rare cancers, their driver genes, and the models that read them</h1>
 <div class="sub" id="subline"></div>
 <div class="search">
  <span class="mag">&#128269;</span>
  <input id="q" type="search" placeholder="Search a rare cancer, driver gene, or model" autocomplete="off">
  <div class="sugg" id="sugg"></div>
 </div>
</div>
<div class="legend" id="legend"></div>
<div class="panel" id="panel"><span class="x" id="px">&times;</span><div id="pbody"></div></div>
<div class="hint" id="hint">Drag to pan &middot; scroll to zoom &middot; click any node</div>
<div class="foot">Developer: <a href="https://digvijayky.com" target="_blank" rel="noopener">digvijayky</a></div>
<div class="disc">Research and educational tool on public data, not medical advice. Model choices should be benchmarked; final decisions rest with a qualified health care provider.</div>
<script>
const G=__GRAPH__;
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
let W,H,DPR;
function resize(){DPR=Math.min(2,window.devicePixelRatio||1);W=cv.clientWidth;H=cv.clientHeight;cv.width=W*DPR;cv.height=H*DPR;ctx.setTransform(DPR,0,0,DPR,0,0);}
window.addEventListener("resize",resize);resize();
document.getElementById("subline").textContent=G.stats.n_cancers_with_driver+" rare cancers with a mapped driver · "+G.stats.n_genes_shown+" shared driver hubs · "+G.stats.n_models+" runnable models. One graph.";

const COL={gene:"#12a0ab",model:"#e6a13c",task:"#8a7be6",cancer:"#6b7c96"};
const show={gene:true,model:true,task:true,cancer:false};

// ---- build node set: gene hubs (center), task ring, model outer ring ----
let nodes=[],byId={};
function add(n){n.vx=0;n.vy=0;byId[n.id]=n;nodes.push(n);return n;}
const cx=W*0.42, cy=H*0.5;
G.genes.forEach((g,i)=>{const a=i/G.genes.length*6.283;add({id:"g:"+g.id,kind:"gene",label:g.id,r:5+Math.sqrt(g.n)*2.2,
  x:cx+Math.cos(a)*(120+((i*53)%140)),y:cy+Math.sin(a)*(120+((i*37)%140)),data:g});});
G.tasks.forEach((t,i)=>{const a=i/G.tasks.length*6.283;add({id:"t:"+t.id,kind:"task",label:t.label,r:8,
  x:cx+Math.cos(a)*300,y:cy+Math.sin(a)*300,data:t});});
G.models.forEach((m,i)=>{const a=i/G.models.length*6.283;add({id:"m:"+m.id,kind:"model",label:m.name,r:7,
  x:cx+Math.cos(a)*430,y:cy+Math.sin(a)*430,data:m});});

// ---- edges ----
let E=[];
G.edges.forEach(e=>E.push({a:"g:"+e[0],b:"g:"+e[1],w:e[2],type:"gg"}));
// task -> model (a model performs a task)
G.models.forEach(m=>m.tasks.forEach(tk=>{if(byId["t:"+tk])E.push({a:"t:"+tk,b:"m:"+m.id,w:1,type:"tm"});}));
// gene -> task edges are implicit (every gene can run the standard panel); drawn on focus only
const GT=G.gene_tasks;

// ---- force layout (light, settles then idles) ----
let cam={x:cx,y:cy,z:1},alpha=1;
function step(){
 if(alpha<0.02)return;
 const k=alpha;
 // repulsion (only within kinds' broad field, cheap O(n^2) since n~90)
 for(let i=0;i<nodes.length;i++){const a=nodes[i];
  for(let j=i+1;j<nodes.length;j++){const b=nodes[j];
   let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+0.01;if(d2>60000)continue;
   let f=380/d2;a.vx+=dx*f*k;a.vy+=dy*f*k;b.vx-=dx*f*k;b.vy-=dy*f*k;}}
 // spring on real edges
 E.forEach(e=>{const a=byId[e.a],b=byId[e.b];if(!a||!b)return;
  let dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)+.01,rest=e.type==="gg"?90:120,f=(d-rest)*0.006*k;
  a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
 // radial anchoring keeps the three rings legible
 nodes.forEach(n=>{const R=n.kind==="gene"?0:n.kind==="task"?300:430;
  if(R){const dx=n.x-cx,dy=n.y-cy,d=Math.hypot(dx,dy)+.01,f=(d-R)*0.02*k;n.vx-=dx/d*f;n.vy-=dy/d*f;}
  n.x+=n.vx;n.y+=n.vy;n.vx*=0.86;n.vy*=0.86;});
 alpha*=0.985;
}

let hover=null,sel=null,focusIds=null,tsn=0;
function neighbors(id){const s=new Set([id]);E.forEach(e=>{if(e.a===id)s.add(e.b);if(e.b===id)s.add(e.a);});
 const n=byId[id];
 if(n&&n.kind==="gene"){GT.forEach(t=>s.add("t:"+t));} // gene lights its task panel
 if(n&&n.kind==="task"){G.genes.forEach(g=>s.add("g:"+g.id));}
 return s;}
function toScreen(n){return{x:(n.x-cam.x)*cam.z+W/2,y:(n.y-cam.y)*cam.z+H/2};}

function draw(){
 step();tsn+=0.02;
 ctx.clearRect(0,0,W,H);
 const foc=focusIds||(hover?neighbors(hover):(sel?neighbors(sel):null));
 // edges
 ctx.lineWidth=1;
 E.forEach(e=>{const a=byId[e.a],b=byId[e.b];if(!a||!b)return;
  if(!show[a.kind]||!show[b.kind])return;
  const on=foc&&(foc.has(e.a)&&foc.has(e.b));
  const A=toScreen(a),B=toScreen(b);
  ctx.strokeStyle=on?"rgba(18,160,171,.55)":(foc?"rgba(120,140,170,.05)":(e.type==="tm"?"rgba(230,161,60,.13)":"rgba(120,140,170,.10)"));
  ctx.lineWidth=on?1.6:1;ctx.beginPath();ctx.moveTo(A.x,A.y);ctx.lineTo(B.x,B.y);ctx.stroke();});
 // gene->task focus edges
 if(foc){const anchor=sel&&byId[sel]&&byId[sel].kind==="gene"?byId[sel]:(hover&&byId[hover]&&byId[hover].kind==="gene"?byId[hover]:null);
  if(anchor){const A=toScreen(anchor);GT.forEach(t=>{const tn=byId["t:"+t];if(!tn)return;const B=toScreen(tn);
   ctx.strokeStyle="rgba(138,123,230,.5)";ctx.lineWidth=1.3;ctx.beginPath();ctx.moveTo(A.x,A.y);ctx.lineTo(B.x,B.y);ctx.stroke();});}}
 // nodes
 nodes.forEach(n=>{if(!show[n.kind])return;const p=toScreen(n),on=!foc||foc.has(n.id);
  const r=n.r*cam.z*(n.id===hover||n.id===sel?1.5:1);
  const pulse=n.kind==="model"?1+0.12*Math.sin(tsn+n.x):1;
  ctx.globalAlpha=on?1:0.16;
  if(on&&(n.id===hover||n.id===sel)){ctx.shadowColor=COL[n.kind];ctx.shadowBlur=18;}else ctx.shadowBlur=0;
  ctx.fillStyle=COL[n.kind];ctx.beginPath();ctx.arc(p.x,p.y,r*pulse,0,6.283);ctx.fill();ctx.shadowBlur=0;
  // labels for hubs, tasks, models, and on focus
  if(on&&(n.kind!=="gene"||n.data.n>=6||n.id===hover||n.id===sel||cam.z>1.4)){
   ctx.globalAlpha=on?0.92:0.2;ctx.fillStyle="#dce4ef";
   ctx.font=(n.kind==="gene"?"600 ":"")+Math.max(9,11*Math.min(1.4,cam.z))+"px "+(n.kind==="gene"?"var(--mono)":"Arial");
   ctx.textAlign="center";ctx.fillText(n.label,p.x,p.y-r-4);}
  ctx.globalAlpha=1;});
 requestAnimationFrame(draw);
}
draw();

// ---- interaction ----
function pick(mx,my){let best=null,bd=1e9;nodes.forEach(n=>{if(!show[n.kind])return;const p=toScreen(n);
 const d=Math.hypot(p.x-mx,p.y-my);if(d<Math.max(9,n.r*cam.z+5)&&d<bd){bd=d;best=n;}});return best;}
let drag=null;
cv.addEventListener("mousemove",e=>{const mx=e.clientX,my=e.clientY;
 if(drag){cam.x-=(mx-drag.x)/cam.z;cam.y-=(my-drag.y)/cam.z;drag={x:mx,y:my};return;}
 const n=pick(mx,my);hover=n?n.id:null;cv.style.cursor=n?"pointer":"grab";});
cv.addEventListener("mousedown",e=>{const n=pick(e.clientX,e.clientY);if(!n)drag={x:e.clientX,y:e.clientY};});
window.addEventListener("mouseup",()=>drag=null);
cv.addEventListener("click",e=>{const n=pick(e.clientX,e.clientY);if(n){openNode(n);}else{closePanel();}});
cv.addEventListener("wheel",e=>{e.preventDefault();const f=e.deltaY<0?1.12:0.89;cam.z=Math.max(0.4,Math.min(4,cam.z*f));alpha=Math.max(alpha,0.05);},{passive:false});
document.getElementById("hint").style.opacity=0;setTimeout(()=>{const h=document.getElementById("hint");if(h)h.style.display="none";},4200);

// ---- legend + layer toggles ----
const LG=[["gene","Driver genes"],["task","Analysis tasks"],["model","Sequence models"],["cancer","Rare cancers (search)"]];
document.getElementById("legend").innerHTML="<b>Layers</b>"+LG.map(([k,l])=>
 `<div class="lrow${show[k]?"":" off"}" data-k="${k}"><span class="dot" style="background:${COL[k]}"></span>${l}<span class="toggle">${show[k]?"ON":"OFF"}</span></div>`).join("");
document.getElementById("legend").querySelectorAll(".lrow").forEach(r=>r.onclick=()=>{const k=r.dataset.k;show[k]=!show[k];
 r.classList.toggle("off",!show[k]);r.querySelector(".toggle").textContent=show[k]?"ON":"OFF";alpha=Math.max(alpha,0.05);});

// ---- panel content ----
const panel=document.getElementById("panel"),pbody=document.getElementById("pbody");
document.getElementById("px").onclick=closePanel;
function closePanel(){panel.classList.remove("on");sel=null;focusIds=null;}
function esc(s){return (s||"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}
function modelsFor(taskId){return G.models.filter(m=>m.tasks.includes(taskId));}
function openNode(n){sel=n.id;focusIds=neighbors(n.id);panel.classList.add("on");
 if(n.kind==="gene")pbody.innerHTML=geneCard(n.data);
 else if(n.kind==="model")pbody.innerHTML=modelCard(n.data);
 else if(n.kind==="task")pbody.innerHTML=taskCard(n.data);
 else if(n.kind==="cancer")pbody.innerHTML=cancerCard(n.data);
 alpha=Math.max(alpha,0.04);}
function geneCard(g){const ms=G.models;
 return `<div class="kind" style="color:${COL.gene}">Driver gene</div><h2>${g.id}</h2>
  <div class="meta">Drives <b>${g.n_cancers}</b> rare cancers in the catalog.</div>
  <div class="sec"><b>Run these tasks on ${g.id}</b>
   ${GT.map(t=>{const td=G.tasks.find(x=>x.id===t);const mm=modelsFor(t).map(m=>m.name).slice(0,4).join(", ");
    return `<div class="li" style="margin-bottom:7px"><span class="chip task">${td?td.label:t}</span><div class="li small">${mm||"see catalog"}</div></div>`;}).join("")}</div>
  <div class="sec"><b>Rare cancers driven by ${g.id}</b><div class="li small">${g.cancers.map(esc).join(" · ")}${g.n_cancers>g.cancers.length?" …":""}</div></div>`;}
function modelCard(m){return `<div class="kind" style="color:${COL.model}">Sequence model · ${esc(m.modality)}</div><h2>${esc(m.name)}</h2>
  <div class="meta">${esc(m.org)} · ${esc(m.params)} · ${esc(m.license)}</div>
  <div class="chips">${m.tasks.map(t=>`<span class="chip task">${t.replace(/_/g," ")}</span>`).join("")}</div>
  <div class="sec"><b>Rare cancer use</b><div class="li">${esc(m.use)}</div></div>
  <div class="sec"><b>Run it</b><div class="li small">${esc(m.framework)}<br>${esc(m.footprint)}<br>weights: ${esc(m.weights)}</div></div>
  ${m.caveat?`<div class="sec"><b>Caveat</b><div class="li small" style="color:var(--warn)">${esc(m.caveat)}</div></div>`:""}
  <div class="sec"><b>Source</b><div class="cite">${esc(m.citation)}</div></div>`;}
function taskCard(t){const mm=modelsFor(t.id);
 return `<div class="kind" style="color:${COL.task}">Analysis task</div><h2>${esc(t.label)}</h2>
  <div class="meta">${esc(t.desc)}</div>
  <div class="sec"><b>Models that perform this</b>${mm.map(m=>`<div class="mrow"><span class="nm">${esc(m.name)}</span><span class="md">${esc(m.modality)}</span></div>`).join("")||'<div class="li small">see catalog</div>'}</div>`;}
function cancerCard(c){return `<div class="kind" style="color:${COL.cancer}">Rare cancer</div><h2>${esc(c.name)}</h2>
  <div class="meta">${esc(c.system||"")}</div>
  <div class="chips">${c.genes.map(g=>`<span class="chip">${esc(g)}</span>`).join("")}</div>
  <div class="sec"><b>Suggested pipeline</b><div class="li">For each driver above, run zero-shot variant effect and missense pathogenicity (ESM-2, Nucleotide Transformer, AlphaMissense), splice disruption (SpliceAI, Pangolin), and expression from sequence (Borzoi, Enformer). Embed the tumor transcriptome with a single-cell model, benchmarked against simpler baselines.</div></div>`;}

// ---- search over cancers, genes, models ----
const q=document.getElementById("q"),sg=document.getElementById("sugg");
const idx=[...G.genes.map(g=>({t:"gene",label:g.id,data:g})),
 ...G.models.map(m=>({t:"model",label:m.name,data:m})),
 ...G.cancers.map(c=>({t:"cancer",label:c.name,data:c}))];
q.addEventListener("input",()=>{const v=q.value.trim().toLowerCase();if(!v){sg.classList.remove("on");return;}
 const hits=idx.filter(x=>x.label.toLowerCase().includes(v)).slice(0,40);
 sg.innerHTML=hits.map((h,i)=>`<div data-i="${i}"><span class="k">${h.t}</span>${esc(h.label)}</div>`).join("");
 sg.classList.toggle("on",hits.length>0);
 sg.querySelectorAll("div").forEach((d,i)=>d.onclick=()=>{sg.classList.remove("on");q.value=hits[i].label;pickResult(hits[i]);});});
function pickResult(h){
 if(h.t==="gene"){const n=byId["g:"+h.data.id];if(n){focusOn(n);openNode(n);}}
 else if(h.t==="model"){const n=byId["m:"+h.data.id];if(n){focusOn(n);openNode(n);}}
 else if(h.t==="cancer"){ // materialize the cancer + its driver genes into the graph
  const cid="c:"+h.data.name;if(!byId[cid])add({id:cid,kind:"cancer",label:h.data.name,r:7,x:cx,y:cy,data:h.data});
  show.cancer=true;const cn=byId[cid];h.data.genes.forEach(g=>{if(byId["g:"+g])E.push({a:cid,b:"g:"+g,w:1,type:"cg"});});
  focusOn(cn);openNode(cn);alpha=Math.max(alpha,0.6);
  document.getElementById("legend").querySelector('[data-k="cancer"]').classList.remove("off");}}
function focusOn(n){cam.x=n.x;cam.y=n.y;cam.z=1.5;alpha=Math.max(alpha,0.05);}
document.addEventListener("keydown",e=>{if(e.key==="Escape"){closePanel();sg.classList.remove("on");}});
</script>
"""

html = HTML.replace("__GRAPH__", GJSON)
os.makedirs(os.path.dirname(OUT_ART), exist_ok=True)
open(OUT_ART, "w", encoding="utf-8").write(html)
if os.path.isdir(os.path.dirname(OUT_SITE)):
    open(OUT_SITE, "w", encoding="utf-8").write(html)
assert "—" not in html and "–" not in html, "dash in atlas explorer"
print("ATLAS_EXPLORER_DONE bytes=%d genes=%d edges=%d models=%d cancers=%d -> %s" %
      (len(html), len(genes), len(edges), len(models), len(cancer_recs), OUT_ART))

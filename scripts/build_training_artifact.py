#!/usr/bin/env python3
"""Build the Anveshar training artifact: a self-contained page that shows a real training
run (ESM-2 pathogenicity head on ClinVar labels), maps every step to a Claude Science tool,
and gives fine-tuning recipes. Reads the training result JSON produced by the notebook/run.
Run: python3 scripts/build_training_artifact.py"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/tmp/tmp/pathogenicity_train_result.json"
OUT_ART = os.path.join(ROOT, "artifacts", "anveshar_training.html")
OUT_SITE = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/rarecancers/training.html"

r = json.load(open(RES))
DATA = json.dumps({"curve": [{"e": h["epoch"], "t": round(h["train_auc"], 4), "v": round(h["val_auc"], 4)} for h in r["curve"]],
                   "base": r["zeroshot_llr_auc"], "cv": r["trained_cv_auc_mean"], "cvsd": r["trained_cv_auc_std"],
                   "n": r["n"], "npath": r["n_path"], "genes": r["genes"]}, separators=(",", ":"))

HTML = r"""<title>Anveshar: train the models</title>
<style>
 :root{--bg:#070a10;--bg2:#0c111b;--ink:#e8eef6;--muted:#8b97ab;--line:#1c2432;
  --teal:#12a0ab;--teal2:#0b6b73;--amber:#e6a13c;--violet:#8a7be6;--warn:#e0b64a;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;--sans:Arial,Helvetica,sans-serif}
 *{box-sizing:border-box}
 body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55;
  background-image:radial-gradient(900px 520px at 20% -8%,rgba(18,160,171,.10),transparent 60%),radial-gradient(760px 500px at 96% 4%,rgba(230,161,60,.06),transparent 55%)}
 .wrap{max-width:1000px;margin:0 auto;padding:40px 22px 70px}
 .eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--teal)}
 h1{font-size:32px;margin:10px 0 6px;letter-spacing:-.02em;font-weight:800;text-wrap:balance}
 .sub{color:var(--muted);font-size:15.5px;max-width:70ch}
 .badge{display:inline-flex;align-items:center;gap:8px;margin-top:14px;font-size:12.5px;color:var(--ink);
  background:rgba(18,160,171,.12);border:1px solid rgba(18,160,171,.4);border-radius:20px;padding:6px 13px}
 .badge b{color:var(--teal)}
 h2{font-size:20px;margin:40px 0 4px;letter-spacing:-.01em}
 .lede{color:var(--muted);font-size:14px;margin:2px 0 14px;max-width:76ch}
 .result{display:grid;grid-template-columns:1.35fr 1fr;gap:18px;background:var(--bg2);border:1px solid var(--line);border-radius:16px;padding:18px;margin-top:14px}
 @media(max-width:760px){.result{grid-template-columns:1fr}}
 .cap{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
 svg{width:100%;height:auto;display:block}
 .kpis{display:flex;flex-direction:column;justify-content:center;gap:10px}
 .kpi{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:rgba(255,255,255,.02)}
 .kpi b{display:block;font-size:26px;font-variant-numeric:tabular-nums;letter-spacing:-.01em}
 .kpi.up b{color:var(--teal)} .kpi span{font-size:12px;color:var(--muted)}
 .arrow{font-size:22px;color:var(--amber);font-weight:800}
 .flow{counter-reset:s;margin-top:14px;display:grid;gap:9px}
 .step{display:flex;gap:13px;align-items:flex-start;background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:12px 15px}
 .step::before{counter-increment:s;content:counter(s);font-family:var(--mono);font-size:12px;font-weight:700;color:var(--bg);
  background:var(--teal);min-width:22px;height:22px;border-radius:6px;display:grid;place-items:center;margin-top:1px}
 .step .w{flex:1}.step h3{margin:0;font-size:14px}.step p{margin:3px 0 0;font-size:12.5px;color:var(--muted)}
 .tool{font-family:var(--mono);font-size:10.5px;color:var(--amber);background:rgba(230,161,60,.12);border:1px solid rgba(230,161,60,.3);border-radius:6px;padding:2px 7px;white-space:nowrap}
 .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px}
 @media(max-width:760px){.grid{grid-template-columns:1fr}}
 .card{background:var(--bg2);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
 .card h3{margin:0 0 4px;font-size:14.5px}.card .m{font-size:12px;color:var(--muted);margin-bottom:9px}
 pre{margin:0;background:#05070c;border:1px solid var(--line);border-radius:10px;padding:12px;overflow-x:auto;font-family:var(--mono);font-size:11.5px;line-height:1.5;color:#cdd6e4}
 pre .k{color:#7fd0d8}pre .s{color:#e6c98a}pre .c{color:#5b6b82}
 ol.strat{margin:10px 0 0;padding-left:20px}ol.strat li{font-size:13.5px;margin:6px 0;color:#cdd6e4}
 .links{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
 .links a{font-size:13px;color:var(--teal);text-decoration:none;border:1px solid var(--line);border-radius:20px;padding:7px 13px}
 .links a:hover{border-color:var(--teal)}
 .disc{margin-top:26px;padding:13px 15px;background:rgba(230,161,60,.06);border:1px solid rgba(230,161,60,.22);border-radius:12px;font-size:12.5px;color:#e6c98a}
 footer{margin-top:20px;padding-top:16px;border-top:1px solid var(--line);font-size:12px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;justify-content:space-between}
 footer a{color:var(--teal);text-decoration:none}
</style>
<div class="wrap">
 <div class="eyebrow">Anveshar &middot; training</div>
 <h1>Train a foundation model on your rare cancer</h1>
 <p class="sub">A rare cancer rarely has enough patients to train a model from scratch. The move is to take a model pretrained on millions of sequences and train a small supervised layer on the labels you have. Here is a real run, and how to drive the whole loop from inside Claude Science.</p>
 <div class="badge">Runnable from inside <b>Claude Science</b>: deep-research, the ClinVar and cBioPortal connectors, scvi-tools, and PubMed all in one loop.</div>

 <h2>A real training run</h2>
 <p class="lede">We pulled <span id="nv"></span> ClinVar-labeled missense variants across twelve rare-cancer driver genes, featurized each with ESM-2 (the zero-shot log-likelihood ratio plus the residue embedding), and trained a small head. It improves on the zero-shot score from notebook 09. Nothing is simulated.</p>
 <div class="result">
  <div><div class="cap">training curve (held-out AUC per epoch)</div><svg id="chart" viewBox="0 0 520 260" preserveAspectRatio="xMidYMid meet"></svg></div>
  <div class="kpis">
   <div class="kpi"><b><span id="base"></span> <span class="arrow">&rarr;</span> <span id="cv"></span></b><span>zero-shot ESM-2 LLR AUC to trained head AUC (5-fold CV)</span></div>
   <div class="kpi up"><b id="nvar2"></b><span>real ClinVar-labeled variants, <span id="np"></span> pathogenic, 12 driver genes</span></div>
   <div class="kpi"><b>minutes</b><span>featurize plus 5-fold cross-validate on one A40 or L40S GPU</span></div>
  </div>
 </div>

 <h2>The loop, inside Claude Science</h2>
 <p class="lede">Every step is a Claude skill or a connected database, so you can drive the whole thing by asking Claude.</p>
 <div class="flow">
  <div class="step"><div class="w"><h3>Choose and vet the model <span class="tool">deep-research skill</span></h3><p>Fan out searches, verify claims adversarially, and pick the model with the strongest evidence for the task.</p></div></div>
  <div class="step"><div class="w"><h3>Pull labeled data <span class="tool">ClinVar / cBioPortal / Open Targets connectors</span></h3><p>Retrieve labeled variants, cohort mutations, and target evidence for the driver genes, with provenance.</p></div></div>
  <div class="step"><div class="w"><h3>Prepare raw sequencing <span class="tool">nextflow-development skill</span></h3><p>Turn FASTQs into counts or variant calls with an nf-core pipeline when you start from raw data.</p></div></div>
  <div class="step"><div class="w"><h3>Train the layer <span class="tool">notebook 10</span></h3><p>Featurize with the foundation model and train a head, or LoRA fine-tune the backbone.</p></div></div>
  <div class="step"><div class="w"><h3>Single-cell fine-tune and baseline <span class="tool">scvi-tools / single-cell-rna-qc skills</span></h3><p>Fine-tune scGPT or Geneformer, and benchmark against a scVI or Harmony baseline, which often wins.</p></div></div>
  <div class="step"><div class="w"><h3>Validate against the literature <span class="tool">PubMed / Consensus / Paperclip</span></h3><p>Check the trained result against published evidence before trusting it.</p></div></div>
 </div>

 <h2>Recipes</h2>
 <div class="grid">
  <div class="card"><h3>Protein LM, LoRA</h3><div class="m">ESM-2 for missense pathogenicity</div>
<pre><span class="c"># pip install peft</span>
<span class="k">from</span> peft <span class="k">import</span> LoraConfig, get_peft_model
lora=LoraConfig(task_type=<span class="s">"SEQ_CLS"</span>,r=<span class="s">8</span>,
  target_modules=[<span class="s">"query"</span>,<span class="s">"value"</span>])
model=get_peft_model(base,lora)  <span class="c"># ~1% of weights</span></pre></div>
  <div class="card"><h3>DNA LM, fine-tune</h3><div class="m">Nucleotide Transformer or DNABERT-2</div>
<pre><span class="k">from</span> transformers <span class="k">import</span> AutoModelForSequenceClassification <span class="k">as</span> M
m=M.from_pretrained(
  <span class="s">"InstaDeepAI/nucleotide-transformer-v2-50m-multi-species"</span>,
  num_labels=<span class="s">2</span>)  <span class="c"># splice / promoter on driver introns</span></pre></div>
  <div class="card"><h3>Single-cell, fine-tune</h3><div class="m">scGPT or Geneformer, then benchmark</div>
<pre><span class="c"># scGPT pan-cancer checkpoint (5.7M cells)</span>
<span class="k">from</span> scgpt.tasks <span class="k">import</span> fine_tune_cell_type
<span class="c"># benchmark vs scVI/scANVI (scvi-tools skill)</span>
<span class="c"># baselines often win on rare tumors</span></pre></div>
  <div class="card"><h3>Frozen features, head</h3><div class="m">fastest and safest for a few hundred labels</div>
<pre>feats=esm2_embed(seq,pos)   <span class="c"># from notebook 09</span>
head=MLP(dim).fit(X_train,y_train)
<span class="c"># compare AUC to the zero-shot LLR baseline</span></pre></div>
 </div>

 <h2>Strategy for small label sets</h2>
 <ol class="strat">
  <li>Train a head on frozen features first; it is fast and resists overfitting on a few hundred labels.</li>
  <li>Move to LoRA only with more data, and prefer a smaller backbone (ESM-2 150M, Nucleotide Transformer 50M).</li>
  <li>Use stratified cross-validation and report a confidence interval, not a single split.</li>
  <li>Always compare against the zero-shot score and a simple baseline. If training does not beat them, do not ship it.</li>
 </ol>

 <div class="links">
  <a href="https://github.com/digvijayky/anveshar/blob/main/notebooks/10_training_sequence_models.ipynb" target="_blank" rel="noopener">Open notebook 10 &rarr;</a>
  <a href="https://github.com/digvijayky/anveshar/blob/main/notebooks/09_sequence_models_rare_cancer.ipynb" target="_blank" rel="noopener">Notebook 09: zero-shot &rarr;</a>
  <a href="https://github.com/digvijayky/anveshar/blob/main/data/sequence_models.json" target="_blank" rel="noopener">The model catalog &rarr;</a>
 </div>

 <div class="disc">Research and educational analysis of public data, not medical advice. Variant interpretation for care must follow ACMG guidelines and a qualified molecular pathologist. Trained scores must be benchmarked before any use.</div>
 <footer><span>Developer: <a href="https://digvijayky.com" target="_blank" rel="noopener">digvijayky</a></span><span>Anveshar, training sequence models for rare cancers</span></footer>
</div>
<script>
const R=__DATA__;
document.getElementById("nv").textContent=R.n;
document.getElementById("nvar2").textContent=R.n;
document.getElementById("np").textContent=R.npath;
document.getElementById("base").textContent=R.base.toFixed(2);
document.getElementById("cv").textContent=R.cv.toFixed(2);
(function(){
 const W=520,H=260,pl=44,pr=14,pt=14,pb=30,y0=0.5,y1=1.0;
 const xs=e=>pl+(W-pl-pr)*(e-1)/(R.curve.length-1);
 const ys=v=>pt+(H-pt-pb)*(1-(v-y0)/(y1-y0));
 let g="";
 // grid + y labels
 for(let t=0.5;t<=1.001;t+=0.1){const y=ys(t);g+=`<line x1="${pl}" y1="${y}" x2="${W-pr}" y2="${y}" stroke="#1c2432"/>`;
  g+=`<text x="${pl-6}" y="${y+3}" fill="#8b97ab" font-size="10" text-anchor="end" font-family="monospace">${t.toFixed(1)}</text>`;}
 // baseline (zero-shot)
 const by=ys(R.base);g+=`<line x1="${pl}" y1="${by}" x2="${W-pr}" y2="${by}" stroke="#c0392b" stroke-dasharray="4 3"/>`;
 g+=`<text x="${W-pr}" y="${by-4}" fill="#c0392b" font-size="10" text-anchor="end">zero-shot ${R.base.toFixed(2)}</text>`;
 const line=(key,col)=>{let d=R.curve.map((h,i)=>(i?"L":"M")+xs(h.e).toFixed(1)+" "+ys(h[key]).toFixed(1)).join(" ");
  return `<path d="${d}" fill="none" stroke="${col}" stroke-width="2"/>`;};
 g+=line("t","#0b6b73")+line("v","#e6a13c");
 g+=`<text x="${W-pr}" y="${ys(R.curve[R.curve.length-1].v)-5}" fill="#e6a13c" font-size="10" text-anchor="end">held-out ${R.cv.toFixed(2)} CV</text>`;
 g+=`<text x="${pl}" y="${H-8}" fill="#8b97ab" font-size="10" font-family="monospace">epoch</text>`;
 document.getElementById("chart").innerHTML=g;
})();
</script>
"""

html = HTML.replace("__DATA__", DATA)
open(OUT_ART, "w", encoding="utf-8").write(html)
if os.path.isdir(os.path.dirname(OUT_SITE)):
    open(OUT_SITE, "w", encoding="utf-8").write(html)
assert "—" not in html and "–" not in html, "dash in training artifact"
print("TRAINING_ARTIFACT_DONE bytes=%d auc %.3f->%.3f -> %s" % (len(html), r["zeroshot_llr_auc"], r["trained_cv_auc_mean"], OUT_ART))

#!/usr/bin/env python3
"""Assemble a static, self-hostable Anveshar website (for GitHub Pages at
digvijayky.github.io/rarecancers). Copies the rendered condition reports, builds a
searchable index over the full rare-conditions catalog, and rewrites cross links to be
relative so the site works under any base path. Run:  PYTHONPATH=. python3 scripts/build_site.py
"""
import os, re, json, glob, shutil, html

BASE = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos"
REPO = BASE + "/github/concord"
REPORTS_SRC = BASE + "/rare_cancer_hackathon/reports"
CATALOG = REPO + "/data/rare_conditions_catalog.json"
NETWORK_SRC = BASE + "/rare_cancer_hackathon/concord_network.html"
ANALYSIS_SRC = BASE + "/rare_cancer_hackathon/concord_analysis.html"
ATLAS_SRC = BASE + "/rare_cancer_hackathon/concord_atlas.html"
ANALYSES_SRC = BASE + "/rare_cancer_hackathon/concord_analyses.html"
MULTIMODAL_SRC = BASE + "/rare_cancer_hackathon/concord_multimodal.html"
OUT = BASE + "/rarecancers"

# condition -> report file (many alias keys per file)
DEEP = [
 ("renal_medullary.html", ["renal medullary carcinoma", "renal medullary"]),
 ("rectal_net_flagship.html", ["rectal neuroendocrine tumor", "rectal net", "rectal carcinoid", "rectal neuroendocrine neoplasm"]),
 ("chordoma.html", ["chordoma"]),
 ("adenoid_cystic_carcinoma.html", ["adenoid cystic carcinoma"]),
 ("alveolar_soft_part_sarcoma.html", ["alveolar soft part sarcoma"]),
 ("atrt.html", ["atypical teratoid rhabdoid tumor", "atrt", "rhabdoid tumor"]),
 ("ewing_sarcoma.html", ["ewing sarcoma", "ewing"]),
 ("uveal_melanoma.html", ["uveal melanoma", "ocular melanoma"]),
 ("nut_carcinoma.html", ["nut carcinoma", "nut midline carcinoma"]),
 ("spinal_muscular_atrophy.html", ["spinal muscular atrophy"]),
 ("duchenne_muscular_dystrophy.html", ["duchenne muscular dystrophy"]),
 ("cystic_fibrosis.html", ["cystic fibrosis"]),
 ("sickle_cell_disease.html", ["sickle cell disease", "sickle cell anemia"]),
 ("rpe65_retinal_dystrophy.html", ["rpe65 retinal dystrophy", "leber congenital amaurosis", "rpe65 related retinal dystrophy"]),
 ("hereditary_attr_amyloidosis.html", ["hereditary attr amyloidosis", "transthyretin amyloidosis", "attr amyloidosis", "hereditary transthyretin amyloidosis"]),
 ("gaucher_disease.html", ["gaucher disease"]),
 ("huntington_disease.html", ["huntington disease", "huntington"]),
 ("cholangiocarcinoma.html", ["cholangiocarcinoma", "bile duct cancer", "intrahepatic cholangiocarcinoma"]),
 ("gastrointestinal_stromal_tumor.html", ["gastrointestinal stromal tumor", "gist"]),
 ("pheochromocytoma_and_paraganglioma.html", ["pheochromocytoma and paraganglioma", "pheochromocytoma", "paraganglioma"]),
 ("medullary_thyroid_carcinoma.html", ["medullary thyroid carcinoma"]),
 ("merkel_cell_carcinoma.html", ["merkel cell carcinoma"]),
 ("dermatofibrosarcoma_protuberans.html", ["dermatofibrosarcoma protuberans"]),
 ("fabry_disease.html", ["fabry disease"]),
 ("pompe_disease.html", ["pompe disease", "acid maltase deficiency"]),
]
# claude.ai artifact uuid -> relative path, so the copied network/analysis are self contained
UUID = {
 "2353d56d-5999-4f36-a80b-37e9e825c077": "reports/renal_medullary.html",
 "ad8d8b93-ba99-4a78-b440-db3ee1676d1d": "reports/rectal_net_flagship.html",
 "a967676a-aefe-4631-aadd-521c469c1494": "reports/rectal_net_klempner.html",
 "0311f784-39ae-40f3-aeaa-13bb4d89fc74": "reports/rectal_net_sophisticated.html",
 "1cb33008-5ecd-4a73-b1e0-c7a0341f6ef9": "reports/spinal_muscular_atrophy.html",
 "9aeab4f3-0d3e-44a3-9fdd-f377d1f869fa": "reports/chordoma.html",
 "eb360eb4-2abb-4166-82ab-7e974e311467": "reports/adenoid_cystic_carcinoma.html",
 "93a2f8e4-da22-4c87-bfc6-bfa5b53e6835": "reports/alveolar_soft_part_sarcoma.html",
 "668fba3f-5f2d-47ba-879c-f67c3fb8175c": "reports/atrt.html",
 "74d610e5-24c1-454a-a29a-702578b7ca0f": "reports/ewing_sarcoma.html",
 "b9a65b7c-4039-43d1-a336-29ba14b51cef": "reports/uveal_melanoma.html",
 "27cee5c3-0aef-4c5a-b6b4-a863f50c49dd": "reports/nut_carcinoma.html",
 "6bcb53e4-e11d-4730-baa5-9d0919fe448b": "reports/duchenne_muscular_dystrophy.html",
 "ebb3d4ee-6c60-42a2-8637-2542774e9463": "reports/cystic_fibrosis.html",
 "ce3ef515-8165-4de7-9a51-ad6068487a2e": "reports/sickle_cell_disease.html",
 "8bddff09-657b-412a-9b2f-7a3b6bc388ce": "reports/rpe65_retinal_dystrophy.html",
 "dee01166-5c7b-42d6-b6db-579173800f15": "reports/hereditary_attr_amyloidosis.html",
 "a4caaca4-2634-4f83-93b7-e0d5fa0bbc72": "reports/gaucher_disease.html",
 "86361979-0b1c-497a-966a-832068356c76": "reports/huntington_disease.html",
 "21b36179-57ef-416b-840d-9937c86ddb54": "index.html",
 "b1d576d4-88e2-423a-bb77-d7490e822cb2": "network.html",
 "22355f01-16fe-4840-9ffc-636ac4f1a190": "analysis.html",
}

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()

def esc(s):
    return html.escape(str(s or ""))

def main():
    if os.path.isdir(OUT):
        for item in os.listdir(OUT):        # clear contents but keep .git so the repo survives rebuilds
            if item == ".git":
                continue
            p = os.path.join(OUT, item)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    else:
        os.makedirs(OUT)
    os.makedirs(OUT + "/reports", exist_ok=True)
    for h in glob.glob(REPORTS_SRC + "/*.html"):
        shutil.copy2(h, OUT + "/reports/" + os.path.basename(h))
    have = set(os.listdir(OUT + "/reports"))
    canon = {}
    for f, keys in DEEP:
        if f in have:
            for k in keys:
                canon[norm(k)] = f

    catalog = json.load(open(CATALOG, encoding="utf-8")) if os.path.exists(CATALOG) else []
    # ensure every deep report condition is in the catalog even if the compiler missed it
    seen = {norm(c.get("name", "")) for c in catalog}
    for f, keys in DEEP:
        if f in have and norm(keys[0]) not in seen:
            cat = "rare cancer" if "sarcoma" in keys[0] or "carcinoma" in keys[0] or "tumor" in keys[0] or "melanoma" in keys[0] or "chordoma" in keys[0] else "rare disease"
            catalog.append({"name": keys[0].title(), "category": cat, "slug": norm(keys[0]).replace(" ", "_"), "aliases": [], "key_gene_or_marker": ""})

    rows = []
    n_report = 0
    for c in catalog:
        name = c.get("name", "")
        keys = [name, c.get("slug", "").replace("_", " ")] + (c.get("aliases") or [])
        rep = ""
        for k in keys:
            if norm(k) in canon:
                rep = canon[norm(k)]; break
        if rep:
            n_report += 1
        short = "cancer" if c.get("category", "").startswith("rare cancer") else "disease"
        rows.append({"n": name, "c": short, "g": c.get("key_gene_or_marker", ""), "r": rep})
    rows.sort(key=lambda r: r["n"].lower())

    featured = "".join(
        f'<a class="fc" href="reports/{esc(r["r"])}"><span class="cb {r["c"]}">{r["c"]}</span>'
        f'<h3>{esc(r["n"])}</h3>{("<p>"+esc(r["g"])+"</p>") if r["g"] else ""}<span class="go">Open report</span></a>'
        for r in sorted([x for x in rows if x["r"]], key=lambda x: x["n"].lower()))

    data_js = json.dumps(rows, ensure_ascii=False)
    total = len(rows)
    page = INDEX.replace("__DATA__", data_js).replace("__TOTAL__", str(total)) \
                .replace("__NREPORT__", str(n_report)).replace("__FEATURED__", featured)
    assert "—" not in page and "–" not in page, "dash in index"
    open(OUT + "/index.html", "w", encoding="utf-8").write(page)

    for src, dst in [(NETWORK_SRC, "network.html"), (ANALYSIS_SRC, "analysis.html"),
                     (ATLAS_SRC, "atlas.html"), (ANALYSES_SRC, "analyses.html"),
                     (MULTIMODAL_SRC, "multimodal.html")]:
        if os.path.exists(src):
            t = open(src, encoding="utf-8").read()
            for u, rel in UUID.items():
                t = t.replace("https://claude.ai/code/artifact/" + u, rel)
            open(OUT + "/" + dst, "w", encoding="utf-8").write(t)

    json.dump(rows, open(OUT + "/catalog.json", "w", encoding="utf-8"), ensure_ascii=False)
    open(OUT + "/.nojekyll", "w").write("")
    print(f"SITE_DONE conditions={total} with_report={n_report} -> {OUT}")


INDEX = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anveshar: search a rare cancer or rare disease</title>
<style>
  :root{--paper:#F5F6F7;--surface:#fff;--ink:#0E1417;--slate:#44515A;--muted:#79868E;--line:#E4E9EB;
    --accent:#0B6B73;--accent-bright:#12A0AB;--disc:#5A57A6;--deep:#0C2024;
    --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
  *{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);line-height:1.55}
  .wrap{max-width:1080px;margin:0 auto;padding:0 22px}
  a{color:var(--accent);text-decoration:none}
  .hero{background:radial-gradient(1000px 460px at 72% -10%,rgba(18,160,171,.18),transparent),linear-gradient(180deg,var(--deep),#0A181B);color:#EAF1F1;border-bottom:3px solid var(--accent)}
  .hero .wrap{padding:52px 22px 40px}
  .brand{font-size:13px;font-weight:650;letter-spacing:.16em;text-transform:uppercase;color:#8FBDC0}
  h1{font-size:clamp(26px,4vw,42px);font-weight:740;letter-spacing:-.02em;margin:14px 0 0;max-width:20ch;color:#F3F8F8}
  .lede{color:#B7CFD0;margin-top:14px;max-width:60ch;font-size:17px}
  .search{margin-top:26px;position:relative;max-width:640px}
  .search input{width:100%;font-size:18px;padding:16px 18px 16px 46px;border-radius:12px;border:1px solid rgba(255,255,255,.2);
    background:rgba(255,255,255,.06);color:#fff;outline:none}
  .search input::placeholder{color:#8FBDC0}
  .search input:focus{border-color:var(--accent-bright);background:rgba(255,255,255,.1)}
  .search .ic{position:absolute;left:16px;top:15px;font-size:19px;opacity:.7}
  .hint{color:#8FBDC0;font-size:13px;margin-top:10px}
  main{padding:34px 0 20px}
  h2{font-size:19px;font-weight:700;letter-spacing:-.01em;margin:0 0 4px}
  .sub{color:var(--slate);margin:0 0 18px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
  .fc{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:18px;color:inherit;transition:border-color .15s,transform .12s}
  .fc:hover{border-color:var(--accent);transform:translateY(-2px)}
  .fc h3{font-size:16.5px;margin:9px 0 0} .fc p{font-size:12.5px;color:var(--muted);margin:6px 0 0;font-family:ui-monospace,Menlo,monospace}
  .fc .go{margin-top:auto;padding-top:14px;font-weight:640;font-size:13px;color:var(--accent)}
  .cb{align-self:flex-start;font-size:10.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:3px 8px;border-radius:6px}
  .cb.cancer{background:#E7F2F2;color:var(--accent)} .cb.disease{background:#EEEEF7;color:var(--disc)}
  #results{margin-top:6px}
  .row{display:flex;align-items:center;gap:12px;padding:12px 14px;border:1px solid var(--line);border-radius:11px;background:var(--surface);margin-bottom:8px}
  .row .nm{font-weight:640} .row .g{color:var(--muted);font-size:12.5px;font-family:ui-monospace,Menlo,monospace}
  .row .sp{flex:1} .row .open{font-weight:640;font-size:13px;white-space:nowrap}
  .row .soon{color:var(--muted);font-size:12.5px;white-space:nowrap}
  .nav{display:flex;flex-wrap:wrap;gap:12px;margin:30px 0}
  .nav a{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:11px 16px;font-weight:640;font-size:14px}
  .nav a:hover{border-color:var(--accent)}
  .disc{background:#FBF6EC;border:1px solid #EBDCC0;border-radius:12px;padding:14px 16px;color:#6B5A38;font-size:13px;margin:26px 0}
  footer{border-top:1px solid var(--line);padding:22px 0 44px;color:var(--muted);font-size:12.5px}
  .hide{display:none}
</style></head><body>
<header class="hero"><div class="wrap">
  <div class="brand">Anveshar</div>
  <h1>Search a rare cancer or rare disease</h1>
  <p class="lede">A translational board for rare conditions. Type your condition to open a cited report of therapies borrowed from other conditions that share its biology, or browse the catalog of __TOTAL__ conditions.</p>
  <div class="search"><span class="ic">&#128269;</span><input id="q" type="search" placeholder="Try renal medullary carcinoma, Fabry disease, GIST..." autocomplete="off"></div>
  <div class="hint">__NREPORT__ conditions have a full cited report today, and the catalog covers __TOTAL__. More reports are added continuously.</div>
</div></header>
<main class="wrap">
  <div id="results" class="hide"></div>
  <section id="featured">
    <h2>Conditions with a full report</h2>
    <p class="sub">Each report includes cross-condition therapies, confidence scores, novel hypotheses, a research workflow, and cited sources.</p>
    <div class="grid">__FEATURED__</div>
    <div class="nav">
      <a href="atlas.html">Rare cancer dependency atlas (every rare cancer)</a>
      <a href="analyses.html">Actionability, causes, and syndrome analyses</a>
      <a href="multimodal.html">Multi-modal analysis on real data (TCGA, MSK-IMPACT)</a>
      <a href="network.html">Explore the shared dependency network</a>
      <a href="analysis.html">Confidence ranked translation index</a>
    </div>
    <div class="disc"><b>Health information, not medical advice.</b> Anveshar is decision support for research and educational use, not a medical device. The final decision about any test or treatment must be made by your qualified health care provider.</div>
  </section>
</main>
<footer><div class="wrap">Developed by Dig Vijay Kumar Yarlagadda, <a href="https://digvijayky.com" target="_blank" rel="noopener">digvijayky.com</a></div></footer>
<script>
const CATALOG=__DATA__;
const q=document.getElementById("q"),res=document.getElementById("results"),feat=document.getElementById("featured");
function esc(s){return (s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));}
function render(term){
  term=term.trim().toLowerCase();
  if(!term){res.classList.add("hide");feat.classList.remove("hide");return;}
  feat.classList.add("hide");res.classList.remove("hide");
  const m=CATALOG.filter(x=>x.n.toLowerCase().includes(term)||(x.g&&x.g.toLowerCase().includes(term))).slice(0,200);
  if(!m.length){res.innerHTML='<div class="row"><span class="nm">No match.</span><span class="sp"></span><span class="soon">Try another spelling</span></div>';return;}
  res.innerHTML=m.map(x=>{
    const cb='<span class="cb '+x.c+'">'+x.c+'</span>';
    const g=x.g?'<span class="g">'+esc(x.g)+'</span>':'';
    const act=x.r?'<a class="open" href="reports/'+x.r+'">Open report &rarr;</a>':'<span class="soon">Report coming</span>';
    return '<div class="row">'+cb+'<span class="nm">'+esc(x.n)+'</span> '+g+'<span class="sp"></span>'+act+'</div>';
  }).join("");
}
q.addEventListener("input",e=>render(e.target.value));
</script></body></html>"""

if __name__ == "__main__":
    main()

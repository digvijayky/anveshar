"""Generate the Anveshar analyses artifact: actionability (borrowable approved therapies with
confidence and citations), etiology landscape, and hereditary syndrome map over all 504 rare
cancers. Self-contained, matches the atlas styling.
Run:  PYTHONPATH=. python3 scripts/build_analyses.py
"""
import os, json, html
from anveshar import analysis

BASE = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos"
OUT = BASE + "/rare_cancer_hackathon/concord_analyses.html"

asum = analysis.actionability_summary()
amap = analysis.actionable_map()
etio = analysis.etiology_landscape()
syn = analysis.hereditary_syndrome_map()
dsum = analysis.druggability_summary()
gap = analysis.druggability_gap()

def esc(s): return html.escape(str(s), quote=True)

# actionable table data (best match per cancer, plus its citation)
adata = []
for a in amap:
    m = min(a["matches"], key=lambda x: x["tier"])
    adata.append({"n": a["name"], "s": a["system"], "g": m["gene"], "d": m["drug"],
                  "ai": m["approved_in"], "ta": bool(m["tissue_agnostic"]),
                  "cl": a["confidence"]["label"], "cp": a["confidence"]["pct"],
                  "cav": m.get("caveat", ""), "u": (m.get("citation") or {}).get("url", ""),
                  "ct": (m.get("citation") or {}).get("label", "")})
ADATA = json.dumps(adata, ensure_ascii=False)

# etiology cards (server rendered)
etio_order = ["Infectious", "Environmental or carcinogen", "Hereditary syndrome",
              "Precursor lesion or transformation", "Cause not established"]
etio_cards = "".join(
    '<div class="ecard"><div class="en">%d</div><div class="el">%s</div>'
    '<div class="ex">%s</div></div>' % (
        etio[k]["count"], esc(k),
        ", ".join(esc(x) for x in etio[k]["examples"][:5]))
    for k in etio_order if k in etio)

gap_chips = "".join(
    '<span class="gchip"><b>%s</b> %d</span>' % (esc(g), len(cs)) for g, cs in gap[:16])

syn_cards = "".join(
    '<div class="scard"><div class="sn">%s</div><div class="sc">%d rare cancers</div>'
    '<div class="chips">%s</div></div>' % (
        esc(name), len(cs),
        " ".join('<span class="chip">%s</span>' % esc(c) for c in cs[:10])
        + ("" if len(cs) <= 10 else ' <span class="more">and %d more</span>' % (len(cs) - 10)))
    for name, cs in syn[:12])

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Anveshar: rare cancer analyses</title>
<style>
 :root{--ink:#14161c;--muted:#5b6472;--line:#e5e7ee;--surface:#fff;--bg:#f6f7fb;
   --accent:#2f5fe0;--disc:#7b3fe4;--disc-bg:#f2ecfe;--chipbg:#eef1f7;
   --hi:#127a3e;--hibg:#e5f5ec;--mod:#9a6a00;--modbg:#fbf1dd;--lo:#6b7280;--lobg:#eef0f3}
 *{box-sizing:border-box}
 body{margin:0;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:var(--bg);line-height:1.5}
 .wrap{max-width:1080px;margin:0 auto;padding:34px 22px 60px}
 h1{font-size:27px;margin:0 0 6px} h2{font-size:20px;margin:36px 0 6px}
 .lede{color:var(--muted);font-size:14.5px;margin:6px 0 0}
 .stat{display:flex;flex-wrap:wrap;gap:26px;margin:18px 0 4px;padding:16px 20px;background:var(--surface);border:1px solid var(--line);border-radius:14px}
 .stat div b{font-size:24px;display:block} .stat div span{font-size:12.5px;color:var(--muted)}
 .ctrl{margin:14px 0}
 .ctrl input{font:inherit;padding:9px 12px;border:1px solid var(--line);border-radius:9px;background:#fff;width:100%;max-width:460px}
 .count{font-size:12.5px;color:var(--muted);margin:8px 2px}
 table{width:100%;border-collapse:collapse;background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden}
 th,td{text-align:left;padding:9px 12px;font-size:13px;border-bottom:1px solid var(--line);vertical-align:top}
 th{background:#f0f2f8;font-size:11.5px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);position:sticky;top:0}
 .ta{display:inline-block;font-size:10px;font-weight:700;color:#fff;background:var(--accent);padding:2px 6px;border-radius:5px;margin-left:5px}
 .conf{white-space:nowrap;font-weight:700;font-size:12px}
 .bar{display:inline-block;height:7px;border-radius:4px;vertical-align:middle;margin-right:6px}
 .hi{color:var(--hi)} .mod{color:var(--mod)} .lo{color:var(--lo)}
 .barhi{background:var(--hi)} .barmod{background:var(--mod)} .barlo{background:var(--lo)}
 td a{color:var(--accent);text-decoration:none;font-weight:600}
 .cav{display:block;font-size:11px;color:var(--mod);font-style:italic;margin-top:3px}
 .egrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:12px}
 .ecard{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:12px;padding:14px}
 .en{font-size:26px;font-weight:800;color:var(--accent)} .el{font-weight:700;font-size:13.5px;margin:2px 0 6px}
 .ex{font-size:11.5px;color:var(--muted)}
 .sgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin-top:12px}
 .scard{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--disc);border-radius:12px;padding:14px 15px}
 .sn{font-weight:800;font-size:14px;color:var(--disc)} .sc{font-size:12px;color:var(--muted);margin:2px 0 8px}
 .chips{display:flex;flex-wrap:wrap;gap:5px} .chip{font-size:11px;background:var(--chipbg);color:#333;padding:3px 7px;border-radius:6px}
 .more{font-size:11px;color:var(--muted);font-style:italic}
 .gaprow{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
 .gchip{font-size:12.5px;background:#fdeaea;color:#8a1c1c;border:1px solid #f2c9c9;padding:5px 10px;border-radius:8px}
 .gchip b{font-weight:800;letter-spacing:.02em}
 .disc{margin-top:30px;padding:14px 16px;background:#fff7ed;border:1px solid #f3d8b0;border-radius:11px;font-size:12.5px;color:#7a4b12}
 footer{margin-top:26px;padding-top:16px;border-top:1px solid var(--line);font-size:12px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;justify-content:space-between}
 footer a{color:var(--accent);text-decoration:none}
</style></head><body><div class="wrap">
 <h1>Rare cancer translation analyses</h1>
 <p class="lede">Three catalog wide analyses over all @@NRARE@@ rare cancers: which carry a driver with a borrowable approved therapy (with confidence and a citation), what causes them, and which inherited syndromes predispose to them.</p>

 <h2>Actionability: borrowable approved therapies</h2>
 <p class="lede">A rare cancer whose driver already has an approved targeted therapy in some condition is a translation opportunity. Confidence follows a transparent rule: a tissue agnostic label reaches High, a cross tumor translation on the same target reaches Moderate, and each carries its source. A gene level match is a hypothesis; the specific variant still governs sensitivity.</p>
 <div class="stat">
   <div><b>@@NACT@@</b><span>rare cancers with a borrowable approved therapy</span></div>
   <div><b>@@PCT@@%</b><span>of the catalog</span></div>
   <div><b>@@NTA@@</b><span>via a tissue agnostic label</span></div>
 </div>
 <div class="ctrl"><input id="q" type="search" placeholder="Search cancer, gene, or drug" autocomplete="off"></div>
 <div class="count" id="count"></div>
 <div style="max-height:560px;overflow:auto;border-radius:12px">
 <table><thead><tr><th>Rare cancer</th><th>Driver</th><th>Borrowable therapy</th><th>Approved in</th><th>Confidence</th><th>Source</th></tr></thead>
 <tbody id="tb"></tbody></table></div>

 <h2>Highest unmet need: shared but undrugged dependencies</h2>
 <p class="lede">Of @@NSHARED@@ dependencies shared across more than one rare cancer, @@NUNMET@@ have no approved targeted therapy. These are the highest leverage drug development targets: making one of them tractable would help many rare cancers at once. Number shows how many rare cancers each drives.</p>
 <div class="gaprow">@@GAP@@</div>

 <h2>Etiology landscape</h2>
 <p class="lede">How the causes distribute across the catalog. A cancer can carry more than one category; where no cause is established, it is counted as such rather than assigned one.</p>
 <div class="egrid">@@ETIO@@</div>

 <h2>Hereditary predisposition syndromes</h2>
 <p class="lede">Inherited syndromes mapped to the rare cancers they cause, read from the cited causes field.</p>
 <div class="sgrid">@@SYN@@</div>

 <div class="disc">Anveshar is decision support for research and education, not medical advice. Confidence scores summarize evidence strength, not the probability of benefit for an individual patient. A driver gene match is a translation hypothesis; variant context, resistance, and tumor biology still govern whether a therapy works. Every treatment decision must be made by a qualified health care provider, ideally within a clinical trial.</div>
 <footer><span>Developed by Dig Vijay Kumar Yarlagadda, <a href="https://digvijayky.com" target="_blank" rel="noopener">digvijayky.com</a></span><span>Anveshar rare cancer analyses</span></footer>
</div>
<script>
const ADATA=@@ADATA@@;
const tb=document.getElementById('tb'),q=document.getElementById('q'),cnt=document.getElementById('count');
function esc(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function conf(d){
  const cls=d.cl==='High'?'hi':(d.cl==='Moderate'?'mod':'lo');
  const bcls=d.cl==='High'?'barhi':(d.cl==='Moderate'?'barmod':'barlo');
  return '<span class="conf '+cls+'"><span class="bar '+bcls+'" style="width:'+Math.round(d.cp*0.5)+'px"></span>'+esc(d.cl)+' '+d.cp+'%</span>';
}
function row(d){
  const ta=d.ta?'<span class="ta">tissue agnostic</span>':'';
  const src=d.u?('<a href="'+d.u+'" target="_blank" rel="noopener">source &#8599;</a>'):'';
  const cav=d.cav?('<span class="cav">'+esc(d.cav)+'</span>'):'';
  return '<tr><td>'+esc(d.n)+'<br><span style="font-size:11px;color:#5b6472">'+esc(d.s)+'</span></td>'+
    '<td>'+esc(d.g)+'</td><td>'+esc(d.d)+ta+cav+'</td><td style="font-size:12px;color:#374151">'+esc(d.ai)+'</td>'+
    '<td>'+conf(d)+'</td><td>'+src+'</td></tr>';
}
function render(){
  const t=(q.value||'').toLowerCase().trim();
  const out=ADATA.filter(d=>!t||(d.n+' '+d.s+' '+d.g+' '+d.d+' '+d.ai).toLowerCase().includes(t));
  tb.innerHTML=out.map(row).join('');
  cnt.textContent=out.length+' of '+ADATA.length+' actionable rare cancers';
}
q.addEventListener('input',render);render();
</script></body></html>"""

out = (PAGE
  .replace("@@NRARE@@", str(asum["n_rare_cancers"]))
  .replace("@@NACT@@", str(asum["n_actionable"]))
  .replace("@@PCT@@", str(asum["pct_actionable"]))
  .replace("@@NTA@@", str(asum["n_tissue_agnostic"]))
  .replace("@@NSHARED@@", str(dsum["n_shared_drivers"]))
  .replace("@@NUNMET@@", str(dsum["n_unmet_shared"]))
  .replace("@@GAP@@", gap_chips)
  .replace("@@ETIO@@", etio_cards)
  .replace("@@SYN@@", syn_cards)
  .replace("@@ADATA@@", ADATA))
open(OUT, "w", encoding="utf-8").write(out)
bad = [c for c in out if c in "—–"]
print("wrote", OUT, "actionable=", len(adata), "syndromes=", len(syn), "emdash=", len(bad), "tokens=", out.count("@@"))

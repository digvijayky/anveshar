"""Generate the rare cancer dependency atlas: a self-contained artifact covering every
rare cancer in the catalog, grouped by shared molecular dependency and organ system.

Run:  PYTHONPATH=. python3 scripts/build_atlas.py
Writes ../rare_cancer_hackathon/concord_atlas.html (picked up by build_site.py).
"""
import os, json, html
from anveshar import analysis

BASE = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos"
HACK = BASE + "/rare_cancer_hackathon"
OUT = os.path.join(HACK, "concord_atlas.html")
REPORTS = os.path.join(HACK, "reports")

rows = analysis.load_catalog()
summary = analysis.catalog_summary(rows)
shared = analysis.catalog_shared_drivers(rows)          # [(gene, [names])]
report_stems = {os.path.splitext(f)[0] for f in os.listdir(REPORTS) if f.endswith(".html")} \
    if os.path.isdir(REPORTS) else set()

# per cancer record for the searchable table
name_to_genes = {}
for g, names in shared:
    for n in names:
        name_to_genes.setdefault(n, []).append(g)

data = []
for r in rows:
    slug = r.get("slug", "")
    rep = "reports/%s.html" % slug if slug in report_stems else ""
    data.append({
        "n": r["name"],
        "s": r.get("organ_system", ""),
        "g": r.get("key_gene_or_marker", ""),
        "k": name_to_genes.get(r["name"], []),   # shared driver genes
        "c": r.get("causes", ""),                 # potential causes / etiology
        "ck": bool(r.get("cause_known", False)),  # is a cause established
        "r": rep,
    })
data.sort(key=lambda d: d["n"].lower())

systems = sorted({d["s"] for d in data if d["s"]})
top_clusters = shared[:24]

def esc(s): return html.escape(str(s), quote=True)

cluster_cards = "".join(
    '<div class="cl" data-gene="%s"><div class="clg">%s</div>'
    '<div class="cln">shared by %d rare cancers</div>'
    '<div class="clc">%s</div></div>' % (
        esc(g), esc(g), len(names),
        " ".join('<span class="chip">%s</span>' % esc(n) for n in names[:14])
        + ("" if len(names) <= 14 else ' <span class="more">and %d more</span>' % (len(names) - 14)))
    for g, names in top_clusters)

sys_opts = "".join('<option value="%s">%s</option>' % (esc(s), esc(s)) for s in systems)
DATA_JSON = json.dumps(data, ensure_ascii=False)

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Anveshar: rare cancer dependency atlas</title>
<style>
 :root{--ink:#14161c;--muted:#5b6472;--line:#e5e7ee;--surface:#fff;--bg:#f6f7fb;
   --accent:#2f5fe0;--accent-wash:#eaf0ff;--disc:#7b3fe4;--disc-bg:#f2ecfe;--chipbg:#eef1f7}
 *{box-sizing:border-box}
 body{margin:0;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:var(--bg);line-height:1.5}
 .wrap{max-width:1080px;margin:0 auto;padding:34px 22px 60px}
 h1{font-size:27px;margin:0 0 6px} h2{font-size:19px;margin:34px 0 4px}
 .lede{color:var(--muted);font-size:14.5px;margin:6px 0 0}
 .stat{display:flex;flex-wrap:wrap;gap:26px;margin:20px 0 6px;padding:16px 20px;background:var(--surface);
   border:1px solid var(--line);border-radius:14px}
 .stat div b{font-size:24px;display:block} .stat div span{font-size:12.5px;color:var(--muted)}
 .clgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin-top:14px}
 .cl{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--disc);
   border-radius:13px;padding:14px 15px;cursor:pointer;transition:box-shadow .12s}
 .cl:hover{box-shadow:0 4px 16px rgba(40,50,90,.10)}
 .clg{font-weight:800;font-size:15px;letter-spacing:.02em;color:var(--disc)}
 .cln{font-size:12px;color:var(--muted);margin:2px 0 8px}
 .clc{display:flex;flex-wrap:wrap;gap:5px}
 .chip{font-size:11px;background:var(--chipbg);color:#333;padding:3px 7px;border-radius:6px}
 .more{font-size:11px;color:var(--muted);font-style:italic}
 .ctrl{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}
 .ctrl input,.ctrl select{font:inherit;padding:9px 12px;border:1px solid var(--line);border-radius:9px;background:#fff}
 .ctrl input{flex:1;min-width:220px}
 table{width:100%;border-collapse:collapse;background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden}
 th,td{text-align:left;padding:9px 12px;font-size:13.5px;border-bottom:1px solid var(--line);vertical-align:top}
 th{background:#f0f2f8;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);position:sticky;top:0}
 td .sysb{font-size:11px;color:var(--muted)} td a{color:var(--accent);text-decoration:none;font-weight:600}
 td .gk{display:inline-block;font-size:11px;background:var(--disc-bg);color:var(--disc);padding:2px 6px;border-radius:5px;margin:1px 2px 1px 0}
 td .cause{font-size:12px;color:#374151;display:inline-block;max-width:340px}
 td .cause.unk{color:var(--muted);font-style:italic}
 .count{font-size:12.5px;color:var(--muted);margin:8px 2px}
 .disc{margin-top:30px;padding:14px 16px;background:#fff7ed;border:1px solid #f3d8b0;border-radius:11px;font-size:12.5px;color:#7a4b12}
 footer{margin-top:26px;padding-top:16px;border-top:1px solid var(--line);font-size:12px;color:var(--muted);
   display:flex;flex-wrap:wrap;gap:6px;justify-content:space-between}
 footer a{color:var(--accent);text-decoration:none}
</style></head><body><div class="wrap">
 <h1>Rare cancer dependency atlas</h1>
 <p class="lede">Every rare cancer in Anveshar, mapped to its molecular dependency. Where two cancers share a driver, a therapy proven against it in one becomes a translation candidate in the other. That overlap is what Anveshar searches.</p>
 <div class="stat">
   <div><b>@@NRARE@@</b><span>rare cancers catalogued</span></div>
   <div><b>@@NDRV@@</b><span>with a mapped molecular dependency</span></div>
   <div><b>@@NSHARE@@</b><span>dependencies shared across cancers</span></div>
   <div><b>@@NSYS@@</b><span>organ systems</span></div>
 </div>

 <h2>Shared molecular dependencies</h2>
 <p class="lede">Each dependency below appears in more than one rare cancer. Click one to filter the full list.</p>
 <div class="clgrid">@@CLUSTERS@@</div>

 <h2>Every rare cancer</h2>
 <div class="ctrl">
   <input id="q" type="search" placeholder="Search rare cancer, gene, or organ system" autocomplete="off">
   <select id="sys"><option value="">All organ systems</option>@@SYSOPTS@@</select>
 </div>
 <div class="count" id="count"></div>
 <div style="max-height:640px;overflow:auto;border-radius:12px">
 <table><thead><tr><th>Rare cancer</th><th>Organ system</th><th>Molecular dependency</th><th>Potential cause</th><th>Shared with</th></tr></thead>
 <tbody id="tb"></tbody></table></div>

 <div class="disc">Anveshar is decision support for research and education, not medical advice. Rare cancer definitions follow the WHO Classification of Tumours 5th edition, Orphanet, the NCI rare cancers list, and RARECAREnet. A blank dependency means no single defining driver is catalogued, not that none exists. Any treatment decision must be made by a qualified health care provider.</div>
 <footer><span>Developer: <a href="https://digvijayky.com" target="_blank" rel="noopener">digvijayky</a></span><span>Anveshar rare cancer dependency atlas</span></footer>
</div>
<script>
const DATA=@@DATA@@;
const tb=document.getElementById('tb'),q=document.getElementById('q'),sys=document.getElementById('sys'),cnt=document.getElementById('count');
function esc(s){const d=document.createElement('div');d.textContent=s;return d.innerHTML;}
function row(d){
  const rep=d.r?(' <a href="'+d.r+'" target="_blank" rel="noopener">report &#8599;</a>'):'';
  const gk=(d.k||[]).map(g=>'<span class="gk">'+esc(g)+'</span>').join('');
  const drv=d.g?esc(d.g):'<span class="sysb">not catalogued</span>';
  const cause=d.c?('<span class="cause'+(d.ck?'':' unk')+'">'+esc(d.c)+'</span>')
                 :'<span class="cause unk">Cause not established</span>';
  return '<tr><td>'+esc(d.n)+rep+'</td><td class="sysb">'+esc(d.s)+'</td><td>'+drv+'</td><td>'+cause+'</td><td>'+gk+'</td></tr>';
}
function render(){
  const term=(q.value||'').toLowerCase().trim(), s=sys.value;
  const out=DATA.filter(d=>{
    if(s&&d.s!==s)return false;
    if(!term)return true;
    return (d.n+' '+d.s+' '+d.g+' '+(d.c||'')+' '+(d.k||[]).join(' ')).toLowerCase().includes(term);
  });
  tb.innerHTML=out.map(row).join('');
  cnt.textContent=out.length+' of '+DATA.length+' rare cancers';
}
document.querySelectorAll('.cl').forEach(c=>c.addEventListener('click',()=>{q.value=c.dataset.gene;sys.value='';render();window.scrollBy({top:0});document.getElementById('q').scrollIntoView({behavior:'smooth',block:'center'});}));
q.addEventListener('input',render);sys.addEventListener('change',render);render();
</script></body></html>"""

out = (PAGE
    .replace("@@NRARE@@", str(summary["n_rare_cancers"]))
    .replace("@@NDRV@@", str(summary["n_with_driver"]))
    .replace("@@NSHARE@@", str(summary["n_shared_drivers"]))
    .replace("@@NSYS@@", str(summary["n_systems"]))
    .replace("@@CLUSTERS@@", cluster_cards)
    .replace("@@SYSOPTS@@", sys_opts)
    .replace("@@DATA@@", DATA_JSON))
open(OUT, "w", encoding="utf-8").write(out)
bad = [c for c in out if c in "—–"]
print("wrote", OUT, "cancers=", len(data), "clusters=", len(top_clusters), "emdash=", len(bad))

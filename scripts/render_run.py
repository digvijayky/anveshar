"""Render a Anveshar pipeline run into a self-contained, shareable HTML run report.

Run:  PYTHONPATH=. python3 scripts/render_run.py "renal medullary carcinoma" [--live] [--out path.html]
Shows the bespoke comp-bio workflow, the databases queried (provenance), the borrowable
therapies with confidence and citations, and the cross condition candidates. Research use only.
"""
import sys, os, html, re
from anveshar import pipeline

def esc(s): return html.escape(str(s), quote=True)

def render(name, live=False, out=None):
    d = pipeline.run(name, live=live)
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    out = out or ("/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos/"
                  "rare_cancer_hackathon/concord_run_" + slug + ".html")
    if not d["resolved"]:
        body = f"<h1>No rare cancer matched {esc(name)}</h1><p>{esc(d['disclaimer'])}</p>"
        open(out, "w").write("<!doctype html><meta charset=utf-8><body>" + body)
        return out, d
    s = d["summary"]; bc = s["best_confidence"]
    w = d["workflow"]

    steps = "".join(
        f'<div class="wstep"><div class="wt">{i+1}. {esc(st["title"])}</div>'
        f'<div class="ww">{esc(st["what"])}</div>'
        f'<div class="wm">{"".join(f"<span class=wtag>{esc(t.strip())}</span>" for t in st["tools"].replace(";", ",").split(",") if t.strip())}</div>'
        f'<div class="wc">Checkpoint: {esc(st["outputs"])}</div></div>'
        for i, st in enumerate(w["steps"]))

    prov = "".join(
        f'<tr><td>{esc(p["stage"])}</td><td>{esc(p["source"])}</td><td class=q>{esc(p["query"])}</td>'
        f'<td>{esc(p["n"])}</td><td class=nt>{esc(p["note"])}</td></tr>'
        for p in d["provenance"])

    def confbar(c):
        cls = "hi" if c["label"] == "High" else ("mod" if c["label"] == "Moderate" else "lo")
        return (f'<span class="conf {cls}"><span class="bar bar{cls}" '
                f'style="width:{round(c["pct"]*0.5)}px"></span>{esc(c["label"])} {c["pct"]}%</span>')

    ther = "".join(
        f'<tr><td>{esc(m["gene"])}</td><td>{esc(m["drug"])}'
        + (f'<div class=cav>{esc(m["caveat"])}</div>' if m.get("caveat") else "")
        + f'</td><td class=ai>{esc(m["approved_in"])}</td>'
        f'<td>{confbar(pipeline.analysis.therapy_confidence({"tier": m["tier"], "citation": m["citation"]}))}</td>'
        f'<td>{"<a href=" + esc(m["citation"]["url"]) + " target=_blank rel=noopener>source &#8599;</a>" if m.get("citation", {}).get("url") else ""}</td></tr>'
        for m in w and d["translation"]["actionable"])
    if not d["translation"]["actionable"]:
        ther = '<tr><td colspan=5 class=nt>No approved therapy targets this driver yet. See the unmet need analysis.</td></tr>'

    cross = "".join(
        f'<div class="ccard"><div class="cg">{esc(g)}</div><div class="chips">'
        + " ".join(f'<span class=chip>{esc(c)}</span>' for c in cs[:12])
        + ("" if len(cs) <= 12 else f' <span class=more>and {len(cs)-12} more</span>')
        + "</div></div>"
        for g, cs in (d["translation"]["cross_condition"] or {}).items())

    ind_block = ""
    ind = d.get("induced_dependencies") or {}
    if ind:
        cards = "".join(
            f'<div class=aim><b>Synthetic lethal pivot.</b> {esc(g)} is a tumor suppressor and cannot be '
            f'drugged directly; its loss induces a dependency on <b>{esc(e["dependency"])}</b>, the druggable '
            f'node ({esc(e["drug"])}). {esc(e["relationship"])}. '
            f'<a href="{esc(e["citation"]["url"])}" target=_blank rel=noopener>source &#8599;</a></div>'
            for g, e in ind.items())
        ind_block = "<h2>Induced dependency (synthetic lethality)</h2>" + cards

    val_block = ""
    tv = d.get("target_validation") or {}
    tv_rows = [(g, v) for g, v in tv.items() if v.get("available")]
    if tv_rows:
        def vpill(v):
            ok = v["verdict"].startswith("Validated")
            cls = "hi" if ok else ("mod" if "Tractable" in v["verdict"] else "lo")
            return f'<span class="conf {cls}"><span class="bar bar{cls}" style="width:{round(v["score"]*0.5)}px"></span>{v["score"]}/100</span>'
        rows = "".join(
            f'<tr><td>{esc(g)}</td><td>{vpill(v)}</td><td>{esc(v["verdict"])}</td>'
            f'<td>SM {esc(v["sm_tractability"])}/10, AB {esc(v["ab_tractability"])}/10</td>'
            f'<td>{"common essential" if v["common_essential"] else ("selective dependency" if v["selective_dependency"] else "not a selective dependency")}'
            f'{" (DepMap min " + str(v["essentiality"]["min"]) + ")" if v.get("essentiality") else ""}</td>'
            f'<td>{esc(v["safety_liabilities"])}</td>'
            f'<td><a href="{esc(v["source"]["url"])}" target=_blank rel=noopener>OT &#8599;</a></td></tr>'
            for g, v in tv_rows)
        val_block = ('<h2>Target validation (functional genomics)</h2>'
                     '<div class=sub>Druggability tractability and DepMap CRISPR gene essentiality from Open Targets. '
                     'A validated target is tractable and a selective dependency; a common essential gene carries a systemic selectivity risk.</div>'
                     '<div class=scroll><table><thead><tr><th>Gene</th><th>Validation score</th><th>Verdict</th>'
                     '<th>Tractability</th><th>Dependency (DepMap)</th><th>Safety liabilities</th><th>Source</th></tr></thead><tbody>'
                     + rows + '</tbody></table></div>')

    live_block = ""
    if live and d.get("databases"):
        rows = []
        for g, db in d["databases"].items():
            rows.append(f'<tr><td>{esc(g)}</td><td>{esc(db.get("opentargets_symbol",""))}</td>'
                        f'<td>{esc(", ".join(db.get("opentargets_drugs",[])[:5]) or "none")}</td>'
                        f'<td class=nt>{esc(", ".join(db.get("opentargets_diseases",[])[:4]))}</td>'
                        f'<td>{esc(db.get("ensembl_id",""))}</td></tr>')
        live_block = ('<h2>Live database results</h2><div class=scroll><table><thead><tr>'
                      '<th>Gene</th><th>Open Targets symbol</th><th>Known drugs</th>'
                      '<th>Associated diseases</th><th>Ensembl</th></tr></thead><tbody>'
                      + "".join(rows) + "</tbody></table></div>")

    page = f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1">
<title>Anveshar run: {esc(d['condition'])}</title>
<style>
 :root{{--ink:#14161c;--muted:#5b6472;--line:#e5e7ee;--surface:#fff;--bg:#f6f7fb;--accent:#2f5fe0;
   --disc:#7b3fe4;--disc-bg:#f2ecfe;--chipbg:#eef1f7;--hi:#127a3e;--mod:#9a6a00;--lo:#6b7280}}
 *{{box-sizing:border-box}} body{{margin:0;font-family:Arial,Helvetica,sans-serif;color:var(--ink);background:var(--bg);line-height:1.5}}
 .wrap{{max-width:960px;margin:0 auto;padding:32px 22px 60px}}
 h1{{font-size:25px;margin:0 0 4px}} h2{{font-size:18px;margin:32px 0 8px}}
 .sub{{color:var(--muted);font-size:14px}} .mode{{display:inline-block;font-size:11px;font-weight:700;color:#fff;background:var(--accent);padding:2px 8px;border-radius:6px;margin-left:6px}}
 .stat{{display:flex;flex-wrap:wrap;gap:22px;margin:16px 0;padding:14px 18px;background:var(--surface);border:1px solid var(--line);border-radius:13px}}
 .stat div b{{font-size:22px;display:block}} .stat div span{{font-size:12px;color:var(--muted)}}
 .cmd{{font-family:ui-monospace,Menlo,monospace;font-size:12.5px;background:#0f172a;color:#e2e8f0;padding:10px 13px;border-radius:9px;overflow-x:auto}}
 .aim{{background:var(--disc-bg);border-left:4px solid var(--disc);border-radius:10px;padding:12px 14px;font-size:14px;margin:10px 0}}
 .wstep{{background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:11px;padding:13px 15px;margin-bottom:9px}}
 .wt{{font-weight:750;font-size:15px}} .ww{{font-size:13.5px;color:#374151;margin:5px 0}}
 .wm{{display:flex;flex-wrap:wrap;gap:6px;margin:7px 0}} .wtag{{font-size:11px;color:var(--accent);background:#eaf0ff;padding:3px 8px;border-radius:6px}}
 .wc{{font-size:12px;color:var(--muted);font-style:italic}}
 table{{width:100%;border-collapse:collapse;background:var(--surface);border:1px solid var(--line);border-radius:11px;overflow:hidden}}
 th,td{{text-align:left;padding:8px 11px;font-size:12.5px;border-bottom:1px solid var(--line);vertical-align:top}}
 th{{background:#f0f2f8;font-size:11px;text-transform:uppercase;color:var(--muted)}}
 .q{{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:var(--muted)}} .nt{{color:var(--muted)}} .ai{{color:#374151}}
 .conf{{white-space:nowrap;font-weight:700;font-size:12px}} .bar{{display:inline-block;height:7px;border-radius:4px;vertical-align:middle;margin-right:6px}}
 .hi{{color:var(--hi)}} .mod{{color:var(--mod)}} .lo{{color:var(--lo)}} .barhi{{background:var(--hi)}} .barmod{{background:var(--mod)}} .barlo{{background:var(--lo)}}
 .cav{{font-size:11px;color:var(--mod);font-style:italic;margin-top:3px}}
 .ccard{{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:11px 13px;margin-bottom:8px}}
 .cg{{font-weight:800;color:var(--disc);font-size:13px;margin-bottom:5px}}
 .chips{{display:flex;flex-wrap:wrap;gap:5px}} .chip{{font-size:11px;background:var(--chipbg);padding:3px 7px;border-radius:6px}} .more{{font-size:11px;color:var(--muted);font-style:italic}}
 .scroll{{overflow-x:auto}} td a{{color:var(--accent);text-decoration:none;font-weight:600}}
 .disc{{margin-top:26px;padding:13px 15px;background:#fff7ed;border:1px solid #f3d8b0;border-radius:11px;font-size:12.5px;color:#7a4b12}}
 footer{{margin-top:22px;padding-top:14px;border-top:1px solid var(--line);font-size:12px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;justify-content:space-between}} footer a{{color:var(--accent);text-decoration:none}}
</style></head><body><div class=wrap>
 <h1>Anveshar workflow run: {esc(d['condition'])}<span class=mode>{esc(d['mode'])} mode</span></h1>
 <div class=sub>{esc(d['system'])} &middot; driver {esc(", ".join(d['drivers']) or "none catalogued")} &middot; class {esc(w['driver_class'])}</div>
 <div class=stat>
   <div><b>{s['n_actionable']}</b><span>borrowable approved therapies</span></div>
   <div><b>{s['n_tissue_agnostic']}</b><span>tissue agnostic</span></div>
   <div><b>{s['n_cross_condition']}</b><span>shared driver candidates</span></div>
   <div><b>{(bc['label']+' '+str(bc['pct'])+'%') if bc else 'n/a'}</b><span>best confidence</span></div>
 </div>

 <h2>Bespoke comp-bio workflow</h2>
 <div class=aim><b>Aim.</b> {esc(w['aim'])} <b>Hypothesis.</b> {esc(w['hypothesis'])}</div>
 {steps}
 <div class=cmd>{esc(w['how_to_run'])}</div>

 <h2>Borrowable approved therapies</h2>
 <div class=scroll><table><thead><tr><th>Driver</th><th>Therapy</th><th>Approved in</th><th>Confidence</th><th>Source</th></tr></thead><tbody>{ther}</tbody></table></div>

 <h2>Cross condition candidates (shared dependency)</h2>
 {cross or '<div class=nt>No other catalogued rare cancer shares this driver.</div>'}

 {ind_block}

 {val_block}

 {live_block}

 <h2>Provenance: every stage, auditable</h2>
 <div class=scroll><table><thead><tr><th>Stage</th><th>Source</th><th>Query</th><th>n</th><th>Note</th></tr></thead><tbody>{prov}</tbody></table></div>

 <div class=disc>{esc(d['disclaimer'])}</div>
 <footer><span>Developer: <a href="https://digvijayky.com" target="_blank" rel="noopener">digvijayky</a></span><span>Anveshar workflow run report</span></footer>
</div></body></html>"""
    assert "—" not in page and "–" not in page, "dash leaked"
    open(out, "w", encoding="utf-8").write(page)
    return out, d


if __name__ == "__main__":
    args = sys.argv[1:]
    live = "--live" in args
    outp = None
    if "--out" in args:
        outp = args[args.index("--out") + 1]
    names = [a for a in args if not a.startswith("--") and a != outp]
    name = " ".join(names)
    path, d = render(name, live=live, out=outp)
    print("wrote", path, "| resolved:", d.get("resolved"), "| mode:", d.get("mode"))

"""Re-skin every rendered report with the current template, preserving its DATA.

Extracts the embedded `const DATA = {...};` from each report HTML and re-injects it
into the current template, so template-level changes (default reading level, new
sections) propagate to all reports without needing their source JSON.
Run:  PYTHONPATH=. python3 scripts/reskin_reports.py
"""
import os, re, glob
from anveshar.report import render

BASE = "/data1/lesliec/vijay/spatial_transcriptomicsg/my_work_Gosabopos"
REPORTS = BASE + "/rare_cancer_hackathon/reports"
PAT = re.compile(r"/\*DATA_START\*/\s*(const DATA = .*?;)\s*/\*DATA_END\*/", re.S)

done = skip = 0
for f in sorted(glob.glob(REPORTS + "/*.html")):
    txt = open(f, encoding="utf-8").read()
    m = PAT.search(txt)
    if not m:
        print("skip (no DATA block):", os.path.basename(f)); skip += 1; continue
    render._write(render.TEMPLATE, m.group(1), f)
    done += 1
print(f"reskinned {done} reports, skipped {skip}")

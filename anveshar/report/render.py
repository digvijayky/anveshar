#!/usr/bin/env python3
"""Anveshar report renderer: inject a validated DATA dict into the HTML template.

Importable API:
    render_data(data: dict, out_html, base=TEMPLATE) -> out_html
    render_report(report, out_html, base=TEMPLATE) -> out_html   # report has .to_render_dict()

CLI (standalone), preserved for the render pipeline:
    python3 render.py <base_html> <data_json> <out_html> [patient_json]
    python3 render.py --patient <base_html_with_inline_DATA> <patient_json> <out_html>

The renderer enforces the no em/en dash rule and validates the DATA block before writing.
"""
import sys, os, re, json

TEMPLATE = os.path.join(os.path.dirname(__file__), "template.html")
REQUIRED = ["cancer", "overview", "targets", "therapies", "trials", "precedents", "disclaimer"]


def _norm(t):
    n = t.count("—") + t.count("–")
    return t.replace("—", ", ").replace("–", "-"), n


def _dump(o):
    return json.dumps(o, ensure_ascii=False)


def _load(p):
    raw, n = _norm(open(p, encoding="utf-8").read())
    if n:
        print(f"[render] normalized {n} dash(es) in {p}")
    return json.loads(raw)


def _expand(c):
    if isinstance(c, dict) and isinstance(c.get("url", ""), str):
        u = c["url"]
        if u.startswith("PMID:"):
            c["url"] = "https://pubmed.ncbi.nlm.nih.gov/" + u[5:].strip() + "/"
        elif u.startswith("NCT"):
            c["url"] = "https://clinicaltrials.gov/study/" + u.strip()
        elif u.startswith("DOI:"):
            c["url"] = "https://doi.org/" + u[4:].strip()


def _expand_all(data):
    for x in data.get("therapies", []):
        _expand(x.get("citation", {}))
        if x.get("trial"):
            _expand(x["trial"])
    for x in data.get("precedents", []):
        _expand(x.get("citation", {}))
    for x in data.get("discovery", []):
        _expand(x.get("citation", {}))
    for x in data.get("trials", []):
        _expand(x)


def _write(base, payload, out):
    txt, _ = _norm(open(base, encoding="utf-8").read())
    o, n = re.subn(r"/\*DATA_START\*/.*?/\*DATA_END\*/",
                   "/*DATA_START*/\n" + payload + "\n/*DATA_END*/", txt, flags=re.S)
    if n != 1:
        sys.exit(f"[render] ERROR expected 1 DATA block, got {n}")
    assert "—" not in o and "–" not in o, "[render] dash leaked into output"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(o)


def render_data(data: dict, out_html: str, base: str = TEMPLATE) -> str:
    """Inject a DATA dict into the template and write out_html. Returns out_html."""
    _expand_all(data)
    from ..score import score_report
    score_report(data)
    _write(base, "const DATA = " + _dump(data) + ";", out_html)
    print(f"[render] wrote {out_html}: {len(data.get('therapies', []))} therapies, "
          f"{len(data.get('discovery', []))} hypotheses")
    return out_html


def render_report(report, out_html: str, base: str = TEMPLATE) -> str:
    """Render a DiseaseReport (or a raw DATA dict) to out_html."""
    data = report.to_render_dict() if hasattr(report, "to_render_dict") else report
    return render_data(data, out_html, base)


def main():
    a = sys.argv[1:]
    if a and a[0] == "--patient":
        base, patient_p, out = a[1], a[2], a[3]
        txt, _ = _norm(open(base, encoding="utf-8").read())
        m = re.search(r"/\*DATA_START\*/\s*(const DATA = .*?;)\s*/\*DATA_END\*/", txt, flags=re.S)
        if not m:
            sys.exit("[render] ERROR no inline DATA block in base")
        patient = _load(patient_p)
        inj = m.group(1)[:-2] + ",\n  patient: " + _dump(patient) + "\n};"
        _write(base, inj, out)
        print(f"[render] wrote {out} with patient ({len(patient.get('alterations', []))} alterations)")
        return
    base, data_p, out = a[0], a[1], a[2]
    data = _load(data_p)
    miss = [k for k in REQUIRED if k not in data]
    if miss:
        sys.exit(f"[render] ERROR missing keys {miss}")
    if len(a) > 3:
        data["patient"] = _load(a[3])
    render_data(data, out, base)


if __name__ == "__main__":
    main()

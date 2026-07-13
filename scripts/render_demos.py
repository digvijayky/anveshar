"""Render every shipped Anveshar demo report to outputs/.

Run from the repo root:  PYTHONPATH=. python3 scripts/render_demos.py
Reproduces the disease boards, the two personalized cases, and the rare-disease demo,
each with the novel discovery layer, from the curated cited knowledge in examples/.
"""
import os
from anveshar.engine import run

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "outputs")
PROF = os.path.join(ROOT, "examples", "profiles")
os.makedirs(OUT, exist_ok=True)

DEMOS = [
    ("renal medullary carcinoma", None, "renal_medullary.html"),
    ("rectal neuroendocrine tumor", None, "rectal_net.html"),
    ("rectal neuroendocrine tumor", os.path.join(PROF, "klempner_braf.json"), "rectal_net_braf_patient.html"),
    ("rectal neuroendocrine tumor", os.path.join(PROF, "pereira_msi_braf.json"), "rectal_net_sophisticated.html"),
    ("spinal muscular atrophy", None, "spinal_muscular_atrophy.html"),
]

if __name__ == "__main__":
    for cancer, prof, fname in DEMOS:
        try:
            d = run(cancer, profile=prof, discovery=True, out=os.path.join(OUT, fname))
            print(f"{fname}: {len(d.get('therapies', []))} therapies, "
                  f"{len(d.get('discovery', []))} novel hypotheses")
        except Exception as e:
            print(f"{fname}: ERROR {e!r}")

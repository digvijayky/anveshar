"""Attach potential causes (etiology) to each rare-cancer catalog entry.

Reads tmp/tmp/causes_*.json (name -> {causes, known, source}) and writes
`causes`, `cause_known`, and `cause_source` onto matching rare cancers.
"""
import json, glob, re, shutil
from collections import Counter

CAT = "data/rare_conditions_catalog.json"

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()

cat = json.load(open(CAT))
shutil.copy2(CAT, CAT + ".bak_causes")
by_name = {r["name"]: r for r in cat}
by_norm = {norm(r["name"]): r for r in cat}

recs = {}
for fp in sorted(glob.glob("tmp/tmp/causes_*.json")):
    recs.update(json.load(open(fp)))

matched = unmatched = 0
miss = []
for name, rec in recs.items():
    r = by_name.get(name) or by_norm.get(norm(name))
    if not r:
        unmatched += 1; miss.append(name); continue
    r["causes"] = (rec.get("causes") or "").strip()
    r["cause_known"] = bool(rec.get("known"))
    if rec.get("source"):
        r["cause_source"] = rec["source"]
    matched += 1

json.dump(cat, open(CAT, "w"), indent=2, ensure_ascii=False)

cancers = [r for r in cat if r.get("category") == "rare cancer"]
with_cause = [r for r in cancers if r.get("causes")]
known = [r for r in with_cause if r.get("cause_known")]
dash = sum(json.dumps(cat).count(c) for c in "—–")
print(f"matched {matched}, unmatched {unmatched}")
if miss: print("UNMATCHED:", miss[:20])
print(f"rare cancers {len(cancers)}, with causes {len(with_cause)}, "
      f"cause established {len(known)}, cause not established {len(with_cause)-len(known)}")
print("em/en dashes in catalog:", dash)

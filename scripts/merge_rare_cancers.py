import json, re, glob, shutil, sys

CAT = "data/rare_conditions_catalog.json"
shutil.copy2(CAT, CAT + ".bak_before_expand")
cat = json.load(open(CAT))

STOP = {"the","of","a","an","and","type","tumour","tumor","neoplasm"}
def norm(s):
    s = s.lower().strip()
    s = re.sub(r"\([^)]*\)", " ", s)          # drop parentheticals
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    toks = [t for t in s.split() if t and t not in STOP]
    return " ".join(sorted(toks))              # order-insensitive token key

def slugify(s):
    s = re.sub(r"\([^)]*\)", " ", s.lower())
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s[:60]

# --- index existing ---
seen = {}          # norm key -> row
slugs = set()
for r in cat:
    seen[norm(r["name"])] = r
    for a in r.get("aliases", []) or []:
        seen.setdefault(norm(a), r)
    if r.get("slug"):
        slugs.add(r["slug"])

def uniq_slug(base):
    s = base or "condition"; i = 2
    while s in slugs:
        s = f"{base}_{i}"; i += 1
    slugs.add(s); return s

# --- merge families ---
added = 0
enriched_gene = 0
for fp in sorted(glob.glob("tmp/tmp/rarecancers_family_*.json")):
    rows = json.load(open(fp))
    for r in rows:
        name = (r.get("name") or "").strip()
        if not name:
            continue
        k = norm(name)
        if k in seen:
            # merge: fill missing gene/alias on existing, do not duplicate
            ex = seen[k]
            if not ex.get("key_gene_or_marker") and r.get("key_gene_or_marker"):
                ex["key_gene_or_marker"] = r["key_gene_or_marker"]; enriched_gene += 1
            for a in (r.get("aliases") or []):
                if a and a not in (ex.get("aliases") or []) and norm(a) not in seen:
                    ex.setdefault("aliases", []).append(a); seen[norm(a)] = ex
            continue
        row = {
            "name": name,
            "category": "rare cancer",
            "slug": uniq_slug(slugify(name)),
            "aliases": [a for a in (r.get("aliases") or []) if a],
            "key_gene_or_marker": r.get("key_gene_or_marker", "") or "",
        }
        if r.get("source"):
            row["source"] = r["source"]
        cat.append(row); seen[k] = row
        for a in row["aliases"]:
            seen.setdefault(norm(a), row)
        added += 1

json.dump(cat, open(CAT, "w"), indent=2, ensure_ascii=False)

# --- report ---
from collections import Counter
c = Counter(r.get("category") for r in cat)
dupes = [k for k, v in Counter(norm(r["name"]) for r in cat).items() if v > 1]
badslug = [k for k, v in Counter(r["slug"] for r in cat).items() if v > 1]
dash = [ch for ch in json.dumps(cat) if ch in "—–"]
print("total:", len(cat), dict(c))
print("added:", added, "gene_enriched_on_existing:", enriched_gene)
print("dup name-keys:", len(dupes), "dup slugs:", len(badslug), "em/en dashes:", len(dash))
if dupes[:5]: print("sample dup keys:", dupes[:5])

"""Extract expressed druggable targets from single-cell RNA-seq.

The public entry point is :func:`extract_targets`. It loads an AnnData from an
h5ad path (scanpy is imported lazily so the core package imports without it),
runs light quality control, selects tumor cells when a label is available or
otherwise uses all cells, then measures for a curated panel of surface and
actionable targets both the mean expression and the percent of cells expressing
each target. Targets expressed above a percent-expressing threshold are emitted
as :class:`~anveshar.schema.Alteration` records with
``variant_class=VariantClass.EXPRESSION``, each annotated with the therapy
modality that an expressed target nominates (for example a bispecific T cell
engager for DLL3, or radioligand therapy for SSTR2).

Every target and therapy mapping in ``TARGET_PANEL`` is a real, approved or
clinically advanced target to therapy pairing (see per-target notes). Nothing
here fabricates a biological result: the numbers are computed directly from the
supplied AnnData, and a target absent from the data is simply skipped.
"""
from __future__ import annotations

from ..schema import Alteration, VariantClass


# Curated panel of surface / actionable druggable targets.
# Each entry: canonical gene symbol -> (canonical target label, therapy modality
# nominated when the target is expressed). Aliases are checked against var_names
# so a matrix that stores, for example, HER2 or TROP2 still resolves.
TARGET_PANEL: dict[str, dict] = {
    "SSTR2": {
        "target": "SSTR2 (somatostatin receptor 2)",
        "therapy": "somatostatin analog or Lu-177 DOTATATE radioligand therapy",
        "aliases": ["SST2", "SSTR2A"],
    },
    "DLL3": {
        "target": "DLL3 (delta like ligand 3)",
        "therapy": "tarlatamab DLL3 bispecific T cell engager",
        "aliases": [],
    },
    "ERBB2": {
        "target": "ERBB2 / HER2",
        "therapy": "trastuzumab deruxtecan antibody drug conjugate",
        "aliases": ["HER2", "NEU"],
    },
    "MET": {
        "target": "MET",
        "therapy": "MET tyrosine kinase inhibitor or MET antibody drug conjugate",
        "aliases": ["HGFR", "CMET", "C-MET"],
    },
    "EGFR": {
        "target": "EGFR",
        "therapy": "EGFR tyrosine kinase inhibitor or anti EGFR antibody",
        "aliases": ["ERBB1", "HER1"],
    },
    "FGFR1": {
        "target": "FGFR1",
        "therapy": "FGFR tyrosine kinase inhibitor",
        "aliases": ["FLT2", "CD331"],
    },
    "FGFR2": {
        "target": "FGFR2",
        "therapy": "FGFR tyrosine kinase inhibitor",
        "aliases": ["CD332", "KGFR"],
    },
    "FGFR3": {
        "target": "FGFR3",
        "therapy": "FGFR tyrosine kinase inhibitor",
        "aliases": ["CD333"],
    },
    "NTRK1": {
        "target": "NTRK1 (TRKA)",
        "therapy": "TRK inhibitor (larotrectinib or entrectinib)",
        "aliases": ["TRKA"],
    },
    "NTRK2": {
        "target": "NTRK2 (TRKB)",
        "therapy": "TRK inhibitor (larotrectinib or entrectinib)",
        "aliases": ["TRKB"],
    },
    "NTRK3": {
        "target": "NTRK3 (TRKC)",
        "therapy": "TRK inhibitor (larotrectinib or entrectinib)",
        "aliases": ["TRKC"],
    },
    "CEACAM5": {
        "target": "CEACAM5 (CEA)",
        "therapy": "anti CEACAM5 antibody drug conjugate (tusamitamab ravtansine)",
        "aliases": ["CEA", "CD66E"],
    },
    "TACSTD2": {
        "target": "TACSTD2 / TROP2",
        "therapy": "sacituzumab govitecan antibody drug conjugate",
        "aliases": ["TROP2", "GA733-1", "M1S1"],
    },
    "MSLN": {
        "target": "MSLN (mesothelin)",
        "therapy": "anti mesothelin antibody drug conjugate or CAR T cell therapy",
        "aliases": ["MPF"],
    },
    "CD276": {
        "target": "CD276 / B7-H3",
        "therapy": "anti B7-H3 antibody drug conjugate",
        "aliases": ["B7H3", "B7-H3"],
    },
    "PDCD1": {
        "target": "PDCD1 / PD-1",
        "therapy": "PD-1 immune checkpoint inhibitor",
        "aliases": ["PD1", "PD-1"],
    },
    "CD274": {
        "target": "CD274 / PD-L1",
        "therapy": "PD-L1 immune checkpoint inhibitor",
        "aliases": ["PDL1", "PD-L1", "B7H1"],
    },
}

# Default percent-expressing threshold (percent of selected cells with count > 0)
# above which a target is reported as an actionable expression finding.
PCT_THRESHOLD = 10.0


def _resolve_var_name(symbol: str, aliases: list[str], var_names) -> str | None:
    """Return the actual var_names entry for a gene symbol or one of its aliases.

    Matching is case insensitive and tolerant of the common canonical spelling,
    so a matrix that stores HER2, TROP2, or lowercased symbols still resolves to
    the intended target. Returns None when neither the symbol nor any alias is
    present, so the caller can skip the target gracefully.
    """
    lookup = {}
    for name in var_names:
        lookup.setdefault(str(name).upper(), str(name))
    for candidate in [symbol] + list(aliases):
        hit = lookup.get(candidate.upper())
        if hit is not None:
            return hit
    return None


def _looks_raw(matrix) -> bool:
    """Heuristic: True if the matrix looks like raw (unnormalized integer) counts.

    Data are treated as raw when the maximum value is a moderately large integer
    (as counts are), so normalize_total + log1p should be applied. Already
    normalized or log transformed data (fractional or small maxima) are left as
    is. Errs toward leaving the data untouched if the maximum cannot be read.
    """
    try:
        mx = matrix.max()
        mx = float(mx.toarray()[0, 0]) if hasattr(mx, "toarray") else float(mx)
    except Exception:
        return False
    return mx > 20.0 and abs(mx - round(mx)) < 1e-6


def extract_targets(h5ad_path: str, tumor_label: str | None = None) -> list[Alteration]:
    """Read expressed druggable targets from a single-cell RNA-seq h5ad.

    Parameters
    ----------
    h5ad_path
        Path to an AnnData ``.h5ad`` file. scanpy and anndata are imported
        lazily inside this function so the core package imports without them.
    tumor_label
        Optional value identifying tumor cells. If given, the function looks for
        an ``.obs`` column whose values include ``tumor_label`` (checked against
        a small set of common annotation columns and, failing that, every obs
        column) and restricts the read out to those cells. If it is None, or no
        matching column is found, all cells are used.

    Returns
    -------
    list[Alteration]
        One :class:`~anveshar.schema.Alteration` per target in ``TARGET_PANEL``
        that is present in ``var_names`` and expressed in more than
        ``PCT_THRESHOLD`` percent of the selected cells, with
        ``variant_class=VariantClass.EXPRESSION``, a ``biomarker`` string of the
        form ``"expressed in N percent of tumor cells"``, the canonical
        ``target`` label, and an ``interpretation`` naming the nominated therapy
        modality. The list is sorted by percent expressing, highest first.
    """
    import numpy as np
    import scanpy as sc  # lazy import: keeps the core package free of this dep

    adata = sc.read_h5ad(h5ad_path)

    # Light QC: drop near-empty cells and genes so percentages are meaningful.
    try:
        sc.pp.filter_cells(adata, min_genes=1)
        sc.pp.filter_genes(adata, min_cells=1)
    except Exception:
        pass

    # Normalize only if the data still look like raw counts.
    if _looks_raw(adata.X):
        sc.pp.normalize_total(adata, target_sum=1e4)
        sc.pp.log1p(adata)

    # Select tumor cells when a label and a matching obs column are available.
    cell_mask = np.ones(adata.n_obs, dtype=bool)
    scope = "cells"
    if tumor_label is not None:
        preferred = ["celltype", "cell_type", "celltype_manual", "annotation",
                     "Annotation", "cell_label", "leiden", "cluster"]
        cols = [c for c in preferred if c in adata.obs.columns]
        cols += [c for c in adata.obs.columns if c not in cols]
        for col in cols:
            values = adata.obs[col].astype(str)
            hit = values == str(tumor_label)
            if hit.any():
                cell_mask = hit.to_numpy()
                scope = "tumor cells"
                break

    n_sel = int(cell_mask.sum())
    if n_sel == 0:
        return []

    X = adata.X
    X = X[cell_mask]
    var_names = list(adata.var_names)

    results: list[tuple[float, float, str, dict]] = []
    for symbol, meta in TARGET_PANEL.items():
        name = _resolve_var_name(symbol, meta.get("aliases", []), var_names)
        if name is None:
            continue  # target not on this panel / matrix, skip gracefully
        col = X[:, var_names.index(name)]
        arr = col.toarray().ravel() if hasattr(col, "toarray") else np.asarray(col).ravel()
        pct = 100.0 * float((arr > 0).sum()) / float(n_sel)
        mean_expr = float(arr.mean())
        results.append((pct, mean_expr, symbol, meta))

    results.sort(key=lambda r: r[0], reverse=True)

    alterations: list[Alteration] = []
    for pct, mean_expr, symbol, meta in results:
        if pct <= PCT_THRESHOLD:
            continue
        pct_int = int(round(pct))
        alterations.append(
            Alteration(
                gene=symbol,
                variant_class=VariantClass.EXPRESSION,
                biomarker=f"expressed in {pct_int} percent of {scope}",
                target=meta["target"],
                interpretation=(
                    f"expression nominates {meta['therapy']} "
                    f"(mean expression {mean_expr:.2f} in {n_sel} {scope})"
                ),
            )
        )
    return alterations

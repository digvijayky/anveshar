"""Offline unit test for anveshar.expression.scrna.extract_targets.

The AnnData built here is a UNIT-TEST FIXTURE only: 50 synthetic cells by 6
genes with arbitrary counts, constructed purely to exercise the code path. It
is NOT scientific data and carries no biological meaning. The test is skipped
when scanpy is not installed (extract_targets imports scanpy lazily).
"""
import pytest


def _build_fixture():
    """Build a tiny in-memory AnnData fixture (not scientific data).

    50 cells by 6 genes including DLL3 and SSTR2, with DLL3 expressed in every
    cell (high counts) and SSTR2 expressed in about half, so extract_targets
    must surface DLL3 as an expressed EXPRESSION target.
    """
    import numpy as np
    import anndata as ad
    import pandas as pd

    rng = np.random.default_rng(0)
    genes = ["DLL3", "SSTR2", "ACTB", "GAPDH", "MET", "EGFR"]
    n = 50
    X = np.zeros((n, len(genes)), dtype=float)
    X[:, 0] = rng.integers(30, 60, size=n)          # DLL3 high in all cells
    X[:, 1] = np.where(rng.random(n) < 0.5,
                       rng.integers(10, 40, size=n), 0)  # SSTR2 in ~half
    X[:, 2] = rng.integers(50, 100, size=n)         # housekeeping
    X[:, 3] = rng.integers(50, 100, size=n)         # housekeeping
    X[:, 4] = 0                                     # MET silent
    X[:, 5] = 0                                     # EGFR silent

    obs = pd.DataFrame(
        {"celltype": ["tumor"] * 40 + ["stroma"] * 10},
        index=[f"cell{i}" for i in range(n)],
    )
    var = pd.DataFrame(index=genes)
    return ad.AnnData(X=X, obs=obs, var=var)


def test_extract_targets_reports_dll3(tmp_path):
    pytest.importorskip("scanpy")
    from anveshar.expression import extract_targets
    from anveshar.schema import VariantClass

    adata = _build_fixture()
    path = tmp_path / "fixture.h5ad"
    adata.write_h5ad(path)

    alts = extract_targets(str(path))

    genes = [a.gene for a in alts]
    assert "DLL3" in genes, "DLL3 should be returned as an expressed target"

    dll3 = next(a for a in alts if a.gene == "DLL3")
    assert dll3.variant_class is VariantClass.EXPRESSION
    assert "percent" in dll3.biomarker
    assert "bispecific" in dll3.interpretation.lower()
    assert dll3.target  # canonical target label populated

    # Silent genes must never be reported.
    assert "MET" not in genes and "EGFR" not in genes

    # Result must be sorted by percent expressing, highest first.
    def pct(a):
        return int([t for t in a.biomarker.split() if t.isdigit()][0])
    pcts = [pct(a) for a in alts]
    assert pcts == sorted(pcts, reverse=True)


def test_tumor_label_scopes_to_tumor_cells(tmp_path):
    pytest.importorskip("scanpy")
    from anveshar.expression import extract_targets

    adata = _build_fixture()
    path = tmp_path / "fixture2.h5ad"
    adata.write_h5ad(path)

    alts = extract_targets(str(path), tumor_label="tumor")
    dll3 = next(a for a in alts if a.gene == "DLL3")
    assert "tumor cells" in dll3.biomarker

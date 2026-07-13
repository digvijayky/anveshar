"""Anveshar single-cell expression module.

Reads out druggable surface and actionable targets from single-cell RNA-seq
(AnnData / h5ad) as ``Alteration`` records with ``VariantClass.EXPRESSION``,
so that an expressed target (for example DLL3 or SSTR2) can nominate the same
therapy modalities (bispecific, radioligand, antibody drug conjugate) that are
validated against that target in other conditions.

scanpy and anndata are imported lazily inside the functions, so importing this
module (and the core package) never requires them to be installed.
"""
from .scrna import extract_targets, TARGET_PANEL

__all__ = ["extract_targets", "TARGET_PANEL"]

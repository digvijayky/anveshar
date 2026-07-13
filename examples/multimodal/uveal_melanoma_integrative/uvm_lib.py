"""Pure, testable helpers extracted from uvm_integrative.py so the metastatic risk
class label cannot be assigned by an arbitrary tie-break. No network, no side effects."""
import numpy as np


def high_risk_class(cls, mono3):
    """Return the cluster label in CLS most enriched for monosomy 3 (membership in
    MONO3). Raises ValueError if MONO3 is empty or the clusters are equally enriched,
    so the high-risk class is never guessed when the data cannot decide it."""
    if len(mono3) == 0:
        raise ValueError("monosomy-3 set is empty; high-risk class is undecidable")
    labels = list(dict.fromkeys(list(cls)))
    frac = {c: float(np.mean([s in mono3 for s in cls.index[cls == c]])) for c in labels}
    values = list(frac.values())
    top = max(values)
    if values.count(top) > 1:
        raise ValueError("clusters equally enriched for monosomy 3; high-risk class ambiguous")
    return max(frac, key=frac.get)

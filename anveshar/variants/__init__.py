"""anveshar.variants: variant interpretation and actionability grading.

Public surface (see docs/interfaces.md, anveshar.variants):
  classify(raw)                          -> VariantClass
  grade(gene, variant, biomarker, cond)  -> Actionability
  reclassify(alt, client=None)           -> Alteration   (VUS in silico triage)
  interpret_profile(raw)                 -> PatientProfile (the entry point)

Every grade is anchored to a real, cited rule in anveshar.variants._knowledge; no
alteration, drug, or citation is fabricated, and unknown queries return empty rather
than a guess.
"""
from __future__ import annotations
from .classes import classify
from .actionability import grade
from .vus import reclassify
from .interpret import interpret_profile

__all__ = ["classify", "grade", "reclassify", "interpret_profile"]

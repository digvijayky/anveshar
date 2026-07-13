"""Anveshar translation engine and novelty discovery layer.

Two responsibilities live here:

  1. Cross-condition translation: map a condition's molecular targets to
     therapies validated elsewhere, tiered and cited, using the tissue-agnostic
     approval table plus a small curated same-target-other-tumor map
     (:mod:`tissue_agnostic`, :mod:`translate`).

  2. The novelty layer: generate novel, testable cross-condition and advanced
     modality hypotheses over shared molecular dependencies
     (:mod:`discovery`).

Public surface: ``PRECEDENTS``, ``for_biomarker``, ``translate_targets``,
``match``, ``generate``.
"""
from .tissue_agnostic import PRECEDENTS, for_biomarker
from .translate import translate_targets, match
from .discovery import generate

__all__ = [
    "PRECEDENTS",
    "for_biomarker",
    "translate_targets",
    "match",
    "generate",
]

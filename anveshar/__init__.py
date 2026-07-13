"""Anveshar: a translational molecular board for rare cancers and rare diseases.

Anveshar matches a rare condition, and optionally a patient's own molecular profile,
to therapies validated in OTHER conditions that share the same molecular dependency.
It grades every match by published actionability frameworks, and it generates novel,
testable cross-condition hypotheses (including gene therapy and other advanced
modalities) that no dedicated trial has yet tested in the target condition.
"""
__version__ = "0.1.0"

from .schema import (
    Tier, VariantClass, Modality, Citation, Actionability, Alteration,
    PatientProfile, Target, Therapy, DiscoveryHypothesis, Trial, Precedent,
    DiseaseReport, assert_no_dashes,
)

__all__ = [
    "Tier", "VariantClass", "Modality", "Citation", "Actionability", "Alteration",
    "PatientProfile", "Target", "Therapy", "DiscoveryHypothesis", "Trial", "Precedent",
    "DiseaseReport", "assert_no_dashes", "__version__",
]

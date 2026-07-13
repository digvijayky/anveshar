"""Anveshar canonical schema (the contract every module builds against).

Anveshar matches a rare cancer, and optionally a patient's own molecular profile,
to therapies validated in OTHER conditions that share the same molecular dependency,
graded by evidence, and it generates novel testable cross-condition hypotheses.

Everything here is plain-stdlib dataclasses so any module can import it with no
third-party dependency. Rendering to the HTML report is via to_render_dict().
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Tier(str, Enum):
    """Evidence strength of a therapy match."""
    T1 = "1"          # FDA tissue-agnostic approval, applies if biomarker present
    T2 = "2"          # approved in another tumor with the same target, or basket signal here
    T3 = "3"          # mechanistic / preclinical rationale only
    DISCOVERY = "0"   # novel, computationally generated hypothesis, not yet tried here


class VariantClass(str, Enum):
    SNV = "SNV"
    INDEL = "indel"
    FUSION = "fusion"
    AMPLIFICATION = "amplification"
    DELETION = "deletion"
    CNV = "cnv"
    SPLICE = "splice"
    EPIGENETIC = "epigenetic"
    SIGNATURE = "signature"
    COMPOSITE = "composite biomarker"
    EXPRESSION = "expression"
    GERMLINE = "germline"
    VUS = "vus"


class Modality(str, Enum):
    SMALL_MOLECULE = "small molecule"
    ANTIBODY = "antibody"
    ADC = "antibody drug conjugate"
    BISPECIFIC = "bispecific T cell engager"
    CELL_THERAPY = "cell therapy"
    GENE_THERAPY = "gene therapy"
    ASO = "antisense oligonucleotide"
    RADIOLIGAND = "radioligand therapy"
    CHEMO = "cytotoxic chemotherapy"
    IMMUNE_CHECKPOINT = "immune checkpoint inhibitor"
    OTHER = "other"


# Actionability frameworks Anveshar grades against (see docs/variant_interpretation_methodology.md).
FRAMEWORKS = ("OncoKB", "AMP/ASCO/CAP", "ESCAT")


@dataclass
class Citation:
    label: str = ""
    url: str = ""          # real https link (PubMed / ClinicalTrials / DOI / ClinVar / FDA)


@dataclass
class Actionability:
    oncokb_level: str = ""     # e.g. "Level 1"
    amp_asco_cap: str = ""     # Tier I..IV
    escat: str = ""            # I-A .. X
    note: str = ""

    def summary(self) -> str:
        parts = []
        if self.oncokb_level: parts.append(f"OncoKB {self.oncokb_level}")
        if self.amp_asco_cap: parts.append(f"AMP/ASCO/CAP {self.amp_asco_cap}")
        if self.escat: parts.append(f"ESCAT {self.escat}")
        return "; ".join(parts)


@dataclass
class Alteration:
    """One molecular finding in a patient profile (any variant class)."""
    gene: str
    variant_class: VariantClass = VariantClass.SNV
    variant: str = ""
    consequence: str = ""
    biomarker: str = ""
    actionability: Actionability = field(default_factory=Actionability)
    pathogenicity: str = ""          # e.g. "ClinVar VCV000013961: Oncogenic, Tier I (Strong)"
    pathogenicity_url: str = ""
    target: str = ""                 # canonical target key used for therapy matching
    interpretation: str = ""
    verified: bool = True            # False => flagged UNVERIFIED / illustrative


@dataclass
class PatientProfile:
    present: bool = True
    source: Citation = field(default_factory=Citation)
    tumor_summary: str = ""
    alterations: list[Alteration] = field(default_factory=list)
    excluded: list[dict] = field(default_factory=list)   # [{target, reason}]
    summary: dict = field(default_factory=dict)           # {patient, clinician, researcher}


@dataclass
class Target:
    name: str
    present_in: str = ""
    evidence: str = ""


@dataclass
class Therapy:
    drug: str
    target: str
    tier: Tier = Tier.T3
    modality: Modality = Modality.SMALL_MOLECULE
    approved_in: str = ""
    dev_stage: str = ""
    rationale: dict = field(default_factory=dict)     # {patient, clinician, researcher}
    citation: Citation = field(default_factory=Citation)
    trial: Optional[dict] = None                      # {nct, url}


@dataclass
class DiscoveryHypothesis:
    """A novel, computationally generated cross-condition hypothesis (the novelty layer).

    Anveshar proposes a therapy or modality that has NOT been tried in the target
    condition, by analogy over a shared molecular dependency, and grades the
    transferability of the analogy. Always a research hypothesis, never a clinical claim.
    """
    hypothesis: str
    shared_dependency: str            # the molecular link that licenses the analogy
    source_condition: str             # where the therapy is validated
    proposed_modality: Modality = Modality.SMALL_MOLECULE
    rationale: str = ""
    transferability: str = ""         # high / medium / speculative + why
    supporting_citation: Citation = field(default_factory=Citation)
    testable_prediction: str = ""     # how a lab could falsify it


@dataclass
class Trial:
    nct: str
    title: str = ""
    phase: str = ""
    intervention: str = ""
    eligibility: str = ""
    url: str = ""


@dataclass
class Precedent:
    biomarker: str
    drug: str
    year: str = ""
    citation: Citation = field(default_factory=Citation)


@dataclass
class DiseaseReport:
    """The full Anveshar report for one condition, optionally personalized."""
    name: str
    sub: str = ""
    chips: list[str] = field(default_factory=list)
    overview: dict = field(default_factory=dict)
    targets_intro: dict = field(default_factory=dict)
    targets: list[Target] = field(default_factory=list)
    therapies_intro: dict = field(default_factory=dict)
    therapies: list[Therapy] = field(default_factory=list)
    trials: list[Trial] = field(default_factory=list)
    precedent_intro: dict = field(default_factory=dict)
    precedents: list[Precedent] = field(default_factory=list)
    discovery_intro: dict = field(default_factory=dict)
    discovery: list[DiscoveryHypothesis] = field(default_factory=list)
    patient: Optional[PatientProfile] = None
    disclaimer: str = ""

    def to_render_dict(self) -> dict:
        """Map the rich model to the flat DATA dict the HTML template consumes."""
        def cite(c): return {"label": c.label, "url": c.url}
        def th(t):
            d = {"drug": t.drug, "target": t.target, "tier": int(t.tier.value),
                 "modality": t.modality.value, "approved_in": t.approved_in,
                 "dev_stage": t.dev_stage, "rationale": t.rationale, "citation": cite(t.citation)}
            if t.trial: d["trial"] = t.trial
            return d
        def alt(a):
            return {"gene": a.gene, "cls": a.variant_class.value, "variant": a.variant,
                    "actionability": a.actionability.summary() or a.actionability.note,
                    "pathogenicity": a.pathogenicity, "pathoUrl": a.pathogenicity_url,
                    "target": a.target, "note": a.interpretation}
        def disc(h):
            return {"hypothesis": h.hypothesis, "shared": h.shared_dependency,
                    "source": h.source_condition, "modality": h.proposed_modality.value,
                    "rationale": h.rationale, "transferability": h.transferability,
                    "prediction": h.testable_prediction, "citation": cite(h.supporting_citation)}
        out = {
            "cancer": {"name": self.name, "sub": self.sub, "chips": self.chips},
            "overview": self.overview, "targetsIntro": self.targets_intro,
            "targets": [{"name": t.name, "present_in": t.present_in, "evidence": t.evidence} for t in self.targets],
            "therapiesIntro": self.therapies_intro, "therapies": [th(t) for t in self.therapies],
            "trials": [asdict(t) for t in self.trials],
            "precedentIntro": self.precedent_intro,
            "precedents": [{"biomarker": p.biomarker, "drug": p.drug, "year": p.year, "citation": cite(p.citation)} for p in self.precedents],
            "discoveryIntro": self.discovery_intro, "discovery": [disc(h) for h in self.discovery],
            "disclaimer": self.disclaimer,
        }
        if self.patient and self.patient.present:
            out["patient"] = {
                "present": True, "source": cite(self.patient.source),
                "tumor": {"summary": self.patient.tumor_summary},
                "summary": self.patient.summary,
                "alterations": [alt(a) for a in self.patient.alterations],
                "excluded": self.patient.excluded,
            }
        return out


NO_DASH = ("—", "–")   # em, en dash: forbidden anywhere in Anveshar output


def assert_no_dashes(obj) -> None:
    """Anveshar never emits em/en dashes. Raise if any string in obj contains one."""
    import json
    s = json.dumps(obj, default=lambda o: getattr(o, "__dict__", str(o)), ensure_ascii=False)
    bad = [d for d in NO_DASH if d in s]
    if bad:
        raise ValueError(f"forbidden dash(es) {bad!r} found in output")

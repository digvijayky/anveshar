"""Generate a bespoke, runnable computational biology workflow for a rare cancer.

Each workflow is a staged plan a scientist can execute on Claude Science. Every stage names the
concrete database, tool, skill, or code to run, the command, the expected output, and a
falsifiable checkpoint, and states how the stage moves confidence. Stages are tailored to the
driver class (fusion, activating mutation, loss of function, amplification, epigenetic) and to
whether a borrowable approved therapy exists, so no two conditions get the same workflow.

The public entry point ``generate(resolved, translation)`` returns a dict in the shape the
report template's ``workflow`` field expects (aim, hypothesis, steps, datasets, validation,
figures) plus a richer ``harness`` list for the pipeline JSON. Research use, not medical advice.
"""
from __future__ import annotations
import re


def driver_class(marker: str) -> str:
    """Classify the molecular driver from its marker string."""
    m = (marker or "").lower()
    if re.search(r"fusion|::|-rearrang|rearrangement|translocation|t\(\d", m):
        return "fusion"
    if re.search(r"loss|deficient|inactivat|deletion|biallelic|truncat", m) or \
       re.search(r"swi/snf|smarc|pbrm|arid|prc2|methylation|epigenetic", m):
        return "loss_or_epigenetic"
    if re.search(r"amplif|amplification|copy number gain", m):
        return "amplification"
    if re.search(r"mutation|mutant|v600|g12|g13|q61|d842|r132|d816|activating|hotspot|[a-z]\d{2,4}[a-z]", m):
        return "activating_mutation"
    return "unknown"


_VALIDATION_STAGE = {
    "fusion": ("Confirm and functionally validate the fusion",
               "Verify the driver fusion by RNA sequencing fusion calling (Arriba or STAR-Fusion) and break apart FISH, then test dependency by fusion directed knockdown or a CRISPR screen readout.",
               "RNA-seq (Arriba, STAR-Fusion), DepMap CRISPR essentiality, Open Targets target profile",
               "The fusion is present and its partners are co-expressed; knockdown reduces viability more than in fusion negative controls."),
    "loss_or_epigenetic": ("Confirm the loss and map the induced dependency",
               "Confirm biallelic loss by immunohistochemistry and copy number, then identify the synthetic lethal or epigenetic dependency created by the loss using DepMap co-dependency and a chromatin state readout.",
               "DepMap co-dependency, Open Targets tractability, CRISPR or ATAC readout",
               "Protein loss is confirmed and a selective dependency (for example an EZH2 or paralog dependency) emerges that is absent in wild type lines."),
    "activating_mutation": ("Confirm the activating alteration and its signaling output",
               "Confirm the specific variant by targeted sequencing, classify it (OncoKB and AMP tiers; AlphaMissense or Evo 2 for a variant of uncertain significance), and measure downstream pathway activation.",
               "OncoKB, AlphaMissense, Evo 2, phospho signaling assay, Open Targets",
               "The exact activating allele is present and drives measurable pathway output; the allele matches the label of the candidate drug."),
    "amplification": ("Confirm amplification and dose dependence",
               "Confirm the amplification by copy number (and FISH where relevant) and test whether viability tracks with copy number and target protein dose.",
               "cBioPortal copy number, DepMap, Open Targets",
               "Amplification and protein overexpression are confirmed and viability depends on the amplified target."),
    "unknown": ("Define the driver dependency",
               "Because no single defining driver is catalogued, run an unbiased dependency map (DepMap CRISPR) and expression profiling to nominate the actionable dependency before targeting.",
               "DepMap CRISPR, GEO or TCGA expression, Open Targets",
               "A reproducible selective dependency is nominated and confirmed in at least two independent models."),
}


def _drug_stage(translation):
    act = translation.get("actionable") or []
    if act:
        m = min(act, key=lambda x: x["tier"])
        return ("Test the borrowable therapy and its mechanism",
                f"Confirm target engagement of {m['drug']} (approved in {m['approved_in']}) against this driver: "
                f"pull ChEMBL bioactivity for the compound versus the target, verify the mechanism, and run a "
                f"dose response in patient derived or established models. Note the variant caveat where present.",
                "ChEMBL bioactivity, UniProt, dose response assay, PubMed",
                f"{m['drug']} inhibits the target at achievable concentrations and reduces viability; the specific "
                f"variant is sensitive (not a documented resistance allele).", m)
    return ("Nominate a mechanistic candidate and test it",
            "With no approved borrowable therapy, use Open Targets tractability and ChEMBL to nominate the most "
            "tractable candidate against the dependency, then test it in models.",
            "Open Targets tractability, ChEMBL, dose response assay",
            "A tractable candidate reduces viability selectively in driver positive models.", None)


def generate(resolved: dict, translation: dict) -> dict:
    """Build a bespoke comp-bio workflow for a resolved condition and its translation result."""
    name = resolved["name"]
    genes = resolved.get("genes") or []
    gene = genes[0] if genes else "the driver"
    cls = driver_class(resolved.get("marker", ""))
    vt, vw, vtool, vcheck = _VALIDATION_STAGE[cls]
    induced = resolved.get("induced") or {}
    if cls == "loss_or_epigenetic" and induced:
        e = next(iter(induced.values()))
        dep = e["dependency"]
        vt = f"Confirm the loss and target the induced {dep} dependency"
        vw = (f"{gene} is a tumor suppressor and cannot be drugged directly. Confirm biallelic loss by "
              f"immunohistochemistry and copy number, then validate the induced synthetic lethal dependency "
              f"on {dep} ({e['relationship']}) by DepMap co-dependency and knockdown, since {dep} is the "
              f"druggable node ({e['drug']}).")
        vtool = f"DepMap co-dependency, Open Targets tractability of {dep}, CRISPR knockdown"
        vcheck = (f"{gene} loss is confirmed and cells depend on {dep}; {dep} tractability supports drugging it "
                  f"where {gene} itself is a common essential gene that cannot be targeted selectively.")
    dt, dw, dtool, dcheck, best = _drug_stage(translation)
    cross = translation.get("cross_condition") or {}
    n_cross = sum(len(v) for v in cross.values())

    aim = (f"Establish {gene} as a therapeutic dependency in {name} and test whether a therapy "
           f"validated against {gene} elsewhere translates here.")
    if best:
        hypo = (f"{name} depends on its {cls.replace('_', ' ')} driver {gene}, so {best['drug']} "
                f"(approved in {best['approved_in']}) is a testable cross condition candidate.")
    else:
        hypo = (f"{name} depends on {gene}; the most tractable agent against this dependency is a "
                f"testable candidate, since no approved therapy targets it yet.")

    steps = [
        {"title": vt, "what": vw, "tools": vtool,
         "outputs": "validated driver and a selective dependency; " + vcheck},
        {"title": "Map the cross condition evidence",
         "what": (f"Retrieve every prior use of the candidate mechanism against {gene} across the "
                  f"{n_cross} rare cancers that share this dependency, using systematic literature and "
                  f"trial retrieval, and grade transferability."),
         "tools": "PubMed, Consensus, Paperclip full text, ClinicalTrials.gov; deep-research skill",
         "outputs": "a graded evidence table of prior responses and resistance, with citations"},
        {"title": "Interpret the patient's specific alteration",
         "what": ("Classify the exact alteration for actionability (OncoKB, AMP and ESCAT tiers) and, "
                  "for a variant of uncertain significance, add a computational pathogenicity call."),
         "tools": "OncoKB, ClinVar, AlphaMissense, Evo 2; anveshar.variants",
         "outputs": "an actionability tier and a defensible call for any uncertain variant"},
        {"title": "Profile expression and the microenvironment",
         "what": (f"Quantify {gene} and the candidate target in this tumor from public expression "
                  f"(GEO, TCGA, cBioPortal) and, where single cell or spatial data exist, resolve which "
                  f"cell compartment expresses the target."),
         "tools": "GEO, TCGA, cBioPortal, scanpy; single-cell-rna-qc and scvi-tools skills",
         "outputs": "target expression, cell of origin, and microenvironment context"},
        {"title": dt, "what": dw, "tools": dtool, "outputs": dcheck},
        {"title": "Design the confirmatory trial",
         "what": ("Turn the validated hypothesis into a biomarker selected basket or phase 1b/2 "
                  "protocol synopsis with endpoints, eligibility, and correlatives."),
         "tools": "clinical-trial-protocol skill; ClinicalTrials.gov comparators",
         "outputs": "a protocol synopsis ready for expert and biostatistician review"},
        {"title": "Score, cite, and assemble the dossier",
         "what": ("Run the Anveshar harness to attach a transparent confidence score to each therapy, "
                  "collect the full provenance, and emit the cited dossier with a health provider disclaimer."),
         "tools": "anveshar.pipeline harness; anveshar.score",
         "outputs": "a reproducible, cited, confidence scored dossier with an auditable run manifest"},
    ]

    datasets = [
        {"name": "Open Targets Platform", "source": "target to disease and tractability", "url": "https://platform.opentargets.org"},
        {"name": "DepMap", "source": "CRISPR gene essentiality", "url": "https://depmap.org"},
        {"name": "cBioPortal", "source": "somatic alterations across cancers", "url": "https://www.cbioportal.org"},
        {"name": "ChEMBL", "source": "compound bioactivity", "url": "https://www.ebi.ac.uk/chembl"},
        {"name": "GEO", "source": "public expression datasets", "url": "https://www.ncbi.nlm.nih.gov/geo"},
    ]
    harness = [{"stage": s["title"], "runs": s["tools"], "checkpoint": s["outputs"]} for s in steps]
    return {
        "aim": aim, "hypothesis": hypo, "driver_class": cls, "steps": steps,
        "datasets": datasets,
        "validation": ("Each stage has a falsifiable checkpoint; the hypothesis is retained only if the "
                       "driver dependency, the target engagement, and the variant sensitivity all hold."),
        "figures": (f"A confidence scored translation dossier for {name} with a {gene} dependency map, "
                    f"target engagement dose response, and a biomarker selected trial synopsis."),
        "harness": harness,
        "how_to_run": f'python3 -m anveshar.cli analyze --cancer "{name}" --live',
    }

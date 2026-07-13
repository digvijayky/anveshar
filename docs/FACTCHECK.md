# Anveshar fact-check report

An independent, adversarial verification pass over everything Anveshar asserts, to confirm
nothing is fabricated. Per-batch details are in `docs/factcheck/batch1.md` to `batch5.md`
and `docs/factcheck/catalog.md`.

## Method

Six independent subagents were instructed to distrust the reports and re-resolve every
identifier from primary sources: each PMID via the PubMed plugin (title, journal, year, and
whether the requested PMID returns the article the claim implies), each NCT via the
ClinicalTrials.gov API, each DOI via resolution, and each regulatory or efficacy claim
against the source abstract or an authoritative registry. They were told to flag anything
UNRESOLVED, MISMATCH, OVERSTATED, or FABRICATED, and not to edit anything. A seventh check
re-counted the quantitative claims made to the user.

## Scope

25 distinct condition reports, roughly 380 citations (179 unique PMIDs, plus NCTs and DOIs),
and the 384-entry rare conditions catalog.

## Result

The integrity is high. Across all 25 reports the adversarial pass found exactly one real
error, now fixed, and no fabrications and no materially overstated efficacy.

| Batch | Reports | Verdict |
|---|---|---|
| 1 | rectal NET, renal medullary carcinoma, chordoma, adenoid cystic carcinoma, alveolar soft part sarcoma | 4 clean, 1 fixed (see below) |
| 2 | ATRT, Ewing, uveal melanoma, NUT, cholangiocarcinoma | all pass |
| 3 | GIST, pheochromocytoma and paraganglioma, medullary thyroid, Merkel, DFSP | all clean |
| 4 | SMA, Duchenne, cystic fibrosis, sickle cell, RPE65 | all verified |
| 5 | hereditary ATTR, Gaucher, Huntington, Fabry, Pompe | all verified |
| catalog | 384 conditions | clean |

## The one real error, fixed

The adenoid cystic carcinoma lenvatinib card carried trial NCT02780025, which does not exist
on ClinicalTrials.gov. The correct Tchekmedyian phase 2 lenvatinib ACC trial is NCT02780310.
Corrected. The efficacy citation for that card (PMID 30939095) was already correct.

## Catalog

All 384 conditions are real, correctly spelled, with no duplicates and no wrong gene
assignments. One garbled name was tidied: "Basal cell carcinoma nevoid syndrome tumor" now
reads "Nevoid basal cell carcinoma syndrome (Gorlin syndrome)".

## Surprising facts that were suspected and confirmed real

The verifiers deliberately tried to break the most unusual claims, and each held up against a
primary source: tazemetostat was withdrawn from all markets and its dedicated renal medullary
carcinoma cohort was 0 of 14 (Gounder, Nat Commun 2026, PMID 41882006); nivolumab plus
ipilimumab induces hyperprogression in renal medullary carcinoma (PMID 41290625); atezolizumab
is the first approval specific to alveolar soft part sarcoma; tebentafusp is the first therapy
to improve survival in uveal melanoma; voretigene neparvovec is the first FDA gene therapy for
a genetic disease; exagamglogene autotemcel is the first CRISPR therapy; voxelotor was
withdrawn worldwide in 2024; and tominersen failed in Huntington disease.

## Cosmetic notes (not errors)

A number of citations carry a print year where the epub year differs by one, or attach a
pivotal-era or class-evidence paper rather than the drug's own registration paper (always
disclosed in the report text), or, in one ATRT case, cite a B7-H3 CAR T trial arm conducted in
other pediatric CNS tumors. None inflate a claim.

## Corrections to the quantitative claims made during development

Confirmed accurate: 93 passing tests; 14 commits at the time of the check.
Corrected: the compiled catalog holds 384 conditions (the hosted site shows 388 because the
site builder adds a few report-only conditions absent from the compiler's list); there are 25
distinct condition reports (earlier phrasing of "29 with reports" counted the rectal NET
variants and catalog alias matches, not 29 separate conditions).

## Verdict

No fabricated citations, drugs, trials, or conditions were found. One wrong trial number and
one garbled catalog name were corrected. Anveshar is decision support for research use, not
medical advice.

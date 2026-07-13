# What is candidate about Anveshar

Anveshar is a hypothesis layer over retrieval. A lookup table answers "what is already approved for this alteration in this tumor type." Anveshar answers a harder question that no curated table contains: "given the molecular dependency this cancer runs on, what therapy validated somewhere else should work here, even though nobody has tried it in this disease, and what is the one experiment that would confirm or kill that idea?" The output is a ranked set of novel, falsifiable, cited hypotheses, held separate from the approved options and clearly labeled as research directions.

This matters because the patients who need cross-condition reasoning most are the ones the evidence base serves least. Rare cancers rarely get their own dedicated trials, so a per-disease lookup returns almost nothing. The engine exists to fill that vacuum with structured, testable leads rather than an empty result.

## The reasoning chain

Every discovery hypothesis Anveshar surfaces is built from the same three step abstraction, encoded in the `DiscoveryHypothesis` schema (`shared_dependency`, `source_condition`, `proposed_modality`, `rationale`, `transferability`, `supporting_citation`, `testable_prediction`).

1. **Shared molecular dependency.** Identify a lesion or dependency in the target cancer (a lost tumor suppressor, a synthetic lethal partner deletion, a lineage surface antigen, a splice event) and find another condition that runs on the same dependency.
2. **Therapeutic analogy.** Borrow the therapy that is validated against that dependency in the source condition, and state the modality it uses (small molecule, bispecific, cell therapy, radioligand, antisense oligonucleotide, gene directed).
3. **Falsifiable prediction.** Convert the analogy into an experiment a lab could run to confirm or refute it, and grade how well the analogy should transfer (high, medium, or speculative, with the reason).

The discovery tier is assigned `Tier.DISCOVERY` ("0") and rendered in a section that is visually and semantically distinct from the approved and trial backed tiers (T1 to T3). Anveshar never lets a computationally generated analogy masquerade as clinical evidence.

## Cite or abstain

The discovery layer is bounded by the same discipline as the rest of the engine. Every analogy carries a real citation for the biology that licenses it (a PMID or DOI). Where the analogy has been formally tested in the target cancer and failed, Anveshar says so and down grades the transferability rather than hiding the negative result. A hypothesis that cannot be anchored to a real dependency and a real source therapy is not emitted. This is what separates an engine that generates leads from one that hallucinates them.

## Worked examples of hypotheses Anveshar surfaces

The following are the kinds of hypotheses the discovery layer generates. Each is a research hypothesis, not a clinical recommendation.

### 1. SMARCB1 / SWI-SNF loss nominates EZH2 inhibition by analogy to epithelioid sarcoma

Renal medullary carcinoma and other SMARCB1 (INI1/BAF47) deficient rare tumors sit in the SWI/SNF deficient rhabdoid family. Loss of the SWI/SNF (BAF) complex shifts the chromatin balance toward EZH2 mediated repression, creating a dependence on EZH2. That dependency is drugged in the source condition: tazemetostat, an EZH2 inhibitor, is FDA approved for INI1/SMARCB1 deficient advanced epithelioid sarcoma (Gounder et al., Lancet Oncol 2020, PMID 33035459, [DOI](https://doi.org/10.1016/S1470-2045(20)30451-4)).

The Anveshar hypothesis is that the same SWI/SNF to PRC2 axis makes EZH2 inhibition worth testing in the SMARCB1 deficient rare kidney cancer, with the testable prediction being loss of viability in SMARCB1 null patient derived models on EZH2 blockade. Honesty note: the transferability here is medium, not high, and Anveshar records why. A dedicated tazemetostat basket cohort in renal medullary carcinoma returned no objective responses (0 of 14), so the mechanistic rationale is strong but single agent clinical signal in that specific disease was negative, which is exactly why the flagship translation is graded Tier 3 and the discovery variant is framed as a combination hypothesis rather than a solved case.

### 2. PRMT5 as a synthetic lethal target when MTAP is co-deleted

MTAP is frequently co-deleted with the CDKN2A locus, a common event across many cancers. MTAP loss raises intracellular methylthioadenosine, which partially inhibits PRMT5 and leaves the cell abnormally dependent on residual PRMT5 activity, a synthetic lethal relationship (Kryukov et al., Science 2016, PMID 26912360, [DOI](https://doi.org/10.1126/science.aad5214)).

Anveshar surfaces this as a cross condition hypothesis for any rare cancer that carries a homozygous MTAP deletion: nominate a PRMT5 directed (MTA cooperative) strategy, with the testable prediction that MTAP null lines are selectively sensitive to PRMT5 inhibition relative to MTAP intact controls. The shared dependency is the deletion itself, so the analogy transfers by genotype rather than by tissue of origin, which is what makes it a lead in cancers that have no trials of their own.

### 3. DLL3 as a lineage antigen nominating bispecific and cell therapies

DLL3 is an inhibitory Notch ligand expressed on the surface of neuroendocrine tumor cells and largely absent from normal tissue, which makes it a lineage restricted surface target. In the source condition, small cell lung cancer, the DLL3 x CD3 bispecific T cell engager tarlatamab produced durable responses in previously treated disease (Ahn et al., N Engl J Med 2023, PMID 37861218, [DOI](https://doi.org/10.1056/NEJMoa2307980)).

Anveshar flags DLL3 as a candidate lineage antigen in other high grade neuroendocrine cancers, including rare extrapulmonary neuroendocrine carcinomas, and nominates bispecific and cell therapy modalities by analogy, with the testable prediction being DLL3 surface positivity by immunohistochemistry in the target tumor followed by ex vivo T cell redirection. The dependency here is a surface lineage program, not a mutation, so the same antigen directed logic that works in the source disease is the basis for the hypothesis.

### 4. Splice lesion nominating antisense correction as a modality

When Anveshar detects a splice altering lesion in a rare cancer (for example an exon skipping event that stabilizes an oncoprotein, or a loss of function splice change in a tumor suppressor), it can nominate antisense oligonucleotide splice modulation as a candidate modality by analogy to diseases where splice directed antisense drugs are validated in the clinic (the concrete cross disease anchors are discussed in `docs/gene_therapy.md` and `docs/rare_disease_expansion.md`). This is a modality level hypothesis: the prediction is that an allele or exon specific antisense reagent shifts splicing back toward the desired isoform in patient derived cells. It is kept firmly in the discovery tier because splice targeting in oncology is early, and Anveshar grades the transferability as speculative accordingly.

### 5. Loss of function tumor suppressor nominating a synthetic lethal or restoration strategy

For a defining biallelic tumor suppressor loss in a rare cancer, small molecule inhibition is often not an option because there is no protein left to inhibit. Anveshar instead nominates two orthogonal directions: a synthetic lethal partner (as in the MTAP/PRMT5 case above) and, at the research frontier, gene directed restoration of the lost function. The testable prediction for the synthetic lethal arm is genotype selective sensitivity; for the restoration arm it is functional rescue in a model system. Both are labeled research directions, and the gene directed arm is explicitly framed as a modality hypothesis rather than an available therapy.

## Why an engine like this matters most for rare cancers

For a common cancer, a per disease lookup is usually enough, because the trials exist and the guidelines are populated. For a rare cancer, the lookup returns almost nothing, and the shared dependency abstraction is often the only path to a rational option. By reasoning over the dependency rather than the disease label, Anveshar can borrow a therapy proven in a common cancer that happens to share the same molecular wiring, and hand a rare cancer researcher a ranked, cited, falsifiable shortlist where a lookup table would return an empty page. The engine does not claim these hypotheses are proven. It claims they are non obvious, mechanistically grounded, and worth testing, and it says exactly what test would settle each one.

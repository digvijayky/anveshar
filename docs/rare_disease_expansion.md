# Beyond cancer: expanding Anveshar to all rare diseases

Anveshar's core abstraction is not specific to cancer. It is: a molecular lesion, mapped through its mechanism, to a therapy validated in a mechanistically related condition, graded by evidence and, where the evidence runs out, converted into a testable hypothesis. That lesion to mechanism to cross condition therapy chain is exactly the reasoning that rare Mendelian and genetic disease also demands. This document explains why the same engine generalizes to the roughly 7,000 rare genetic diseases, gives concrete cited illustrations of cross condition borrowing and gene directed therapy, and describes the architectural changes required, which are mostly a swap of the knowledge bases rather than a rebuild of the engine.

## Why the abstraction transfers

A rare cancer and a rare Mendelian disease pose the same structural problem. Both are defined by a molecular lesion. Both are individually too rare to attract dedicated trials, so the per disease evidence base is nearly empty. And in both, the rational path to a therapy is frequently to reason over the shared molecular mechanism rather than the disease label, and to borrow a therapy proven in a mechanistically adjacent condition. A therapy proven in one channelopathy, lysosomal storage disorder, or DNA repair syndrome is often the most rational lead for a mechanistically adjacent one, and gene directed modalities are frequently the only realistic option when the lesion is a loss of function that no small molecule can restore.

The engine already reasons this way. In the cancer setting Anveshar walks from a lesion (for example SMARCB1 loss) to a mechanism (SWI/SNF to PRC2 imbalance and EZH2 dependence) to a therapy validated in a related condition (an EZH2 inhibitor in epithelioid sarcoma). Replace the oncology axis with a rare disease axis, keeping the same `DiscoveryHypothesis` structure (`shared_dependency`, `source_condition`, `proposed_modality`, `transferability`, `supporting_citation`, `testable_prediction`), and the same walk produces rare disease hypotheses.

## Illustrations of cross condition borrowing and gene directed therapy

Each example below is a real, cited, approved therapy in rare genetic disease. They illustrate the two patterns Anveshar is built to surface: gene directed correction of the causal lesion, and modality level borrowing across mechanistically related conditions.

### 1. Antisense oligonucleotide splice correction: nusinersen for spinal muscular atrophy

Spinal muscular atrophy is caused by loss of function of SMN1. The therapeutic insight is mechanistic rather than gene replacement: the nearly identical paralog SMN2 is present but is mostly mis spliced to skip exon 7, so an antisense oligonucleotide that corrects SMN2 splicing restores functional SMN protein. Nusinersen, an intrathecal splice switching antisense oligonucleotide, improved motor function and survival in infantile onset disease (Finkel et al., N Engl J Med 2017, PMID 29091570, [DOI](https://doi.org/10.1056/NEJMoa1702752)).

The Anveshar relevant pattern: a splice lesion (or a modifiable splicing paralog) maps to antisense oligonucleotide splice modulation as a modality. This is precisely the splice to antisense analogy that Anveshar uses in the cancer setting, run instead on a Mendelian splice mechanism.

### 2. Gene replacement: onasemnogene abeparvovec for the same disease, different modality

The same SMN1 loss can be addressed by a different modality entirely. Onasemnogene abeparvovec is a one time intravenous adeno associated virus serotype 9 vector that delivers a functional SMN1 transgene, and it improved survival and motor milestones in spinal muscular atrophy type 1 (Mendell et al., N Engl J Med 2017, PMID 29091557, [DOI](https://doi.org/10.1056/NEJMoa1706198)).

The Anveshar relevant pattern: a defining loss of function lesion maps to gene replacement as a modality. That spinal muscular atrophy is treatable by two different modalities on the same lesion (antisense splice correction and gene replacement) is exactly the modality dimension Anveshar is designed to enumerate rather than collapse (see `docs/gene_therapy.md`).

Verification note: the prompt supplied PMID 31091570 for onasemnogene abeparvovec, but that identifier resolves to an unrelated article; the pivotal spinal muscular atrophy gene replacement report is PMID 29091557 (Mendell et al., 2017), which is used here.

### 3. RNA silencing borrowed across a mechanistic class: patisiran for hereditary transthyretin amyloidosis

Hereditary transthyretin amyloidosis is driven by a mutant TTR gene whose product misfolds and deposits as amyloid. Patisiran is a lipid nanoparticle delivered small interfering RNA that knocks down hepatic TTR messenger RNA, reducing the pathogenic protein at its source and improving polyneuropathy outcomes (Adams et al., N Engl J Med 2018, PMID 29972753, [DOI](https://doi.org/10.1056/NEJMoa1716153)).

The Anveshar relevant pattern: a gain of function or toxic protein lesion maps to RNA knockdown as a modality, a lead that generalizes to other diseases driven by a toxic or overexpressed transcript rather than by loss of function.

### 4. Gene editing to reactivate a compensatory program: exagamglogene autotemcel for hemoglobinopathies

Sickle cell disease and transfusion dependent beta thalassemia are distinct beta globin lesions, yet both were addressed by the same borrowed mechanism: CRISPR-Cas9 editing of the BCL11A erythroid enhancer to de repress fetal hemoglobin, which compensates for the defective adult beta globin. Editing produced transfusion independence and, in sickle cell disease, elimination of vaso occlusive episodes (Frangoul et al., N Engl J Med 2021, PMID 33283989, [DOI](https://doi.org/10.1056/NEJMoa2031054)).

The Anveshar relevant pattern: two mechanistically related lesions (different mutations, shared downstream program) map to the same gene editing strategy that reactivates a compensatory pathway. This is cross condition borrowing at the mechanism level, the rare disease analog of a genotype defined synthetic lethal lead in cancer.

## Architectural changes needed

The engine, the schema, and the evidence discipline stay. What changes is the knowledge layer.

Swap the cancer knowledge bases for rare disease ones. The oncology actionability frameworks (OncoKB, AMP/ASCO/CAP, ESCAT) and the tissue agnostic precedent table are replaced with rare disease equivalents: gene to disease and variant to phenotype resources (for example ClinVar, which Anveshar already connects to, alongside OMIM, Orphanet, and ClinGen style curation), and a catalog of approved and investigational rare disease therapies indexed by mechanism and modality. The `Tier` semantics generalize cleanly, since the top tiers already encode approval and cross condition transfer rather than anything cancer specific, and `Tier.DISCOVERY` remains the novel hypothesis tier.

Keep the connectors that are already disease agnostic. UniProt, Ensembl, Reactome, and ClinVar are not oncology specific and carry over unchanged. Reactome pathway context is what lets the engine reason about mechanistic adjacency between conditions, which is the heart of rare disease borrowing. The Evo 2 and AlphaMissense variant effect adapters carry over directly and are arguably more central in Mendelian disease, where variant of uncertain significance interpretation is the dominant bottleneck.

Retarget the target extractor and the translation table. In the cancer setting, `anveshar.translation` maps molecular targets to therapies validated in other tumors. In the rare disease setting it maps a causal gene and its mechanism (loss of function, gain of function, toxic protein, splice defect) to therapies validated in mechanistically adjacent conditions, and to the modality that fits the lesion (gene replacement or editing for loss of function, RNA knockdown or antisense for toxic or mis spliced transcripts, small molecule for a druggable residual enzyme). The discovery layer is unchanged in structure; only the knowledge it reasons over is different.

Keep the honesty. Every borrowed therapy still carries a real citation, transferability is still graded, negative cross condition results are still recorded rather than hidden, and unverifiable claims are still marked UNVERIFIED. Anveshar in the rare disease setting generates hypotheses; it does not claim clinical proof, and it defers every treatment decision to a qualified clinical team.

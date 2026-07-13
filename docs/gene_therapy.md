# The modality dimension: advanced therapies beyond small molecules

Most precision oncology tools implicitly assume the answer to a lesion is a small molecule inhibitor. That assumption fails exactly where rare cancers and rare diseases live: when the lesion is a lost tumor suppressor with no protein to inhibit, a lineage surface antigen better attacked by a redirected immune cell, a splice defect better fixed at the RNA level, or a receptor better delivered a radioactive payload than blocked. Anveshar treats the therapeutic modality as a first class axis. The `Modality` enum in `anveshar.schema` enumerates small molecule, antibody, antibody drug conjugate, bispecific T cell engager, cell therapy, gene therapy, antisense oligonucleotide, radioligand therapy, cytotoxic chemotherapy, and immune checkpoint inhibitor, and every `Therapy` and `DiscoveryHypothesis` carries a `proposed_modality`. This lets the discovery layer nominate an advanced modality when the lesion calls for one, not only a kinase inhibitor.

Everything below is a research direction when it appears in the discovery tier. The cited anchors are real, approved or trial validated therapies in their source conditions; Anveshar's contribution is to reason about when a given lesion class should nominate a given modality, and to state the experiment that would test it.

## Small molecule

Anchor: encorafenib plus cetuximab for BRAF V600E colorectal cancer, where the actionable regimen is context dependent RAF plus EGFR co blockade rather than RAF monotherapy (see `docs/variant_interpretation_methodology.md`).

When Anveshar nominates it: an activating hotspot or a druggable residual enzyme, where a defined pocket can be inhibited. This is the default modality and the best populated, so it is where lookup style matching already works; the modality axis matters most for everything that follows.

## Antibody and antibody drug conjugate

Anchor: HER2 (ERBB2) directed antibodies and the antibody drug conjugate trastuzumab deruxtecan for HER2 amplified or expressing tumors (see `docs/variant_interpretation_methodology.md`).

When Anveshar nominates it: an amplified or over expressed cell surface receptor. Amplification nominates a naked antibody or, when a cytotoxic payload is warranted, an antibody drug conjugate that carries chemotherapy directly to antigen positive cells.

## Bispecific T cell engager

Anchor: tarlatamab, a DLL3 x CD3 bispecific T cell engager, produced durable responses in previously treated small cell lung cancer (Ahn et al., N Engl J Med 2023, PMID 37861218, [DOI](https://doi.org/10.1056/NEJMoa2307980)).

When Anveshar nominates it: a lineage restricted surface antigen expressed on tumor and largely absent from normal tissue (DLL3 in neuroendocrine lineages is the paradigm). A bispecific redirects the patient's own T cells to the antigen, so surface positivity, not a mutation, is the dependency, and the testable prediction is antigen positivity by immunohistochemistry plus ex vivo T cell redirection.

## Cell therapy

Anchor: tisagenlecleucel, an autologous CD19 directed chimeric antigen receptor T cell product, in relapsed or refractory B cell acute lymphoblastic leukemia (Maude et al., N Engl J Med 2018, PMID 29385370, [DOI](https://doi.org/10.1056/NEJMoa1709866)).

When Anveshar nominates it: a lineage surface antigen where durable, self renewing killing is desirable, especially in hematologic or antigen homogeneous disease. The same lineage antigen that nominates a bispecific can nominate an engineered cell therapy; Anveshar surfaces both as parallel modality hypotheses on the same dependency.

## Radioligand therapy

Anchor: lutetium-177-PSMA-617, a radioligand that delivers beta emitting radiation to PSMA positive cells, in metastatic castration resistant prostate cancer (Sartor et al., N Engl J Med 2021, PMID 34161051, [DOI](https://doi.org/10.1056/NEJMoa2107322)).

When Anveshar nominates it: a receptor or surface molecule that is over expressed and internalizing, so a targeting ligand can carry a radioactive payload to it. Receptor over expression maps to radioligand therapy as a modality, with the testable prediction being target positive uptake on companion imaging.

## Antisense oligonucleotide

Anchor: nusinersen, an intrathecal splice switching antisense oligonucleotide that corrects SMN2 splicing in spinal muscular atrophy (Finkel et al., N Engl J Med 2017, PMID 29091570, [DOI](https://doi.org/10.1056/NEJMoa1702752)).

When Anveshar nominates it: a splice lesion, or a target better silenced or spliced at the RNA level than at the protein level. A splice altering event maps to antisense oligonucleotide splice modulation; a toxic or over expressed transcript maps to RNA knockdown (the same RNA directed logic underlies the small interfering RNA drug patisiran in hereditary transthyretin amyloidosis, Adams et al., N Engl J Med 2018, PMID 29972753, [DOI](https://doi.org/10.1056/NEJMoa1716153)). In oncology this is early, so Anveshar grades it as a speculative discovery direction.

## Gene directed strategies

This is the frontier of the modality axis, reserved for the discovery tier and framed explicitly as research directions.

**Synthetic lethality.** For a loss of function driver where the lost protein cannot be restored pharmacologically, Anveshar nominates a synthetic lethal partner instead. The canonical anchor is PRMT5 dependence created by MTAP co deletion (Kryukov et al., Science 2016, PMID 26912360, [DOI](https://doi.org/10.1126/science.aad5214)); the SWI/SNF to EZH2 dependence created by SMARCB1 loss is a related epigenetic example (see `docs/novelty.md`). When Anveshar nominates it: a biallelic loss of function lesion with a known or inferable synthetic lethal partner, with the testable prediction being genotype selective sensitivity to inhibition of the partner.

**Gene replacement.** For a defining loss of function lesion, deliver a functional copy of the gene. The anchor is onasemnogene abeparvovec, an adeno associated virus vector delivering a functional SMN1 transgene in spinal muscular atrophy (Mendell et al., N Engl J Med 2017, PMID 29091557, [DOI](https://doi.org/10.1056/NEJMoa1706198)). When Anveshar nominates it: a loss of function driver in a setting where restoring the gene is plausible, framed as a research direction given the delivery and safety constraints in oncology.

**Base and prime editing.** For a lesion best fixed by precise nucleotide level correction or by reactivating a compensatory program, Anveshar nominates a gene editing strategy. The clinical anchor for therapeutic in vivo relevant editing is CRISPR-Cas9 editing of the BCL11A enhancer to de repress fetal hemoglobin in sickle cell disease and beta thalassemia (Frangoul et al., N Engl J Med 2021, PMID 33283989, [DOI](https://doi.org/10.1056/NEJMoa2031054)); base and prime editing extend this toward single base and small insertion or deletion correction without a double strand break. When Anveshar nominates it: a correctable point lesion or a targetable regulatory element, kept firmly in the discovery tier.

## Honesty

Anveshar does not claim any of these advanced modalities is available or proven for the target disease when it nominates one. It states the lesion class, the modality the analogy points to, the cited anchor in the source condition, the transferability grade, and the experiment that would confirm or refute the lead. The modality axis exists so that a rare cancer or rare disease researcher sees the full space of rational options, including the ones a small molecule only tool would never surface, while every option stays honestly graded and every treatment decision is deferred to a qualified clinical team.

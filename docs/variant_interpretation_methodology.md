# Variant Interpretation and Actionability Methodology (Anveshar)

Purpose: define how the Anveshar decision-support engine interprets a wide range of variant classes (not only hotspot point mutations) and grades each alteration for therapeutic actionability using published clinical frameworks. Every interpretation rule below is traceable to a primary source (see SOURCES). Any value that could not be independently verified is marked UNVERIFIED.

Design principle: never fabricate a variant, a numeric score, or a citation. Named single variants are corroborated against ClinVar via NCBI E-utilities and the accession plus classification is recorded. Predicted (in silico) scores from sequence models are used only as method rationale for reclassifying variants of uncertain significance (VUS), never as invented numbers.

---

## PART A. Clinical actionability frameworks

Anveshar grades each alteration on three complementary, published axes: OncoKB therapeutic level (drug-matching evidence), AMP/ASCO/CAP tier (clinical significance of the variant), and ESCAT tier (readiness of the target for clinical decisions). Using all three avoids over-calling a variant that looks compelling biologically but lacks clinical evidence.

### A1. OncoKB Therapeutic Levels of Evidence (Chakravarty et al 2017, JCO Precision Oncology; PMID 28890946)

OncoKB is an expert-curated precision oncology knowledge base that annotates the oncogenic effect and the predictive or prognostic significance of somatic alterations, and stratifies treatment implications by an evidence ladder anchored to FDA labeling, NCCN and expert-panel guidelines, and the literature. In the original report, 41 percent of tumors carried at least one potentially actionable alteration and 7.5 percent carried an alteration predictive of benefit from a standard therapy. A portion of OncoKB was granted partial FDA recognition in October 2021 as a source of valid scientific evidence for variant interpretation.

Therapeutic levels (predictive of response):
1. Level 1: the alteration is an FDA-recognized biomarker predictive of response to an FDA-approved drug in this indication (tumor type).
2. Level 2: the alteration is a standard-care biomarker recommended by NCCN or other expert panels as predictive of response to an FDA-approved drug in this indication.
3. Level 3A: compelling clinical evidence supports the alteration as predictive of response to a drug in this indication, but neither FDA-recognized nor standard care.
4. Level 3B: the alteration is a standard-care or investigational biomarker predictive of response to an FDA-approved or investigational drug in another indication (a different tumor type).
5. Level 4: compelling biological (preclinical) evidence supports the alteration as predictive of drug response.

Resistance levels:
6. Level R1: the alteration is a standard-care biomarker predictive of resistance to an FDA-approved drug.
7. Level R2: compelling clinical evidence supports the alteration as predictive of resistance to a drug.

Interpretation rule in Anveshar: Level 1 and Level 2 alterations drive standard-of-care matching; Level 3A/3B and Level 4 are surfaced as clinical-trial or off-label rationale, explicitly flagged as investigational. Resistance calls (R1/R2) are shown as contraindications alongside the matched drug.

### A2. AMP/ASCO/CAP 2017 four-tier somatic variant classification (Li et al 2017, Journal of Molecular Diagnostics; PMID 27993330)

A joint consensus of the Association for Molecular Pathology, the American Society of Clinical Oncology, and the College of American Pathologists that classifies somatic sequence variants by their clinical significance into four tiers, independent of any single drug. This is the axis that answers "how strong is the evidence that this variant matters clinically," and it is the classification recorded in ClinVar's somatic (clinical impact) field.

1. Tier I: variants of strong clinical significance. Tier I-A: FDA-approved therapy or included in professional guidelines for this specific tumor type. Tier I-B: well-powered studies with expert consensus.
2. Tier II: variants of potential clinical significance. Tier II-C: FDA-approved therapy for a different tumor type, or used as an inclusion criterion for clinical trials. Tier II-D: plausible therapeutic, prognostic, or diagnostic significance supported by preclinical or small studies.
3. Tier III: variants of unknown clinical significance (VUS). Not observed at significant population frequency in databases and without convincing published evidence of cancer association.
4. Tier IV: benign or likely benign variants. Not reported in clinical databases as somatic drivers.

Interpretation rule in Anveshar: Tier I and Tier II variants are reportable and actionability-graded; Tier III (VUS) are candidates for in silico reclassification (see A-below and Part A2 on Evo 2 / AlphaMissense); Tier IV are suppressed from the actionability view.

### A3. ESCAT, the ESMO Scale for Clinical Actionability of molecular Targets (Mateo et al 2018, Annals of Oncology 29(9):1895-1902; PMID 30137196; DOI 10.1093/annonc/mdy263)

ESCAT ranks a genomic alteration by how ready the target is to inform a routine clinical decision, emphasizing the strength and transferability of the supporting evidence across tumor types. Six tiers:

1. Tier I: target ready for routine clinical use. Alteration-drug match associated with improved outcome in prospective trials (I-A), or by prospective trials or retrospective studies where the alteration itself is the biomarker in the studied tumor type (I-B), or across tumor types in a basket-trial or tumor-agnostic setting (I-C).
2. Tier II: investigational target. Antitumor activity is shown but the magnitude of benefit is not yet established, or data come from a single-arm setting (II-A retrospective; II-B early signal).
3. Tier III: clinical benefit demonstrated in a different tumor type or for a related alteration in the same pathway (III-A same alteration different tumor type; III-B similar alteration same gene or pathway).
4. Tier IV: preclinical evidence of actionability only (in vitro or in vivo).
5. Tier V: evidence that co-targeting the alteration alongside another target improves outcome, without single-agent evidence.
6. Tier X: no evidence that the alteration is actionable.

Interpretation rule in Anveshar: ESCAT tier I to II support treatment recommendations; tier III supports tumor-agnostic or basket-trial rationale; tier IV/V are hypothesis-generating; tier X alterations are not surfaced as targets. ESCAT and OncoKB are cross-checked; a divergence (for example OncoKB Level 1 in this tumor type but ESCAT tier III because the pivotal evidence came from another tumor type) is flagged for the reviewing clinician.

---

## PART A2. Interpreting sophisticated variant CLASSES for therapy matching

Each class below lists what the alteration means biologically, a real actionable example with citation, and the therapy implication. Anveshar routes each detected alteration to the matching interpreter.

### (a) SNV and indel hotspots
Recurrent activating point mutations or small indels at defined codons that switch on an oncogene or knock out a tumor suppressor.
Examples: BRAF V600E (activating class I RAF mutation) is targeted by RAF-directed regimens; in BRAF V600E metastatic colorectal cancer the encorafenib plus cetuximab doublet is approved after prior therapy (BEACON CRC, Kopetz et al 2019, NEJM). KRAS G12C, long considered undruggable, is targeted by covalent G12C inhibitors; sotorasib was approved for KRAS G12C non-small-cell lung cancer (CodeBreaK 100, Skoulidis et al 2021, NEJM). IDH1 R132 defines IDH1-mutant tumors targeted by ivosidenib. Therapy implication: hotspot identity determines the matched inhibitor and, critically, the tumor context (BRAF V600E responds to BRAF/EGFR co-blockade in colorectal cancer but not to BRAF monotherapy, which produces feedback EGFR reactivation).

### (b) Gene fusions
A structural rearrangement that joins two genes so a kinase domain is placed under a constitutively active promoter or dimerization partner.
Examples: NTRK1/2/3 fusions are tumor-agnostic targets for larotrectinib and entrectinib (Drilon et al 2018, NEJM, pooled TRK-fusion dataset). RET fusions are targeted by selpercatinib and pralsetinib; ALK and ROS1 fusions by ALK/ROS1 inhibitors (alectinib, lorlatinib, entrectinib, crizotinib); FGFR2 fusions by pemigatinib and futibatinib in cholangiocarcinoma; NRG1 fusions by zenocutuzumab. Therapy implication: fusions are frequently tumor-agnostic (OncoKB Level 1 or ESCAT tier I-C in a basket setting) and are often missed by DNA-only hotspot panels, so RNA-based fusion detection is required to avoid false negatives.

### (c) Copy-number amplification and deep deletion
Amplification raises oncogene dosage; homozygous (deep) deletion removes a tumor suppressor.
Examples of amplification: ERBB2 (HER2) amplification is targeted by trastuzumab, trastuzumab deruxtecan, and (in colorectal cancer) trastuzumab plus tucatinib or lapatinib; MET amplification by MET inhibitors; FGFR1/2 amplification by FGFR inhibitors in selected contexts. Examples of deep deletion: CDKN2A/B loss removes p16 and sensitizes to CDK4/6-directed strategies under investigation; PTEN loss activates PI3K/AKT signaling; SMARCB1 loss defines rhabdoid tumors and is a target of EZH2 inhibition (tazemetostat); RB1 loss is prognostic and confers CDK4/6-inhibitor resistance. Therapy implication: copy-number thresholds matter (focal high-level amplification is actionable; low-level gain often is not), so the caller records copy number and focality, not a binary flag.

### (d) Splice variants
Mutations that disrupt splicing so an exon is skipped or retained, changing the protein without a canonical missense change.
Example: MET exon 14 skipping (splice-site alterations that delete the juxtamembrane exon 14, stabilizing MET) is targeted by capmatinib and tepotinib in non-small-cell lung cancer (capmatinib GEOMETRY mono-1, Wolf et al). Therapy implication: splice events are invisible to a caller that only reports coding SNVs at the affected codon; they require splice-aware annotation (and, for VUS-level splice changes, splicing predictors or RNA confirmation).

### (e) Epigenetic events
Promoter methylation that silences a gene without any sequence change.
Examples: MLH1 promoter hypermethylation silences MLH1, produces mismatch-repair deficiency and the sporadic MSI-H phenotype in colorectal and other cancers, which in turn predicts benefit from immune-checkpoint blockade; MLH1 methylation (often with BRAF V600E) is also used to distinguish sporadic MSI from Lynch syndrome. MGMT promoter methylation predicts benefit from temozolomide in glioblastoma (Hegi et al 2005, NEJM). Therapy implication: an epigenetic silencing event is functionally equivalent to a biallelic loss-of-function and must be interpreted as such; MLH1 methylation is the mechanistic bridge from an epigenetic event to a composite immunotherapy biomarker (MSI-H), and MGMT methylation directly grades a chemotherapy choice.

### (f) Composite genomic biomarkers
Aggregate features computed across the genome rather than a single locus.
Examples: MSI-H / dMMR predicts benefit from PD-1 blockade and is a tumor-agnostic indication for pembrolizumab (KEYNOTE-158, Marabelle et al 2020; and first-line colorectal approval from KEYNOTE-177). TMB-high (defined at 10 mutations per megabase in the pembrolizumab tumor-agnostic label) predicts checkpoint-inhibitor benefit. HRD / genomic LOH (homologous-recombination deficiency, quantified by LOH, telomeric allelic imbalance, and large-scale transitions) predicts PARP-inhibitor benefit in ovarian and other cancers. Therapy implication: composite biomarkers are computed by the engine from the full variant set and mapped to immunotherapy or PARP-inhibitor eligibility; they can be actionable even when no single mutation is druggable.

### (g) Mutational signatures
Genome-wide patterns of substitutions that fingerprint the underlying mutational process (Alexandrov et al 2020, Nature; PMID 32025018; the COSMIC SBS/DBS/ID signature reference set).
Examples: mismatch-repair-deficiency signatures (SBS6, SBS15, SBS20, SBS21, SBS26 and the associated indel signatures) corroborate an MSI-H / dMMR state and thus checkpoint-inhibitor rationale; SBS3 (and ID6) indicate homologous-recombination deficiency and support PARP-inhibitor or platinum rationale even when BRCA1/2 status is ambiguous; APOBEC signatures (SBS2 and SBS13) mark APOBEC-driven hypermutation. Therapy implication: signatures are orthogonal corroboration for composite biomarkers. A dMMR signature strengthens an MSI-H call; an SBS3 signature can rescue an HRD call when the causal gene event is a VUS.

### (h) VUS reclassification with sequence models
Variants of uncertain significance (AMP/ASCO/CAP Tier III) can be re-graded with machine-learning variant-effect predictors, used strictly as method rationale, not as fabricated numbers.
1. Evo 2 (Brixi, Durrant, Ku et al 2025) is a DNA foundation model trained on 9.3 trillion base pairs across all domains of life; it predicts the functional impact of coding and noncoding variation zero-shot, including clinically significant BRCA1 variants and splice-affecting noncoding changes, without task-specific fine-tuning. This makes it useful for coding, noncoding, and splice-region VUS where AlphaMissense (which scores only missense substitutions) does not apply. The peer-reviewed version appeared in Nature in 2026 (PMID 41781614).
2. AlphaMissense (Cheng et al 2023, Science; PMID 37733863) assigns every possible human missense substitution a calibrated pathogenicity score (likely benign / ambiguous / likely pathogenic) and classifies about 89 percent of missense variants, far more than are curated in ClinVar.
Interpretation rule in Anveshar: for a Tier III missense VUS, an AlphaMissense "likely pathogenic" prediction and/or an Evo 2 damaging prediction raises the pre-test suspicion and routes the variant to functional review; the model output is always labeled as computational prediction and never converted into a clinical tier on its own. These tools reduce the fraction of alterations that are dead-ends by proposing which VUS deserve orthogonal confirmation.

---

## PART B. Sophisticated demo profile (a real, published, multi-class case)

Case chosen: a right colon high-grade mixed neuroendocrine and non-neuroendocrine neoplasm (MiNEN) that is microsatellite-unstable and BRAF V600E-mutated, reported by Pereira, White, Mortellaro and Jiang, "Unusual Microsatellite-Instable Mixed Neuroendocrine and Non-neuroendocrine Neoplasm: A Clinicopathological Inspection and Literature Review," Cancer Control 2023; 30:10732748231160992 (PMID 36840617; DOI 10.1177/10732748231160992).

Why this case: it is a rare, molecularly rich gastrointestinal high-grade tumor whose actual reported alterations span several distinct variant classes at once, so it exercises the full interpreter set without any invented variants.

Reported alterations (only what the paper actually reports):
1. Mismatch-repair deficiency by immunohistochemistry: loss of MLH1 and PMS2 with intact MSH2 and MSH6. Lynch syndrome was excluded by germline testing, so the MLH1/PMS2 loss is the sporadic pattern, which is characteristically driven by MLH1 promoter hypermethylation (the paper reports the dMMR IHC pattern and excludes Lynch; promoter-methylation testing itself is not separately reported, so the methylation mechanism is annotated as inferred and marked UNVERIFIED at the assay level while the dMMR phenotype is verified).
2. BRAF p.V600E mutation, identified by next-generation sequencing. Corroborated in ClinVar: accession VCV000013961, NM_004333.6(BRAF):c.1799T>A (p.Val600Glu); somatic (clinical impact) classification "Tier I - Strong"; oncogenicity "Oncogenic"; germline classification "Conflicting classifications of pathogenicity." The co-occurrence of BRAF V600E with MLH1-loss dMMR is itself the classic sporadic-MSI signature that argues against Lynch syndrome, consistent with the paper's germline result.
3. Derived composite biomarker: MSI-H / dMMR (from finding 1). This is the alteration that carried the treatment decision.
4. High proliferative index (Ki-67 approximately 84 percent) supporting the high-grade neuroendocrine component; this is an immunohistochemical phenotype, not a sequence variant, and is recorded as context rather than an actionable alteration.

Variant classes exercised by this one case: SNV hotspot (BRAF V600E), epigenetic silencing (MLH1 loss, sporadic dMMR), composite genomic biomarker (MSI-H / dMMR), and mutational signature (the MMR-deficiency SBS/ID signature class is the genome-wide corroboration of the dMMR state; the paper did not perform signature deconvolution, so any specific SBS assignment is marked UNVERIFIED and is used only as the class-level rationale).

Interpretation and actionability grading:
1. MSI-H / dMMR maps to PD-1 blockade. Pembrolizumab is a tumor-agnostic option for MSI-H/dMMR solid tumors (KEYNOTE-158, Marabelle et al 2020) and first-line standard for MSI-H/dMMR metastatic colorectal cancer (KEYNOTE-177). Grading: OncoKB Level 1; AMP/ASCO/CAP Tier I; ESCAT tier I-C (tumor-agnostic). This is the decisive actionable finding.
2. BRAF V600E maps to RAF-directed therapy, but context-dependently. In colorectal cancer the actionable regimen is encorafenib plus cetuximab (BEACON CRC, Kopetz et al 2019), not BRAF monotherapy. Grading for the BRAF V600E-to-encorafenib+cetuximab match in colorectal cancer: OncoKB Level 1; AMP/ASCO/CAP Tier I; ESCAT tier I-B. In this particular patient BRAF V600E is secondary to the MSI-H immunotherapy indication but is a validated backup or combination rationale, and it also functions diagnostically (sporadic-MSI marker).
3. MLH1 silencing (epigenetic) is interpreted as the mechanism producing dMMR; it is not independently drug-matched but is the causal bridge to the MSI-H immunotherapy indication and to the sporadic-versus-Lynch distinction.

VUS-reclassification demonstration on this case: BRAF V600E is not a VUS (it is ClinVar Tier I - Strong, oncogenic), so it does not itself require reclassification. To demonstrate the idea concretely, consider the hypothetical in which the NGS report had instead returned a rare BRAF non-V600 missense change of uncertain significance (AMP/ASCO/CAP Tier III). Anveshar would route that missense VUS to AlphaMissense (Cheng et al 2023), whose calibrated per-substitution pathogenicity score would classify it as likely benign, ambiguous, or likely pathogenic; if the change fell in or near a splice region, or were noncoding, Anveshar would instead query Evo 2 (Brixi et al 2025 / Nature 2026), which scores coding, noncoding, and splice-affecting variants zero-shot. A "likely pathogenic" or damaging prediction would raise suspicion and route the variant to functional confirmation, but would never by itself be promoted to a clinical tier. This is stated as method rationale; no numeric model score is asserted for this case because none is published for it (marked UNVERIFIED).

Summary of the demo case: one real, published, rare gastrointestinal high-grade tumor whose actual alterations exercise four variant classes and yield a decisive, guideline-backed treatment match (PD-1 blockade for MSI-H/dMMR), with BRAF V600E as a corroborating and secondary actionable event, and a clearly labeled method-rationale demonstration of how a missense or splice-region VUS would be triaged by AlphaMissense or Evo 2. The reported outcome (durable remission on pembrolizumab) is consistent with the MSI-H/dMMR actionability grade.

---

## SOURCES

Frameworks:
1. Chakravarty D, Gao J, Phillips S, et al. OncoKB: A Precision Oncology Knowledge Base. JCO Precision Oncology. 2017. PMID 28890946. DOI 10.1200/PO.17.00011.
2. Li MM, Datto M, Duncavage EJ, et al. Standards and Guidelines for the Interpretation and Reporting of Sequence Variants in Cancer: A Joint Consensus Recommendation of the Association for Molecular Pathology, American Society of Clinical Oncology, and College of American Pathologists. Journal of Molecular Diagnostics. 2017. PMID 27993330. DOI 10.1016/j.jmoldx.2016.10.002.
3. Mateo J, Chakravarty D, Dienstmann R, et al. A framework to rank genomic alterations as targets for cancer precision medicine: the ESMO Scale for Clinical Actionability of molecular Targets (ESCAT). Annals of Oncology. 2018; 29(9):1895-1902. PMID 30137196. DOI 10.1093/annonc/mdy263.

Variant-class actionability examples:
4. Kopetz S, Grothey A, Yaeger R, et al. Encorafenib, Binimetinib, and Cetuximab in BRAF V600E-Mutated Colorectal Cancer (BEACON CRC). New England Journal of Medicine. 2019. PMID 31566309. DOI 10.1056/NEJMoa1908075.
5. Skoulidis F, Li BT, Dy GK, et al. Sotorasib for Lung Cancers with KRAS p.G12C Mutation (CodeBreaK 100). New England Journal of Medicine. 2021. PMID 34096690. DOI 10.1056/NEJMoa2103695.
6. Drilon A, Laetsch TW, Kummar S, et al. Efficacy of Larotrectinib in TRK Fusion-Positive Cancers in Adults and Children. New England Journal of Medicine. 2018. PMID 29466156. DOI 10.1056/NEJMoa1714448.
7. Wolf J, Seto T, Han JY, et al. Capmatinib in MET Exon 14-Mutated or MET-Amplified Non-Small-Cell Lung Cancer (GEOMETRY mono-1). New England Journal of Medicine. 2020. PMID 32877583. DOI 10.1056/NEJMoa2002787.
8. Hegi ME, Diserens AC, Gorlia T, et al. MGMT Gene Silencing and Benefit from Temozolomide in Glioblastoma. New England Journal of Medicine. 2005. PMID 15758010. DOI 10.1056/NEJMoa043331.
9. Marabelle A, Le DT, Ascierto PA, et al. Efficacy of Pembrolizumab in Patients With Noncolorectal High Microsatellite Instability/Mismatch Repair-Deficient Cancer: Results From the Phase II KEYNOTE-158 Study. Journal of Clinical Oncology. 2020. PMID 31682550. DOI 10.1200/JCO.19.02105.
10. Andre T, Shiu KK, Kim TW, et al. Pembrolizumab in Microsatellite-Instability-High Advanced Colorectal Cancer (KEYNOTE-177). New England Journal of Medicine. 2020. PMID 33264544. DOI 10.1056/NEJMoa2017699.

Signatures and in silico VUS reclassification:
11. Alexandrov LB, Kim J, Haradhvala NJ, et al. The repertoire of mutational signatures in human cancer. Nature. 2020; 578:94-101. PMID 32025018. DOI 10.1038/s41586-020-1943-3.
12. Cheng J, Novati G, Pan J, et al. Accurate proteome-wide missense variant effect prediction with AlphaMissense. Science. 2023. PMID 37733863. DOI 10.1126/science.adg7492.
13. Brixi G, Durrant MG, Ku J, et al. Genome modeling and design across all domains of life with Evo 2. bioRxiv. 2025. DOI 10.1101/2025.02.18.638918. Peer-reviewed version: Nature. 2026. PMID 41781614.

Demo case and its corroborating evidence:
14. Pereira D, White D, Mortellaro M, Jiang K. Unusual Microsatellite-Instable Mixed Neuroendocrine and Non-neuroendocrine Neoplasm: A Clinicopathological Inspection and Literature Review. Cancer Control. 2023; 30:10732748231160992. PMID 36840617. DOI 10.1177/10732748231160992.
15. ClinVar, BRAF NM_004333.6:c.1799T>A (p.Val600Glu). Accession VCV000013961. Somatic (clinical impact) classification: Tier I - Strong; oncogenicity: Oncogenic; germline classification: Conflicting classifications of pathogenicity. https://www.ncbi.nlm.nih.gov/clinvar/variation/13961/

Note on verification: PMIDs and DOIs for items 4 to 10 (drug-approval anchor citations) were resolved from PubMed during preparation; where a specific PMID/DOI could not be confirmed at write time it is marked UNVERIFIED inline in the JSON evidence field rather than asserted here.

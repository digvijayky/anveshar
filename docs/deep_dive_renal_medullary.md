# Deep Translational Intelligence: Renal Medullary Carcinoma (RMC)

**Scope.** RMC is an ultra-rare, highly aggressive kidney cancer of young people of African descent with sickle cell trait, defined by complete biallelic loss of SMARCB1 (INI1/BAF47), a core SWI/SNF (BAF) chromatin-remodeling subunit. This places RMC in the SWI/SNF-deficient rhabdoid tumor family alongside malignant rhabdoid tumor (MRT), atypical teratoid/rhabdoid tumor (AT/RT), and epithelioid sarcoma. This document is a cross-cancer translation deep dive for the four candidate axes (EZH2 inhibition, PRMT5/MTAP synthetic lethality, proteasome inhibition, checkpoint blockade), assembled to demonstrate breadth of tool use and to attribute each key finding to the tool that produced it.

**Method note (tool attribution).** This is a companion to the broader `example_dossier_renal_medullary.md`. The special requirement here was to route each claim through a specific tool and label its provenance. Every nontrivial claim carries a real PMID, DOI, NCT, or a clearly attributed tool result. Items that could not be verified are marked **UNVERIFIED**. No dashes are used per house style; American English throughout. Compiled July 2026.

---

## (a) Tools used

| Tool | Reachable? | What it contributed here |
|---|---|---|
| **Consensus** (`mcp__plugin_consensus_Consensus__search`) | Yes | Evidence synthesis across the four translation axes. Surfaced the pediatric MATCH tazemetostat result (RMC = stable disease), the SMARCB1/EZH2 rhabdoid dependency landmark, the MTA-cooperative PRMT5/MTAP synthetic-lethality literature (MRTX1719, AMG 193, MTAP-deletion reviews), and the bortezomib mechanism-of-action base. |
| **Paperclip** (`mcp__paperclip__paperclip`, full text/preprints) | Yes | Pulled full-text specifics abstracts miss: the Hong 2019 eLife RMC study (UPS/proteasome synthetic lethality, UBE2C dependency, cyclin B1, in vivo MLN2238), and preprints extending PRMT5/MTAP biology (PARP-inhibitor-induced PRMT5 suppression, TNG908 brain-penetrant PRMT5i, PRMT5 in MTAP-deficient MPNST). Confirmed no RMC-specific PRMT5 dataset exists in the corpus. |
| **PubMed plugin** (`search_articles`, `get_article_metadata`, `find_related_articles`) | Yes | Primary literature and verified metadata (authors, journal, year, DOI) for the tazemetostat basket (RMC cohort 0/14), the nivolumab plus ipilimumab hyperprogression phase II, MRTX1719/BMS-986504, AMG 193 first-in-human, and the MTAP synthetic-lethality review. Also established the negative result that PubMed indexes no RMC-specific PRMT5/MTAP study. |
| **WebSearch** | Yes | FDA/company/registry confirmation: tazemetostat 2020 approvals AND the March 2026 Ipsen voluntary market withdrawal; MRTX1719 = BMS-986504 = navlimetostat identity and active NCTs; AMG 193 program; the RMC MTAP/CDKN2A 9p21 context. |
| **WebFetch** | Yes | Read the Ipsen press release directly to confirm the withdrawal date (March 9, 2026), the SYMPHONY-1 confirmatory trial, and the secondary-hematologic-malignancy safety signal. |
| **Cortellis** (`mcp__plugin_cortellis_Cortellis__authenticate`) | **No, required interactive OAuth I could not complete in this session** | Attempted authentication; the server returned an OAuth authorization URL requiring the user to authorize in a browser and paste back a localhost callback URL. That interactive handshake could not be completed non-interactively. **No Cortellis pipeline data is used or fabricated.** The development pipeline snapshot in Section (e) is therefore built from PubMed, ClinicalTrials.gov, FDA, and company sources and is labeled as such. |

---

## (b) SMARCB1 to EZH2 dependency (Consensus + full text), with the honest negative RMC signal

**Mechanism (Consensus + PubMed).** The BAF (SWI/SNF) complex and the EZH2-containing PRC2 complex act antagonistically on chromatin. Loss of SWI/SNF function (here, biallelic SMARCB1 loss) tilts the balance toward EZH2-mediated H3K27me3 repression, producing an oncogenic dependence on EZH2 enzymatic activity. Consensus surfaced the founding preclinical proof in the rhabdoid family: a selective EZH2 inhibitor induced apoptosis and differentiation specifically in SMARCB1-deleted MRT cells and drove durable, dose-dependent tumor regression in xenografts, establishing the SMARCB1-loss to EZH2-dependency axis (Knutson et al., *PNAS* 2013, PMID 23620515, [DOI](https://doi.org/10.1073/pnas.1303800110)). A 2023 review Consensus returned frames the clinical reality: EZH2 targeting is a druggable vulnerability across SMARCB1-deficient soft-tissue sarcomas, but responses to EZH2 inhibitors are variable, robust in epithelioid sarcoma yet modest and sporadic in extrarenal MRT and synovial sarcoma, motivating combination strategies (Lanzi et al., *Biochem Pharmacol* 2023, PMID 37339681, [DOI](https://doi.org/10.1016/j.bcp.2023.115727)).

**RMC-specific EZH2 evidence, graded honestly (PubMed + Consensus).** RMC patient-derived lines (UOK353, UOK360) overexpress EZH2 and other PRC2 members, and EZH2 inhibition reduced RMC spheroid viability, giving a preclinical rationale (Wei et al., *Genes Chromosomes Cancer* 2020, PMID 32259323, [DOI](https://doi.org/10.1002/gcc.22847)). **However, the clinical signal in RMC is negative.** The dedicated tazemetostat phase II basket study in SWI/SNF-altered solid tumors enrolled a renal medullary carcinoma cohort (Cohort 4, n=14) that had a **0% objective response rate** and did not meet its efficacy threshold; responses were confined to malignant rhabdoid tumors (9%), INI1-negative tumors (9%), and poorly differentiated chordoma (6%). The authors conclude combination strategies are needed when EZH2 signaling is not the sole driver (Gounder et al., *Nat Commun* 2026, PMID 41882006, [DOI](https://doi.org/10.1038/s41467-026-69708-2)). Consistent with a disease-stabilizing rather than cytoreductive effect, NCI-COG Pediatric MATCH (APEC1621C) recorded one RMC patient with a best response of stable disease among a cohort that overall did not meet its primary endpoint (objective response rate 5%), though 25% of patients across diagnoses had prolonged stable disease (Chi et al., *J Natl Cancer Inst* 2023, PMID 37228094, [DOI](https://doi.org/10.1093/jnci/djad085); returned by Consensus as its top hit for this axis).

**Safety-plasticity caveat (Paperclip/PubMed).** A cautionary case documented glial transdifferentiation in an RMC brain metastasis after tazemetostat, suggesting that EZH2/epigenetic modulation can unmask lineage plasticity (Gubbiotti et al., *Acta Neuropathol Commun* 2025, PMID 39833894, [DOI](https://doi.org/10.1186/s40478-025-01929-w)).

**Verdict.** Strong mechanistic rationale, negative single-agent RMC clinical signal. EZH2 inhibition in RMC is a combination-only proposition, not a standalone therapy.

---

## (c) PRMT5 / MTAP synthetic lethality: an emerging cross-cancer angle (Consensus + Paperclip + PubMed + WebSearch)

**The general synthetic-lethality principle (Consensus + PubMed).** Homozygous MTAP deletion occurs in roughly 10% to 15% of solid tumors (up to ~45% in some types). MTAP loss causes accumulation of methylthioadenosine (MTA), which outcompetes S-adenosylmethionine (SAM) at PRMT5, partially inhibiting PRMT5 and rendering the cell hypersensitive to further PRMT5 blockade. First-generation PRMT5 inhibitors failed clinically from dose-limiting hematologic toxicity because they blocked PRMT5 indiscriminately; the second-generation **MTA-cooperative** inhibitors selectively kill MTAP-deleted cells while sparing MTAP-wild-type hematopoiesis (Rodon et al., *Cancer Res* 2026, PMID 41512197, [DOI](https://doi.org/10.1158/0008-5472.CAN-25-2126); Li et al., *J Med Chem* 2025, returned by Consensus). The lead MTA-cooperative agent MRTX1719 shows >70-fold selectivity for MTAP-deleted over MTAP-wild-type isogenic cells and produced objective responses in MTAP-deleted melanoma, gallbladder, mesothelioma, NSCLC, and MPNST in phase I/II (Engstrom et al., *Cancer Discov* 2023, PMID 37552839, [DOI](https://doi.org/10.1158/2159-8290.CD-23-0669)).

**Why this is an RMC angle at all (the SWI/SNF-loss to PRMT5 bridge).** There are two distinct routes to a PRMT5 dependency, and RMC is a candidate for the second:
1. **MTAP-deletion route (biomarker-defined).** Applies to any tumor with 9p21 MTAP co-deletion. WebSearch confirmed MTAP is co-deleted with CDKN2A on 9p21 in roughly 80% to 90% of CDKN2A-deleted tumors, and that 9p21/MTAP loss associates with a cold immune microenvironment and checkpoint resistance across cancers (Frontiers in Immunology 2022 RCC MTAP/CDKN2A analysis; general 9p21 literature via WebSearch).
2. **SWI/SNF-loss chromatin route (lineage-defined).** SMARCB1-deficient rhabdoid-family tumors are broadly dependent on chromatin-regulatory cofactors that maintain the oncogenic epigenome (for example PHF6 cooperating with residual SWI/SNF, surfaced by Paperclip; Mittal et al., PMC11344777). PRMT5 is a plausible node in this network because it deposits symmetric dimethylarginine marks that intersect with PRC2/EZH2 and splicing programs that SMARCB1-deficient cells rely on. A Paperclip preprint shows PRMT5 is frequently upregulated and targetable in another aggressive MTAP-deficient tumor family, malignant peripheral nerve sheath tumors (Wang et al., bioRxiv 2026, [DOI](https://doi.org/10.64898/2026.03.09.710638)), establishing the template but not the RMC data point.

**Honest status for RMC (PubMed + Paperclip negative result).** **There is no published RMC-specific PRMT5 dependency or RMC MTAP-deletion-frequency dataset.** PubMed returned zero RMC-specific PRMT5/MTAP synthetic-lethality records, and the Paperclip corpus contains no RMC PRMT5 study. Therefore the RMC-specific magnitude of any PRMT5 dependency, and the true prevalence of MTAP co-deletion in RMC, are both **UNVERIFIED**. This axis is presented as an emerging, testable hypothesis (Section f), grounded in the cross-cancer MTA-cooperative PRMT5 field and the shared SWI/SNF-loss chromatin biology, not as an established RMC dependency.

**Development stage of the class (Cortellis unavailable, so PubMed/registry/WebSearch, clearly labeled).** MTA-cooperative PRMT5 inhibitors are in active clinical development but none has an RMC indication:
- **MRTX1719 / BMS-986504 / navlimetostat** (Mirati, now Bristol Myers Squibb): phase I established antitumor activity in MTAP-deleted tumors (PMID 37552839, [DOI](https://doi.org/10.1158/2159-8290.CD-23-0669)); WebSearch confirmed durable responses in MTAP-deleted NSCLC reported at WCLC 2025 and multiple active combination trials (with olaparib NCT07382544; with pembrolizumab plus chemotherapy in first-line MTAP-deleted NSCLC NCT07063745; with pemetrexed NCT07594626; mass-balance NCT06672523; monotherapy NCT05245500).
- **AMG 193** (Amgen): CNS-penetrant MTA-cooperative PRMT5 inhibitor; first-in-human phase I (n=80 dose exploration) reached MTD 1200 mg once daily with **objective response rate 21.4%** across MTAP-deleted solid tumors and no clinically significant myelosuppression (Rodon et al., *Ann Oncol* 2024, PMID 39293516, [DOI](https://doi.org/10.1016/j.annonc.2024.08.2339)).
- **TNG908** (Tango): brain-penetrant MTA-cooperative PRMT5 inhibitor developed for histology-agnostic use in MTAP-deleted cancers (Paperclip full text, PMC11832951; Cottrell et al., PMC11056935).
- **IDE397** (IDEAYA): a MAT2A inhibitor that starves PRMT5 of SAM, an orthogonal way to exploit the same node (per the Rodon *Cancer Res* 2026 review, PMID 41512197).

---

## (d) Proteasome inhibition and checkpoint blockade

### Proteasome inhibition (Paperclip full text + Consensus + PubMed): the strongest mechanism-informed RMC lead

**Genetic proof of a UPS synthetic lethality (Paperclip full text of Hong 2019 eLife).** Reading the full text rather than the abstract, the Hong et al. study built faithful patient-derived RMC models and, by integrating RNAi, CRISPR-Cas9, and small-molecule screens, found the ubiquitin-proteasome system (UPS) is a core, selective dependency of SMARCB1-deficient cancers. Specific full-text findings:
- Nineteen genes scored across all three orthogonal screens in two RMC sublines, including proteasome subunits PSMB1, PSMB2, PSMB5, PSMD1, PSMD2, and CUL1 (Hong et al., *eLife* 2019, [DOI](https://doi.org/10.7554/eLife.44161)).
- SMARCB1-deficient cells were selectively sensitive to bortezomib and to the oral proteasome inhibitor MLN2238 (ixazomib); re-expression of SMARCB1 shifted the dose-response 2 to 3 fold rightward, confirming the dependency is driven by SMARCB1 loss.
- Across the Cancer Cell Line Encyclopedia, SMARCB1-deficient lines were as sensitive to MLN2238 as multiple myeloma lines (two-tailed t-test p=0.011), the canonical proteasome-inhibitor-sensitive disease.
- Mechanistically, proteasome inhibition caused a G2/M arrest from inappropriate accumulation of cyclin B1, and the lines were dependent on the E2 ubiquitin-conjugating enzyme UBE2C (SMARCB1-deficient lines sat in the top 5% of UBE2C-dependent lines in Project Achilles). In vivo, MLN2238 at 7 mg/kg twice weekly induced significant tumor stabilization/regression and prolonged survival in a SMARCB1-deficient xenograft.

The authors explicitly frame this as the foundation for a mechanism-informed clinical trial of proteasome inhibitors in RMC. Consensus independently confirmed the bortezomib mechanism base (proteasome/NF-kB/NOXA/ROS; Sogbein et al., *Life Sci* 2024, PMID 38431182, [DOI](https://doi.org/10.1016/j.lfs.2024.122612)).

**Clinical anchor (PubMed).** Two pediatric patients with metastatic RMC treated with platinum-based chemotherapy plus bortezomib achieved complete responses, one alive at 7 years and one disease-free near 2 years (Carden et al., *Pediatr Blood Cancer* 2017, PMID 28052556, [DOI](https://doi.org/10.1002/pbc.26402)), consistent with the extraordinary-responder cases cited inside the Hong full text.

**Verdict.** The proteasome/UPS is the best-substantiated RMC-specific vulnerability of the four axes: orthogonal genetic proof, isogenic rescue, in vivo efficacy, plus durable human complete responses on a platinum backbone.

### Checkpoint blockade (WebSearch + PubMed): inflamed but clinically harmful as combination ICB

RMC carries an inflamed, cGAS-STING-activated phenotype from its focal copy-number instability, which historically suggested checkpoint benefit. The clinical data refute single-agent and dual checkpoint blockade, and the newest evidence shows active harm:
- **Single-agent pembrolizumab (PubMed).** The first prospective phase II (NCT02721732, n=5) showed no activity; all patients progressed rapidly regardless of PD-L1 or tumor-infiltrating-lymphocyte levels (Nze et al., *Cancers* 2023, PMID 37568622, [DOI](https://doi.org/10.3390/cancers15153806)).
- **Nivolumab plus ipilimumab induces hyperprogression (WebSearch discovery, PubMed-verified, new).** A phase II trial (NCT03274258, n=10) of nivolumab plus ipilimumab was halted for futility: **0% objective response rate, 5 of 10 patients met radiologic criteria for hyperprogression, and median progression-free survival was 1.38 months.** Post-hoc single-cell RNA sequencing showed checkpoint therapy triggered an interferon-gamma response that induced a "myeloid mimicry" program in tumor cells via the CEBPB/p300 axis, linked to proliferation and hyperprogression; in an immunocompetent RMC mouse model, combination checkpoint therapy accelerated growth, and pharmacologic p300 inhibition suppressed the program and restored sensitivity (Soeung et al., *Nat Commun* 2025, PMID 41290625, [DOI](https://doi.org/10.1038/s41467-025-65462-z)).

**Verdict.** Do not give single-agent or dual checkpoint blockade to RMC as a standalone strategy; the dual-checkpoint data show a real risk of accelerating the cancer. The mechanistic silver lining is a druggable resistance node (CEBPB/p300 myeloid mimicry), which feeds Hypothesis 3 below. Because RMC is microsatellite stable with low tumor mutational burden, the tissue-agnostic MSI-H (2017) and TMB-high (2020) pembrolizumab labels do not apply.

---

## (e) Development pipeline snapshot of relevant targeted assets

**Provenance label.** Cortellis was **not reachable** (interactive OAuth could not be completed in this session; see Section a). This snapshot is therefore compiled entirely from **PubMed, ClinicalTrials.gov, FDA, and company press releases via WebSearch/WebFetch**, and is labeled as such. No proprietary drug-intelligence pipeline data are used or invented.

| Asset (target) | Class | Stage / status | RMC relevance | Source (tool) |
|---|---|---|---|---|
| **Tazemetostat** (EZH2) | First-in-class EZH2 inhibitor | FDA accelerated approvals Jan 2020 (INI1/SMARCB1-negative epithelioid sarcoma) and Jun 2020 (EZH2-mutant R/R follicular lymphoma). **VOLUNTARILY WITHDRAWN from all markets by Ipsen, effective March 9, 2026**, after the SYMPHONY-1 confirmatory trial flagged secondary hematologic malignancies (risk may outweigh benefit). | RMC basket cohort was 0/14 responders; the drug is now off-market for its prior indications. Any future RMC use would be trial-based and combination-focused. | WebSearch + WebFetch (Ipsen press release, OncLive, Pharmacy Times); PubMed (PMID 33035459, 41882006) |
| **MRTX1719 / BMS-986504 / navlimetostat** (PRMT5, MTA-cooperative) | Second-gen synthetic-lethal PRMT5i | Phase I complete with responses in MTAP-deleted tumors; multiple active phase Ib/II combinations (olaparib NCT07382544; pembrolizumab plus chemo NCT07063745; pemetrexed NCT07594626; monotherapy NCT05245500). No RMC cohort. | Emerging class for MTAP-deleted and, hypothetically, SWI/SNF-loss tumors. **RMC not enrolled; RMC MTAP frequency UNVERIFIED.** | PubMed (PMID 37552839); WebSearch (NCTs, WCLC 2025) |
| **AMG 193** (PRMT5, MTA-cooperative, CNS-penetrant) | Second-gen synthetic-lethal PRMT5i | First-in-human phase I n=80; MTD 1200 mg once daily; ORR 21.4% in MTAP-deleted solid tumors; no significant myelosuppression; phase I/II expansions ongoing. | Same emerging class; brain penetration is notable given RMC's rare CNS spread. No RMC data. | PubMed (PMID 39293516); WebSearch (OncLive, Ann Oncol) |
| **TNG908** (PRMT5, MTA-cooperative, brain-penetrant) | Second-gen synthetic-lethal PRMT5i | Clinical development for MTAP-deleted cancers (histology-agnostic). | Emerging class; no RMC data. | Paperclip full text (PMC11832951, PMC11056935) |
| **IDE397** (MAT2A) | SAM-depletion (orthogonal PRMT5 axis) | Clinical development for MTAP-deleted cancers. | Orthogonal way to hit the PRMT5 node; no RMC data. | PubMed review (PMID 41512197) |
| **Bortezomib / ixazomib (MLN2238)** (26S proteasome) | Proteasome inhibitors (from multiple myeloma) | Approved in myeloma/mantle cell lymphoma; repurposing rationale in SMARCB1-deficient cancers with preclinical and case-level RMC support. | Best mechanism-informed RMC lead; durable pediatric complete responses with platinum. | Paperclip full text (eLife 2019); PubMed (PMID 28052556) |
| **p300/CBP inhibitors** (e.g., CCS1477/inobrodib class) | Bromodomain/HAT inhibitors | Clinical development in other cancers (not RMC-specific). | Newly nominated RMC resistance node (CEBPB/p300 myeloid mimicry driving checkpoint hyperprogression). RMC use is preclinical only. | PubMed (PMID 41290625) |

---

## (f) Novel, testable cross-cancer hypotheses

**Hypothesis 1 (proteasome + EZH2 combination, or proteasome + platinum, as the RMC backbone).** Because single-agent EZH2 inhibition failed in the RMC basket (0/14) while the UPS is a proven orthogonal SMARCB1-loss dependency with human complete responses, EZH2 inhibition is likely useful only as a sensitizer. **Testable prediction:** in SMARCB1-deficient RMC models, an EZH2 inhibitor plus a proteasome inhibitor (or a proteasome inhibitor added to platinum) produces greater-than-additive cytotoxicity and G2/M arrest than either agent alone, because EZH2 blockade relieves PRC2-mediated repression of pro-apoptotic and cell-cycle-checkpoint genes while proteasome inhibition drives the cyclin-B1/UBE2C-dependent mitotic catastrophe. Anchors: EZH2 basket negative and combination call (PMID 41882006, [DOI](https://doi.org/10.1038/s41467-026-69708-2)); UPS/UBE2C/cyclin-B1 dependency (Hong *eLife* 2019, [DOI](https://doi.org/10.7554/eLife.44161)); durable platinum-plus-bortezomib responses (PMID 28052556, [DOI](https://doi.org/10.1002/pbc.26402)).

**Hypothesis 2 (MTA-cooperative PRMT5 inhibition as a rhabdoid-family, not just MTAP-defined, strategy).** If SMARCB1-deficient RMC cells rely on PRMT5-dependent symmetric-arginine methylation to maintain the residual SWI/SNF/PRC2 oncogenic epigenome and splicing fidelity, they may be sensitive to PRMT5 inhibition even without MTAP co-deletion, and clearly sensitive if MTAP is co-deleted. **Testable predictions, in order of stringency:** (i) profile MTAP status across an RMC cohort to establish the co-deletion frequency (currently **UNVERIFIED**); (ii) in MTAP-deleted RMC lines, MTA-cooperative PRMT5 inhibitors (MRTX1719-class, AMG 193, TNG908) reduce viability and clear symmetric dimethylarginine marks selectively versus MTAP-wild-type controls; (iii) in MTAP-intact SMARCB1-deficient RMC lines, PRMT5 inhibition still suppresses growth if the dependency is chromatin-driven rather than MTA-driven. Anchors: MTA-cooperative PRMT5 synthetic lethality (Engstrom *Cancer Discov* 2023, [DOI](https://doi.org/10.1158/2159-8290.CD-23-0669); Rodon *Ann Oncol* 2024, [DOI](https://doi.org/10.1016/j.annonc.2024.08.2339); Rodon *Cancer Res* 2026, [DOI](https://doi.org/10.1158/0008-5472.CAN-25-2126)); PRMT5 targetability in another MTAP-deficient tumor family (Wang bioRxiv 2026, [DOI](https://doi.org/10.64898/2026.03.09.710638)).

**Hypothesis 3 (p300/CEBPB inhibition rescues checkpoint blockade in RMC).** Dual checkpoint blockade paradoxically accelerated RMC via an interferon-gamma-driven CEBPB/p300 "myeloid mimicry" program, and p300 inhibition restored checkpoint sensitivity in mice. **Testable prediction:** sequencing or combining a p300/CBP inhibitor with checkpoint blockade in RMC models converts hyperprogression into disease control by blocking the CEBPB/p300 transcriptional circuit, whereas checkpoint blockade alone or p300 inhibition alone does not. This reframes checkpoint therapy in RMC from contraindicated-as-monotherapy to conditionally-usable-with-a-p300-partner. Anchor: Soeung/Msaouel/Genovese *Nat Commun* 2025 (PMID 41290625, [DOI](https://doi.org/10.1038/s41467-025-65462-z)).

---

## (g) Sources

According to PubMed, DOIs are provided as links per attribution requirements. Consensus results are attributed inline in the relevant sections. WebSearch/WebFetch and ClinicalTrials.gov sources are listed with URLs.

**EZH2 axis (Consensus + PubMed + Paperclip):**
1. Knutson et al. Durable tumor regression in genetically altered MRT by EZH2 inhibition. *PNAS* 2013. PMID 23620515. [DOI](https://doi.org/10.1073/pnas.1303800110) (Consensus)
2. Lanzi et al. Targeting EZH2 in SMARCB1-deficient sarcomas. *Biochem Pharmacol* 2023. PMID 37339681. [DOI](https://doi.org/10.1016/j.bcp.2023.115727) (Consensus)
3. Wei et al. RMC cell lines UOK353/UOK360 (EZH2 + bortezomib preclinical). *Genes Chromosomes Cancer* 2020. PMID 32259323. [DOI](https://doi.org/10.1002/gcc.22847) (PubMed)
4. Gounder et al. Tazemetostat in SWI/SNF-altered solid tumors: phase II basket (RMC cohort 4, 0/14 ORR). *Nat Commun* 2026. PMID 41882006. [DOI](https://doi.org/10.1038/s41467-026-69708-2) (PubMed)
5. Chi et al. Tazemetostat for SMARCB1/SMARCA4 or EZH2 alterations (NCI-COG Pediatric MATCH APEC1621C; RMC stable disease). *J Natl Cancer Inst* 2023. PMID 37228094. [DOI](https://doi.org/10.1093/jnci/djad085) (Consensus + PubMed)
6. Gubbiotti et al. Glial transdifferentiation in RMC brain metastasis after tazemetostat. *Acta Neuropathol Commun* 2025. PMID 39833894. [DOI](https://doi.org/10.1186/s40478-025-01929-w) (Paperclip + PubMed)
7. Gounder et al. Tazemetostat in advanced epithelioid sarcoma with INI1/SMARCB1 loss. *Lancet Oncol* 2020. PMID 33035459. [DOI](https://doi.org/10.1016/S1470-2045(20)30451-4) (PubMed)

**PRMT5 / MTAP axis (Consensus + Paperclip + PubMed + WebSearch):**
8. Engstrom et al. MRTX1719 MTA-cooperative PRMT5 inhibitor, synthetic lethality in MTAP-deleted cancer. *Cancer Discov* 2023. PMID 37552839. [DOI](https://doi.org/10.1158/2159-8290.CD-23-0669) (Consensus + PubMed)
9. Rodon et al. First-in-human AMG 193 in MTAP-deleted solid tumors (phase I). *Ann Oncol* 2024. PMID 39293516. [DOI](https://doi.org/10.1016/j.annonc.2024.08.2339) (PubMed + WebSearch)
10. Rodon et al. MTAP Deletion in Oncogenesis: A Synthetic Lethality Scenario (review). *Cancer Res* 2026. PMID 41512197. [DOI](https://doi.org/10.1158/0008-5472.CAN-25-2126) (Consensus + PubMed)
11. Wang et al. PRMT5 frequently upregulated and targetable in MTAP-deficient MPNST (preprint). *bioRxiv* 2026. [DOI](https://doi.org/10.64898/2026.03.09.710638) (Paperclip)
12. Cottrell et al. Discovery of TNG908, brain-penetrant MTA-cooperative PRMT5 inhibitor. PMC11056935 (Paperclip)
13. Briggs et al. TNG908 brain-penetrant MTA-cooperative PRMT5 inhibitor for MTAP-deleted cancers. PMC11832951 (Paperclip)
14. Mittal et al. PHF6 cooperates with SWI/SNF in SMARCB1-deficient rhabdoid tumors. PMC11344777 (Paperclip)

**Proteasome axis (Paperclip full text + Consensus + PubMed):**
15. Hong et al. Renal medullary carcinomas depend upon SMARCB1 loss and are sensitive to proteasome inhibition. *eLife* 2019. [DOI](https://doi.org/10.7554/eLife.44161) (Paperclip full text; PMC6436895)
16. Carden et al. Platinum plus bortezomib for pediatric RMC: two cases (complete responses). *Pediatr Blood Cancer* 2017. PMID 28052556. [DOI](https://doi.org/10.1002/pbc.26402) (PubMed)
17. Sogbein et al. Bortezomib in cancer therapy: mechanisms, side effects, future proteasome inhibitors. *Life Sci* 2024. PMID 38431182. [DOI](https://doi.org/10.1016/j.lfs.2024.122612) (Consensus)

**Checkpoint axis (WebSearch + PubMed):**
18. Soeung et al. Nivolumab plus ipilimumab induce hyper-progression in RMC (phase II NCT03274258 + preclinical; CEBPB/p300 myeloid mimicry). *Nat Commun* 2025. PMID 41290625. [DOI](https://doi.org/10.1038/s41467-025-65462-z) (WebSearch discovery + PubMed)
19. Nze et al. Phase II pembrolizumab in advanced RMC (negative; NCT02721732). *Cancers* 2023. PMID 37568622. [DOI](https://doi.org/10.3390/cancers15153806) (PubMed + Paperclip)

**Pipeline / regulatory (WebSearch + WebFetch + registry):**
20. Ipsen. Update: Ipsen voluntarily withdraws Tazverik (tazemetostat) in follicular lymphoma and epithelioid sarcoma (March 9, 2026; SYMPHONY-1 secondary hematologic malignancy signal). https://www.ipsen.com/press-release/update-ipsen-voluntarily-withdraws-tazverik-tazemetostat-in-follicular-lymphoma-and-epithelioid-sarcoma-3252192/ (WebFetch)
21. OncLive. FDA Indications for Tazemetostat in R/R FL and ES Are Voluntarily Withdrawn. https://www.onclive.com/view/fda-indications-for-tazemetostat-in-r-r-follicular-lymphoma-and-epithelioid-sarcoma-are-voluntarily-withdrawn (WebSearch)
22. FDA. FDA granted accelerated approval to tazemetostat for follicular lymphoma. https://www.fda.gov/drugs/fda-granted-accelerated-approval-tazemetostat-follicular-lymphoma (WebSearch)

**Relevant ClinicalTrials.gov identifiers (registry via WebSearch):**
- NCT02601950 (tazemetostat SWI/SNF-altered basket; RMC Cohort 4): https://clinicaltrials.gov/study/NCT02601950
- NCT02721732 (pembrolizumab in RMC; negative): https://clinicaltrials.gov/study/NCT02721732
- NCT03274258 (nivolumab plus ipilimumab in RMC; hyperprogression): https://clinicaltrials.gov/study/NCT03274258
- NCT05245500 (MRTX1719/BMS-986504 monotherapy, MTAP-deleted): https://clinicaltrials.gov/study/NCT05245500
- NCT07382544 (BMS-986504 plus olaparib, MTAP loss): https://clinicaltrials.gov/study/NCT07382544
- NCT07063745 (BMS-986504 plus pembrolizumab plus chemo, MTAP-deleted NSCLC): https://clinicaltrials.gov/study/NCT07063745
- NCT07594626 (BMS-986504 plus pemetrexed, MTAP-deleted): https://clinicaltrials.gov/study/NCT07594626
- NCT06672523 (BMS-986504 mass balance, MTAP-deleted): https://clinicaltrials.gov/study/NCT06672523

---

## Tool reachability note (explicit, as required)

**Reachable and used in this analysis:** Consensus, Paperclip (full text and preprints), PubMed plugin (search, metadata, and negative-result confirmation), WebSearch, and WebFetch.

**Not reachable:** **Cortellis** (`mcp__plugin_cortellis_Cortellis`). Authentication was attempted and returned an OAuth authorization URL requiring the user to authorize in a browser and paste back a localhost callback URL. That interactive handshake could not be completed non-interactively in this session, so no Cortellis drug-intelligence data were retrieved. Per the task rules, the development pipeline snapshot (Section e) falls back to PubMed, ClinicalTrials.gov, FDA, and company sources, and is labeled accordingly. **No Cortellis-sourced facts are stated or fabricated anywhere in this document.** If the user completes the Cortellis OAuth flow (authorize URL provided in chat, then paste the localhost callback URL), the pipeline snapshot can be enriched with formal development-stage and competitive-landscape records.

**UNVERIFIED items flagged in text:** (1) the prevalence of MTAP co-deletion in RMC specifically; (2) the existence and magnitude of an RMC-specific PRMT5 dependency (no published RMC PRMT5 dataset found in PubMed or Paperclip). Both are framed as testable hypotheses, not established facts.

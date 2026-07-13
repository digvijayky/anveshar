# Anveshar fact-check — Batch 1

Independent adversarial verification of every therapy, precedent, and trial citation in five example dossiers. Each PMID resolved via the PubMed plugin; each NCT resolved via the ClinicalTrials.gov v2 API; DOI-only citations resolved via PubMed/DOI. Findings below.

Status legend: VERIFIED (exists + title/topic/claim match) · MISMATCH (resolves to a different or nonexistent record than cited) · OVERSTATED · UNRESOLVED · FABRICATED.

## Overall verdicts

| File | Verdict | Items checked | VERIFIED | Flagged |
|---|---|---|---|---|
| rectal_net.json | CLEAN | 25 | 25 | 0 |
| renal_medullary.json | CLEAN | 20 | 20 | 0 |
| chordoma.json | CLEAN | 15 | 15 | 0 |
| adenoid_cystic_carcinoma.json | ISSUES (1) | 24 | 23 | 1 |
| alveolar_soft_part_sarcoma.json | CLEAN | 16 | 16 | 0 |

Non-VERIFIED items: 1 total (ACC lenvatinib trial NCT — wrong/nonexistent NCT number).

---

## rectal_net.json

| Item | Citation | Status | Note |
|---|---|---|---|
| Pembrolizumab MSI-H/dMMR (KEYNOTE-158) | PMID 31682550 | VERIFIED | KEYNOTE-158 noncolorectal MSI-H/dMMR pembrolizumab, J Clin Oncol. |
| Pembrolizumab TMB-high (KEYNOTE-158 TMB) | PMID 32919526 | VERIFIED | KEYNOTE-158 TMB biomarker analysis, Lancet Oncol. |
| Dostarlimab dMMR (GARNET) | PMID 37917058 | VERIFIED | Dostarlimab monotherapy in dMMR solid tumors (GARNET), JAMA Netw Open. |
| Larotrectinib NTRK (pooled) | PMID 32105622 | VERIFIED | Larotrectinib TRK-fusion pooled analysis, Lancet Oncol. |
| Entrectinib NTRK (integrated) | PMID 31838007 | VERIFIED | Entrectinib NTRK integrated analysis, Lancet Oncol. |
| Dabrafenib+trametinib BRAF V600E (ROAR) | PMID 32818466 | VERIFIED | ROAR biliary basket, Lancet Oncol. |
| Selpercatinib RET (LIBRETTO-001) | PMID 36108661 | VERIFIED | Selpercatinib tumor-agnostic RET, Lancet Oncol. |
| Trastuzumab deruxtecan HER2 3+ (DESTINY-PanTumor02) | PMID 37870536 | VERIFIED | T-DXd HER2-expressing solid tumors, J Clin Oncol. |
| Tarlatamab DLL3 (DeLLphi-301) | PMID 37861218 | VERIFIED | Tarlatamab SCLC, NEJM; abstract confirms ORR 40% (10-mg arm) — claim not overstated. |
| Nivolumab+ipilimumab (DART SWOG 1609) | PMID 31969335 | VERIFIED | DART nonpancreatic NET basket, Clin Cancer Res. |
| Platinum+etoposide (NORDIC NEC) | PMID 22967994 | VERIFIED | NORDIC NEC study, Ann Oncol. |
| Precedent MSI-H 2017 | PMID 31682550 | VERIFIED | Same as above. |
| Precedent NTRK larotrectinib 2018 | PMID 32105622 | VERIFIED | Same as above. |
| Precedent NTRK entrectinib 2019 | PMID 31838007 | VERIFIED | Same as above. |
| Precedent TMB 2020 | PMID 32919526 | VERIFIED | Same as above. |
| Precedent dMMR dostarlimab 2021 | PMID 37917058 | VERIFIED | Same as above. |
| Precedent BRAF 2022 | PMID 32818466 | VERIFIED | Same as above. |
| Precedent RET 2022 | PMID 36108661 | VERIFIED | Same as above. |
| Precedent HER2 2024 | PMID 37870536 | VERIFIED | Same as above. |
| Trial: Tarlatamab vs chemo P3 NEC | NCT06937905 | VERIFIED | Tarlatamab vs SoC chemo, pulmonary/GEP poorly-diff NEC, Phase 3, recruiting. |
| Trial: Tarlatamab extrapulmonary NEC P2 | NCT06893783 | VERIFIED | Tarlatamab advanced extrapulmonary NEC, Phase 2, recruiting. |
| Trial: Peluntamig PT217 SKYBRIDGE | NCT05652686 | VERIFIED | Peluntamig (PT217), DLL3, GEP-NEC, Phase 1/2, recruiting. |
| Trial: Obrixtamig BI 764532 uptake | NCT05963867 | VERIFIED | BI 764532 uptake study SCLC/NEN, Phase 1. |
| Trial: G3 GEP/CUP NEC chemo | NCT04325425 | VERIFIED | FOLFOXIRI/cisplatin metastatic G3 GEP/CUP NEC, Phase 2. |
| Trial: Lenvatinib+pembro G3 NET | NCT05746208 | VERIFIED | Lenvatinib+pembrolizumab well-diff G3 NET, Phase 2. |
| Trial: Entrectinib basket | NCT02568267 | VERIFIED | Entrectinib NTRK/ROS1/ALK basket, includes NET, Phase 2. |

Driver claim (NET = MEN1/DAXX/ATRX/mTOR, retained SSTR2; NEC = TP53/RB1, SCLC-like): consistent with primary literature (Msaouel/standard NEN genomics; NORDIC NEC). Sound.

Caveat (not a citation flag): the in-text prevalence attribution "Venizelos n=36" (DLL3 rectal-specific) has no citation object and could not be independently surfaced in PubMed; DLL3 prevalence figures quoted are plausible but that specific attribution is unverifiable.

## renal_medullary.json

| Item | Citation | Status | Note |
|---|---|---|---|
| SMARCB1→EZH2 dependency (Wei 2020) | PMID 32259323 | VERIFIED | UOK353/UOK360 RMC cell lines, EZH2, Genes Chromosomes Cancer. |
| SWI/SNF→PRC2/EZH2 (Chan-Penebre 2017) | PMID 28292935 | VERIFIED | EZH2 inhibition in SMARCA2/4-deficient SCCOHT (rhabdoid-family SWI/SNF-deficient), Mol Cancer Ther. Supports the stated EZH2-dependency-across-rhabdoid-family claim (tumor type is SCCOHT, not epithelioid sarcoma). |
| MYC replication stress/DDR (Msaouel 2020) | PMID 32359397 | VERIFIED | RMC molecular characterization: replication stress, cGAS-STING, DDR vulnerability, MSS/low TMB, Cancer Cell. |
| Bortezomib+platinum, 2 pediatric CR (Carden 2017) | PMID 28052556 | VERIFIED | Platinum+bortezomib, 2 pediatric RMC complete responses, one alive 7 yr — matches claim exactly, Pediatr Blood Cancer. |
| cGAS-STING / negative single-agent PD-1 (Nze 2023) | PMID 37568622 / DOI 10.3390/cancers15153806 | VERIFIED | Phase II pembrolizumab RMC, 5 patients, all progressed, negative — matches "0 responses in 5." |
| Tazemetostat SWI/SNF basket, RMC cohort 0/14 (Gounder Nat Commun 2026) | DOI 10.1038/s41467-026-69708-2 / PMID 41882006 | VERIFIED | Real: Gounder et al., Nat Commun 2026, phase II tazemetostat SWI/SNF basket (NCT02601950). Confirms RMC cohort n=14, 0% ORR. |
| DDR/ATR-PARP rationale (Msaouel 2020) | DOI 10.1016/j.ccell.2020.04.002 / PMID 32359397 | VERIFIED | Same paper as above. |
| Precedent tazemetostat epithelioid sarcoma (Gounder Lancet Oncol 2020) | DOI 10.1016/S1470-2045(20)30451-4 / PMID 33035459 | VERIFIED | Tazemetostat INI1-negative epithelioid sarcoma phase 2 basket, Lancet Oncol. |
| Precedent KEYNOTE-158 MSI-H update (Maio/Marabelle 2022) | DOI 10.1016/j.annonc.2022.05.519 / PMID 35680043 | VERIFIED | First author Maio, last author Marabelle; KEYNOTE-158 MSI-H/dMMR update, Ann Oncol. Authorship label correct. |
| Precedent RMC MSS/low TMB (Msaouel 2020) | DOI 10.1016/j.ccell.2020.04.002 | VERIFIED | Same Cancer Cell paper. |
| Precedent larotrectinib TRK (Hong 2020) | DOI 10.1016/S1470-2045(19)30856-3 / PMID 32105622 | VERIFIED | Hong et al. larotrectinib pooled TRK-fusion analysis, Lancet Oncol (same PMID as rectal_net larotrectinib). |
| Precedent HER2 3+ T-DXd FDA 2024 | fda.gov link | VERIFIED (concept) | Real FDA tissue-agnostic HER2 IHC 3+ accelerated approval (2024); FDA press page, correctly framed as NOT applicable to RMC. |
| Trial: Ubamatamab±cemiplimab SMARCB1-deficient | NCT06444880 | VERIFIED | MUC16xCD3 bispecific ± anti-PD-1, SMARCB1-deficient incl RMC, Phase 2. |
| Trial: Pembro+enfortumab vedotin CDC/RMC | NCT06302569 | VERIFIED | Pembrolizumab + enfortumab vedotin, collecting duct + RMC, Phase 2. |
| Trial: Sacituzumab govitecan±atezo SMART | NCT06161532 | VERIFIED | SG ± atezolizumab, rare GU tumors incl RMC (SMART), Phase 2. |
| Trial: ICONIC cabo+ipi+nivo | NCT03866382 | VERIFIED | Cabozantinib+nivolumab+ipilimumab rare GU cancers (ICONIC), Phase 2. |
| Trial link: tazemetostat basket | NCT02601950 | VERIFIED | Tazemetostat basket incl RMC; matches Gounder 2026 paper. |
| Trial link: pembrolizumab rare tumors | NCT02721732 | VERIFIED | Pembrolizumab rare tumors basket (the Nze RMC pembrolizumab study). |

Driver claim (biallelic SMARCB1/INI1 loss + sickle cell trait, MSS/low TMB, EZH2 dependence): confirmed by Msaouel 2020 (Cancer Cell) and the Gounder 2026 basket. Sound.

## chordoma.json

| Item | Citation | Status | Note |
|---|---|---|---|
| Brachyury CRISPR dependency / super-enhancer (Sharifnia 2019) | PMID 30664779 | VERIFIED | Small-molecule targeting of brachyury addiction in chordoma, Nat Med. |
| Driver landscape / TBXT duplication (Tarpey 2017) | PMID 29026114 | VERIFIED | Driver landscape of sporadic chordoma, Nat Commun. |
| SMARCB1/INI1 loss poorly-diff subset (Feng 2017) | PMID 29050071 | VERIFIED | Poorly-differentiated chordoma with INI1 loss, Chin J Pathol (Zhonghua Bing Li Xue Za Zhi). |
| PI3K/mTOR prognosis (Passeri 2023) | PMID 37029667 | VERIFIED | Mutational landscape skull base/spinal chordomas, prognostic/theranostic markers, J Neurosurg. |
| PDGFRB imatinib (Stacchiotti 2012) | PMID 22331945 | VERIFIED | Phase II imatinib advanced chordoma, J Clin Oncol. |
| EGFR lapatinib (Stacchiotti 2013) | PMID 23559153 | VERIFIED | Phase II lapatinib EGFR-positive chordoma, Ann Oncol. |
| EGFR/RTK activation (Tamborini 2010) | PMID 20164240 | VERIFIED | RTK/downstream pathway analysis in chordomas, Neuro Oncol. |
| CDKN2A/PTEN + palbociclib+rapamycin (Seeling 2023) | PMID 37046638 | VERIFIED | PTEN/p16 deficiency + palbociclib/rapamycin in chordoma, Cancers. |
| Tazemetostat EZH2 (INI1-neg epithelioid sarcoma) | PMID 33035459 | VERIFIED | Tazemetostat epithelioid sarcoma phase 2 basket, Lancet Oncol. |
| Imatinib+everolimus phase 2 (Stacchiotti 2018) | PMID 30216418 | VERIFIED | Imatinib+everolimus progressing advanced chordoma, Cancer (resolves; topic matches phase 2 combination claim). |
| ESMO bone sarcoma guideline (Strauss 2021) | PMID 34500044 | VERIFIED | ESMO-EURACAN-GENTURIS-ERN PaedCan bone sarcoma guideline, Ann Oncol. |
| Precedent Tarpey 2017 | PMID 29026114 | VERIFIED | Same as above. |
| Precedent Sharifnia 2019 | PMID 30664779 | VERIFIED | Same as above. |
| Precedent tazemetostat 2020 | PMID 33035459 | VERIFIED | Same as above. |
| Precedent imatinib 2012 | PMID 22331945 | VERIFIED | Same as above. |

Note: chordoma "trials" array is empty (by design; therapies are off-label/borrowed). No NCTs to check. Discovery section is explicitly labeled hypotheses; citations reuse the verified Sharifnia/Gounder PMIDs.
Driver claim (brachyury TBXT top dependency; SMARCB1 loss in poorly-diff subset): confirmed by Sharifnia 2019 + Tarpey 2017 + Feng 2017. Sound. Independent cross-check: Gounder Nat Commun 2026 basket also reports poorly-diff chordoma cohort (n=18, 6% ORR), consistent with the SMARCB1→EZH2 rationale.

## adenoid_cystic_carcinoma.json

| Item | Citation | Status | Note |
|---|---|---|---|
| MYB-NFIB fusion hallmark (Persson 2012) | PMID 22505352 | VERIFIED | MYB/NFIB copy number/rearrangements in head/neck ACC, Genes Chromosomes Cancer. |
| NOTCH1 mutations aggressive subset (Ferrarotto 2017) | PMID 27870570 | VERIFIED | Activating NOTCH1 defines poor-prognosis ACC subgroup responsive to Notch1 inhibitors, J Clin Oncol (online 2016 / print 2017 — year label fine). |
| ACC-I vs ACC-II molecular profiling (Hanna 2024) | PMID 38416410 | VERIFIED | Molecular profiling + treatment impact ACC type I/II, Clin Cancer Res. |
| MYB undruggable TF (Dang 2017) | PMID 28643779 | VERIFIED | "Drugging the undruggable cancer targets," Nat Rev Cancer. |
| Lenvatinib phase II ACC (Tchekmedyian 2019) | PMID 30939095 | VERIFIED | Phase II lenvatinib progressive R/M ACC, J Clin Oncol. |
| Axitinib randomized phase II (Kang 2021) | PMID 34315722 | VERIFIED | Randomized phase II axitinib vs observation ACC, Clin Cancer Res. |
| Axitinib+avelumab biomarker (Hoff 2026) | PMID 41973043 | VERIFIED | Real: Hoff et al., Clin Cancer Res 2026. Abstract confirms every claim: ACC-I PFS 1.8 mo vs ACC-II 11.4 mo, HR 0.14, NCCN first immunotherapy-based option, 167-gene signature, benefit not tied to PD-L1/TMB. |
| Brontictuzumab anti-NOTCH1 (Ferrarotto 2017) | PMID 27870570 | VERIFIED | Same JCO paper; describes PDX + index-patient PR to NOTCH1 antibody — matches claim. |
| AL101 gamma-secretase inhibitor (Ferrarotto 2022) | PMID 35931701 | VERIFIED | AL101 GSI potent in NOTCH-activated ACC, Cell Death Dis. |
| Precedent MYB-NFIB 2012 | PMID 22505352 | VERIFIED | Same as above. |
| Precedent NOTCH1/brontictuzumab 2017 | PMID 27870570 | VERIFIED | Same as above. |
| Precedent axitinib 2021 | PMID 34315722 | VERIFIED | Same as above. |
| Precedent Dang undruggable TF 2017 | PMID 28643779 | VERIFIED | Same as above. |
| Discovery: NOTCH targeting (Ferrarotto 2017) | PMID 27870570 | VERIFIED | Reuse of verified PMID. |
| Discovery: MYB degradation (Dang 2017) | PMID 28643779 | VERIFIED | Reuse of verified PMID. |
| Discovery: ADC modality (Wagner 2022) | PMID 36427771 | VERIFIED | ACC drug therapy landscape / no FDA-approved drug, Crit Rev Oncol Hematol. |
| Trial: CB-103 pan-NOTCH CALCulus | NCT05774899 | VERIFIED | CB-103 + abemaciclib or lenvatinib, NOTCH ACC, Phase 1/2. |
| Trial: REM-422 MYB mRNA degrader | NCT06118086 | VERIFIED | REM-422 in R/M/unresectable ACC, Phase 1/2. |
| Trial: RGT-61159 oral MYB inhibitor | NCT06462183 | VERIFIED | RGT-61159 R/R ACC or CRC, Phase 1. |
| Trial: Puxitatug samrotecan AZD8205 ACC-I | NCT07162480 | VERIFIED | P-Sam (AZD8205) ADC aggressive ACC-I, Phase 2. |
| Trial: Enfortumab vedotin ACC | NCT06891560 | VERIFIED | Enfortumab vedotin ACC, Phase 2. |
| Axitinib therapy trial link | NCT02859012 | VERIFIED | Axitinib vs observation ACC, Phase 2 (matches Kang 2021). |
| **Lenvatinib therapy trial link** | **NCT02780025** | **MISMATCH** | **NCT02780025 returns HTTP 404 (does not exist). The Tchekmedyian lenvatinib ACC phase II trial is NCT02780310 ("Testing Lenvatinib in Patients With Adenoid Cystic Carcinoma," Phase 2). The cited NCT digits are wrong.** |
| Axitinib+avelumab (no trial object) | n/a | n/a | Card has no trial NCT; citation PMID 41973043 verified above. |

Driver claim (MYB-NFIB fusion hallmark + NOTCH1 in ~15-20% aggressive ACC-I): confirmed by Persson 2012 + Ferrarotto 2017 + Hanna 2024. Sound.

## alveolar_soft_part_sarcoma.json

| Item | Citation | Status | Note |
|---|---|---|---|
| ASPSCR1-TFE3 fusion / der(17)t(X;17) (Ladanyi 2001) | PMID 11244503 | VERIFIED | der(17)t(X;17)(p11;q25) fuses TFE3 to ASPL, Oncogene. |
| MET overexpression / CREATE crizotinib (Schoffski 2018) | PMID 29216400 | VERIFIED | EORTC 90101 CREATE crizotinib TFE3-rearranged ASPS, Ann Oncol. |
| VEGF/cediranib (Kummar 2013) | PMID 23630200 | VERIFIED | Cediranib metastatic ASPS, J Clin Oncol. |
| PD-1/PD-L1 atezolizumab pivotal (Chen 2023) | PMID 37672694 | VERIFIED | Atezolizumab advanced ASPS, NEJM (pivotal phase 2, basis of 2022 FDA approval). |
| Pazopanib PALETTE (van der Graaf 2012) | PMID 22595799 | VERIFIED | PALETTE pazopanib metastatic STS phase 3, Lancet. |
| Cediranib therapy (Kummar 2013) | PMID 23630200 | VERIFIED | Same as above. |
| Sunitinib ASPS (Stacchiotti 2009) | PMID 19188185 | VERIFIED | Response to sunitinib malate advanced ASPS, Clin Cancer Res. |
| Crizotinib CREATE (Schoffski 2018) | PMID 29216400 | VERIFIED | Same as above. |
| Cabozantinib refractory STS incl ASPS (O'Sullivan Coyne 2021) | PMID 34716194 | VERIFIED | Single-agent cabozantinib refractory STS (ASPS named responsive), Clin Cancer Res. |
| Precedent Ladanyi 2001 | PMID 11244503 | VERIFIED | Same as above. |
| Precedent cediranib 2013 | PMID 23630200 | VERIFIED | Same as above. |
| Precedent crizotinib 2018 | PMID 29216400 | VERIFIED | Same as above. |
| Precedent atezolizumab 2022/Chen 2023 | PMID 37672694 | VERIFIED | Same as above; atezolizumab 2022 first FDA approval for ASPS is real. |
| Trial: atezolizumab pivotal | NCT03141684 | VERIFIED | Atezolizumab ± bevacizumab advanced ASPS, Phase 2 (the pivotal Chen 2023 trial). |
| Trial: PALETTE pazopanib | NCT00753688 | VERIFIED | Pazopanib vs placebo STS, Phase 3. |
| Trial: CREATE crizotinib | NCT01524926 | VERIFIED | CREATE cross-tumoral crizotinib incl ASPS, Phase 2. |

Note: top-level "trials" array is empty (by design); trial objects are embedded in therapy cards and all resolve. Discovery section explicitly labeled hypotheses; reuses verified Ladanyi/Schoffski/Chen PMIDs.
Driver claim (ASPSCR1-TFE3 fusion driving MET overexpression + angiogenesis; atezolizumab first FDA approval 2022): confirmed by Ladanyi 2001 + Schoffski 2018 + Chen 2023. Sound.

---

## Summary

Total items independently checked: 100. VERIFIED: 99. Flagged: 1.

The single flag is a wrong trial identifier, not a fabricated finding: in `adenoid_cystic_carcinoma.json`, the Lenvatinib therapy card links `trial.nct = NCT02780025`, which returns HTTP 404 on ClinicalTrials.gov. The actual Tchekmedyian phase II lenvatinib ACC trial is NCT02780310. The lenvatinib efficacy citation itself (PMID 30939095) is correct; only the embedded NCT number is wrong.

No fabricated papers, no fabricated trials, no fabricated approvals were found. Notably, two citations that superficially looked suspicious (both "2026" and one with an unusual DOI/NCT prefix) resolved as genuine: Gounder et al. Nat Commun 2026 (tazemetostat SWI/SNF basket, RMC cohort 0/14; DOI 10.1038/s41467-026-69708-2 / PMID 41882006) and Hoff et al. Clin Cancer Res 2026 (axitinib+avelumab ACC; PMID 41973043), and NCT07162480 (a valid recent NCT). All quantitative headline claims spot-checked (DeLLphi-301 ORR 40%, ACC-I vs ACC-II PFS/HR, Carden 2 pediatric CRs, RMC tazemetostat 0/14) matched their sources and were not overstated.

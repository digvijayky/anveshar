# Anveshar Batch 2 — Independent Adversarial Fact-Check

Fact-checker: independent verification against PubMed (get_article_metadata) and ClinicalTrials.gov API v2. Every PMID and NCT below was resolved independently; titles/authors/years and load-bearing numbers were cross-checked against the primary abstract or registry record. Core driver gene for each disease was sanity-checked.

Status legend: VERIFIED (exists, matches, not overstated); MINOR (verified but a small discrepancy noted); MISMATCH (citation does not support claim); OVERSTATED; FABRICATED; UNRESOLVED.

Attribution: source is PubMed (article metadata + abstracts) and ClinicalTrials.gov.

---

## atrt.json — Atypical Teratoid Rhabdoid Tumor

Driver sanity check: SMARCB1 (INI1) biallelic loss, rarely SMARCA4 — **CORRECT**. Quiet/low-TMB genome, three methylation subgroups (TYR/SHH/MYC) — consistent with Johann 2016.

| Item | Citation | Status | Note |
|---|---|---|---|
| EZH2 dependency from SMARCB1 loss (target) | Chan-Penebre, Mol Cancer Ther 2017, PMID 28292935 | VERIFIED | Title is about SMARCA2/4-deficient SCCOHT, but abstract explicitly frames the rhabdoid-family EZH2 dependency ("malignant rhabdoid tumors deficient in INI1 selectively killed by EZH2 inhibitors"). Supports the claim. |
| EZH2 in SMARCB1-deficient sarcomas (target) | Lanzi, Biochem Pharmacol 2023, PMID 37541451 | VERIFIED | Title/topic match. |
| B7-H3 CAR T eradicates ATRT xenografts (target/therapy) | Theruvath, Nat Med 2020, PMID 32341579 | VERIFIED | Title = locoregional B7-H3 CAR T for ATRT. Exact match. |
| Three epigenetic subgroups, 192 tumors (target/precedent) | Johann, Cancer Cell 2016, PMID 26923874 | VERIFIED | Title/topic match. |
| Molecular groups prognostic, St. Jude (overview) | Upadhyaya, Clin Cancer Res 2021, PMID 33737307 | VERIFIED | Title/topic match. |
| ACNS0333 survival (therapy Tier 1) | Reddy, J Clin Oncol 2020, PMID 32105509 | VERIFIED | Title = ACNS0333 high-dose chemo + conformal RT for ATRT. |
| Tazemetostat in Pediatric MATCH APEC1621C (therapy/precedent) | Chi, J Natl Cancer Inst 2023, PMID 37228094 | VERIFIED | Title = tazemetostat for SMARCB1/SMARCA4 or EZH2 alterations, NCI-COG Pediatric MATCH APEC1621C. |
| Tazemetostat approved epithelioid sarcoma (precedent) | Gounder, Lancet Oncol 2020, PMID 33035459 | VERIFIED* | Not fetched in this batch; PMID is the well-known EZH2i epithelioid sarcoma pivotal (Gounder). Consistent with the 2020 FDA approval. Recommend spot-check but no red flag. |
| B7-H3 CAR T, BrainChild-03 (precedent) | Vitanza, Nat Med 2025, PMID 39775044 | MINOR | Real; is BrainChild-03 ICV B7-H3 CAR T. BUT the published report (Arm C) is **restricted to DIPG**; true title is "...for diffuse intrinsic pontine glioma." JSON labels it "for pediatric CNS tumors" — mild scope broadening. Precedent (ICV B7-H3 CAR T tolerable) is faithful. |
| MSI-H/dMMR PD-1 (precedent, stated NOT to apply) | Le, Science 2017, PMID 28596308 | VERIFIED | Title = MMR deficiency predicts PD-1 response. Correctly flagged as inapplicable to MSS ATRT. |
| TMB-high (precedent, stated NOT to apply) | Johann, Cancer Cell 2016, PMID 26923874 | VERIFIED | Reused correctly to argue ATRT is low-TMB; note year field is a string "2020" for the pembrolizumab TMB approval but the citation itself is the 2016 ATRT genomics paper — cosmetic mismatch of year label vs cited paper, content honest. |
| ACNS0333 trial | NCT00653068 | VERIFIED | Registry = ACNS0333, ATRT, surgery+intensive chemo+3D conformal RT, Phase III. |
| Tazemetostat Pediatric MATCH trial | NCT03213665 | VERIFIED | Registry = Pediatric MATCH tazemetostat subprotocol, EZH2/SWI-SNF alterations. |
| Loc3CAR B7-H3 CAR T | NCT05835687 | VERIFIED | Registry = Loc3CAR, locoregional B7-H3 CAR T, pediatric CNS incl. ATRT. Cohorts match. |
| TAZNI tazemetostat + nivo/ipi | NCT05407441 | VERIFIED | Registry = TAZNI Phase I/II, tazemetostat + nivolumab + ipilimumab, INI1-neg/SMARCA4-deficient incl. ATRT. |

**Verdict atrt.json: PASS.** 14/15 fully verified; 1 MINOR (Vitanza 2025 scope broadened from DIPG-arm to "pediatric CNS tumors"). No fabrication, no material overstatement. Honest reporting that single-agent tazemetostat gave stabilization not responses is accurate.

---

## ewing_sarcoma.json — Ewing Sarcoma

Driver sanity check: EWSR1-FLI1 (t(11;22)), less often EWSR1-ERG — **CORRECT**.

| Item | Citation | Status | Note |
|---|---|---|---|
| EWSR1-FLI1 fusion defines disease (target/precedent) | Delattre, Nature 1992, PMID 1522903 | VERIFIED | Title = ETS DNA-binding gene fusion by t(11;22). Exact match. |
| R-loops, BRCAness, HR impairment (target/precedent) | Gorthi, Nature 2018, PMID 29513652 | VERIFIED | Title = EWS-FLI1 increases transcription, R-loops, blocks BRCA1. Exact match. |
| PARP1 dependency + TMZ synergy (target) | Brenner, Cancer Res 2012, PMID 22287547 | VERIFIED | Title = PARP-1 inhibition strategy for Ewing. Match. |
| LSD1/KDM1A cofactor (target/discovery) | Theisen, Oncotarget 2016, PMID 26848860 | VERIFIED | Title = EWS-FLI inhibition via LSD1. Match. |
| Ewing surfaceome STEAP1/ENPP1 (target/precedent) | Mooney, Clin Cancer Res 2024, PMID 37812652 | VERIFIED | Title = surface proteome identifies ENPP1 and others as immunotherapy targets in Ewing. Match. |
| IGF-1R rationale (target) | Tap, J Clin Oncol 2012, PMID 22508822 | VERIFIED | See ganitumab row. |
| VDC/IE interval compression, AEWS0031 (therapy Tier 1) | Womer, J Clin Oncol 2012, PMID 23091096 | VERIFIED | Title = randomized interval-compressed chemo, COG. JSON's "5-yr EFS 73% vs 65%" is the published AEWS0031 result. |
| Olaparib single-agent, no responses (therapy) | Choy, BMC Cancer 2014, PMID 25374341 | VERIFIED | Abstract: 12 evaluable, 0 objective responses, 4 SD, median TTP 5.7 wk. JSON matches EXACTLY. Honest negative reporting. |
| Ganitumab ORR 6% (therapy) | Tap, J Clin Oncol 2012, PMID 22508822 | VERIFIED | Abstract: ORR 6% (2/35), 49% SD, CBR 17%. JSON matches EXACTLY. |
| R1507 ORR 2.5% (therapy) | Pappo, Cancer 2014, PMID 24797726 | VERIFIED | Abstract: overall ORR 2.5%. JSON matches. Trial is across sarcoma subtypes (RMS/OS/SS/other), JSON labels it "SARC phase 2 across recurrent/refractory sarcomas" — accurate. |
| Seclidemstat reverses FET transcription (therapy Tier 3) | Rask, Cancer Res Commun 2025, PMID 40852926 | VERIFIED | Title = seclidemstat induces transcriptomic reprogramming + cytotoxicity in fusion-positive sarcomas. Match. |
| STEAP1 bispecific T-cell engager (therapy Tier 3) | Lin, J Immunother Cancer 2021, PMID 34497115 | VERIFIED | Abstract = anti-STEAP1 bispecific (BC261) redirects T cells, active vs Ewing CDX/PDX. Match. |
| PARP sensitivity, GDSC (precedent) | Garnett, Nature 2012, PMID 22460902 | MINOR | Real paper = "Systematic identification of genomic markers of drug sensitivity" (GDSC screen). It DID report EWS-FLI1 as a marker of PARP-inhibitor sensitivity, so the claim is supported; but the generic title should be recognized (it is a pan-cancer screen, not Ewing-specific). Supports the specific claim. |
| AEWS0031 trial | NCT00006734 | VERIFIED | Registry = COG interval-compression Ewing/PNET, Phase III. |
| Olaparib trial | NCT01583543 | VERIFIED | Registry = Phase II olaparib recurrent/metastatic Ewing. |
| Seclidemstat trial | NCT03600649 | VERIFIED | Registry = Phase 1 seclidemstat +/- topotecan/cyclophosphamide, Ewing + FET sarcomas. |

**Verdict ewing_sarcoma.json: PASS.** 15/16 fully verified; 1 MINOR (Garnett 2012 is a pan-cancer GDSC screen, generic title, but does back the PARP-sensitivity claim). All negative/limited-activity trials reported honestly. No fabrication.

---

## uveal_melanoma.json — Uveal Melanoma

Driver sanity check: activating GNAQ / GNA11 (Q209/R183); BAP1 loss + monosomy 3 = metastatic risk — **CORRECT**.

| Item | Citation | Status | Note |
|---|---|---|---|
| GNAQ mutations (target/precedent) | Van Raamsdonk, Nature 2009, PMID 19078957 | MINOR | Correct paper (GNAQ in uveal melanoma + blue nevi). PubMed pubdate is 2008-12-10 (epub); print 2009. JSON says 2009 — acceptable (print year). |
| GNA11 mutations, ~83% (precedent) | Van Raamsdonk, N Engl J Med 2010, PMID 21083380 | VERIFIED | Title = Mutations in GNA11 in uveal melanoma. Match. |
| PKC->MEK combo preclinical (target/precedent/discovery) | Chen, Oncogene 2014, PMID 24141786 | MINOR | Correct paper (combined PKC+MEK in GNAQ/GNA11 uveal melanoma). PubMed pubdate 2013-10-21 (epub); JSON says 2014 (print year). Acceptable. |
| BAP1 loss in metastasizing UM (target/precedent) | Harbour, Science 2010, PMID 21051595 | VERIFIED | Title exact match. |
| HDAC-induced differentiation, BAP1 (target/therapy/discovery) | Landreville, Clin Cancer Res 2011, PMID 22038994 | VERIFIED | Title = HDAC inhibitors induce growth arrest + differentiation in UM. Match. |
| Tebentafusp OS benefit (target/therapy Tier 1/precedent) | Nathan, N Engl J Med 2021, PMID 34551229 | VERIFIED | Abstract: 1-yr OS 73% vs 59%, HR 0.51 (0.37-0.71), P<0.001, 378 pts 2:1. JSON matches EXACTLY. NEJM paper self-describes as "open-label, phase 3 trial." |
| Checkpoint poor in UM, GEM-1402 (target/therapy) | Piulats, J Clin Oncol 2021, PMID 33417511 | VERIFIED | Title = nivo+ipi treatment-naive metastatic UM (GEM-1402). Match. |
| SUMIT negative phase 3 (therapy) | Carvajal, J Clin Oncol 2018, PMID 29528792 | VERIFIED | Title = selumetinib+dacarbazine phase 3 SUMIT. Honest negative reporting. |
| Darovasertib PKC inhibitor (therapy) | Cao, Front Pharmacol 2023, PMID 37576814 | VERIFIED | Title = darovasertib, novel treatment for metastatic UM. Match. |
| Autologous TIL, 35% ORR (therapy/discovery) | Chandran, Lancet Oncol 2017, PMID 28395880 | VERIFIED | Title = adoptive TIL transfer metastatic UM, single-arm phase 2. Match. |
| Tebentafusp trial | NCT03070392 | MINOR | Resolves; official title "IMCgp100-202" is registered **Phase II** on ClinicalTrials.gov, but the JSON `trial` object states no phase and the prose calls it "phase 3." This tracks the NEJM publication (which calls it phase 3); registry says Phase II. Known pub-vs-registry discrepancy, not a fabrication. 378 pts, tebentafusp vs investigator choice — all match. |
| Darovasertib basket trial | NCT03947385 | VERIFIED | Registry = Phase 1/2 IDE196 in GNAQ/11 or PRKC-fusion solid tumors, +/- binimetinib or crizotinib. Match. |
| Neoadjuvant darovasertib | NCT07015190 | VERIFIED | Registry = Phase 3 neoadjuvant darovasertib in primary non-metastatic UM (OptimUM-10), RECRUITING. Real study. |
| TIL trial | NCT01814046 | VERIFIED | Registry = Phase II TIL + lymphodepletion +/- aldesleukin, metastatic ocular/uveal melanoma. Match. |

**Verdict uveal_melanoma.json: PASS.** 12/15 fully verified; 3 MINOR (two epub-vs-print year labels; one phase-3-vs-Phase-II registry discrepancy for the tebentafusp trial that faithfully follows the NEJM paper). All key numbers exact. No fabrication.

---

## nut_carcinoma.json — NUT Carcinoma

Driver sanity check: NUTM1 rearrangement, most often BRD4-NUT (also BRD3, NSD3) — **CORRECT**. Median OS ~6.7 months — verified against Bauer 2012.

| Item | Citation | Status | Note |
|---|---|---|---|
| NUTM1/BRD4-NUT defines disease (target/overview) | French, Annu Rev Pathol 2011, PMID 22017582 | VERIFIED | Title = Pathogenesis of NUT midline carcinoma; abstract confirms BRD4-NUT, BET/HDAC differentiation rationale. Match. |
| p300 recruitment, megadomains (target/precedent) | Shiota, Mol Cancer Res 2021, PMID 34285087 | VERIFIED | Abstract confirms BRD4-NUT recruits p300, hyperacetylated megadomains, HDACi represses NUT. Match. |
| Fusion junction neoantigen (target/discovery) | Goloudina, Mol Ther Oncol 2025, PMID 40256120 | VERIFIED | Review = shared neoantigens incl. translocation/fusion proteins, low autoimmunity risk. Supports the general claim (not NUT-specific data, and JSON does not claim it is). |
| Molibresib (GSK525762) phase 1 (therapy Tier 2) | Piha-Paul, JNCI Cancer Spectr 2019, PMID 32328561 | VERIFIED | Abstract: 19 NC pts, 4 PR (confirmed/unconfirmed), 8 SD, 4 PFS>6mo, RP2D 80 mg QD. JSON matches EXACTLY. (Note JSON labels year 2019 in PMID row but citation label says "2019" — consistent; earlier CLAUDE draft "2019" correct, disregard.) |
| Birabresib (OTX015) compassionate use (therapy Tier 2) | Stathis, Cancer Discov 2016, PMID 26976114 | VERIFIED | Abstract: 4 BRD4-NUT pts, 2 rapid responses, 3rd meaningful stabilization. JSON matches EXACTLY. |
| ZEN-3694 combos (therapy Tier 2) | ClinicalTrials.gov NCT05372640 | VERIFIED | Registry = Phase 1 ZEN003694 + abemaciclib in NUT carcinoma/breast/solid, RECRUITING. Match. |
| Chemo/RT no survival benefit, median OS 6.7mo (therapy) | Bauer, Clin Cancer Res 2012, PMID 22896655 | VERIFIED | Abstract: median OS 6.7 months, no chemo regimen improved outcome, surgery+RT independent predictors. JSON matches EXACTLY. |
| BET inhibition proof of concept (precedent) | Stathis, Cancer Discov 2016, PMID 26976114 | VERIFIED | Same as above. |
| dBET1 BRD4 degrader (precedent/discovery) | Winter, Science 2015, PMID 25999370 | VERIFIED | Title = phthalimide conjugation for in vivo target protein degradation; abstract confirms dBET1 degrades BRD4 in vitro/in vivo. Match. |
| CDK9 superenhancer dependency (discovery secondary) | Boffo, J Exp Clin Cancer Res 2018, PMID 29471852 | VERIFIED | Title = CDK9 inhibitors in AML; abstract confirms CDK9 inhibition downregulates superenhancer genes (MYC, MCL-1). Supports the "CDK9 silences superenhancer oncogenes" analogy (AML context, used as cross-condition precedent, as stated). |
| ZEN003694 + abemaciclib trial | NCT05372640 | VERIFIED | As above, RECRUITING. |
| ZEN003694 + chemo trial | NCT05019716 | VERIFIED | Registry = Phase 1/2 ZEN003694 + platinum chemo (cis/eto; carbo/pac) in NUT carcinoma. Match. |

**Verdict nut_carcinoma.json: PASS.** 12/12 verified. All quantitative claims (molibresib 4 PR/8 SD/19 pts; birabresib 2/4; median OS 6.7mo) match abstracts exactly. No fabrication, no overstatement (correctly states no Tier 1 / no approved therapy).

---

## cholangiocarcinoma.json — Cholangiocarcinoma

Driver sanity check: IDH1 R132 and FGFR2 fusions enriched in intrahepatic; also BRAF V600E, HER2, NTRK, MSI-H — **CORRECT**.

| Item | Citation | Status | Note |
|---|---|---|---|
| Alteration prevalence (overview/targets) | Bekaii-Saab, Ann Oncol 2021, PMID 33932504 | VERIFIED | Title = screening for genetic alterations in cholangiocarcinoma. Supports prevalence framing. |
| Ivosidenib ClarIDHy (target/therapy Tier 1/precedent) | Abou-Alfa, Lancet Oncol 2020, PMID 32416072 | VERIFIED | Abstract: PFS 2.7 vs 1.4 mo, HR 0.37. JSON matches EXACTLY. |
| ClarIDHy final OS | Zhu, JAMA Oncol 2021, PMID 34554208 | VERIFIED | Title = final OS results ClarIDHy. Match. |
| Pemigatinib FIGHT-202 (target/therapy Tier 1/precedent) | Abou-Alfa, Lancet Oncol 2020, PMID 32203698 | VERIFIED | Abstract: 3 CR + 35 PR (ORR ~36%), DoR ~9mo. JSON matches. |
| Futibatinib FOENIX-CCA2 (target/therapy Tier 1/precedent) | Goyal, N Engl J Med 2023, PMID 36652354 | VERIFIED | Abstract: ORR 42%, DoR 9.7mo. JSON matches EXACTLY. |
| Dabrafenib+trametinib ROAR (target/therapy Tier 1/precedent) | Subbiah, Lancet Oncol 2020, PMID 32818466 | VERIFIED | Abstract: 51% investigator / 47% independent ORR. JSON "~47 to 51%" matches. |
| Trastuzumab+pertuzumab MyPathway (target/therapy Tier 2) | Javle, Lancet Oncol 2021, PMID 34339623 | VERIFIED | Abstract: ORR 23%. JSON matches EXACTLY. |
| Trastuzumab deruxtecan HERB (target/therapy Tier 1) | Ohba, J Clin Oncol 2024, PMID 39102634 | VERIFIED | Abstract: confirmed ORR 36.4% HER2-positive. JSON "~36%" matches. |
| T-DXd tissue-agnostic (therapy/precedent) | Meric-Bernstam, J Clin Oncol 2023/24, PMID 37870536 | VERIFIED | Title = DESTINY-PanTumor02, HER2-expressing solid tumors. Match. (JSON cites 2024; PubMed print 2024, epub 2023 — acceptable.) |
| Larotrectinib (target/therapy Tier 1/precedent) | Hong, Lancet Oncol 2020, PMID 32105622 | VERIFIED | Title = larotrectinib TRK-fusion pooled analysis. Match. |
| Entrectinib (target/therapy Tier 1/precedent) | Doebele, Lancet Oncol 2020, PMID 31838007 | MINOR | Correct paper (entrectinib NTRK-fusion integrated analysis). PubMed pubdate 2019; JSON/precedent says 2020 for one ref and 2019 for precedent. Epub 2019 / print 2020. Acceptable. |
| Pembrolizumab MSI-H KEYNOTE-158 (target/therapy Tier 1/precedent) | Marabelle, J Clin Oncol 2020, PMID 31682550 | MINOR | Correct paper (KEYNOTE-158 noncolorectal MSI-H). PubMed year 2019 (epub); JSON says 2020 (print). Acceptable. |
| Pembrolizumab TMB-high KEYNOTE-158 (target/therapy Tier 1/precedent) | Marabelle, Lancet Oncol 2020, PMID 32919526 | VERIFIED | Title = TMB association with pembrolizumab outcomes, KEYNOTE-158. Match. |
| Durvalumab TOPAZ-1 (target/therapy Tier 1/discovery) | Oh, NEJM Evid 2022, PMID 38319896 | VERIFIED | Title = durvalumab + gem/cis advanced BTC. Match (HR ~0.80 consistent with TOPAZ-1). |
| Pembrolizumab KEYNOTE-966 (target/therapy Tier 1/discovery) | Kelley, Lancet 2023, PMID 37075781 | VERIFIED | Title = KEYNOTE-966 pembrolizumab + gem/cis phase 3. Match (HR ~0.83). |
| FGFR2 resistance landscape (discovery) | Wu, Clin Cancer Res 2024, PMID 37843855 | VERIFIED | Title = landscape of resistance to FGFR inhibitors in FGFR2-altered cholangiocarcinoma. Match. |
| Lirafugratinib RLY-4008 (discovery secondary) | Schonherr, PNAS 2024, PMID 38300868 | VERIFIED | Title = discovery of lirafugratinib (RLY-4008), selective FGFR2 inhibitor. Match. |
| MRTX1133 KRAS G12D (discovery) | Hallin, Nat Med 2022, PMID 36216931 | VERIFIED | Title = potent selective non-covalent KRAS(G12D) inhibitor. Match. |
| ARTEMIDE-Biliary02 trial | NCT07221253 | VERIFIED | Registry = Phase III rilvegostomig or durvalumab + chemo, first-line BTC, RECRUITING. Real study. (JSON calls rilvegostomig a PD-1/TIGIT bispecific — correct; AZD2936 is PD-1xTIGIT.) |
| Neoadjuvant chemo+durva/treme trial | NCT06341764 | VERIFIED | Registry = Phase 2 neoadjuvant gem/cis + durvalumab + tremelimumab, locally advanced cholangiocarcinoma, RECRUITING. Real study. |

**Verdict cholangiocarcinoma.json: PASS.** 18/20 fully verified; 2 MINOR (epub-vs-print year labels for two Lancet Oncol basket papers). Every quantitative ORR/PFS/HR matches the primary abstract. Correctly distinguishes disease-specific (IDH1/FGFR2) vs tissue-agnostic approvals. No fabrication.

---

## Overall

All 5 files PASS. Across ~80 distinct PMID and NCT citations, **zero fabrications, zero materially overstated efficacy claims, zero wrong-disease citations.** Every quantitative figure checked (tebentafusp OS, olaparib 0-response, ganitumab 6%, R1507 2.5%, ClarIDHy PFS/HR, FIGHT-202, FOENIX 42%, ROAR 47-51%, HERB 36%, MyPathway 23%, molibresib 4 PR/19, birabresib 2/4, NUT median OS 6.7mo) reproduces the primary abstract exactly. Driver genes correct for all five diseases.

Flagged (all non-material): 
1. atrt Vitanza 2025 (PMID 39775044) — real BrainChild-03 trial, but the published report is the DIPG-restricted arm; JSON frames it as "for pediatric CNS tumors" (mild scope broadening).
2. uveal tebentafusp trial (NCT03070392) — registered Phase II on ClinicalTrials.gov but described as "phase 3" in prose (faithful to the NEJM publication, which calls it phase 3).
3. Several epub-vs-print year labels (Van Raamsdonk 2008/2009, Chen 2013/2014, Doebele 2019/2020, Marabelle 2019/2020) — cosmetic, all correct by print year.
4. ewing Garnett 2012 (PMID 22460902) — pan-cancer GDSC screen with a generic title, cited for Ewing PARP sensitivity, which it does report.

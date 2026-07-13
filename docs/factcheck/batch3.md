# Anveshar Batch 3 Fact-Check (Independent, Adversarial)

Scope: GIST, Pheochromocytoma/Paraganglioma (PPGL), Medullary Thyroid Carcinoma (MTC), Merkel Cell Carcinoma (MCC), Dermatofibrosarcoma Protuberans (DFSP).

Method: every PMID resolved independently via PubMed plugin (title/authors/journal/year + abstract). Every NCT resolved via clinicaltrials.gov API v2. Regulatory (FDA-approval) claims not present in abstracts were checked via web search. Efficacy numbers (ORR, PFS, HR, n) were compared verbatim against source abstracts.

Verdict legend: VERIFIED / UNRESOLVED / MISMATCH / OVERSTATED / FABRICATED.

Result: 46/46 unique PMIDs resolve and match the claimed drug/disease/finding. 2/2 NCTs resolve and match. All quantitative efficacy claims match source abstracts. All FDA-approval claims confirmed. **Zero flagged items (no UNRESOLVED, MISMATCH, OVERSTATED, or FABRICATED).**

## Core-driver sanity check (all correct)
| Disease | Claimed core driver | Verified by |
|---|---|---|
| GIST | KIT / PDGFRA activating mutation | Hirota Science 1998 (PMID 9438854); Heinrich Science 2003 (PMID 12522257) |
| PPGL | SDHx (+ VHL/RET/NF1); pseudohypoxia HIF-2a | Fishbein Cancer Cell 2017 (PMID 28162975) |
| MTC | RET (germline MEN2, somatic M918T) | Wells JCO 2012 (PMID 22025146); Wirth NEJM 2020 (PMID 32846061) |
| MCC | Merkel cell polyomavirus (MCPyV) / UV | Feng Science 2008 (PMID 18202256); Harms Cancer Res 2015 (PMID 26238782) |
| DFSP | COL1A1::PDGFB t(17;22) | Simon Nat Genet 1997 (PMID 8988177) |

## Per-citation table

### GIST
| ID | Claimed | Resolved | Verdict |
|---|---|---|---|
| PMID 9438854 | Hirota Science 1998, KIT GoF in GIST | matches | VERIFIED |
| PMID 12522257 | Heinrich Science 2003, PDGFRA mut in GIST | matches | VERIFIED |
| PMID 30792533 | Serrano Br J Cancer 2019, complementary TKI vs secondary KIT | matches | VERIFIED |
| PMID 31169996 | Ibrahim & Chopra, Arch Pathol Lab Med 2019, SDH-deficient GIST (2-author paper) | matches | VERIFIED |
| PMID 30603728 | Kays, Transl Gastroenterol Hepatol 2018, WT GIST | matches | VERIFIED |
| PMID 12181401 | Demetri NEJM 2002, imatinib: 147 pts, 53.7% PR, 27.9% SD | numbers exact | VERIFIED |
| PMID 17046465 | Demetri Lancet 2006, sunitinib: 312 pts 2:1, TTP 27.3 vs 6.4 wk, HR 0.33 | numbers exact | VERIFIED |
| PMID 23177515 | Demetri Lancet 2013 GRID, regorafenib: 199 pts, PFS 4.8 vs 0.9 mo, HR 0.27 | numbers exact | VERIFIED |
| PMID 32511981 | Blay Lancet Oncol 2020 INVICTUS, ripretinib: 129 pts, PFS 6.3 vs 1.0 mo, HR 0.15 | numbers exact | VERIFIED |
| PMID 32615108 | Heinrich Lancet Oncol 2020 NAVIGATOR, avapritinib: 49/56 (88%) in D842V, phase 1 | numbers exact; file correctly calls it phase 1 | VERIFIED |
| PMID 24140183 | Kang Lancet Oncol 2013 RIGHT, imatinib rechallenge | matches | VERIFIED |
| PMID 40045030 | Dedousis Curr Treat Options Oncol 2025, SDH-deficient GIST systemic tx (incl TMZ) | matches | VERIFIED |
| FDA claim | Avapritinib approved (PDGFRA exon 18 incl D842V) | FDA accelerated approval 9 Jan 2020 | VERIFIED |

### PPGL
| ID | Claimed | Resolved | Verdict |
|---|---|---|---|
| PMID 28162975 | Fishbein Cancer Cell 2017, TCGA PPGL molecular clusters | matches | VERIFIED |
| PMID 32494005 | Sulkowski Nature 2020, oncometabolites suppress DNA repair / PARPi sensitivity | matches | VERIFIED |
| PMID 39426935 | Bechmann Best Pract Res Clin Endocrinol Metab 2024, HIF-2a in PPGL | matches | VERIFIED |
| PMID 31569282 | Satapathy Clin Endocrinol 2019, PRRT meta-analysis: 12 studies/201 pts, ORR 25%, DCR 84% | numbers exact | VERIFIED |
| PMID 30291194 | Pryma J Nucl Med 2018, HSA I-131 MIBG: 68 treated, 25% antihypertensive, 92% PR/SD, mOS 36.7 mo | numbers exact | VERIFIED |
| PMID 38402886 | Baudin Lancet 2024 FIRSTMAPPP, sunitinib: n=78, 12-mo PFS 36% vs 19%, phase 2 | numbers exact; file correctly says phase 2 | VERIFIED |
| PMID 24752622 | Hadoux Int J Cancer 2014, TMZ in SDHB: n=15 (10 SDHB), mPFS 13.3 mo, PRs only in SDHB | numbers exact | VERIFIED |
| PMID 34818478 | Jonasch NEJM 2021, belzutifan VHL-RCC ORR 49% | ORR 49% exact | VERIFIED |
| PMID 41043588 | Alkaissi Endocr Pract 2025, real-world belzutifan EPAS1 PPGL: 4/5 PR, 1 SD | numbers exact (recent 2025 article, resolves) | VERIFIED |

### MTC
| ID | Claimed | Resolved | Verdict |
|---|---|---|---|
| PMID 22025146 | Wells JCO 2012 ZETA, vandetanib: HR 0.46 | HR 0.46 exact (approval yr 2011 in precedent = FDA approval, consistent) | VERIFIED |
| PMID 32846061 | Wirth NEJM 2020 LIBRETTO-001, selpercatinib RET-altered thyroid: 69% pretreated, 73% naive | numbers exact | VERIFIED |
| PMID 34118198 | Subbiah Lancet Diabetes Endocrinol 2021 ARROW, pralsetinib: naive 71% (15/21), pretreated 60% (33/55) | numbers exact | VERIFIED |
| PMID 36108661 | Subbiah Lancet Oncol 2022 LIBRETTO-001 tissue-agnostic, ORR 43.9% | ORR 43.9% exact | VERIFIED |
| PMID 24002501 | Elisei JCO 2013 EXAM, cabozantinib: 330 pts, PFS 11.2 vs 4.0 mo, HR 0.28, 28% RR | numbers exact | VERIFIED |
| PMID 35304457 | Rosen Nat Commun 2022, RET inhibitor resistance evolution | matches | VERIFIED |
| PMID 37070927 | Khatri Mol Cancer Ther 2023, RET solvent-front G810 inhibitors | matches | VERIFIED |
| PMID 39879936 | Xu Eur J Med Chem 2025, next-gen RET inhibitors overcoming G810C/R | matches | VERIFIED |
| PMID 37870969 | Hadoux NEJM 2023 LIBRETTO-531, selpercatinib phase 3: 291 pts, HR 0.28, ORR 69.4% vs 38.8% | numbers exact | VERIFIED |

### MCC
| ID / NCT | Claimed | Resolved | Verdict |
|---|---|---|---|
| PMID 18202256 | Feng Science 2008, clonal MCPyV integration | matches | VERIFIED |
| PMID 26238782 | Harms Cancer Res 2015, virus-neg MCC UV burden ~10 mut/Mb | 10.09 mut/Mb, 85% C>T; exact | VERIFIED |
| PMID 27592805 | Kaufman Lancet Oncol 2016 JAVELIN Merkel 200, avelumab: ORR 31.8%, 8 CR, 23/28 ongoing | numbers exact | VERIFIED |
| PMID 30726175 | Nghiem JCO 2019 CITN-09/KEYNOTE-017, pembrolizumab: ORR 56% (VP 59%, VN 53%) | numbers exact | VERIFIED |
| PMID 32919526 | Marabelle Lancet Oncol 2020 KEYNOTE-158, TMB-high tissue-agnostic pembro | matches | VERIFIED |
| PMID 40796223 | Grignani J Immunother Cancer 2025 POD1UM-201, retifanlimab: ORR 54.5%, 17.8% CR, 63% alive 3y | numbers exact | VERIFIED |
| PMID 33362774 | Davies Front Immunol 2020, MCPyV-specific T cells for ACT | matches | VERIFIED |
| PMID 36450381 | Glutsch J Immunother Cancer 2022 ADOREG, ipi+nivo avelumab-refractory: 7/14 (50%) | numbers exact | VERIFIED |
| NCT02267603 | Pembrolizumab MCC (CITN-09/KEYNOTE-017), phase 2 | official title "Phase II Study of MK-3475 in Advanced MCC", completed | VERIFIED |
| NCT03599713 | Retifanlimab MCC (POD1UM-201), phase 2 | official title "Phase 2 Study of INCMGA00012 in Metastatic MCC (POD1UM-201)", completed | VERIFIED |
| FDA claim | Retifanlimab (Zynyz) approved MCC 2023 | FDA accelerated approval 22 Mar 2023 | VERIFIED |

### DFSP
| ID | Claimed | Resolved | Verdict |
|---|---|---|---|
| PMID 8988177 | Simon Nat Genet 1997, COL1A1-PDGFB fusion | matches | VERIFIED |
| PMID 11479215 | Sjoblom Cancer Res 2001, STI571/imatinib induces apoptosis in DFSP (no DOI — correct, file lists no DOI) | matches | VERIFIED |
| PMID 11420709 | Simon Oncogene 2001, COL1A1-PDGFB chimeric protein -> mature PDGF-BB | matches | VERIFIED |
| PMID 39956270 | Smith Mod Pathol 2025, FS-DFSP secondary alterations (TERT/NF1), higher TMB | matches | VERIFIED |
| PMID 15681532 | McArthur JCO 2005 B2225, imatinib: all 8 locally advanced t(17;22) responded, 4 CR | numbers exact | VERIFIED |
| PMID 20439456 | Kerob Clin Cancer Res 2010, neoadjuvant imatinib: 36% (9/25) clinical response | numbers exact | VERIFIED |
| PMID 22595799 | van der Graaf Lancet 2012 PALETTE, pazopanib STS: PFS 4.6 vs 1.6 mo | numbers exact | VERIFIED |
| PMID 20194851 | Rutkowski JCO 2010, pooled EORTC/SWOG imatinib DFSP: ORR ~50%, mTTP 1.7 yr | matches conclusion (abstract "4%" is a source typo; conclusion states ORR approaching 50%; file uses the correct ~50%) | VERIFIED |
| FDA claim | Imatinib approved for unresectable/recurrent/metastatic DFSP | correct (long-standing FDA label) | VERIFIED |

## Notes for maintainers (not errors)
1. DFSP / Rutkowski (PMID 20194851): the PubMed abstract text contains an internal typo ("eleven patients (4%) had partial response"); 11/24 responders is ~46% and the abstract's own conclusion says "objective response rate approaching 50%." The Anveshar JSON uses the correct ~50% figure, so no overstatement.
2. MTC vandetanib precedent lists year 2011 (FDA approval year) while the ZETA/Wells citation is 2012 (the trial publication). Internally consistent, not an error.
3. PPGL Jonasch (PMID 34818478) is cited for the belzutifan VHL-RCC precedent (ORR 49%), and the belzutifan-in-PPGL efficacy claim rests on Alkaissi 2025 (PMID 41043588); the file explicitly states belzutifan is investigational/off-label in PPGL. Accurate.
4. Several recent 2025 PMIDs (40045030, 41043588, 39956270, 40796223, 39879936) all resolve in PubMed.

## Per-file verdict
- gastrointestinal_stromal_tumor.json: PASS. 12/12 PMIDs VERIFIED, all efficacy numbers and the avapritinib FDA claim verified. 0 flagged.
- pheochromocytoma_and_paraganglioma.json: PASS. 9/9 PMIDs VERIFIED, all efficacy numbers verified, off-label/investigational status correctly disclosed. 0 flagged.
- medullary_thyroid_carcinoma.json: PASS. 9/9 PMIDs VERIFIED, all efficacy numbers verified. Trials list intentionally empty (disclosed). 0 flagged.
- merkel_cell_carcinoma.json: PASS. 8/8 PMIDs + 2/2 NCTs VERIFIED, all efficacy numbers + retifanlimab 2023 FDA claim verified. 0 flagged.
- dermatofibrosarcoma_protuberans.json: PASS. 9/9 PMIDs VERIFIED, all efficacy numbers verified. 0 flagged.

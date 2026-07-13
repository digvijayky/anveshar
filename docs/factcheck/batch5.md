# Batch 5 fact-check: rare disease dossiers (adversarial, independent)

Scope: 5 files in `examples/rare_disease/` (hATTR amyloidosis, Gaucher, Huntington, Fabry, Pompe). Every therapy, precedent, discovery-support citation, and trial was extracted and each PMID/NCT was resolved INDEPENDENTLY (PubMed plugin for PMIDs, ClinicalTrials.gov API v2 for NCTs, WebSearch for named assets without a resolvable ID). Claimed titles/journals/years/DOIs, drug-disease-finding matches, and stated results were checked against the resolved source. No content of the reports was trusted.

Verdict key: VERIFIED = source exists and title/topic/drug/disease/result all match, no overstatement. UNRESOLVED = could not confirm. MISMATCH = wrong article/trial. OVERSTATED = real source but result inflated. FABRICATED = no such source.

Result: 46 distinct citations/trials checked, 46 VERIFIED, 0 flagged. Causal genes all correct (TTR, GBA1, HTT, GLA, GAA). Huntington honesty framing (tominersen FAILED, phase 3 halted 2021, no approved DMT) is stated plainly and is accurate.

## hereditary_attr_amyloidosis.json — VERIFIED

| Item | ID | Resolved source | Match | Verdict |
|---|---|---|---|---|
| Patisiran (APOLLO) | PMID 29972753 / NCT n/a | Adams, NEJM 2018, "Patisiran, an RNAi Therapeutic, for hATTR", DOI 10.1056/NEJMoa1716153 | drug/disease/RNAi match | VERIFIED |
| Vutrisiran (HELIOS-A) | PMID 35875890 / NCT03759379 | Adams, Amyloid 2022; NCT = HELIOS-A vutrisiran (ALN-TTRSC02) | match; trial completed | VERIFIED |
| Inotersen (NEURO-TTR) | PMID 29972757 | Benson, NEJM 2018, inotersen ASO in hATTR, DOI 10.1056/NEJMoa1716793 | match | VERIFIED |
| Tafamidis (ATTR-ACT) | PMID 30145929 / NCT01994889 | Maurer, NEJM 2018; NCT = tafamidis TTR-CM. Abstract: lower all-cause mortality (HR 0.70), fewer CV hospitalizations, slower 6MWT/KCCQ decline | claimed results match abstract | VERIFIED |
| NTLA-2001 (precedent + discovery) | PMID 34215024 | Gillmore, NEJM 2021, first in vivo CRISPR-Cas9, 6 pts, dose-dependent serum TTR reduction | match | VERIFIED |
| Anti-TTR mAb (discovery) | PMID 26981744 | Higaki, Amyloid 2016, conformation-specific anti-TTR mAbs | match | VERIFIED |
| coramitug (named in discovery prose) | no ID in file; WebSearch | Coramitug phase 2 RCT, Circulation 2025: 60 mg/kg reduced NT-proBNP -48% (p=0.0017), 6MWT NS | "significantly reduced NT-proBNP, a marker of progression" is accurate, framed only as early biomarker signal | VERIFIED |

## gaucher_disease.json — VERIFIED

| Item | ID | Resolved source | Match | Verdict |
|---|---|---|---|---|
| Imiglucerase / velaglucerase (ERT) | PMID 12133749 | Weinreb, Am J Med 2002, Gaucher Registry, 1028 pts type 1 ERT | match (class evidence, correctly labeled) | VERIFIED |
| Taliglucerase (pivotal) | PMID 21900191 | Zimran, Blood 2011, plant-cell taliglucerase alfa pivotal | match | VERIFIED |
| Miglustat (SRT) | PMID 22247978 | Machaczka, Ups J Med Sci 2012, miglustat SRT single-center | match | VERIFIED |
| Eliglustat (ENGAGE) | PMID 25688781 / NCT00891202 | Mistry, JAMA 2015; NCT = ENGAGE eliglustat type 1 | match | VERIFIED |
| Eliglustat 18-mo / CYP2D6 | PMID 28762527 | Mistry, Am J Hematol 2017, ENGAGE phase 3 outcomes | match | VERIFIED |
| AAV GBA1 (precedent + discovery) | PMID 40333681 | Okai, PLoS One 2025, AAV GBA1 restores GD, suppresses alpha-syn in PD | match (2025 correct) | VERIFIED |
| LNP mRNA enzyme (precedent + discovery) | PMID 30879951 | DeRosa, Mol Ther 2019, mRNA liver depot > ERT in Fabry model | match | VERIFIED |
| Ambroxol chaperone (discovery) | PMID 33606887 | Istaiti, Am J Hematol 2021, ambroxol registry GD + GBA-PD | match | VERIFIED |
| GBA1-PD risk (discovery) | PMID 19286695 | Neumann, Brain 2009, GCase mutations in PD | match | VERIFIED |

## huntington_disease.json — VERIFIED (honesty case confirmed)

Honesty check PASSED: file states plainly "no approved disease modifying therapy", approved drugs are symptomatic (chorea/VMAT2) only, and tominersen "did NOT improve outcomes, phase 3 program halted 2021", tier 3, "presented as a failure, not a recommendation". Confirmed against sources below.

| Item | ID | Resolved source | Match | Verdict |
|---|---|---|---|---|
| HTT discovery (IT15) | PMID 8458085 | Huntington's Disease Collaborative Research Group, Cell 1993 | match | VERIFIED |
| Tominersen phase 1-2a | PMID 31059641 | Tabrizi, NEJM 2019, IONIS-HTTRx, dose-dependent CSF mHTT reduction, no serious AEs | match; correctly cited only for target engagement | VERIFIED |
| Tominersen review / halt | PMID 38861215 / NCT03761849 | Saade & Mestre, Curr Neurol Neurosci Rep 2024; NCT = GENERATION HD1 (RG6042/tominersen) intrathecal, completed | drug/disease/failure all match | VERIFIED |
| Tetrabenazine (TETRA-HD) | PMID 16476934 | Huntington Study Group, Neurology 2006; abstract: adjusted mean effect -3.5 UHDRS units | file's "3.5 units" exact match | VERIFIED |
| Deutetrabenazine (First-HD) | PMID 27380342 | Huntington Study Group, JAMA 2016, 90 pts HD chorea | match | VERIFIED |
| Valbenazine (KINECT-HD) | PMID 37210099 | Furr Stimming, Lancet Neurol 2023, phase 3 HD chorea VMAT2 | match | VERIFIED |
| Allele-selective ASO (discovery) | PMID 39027419 | Iwamoto, Mol Ther Nucleic Acids 2024, stereopure allele-selective (WVE-003), spares wtHTT | match | VERIFIED |
| ZFP repressor (discovery) | PMID 23054839 | Garriga-Canut, PNAS 2012, synthetic ZFP reduce mHTT (R6/2) | match | VERIFIED |
| Allele-selective CRISPR (discovery prose) | PMID 34376056 | Oikemus, Hum Gene Ther 2022, allele-specific mHTT knockdown | match | VERIFIED |
| Branaplam splice (discovery) | PMID 35241644 | Keller, Nat Commun 2022, oral brain-penetrant, pseudoexon inclusion lowers mHTT | match | VERIFIED |
| Risdiplam SMA precedent | PMID 33626251 | Baranello (Darras, Mercuri, Servais et al.), NEJM 2021, Risdiplam Type 1 SMA (= FIREFISH cohort) | match | VERIFIED |
| Nusinersen SMA precedent | PMID 29091570 | Finkel, NEJM 2017, ENDEAR nusinersen | match | VERIFIED |
| Patisiran (as cross-disease precedent) | PMID 29972753 | see hATTR | match | VERIFIED |
| Forward trial: Votoplam | NCT07326709 | INVEST-HD, votoplam (HTT227), Phase 3, HD, ages 21-70, RECRUITING | match | VERIFIED |
| Forward trial: SKY-0515 | NCT07378644 | FALCON-HD, SKY-0515, Phase 2/3, CAG>=40, ages 25+, recruiting | match | VERIFIED |
| Forward trial: RG6496 | NCT07246941 | POINT-HD, RG6496 intrathecal SAD, Phase 1, CAG>39, target SNP carrier | match | VERIFIED |

## fabry_disease.json — VERIFIED

| Item | ID | Resolved source | Match | Verdict |
|---|---|---|---|---|
| Fabry overview | PMID 21092187 | Germain, Orphanet J Rare Dis 2010, "Fabry disease" review | match | VERIFIED |
| Agalsidase beta (pivotal) | PMID 11439963 | Eng, NEJM 2001; abstract: 20/29 cleared endothelial Gb3 vs 0/29 placebo | file's "20 of 29 vs 0 of 29" exact match | VERIFIED |
| Agalsidase alfa (RCT) | PMID 11386930 | Schiffmann, JAMA 2001, 26 hemizygous males, reduced BPI pain, mesangial widening, ~50% GSL drop | claimed results match abstract; "not FDA approved" correct | VERIFIED |
| Migalastat (FACETS) | PMID 27509102 / NCT00925301 | Germain, NEJM 2016; NCT = AT1001/migalastat, amenable GLA variants | match; mutation-gating correct | VERIFIED |
| Pegunigalsidase (BALANCE) | PMID 37940383 / NCT02795676 | Wallace, J Med Genet 2024; NCT = PRX-102 vs agalsidase beta, renal, non-inferiority | match | VERIFIED |
| Lentiviral HSC GT (precedent + discovery) | PMID 33633114 | Khan, Nat Commun 2021, first-in-human lentiviral Fabry GT | match | VERIFIED |
| LNP mRNA aGalA (precedent + discovery) | PMID 30879639 | Zhu, Am J Hum Genet 2019, systemic mRNA Fabry, mice + NHP | match | VERIFIED |
| FLT190 AAV (discovery prose) | PMID 36631545 | Jeyakumar, Gene Ther 2023, FLT190 AAVS3/GLA liver-directed, preclinical, NCT04040049 in trial | match, incl. "in early-phase clinical evaluation" | VERIFIED |
| Lucerastat (MODIFY, discovery) | PMID 41519901 / NCT03425539 | Nordbeck, Nat Commun 2026; abstract: FAILED neuropathic pain primary endpoint (p=0.32), lowered plasma Gb3 (p<0.0001) | file honestly states "did not meet its neuropathic pain primary endpoint" | VERIFIED |
| Venglustat (discovery prose) | PMID 36481125 | Deegan, Mol Genet Metab 2022, open-label phase 2 3-yr classic Fabry males | match | VERIFIED |
| GCS inhibitor + ERT (discovery prose) | PMID 25938659 | Ashe, Mol Med 2015, Genz-682452 crosses BBB, additive to ERT in Fabry mice | match | VERIFIED |

## pompe_disease.json — VERIFIED

| Item | ID | Resolved source | Match | Verdict |
|---|---|---|---|---|
| Alglucosidase alfa (infantile) | PMID 17151339 | Kishnani, Neurology 2007; abstract: 100% survived to 18 mo, risk of death reduced 99%, death/invasive vent 92% | file's "99%/92%" exact match | VERIFIED |
| Avalglucosidase (COMET) | PMID 34800399 / NCT02782741 | Diaz-Manera, Lancet Neurol 2021; abstract: FVC% LS-mean 2.89 vs 0.46, non-inferior, superiority NOT reached (p=0.063), 6MWT gain | file "2.89 vs 0.46; superiority not reached" exact match | VERIFIED |
| Cipaglucosidase+miglustat (PROPEL) | PMID 34800400 / NCT03729362 | Schoser, Lancet Neurol 2021; abstract: 6MWD 20.8 m vs 7.2 m, superiority NOT achieved | file "20.8 m vs 7.2 m; did not reach superiority" exact match | VERIFIED |
| Onasemnogene SMA precedent | PMID 29091557 | Mendell, NEJM 2017, AAV9 SMN1 gene replacement | match | VERIFIED |
| Nusinersen SMA precedent | PMID 29091570 | Finkel, NEJM 2017, ENDEAR | match | VERIFIED |
| Patisiran precedent | PMID 29972753 | see hATTR | match | VERIFIED |
| AAV1 GAA diaphragm (discovery) | PMID 27453480 | Smith, Exp Neurol 2016; abstract: first-in-human diaphragmatic AAV1-CMV-GAA in infantile Pompe | file "first in human AAV1 GAA to diaphragm" match | VERIFIED |
| GYS1 inhibitor MZ-101 (discovery) | PMID 38232139 | Ullman, Sci Transl Med 2024, GYS1 inhibitor SRT in Pompe model, additive to ERT | match | VERIFIED |

## Notes / minor observations (not flags)
- Some citation LABELS attach a pivotal-era or class-evidence paper rather than the drug's own registration paper (e.g., velaglucerase alfa cites the Weinreb 2002 registry as "class evidence for recombinant GCase infusion"; patisiran precedent cites APOLLO). In every case the file text discloses this framing, the cited paper is real, and the claim is not overstated. Not flagged.
- The file DOIs match PubMed's returned DOIs in every checked case (spot-verified: NEJMoa1716153, NEJMoa1716793, NEJMoa1805689, NEJMoa2107454, NEJMoa1510198, s41467-025-68256-5, etc.).
- Forward-looking Huntington NCTs use the new NCT073/074 numbering (2025-2026 registrations) and all three resolve to real, recruiting studies with matching drug/phase/eligibility.
- Discovery-only named assets without a resolvable primary ID are already flagged "UNVERIFIED" inside the files themselves (e.g., specific AAV9 GBA1 PD program in Gaucher; specific clinical GT durability in Fabry/Pompe); those self-flags are appropriate and honest.

## Per-file verdict summary
- hereditary_attr_amyloidosis.json: VERIFIED (7/7 items)
- gaucher_disease.json: VERIFIED (9/9)
- huntington_disease.json: VERIFIED (16/16); honesty/tominersen-failure framing confirmed accurate
- fabry_disease.json: VERIFIED (11/11)
- pompe_disease.json: VERIFIED (8/8)

Non-VERIFIED items: NONE.

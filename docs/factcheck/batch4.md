# Batch 4 Fact-Check: Rare Disease Gene / Antisense / Cell Therapy Dossiers

Independent adversarial verification. Every PMID resolved via the PubMed plugin; every NCT resolved via the ClinicalTrials.gov v2 API; regulatory / withdrawal / "first-in-class" claims cross-checked via web search. Reviewer did not trust dossier content; each identifier was resolved from scratch.

Files reviewed (all under `examples/rare_disease/`):
`spinal_muscular_atrophy.json`, `duchenne_muscular_dystrophy.json`, `cystic_fibrosis.json`, `sickle_cell_disease.json`, `rpe65_retinal_dystrophy.json`.

## Causal gene sanity check (all correct)

| Disease | Gene claimed | Correct? |
|---|---|---|
| Spinal muscular atrophy (5q) | SMN1 loss, SMN2 copy-number modifier | VERIFIED |
| Duchenne muscular dystrophy | DMD / dystrophin (Xp21.2) | VERIFIED |
| Cystic fibrosis | CFTR (7q31.2), Phe508del / G551D classes | VERIFIED |
| Sickle cell disease | HBB c.20A>T p.Glu6Val | VERIFIED |
| RPE65 retinal dystrophy / LCA2 | RPE65 isomerohydrolase | VERIFIED |

## Citation-by-citation resolution

### PMIDs (all resolved; title, journal, year, drug/disease all MATCH)

| PMID | Resolved title (abbrev.) | Journal / year | 1st author | Used for | Verdict |
|---|---|---|---|---|---|
| 29091557 | Single-Dose Gene-Replacement Therapy for SMA | NEJM 2017 | Mendell | onasemnogene / AAV9 SMN1 | VERIFIED |
| 29091570 | Nusinersen vs Sham in Infantile-Onset SMA (ENDEAR) | NEJM 2017 | Finkel | nusinersen | VERIFIED |
| 33626251 | Risdiplam in Type 1 SMA (FIREFISH) | NEJM 2021 | Baranello | risdiplam | VERIFIED |
| 29972753 | Patisiran, an RNAi Therapeutic, for hATTR | NEJM 2018 | Adams | patisiran precedent | VERIFIED |
| 33283989 | CRISPR-Cas9 for SCD and beta-thalassemia | NEJM 2020 (online) | Frangoul | exa-cel proof-of-concept | VERIFIED (year note below) |
| 31597037 | Patient-Customized Oligonucleotide (milasen) | NEJM 2019 | Kim | milasen ASO precedent | VERIFIED |
| 16770791 | Reading-frame rule, Leiden DMD database | Muscle Nerve 2006 | Aartsma-Rus | frame rule | VERIFIED |
| 39385046 | AAV gene therapy for DMD: EMBARK phase 3 | Nat Med 2024 | Mendell | delandistrogene | VERIFIED |
| 33999469 | Utrophin modulator drugs for DMD/BMD | Neuropathol Appl Neurobiol 2021 | Soblechero-Martin | utrophin hypothesis | VERIFIED |
| 26573217 | Eteplirsen vs historical control, ambulation | Ann Neurol 2016 | Mendell | eteplirsen | VERIFIED |
| 32139505 | Increased dystrophin with golodirsen | Neurology 2020 | Frank | golodirsen | VERIFIED |
| 32453377 | Viltolarsen phase 2, exon 53 | JAMA Neurol 2020 | Clemens | viltolarsen | VERIFIED |
| 34105177 | Casimersen safety/PK, exon 45 | Muscle Nerve 2021 | Wagner | casimersen | VERIFIED |
| 35381069 | Corticosteroid dosing regimens (FOR-DMD) | JAMA 2022 | Guglieri | corticosteroids | VERIFIED |
| 36036925 | Vamorolone vs placebo & prednisone (VISION-DMD) | JAMA Neurol 2022 | Guglieri | vamorolone | VERIFIED |
| 29187645 | Single-cut genome editing restores dystrophin (mouse) | Sci Transl Med 2017 | Amoasii | CRISPR DMD hypothesis | VERIFIED |
| 22047557 | CFTR potentiator in CF w/ G551D | NEJM 2011 | Ramsey | ivacaftor | VERIFIED |
| 25981758 | Lumacaftor-Ivacaftor, Phe508del homozygous | NEJM 2015 | Wainwright | luma/iva | VERIFIED |
| 31697873 | Elexacaftor-Tezacaftor-Ivacaftor, single Phe508del | NEJM 2019 | Middleton | Trikafta | VERIFIED |
| 34226157 | ASO for CFTR 3849+10kb C-to-T splicing | J Cyst Fibros 2021 | Oren | CF ASO hypothesis | VERIFIED |
| 26149841 | Repeated nebulised non-viral CFTR gene therapy ph2b | Lancet Respir Med 2015 | Alton | CF gene therapy hypothesis | VERIFIED |
| 37014818 | ELX-02 readthrough of G550X-CFTR | Am J Physiol Lung 2023 | Chen | readthrough hypothesis | VERIFIED (nuance below) |
| 13369537 | Chemical difference in sickle-cell globin | Nature 1956 | Ingram | founding molecular disease | VERIFIED |
| 31199090 | Phase 3 Voxelotor in SCD (HOPE) | NEJM 2019 | Vichinsky | voxelotor | VERIFIED |
| 7715639 | Hydroxyurea reduces painful crises (MSH) | NEJM 1995 | Charache | hydroxyurea | VERIFIED |
| 38661449 | Exagamglogene Autotemcel for Severe SCD | NEJM 2024 | Frangoul | exa-cel pivotal | VERIFIED |
| 27959701 | Crizanlizumab for pain crises (SUSTAIN) | NEJM 2016/2017 | Ataga | crizanlizumab | VERIFIED (year note below) |
| 30021096 | Phase 3 L-glutamine in SCD | NEJM 2018 | Niihara | L-glutamine | VERIFIED |
| 34898139 | Biologic & clinical efficacy of LentiGlobin | NEJM 2021/2022 | Kanter | lovo-cel | VERIFIED (year note below) |
| 34898140 | AML case after gene therapy for SCD | NEJM 2021 | Goyal | lovo-cel AML boxed-warning ref | VERIFIED |
| 34079130 | Base editing of HSCs rescues SCD in mice (Makassar) | Nature 2021 | Newby | base-editing hypothesis | VERIFIED |
| 28712537 | Voretigene neparvovec (AAV2-hRPE65v2) phase 3 | Lancet 2017 | Russell | voretigene | VERIFIED |
| 34031601 | Partial visual recovery after optogenetic therapy | Nat Med 2021 | Sahel | ChrimsonR precedent | VERIFIED |
| 32094925 | First-in-human RPGR gene therapy (AAV8-coRPGR) | Nat Med 2020 | Cehajic-Kapetanovic | RPGR hypothesis | VERIFIED |
| 37388818 | Durable vision improvement, sepofarsen ASO, CEP290 LCA | Am J Ophthalmol Case Rep 2023 | Cideciyan | sepofarsen hypothesis | VERIFIED |
| 36589710 | Base editing restores vision, RPE65 LCA mouse | Mol Ther Nucleic Acids 2022 | Jo | RPE65 base-editing hypothesis | VERIFIED |

All DOIs in the dossiers match the DOI returned by PubMed for the corresponding PMID (spot-checked all that carried an explicit DOI string; every one matched, e.g. NEJMoa1706198, NEJMoa1702752, NEJMoa2009965, S0140-6736(17)31868-8, s41591-021-01351-4, s41591-020-0763-1, omtn.2022.11.021, ajoc.2023.101873).

### NCTs (all resolved; drug + disease + phase MATCH)

| NCT | Trial (resolved) | Drug (resolved) | Verdict |
|---|---|---|---|
| NCT02193074 | ENDEAR, phase 3 | nusinersen (ISIS 396443 / Spinraza) | VERIFIED |
| NCT02122952 | Phase 1 gene transfer SMA type 1 | AVXS-101 / Zolgensma (onasemnogene) | VERIFIED |
| NCT02913482 | FIREFISH phase 2 | risdiplam (Evrysdi) | VERIFIED |
| NCT02310906 | SRP-4053 phase 1/2 | golodirsen | VERIFIED |
| NCT02740972 | NS-065/NCNP-01 phase 2 | viltolarsen | VERIFIED |
| NCT02500381 | ESSENCE phase 3 (SRP-4045 + SRP-4053) | casimersen + golodirsen | VERIFIED |
| NCT05096221 | EMBARK phase 3 | delandistrogene moxeparvovec (SRP-9001, Elevidys) | VERIFIED |
| NCT01603407 | FOR-DMD phase 3 | prednisone / deflazacort | VERIFIED |
| NCT03439670 | Vamorolone phase 2b | vamorolone | VERIFIED |
| NCT00909532 | VX-770 phase 3, G551D | ivacaftor | VERIFIED |
| NCT01807923 | Luma+Iva phase 3, F508del homozygous | lumacaftor/ivacaftor | VERIFIED |
| NCT03525444 | VX-445 phase 3, F/MF | elexacaftor/tezacaftor/ivacaftor | VERIFIED |
| NCT03036813 | GBT_HOPE phase 3 | voxelotor (GBT440) | VERIFIED |
| NCT03745287 | CTX001 phase 1/2/3, severe SCD | exagamglogene autotemcel (exa-cel) | VERIFIED |
| NCT02140554 | HGB-206 phase 1/2, severe SCD | lovotibeglogene autotemcel (BB305 LVV) | VERIFIED |
| NCT00999609 | RPE65 LCA phase 3 | voretigene neparvovec (AAV2-hRPE65v2) | VERIFIED |

### Regulatory / product / "first-in-class" claims (all independently confirmed)

| Claim | Verdict |
|---|---|
| Voretigene = first FDA-approved gene therapy for a genetic disease (2017, Luxturna) | VERIFIED (Spark/FDA language) |
| Exa-cel (Casgevy) = first approved CRISPR gene-editing therapy, Dec 8 2023, BCL11A enhancer | VERIFIED |
| Lovo-cel (Lyfgenia) approved Dec 8 2023, boxed warning for hematologic malignancy, BB305 / HbA-T87Q | VERIFIED |
| Eteplirsen FDA accelerated approval Sept 19 2016, exon 51 (~13% of DMD), dystrophin surrogate | VERIFIED |
| Vamorolone (Agamree) FDA approved Oct 2023, first-in-class dissociative steroid, MR antagonism | VERIFIED |
| Voxelotor voluntarily withdrawn worldwide by Pfizer in 2024 (VOC / fatal-event imbalance) | VERIFIED |
| Crizanlizumab: STAND confirmatory trial no benefit; EMA CHMP revocation recommendation 2023 | VERIFIED |
| Numeric efficacy figures (voxelotor 51% Hb response at 1500 mg; crizanlizumab high-dose 5 mg/kg; eteplirsen +151 m 6MWT at 36 mo; voretigene MLMT phase 3; Newby ~80% Makassar conversion) | VERIFIED against abstracts, not overstated |

## Minor / non-blocking notes (NOT fabrications, NOT overstatements)

1. **Frangoul CRISPR proof-of-concept year (PMID 33283989).** PubMed dates it 2020-12-05 (online 2020; print Jan 2021). The SMA and CF dossiers cite it as "N Engl J Med 2021," the DMD dossier as "N Engl J Med 2020," and the SCD dossier body as "Frangoul et al. 2021, PMID 33283989." Both 2020 and 2021 are defensible (online vs print); the citation is internally inconsistent across files but the PMID, authors, journal, and topic are all correct. Cosmetic only.

2. **Crizanlizumab SUSTAIN year (PMID 27959701).** PubMed print date is 2016-12-03 (Dec 2016 issue). Dossier labels it "Ataga et al., N Engl J Med 2017." The article is commonly cited as 2017; PMID/topic correct. Cosmetic.

3. **Kanter LentiGlobin year (PMID 34898139).** PubMed dates it 2021-12-12; dossier says "Kanter et al., N Engl J Med 2022." Widely cited as 2022 (print). Cosmetic.

4. **ELX-02 readthrough citation (PMID 37014818).** The resolved paper is specifically about the **G550X**-CFTR nonsense allele ("superfunctional protein"), while the dossier text describes it generically as "readthrough of a CFTR nonsense mutation ... enhanced by CFTR modulators." Accurate in substance (it is a CFTR premature-stop readthrough enhanced by modulators); the dossier just does not name the specific G550X allele. Not an overstatement.

5. **Casimersen citation vs linked trial.** The prose citation (Wagner 2021, PMID 34105177) is the phase 1/2 dose-titration safety/PK paper, while the linked trial NCT02500381 is the pivotal phase 3 (ESSENCE). The dossier text explicitly says accelerated approval rested on "the ongoing pivotal program," so the pairing is transparent and correct, not misleading.

6. **NCT02140554 sponsor** shows as "Genetix Biotherapeutics Inc." in the registry record (bluebird bio predecessor entity); the trial is unambiguously the LentiGlobin/lovo-cel HGB-206 study (BB305 LVV, betaA-T87Q). Consistent with the Kanter 2022 citation.

## Per-file verdicts

- **spinal_muscular_atrophy.json** — VERIFIED. 3 therapies (nusinersen, onasemnogene, risdiplam) + 4 precedents + 4 discovery hypotheses. All PMIDs, NCTs, DOIs, gene biology, and approval statements correct. Note (1) applies.
- **duchenne_muscular_dystrophy.json** — VERIFIED. 7 therapies (eteplirsen, golodirsen, viltolarsen, casimersen, delandistrogene, corticosteroids, vamorolone) + precedents + 3 discovery hypotheses. All identifiers and approval facts correct. Notes (1),(5) apply. EMBARK phase-3 primary endpoint (NSAA) "not met" is stated accurately and honestly in the dossier.
- **cystic_fibrosis.json** — VERIFIED. 3 modulator regimens (ivacaftor, luma/iva, ETI) + precedents + 3 discovery hypotheses. All identifiers correct. Notes (1),(4) apply.
- **sickle_cell_disease.json** — VERIFIED. 6 therapies (hydroxyurea, L-glutamine, voxelotor, crizanlizumab, exa-cel, lovo-cel) + precedents + 3 discovery hypotheses. All identifiers, numeric results, and the voxelotor-withdrawal / crizanlizumab-STAND / lovo-cel-boxed-warning caveats correct and appropriately caveated. Notes (2),(3) apply.
- **rpe65_retinal_dystrophy.json** — VERIFIED. 1 therapy (voretigene) + precedents (onasemnogene, nusinersen, ChrimsonR optogenetic) + 4 discovery hypotheses (RPGR, sepofarsen/CEP290, RPE65 base editing, optogenetics). All identifiers correct; "first FDA-approved gene therapy for a genetic disease" confirmed.

## Bottom line

Across all 5 files: **36 unique PMIDs, 16 NCTs, and every DOI resolved and matched.** Zero FABRICATED, zero MISMATCH, zero UNRESOLVED, zero OVERSTATED items. All causal genes correct. All drugs are real approved products (or, for discovery-layer items, correctly labeled preclinical/early-clinical hypotheses) with the correct pivotal trial attached. The only findings are 6 cosmetic notes (online-vs-print citation years and one allele-specific vs generic phrasing), none of which is a factual error or an overstatement.

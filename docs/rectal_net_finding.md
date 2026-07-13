# A reproducible finding: rectal neuroendocrine tumors are not colorectal cancer

Anveshar research track submission. A discrete, reproducible multi-omics analysis run during the
hackathon on public data through the cBioPortal REST API. No simulated or subsampled data.

## Question

Rectal neuroendocrine tumors (NETs) are the most common gastrointestinal NET, yet they are rare
and lack their own trials, so they are often managed by extrapolation from colorectal
adenocarcinoma (same organ) or from pancreatic NET (same histology). Are rectal and GI NETs
molecularly the same as the adenocarcinoma of their organ, or the same as NETs of other organs?
The answer decides whether colorectal cancer therapy or NET therapy is the right frame.

## Data

All public, accessed live during the event via the cBioPortal REST API:

- MSK-IMPACT (Zehir et al., Nat Med 2017): 35 gastrointestinal well-differentiated NETs (rectum,
  gastrointestinal, small bowel, stomach, appendix).
- Pancreatic NET, ARC-Net (Scarpa et al., Nature 2017): 98 tumors, as a well-powered NET reference.
- TCGA colorectal adenocarcinoma (COADREAD PanCancer Atlas): 594 tumors.
- TCGA pancreatic adenocarcinoma (PAAD PanCancer Atlas): 184 tumors.

## Genomics: histology sets the driver landscape, not the organ

Driver mutation frequency (percent of tumors), from `rectal_net_genomics_driver_frequency_source.csv`:

| Gene | GI NET (n=35) | Pancreatic NET (n=98) | Colorectal adenoca (n=594) | Pancreatic adenoca (n=184) |
|---|---|---|---|---|
| APC | 2.9 | 1.0 | 65.2 | 2.2 |
| KRAS | 2.9 | 0.0 | 36.7 | 63.6 |
| TP53 | 5.7 | 3.1 | 52.9 | 58.2 |
| SMAD4 | 2.9 | 1.0 | 11.4 | 20.1 |
| PIK3CA | 0.0 | 0.0 | 24.7 | 2.7 |
| MEN1 | 5.7 | 36.7 | 1.3 | 1.6 |
| DAXX | 2.9 | 22.4 | 1.9 | 1.1 |
| ATRX | 2.9 | 10.2 | 6.1 | 1.6 |
| CDKN1B | 20.0 | 0.0 | 0.8 | 0.0 |
| TSC2 | 8.6 | 2.0 | 2.9 | 1.1 |

Two patterns separate cleanly. Adenocarcinomas, colorectal and pancreatic alike, are dominated by
APC, KRAS, TP53, and SMAD4, the canonical epithelial drivers. Both NET cohorts essentially lack
these and instead carry MEN1, DAXX, ATRX, CDKN1B, and TSC2, the chromatin and mTOR pathway genes
of neuroendocrine biology. GI NET is defined here by CDKN1B (20 percent), a known small intestine
NET driver (Francis et al., Nat Genet 2013), while pancreatic NET is defined by MEN1, DAXX, and
ATRX (Jiao et al., Science 2011; Scarpa et al., Nature 2017). A rectal NET shares its driver set
with a pancreatic NET, not with the colorectal adenocarcinoma sitting a few centimeters away. See
`rectal_net_genomics_driver_dichotomy.pdf`.

## Transcriptomics: the neuroendocrine program is absent from colorectal cancer

In TCGA colorectal adenocarcinoma (n=592), a neuroendocrine score (mean mRNA z of CHGA, SYP,
INSM1, SSTR2, ASCL1, NEUROD1) is neuroendocrine-high in only 3.7 percent of tumors, the rare
colorectal neuroendocrine carcinoma and mixed neoplasm tail. Ordinary colorectal adenocarcinoma is
not a neuroendocrine tumor, while a rectal NET is neuroendocrine by definition (WHO diagnostic
criteria require chromogranin A and synaptophysin positivity). See
`rectal_net_transcriptomics_ne_score.pdf`.

## Therapeutic consequence

Because rectal and GI NETs lack APC, KRAS, TP53, BRAF, and mismatch repair loss, the colorectal
cancer toolkit (fluoropyrimidine chemotherapy, anti-EGFR antibodies, BRAF inhibition, and MSI
directed immunotherapy) has no molecular basis in them. Their actionable feature is the
neuroendocrine program itself: somatostatin receptor 2 (SSTR2), the target of Ga-68 DOTATATE
imaging and Lu-177 DOTATATE peptide receptor radionuclide therapy, which improved outcomes in
gastroenteropancreatic NET (Strosberg et al., N Engl J Med 2017). The molecular data reproducibly
say a rectal NET should be worked up and treated as a NET, not as colorectal cancer. This is the
same conclusion Anveshar reaches from cross-condition reasoning, here confirmed from primary data.

## Limitations

Rectal-NET-specific public cohorts are small (4 well-differentiated rectal NET in MSK-IMPACT,
pooled into 35 GI NET), so pancreatic NET serves as the well-powered NET reference. The genomic
contrast is corroborated by dedicated rectal NET studies (Li et al., Endocr Relat Cancer 2023,
whole exome of 18 rectal NET; Duan et al., Cancer Med 2023; van Riet et al., Nat Commun 2021,
whole genome of 85 neuroendocrine neoplasms). mRNA z-scores are within-study normalized, so the
transcriptomic claim is made within colorectal adenocarcinoma rather than as a cross-cohort
comparison.

## Reproducibility

One script, `examples/multimodal/rectal_net_multiomics/` (plus the transcriptomic panel), runs in a
few minutes against the public cBioPortal API and writes the figures and source CSVs. Rerunning
reproduces every number above.

## Written summary (for submission)

Rectal neuroendocrine tumors are rare and are often managed by analogy to colorectal cancer. Using
public data through the cBioPortal API, we show they should not be. Across MSK-IMPACT gastrointestinal
NET, pancreatic NET, and TCGA colorectal and pancreatic adenocarcinoma, the driver landscape tracks
histology, not organ: adenocarcinomas are dominated by APC, KRAS, TP53, and SMAD4, while both NET
cohorts lack these and carry MEN1, DAXX, ATRX, CDKN1B, and TSC2. Transcriptomically, the
neuroendocrine program is neuroendocrine-high in only 3.7 percent of colorectal adenocarcinomas.
The consequence is therapeutic: rectal NET has no molecular basis for the colorectal cancer toolkit
and instead presents SSTR2, the target of Lu-177 DOTATATE. The analysis is reproducible in minutes
and corroborates Anveshar's cross-condition recommendation from primary data.

## Citations

MSK-IMPACT: Zehir et al., Nat Med 2017, doi:10.1038/nm.4333. Pancreatic NET: Scarpa et al., Nature
2017, doi:10.1038/nature21063; Jiao et al., Science 2011, doi:10.1126/science.1200609. Small
intestine NET CDKN1B: Francis et al., Nat Genet 2013, doi:10.1038/ng.2821. Rectal NET sequencing:
Li et al., Endocr Relat Cancer 2023, doi:10.1530/ERC-22-0257; Duan et al., Cancer Med 2023,
doi:10.1002/cam4.6281; van Riet et al., Nat Commun 2021, doi:10.1038/s41467-021-24812-3. Lu-177
DOTATATE: Strosberg et al., N Engl J Med 2017, doi:10.1056/NEJMoa1607427.

## Disclaimer

This is a research and educational analysis of public cohort data, not medical advice. It describes
tumor biology at the group level and does not describe any individual. Every diagnostic and
treatment decision must be made by a qualified health care provider, ideally within a clinical trial.

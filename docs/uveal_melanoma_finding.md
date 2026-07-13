# A reproducible finding: in uveal melanoma, integrated multi-omics beats mutation calls for risk

Anveshar research track. A discrete, reproducible integrative multi-omics analysis run during the
hackathon on public data (TCGA-UVM) through the cBioPortal REST API. No simulated or subsampled data.

## Question

Uveal melanoma is a rare cancer with a well-known prognostic split: the class 2, BAP1-deficient,
monosomy-3 tumors metastasize, the class 1 tumors usually do not. In practice, risk is often read
from a single marker (a BAP1 mutation call, or monosomy 3). Does an integrated multi-omic readout
(DNA copy number plus transcriptome plus proteome) capture metastatic risk better than any single
marker, and if so, why?

## Data

TCGA uveal melanoma (Robertson et al., Cancer Cell 2017), 80 tumors, all layers on the same
samples, accessed live during the event via cBioPortal: mutations, copy number (GISTIC), RNA-seq
z-scores, reverse phase protein array (RPPA), and overall survival.

## Method

An integrated multi-omic class was assigned by unsupervised clustering of tumors on a published
prognostic transcriptional signature (the DecisionDx-UM class-discriminating genes; Onken et al.).
The class was then aligned with DNA features (BAP1 mutation, monosomy 3 as GISTIC loss at the BAP1
locus, 8q gain, and the class-1 markers SF3B1 and EIF1AX), and with BAP1 at the mRNA and protein
level. Overall survival was compared by log-rank, for the integrated class and, separately, for
BAP1 mutation alone.

## Finding

The integrated multi-omic class and the single mutation marker do not agree, and the integrated
class is far more informative.

Survival:

| Stratifier | log-rank chi-square | p |
|---|---|---|
| Integrated multi-omic class (n=37 vs 43) | 21.9 | 2.9e-6 |
| BAP1 mutation alone | 0.4 | 0.54 |

The integrated class separates survival strongly, while BAP1 mutation status alone does not separate
it at all. The reason is that BAP1 point mutation captures only a minority of functional BAP1 loss:

| Feature | Class 1 | Class 2 (high risk) |
|---|---|---|
| BAP1 mutation | 0% | 30% |
| Monosomy 3 | 8% | 95% |
| 8q gain | 57% | 93% |
| SF3B1 mutation | 41% | 7% |
| EIF1AX mutation | 24% | 2% |
| BAP1 mRNA, median z | -0.26 | -2.48 (p=6e-12) |
| BAP1 protein RPPA, median z | +0.71 | -1.32 (p=0.003) |

Seventy percent of the high-risk class 2 tumors carry no BAP1 point mutation, yet 95 percent have
lost the chromosome 3 copy and both BAP1 mRNA and BAP1 protein are strongly reduced. Functional
BAP1 loss in uveal melanoma is therefore delivered mostly through monosomy 3 and expression, not
through point mutations that a sequencing panel would report, which is exactly why mutation-only
risk assessment fails here (p=0.54) while the integrated readout succeeds (p=2.9e-6). The class-1
markers SF3B1 and EIF1AX are mutually skewed to the good-prognosis class, as expected.

## Why it matters

Uveal melanoma risk stratification should be multi-omic, not mutation-only. Reading BAP1 by point
mutation alone misclassifies most high-risk tumors; adding copy number (monosomy 3) and BAP1
mRNA or protein recovers them. This is a general caution for any tumor where the driver is
inactivated by copy loss or silencing rather than by a reported mutation, and it is directly
testable and reproducible from public data. The first therapy to improve survival in metastatic
uveal melanoma is tebentafusp (Nathan et al., N Engl J Med 2021), so identifying the high-risk
class correctly has a real downstream consequence.

## Reproducibility

One script, `examples/multimodal/uveal_melanoma_integrative/uvm_integrative.py`, runs in a few
minutes against the public cBioPortal API and writes the figures, the class alignment table, and a
run log. Rerunning reproduces every number above.

## Written summary (for submission)

In uveal melanoma (TCGA-UVM, n=80, all omic layers, via cBioPortal), we assigned an integrated
multi-omic class from a prognostic transcriptional signature and tested it against survival. The
integrated class predicted overall survival strongly (log-rank p=2.9e-6), while BAP1 mutation alone
did not (p=0.54). The reason is mechanistic: 95 percent of high-risk class 2 tumors have monosomy 3
with reduced BAP1 mRNA (p=6e-12) and protein (RPPA, p=0.003), but only 30 percent carry a BAP1
point mutation. Functional BAP1 loss is delivered by copy loss and expression, not by reportable
mutations, so mutation-only risk assessment fails while integrated multi-omics succeeds. The
analysis reruns in minutes from public data.

## Citations

TCGA-UVM: Robertson et al., Cancer Cell 2017, doi:10.1016/j.ccell.2017.07.003. BAP1 in metastatic
uveal melanoma: Harbour et al., Science 2010, doi:10.1126/science.1194472. Prognostic class
signature: Onken et al., Cancer Res 2004, doi:10.1158/0008-5472.CAN-04-1750. SF3B1 and EIF1AX good
prognosis: Yavuzyigitoglu et al., Ophthalmology 2016, doi:10.1016/j.ophtha.2016.01.023. Tebentafusp:
Nathan et al., N Engl J Med 2021, doi:10.1056/NEJMoa2103485.

## Disclaimer

This is a research and educational analysis of public cohort data, not medical advice. It describes
tumor biology at the group level and does not describe any individual. Every diagnostic and
treatment decision must be made by a qualified health care provider, ideally within a clinical trial.

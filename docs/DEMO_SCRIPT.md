# Demo video script and run of show

Built with Claude, Life Sciences hackathon. Target length 2:45 (a 60-second cut is at the end).
Working product name is "Anveshar"; swap for your final name (for example Anvesha, or Nayab AI)
with a find and replace before recording.

Record the screen while you narrate. Show real clicks in the live artifacts, not slides. 1080p,
show the cursor, add captions. Links to open are listed in the run of show.

---

## Run of show (2:45)

| Time | On screen (do this) | Say this (verbatim) |
|---|---|---|
| 0:00-0:18 | Open the **hub** artifact (the landing page with the moving network). Let it breathe. | "Every year, thousands of people are told they have a cancer so rare it has no dedicated trial and no standard treatment. But very often the answer already exists, in a different cancer that shares the exact same molecular dependency. Anveshar finds it." |
| 0:18-0:40 | From the hub, click **Rare cancer dependency atlas**. Type "renal medullary" in the search box. | "Anveshar is a research tool for rare cancers. It catalogs five hundred and four of them, searchable by name, by gene, by organ system, even by potential cause. Say a patient has renal medullary carcinoma, an ultra rare, aggressive kidney cancer." |
| 0:40-1:10 | Open the **renal medullary carcinoma report**. It opens in Researcher view. Scroll to the therapies; hover the confidence bar; point at a citation link; scroll to "Evidence databases queried". Toggle to **Patient** view for one second. | "Anveshar returns a cited, confidence scored report, in three registers: researcher, clinician, and patient. Its driver is loss of SMARCB1. That same loss makes the tumor depend on EZH2, which is drugged by tazemetostat, approved in a different sarcoma. Every therapy carries a confidence score and a real citation, and you can see the exact databases Anveshar queried to build this." |
| 1:10-1:35 | Open the **analyses** artifact. Point at the actionability count, then the "highest unmet need" red chips (TP53, EWSR1). | "Across all rare cancers, ninety nine already have a borrowable approved therapy. And Anveshar flags the highest leverage gaps: the dependencies like TP53 and EWSR1 that drive many rare cancers but have no drug yet. Every number is cited and scored." |
| 1:35-2:05 | Open the **harness run** artifact. Scroll through the 7 workflow stages, then the target validation table (SMARCB1 42, EZH2 95), then the provenance table. | "The pipeline is reproducible and provenance tracked. It resolves the driver, then validates the target with live functional genomics from Open Targets and DepMap. SMARCB1 itself is a common essential gene you cannot drug, so the harness pivots to its synthetic lethal partner EZH2, which scores as a validated, tractable target. Every step is logged and auditable." |
| 2:05-2:30 | Open the **multi-modal** artifact. Let the bar charts render. Point at the GNAQ/GNA11 chart, then the clinical sequencing cohort numbers. | "And it is grounded in real data. On a cluster, Anveshar analyzed TCGA uveal melanoma across genomics, transcriptomics, and imaging, and mapped a clinical sequencing cohort's almost eleven thousand sequenced tumors onto the rare cancer catalog. The driver frequencies it recovers reproduce the known biology, exactly." |
| 2:30-2:45 | Return to the **hub**. End on the title. | "Anveshar is built with Claude, using its agents, skills, and connected databases. It extends to every rare disease and to gene therapies, and every claim is traceable to a source. It is decision support for research, not medical advice; the final decision always rests with a health care provider. Built by Dig Vijay Kumar Yarlagadda." |

---

## Links to open, in order

1. Hub: https://claude.ai/code/artifact/21dd72b9-0696-4402-a72a-9a365b3094d6
2. Atlas: https://claude.ai/code/artifact/352952a9-3871-4d50-9675-7e12a15872d6
3. Report (renal medullary carcinoma): https://claude.ai/code/artifact/bec29cdd-185d-4554-a0c2-9857cecae835
4. Analyses: https://claude.ai/code/artifact/b0d976b0-6971-4fcd-b7b4-af05872ddb3d
5. Harness run: https://claude.ai/code/artifact/2cf816b4-390a-4a7e-b6b9-22ba6291222f
6. Multi-modal: https://claude.ai/code/artifact/bdf14ffd-3f17-42be-bf1b-4e34fcda949c

---

## 60-second cut (if the platform caps at one minute)

On screen: hub, then atlas search, then report, then harness run, then hub.

"Thousands of people get a cancer too rare to have its own trial. But the treatment often exists
already, in another disease with the same molecular dependency. Anveshar finds it. It catalogs
five hundred and four rare cancers and, for each, returns a cited, confidence scored report that
borrows therapies proven elsewhere. It is a reproducible pipeline: it validates each target with
live Open Targets and DepMap functional genomics, and pivots an undruggable tumor suppressor
to its synthetic lethal partner. It is proven on real TCGA and clinical sequencing data data, extends to all
rare diseases, and every claim is cited. Built with Claude. Decision support for research, not
medical advice."

---

## Recording checklist

1. Tool: Loom, QuickTime screen recording, or OBS. Loom is fastest and gives a shareable link.
2. Rehearse twice; the narration above is timed for about 150 words per minute.
3. Record at 1920x1080, show the cursor, and slow your clicks so the viewer can follow.
4. Let animated elements (the hub network, the multi-modal charts) finish rendering before you talk over them.
5. Add captions (Loom and CapCut auto-generate them); many judges watch muted.
6. Keep the disclaimer line in; it signals responsibility and is required for health tools.
7. Export and keep it under the platform's time limit. Put the hub URL in the submission description.

---

Developer: [digvijayky](https://digvijayky.com)

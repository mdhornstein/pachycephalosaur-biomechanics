# Independent Literature Audit — *Stegoceras* Biomechanics + UQ

**Audit target:** repository `mdhornstein/pachycephalosaur-biomechanics` at commit `473d978`  
**Commit:** `473d978` — `docs: organize literature directory into dossiers, protocols, and synthesis`  
**Audit date:** 2026-09-23  
**Role:** independent scientific reviewer; this document is a challenge audit, not a co-author synthesis.

## Audit scope and evidence standard

This audit treats commit `473d978` as the starting corpus and independently checks major claims against original papers or authoritative bibliographic records where those were retrievable. The principal reviewed materials are:

- `literature/stegoceras_biomechanics_literature_synthesis.md`
- `literature/dossiers/feafem_paleontology_scoping_review.md`
- `literature/dossiers/pachycephalosaur_stegoceras_ualvp2_dossier.md`
- `literature/dossiers/uq_sensitivity_computational_biomechanics_scoping_review.md`
- the associated evidence-matrix structure and selected rows added in the commit
- the commit-level file manifest and epistemic coding rules

Primary-source checks included the original Snively & Cox (2008), Snively & Theodor (2011), Schott et al. (2011), Goodwin & Horner (2004), Peterson et al. (2013), Woodruff & Ackermans (2026 issue / 2024 first online), Bateman & Larsson (2026), Bright & Rayfield (2011), McCurry et al. (2015), Baugnon et al. (2026), and other cited records where accessible.

**Important limitation:** this is an independent audit of the literature-review work, not a fresh systematic review of every biomechanical paper ever published. A number of records in the corpus are explicitly marked `UNVERIFIED`; those are preserved as such here rather than being silently filled from memory. Not every CSV row received a primary-paper re-read.

## 1. Executive audit

### Major strengths

1. **The review architecture is unusually explicit about epistemic status.** The `DO / AI / MA / IN / SYN / UNVERIFIED` vocabulary is useful and, in principle, exactly the distinction needed for a fossil FE project. The master review also correctly warns that absence from the corpus is not evidence of absence and treats novelty statements conservatively.

2. **The central numerical-vs-biological distinction is mostly correct.** The review repeatedly separates mesh/discretization uncertainty from geometry, material, loading, boundary-condition, and model-form uncertainty. The statement that mesh convergence is verification rather than physical validation is methodologically sound.

3. **The review is appropriately skeptical about behavioral inference.** Snively & Cox (2008) and Snively & Theodor (2011) are generally represented as demonstrations of modeled mechanical plausibility/capability rather than direct behavioral observations. The 2024/2026 Woodruff & Ackermans review is also appropriately used to warn that “headbutting” collapses multiple distinct behaviors and contact geometries.

4. **The UALVP 2 benchmark is correctly identified as a rare specimen-specific precedent.** Snively & Theodor (2011) did directly analyze the UA 2 / UALVP 2 *Stegoceras* model, including a 2.2-million-element tetrahedral model, the Austin high-resolution CT dataset, the 1360 N benchmark load, multiple load-spread scenarios, and explicit acknowledgment of fossilization/beam-hardening and constraint artifacts.

5. **The review correctly resists “more UQ is automatically better.”** The proposed progression from deterministic verification to targeted sensitivity and, only where justified, probabilistic/global methods is much more defensible than imposing Bayesian calibration, Gaussian-process emulation, or active learning from the outset.

### Major weaknesses

1. **There are real bibliographic errors, not just missing metadata.** Most importantly, the dossier conflates two different Robert M. Sullivan publications and gives the wrong year/journal/pages for the *Stegoceras* revision; the pathology paper has the wrong authors in one dossier entry; and the master reference key mislabels the journal for Dumont et al. (2009).

2. **“Validation” is used too loosely in the prior-model table.** The 2011 comparison of *Stegoceras* with extant artiodactyls is comparative biological corroboration, not experimental/physical validation of the FE model. The extant taxa were not used as ground-truth strain measurements for UALVP 2. This is the most consequential terminology correction in the whole corpus.

3. **The material-property discussion still risks making scalar Young’s modulus look more primary than the evidence supports.** UALVP 2 has visibly heterogeneous internal architecture; Snively & Theodor explicitly treated fossilization and beam hardening as obstacles to literal CT-to-stiffness mapping. A single homogeneous `E` should therefore be a deliberate simplified model-form branch, not the default representation of “material uncertainty.” Spatial architecture and zonation should be characterized first, followed by uncertainty in the properties of those regions and in the mapping itself.

4. **The proposed uncertainty taxonomy is better than the proposed parameterization.** The review correctly lists load/contact, BCs, geometry, segmentation, materials, and model form. However, several of these need stronger prioritization based on specimen-specific evidence. Contact/load spread and BCs have direct precedent in the 2011 model; anisotropy and suture mechanics are much less constrained and should not automatically become first-tier UQ parameters.

5. **Some methodological statements are stronger than the cited evidence warrants.** Examples include arbitrary numerical prescriptions such as a “4–6 tier” refinement ladder, broad statements implying comparative trends are generally robust to uncertain material properties, and language that could be read as treating 2011 comparative analysis as validation.

### Most important corrections

- Correct Sullivan’s *Stegoceras* bibliography: the genus revision is **Sullivan 2003, Journal of Vertebrate Paleontology 23(1):181–207**, DOI `10.1671/0272-4634(2003)23[181:ROTDSL]2.0.CO;2`; Sullivan 2006 is a different taxonomic review in *New Mexico Museum of Natural History and Science Bulletin* 35:347–365.
- Correct Peterson et al. (2013) authors everywhere: **Joseph E. Peterson, Collin Dischler, Nicholas R. Longrich**.
- Correct Dumont et al. (2009) to **Journal of Theoretical Biology 256:96–103**, not Journal of Experimental Biology.
- Replace phrases such as **“comparative validation”** for Snively & Theodor (2011) with **“comparative extant-taxon support / comparative functional corroboration.”**
- Treat `E = 1 GPa` in the Stegoceras cancellous region as a **model input adopted by Snively & Theodor**, not as a measured fossil-specific material property.
- Treat 1360 N as a **literature benchmark scenario**, not as an estimate of the actual force experienced by a living *Stegoceras*.
- Add the directly relevant high-resolution CT vascularity study of *Stegoceras* by **Nirody et al. (2022)** to the core UALVP 2 evidence base.

### Most consequential omissions

1. **Nirody et al. (2022), “Quantifying vascularity in the frontoparietal dome of *Stegoceras validum* from high resolution CT scans.”** This is directly relevant to internal architecture/vascularity and should sit next to Schott et al. (2011) and Snively & Theodor (2011) in the UALVP 2 core evidence chain.
2. The existing review has **Moore et al. (2022)** in the bibliography but under-integrates its postcranial/myological implications for the plausibility of whole-body stabilization and force transmission during head-strike behavior.
3. The review would benefit from a more explicit treatment of **load-case heterogeneity within extant “headbutting” taxa**, which Woodruff & Ackermans (2024/2026) now makes particularly important.
4. The model-form uncertainty section should more explicitly separate **sutural/interface behavior**, **anisotropy**, and **dynamic/contact mechanics** from ordinary scalar parameter uncertainty.

### Most important scientific uncertainties

- actual impact force history, duration, direction, and contact mechanics;
- living keratin-pad geometry and material properties;
- how fossilization and beam hardening affect any CT-based material mapping;
- biological neck/head support and effective boundary conditions;
- whether the current CT actually resolves all mechanically important internal architecture;
- which FE outputs are robust enough to interpret biologically;
- whether a static linear model is adequate for the particular question being asked.

---

# 2. Critical corrections table

| Severity | Claim/file | Problem | Evidence | Recommended correction |
|---|---|---|---|---|
| **Critical** | `pachycephalosaur_stegoceras_ualvp2_dossier.md`, P03 | Sullivan citation is wrong: it gives a 2006 *Journal of Vertebrate Paleontology* paper at 26(2):370–383. | The *Stegoceras* revision is Sullivan 2003, *Journal of Vertebrate Paleontology* 23(1):181–207, DOI `10.1671/0272-4634(2003)23[181:ROTDSL]2.0.CO;2`. Sullivan 2006 is a different taxonomic review in New Mexico Museum Bulletin 35:347–365. | Split these into two records. Cite Sullivan 2003 for the *Stegoceras* revision and Sullivan 2006 separately if needed for broader taxonomy. |
| **Critical** | `pachycephalosaur_stegoceras_ualvp2_dossier.md`, P07 | Wrong authors: “Peterson & Vittore (2013)” is not the 22% lesion-distribution paper. | The cited DOI `10.1371/journal.pone.0068620` is Peterson, Dischler & Longrich (2013), PLOS ONE 8:e68620. Peterson & Vittore is a different publication. | Correct authors and keep the DOI/title pair. Do not merge the two pathology studies. |
| **Important** | `stegoceras_biomechanics_literature_synthesis.md`, FE-17 | Master reference key says “Journal of Experimental Biology / related comparative methods record.” | The dossier itself gives Dumont, Grosse & Slater (2009), *Journal of Theoretical Biology* 256:96–103, DOI `10.1016/j.jtbi.2008.08.017`. | Normalize the master citation to *Journal of Theoretical Biology*. |
| **Important** | Master synthesis §5.3, “Validation / sensitivity” for Snively & Theodor 2011 | Extant comparison is called “comparative validation.” | Snively & Theodor compared simulated *Stegoceras* response with extant taxa and behavioral categories; they did not compare the UALVP 2 model against direct measured strain/deformation from the same specimen. | Use “comparative support,” “comparative functional evidence,” or “extant-analogue comparison,” not validation. |
| **Important** | Master synthesis §6.0–6.3 | Scalar material uncertainty can read as though homogeneous `E` is the primary material problem. | UALVP 2 CT showed distinct compact/trabecular architecture; Snively & Theodor explicitly noted unknown permineralization and beam hardening, manually assigned fossil properties, and used `E=1 GPa` for the cancellous region. | Establish spatial material architecture/regions first; then vary region-specific properties and CT-to-property mappings. Keep homogeneous-E as a simplified branch. |
| **Important** | Master synthesis §11, “4–6 tier refinement ladder” | The number 4–6 is a numerical prescription rather than a literature-supported requirement. | Bright & Rayfield (2011) used many refinement levels in a specific pig-cranium convergence experiment and showed that regions/outputs converge differently. | Define the stopping criterion first; use as many tiers as needed to demonstrate convergence, without making 4–6 a methodological rule. |
| **Important** | CT evidence matrix, EV-018 / S19 | “Recent 2026 microFE evidence…” is not traceable to a named bibliographic source in the evidence row. | The row gives “Recent microFE evidence” but no source citation. | Add a stable source ID/DOI and reclassify as `UNVERIFIED` until the primary paper is explicitly linked. |
| **Important** | Master synthesis §7, material decision | “Use heterogeneous/zonated representation where current CT and evidence support it” is sound, but its decision logic is not explicit enough. | CT/histology establish architecture; they do not establish fossil constitutive properties. | Separate (a) architecture/regions, (b) constitutive values, and (c) CT-to-property mapping uncertainty. |
| **Important** | Master synthesis §7, “comparative FEA can distinguish mechanical behavior … even when absolute tissue properties are uncertain” | Too broad as written. Material uncertainty can alter relative rankings depending on model structure and QoI. | Validation/sensitivity literature shows material and loading effects are model- and output-dependent. | State this as a conditional claim: comparative inference is possible only if uncertainty does not reverse the comparison for the specified QoI and scenario. |
| **Important** | Master synthesis §3 / §11 | “Freeze the FE-ready geometry/modeling pipeline” is correct for h-refinement, but not sufficient for all mesh studies. | Surface resolution is itself a sensitivity layer; volume-mesh refinement and surface-geometry sensitivity answer different questions. | State explicitly that h-refinement holds surface geometry, element formulation, material map, loads, BCs, and solver settings fixed. Perform separate surface-geometry sensitivity experiments. |
| **Important** | Snively & Theodor material description | The review sometimes compresses “CT-informed” and “measured” into one phrase. | The source says fossil density-to-stiffness mapping could not be fully automated because permineralization was unknown; some values were manually assigned. | Use “CT-informed/manual material assignment” rather than implying a calibrated fossil material law. |
| **Important** | Snively & Theodor baseline load | 1360 N could be misread as a biological force estimate. | The source explicitly says it was calculated for similarly sized *Homalocephale* at 3 m/s and was introduced to place the model in a biological context. | Call it a benchmark load case/scenario. Do not label it “actual impact force.” |
| **Minor** | Woodruff & Ackermans metadata | “2024 (issue 2026)” is historically accurate but awkward for a current bibliography. | Wiley lists first publication 4 July 2024; PubMed lists *Anatomical Record* 309(5):1235–1256 in May 2026. | Use final issue metadata in the bibliography and note “first published online 2024” only when publication chronology matters. |
| **Minor** | Several FE/UQ records | Exact DOI or pagination is marked `UNVERIFIED` in the master reference key. | The review correctly flags these but still sometimes presents the shortened citation as if bibliographically closed. | Keep `UNVERIFIED` visible until checked; do not promote these entries to “verified” through downstream summaries. |

---

# 3. Citation audit

## 3.1 Bibliographic errors

### Sullivan: two papers were conflated

The dossier’s P03 entry is the clearest bibliographic error in the corpus.

**What the corpus says:**
> Sullivan (2006), “Revision of the dinosaur *Stegoceras* Lambe…”, *Journal of Vertebrate Paleontology* 26(2), 370–383.

**What the primary/authoritative record shows:**

- **Sullivan, R. M. (2003).** “Revision of the dinosaur *Stegoceras* Lambe (Ornithischia, Pachycephalosauridae).” *Journal of Vertebrate Paleontology* **23(1):181–207**. DOI: `10.1671/0272-4634(2003)23[181:ROTDSL]2.0.CO;2`.
- **Sullivan, R. M. (2006).** “A taxonomic review of the Pachycephalosauridae (Dinosauria: Ornithischia).” *New Mexico Museum of Natural History and Science Bulletin* **35:347–365**.

These are different works. This matters because a specimen/taxonomic statement attributed to a “revision of *Stegoceras*” should point to the 2003 genus-level revision.

### Peterson et al. pathology paper: wrong authors in P07

The dossier gives “Peterson & Vittore (2013)” for the lesion-distribution study. The cited DOI `10.1371/journal.pone.0068620` is actually:

> Peterson, J. E., Dischler, C., & Longrich, N. R. (2013). “Distributions of Cranial Pathologies Provide Evidence for Head-Butting in Dome-Headed Dinosaurs (Pachycephalosauridae).” *PLOS ONE* 8(7):e68620. DOI: `10.1371/journal.pone.0068620`.

Peterson & Vittore is a separate pathology publication and should not be used interchangeably with the 22%-of-specimens / apex-clustering study.

### Dumont et al. journal mismatch in the master reference key

The master synthesis labels FE-17 as “Journal of Experimental Biology / related comparative methods record,” whereas the specialist FE dossier correctly identifies:

> Dumont, E. R., Grosse, I. R., & Slater, G. J. (2009). “Requirements for comparing the performance of finite element models of biological structures.” *Journal of Theoretical Biology* 256:96–103. DOI: `10.1016/j.jtbi.2008.08.017`.

The master key should be corrected to the peer-reviewed journal actually containing the paper.

### Bibliographic entries that should remain `UNVERIFIED`

The following were explicitly marked `UNVERIFIED` in the corpus and should not be silently promoted:

- exact DOI for Marinescu et al. (2005) in FE-06;
- exact DOI for Ross et al. (2005) in FE-07;
- exact DOI for Panagiotopoulou et al. (2010) in FE-09;
- exact DOI for Fitton et al. (2012) in FE-12;
- exact DOI for Cuff et al. (2015) in FE-16;
- exact DOI for Marcé-Nogué (2022) in FE-19;
- exact identifiers for several historical taxonomy records in BIO-01 through BIO-03;
- DOI/complete metadata for the historical Snively & Cox (2008) article should be represented by its stable article page rather than a guessed DOI.

That use of `UNVERIFIED` is good practice and should be retained until primary/authoritative records are checked.

## 3.2 Citation-to-claim mismatches or category errors

### “Validation” versus comparative inference

The review correctly states elsewhere that validation and convergence answer different questions, but its prior-model table undermines that distinction by describing the Snively & Theodor extant-taxon comparison as “comparative validation.”

The 2011 paper does **not** provide a physical strain-gauge or ex vivo deformation validation of the UALVP 2 skull. It provides:

- direct CT/anatomical observations;
- FE simulation;
- comparison with extant artiodactyl morphology and modeled mechanics;
- recursive partitioning of morphology/behavior correlations.

This is evidence for comparative biological interpretation, not solver/model validation in the V&V sense. The project should not inherit “validated” from that paper.

### “CT-based material properties” need a two-step qualification

Snively & Theodor did use CT Hounsfield values to inform material assignments in extant taxa, but for *Stegoceras* they explicitly said the densities could not be fully automated because permineralization was unknown. Above 2500 HU they assumed beam-hardening inflation, and the cancellous region was given `E = 1 GPa`.

Therefore the defensible description is:

> CT-informed / manually assigned material representation under fossilization and beam-hardening uncertainty.

It is not:

> experimentally measured CT-calibrated fossil elastic properties.

### “Safety factors” are model-relative, not organism-level failure margins

The 2011 paper reports safety factors under its chosen model properties and failure/ultimate-strain criteria. The project can reproduce these quantities, but should always phrase them as:

> “safety factor relative to the tissue-strength criterion adopted in the model.”

It should not be converted into a claim that UALVP 2 had a known biological safety margin in life.

### Apex/pathology evidence is not a load reconstruction

Peterson et al. (2013) provide systematic pathology frequency and location evidence. Those observations constrain behavioral hypotheses, but do not determine:

- impact energy;
- impact direction;
- contact time;
- contact area;
- peak force;
- whether an individual lesion arose from head-to-head impact rather than another trauma mechanism.

The dossier mostly respects this, but future synthesis should keep pathology in the “behavioral plausibility evidence” layer rather than using it as a quantitative loading calibration source.

### Ontogeny is correctly used but should not be converted into exact age

Schott et al. (2011) provide a quantitative *Stegoceras* growth series and include UALVP 2. This supports ontogenetic context and specimen-specific geometry interpretation. It does **not** establish a precise chronological age for UALVP 2 by itself. The synthesis correctly cautions against that overreach; that caution should remain explicit in future versions.

---

# 4. Missing-literature audit

## Essential

### Nirody et al. (2022) — quantitative vascularity from high-resolution CT

**Citation:** Nirody, J. A., Goodwin, M. B., Horner, J. R., Huynh, T. L., Colbert, M. W., Smith, D. K., & Evans, D. C. (2022). “Quantifying vascularity in the frontoparietal dome of *Stegoceras validum* (Dinosauria: Pachycephalosauridae) from high resolution CT scans.” *Journal of Vertebrate Paleontology* 41(5), e2036991. DOI `10.1080/02724634.2021.2036991`.

**Why it matters:** This paper is directly about *Stegoceras* dome internal vascular architecture using high-resolution CT. The current review makes several model-relevant claims about vascular canals, internal architecture, and the relation between histology and CT, but omits a directly relevant 2022 quantitative CT study from its core biological evidence chain.

**Question affected:** What internal structures are actually resolved in *Stegoceras* CT, how variable is vascularity, and which apparent low/high-density features are anatomically meaningful?

**Priority:** **Essential.**

### More explicit load-case diversity from the 2024/2026 headbutting review

Woodruff & Ackermans is already included, but its implications should be upgraded from a conceptual warning to an explicit modeling requirement: “headbutting” encompasses different striking surfaces, contact configurations and velocities among extant taxa. For a model that explores load direction/contact area, this review is central to the biological rationale for using a **family of load cases** rather than one canonical “headbutt.”

**Priority:** **Essential for the behavioral interpretation section.**

## Useful

### Moore et al. (2022) — appendicular myology of UALVP 2

The corpus cites this paper, but it is under-integrated. Moore et al. use UALVP 2 to reconstruct appendicular musculature and argue that multiple postcranial features would have strengthened/stabilized the pelvis, hindlimbs and tail in ways compatible with agonistic head-butting.

**Why it matters:** It provides a postcranial mechanics context missing from a cranial-only narrative. It does not prove head-butting, but it bears directly on whether a plausible whole-body mechanical chain exists.

**Priority:** **Useful; essential if the project claims whole-animal behavioral mechanics.**

### Schott et al. (2012) — squamosal ontogeny and variation

This paper provides additional specimen- and ontogeny-relevant context for *Stegoceras* skull geometry and peripheral cranial structures. It is not a substitute for Schott et al. (2011), but it can help distinguish genuine biological geometry variation from reconstruction artifacts.

**Priority:** **Useful.**

### Cross-taxon ontogeny and extreme cranial development

Horner & Goodwin (2009) on *Pachycephalosaurus* and related ontogenetic work can be useful for the broader evolutionary context of dome development, but it is less direct evidence for UALVP 2 than the *Stegoceras*-specific studies.

**Priority:** **Useful/optional depending on manuscript scope.**

## Optional

### Historical behavioral literature

Older behavioral proposals such as Carpenter’s work on agonistic behavior and earlier functional interpretations are useful for reconstructing the genealogy of the head-strike hypothesis. They become important if the project makes historical claims about how the hypothesis developed, but they are not necessary for the numerical FE/UQ core.

**Priority:** **Optional for methods-focused work; useful for a full paleobiological review.**

### Additional VVUQ/standards literature

The project already cites Roy & Oberkampf and Henninger et al. That is adequate for the core conceptual distinction. Standards/guidelines may be added later for reporting consistency, but they should not be allowed to substitute for biomechanics-specific primary evidence.

**Priority:** **Optional.**

---

# 5. Scientific-interpretation audit

## 5.1 Claims that are adequately supported

### “UALVP 2 has been directly modeled”

**Status:** Directly supported.

Snively & Theodor (2011) explicitly created a high-resolution *Stegoceras* model from the Austin CT dataset and used it as their primary *Stegoceras* FE model. They identify the specimen as UA 2. The project is therefore justified in treating UALVP 2 as a specimen-specific historical benchmark.

### “1360 N is a published benchmark”

**Status:** Directly supported.

The 2011 paper states that 1360 N was calculated for similarly sized *Homalocephale* at a closing speed of 3 m/s and applied as the Stegoceras baseline. This is a benchmark scenario, not an observed force.

### “Contact/load spread is an explicit uncertainty”

**Status:** Strongly supported.

Snively & Theodor varied the area of force application because the size/spread of a hypothetical keratin pad was unknown. This is unusually strong specimen-specific precedent for treating contact footprint as a primary scenario variable.

### “Constraint artifacts are real in the 2011 model”

**Status:** Directly supported.

The paper reports artificial stress concentrations at the occipital condyle constraint and near neurovascular canals. A modern model should therefore mask/flag such regions when selecting summary stress metrics.

## 5.2 Claims that need qualification

### “The dome can withstand substantial impact”

This is acceptable only with a model qualifier. The evidence is:

> Under the tested geometry, material assignments, constraints, load magnitudes and contact representations, the simulated stresses/strains did not exceed the criteria adopted in the study across the reported baseline scenarios.

That is materially different from:

> The living dome could withstand substantial impacts.

The second statement adds an unsupported leap across uncertain material properties, dynamics, and biological loading.

### “The architecture is protective / energy dissipative”

The FE model shows load transmission and stress/strain patterns consistent with energy storage/distribution under chosen conditions. But “protective” is an evolutionary-function claim, whereas “load-dispersing under a model” is a mechanical-description claim. The report should keep those separate.

### “The dome evolved for headbutting”

Not supported as a settled conclusion. The literature contains multiple interpretations:

- Snively & Cox (2008) and Snively & Theodor (2011) emphasize mechanical capability and comparative correlates consistent with head-strike behavior.
- Goodwin & Horner (2004) interpreted ontogenetic histology as inconsistent with head-butting as the primary function.
- Peterson et al. (2013) interpreted lesion frequency/distribution as evidence consistent with intraspecific butting.
- Woodruff & Ackermans (2024/2026) emphasize that the term “headbutting” contains distinct behavioral/mechanical possibilities.
- Moore et al. (2022) argue that postcranial morphology is compatible with stabilization/force transmission during agonistic head-butting.
- Bateman & Larsson (2026) introduce a feeding-performance trade-off hypothesis relevant to the evolutionary history of the dome.

The correct project-level conclusion is therefore that **mechanical capability is one component of a broader, still-contested behavioral/evolutionary inference**.

## 5.3 “Homogeneous E” should not be treated as the default unknown

This is the most important scientific interpretation issue for UQ.

UALVP 2 does not present the FE problem as a homogeneous bone block. Snively & Theodor reported compact and lower-density regions, internal trabecular architecture, and dense structures/canals. Goodwin & Horner provide independent histological evidence for zonation. Nirody et al. (2022) further quantify vascularity from high-resolution CT.

Therefore:

1. **Architecture uncertainty** comes first: what regions/interfaces exist and where?
2. **Constitutive uncertainty** comes second: what `E`, `ν`, failure criteria, and possibly anisotropy belong to each region?
3. **Mapping uncertainty** comes third: how, if at all, should CT intensity map to living-equivalent mechanical properties after fossilization?

A single homogeneous `E` can still be valuable as a **simplification/control model**, because it helps isolate the effect of heterogeneity. It should not, however, be treated as the natural probabilistic center of the material UQ problem.

## 5.4 Anisotropy

The corpus correctly lists anisotropy as a possible model-form uncertainty, but the evidence base is too weak to make it a primary UALVP 2 parameter.

Trabecular orientation provides a biological reason to consider directional behavior, but orientation does not by itself establish the orthotropic constitutive law, elastic constants, or scale required for an anisotropic FE model. A defensible sequence is:

- isotropic zonated baseline;
- sensitivity to region-specific isotropic properties;
- only then, if a specific scientific question demands it and architecture supports it, an anisotropic model-form branch.

## 5.5 Sutures

Suture mechanics should be treated as a **model-form branch conditional on anatomy**, not automatically as a high-priority scalar UQ input. The project needs to establish whether the relevant UALVP 2 cranial interfaces are anatomically persistent, mechanically compliant, or effectively continuous at the scale of interest. A speculative low-stiffness suture model could introduce more model-form uncertainty than it resolves.

## 5.6 Scale

For a single specimen-specific UALVP 2 model, “scale” is not automatically a biological uncertainty variable. CT provides specimen geometry and the main uncertainty is more likely to be **digital scale/provenance** rather than unknown biological size.

Scale becomes a meaningful uncertain parameter when:

- comparing individuals;
- modeling reconstructed missing anatomy by allometric scaling;
- propagating uncertainty from unknown dimensions.

Otherwise it should remain a provenance/geometry audit variable, not a generic UQ RV.

---

# 6. FEM / UQ audit

## 6.1 Strongly supported project decisions

| Decision | Assessment | Why |
|---|---|---|
| Freeze geometry during h-refinement | **Strongly supported** | Separates discretization effects from geometry-processing effects. |
| Treat mesh convergence as verification | **Strongly supported** | Consistent with VVUQ literature and Bright & Rayfield (2011). |
| Use multiple convergence QoIs | **Strongly supported** | Different regions/outputs converge at different rates. |
| Report exact loads and BCs | **Strongly supported** | Loading and BCs materially affect cranial FE response. |
| Keep 1360 N as a benchmark, not biological truth | **Strongly supported** | Directly consistent with Snively & Theodor’s force-scaling description. |
| Separate numerical, geometry, material, load/BC and model-form uncertainty | **Strongly supported** | Matches the structure of the evidence and VVUQ methodology. |
| Treat segmentation/repair as part of the model chain | **Strongly supported** | Surface geometry and segmentation can change FE outputs. |
| Avoid behavior claims from a single static FE result | **Strongly supported** | Directly required by the uncertainty in loads, behavior and model form. |

## 6.2 Reasonably supported decisions

| Decision | Assessment | Caveat |
|---|---|---|
| Start UQ with OAT | **Reasonably supported** | Useful for baseline debugging and directional understanding; insufficient for interactions. |
| Use Morris when the candidate-input set becomes large | **Reasonably supported** | Screening method, not final variance attribution. |
| Use LHS for expensive probabilistic FE ensembles | **Reasonably supported** | Requires defensible ranges/distributions first. |
| Use Sobol only when variance attribution/interactions matter | **Reasonably supported** | Sampling convergence must be demonstrated. |
| Use GP/PCE/response-surface surrogates only if FE cost justifies them | **Reasonably supported** | Emulator validation is a separate numerical result. |
| Keep discrete model-form branches separate from scalar parameter distributions | **Reasonably supported** | This is particularly important for BC/segmentation/constitutive-form alternatives. |

## 6.3 Plausible but currently unverified

| Decision | Assessment | What must be demonstrated |
|---|---|---|
| 4–6 mesh tiers | **Plausible but unverified** | Choose tiers based on convergence criteria, not a fixed count. |
| Sensitivity-index convergence as a formal result | **Plausible but strong** | Demonstrate stability of indices with increasing sample size; useful recent precedent exists (Baugnon et al. 2026). |
| Active learning | **Plausible but conditional** | Show that an adaptive surrogate/sampling problem actually exists and beats direct FE cost. |
| Anisotropic material model | **Plausible but unverified** | Establish directional material evidence and a defensible constitutive law. |
| Suture-mechanics branch | **Plausible but conditional** | Establish that the UALVP 2 anatomy justifies a compliant-interface model. |
| Dynamic/nonlinear impact FE | **Plausible but conditional** | Demonstrate that the biological question requires transient/contact/nonlinear mechanics beyond the baseline static model. |

## 6.4 Unsupported or should be reconsidered

### “Validated” 2011 model

**Reconsider.** There is no specimen-specific physical validation in Snively & Theodor (2011). Call it a historical benchmark and comparative model, not a validated UALVP 2 model.

### Homogeneous `E` as the central material UQ variable

**Reconsider.** The internal architecture is demonstrably heterogeneous. Use homogeneous `E` as a control/simplification branch, not as the sole material uncertainty axis.

### Automatic escalation to the most sophisticated UQ method

**Reconsider.** The current review already avoids this conceptually. That principle should be enforced in the roadmap: no GP, PCE, Sobol, active learning or Bayesian calibration unless a demonstrated decision problem requires it.

### Treating peak local von Mises stress as the principal endpoint

**Reconsider.** The 2011 paper itself documents high local artifacts around constraints and neurovascular canals. Primary endpoints should be defined regionally and physiologically, for example:

- elastic/strain energy;
- displacement at anatomically defined landmarks;
- regional stress/strain percentiles or volume fractions;
- force/reaction equilibrium;
- optionally, artifact-masked maxima only as secondary diagnostics.

### Calling one converged mesh “the converged model”

**Reconsider.** Convergence is QoI-specific. A model can have converged global energy and still have non-converged local stress peaks.

---

# 7. Revised scientific roadmap

The revised roadmap below is intentionally conservative. It adds complexity only when it answers a specific unresolved question.

## Phase 0 — Repair the evidence base

1. Correct the Sullivan 2003/2006 conflation.
2. Correct Peterson, Dischler & Longrich authorship.
3. Correct Dumont et al. journal metadata.
4. Add Nirody et al. (2022) to the UALVP 2 core bibliography.
5. Give every evidence-matrix row a traceable source ID and DOI/stable URL where possible.
6. Preserve `UNVERIFIED` labels until primary verification is complete.

## Phase 1 — Specimen and geometry provenance

Create an immutable chain:

`source CT / original mesh → segmented anatomy → repaired geometry → FE-ready surface → volume mesh`.

For each state record:

- voxel size and scan provenance;
- segmentation method;
- matrix treatment;
- repaired/mirrored regions;
- smoothing/decimation;
- surface resolution;
- watertight/manifold checks;
- physical scale.

Do not call these “preprocessing details.” They are part of the scientific model.

## Phase 2 — Anatomical/material model definition

Before large UQ, characterize the internal model structure from CT + histology:

1. identify defensible material regions;
2. reproduce the broad compact/trabecular architecture used by Snively & Theodor where the current data support it;
3. define a homogeneous control model;
4. define one or more zonated models;
5. document exactly what is measured versus inferred.

Only after this structure is fixed should the project define uncertain constitutive parameters.

## Phase 3 — Deterministic verification

Before interpreting any fossil result:

- unit/dimensional checks;
- force/reaction equilibrium;
- solver residual checks;
- simple analytical or manufactured-solution tests;
- linearity check for the static elastic formulation;
- load-area and load-direction implementation checks;
- mesh-quality diagnostics.

This phase is about whether the code solves the stated mathematical model correctly.

## Phase 4 — Historical benchmark reproduction

Recreate the published 2011 benchmark as closely as the current data permit:

- UALVP 2 geometry/provenance;
- internal material representation;
- 1360 N force;
- published constraint strategy;
- comparable load-spread cases;
- comparable global/regional outputs.

Interpret differences as **provenance/model differences** unless the published implementation can be independently reproduced exactly.

Do not call agreement “validation.” It is reproduction/benchmark concordance.

## Phase 5 — Controlled mesh convergence

Use the same FE-ready geometry and model for all h-refinement tiers.

Stop based on predefined output tolerances rather than an arbitrary number of meshes. Track at least:

- strain/elastic energy;
- landmark displacement;
- regional stress/strain summaries.

Report convergence separately for each QoI. Flag local singular/constraint-adjacent stress extrema rather than treating them as authoritative convergence targets.

## Phase 6 — Focused scenario sensitivity

Start with the assumptions for which there is direct evidence of uncertainty:

1. force magnitude;
2. contact/load area or spread;
3. load direction;
4. boundary-condition alternatives;
5. material-region properties;
6. segmentation/matrix alternatives where anatomy genuinely remains ambiguous.

Use OAT first for interpretability. Add Morris only if the candidate input set becomes large enough to justify screening.

## Phase 7 — Probabilistic propagation only where distributions are defensible

For any variable assigned a probability distribution, document:

- empirical basis;
- biological interpretation;
- range/distribution;
- independence/dependence assumptions;
- why a continuous RV is more appropriate than a discrete scenario.

Use LHS or Monte Carlo only after this step.

Keep model-form branches discrete, for example:

- homogeneous vs zonated material;
- BC family A vs B;
- segmentation alternative A vs B.

Do not average fundamentally different models into one unjustified parameter distribution.

## Phase 8 — Global sensitivity if the question demands it

Use Sobol or another global method when the project actually needs variance attribution and interactions. Demonstrate convergence of the sensitivity estimates themselves.

The Baugnon et al. (2026) study is useful methodological precedent here, especially because it explicitly found that contact-sensitive outputs can need larger sample sizes than global metrics.

## Phase 9 — Surrogate / active-learning branch only if cost demands it

A surrogate is justified only after measuring the direct FE cost and showing that repeated evaluations are the dominant bottleneck.

Validate the surrogate against held-out FE cases for the exact QoIs used in downstream UQ.

## Phase 10 — Dynamic/nonlinear branch only for a specific biological question

A transient impact model should answer a concrete question that the static baseline cannot answer. Potential examples include:

- dependence on contact duration;
- peak dynamic acceleration/deceleration;
- transient brain-protection metrics;
- contact separation and rebound;
- nonlinear material or failure behavior.

It should not be presented as a generic “upgrade” or as automatically more biologically realistic.

---

# 8. Final synthesis audit

The evidence matrix does **not** support a single behavioral conclusion. It supports a hierarchy of increasingly strong statements:

### Strongest defensible statement

**UALVP 2 can be modeled quantitatively as a specimen-specific cranial FE problem, and the published 2011 model provides a directly relevant benchmark.**

### Also defensible

**The published UALVP 2 model shows that, under its chosen material assignments, force, contact areas, and boundary conditions, simulated loads are substantially redistributed through the dome and remain below the tissue-failure criteria adopted in that model.**

### Defensible only with qualifiers

**The combined anatomy, pathology, histology, comparative biomechanics, and postcranial morphology are consistent with several hypotheses about agonistic cranial behavior, including head-strike behavior.**

### Not established by the corpus

- the actual impact force history of a living *Stegoceras*;
- a unique biologically correct contact geometry;
- a unique living material-property map for fossilized UALVP 2 bone;
- a physically validated UALVP 2 FE model;
- that the dome evolved primarily for head-butting;
- that any single absolute peak stress is a biological measurement;
- that homogeneous Young’s modulus is the dominant source of uncertainty;
- that a fully probabilistic or surrogate-heavy pipeline is scientifically necessary from the outset.

The master synthesis is therefore **methodologically stronger than its bibliographic hygiene and V&V terminology currently suggest**. Its core conceptual direction is defensible, but the project should not move from that direction to strong biological conclusions until the citation errors are corrected, the direct UALVP 2 internal-anatomy literature is strengthened, and the material/load model is decomposed into evidence-backed architecture plus explicit assumptions.

---

# 9. Recommended wording changes for future project documents

Prefer:

- “benchmark reproduction” over “validation” for matching Snively & Theodor (2011);
- “CT-informed/manual material assignment” over “measured material properties”;
- “literature benchmark load of 1360 N” over “estimated biological impact force”;
- “mechanically tolerates the modeled load under the stated assumptions” over “can withstand impacts”;
- “comparative support from extant analogues” over “comparative validation”;
- “behavioral plausibility” over “demonstrated behavior”;
- “scenario-dependent” when conclusions change with BC/load/contact/model form;
- “regional stress summary” or “stress distribution” rather than a single peak value near known singularities.

Avoid:

- “proves head-butting”;
- “validated UALVP 2 model” unless an independent physical validation pathway exists;
- “biologically realistic” without naming which biological observations constrain the model;
- “novel/first” until the exhaustive citation chase promised by the corpus is actually completed.

---

# 10. Primary sources checked / priority references

1. Snively, E., & Cox, A. (2008). *Structural Mechanics of Pachycephalosaur Crania Permitted Head-Butting Behavior*. Palaeontologia Electronica 11(1):3A.  
   https://palaeo-electronica.org/2008_1/140/index.html

2. Snively, E., & Theodor, J. M. (2011). *Common Functional Correlates of Head-Strike Behavior in the Pachycephalosaur Stegoceras validum and Combative Artiodactyls*. PLOS ONE 6(6):e21422.  
   https://doi.org/10.1371/journal.pone.0021422

3. Schott, R. K., Evans, D. C., Goodwin, M. B., Horner, J. R., Brown, C. M., & Longrich, N. R. (2011). *Cranial Ontogeny in Stegoceras validum: A Quantitative Model of Pachycephalosaur Dome Growth and Variation*. PLOS ONE 6:e21092.  
   https://doi.org/10.1371/journal.pone.0021092

4. Goodwin, M. B., & Horner, J. R. (2004). *Cranial histology of pachycephalosaurs (Ornithischia: Marginocephalia) reveals transitory structures inconsistent with head-butting behavior*. Paleobiology 30:253–267.  
   https://doi.org/10.1666/0094-8373(2004)030<0253:CHOPOM>2.0.CO;2

5. Peterson, J. E., Dischler, C., & Longrich, N. R. (2013). *Distributions of Cranial Pathologies Provide Evidence for Head-Butting in Dome-Headed Dinosaurs (Pachycephalosauridae)*. PLOS ONE 8(7):e68620.  
   https://doi.org/10.1371/journal.pone.0068620

6. Woodruff, D. C., & Ackermans, N. L. (2026). *Headbutting through time: A review of this hypothesized behavior in “dome-headed” fossil taxa*. The Anatomical Record 309(5):1235–1256. First published online 4 July 2024.  
   https://doi.org/10.1002/ar.25526

7. Bateman, L.-P., & Larsson, H. C. E. (2026). *On Pachycephalosaurs, Trade-Offs, and the Historical Genesis of Sociosexual Display Structures*. The American Naturalist 208(1):9–29.  
   https://doi.org/10.1086/740811

8. Nirody, J. A., et al. (2022). *Quantifying vascularity in the frontoparietal dome of Stegoceras validum (Dinosauria: Pachycephalosauridae) from high resolution CT scans*. Journal of Vertebrate Paleontology 41(5):e2036991.  
   https://doi.org/10.1080/02724634.2021.2036991

9. Bright, J. A., & Rayfield, E. J. (2011). *The response of cranial biomechanical finite element models to variations in mesh density*. The Anatomical Record 294:610–620.  
   https://doi.org/10.1002/ar.21358

10. Bright, J. A., & Rayfield, E. J. (2011). *Sensitivity and ex vivo validation of finite element models of the domestic pig cranium*. Journal of Anatomy 219:456–471.  
    https://doi.org/10.1111/j.1469-7580.2011.01408.x

11. McCurry, M. R., Evans, A. R., & McHenry, C. R. (2015). *The sensitivity of biological finite element models to the resolution of surface geometry: a case study of crocodilian crania*. PeerJ 3:e988.  
    https://doi.org/10.7717/peerj.988

12. Dumont, E. R., Grosse, I. R., & Slater, G. J. (2009). *Requirements for comparing the performance of finite element models of biological structures*. Journal of Theoretical Biology 256:96–103.  
    https://doi.org/10.1016/j.jtbi.2008.08.017

13. Sullivan, R. M. (2003). *Revision of the dinosaur Stegoceras Lambe (Ornithischia, Pachycephalosauridae)*. Journal of Vertebrate Paleontology 23(1):181–207.  
    https://doi.org/10.1671/0272-4634(2003)23[181:ROTDSL]2.0.CO;2

14. Baugnon, L., Nicot, R., Bethune, N., et al. (2026). *Uncertainty quantification and global sensitivity analysis of a patient-specific mandibular finite element model using Latin hypercube sampling and sparse polynomial chaos expansion*. Medical Engineering & Physics 147. DOI `10.1088/1873-4030/ae995b`.

15. Valerio, T., & Dall’Ara, E. (2026). *Sensitivity analysis of musculoskeletal parameters and motion variability on the mouse tibial loading*. Journal of Biomechanics 204:113377.  
    https://doi.org/10.1016/j.jbiomech.2026.113377

---

# Bottom line

The literature-review work in commit `473d978` has a strong methodological backbone and is substantially more cautious than a conventional “pachycephalosaur head-butting” narrative. The main problems are **not** that the review is too skeptical; they are that a few bibliographic records are wrong, “validation” is occasionally used incorrectly, and the material/UQ framework needs to be anchored more firmly in the demonstrably heterogeneous internal anatomy of UALVP 2 before homogeneous property uncertainty is elevated to the main probabilistic axis.

The safest scientific next step is therefore **not** “add more UQ.” It is to repair the source record, add the missing high-resolution *Stegoceras* CT/vascularity evidence, reproduce the published benchmark transparently, verify the deterministic FE implementation, and only then decide which uncertainties are sufficiently constrained to deserve probabilistic treatment.

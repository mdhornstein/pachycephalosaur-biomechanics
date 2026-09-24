# Stegoceras Biomechanics + UQ — Literature Review Management

> **Canonical review artifact for humans and agents.** This Markdown file supersedes the DOCX as the primary review-management document. The CSV companion remains the canonical flat evidence export; DOCX/PDF are presentation exports only.

**Scope:** evidence-based scoping review for *Stegoceras validum* UALVP 2 and the methodological literature needed to interpret its CT-derived FEM and future UQ workflow.

**Search date:** 23 September 2026 (America/Los_Angeles)

## 0. Scope guard and evidence semantics

This document distinguishes source evidence from coordinator synthesis. Repository/project-state statements are not counted as independent scientific literature evidence.

| Code | Meaning |
|---|---|
| `DO` | Direct observation/report: explicitly stated or directly shown by the source, including reported model inputs, specimen identity, methods, or results. |
| `AI` | Author interpretation: the source authors’ interpretation or causal/behavioral conclusion. |
| `MA` | Model assumption: an explicit or implicit modeling choice required to construct the simulation. |
| `SYN` | Our synthesis: coordinator-level comparison across sources or an inference about project implications. |
| `UNVERIFIED` | The detail could not be verified from the paper/authoritative record retrieved in this pass; it must not be silently filled in. |

### Source-priority rules

1. Peer-reviewed primary research papers: highest priority for model inputs, methods, results, and specimen-specific claims.
2. Peer-reviewed methodological/validation papers and reviews: high priority for general practice, validity, sensitivity, and UQ framework.
3. Peer-reviewed biological/histological papers: high priority for anatomical and tissue priors, but not equivalent to mechanical validation.
4. Conference abstracts, theses, repositories, project documentation, and websites: context/provenance only unless the underlying primary publication is absent; never silently merge them into peer-reviewed evidence.

## 1. Project context snapshot — repository evidence, not literature evidence

| Item | Current project record | Locator |
|---|---|---|
| Lead specimen | Stegoceras validum UALVP 2; the repository identifies it as the lead specimen and Phase 4 target. | Repository HANDOFF / CURRENT_STATE |
| Current state | Phase 4 FROZEN; Phase 5 UQ + sensitivity design pending. | Repository HANDOFF |
| Current Model A | Surface-derived fused monolithic continuum; homogeneous isotropic compact bone; E=17 GPa, nu=0.30 in the project baseline. | Repository CURRENT_STATE |
| Geometry | Canonical watertight 2-manifold surface; project reports no non-manifold edges/self-intersections. | Repository CURRENT_STATE |
| Mesh convergence | Three-tier h-refinement hierarchy; project treats global compliance/energy and apex displacement as more stable than localized internal stress. | Repository HANDOFF |
| Scientific caution | The project itself records localized stress discretization sensitivity and proposes carrying numerical discretization forward as a model-form uncertainty component. | Repository HANDOFF |

## 2. Search protocol

### 2.1 Search engines and databases actually used

- Web-scale literature search/indexing for discovery and exact-title retrieval: publisher pages, PubMed, PMC, PLOS, Cambridge Core, Wiley, ScienceDirect, university repositories.
- PubMed/PMC records for biomedical FE/UQ and specimen metadata.
- Publisher/official article pages for primary-method extraction when full HTML was available.
- GitHub repository and raw repository files for project-state and provenance context; repository records are not counted as scientific literature evidence.

### 2.2 Exact search strings executed (representative log)

- `"Snively" "Cox" 2008 "pachycephalosaur" biomechanics`
- `"Snively" "Theodor" 2011 Stegoceras finite element analysis`
- `"Stegoceras validum" finite element analysis`
- `"UALVP 2" Stegoceras biomechanics`
- `"Cranial Ontogeny in Stegoceras validum"`
- `"A review of paleontological finite element models and their validity"`
- `"finite element analysis" cranium validity sensitivity future directions`
- `"finite-element modeling of bones from CT data" sensitivity geometry material uncertainties`
- `"probabilistic finite element analysis" craniofacial Latin hypercube`
- `"sensitivity" finite element skull boundary conditions loading material properties`
- `"surface geometry" sensitivity biological finite element crocodilian crania`
- `"nonlinear finite element analysis" palaeontology review`
- `"uncertainty quantification" "finite element" mandible Latin hypercube Sobol`
- `"global sensitivity analysis" "finite element" biomechanics Sobol`
- `"deep learning-aided segmentation" finite element dinosaur fossil`
- `"model discrepancy" finite element biomechanics validation uncertainty`
- `"mesh convergence" finite element skull biomechanics`
- `"head-butting" pachycephalosaur review biomechanics`
- `"Goodwin" "Horner" 2004 pachycephalosaur dome histology`
- `"The appendicular myology of Stegoceras validum" UALVP 2`

### 2.3 Inclusion rules

- Include peer-reviewed primary studies that materially inform fossil FEA methodology, cranial biomechanics, pachycephalosaur biology, CT/segmentation/geometry/meshing, validation, sensitivity, probabilistic FE, UQ, or model discrepancy.
- Include reviews that synthesize paleontological FEA practice, validity, sensitivity, or nonlinear methods and that provide citation maps for further chasing.
- Include extant cranial/osseous FE validation and UQ papers when the methodological issue is transferable to a fossil workflow and the taxonomic transfer is stated explicitly.
- Include specimen/provenance webpages only when they establish CT availability, specimen identity, scan provenance, or digital anatomy; classify them as non-peer-reviewed context.

### 2.4 Exclusion / downgrade rules

- Do not treat conference abstracts, theses, websites, preprints, or repository copies as equivalent to peer-reviewed primary papers.
- Do not use a numerical result from a secondary summary when the primary paper can be accessed; mark it `UNVERIFIED` pending primary-paper checking.
- Do not merge duplicate records for the same publication simply because publisher, PubMed, repository, or PMC pages differ; the P24 management record is retained only for the deduplication audit.
- No citation, DOI, parameter value, result, or methodological detail is to be inferred from a familiar pattern alone. The value is either verified or `UNVERIFIED`.

### 2.5 Citation-chasing protocol

- Start with gateway sources P01, P04, P08–P09, P23, P07, P06, P12–P16, and P22.
- Backward chase reference lists for seminal FEA, cranial biomechanics, validation, tissue-property, and head-strike papers.
- Forward chase citing articles using exact title/DOI/PMID searches and prioritize papers that introduce new validation, uncertainty, segmentation, nonlinear FE, or fossil-specific biomechanics.
- For candidate novelty statements, repeat forward/backward chasing until the search produces no new directly relevant UQ/validation/mesh/geometry studies, then retain the claim as `TO VERIFY` rather than “novel”.

## 3. Master bibliography and source records

**Core scientific records currently tracked: 23.** One additional management record (P24) exists only to document duplicate detection.

Each source has a stable project ID (`P01` etc.). The CSV companion preserves these records in flat form.

### 3.1 Bibliography index

| ID | Year | Type | Peer-review status | Taxon/specimen | Citation | DOI/stable ID |
|---|---:|---|---|---|---|---|
| P01 | 2001 | Research Article | Known peer-reviewed journal article | Allosaurus fragilis; MOR 693 | Rayfield EJ, Norman DB, Horner CC, Horner JR, Smith PM, Thomason JJ, Upchurch P. 2001. Cranial design and function in a large theropod dinosaur. Nature 409:1033-1037. | 10.1038/35059070 |
| P02 | 2005 | Research Article | Known peer-reviewed journal article | Allosaurus fragilis; MOR 693 | Rayfield EJ. 2005. Using finite-element analysis to investigate suture morphology: a case study using large carnivorous dinosaurs. Anatomical Record 283A:349-365. | 10.1002/ar.a.20168 |
| P03 | 2005 | Research Article | Known peer-reviewed journal article | Coelophysis bauri; Allosaurus fragilis; Tyrannosaurus rex | Rayfield EJ. 2005. Aspects of comparative cranial mechanics in the theropod dinosaurs Coelophysis, Allosaurus and Tyrannosaurus. Zoological Journal of the Linnean Society 144:309-316. | 10.1111/j.1096-3642.2005.00176.x |
| P04 | 2007 | Review | Known peer-reviewed review journal | Extant and fossil vertebrates | Rayfield EJ. 2007. Finite element analysis and understanding the biomechanics and evolution of living and fossil organisms. Annual Review of Earth and Planetary Sciences 35:541-576. | UNVERIFIED |
| P05 | 2006 | Research Article | Known peer-reviewed journal article | Human femur models | Taddei F, Martelli S, Reggiani B, Cristofolini L, Viceconti M. 2006. Finite-element modeling of bones from CT data: sensitivity to geometry and material uncertainties. IEEE Transactions on Biomedical Engineering. | 10.1109/TBME.2006.879473 |
| P06 | 2011 | Validation Study | Known peer-reviewed journal article | Domestic pig | Bright JA et al. 2011. Sensitivity and ex vivo validation of finite element models of the domestic pig cranium. Journal of Anatomy. | 10.1111/j.1469-7580.2011.01408.x |
| P07 | 2009 | Methodological Article | Known peer-reviewed journal article | Extant/fossil biological structures | Dumont ER, Grosse IR, Slater GJ. 2009. Requirements for comparing the performance of finite element models of biological structures. Journal of Theoretical Biology 256:96-103. | 10.1016/j.jtbi.2008.08.017 |
| P08 | 2008 | Research Article | Peer-review status UNVERIFIED in retrieved source | Pachycephalosauria; adult Homalocephale and Pachycephalosaurus; subadult pachycephalosaurine | Snively E, Cox A. 2008. Structural mechanics of pachycephalosaur crania permitted head-butting behavior. Palaeontologia Electronica 11(1), 11.1.3A. | UNVERIFIED |
| P09 | 2011 | Research Article | Peer-reviewed (PLOS article page) | Stegoceras validum UALVP 2 (UA 2) and comparative artiodactyls | Snively E, Theodor JM. 2011. Common functional correlates of head-strike behavior in the pachycephalosaur Stegoceras validum and combative artiodactyls. PLoS ONE 6(6):e21422. | 10.1371/journal.pone.0021422 |
| P10 | 2004 | Research Article | Known peer-reviewed journal article | Pachycephalosaurids; ontogenetic series (not conspecific) | Goodwin MB, Horner JR. 2004. Cranial histology of pachycephalosaurs (Ornithischia: Marginocephalia) reveals transitory structures inconsistent with head-butting behavior. Paleobiology 30(2):253-267. | 10.1666/0094-8373(2004)030<0253:CHOPOM>2.0.CO;2 |
| P11 | 2011 | Research Article | Peer-reviewed (PLOS article page) | Stegoceras validum; multiple specimens including UALVP 2 | Schott RK, Evans DC, Goodwin MB, Horner JR, Brown CM, Longrich NR. 2011. Cranial ontogeny in Stegoceras validum: a quantitative model of pachycephalosaur dome growth and variation. PLoS ONE 6(6):e21092. | 10.1371/journal.pone.0021092 |
| P12 | 2015 | Research Article | Peer-reviewed (PeerJ) | Crocodilian crania; multiple specimens | McCurry MR, Evans AR, McHenry CR. 2015. The sensitivity of biological finite element models to the resolution of surface geometry: a case study of crocodilian crania. PeerJ 3:e988. | 10.7717/peerj.988 |
| P13 | 2017 | Validation Study / Review-Context Paper | Known peer-reviewed journal article | Human cadaveric cranium | Godinho RM, Toro-Ibacache V, Fitton LC, O’Higgins P. 2017. Finite element analysis of the cranium: validity, sensitivity and future directions. Comptes Rendus Palevol 16:600-612. | 10.1016/j.crpv.2016.11.002 |
| P14 | 2013 | Research Article | Known peer-reviewed journal article | Lacerta bilineata | Moazen M. et al. 2013. A sensitivity analysis to the role of the fronto-parietal suture in Lacerta bilineata: a preliminary finite element study. Anatomical Record. | 10.1002/ar.22629 |
| P15 | 2012 | Research Article | Known peer-reviewed journal article | Macaca fascicularis | Probabilistic finite element analysis of a craniofacial finite element model. Journal of Theoretical Biology 300:242-253 (2012). | 10.1016/j.jtbi.2012.01.031 |
| P16 | 2022 | Review | Known peer-reviewed journal article | Fossil and extant biomechanical models | Marcé-Nogué J. 2022. One step further in biomechanical models in palaeontology: a nonlinear finite element analysis review. PeerJ 10:e13890. | 10.7717/peerj.13890 |
| P17 | 2022 | Research Article | Peer-reviewed (PLOS) | Stegoceras validum UALVP 2 | Moore BRS, Roloson MJ, Currie PJ, Ryan MJ, Patterson RT, Mallon JL. 2022. The appendicular myology of Stegoceras validum and implications for the head-butting hypothesis. PLoS ONE 17(9):e0268144. | 10.1371/journal.pone.0268144 |
| P18 | 2009 | Research Article | Known peer-reviewed journal article; DOI UNVERIFIED | Ceratopsid dinosaurs | Hieronymus TL, Witmer LM, Tanke DH, Currie PJ. 2009. The facial integument of centrosaurine ceratopsids: morphological and histological correlates of novel skin structures. Anatomical Record 292:1370-1396. | UNVERIFIED |
| P19 | 2008 | Research Article | Known peer-reviewed journal article; URL/DOI UNVERIFIED | Capra hircus (goat) | Farke AA. 2008. Frontal sinuses and head-butting in goats: a finite element analysis. Journal of Experimental Biology 211:3085-3094. | UNVERIFIED |
| P20 | 2021 | Research Article | Known peer-reviewed article; exact bibliographic details UNVERIFIED | Primarily comparative skull/teeth models | McCurry MR? 2021. Modeling tooth enamel in FEA comparisons of skulls: comparing common simplifications with biologically realistic models. | UNVERIFIED |
| P21 | 2025 | Research Article | Journal article; peer-review status UNVERIFIED in retrieved page | Dinosaur fossil (taxon not captured in excerpt) | Zhang L, Cao Z, Zhao Q. 2025. Deep learning-aided segmentation combined with finite element analysis reveals a more natural biomechanic of dinosaur fossil. Scientific Reports 15:13964. | UNVERIFIED |
| P22 | 2026 | Research Article | Publication type is Journal Article; peer-reviewed status UNVERIFIED in retrieved record | Human patient-specific mandible | Uncertainty quantification and global sensitivity analysis of a patient-specific mandibular finite element model using Latin hypercube sampling and sparse polynomial chaos expansion. 2026. PubMed PMID 42594916. | UNVERIFIED |
| P23 | 2014 | Review | Peer-reviewed (repository record) | Paleontological FE models; extant validation literature | Bright JA. 2014. A review of paleontological finite element models and their validity. Journal of Paleontology 88(4):760-769. | 10.1666/13-090 |

### 3.2 Detailed source records

#### P01 — Rayfield EJ, Norman DB, Horner CC, Horner JR, Smith PM, Thomason JJ, Upchurch P. 2001. Cranial design and function in a large theropod dinosaur. Nature 409:1033-1037.

- **Citation:** Rayfield EJ, Norman DB, Horner CC, Horner JR, Smith PM, Thomason JJ, Upchurch P. 2001. Cranial design and function in a large theropod dinosaur. Nature 409:1033-1037.
- **DOI or stable identifier:** 10.1038/35059070
- **URL:** [https://doi.org/10.1038/35059070](https://doi.org/10.1038/35059070)
- **Publication year:** 2001
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Allosaurus fragilis; MOR 693
- **Anatomical structure:** cranium/skull
- **Computational method:** 3-D linear static FEA
- **Geometry source:** CT-derived 3-D geometry; 193 transverse slices; pneumatic cavities represented
- **Material model:** Not fully captured in abstract; literature-based bone properties; exact spatial assignment UNVERIFIED
- **Loading conditions:** Several bite/impact load cases; exact force values by case UNVERIFIED
- **Boundary conditions:** Constraints representing skull functional loading; exact formulation UNVERIFIED
- **Mesh strategy:** Volumetric FE model; >200,000 elements reported in later review
- **Validation strategy:** No experimental validation; hypothesis-testing study
- **Sensitivity / UQ methodology:** None
- **Principal scientific question:** Can a CT-derived fossil skull model distinguish feeding hypotheses and quantify cranial strength?
- **Principal finding:** FEA showed high cranial strength relative to estimated muscle-driven bite, supporting a mechanically constrained feeding interpretation by the authors.
- **Limitations:** Model assumptions, loading, and material properties are reconstructed from early-generation FEA; exact inputs need primary-paper extraction before reuse.
- **Relevance to project:** Historical foundation for CT-to-FEA paleontology and hypothesis testing.
- **Epistemic notes:** DO: CT basis and main result from Nature abstract. AI: feeding interpretation is author conclusion. MA: material/loading details partly UNVERIFIED.

#### P02 — Rayfield EJ. 2005. Using finite-element analysis to investigate suture morphology: a case study using large carnivorous dinosaurs. Anatomical Record 283A:349-365.

- **Citation:** Rayfield EJ. 2005. Using finite-element analysis to investigate suture morphology: a case study using large carnivorous dinosaurs. Anatomical Record 283A:349-365.
- **DOI or stable identifier:** 10.1002/ar.a.20168
- **URL:** [https://doi.org/10.1002/ar.a.20168](https://doi.org/10.1002/ar.a.20168)
- **Publication year:** 2005
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Allosaurus fragilis; MOR 693
- **Anatomical structure:** cranium; cranial sutures
- **Computational method:** 3-D FE, linear/static baseline with comparative load cases
- **Geometry source:** CT-derived skull; fused solid model altered to study suture effects
- **Material model:** Bone properties inherited from prior Allosaurus model; exact values UNVERIFIED
- **Loading conditions:** Bite/feeding forces plus yield-inducing loads; true dynamic impact noted as a future need
- **Boundary conditions:** Functional cranial constraints; exact node/DOF details UNVERIFIED
- **Mesh strategy:** 3-D volumetric tetrahedral model based on CT/digitized slices
- **Validation strategy:** No direct experimental validation; model comparison and hypothesis test
- **Sensitivity / UQ methodology:** Sensitivity to suture representation; not full UQ
- **Principal scientific question:** Are patent sutures mechanically compatible with predicted feeding stress/strain?
- **Principal finding:** Suture locations/orientations were broadly consistent with accommodating modeled loading, according to the study.
- **Limitations:** Static treatment of large external loads; suture tissue/soft-tissue properties uncertain.
- **Relevance to project:** Supports separating physiological interpretation from numerical artifacts and motivates load/BC sensitivity.
- **Epistemic notes:** DO: CT and model basis are stated. AI: suture accommodation conclusion. MA: dynamic loads are simplified as static.

#### P03 — Rayfield EJ. 2005. Aspects of comparative cranial mechanics in the theropod dinosaurs Coelophysis, Allosaurus and Tyrannosaurus. Zoological Journal of the Linnean Society 144:309-316.

- **Citation:** Rayfield EJ. 2005. Aspects of comparative cranial mechanics in the theropod dinosaurs Coelophysis, Allosaurus and Tyrannosaurus. Zoological Journal of the Linnean Society 144:309-316.
- **DOI or stable identifier:** 10.1111/j.1096-3642.2005.00176.x
- **URL:** [https://doi.org/10.1111/j.1096-3642.2005.00176.x](https://doi.org/10.1111/j.1096-3642.2005.00176.x)
- **Publication year:** 2005
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Coelophysis bauri; Allosaurus fragilis; Tyrannosaurus rex
- **Anatomical structure:** cranium/skull
- **Computational method:** Comparative FE
- **Geometry source:** Comparative fossil skull geometries; exact acquisition details UNVERIFIED
- **Material model:** Literature-derived, likely homogeneous elastic in baseline; exact spatial maps UNVERIFIED
- **Loading conditions:** Biting/feeding load cases; exact forces UNVERIFIED
- **Boundary conditions:** Comparative functional constraints; exact formulation UNVERIFIED
- **Mesh strategy:** 2-D/3-D comparative FE; exact element types/counts UNVERIFIED
- **Validation strategy:** No experimental validation
- **Sensitivity / UQ methodology:** Morphological/parameter comparison rather than uncertainty propagation
- **Principal scientific question:** How does cranial shape influence stress/strain among theropod taxa?
- **Principal finding:** Stress/strain patterns were used to relate skull architecture to functional performance.
- **Limitations:** Cross-taxon comparisons are sensitive to scaling, material assumptions and load normalization.
- **Relevance to project:** Historical comparative-FEA practice and caveat for cross-model normalization.
- **Epistemic notes:** UNVERIFIED

#### P04 — Rayfield EJ. 2007. Finite element analysis and understanding the biomechanics and evolution of living and fossil organisms. Annual Review of Earth and Planetary Sciences 35:541-576.

- **Citation:** Rayfield EJ. 2007. Finite element analysis and understanding the biomechanics and evolution of living and fossil organisms. Annual Review of Earth and Planetary Sciences 35:541-576.
- **DOI or stable identifier:** UNVERIFIED
- **URL:** [https://www.annualreviews.org/doi/10.1146/annurev.earth.35.031306.140104](https://www.annualreviews.org/doi/10.1146/annurev.earth.35.031306.140104)
- **Publication year:** 2007
- **Publication type:** Review
- **Peer-reviewed status:** Known peer-reviewed review journal
- **Taxon / specimen:** Extant and fossil vertebrates
- **Anatomical structure:** skeletal structures broadly
- **Computational method:** FEA methodological review
- **Geometry source:** CT-derived and reconstructed geometries across studies
- **Material model:** Literature-derived materials; uncertainty emphasized
- **Loading conditions:** Feeding and structural loading across case studies
- **Boundary conditions:** Boundary conditions treated as core modeling inputs
- **Mesh strategy:** Multiple mesh strategies; early fossil models include >200k elements
- **Validation strategy:** Reviews validation/sensitivity literature
- **Sensitivity / UQ methodology:** Sensitivity and validation discussed conceptually
- **Principal scientific question:** How has FEA been used to connect form, function and evolution?
- **Principal finding:** FEA enables quantitative stress/strain predictions but depends critically on geometry, material, loads and constraints.
- **Limitations:** Fossil models inherit large uncertainty from unavailable tissue properties and reconstructed loads.
- **Relevance to project:** Provides historical methodological framework and source map for backward/forward chasing.
- **Epistemic notes:** DO: review scope and CT/FEA framing. SYN: use as gateway source for citation chasing. DOI field UNVERIFIED.

#### P05 — Taddei F, Martelli S, Reggiani B, Cristofolini L, Viceconti M. 2006. Finite-element modeling of bones from CT data: sensitivity to geometry and material uncertainties. IEEE Transactions on Biomedical Engineering.

- **Citation:** Taddei F, Martelli S, Reggiani B, Cristofolini L, Viceconti M. 2006. Finite-element modeling of bones from CT data: sensitivity to geometry and material uncertainties. IEEE Transactions on Biomedical Engineering.
- **DOI or stable identifier:** 10.1109/TBME.2006.879473
- **URL:** [https://doi.org/10.1109/TBME.2006.879473](https://doi.org/10.1109/TBME.2006.879473)
- **Publication year:** 2006
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Human femur models
- **Anatomical structure:** femur/bone
- **Computational method:** Probabilistic FE; Monte Carlo sensitivity
- **Geometry source:** Three in vivo CT-based femur models
- **Material model:** Geometry, density and mechanical properties treated as random variables
- **Loading conditions:** Two loading conditions per model
- **Boundary conditions:** Exact BCs UNVERIFIED
- **Mesh strategy:** FE simulations with stochastic input sampling; exact mesh metrics UNVERIFIED
- **Validation strategy:** No direct physical validation in abstract
- **Sensitivity / UQ methodology:** Monte Carlo sensitivity analysis
- **Principal scientific question:** How do geometry and material uncertainty affect FE outputs?
- **Principal finding:** Geometry, density and material-property variability can be propagated probabilistically into biomechanical outputs.
- **Limitations:** Human femur rather than fossil cranium; distributions and correlations are context-specific.
- **Relevance to project:** Direct precedent for geometry + material uncertainty propagation and Monte Carlo design.
- **Epistemic notes:** DO: Monte Carlo, three femur models, two loads. SYN: transferability to fossils is methodological, not empirical.

#### P06 — Bright JA et al. 2011. Sensitivity and ex vivo validation of finite element models of the domestic pig cranium. Journal of Anatomy.

- **Citation:** Bright JA et al. 2011. Sensitivity and ex vivo validation of finite element models of the domestic pig cranium. Journal of Anatomy.
- **DOI or stable identifier:** 10.1111/j.1469-7580.2011.01408.x
- **URL:** [https://doi.org/10.1111/j.1469-7580.2011.01408.x](https://doi.org/10.1111/j.1469-7580.2011.01408.x)
- **Publication year:** 2011
- **Publication type:** Validation Study
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Domestic pig
- **Anatomical structure:** cranium
- **Computational method:** 3-D FE with ex vivo validation and sensitivity analysis
- **Geometry source:** CT-based specimen-specific cranial geometry; resolution limitations explicitly discussed
- **Material model:** Material property variation was a major sensitivity driver; detailed local heterogeneity incompletely known
- **Loading conditions:** Experimental load reproduced in FE; exact magnitudes UNVERIFIED
- **Boundary conditions:** Constraints intended to mimic experimental loading; exact details UNVERIFIED
- **Mesh strategy:** Solid FE skull; exact mesh metrics UNVERIFIED
- **Validation strategy:** Ex vivo strain-gauge comparison
- **Sensitivity / UQ methodology:** Material-property sensitivity; no full probabilistic UQ
- **Principal scientific question:** Can FE reproduce measured cranial strain patterns and magnitudes?
- **Principal finding:** Model reproduced loading/overall strain environment better than absolute local strain magnitudes; material properties strongly affected outputs.
- **Limitations:** CT resolution and missing local material-property data can explain discrepancies; absolute breaking stress/bite force should be treated cautiously.
- **Relevance to project:** Core validation evidence for interpreting pattern vs magnitude and for material UQ.
- **Epistemic notes:** UNVERIFIED

#### P07 — Dumont ER, Grosse IR, Slater GJ. 2009. Requirements for comparing the performance of finite element models of biological structures. Journal of Theoretical Biology 256:96-103.

- **Citation:** Dumont ER, Grosse IR, Slater GJ. 2009. Requirements for comparing the performance of finite element models of biological structures. Journal of Theoretical Biology 256:96-103.
- **DOI or stable identifier:** 10.1016/j.jtbi.2008.08.017
- **URL:** [https://doi.org/10.1016/j.jtbi.2008.08.017](https://doi.org/10.1016/j.jtbi.2008.08.017)
- **Publication year:** 2009
- **Publication type:** Methodological Article
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Extant/fossil biological structures
- **Anatomical structure:** general biological FE models
- **Computational method:** Comparative FE methodology
- **Geometry source:** Varied biological geometries
- **Material model:** Exact material assumptions vary by case; comparison principles are the focus
- **Loading conditions:** Comparative load cases normalized for size/shape considerations
- **Boundary conditions:** Comparative BCs
- **Mesh strategy:** Varied FE discretizations
- **Validation strategy:** No direct validation; methodological argument
- **Sensitivity / UQ methodology:** No formal UQ
- **Principal scientific question:** What metrics and normalization are appropriate for comparative FE?
- **Principal finding:** Total strain energy is argued to be a robust metric for comparative performance because it captures work expended in deformation and can help disentangle size/shape effects.
- **Limitations:** Comparisons remain dependent on consistent loads, constraints and model construction.
- **Relevance to project:** Supports project use of strain energy alongside displacement/stress, and normalization rules.
- **Epistemic notes:** DO: abstract explicitly argues for total strain energy. SYN: direct relevance to current Phase 4 output design.

#### P08 — Snively E, Cox A. 2008. Structural mechanics of pachycephalosaur crania permitted head-butting behavior. Palaeontologia Electronica 11(1), 11.1.3A.

- **Citation:** Snively E, Cox A. 2008. Structural mechanics of pachycephalosaur crania permitted head-butting behavior. Palaeontologia Electronica 11(1), 11.1.3A.
- **DOI or stable identifier:** UNVERIFIED
- **URL:** [https://palaeo-electronica.org/2008_1/140/index.html](https://palaeo-electronica.org/2008_1/140/index.html)
- **Publication year:** 2008
- **Publication type:** Research Article
- **Peer-reviewed status:** Peer-review status UNVERIFIED in retrieved source
- **Taxon / specimen:** Pachycephalosauria; adult Homalocephale and Pachycephalosaurus; subadult pachycephalosaurine
- **Anatomical structure:** frontoparietal dome/cranium
- **Computational method:** 2-D and 3-D FE; impact mechanics
- **Geometry source:** Reconstructed dorsal skull shapes; one subadult dome model
- **Material model:** Histological-zone based materials; keratin layers modeled parametrically
- **Loading conditions:** Impact force/closing-speed scenarios; low-speed head impacts emphasized
- **Boundary conditions:** Exact constraints UNVERIFIED
- **Mesh strategy:** 2-D and 3-D FE models; exact element counts/types UNVERIFIED
- **Validation strategy:** No direct experimental validation
- **Sensitivity / UQ methodology:** Parametric keratin thickness/shape sensitivity
- **Principal scientific question:** Can dome geometry and internal trabecular structure sustain head impacts?
- **Principal finding:** Authors report that modeled domes could withstand substantial low-speed impacts and that stresses/strains dissipate through the dorsal skull; keratin coverings reduced transmitted force/energy.
- **Limitations:** Older/adult domes, tissue reconstruction and model assumptions remain uncertain; behavior is not directly observed.
- **Relevance to project:** Direct precursor to Snively & Theodor and key behavioral-mechanics context.
- **Epistemic notes:** DO: abstract and study page. AI: “permitted head-butting” is the author interpretation. MA: keratin and closing-speed cases are assumed/modelled.

#### P09 — Snively E, Theodor JM. 2011. Common functional correlates of head-strike behavior in the pachycephalosaur Stegoceras validum and combative artiodactyls. PLoS ONE 6(6):e21422.

- **Citation:** Snively E, Theodor JM. 2011. Common functional correlates of head-strike behavior in the pachycephalosaur Stegoceras validum and combative artiodactyls. PLoS ONE 6(6):e21422.
- **DOI or stable identifier:** 10.1371/journal.pone.0021422
- **URL:** [https://doi.org/10.1371/journal.pone.0021422](https://doi.org/10.1371/journal.pone.0021422)
- **Publication year:** 2011
- **Publication type:** Research Article
- **Peer-reviewed status:** Peer-reviewed (PLOS article page)
- **Taxon / specimen:** Stegoceras validum UALVP 2 (UA 2) and comparative artiodactyls
- **Anatomical structure:** cranium/dome
- **Computational method:** 3-D FE; recursive partition analysis
- **Geometry source:** Medical CT + high-resolution UTCT; manually cleaned STL; 2.2M-element tetrahedral primary Stegoceras model
- **Material model:** Manual fossil material assignment; compact bone capped at >2500 HU; cancellous bone E=1 GPa; keratin E=3.9 GPa, nu=0.28 in Ovibos
- **Loading conditions:** 1360 N compressive force for Stegoceras; broad vs concentrated dome loads; force-scaled artiodactyl cases
- **Boundary conditions:** Occipital condyles constrained against translation/rotation plus nuchal-crest constraints; basitubera constraint tested and produced artifacts
- **Mesh strategy:** 2.2M tetrahedra in primary Stegoceras model; voxel hexahedral comparison ~200k for some models
- **Validation strategy:** No direct validation; artifact/singularity discussion
- **Sensitivity / UQ methodology:** Load-distribution sensitivity across keratin-pad scenarios; comparative structural analysis
- **Principal scientific question:** How do CT-derived cranial structure and modeled impact loads compare among head-striking taxa?
- **Principal finding:** Broad dome loading produced lower/more diffuse stress; local stress peaks occurred near constraints/neurovascular features; authors interpret Stegoceras as mechanically compatible with head-strike behavior.
- **Limitations:** Force magnitude is biologically scaled but modelled as quasi-static; material properties are not dinosaur measurements; singularities/artifacts and unknown keratin geometry affect absolute stresses.
- **Relevance to project:** Primary benchmark target and central source for UALVP 2 load/material/geometry reconstruction.
- **Epistemic notes:** DO: 2.2M tet mesh, CT systems, 1360N, materials, BC artifacts, results are directly in full text. AI: behavior inference. MA: static impact and fossil material mapping.

#### P10 — Goodwin MB, Horner JR. 2004. Cranial histology of pachycephalosaurs (Ornithischia: Marginocephalia) reveals transitory structures inconsistent with head-butting behavior. Paleobiology 30(2):253-267.

- **Citation:** Goodwin MB, Horner JR. 2004. Cranial histology of pachycephalosaurs (Ornithischia: Marginocephalia) reveals transitory structures inconsistent with head-butting behavior. Paleobiology 30(2):253-267.
- **DOI or stable identifier:** 10.1666/0094-8373(2004)030<0253:CHOPOM>2.0.CO;2
- **URL:** [https://doi.org/10.1666/0094-8373(2004)030%3C0253:CHOPOM%3E2.0.CO%3B2](https://doi.org/10.1666/0094-8373(2004)030%3C0253:CHOPOM%3E2.0.CO%3B2)
- **Publication year:** 2004
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Pachycephalosaurids; ontogenetic series (not conspecific)
- **Anatomical structure:** frontoparietal dome histology
- **Computational method:** Histological microscopy, not FE
- **Geometry source:** Thin sections across growth series
- **Material model:** Histological zones and vascularity characterized directly
- **Loading conditions:** No loading
- **Boundary conditions:** No FE mesh
- **Mesh strategy:** Not a computational validation study
- **Validation strategy:** None
- **Sensitivity / UQ methodology:** What is the ontogenetic meaning of dome microstructure?
- **Principal scientific question:** Authors identified three histological zones and reported that radiating/spongy structures diminish with maturity, interpreting them as transient growth-related structures rather than adaptations for adult head-butting.
- **Principal finding:** Series is not conspecific; external soft-tissue covering is unpreserved; behavioral conclusion is interpretive.
- **Limitations:** Critical biological prior for internal zonation and material-model uncertainty in adult Stegoceras.
- **Relevance to project:** DO: three zones and ontogenetic changes. AI: “inconsistent with head-butting” is author interpretation. MA: none computational.
- **Epistemic notes:** UNVERIFIED

#### P11 — Schott RK, Evans DC, Goodwin MB, Horner JR, Brown CM, Longrich NR. 2011. Cranial ontogeny in Stegoceras validum: a quantitative model of pachycephalosaur dome growth and variation. PLoS ONE 6(6):e21092.

- **Citation:** Schott RK, Evans DC, Goodwin MB, Horner JR, Brown CM, Longrich NR. 2011. Cranial ontogeny in Stegoceras validum: a quantitative model of pachycephalosaur dome growth and variation. PLoS ONE 6(6):e21092.
- **DOI or stable identifier:** 10.1371/journal.pone.0021092
- **URL:** [https://doi.org/10.1371/journal.pone.0021092](https://doi.org/10.1371/journal.pone.0021092)
- **Publication year:** 2011
- **Publication type:** Research Article
- **Peer-reviewed status:** Peer-reviewed (PLOS article page)
- **Taxon / specimen:** Stegoceras validum; multiple specimens including UALVP 2
- **Anatomical structure:** frontoparietal dome
- **Computational method:** Landmark morphometrics + histology + CT
- **Geometry source:** HRCT images; Huang thresholding for a void-space/vascularity proxy
- **Material model:** No FE materials
- **Loading conditions:** No loading
- **Boundary conditions:** No FE BCs
- **Mesh strategy:** No FE mesh
- **Validation strategy:** Morphometric/statistical validation across specimens
- **Sensitivity / UQ methodology:** No FE UQ
- **Principal scientific question:** Does dome shape/vascularity vary continuously with ontogeny?
- **Principal finding:** Frontoparietal dome development and reduction in relative void space/vascularity track size; the UALVP 2 rough estimate is reported at ~7% relative void space.
- **Limitations:** UALVP 2 is a rough estimate in this analysis; measurements are specimen/section dependent and not direct 3-D material-property estimates.
- **Relevance to project:** Provides biological evidence for ontogenetic variation in internal structure and CT segmentation thresholds.
- **Epistemic notes:** UNVERIFIED

#### P12 — McCurry MR, Evans AR, McHenry CR. 2015. The sensitivity of biological finite element models to the resolution of surface geometry: a case study of crocodilian crania. PeerJ 3:e988.

- **Citation:** McCurry MR, Evans AR, McHenry CR. 2015. The sensitivity of biological finite element models to the resolution of surface geometry: a case study of crocodilian crania. PeerJ 3:e988.
- **DOI or stable identifier:** 10.7717/peerj.988
- **URL:** [https://doi.org/10.7717/peerj.988](https://doi.org/10.7717/peerj.988)
- **Publication year:** 2015
- **Publication type:** Research Article
- **Peer-reviewed status:** Peer-reviewed (PeerJ)
- **Taxon / specimen:** Crocodilian crania; multiple specimens
- **Anatomical structure:** cranium
- **Computational method:** 3-D FE sensitivity study
- **Geometry source:** High-resolution surface meshes down-sampled to multiple resolutions; solid element count held constant
- **Material model:** Material/load settings held constant for surface-resolution comparison; exact values UNVERIFIED
- **Loading conditions:** 30 N bite and shake cases in source excerpt; broad local load patches
- **Boundary conditions:** Standardized constraints including point/beam networks; exact details in full text
- **Mesh strategy:** Same number of solid elements across surface resolutions
- **Validation strategy:** No direct experimental validation
- **Sensitivity / UQ methodology:** Surface geometry resolution sensitivity
- **Principal scientific question:** How much does surface-mesh resolution alter FE outputs?
- **Principal finding:** Lowering surface resolution can fluctuate strain magnitudes, but stable comparative results can be achieved at reduced surface resolution when solid element counts are held constant.
- **Limitations:** This supports comparative stability, not equivalence of absolute local stresses; crocodilian skulls are not fossil domes.
- **Relevance to project:** Direct precedent for separating surface geometry resolution from solid-mesh refinement and for reporting local-vs-global sensitivity.
- **Epistemic notes:** UNVERIFIED

#### P13 — Godinho RM, Toro-Ibacache V, Fitton LC, O’Higgins P. 2017. Finite element analysis of the cranium: validity, sensitivity and future directions. Comptes Rendus Palevol 16:600-612.

- **Citation:** Godinho RM, Toro-Ibacache V, Fitton LC, O’Higgins P. 2017. Finite element analysis of the cranium: validity, sensitivity and future directions. Comptes Rendus Palevol 16:600-612.
- **DOI or stable identifier:** 10.1016/j.crpv.2016.11.002
- **URL:** [https://doi.org/10.1016/j.crpv.2016.11.002](https://doi.org/10.1016/j.crpv.2016.11.002)
- **Publication year:** 2017
- **Publication type:** Validation Study / Review-Context Paper
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Human cadaveric cranium
- **Anatomical structure:** cranium
- **Computational method:** 3-D FE validation + sensitivity
- **Geometry source:** Specimen-specific cadaveric skull with CT-based geometry
- **Material model:** Sensitivity to simplified material properties and segmentation
- **Loading conditions:** Equivalent simulated loading to cadaver experiment; exact force UNVERIFIED
- **Boundary conditions:** Experimental constraints replicated as closely as possible; exact details UNVERIFIED
- **Mesh strategy:** Solid FE model; exact mesh metrics UNVERIFIED
- **Validation strategy:** Cadaveric experimental deformation comparison
- **Sensitivity / UQ methodology:** Segmentation/material sensitivity
- **Principal scientific question:** Can FE approximate real cranial deformation under controlled loading?
- **Principal finding:** Absolute deformations were not accurately predicted, but relative high/low strain regions and global deformation modes were reasonably approximated.
- **Limitations:** Human material/geometry and controlled loading differ from fossils; absolute magnitude mismatch remains.
- **Relevance to project:** Strong validation analogue for calibrating claims to patterns vs magnitudes.
- **Epistemic notes:** UNVERIFIED

#### P14 — Moazen M. et al. 2013. A sensitivity analysis to the role of the fronto-parietal suture in Lacerta bilineata: a preliminary finite element study. Anatomical Record.

- **Citation:** Moazen M. et al. 2013. A sensitivity analysis to the role of the fronto-parietal suture in Lacerta bilineata: a preliminary finite element study. Anatomical Record.
- **DOI or stable identifier:** 10.1002/ar.22629
- **URL:** [https://doi.org/10.1002/ar.22629](https://doi.org/10.1002/ar.22629)
- **Publication year:** 2013
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Lacerta bilineata
- **Anatomical structure:** skull; fronto-parietal suture
- **Computational method:** 3-D FE sensitivity
- **Geometry source:** Reconstructed skull geometry; exact imaging source UNVERIFIED
- **Material model:** Exact material values UNVERIFIED
- **Loading conditions:** 10 N vertical anterior tooth load
- **Boundary conditions:** Three nodes at occipital condyle fully constrained in simplified study
- **Mesh strategy:** FE skull models comparing suture representation
- **Validation strategy:** No direct validation in abstract
- **Sensitivity / UQ methodology:** Suture/BC sensitivity
- **Principal scientific question:** How sensitive are skull stresses to inclusion of a cranial suture?
- **Principal finding:** Simplified BCs can underestimate stress magnitude and create artificial concentration at constrained points while still producing qualitative stress patterns.
- **Limitations:** Simplified BCs limit quantitative interpretation; preliminary study.
- **Relevance to project:** Direct evidence that BC artifacts should be characterized before interpreting localized stress.
- **Epistemic notes:** UNVERIFIED

#### P15 — Probabilistic finite element analysis of a craniofacial finite element model. Journal of Theoretical Biology 300:242-253 (2012).

- **Citation:** Probabilistic finite element analysis of a craniofacial finite element model. Journal of Theoretical Biology 300:242-253 (2012).
- **DOI or stable identifier:** 10.1016/j.jtbi.2012.01.031
- **URL:** [https://doi.org/10.1016/j.jtbi.2012.01.031](https://doi.org/10.1016/j.jtbi.2012.01.031)
- **Publication year:** 2012
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Macaca fascicularis
- **Anatomical structure:** cranium
- **Computational method:** Probabilistic FE + LHS
- **Geometry source:** Cranial FE model with homogeneous/non-homogeneous and isotropic/orthotropic alternatives
- **Material model:** Cortical material properties randomized with Gaussian distributions; CV 0.2 or empirical CVs
- **Loading conditions:** Exact loading UNVERIFIED
- **Boundary conditions:** Exact BCs UNVERIFIED
- **Mesh strategy:** 426 deterministic FE simulations
- **Validation strategy:** No direct physical validation reported in abstract
- **Sensitivity / UQ methodology:** Latin hypercube sampling; material-uncertainty propagation
- **Principal scientific question:** How does material-property uncertainty affect cranial stress/strain predictions?
- **Principal finding:** Material variability can be propagated with LHS across competing material-model formulations; 426 deterministic runs were performed.
- **Limitations:** Distribution choices are human/monkey-specific; not fossil tissue data.
- **Relevance to project:** Direct precedent for probabilistic material uncertainty and for separating constitutive-model uncertainty from parameter uncertainty.
- **Epistemic notes:** UNVERIFIED

#### P16 — Marcé-Nogué J. 2022. One step further in biomechanical models in palaeontology: a nonlinear finite element analysis review. PeerJ 10:e13890.

- **Citation:** Marcé-Nogué J. 2022. One step further in biomechanical models in palaeontology: a nonlinear finite element analysis review. PeerJ 10:e13890.
- **DOI or stable identifier:** 10.7717/peerj.13890
- **URL:** [https://doi.org/10.7717/peerj.13890](https://doi.org/10.7717/peerj.13890)
- **Publication year:** 2022
- **Publication type:** Review
- **Peer-reviewed status:** Known peer-reviewed journal article
- **Taxon / specimen:** Fossil and extant biomechanical models
- **Anatomical structure:** skulls/bones/soft tissues broadly
- **Computational method:** Nonlinear FE review
- **Geometry source:** Varied fossil/extant geometries
- **Material model:** Linear elastic is the dominant baseline; nonlinear soft tissue/contact/buckling discussed
- **Loading conditions:** Static structural loading is common; exact case details vary
- **Boundary conditions:** Contacts, sutures and soft tissues can introduce nonlinear BCs
- **Mesh strategy:** Varied meshes; computational cost emphasized
- **Validation strategy:** No new validation experiment; review synthesizes examples
- **Sensitivity / UQ methodology:** Nonlinear model-form alternatives
- **Principal scientific question:** What can nonlinear FEA add to paleontological biomechanics?
- **Principal finding:** Most published paleo FE models use linear materials in static structural problems; nonlinearities can expand the question space to contact, soft tissues, buckling and large deformation.
- **Limitations:** Nonlinear models cost more and require additional assumptions/data; “possible” does not mean required for every question.
- **Relevance to project:** Frames the boundary between current linear baseline and future model-form/UQ extensions.
- **Epistemic notes:** UNVERIFIED

#### P17 — Moore BRS, Roloson MJ, Currie PJ, Ryan MJ, Patterson RT, Mallon JL. 2022. The appendicular myology of Stegoceras validum and implications for the head-butting hypothesis. PLoS ONE 17(9):e0268144.

- **Citation:** Moore BRS, Roloson MJ, Currie PJ, Ryan MJ, Patterson RT, Mallon JL. 2022. The appendicular myology of Stegoceras validum and implications for the head-butting hypothesis. PLoS ONE 17(9):e0268144.
- **DOI or stable identifier:** 10.1371/journal.pone.0268144
- **URL:** [https://doi.org/10.1371/journal.pone.0268144](https://doi.org/10.1371/journal.pone.0268144)
- **Publication year:** 2022
- **Publication type:** Research Article
- **Peer-reviewed status:** Peer-reviewed (PLOS)
- **Taxon / specimen:** Stegoceras validum UALVP 2
- **Anatomical structure:** postcranial skeleton/appendicular musculature
- **Computational method:** Comparative anatomical reconstruction; no cranial FE
- **Geometry source:** Exceptional articulated UALVP 2 skeleton used as osteological basis
- **Material model:** Muscle reconstructions inferred from extant phylogenetic comparisons; exact force values UNVERIFIED
- **Loading conditions:** No FE loading study
- **Boundary conditions:** Anatomical muscle-origin/insertion reconstructions; exact BCs UNVERIFIED
- **Mesh strategy:** No FE mesh
- **Validation strategy:** Comparative anatomical validation by extant muscle anatomy
- **Sensitivity / UQ methodology:** No formal UQ
- **Principal scientific question:** What does UALVP 2 anatomy imply about locomotor and combat-related muscle function?
- **Principal finding:** Authors reconstructed appendicular musculature and discussed implications for the head-butting hypothesis.
- **Limitations:** This is not a cranial FE validation or impact simulation; behavioral implications remain interpretive.
- **Relevance to project:** Important specimen-specific anatomy source for future whole-head/body load-case design and model constraints.
- **Epistemic notes:** UNVERIFIED

#### P18 — Hieronymus TL, Witmer LM, Tanke DH, Currie PJ. 2009. The facial integument of centrosaurine ceratopsids: morphological and histological correlates of novel skin structures. Anatomical Record 292:1370-1396.

- **Citation:** Hieronymus TL, Witmer LM, Tanke DH, Currie PJ. 2009. The facial integument of centrosaurine ceratopsids: morphological and histological correlates of novel skin structures. Anatomical Record 292:1370-1396.
- **DOI or stable identifier:** UNVERIFIED
- **URL:** [https://onlinelibrary.wiley.com/doi/10.1002/ar.20931](https://onlinelibrary.wiley.com/doi/10.1002/ar.20931)
- **Publication year:** 2009
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed journal article; DOI UNVERIFIED
- **Taxon / specimen:** Ceratopsid dinosaurs
- **Anatomical structure:** cranial integument
- **Computational method:** Comparative soft-tissue inference
- **Geometry source:** CT/histology and osteological correlates
- **Material model:** No FE material model
- **Loading conditions:** No FE loading
- **Boundary conditions:** No FE BCs
- **Mesh strategy:** No FE mesh
- **Validation strategy:** Histological/anatomical evidence
- **Sensitivity / UQ methodology:** None
- **Principal scientific question:** What osteological correlates reveal soft-tissue coverings?
- **Principal finding:** Identifies osteological correlates of facial integument, relevant to inferring unpreserved keratinous/soft-tissue structures.
- **Limitations:** Taxon differs from pachycephalosaurs; inferred soft-tissue morphology is not directly observed in fossils.
- **Relevance to project:** Useful for framing the epistemic status of keratin shielding assumptions.
- **Epistemic notes:** DO/AI mixed; exact DOI requires verification.

#### P19 — Farke AA. 2008. Frontal sinuses and head-butting in goats: a finite element analysis. Journal of Experimental Biology 211:3085-3094.

- **Citation:** Farke AA. 2008. Frontal sinuses and head-butting in goats: a finite element analysis. Journal of Experimental Biology 211:3085-3094.
- **DOI or stable identifier:** UNVERIFIED
- **URL:** UNVERIFIED
- **Publication year:** 2008
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed journal article; URL/DOI UNVERIFIED
- **Taxon / specimen:** Capra hircus (goat)
- **Anatomical structure:** frontal sinus/cranium
- **Computational method:** 3-D FE; extant analogue
- **Geometry source:** CT-derived goat skull/cranial sinus geometry; exact source UNVERIFIED
- **Material model:** Literature/CT-derived material mapping; exact values UNVERIFIED
- **Loading conditions:** Simulated head-butting impacts; exact loading UNVERIFIED
- **Boundary conditions:** Physiological skull/neck constraints; exact formulation UNVERIFIED
- **Mesh strategy:** 3-D FE; exact mesh metrics UNVERIFIED
- **Validation strategy:** Comparative/biomechanical analogy, not a direct validation of fossil behavior
- **Sensitivity / UQ methodology:** Sinus/trabecular sensitivity
- **Principal scientific question:** Do sinus struts alter mechanical response to head impacts?
- **Principal finding:** Authors reported that frontal sinuses and their trabecular structure influence stress/strain transmission during impact.
- **Limitations:** Extant goat anatomy and behavior are an analogue, not evidence of pachycephalosaur behavior; details require primary-paper verification.
- **Relevance to project:** Important analogue for interpreting cancellous/strut-bearing cranial regions.
- **Epistemic notes:** Included because Snively & Theodor explicitly build on it; fields not retrieved in this pass are UNVERIFIED.

#### P20 — McCurry MR? 2021. Modeling tooth enamel in FEA comparisons of skulls: comparing common simplifications with biologically realistic models.

- **Citation:** McCurry MR? 2021. Modeling tooth enamel in FEA comparisons of skulls: comparing common simplifications with biologically realistic models.
- **DOI or stable identifier:** UNVERIFIED
- **URL:** [https://pmc.ncbi.nlm.nih.gov/articles/PMC8567004/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8567004/)
- **Publication year:** 2021
- **Publication type:** Research Article
- **Peer-reviewed status:** Known peer-reviewed article; exact bibliographic details UNVERIFIED
- **Taxon / specimen:** Primarily comparative skull/teeth models
- **Anatomical structure:** tooth enamel / skull
- **Computational method:** Comparative FE sensitivity to material simplification
- **Geometry source:** Biologically realistic vs simplified tooth material models
- **Material model:** Tooth material-property alternatives
- **Loading conditions:** Bite loading; exact force UNVERIFIED
- **Boundary conditions:** Constraint/loading artefacts examined near teeth
- **Mesh strategy:** Solid FE skull models; exact mesh metrics UNVERIFIED
- **Validation strategy:** No direct experimental validation reported in abstract
- **Sensitivity / UQ methodology:** Material simplification sensitivity
- **Principal scientific question:** Does biologically realistic enamel material materially change comparative skull FEA?
- **Principal finding:** General stress patterns were similar despite different tooth properties, with localized differences near constrained teeth.
- **Limitations:** Study is tooth-focused; transfer to cranial dome materials is indirect.
- **Relevance to project:** Supports question-specific model detail and localized-artifact reporting.
- **Epistemic notes:** Full citation/DOI UNVERIFIED; retain for follow-up verification.

#### P21 — Zhang L, Cao Z, Zhao Q. 2025. Deep learning-aided segmentation combined with finite element analysis reveals a more natural biomechanic of dinosaur fossil. Scientific Reports 15:13964.

- **Citation:** Zhang L, Cao Z, Zhao Q. 2025. Deep learning-aided segmentation combined with finite element analysis reveals a more natural biomechanic of dinosaur fossil. Scientific Reports 15:13964.
- **DOI or stable identifier:** UNVERIFIED
- **URL:** [https://www.nature.com/articles/s41598-025-99131-4](https://www.nature.com/articles/s41598-025-99131-4)
- **Publication year:** 2025
- **Publication type:** Research Article
- **Peer-reviewed status:** Journal article; peer-review status UNVERIFIED in retrieved page
- **Taxon / specimen:** Dinosaur fossil (taxon not captured in excerpt)
- **Anatomical structure:** CT-segmented fossil geometry
- **Computational method:** Deep-learning segmentation + FEA
- **Geometry source:** CT-derived fossil geometry; segmentation is the experimental variable
- **Material model:** Material/model details UNVERIFIED
- **Loading conditions:** Loading details UNVERIFIED
- **Boundary conditions:** Boundary details UNVERIFIED
- **Mesh strategy:** FE mesh details UNVERIFIED
- **Validation strategy:** No direct validation details in retrieved excerpt
- **Sensitivity / UQ methodology:** Segmentation-method sensitivity
- **Principal scientific question:** How does improved fossil segmentation affect biomechanical simulation?
- **Principal finding:** The authors report that rock matrix in intertrabecular spaces can cause severe FEA deviations and compare deep-learning segmentation with conventional threshold/manual approaches.
- **Limitations:** Full material/mesh/load/validation details require primary-paper extraction.
- **Relevance to project:** Directly relevant to CT segmentation, fossil matrix contamination, and geometry-driven uncertainty.
- **Epistemic notes:** DO: matrix/segmentation issue from abstract. All other detailed fields UNVERIFIED.

#### P22 — Uncertainty quantification and global sensitivity analysis of a patient-specific mandibular finite element model using Latin hypercube sampling and sparse polynomial chaos expansion. 2026. PubMed PMID 42594916.

- **Citation:** Uncertainty quantification and global sensitivity analysis of a patient-specific mandibular finite element model using Latin hypercube sampling and sparse polynomial chaos expansion. 2026. PubMed PMID 42594916.
- **DOI or stable identifier:** UNVERIFIED
- **URL:** [https://pubmed.ncbi.nlm.nih.gov/42594916/](https://pubmed.ncbi.nlm.nih.gov/42594916/)
- **Publication year:** 2026
- **Publication type:** Research Article
- **Peer-reviewed status:** Publication type is Journal Article; peer-reviewed status UNVERIFIED in retrieved record
- **Taxon / specimen:** Human patient-specific mandible
- **Anatomical structure:** mandible
- **Computational method:** UQ FE + LHS + sparse polynomial chaos + Sobol + rank correlations
- **Geometry source:** Patient-specific FE geometry; one variable class included geometric discretization
- **Material model:** 24 uncertain parameters spanning muscle loading, material properties and geometric discretization; exact distributions UNVERIFIED
- **Loading conditions:** Muscle-force parameters and articular-disc stiffness included
- **Boundary conditions:** Contact-sensitive regions; exact BCs UNVERIFIED
- **Mesh strategy:** 2400 simulations; sample-size convergence examined
- **Validation strategy:** Statistical convergence of sensitivity estimates, not physical ground-truth validation
- **Sensitivity / UQ methodology:** Global and regional Sobol indices; Spearman rank correlations
- **Principal scientific question:** How can global UQ be integrated efficiently into patient-specific craniofacial FE?
- **Principal finding:** Muscle force magnitudes and disc stiffness dominated stress variability in the studied model; high-resolution bone property classification had little effect over the tested ranges; regional sensitivity required larger N.
- **Limitations:** Human mandible and contact mechanics differ materially from a fossil skull; current DOI and full methods UNVERIFIED.
- **Relevance to project:** Very recent methodological benchmark for UQ/DoE/surrogate design and convergence of sensitivity estimates.
- **Epistemic notes:** DO: 24 inputs, 2400 simulations, LHS/PCE/Sobol, regional sample-size issue. Results are study-specific.

#### P23 — Bright JA. 2014. A review of paleontological finite element models and their validity. Journal of Paleontology 88(4):760-769.

- **Citation:** Bright JA. 2014. A review of paleontological finite element models and their validity. Journal of Paleontology 88(4):760-769.
- **DOI or stable identifier:** 10.1666/13-090
- **URL:** [https://doi.org/10.1666/13-090](https://doi.org/10.1666/13-090)
- **Publication year:** 2014
- **Publication type:** Review
- **Peer-reviewed status:** Peer-reviewed (repository record)
- **Taxon / specimen:** Paleontological FE models; extant validation literature
- **Anatomical structure:** vertebrate skeletal structures
- **Computational method:** Review of fossil FEA, validation and sensitivity
- **Geometry source:** Varied fossil/extant geometries
- **Material model:** Material properties highlighted as a major uncertainty
- **Loading conditions:** Varied loading cases
- **Boundary conditions:** Validation and sensitivity emphasized; no standardized criterion
- **Mesh strategy:** Varied mesh strategies
- **Validation strategy:** Reviews extant validation experiments and fossil practice
- **Sensitivity / UQ methodology:** Sensitivity + validation synthesis
- **Principal scientific question:** What can paleontological FEA reliably say given uncertain inputs?
- **Principal finding:** Relative stress/strain patterns may be more reliable than absolute magnitudes; validation and sensitivity are essential; unknown fossil material properties limit absolute performance claims.
- **Limitations:** No single universal accuracy criterion; usefulness depends on the scientific question.
- **Relevance to project:** Core review guiding evidence hierarchy and claim calibration.
- **Epistemic notes:** UNVERIFIED

## 4. Evidence matrix — compact index

The CSV is the flat evidence export. For agent use, every source also has stable IDs above, and the fields below should be treated as typed evidence rather than free-form narrative.

| ID | Taxon/specimen | Computational method | Geometry source | Material model | Loading | Boundary conditions | Validation | Sensitivity/UQ |
|---|---|---|---|---|---|---|---|---|
| P01 | Allosaurus fragilis; MOR 693 | 3-D linear static FEA | CT-derived 3-D geometry; 193 transverse slices; pneumatic cavities represented | Not fully captured in abstract; literature-based bone properties; exact spatial assignment UNVERIFIED | Several bite/impact load cases; exact force values by case UNVERIFIED | Constraints representing skull functional loading; exact formulation UNVERIFIED | No experimental validation; hypothesis-testing study | None |
| P02 | Allosaurus fragilis; MOR 693 | 3-D FE, linear/static baseline with comparative load cases | CT-derived skull; fused solid model altered to study suture effects | Bone properties inherited from prior Allosaurus model; exact values UNVERIFIED | Bite/feeding forces plus yield-inducing loads; true dynamic impact noted as a future need | Functional cranial constraints; exact node/DOF details UNVERIFIED | No direct experimental validation; model comparison and hypothesis test | Sensitivity to suture representation; not full UQ |
| P03 | Coelophysis bauri; Allosaurus fragilis; Tyrannosaurus rex | Comparative FE | Comparative fossil skull geometries; exact acquisition details UNVERIFIED | Literature-derived, likely homogeneous elastic in baseline; exact spatial maps UNVERIFIED | Biting/feeding load cases; exact forces UNVERIFIED | Comparative functional constraints; exact formulation UNVERIFIED | No experimental validation | Morphological/parameter comparison rather than uncertainty propagation |
| P04 | Extant and fossil vertebrates | FEA methodological review | CT-derived and reconstructed geometries across studies | Literature-derived materials; uncertainty emphasized | Feeding and structural loading across case studies | Boundary conditions treated as core modeling inputs | Reviews validation/sensitivity literature | Sensitivity and validation discussed conceptually |
| P05 | Human femur models | Probabilistic FE; Monte Carlo sensitivity | Three in vivo CT-based femur models | Geometry, density and mechanical properties treated as random variables | Two loading conditions per model | Exact BCs UNVERIFIED | No direct physical validation in abstract | Monte Carlo sensitivity analysis |
| P06 | Domestic pig | 3-D FE with ex vivo validation and sensitivity analysis | CT-based specimen-specific cranial geometry; resolution limitations explicitly discussed | Material property variation was a major sensitivity driver; detailed local heterogeneity incompletely known | Experimental load reproduced in FE; exact magnitudes UNVERIFIED | Constraints intended to mimic experimental loading; exact details UNVERIFIED | Ex vivo strain-gauge comparison | Material-property sensitivity; no full probabilistic UQ |
| P07 | Extant/fossil biological structures | Comparative FE methodology | Varied biological geometries | Exact material assumptions vary by case; comparison principles are the focus | Comparative load cases normalized for size/shape considerations | Comparative BCs | No direct validation; methodological argument | No formal UQ |
| P08 | Pachycephalosauria; adult Homalocephale and Pachycephalosaurus; subadult pachycephalosaurine | 2-D and 3-D FE; impact mechanics | Reconstructed dorsal skull shapes; one subadult dome model | Histological-zone based materials; keratin layers modeled parametrically | Impact force/closing-speed scenarios; low-speed head impacts emphasized | Exact constraints UNVERIFIED | No direct experimental validation | Parametric keratin thickness/shape sensitivity |
| P09 | Stegoceras validum UALVP 2 (UA 2) and comparative artiodactyls | 3-D FE; recursive partition analysis | Medical CT + high-resolution UTCT; manually cleaned STL; 2.2M-element tetrahedral primary Stegoceras model | Manual fossil material assignment; compact bone capped at >2500 HU; cancellous bone E=1 GPa; keratin E=3.9 GPa, nu=0.28 in Ovibos | 1360 N compressive force for Stegoceras; broad vs concentrated dome loads; force-scaled artiodactyl cases | Occipital condyles constrained against translation/rotation plus nuchal-crest constraints; basitubera constraint tested and produced artifacts | No direct validation; artifact/singularity discussion | Load-distribution sensitivity across keratin-pad scenarios; comparative structural analysis |
| P10 | Pachycephalosaurids; ontogenetic series (not conspecific) | Histological microscopy, not FE | Thin sections across growth series | Histological zones and vascularity characterized directly | No loading | No FE mesh | None | What is the ontogenetic meaning of dome microstructure? |
| P11 | Stegoceras validum; multiple specimens including UALVP 2 | Landmark morphometrics + histology + CT | HRCT images; Huang thresholding for a void-space/vascularity proxy | No FE materials | No loading | No FE BCs | Morphometric/statistical validation across specimens | No FE UQ |
| P12 | Crocodilian crania; multiple specimens | 3-D FE sensitivity study | High-resolution surface meshes down-sampled to multiple resolutions; solid element count held constant | Material/load settings held constant for surface-resolution comparison; exact values UNVERIFIED | 30 N bite and shake cases in source excerpt; broad local load patches | Standardized constraints including point/beam networks; exact details in full text | No direct experimental validation | Surface geometry resolution sensitivity |
| P13 | Human cadaveric cranium | 3-D FE validation + sensitivity | Specimen-specific cadaveric skull with CT-based geometry | Sensitivity to simplified material properties and segmentation | Equivalent simulated loading to cadaver experiment; exact force UNVERIFIED | Experimental constraints replicated as closely as possible; exact details UNVERIFIED | Cadaveric experimental deformation comparison | Segmentation/material sensitivity |
| P14 | Lacerta bilineata | 3-D FE sensitivity | Reconstructed skull geometry; exact imaging source UNVERIFIED | Exact material values UNVERIFIED | 10 N vertical anterior tooth load | Three nodes at occipital condyle fully constrained in simplified study | No direct validation in abstract | Suture/BC sensitivity |
| P15 | Macaca fascicularis | Probabilistic FE + LHS | Cranial FE model with homogeneous/non-homogeneous and isotropic/orthotropic alternatives | Cortical material properties randomized with Gaussian distributions; CV 0.2 or empirical CVs | Exact loading UNVERIFIED | Exact BCs UNVERIFIED | No direct physical validation reported in abstract | Latin hypercube sampling; material-uncertainty propagation |
| P16 | Fossil and extant biomechanical models | Nonlinear FE review | Varied fossil/extant geometries | Linear elastic is the dominant baseline; nonlinear soft tissue/contact/buckling discussed | Static structural loading is common; exact case details vary | Contacts, sutures and soft tissues can introduce nonlinear BCs | No new validation experiment; review synthesizes examples | Nonlinear model-form alternatives |
| P17 | Stegoceras validum UALVP 2 | Comparative anatomical reconstruction; no cranial FE | Exceptional articulated UALVP 2 skeleton used as osteological basis | Muscle reconstructions inferred from extant phylogenetic comparisons; exact force values UNVERIFIED | No FE loading study | Anatomical muscle-origin/insertion reconstructions; exact BCs UNVERIFIED | Comparative anatomical validation by extant muscle anatomy | No formal UQ |
| P18 | Ceratopsid dinosaurs | Comparative soft-tissue inference | CT/histology and osteological correlates | No FE material model | No FE loading | No FE BCs | Histological/anatomical evidence | None |
| P19 | Capra hircus (goat) | 3-D FE; extant analogue | CT-derived goat skull/cranial sinus geometry; exact source UNVERIFIED | Literature/CT-derived material mapping; exact values UNVERIFIED | Simulated head-butting impacts; exact loading UNVERIFIED | Physiological skull/neck constraints; exact formulation UNVERIFIED | Comparative/biomechanical analogy, not a direct validation of fossil behavior | Sinus/trabecular sensitivity |
| P20 | Primarily comparative skull/teeth models | Comparative FE sensitivity to material simplification | Biologically realistic vs simplified tooth material models | Tooth material-property alternatives | Bite loading; exact force UNVERIFIED | Constraint/loading artefacts examined near teeth | No direct experimental validation reported in abstract | Material simplification sensitivity |
| P21 | Dinosaur fossil (taxon not captured in excerpt) | Deep-learning segmentation + FEA | CT-derived fossil geometry; segmentation is the experimental variable | Material/model details UNVERIFIED | Loading details UNVERIFIED | Boundary details UNVERIFIED | No direct validation details in retrieved excerpt | Segmentation-method sensitivity |
| P22 | Human patient-specific mandible | UQ FE + LHS + sparse polynomial chaos + Sobol + rank correlations | Patient-specific FE geometry; one variable class included geometric discretization | 24 uncertain parameters spanning muscle loading, material properties and geometric discretization; exact distributions UNVERIFIED | Muscle-force parameters and articular-disc stiffness included | Contact-sensitive regions; exact BCs UNVERIFIED | Statistical convergence of sensitivity estimates, not physical ground-truth validation | Global and regional Sobol indices; Spearman rank correlations |
| P23 | Paleontological FE models; extant validation literature | Review of fossil FEA, validation and sensitivity | Varied fossil/extant geometries | Material properties highlighted as a major uncertainty | Varied loading cases | Validation and sensitivity emphasized; no standardized criterion | Reviews extant validation experiments and fossil practice | Sensitivity + validation synthesis |
### 4.1 Atomic evidence register

The register below turns each source row into stable, lightweight evidence units without introducing new scientific claims. The text is copied/normalized from the source record above; evidence type is governed by the source epistemic notes.

| Evidence ID | Source | Evidence type | Content |
|---|---|---|---|
| `EV-P01-Q` | P01 | `DO` | Can a CT-derived fossil skull model distinguish feeding hypotheses and quantify cranial strength? |
| `EV-P01-F` | P01 | `DO/AI` | FEA showed high cranial strength relative to estimated muscle-driven bite, supporting a mechanically constrained feeding interpretation by the authors. |
| `EV-P01-L` | P01 | `DO/AI` | Model assumptions, loading, and material properties are reconstructed from early-generation FEA; exact inputs need primary-paper extraction before reuse. |
| `EV-P01-R` | P01 | `SYN` | Historical foundation for CT-to-FEA paleontology and hypothesis testing. |
| `EV-P01-N` | P01 | `DO/AI/MA/UNVERIFIED` | DO: CT basis and main result from Nature abstract. AI: feeding interpretation is author conclusion. MA: material/loading details partly UNVERIFIED. |
| `EV-P02-Q` | P02 | `DO` | Are patent sutures mechanically compatible with predicted feeding stress/strain? |
| `EV-P02-F` | P02 | `DO/AI` | Suture locations/orientations were broadly consistent with accommodating modeled loading, according to the study. |
| `EV-P02-L` | P02 | `DO/AI` | Static treatment of large external loads; suture tissue/soft-tissue properties uncertain. |
| `EV-P02-R` | P02 | `SYN` | Supports separating physiological interpretation from numerical artifacts and motivates load/BC sensitivity. |
| `EV-P02-N` | P02 | `DO/AI/MA/UNVERIFIED` | DO: CT and model basis are stated. AI: suture accommodation conclusion. MA: dynamic loads are simplified as static. |
| `EV-P03-Q` | P03 | `DO` | How does cranial shape influence stress/strain among theropod taxa? |
| `EV-P03-F` | P03 | `DO/AI` | Stress/strain patterns were used to relate skull architecture to functional performance. |
| `EV-P03-L` | P03 | `DO/AI` | Cross-taxon comparisons are sensitive to scaling, material assumptions and load normalization. |
| `EV-P03-R` | P03 | `SYN` | Historical comparative-FEA practice and caveat for cross-model normalization. |
| `EV-P03-N` | P03 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P04-Q` | P04 | `DO` | How has FEA been used to connect form, function and evolution? |
| `EV-P04-F` | P04 | `DO/AI` | FEA enables quantitative stress/strain predictions but depends critically on geometry, material, loads and constraints. |
| `EV-P04-L` | P04 | `DO/AI` | Fossil models inherit large uncertainty from unavailable tissue properties and reconstructed loads. |
| `EV-P04-R` | P04 | `SYN` | Provides historical methodological framework and source map for backward/forward chasing. |
| `EV-P04-N` | P04 | `DO/AI/MA/UNVERIFIED` | DO: review scope and CT/FEA framing. SYN: use as gateway source for citation chasing. DOI field UNVERIFIED. |
| `EV-P05-Q` | P05 | `DO` | How do geometry and material uncertainty affect FE outputs? |
| `EV-P05-F` | P05 | `DO/AI` | Geometry, density and material-property variability can be propagated probabilistically into biomechanical outputs. |
| `EV-P05-L` | P05 | `DO/AI` | Human femur rather than fossil cranium; distributions and correlations are context-specific. |
| `EV-P05-R` | P05 | `SYN` | Direct precedent for geometry + material uncertainty propagation and Monte Carlo design. |
| `EV-P05-N` | P05 | `DO/AI/MA/UNVERIFIED` | DO: Monte Carlo, three femur models, two loads. SYN: transferability to fossils is methodological, not empirical. |
| `EV-P06-Q` | P06 | `DO` | Can FE reproduce measured cranial strain patterns and magnitudes? |
| `EV-P06-F` | P06 | `DO/AI` | Model reproduced loading/overall strain environment better than absolute local strain magnitudes; material properties strongly affected outputs. |
| `EV-P06-L` | P06 | `DO/AI` | CT resolution and missing local material-property data can explain discrepancies; absolute breaking stress/bite force should be treated cautiously. |
| `EV-P06-R` | P06 | `SYN` | Core validation evidence for interpreting pattern vs magnitude and for material UQ. |
| `EV-P06-N` | P06 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P07-Q` | P07 | `DO` | What metrics and normalization are appropriate for comparative FE? |
| `EV-P07-F` | P07 | `DO/AI` | Total strain energy is argued to be a robust metric for comparative performance because it captures work expended in deformation and can help disentangle size/shape effects. |
| `EV-P07-L` | P07 | `DO/AI` | Comparisons remain dependent on consistent loads, constraints and model construction. |
| `EV-P07-R` | P07 | `SYN` | Supports project use of strain energy alongside displacement/stress, and normalization rules. |
| `EV-P07-N` | P07 | `DO/AI/MA/UNVERIFIED` | DO: abstract explicitly argues for total strain energy. SYN: direct relevance to current Phase 4 output design. |
| `EV-P08-Q` | P08 | `DO` | Can dome geometry and internal trabecular structure sustain head impacts? |
| `EV-P08-F` | P08 | `DO/AI` | Authors report that modeled domes could withstand substantial low-speed impacts and that stresses/strains dissipate through the dorsal skull; keratin coverings reduced transmitted force/energy. |
| `EV-P08-L` | P08 | `DO/AI` | Older/adult domes, tissue reconstruction and model assumptions remain uncertain; behavior is not directly observed. |
| `EV-P08-R` | P08 | `SYN` | Direct precursor to Snively & Theodor and key behavioral-mechanics context. |
| `EV-P08-N` | P08 | `DO/AI/MA/UNVERIFIED` | DO: abstract and study page. AI: “permitted head-butting” is the author interpretation. MA: keratin and closing-speed cases are assumed/modelled. |
| `EV-P09-Q` | P09 | `DO` | How do CT-derived cranial structure and modeled impact loads compare among head-striking taxa? |
| `EV-P09-F` | P09 | `DO/AI` | Broad dome loading produced lower/more diffuse stress; local stress peaks occurred near constraints/neurovascular features; authors interpret Stegoceras as mechanically compatible with head-strike behavior. |
| `EV-P09-L` | P09 | `DO/AI` | Force magnitude is biologically scaled but modelled as quasi-static; material properties are not dinosaur measurements; singularities/artifacts and unknown keratin geometry affect absolute stresses. |
| `EV-P09-R` | P09 | `SYN` | Primary benchmark target and central source for UALVP 2 load/material/geometry reconstruction. |
| `EV-P09-N` | P09 | `DO/AI/MA/UNVERIFIED` | DO: 2.2M tet mesh, CT systems, 1360N, materials, BC artifacts, results are directly in full text. AI: behavior inference. MA: static impact and fossil material mapping. |
| `EV-P10-Q` | P10 | `DO` | Authors identified three histological zones and reported that radiating/spongy structures diminish with maturity, interpreting them as transient growth-related structures rather than adaptations for adult head-butting. |
| `EV-P10-F` | P10 | `DO/AI` | Series is not conspecific; external soft-tissue covering is unpreserved; behavioral conclusion is interpretive. |
| `EV-P10-L` | P10 | `DO/AI` | Critical biological prior for internal zonation and material-model uncertainty in adult Stegoceras. |
| `EV-P10-R` | P10 | `SYN` | DO: three zones and ontogenetic changes. AI: “inconsistent with head-butting” is author interpretation. MA: none computational. |
| `EV-P10-N` | P10 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P11-Q` | P11 | `DO` | Does dome shape/vascularity vary continuously with ontogeny? |
| `EV-P11-F` | P11 | `DO/AI` | Frontoparietal dome development and reduction in relative void space/vascularity track size; the UALVP 2 rough estimate is reported at ~7% relative void space. |
| `EV-P11-L` | P11 | `DO/AI` | UALVP 2 is a rough estimate in this analysis; measurements are specimen/section dependent and not direct 3-D material-property estimates. |
| `EV-P11-R` | P11 | `SYN` | Provides biological evidence for ontogenetic variation in internal structure and CT segmentation thresholds. |
| `EV-P11-N` | P11 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P12-Q` | P12 | `DO` | How much does surface-mesh resolution alter FE outputs? |
| `EV-P12-F` | P12 | `DO/AI` | Lowering surface resolution can fluctuate strain magnitudes, but stable comparative results can be achieved at reduced surface resolution when solid element counts are held constant. |
| `EV-P12-L` | P12 | `DO/AI` | This supports comparative stability, not equivalence of absolute local stresses; crocodilian skulls are not fossil domes. |
| `EV-P12-R` | P12 | `SYN` | Direct precedent for separating surface geometry resolution from solid-mesh refinement and for reporting local-vs-global sensitivity. |
| `EV-P12-N` | P12 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P13-Q` | P13 | `DO` | Can FE approximate real cranial deformation under controlled loading? |
| `EV-P13-F` | P13 | `DO/AI` | Absolute deformations were not accurately predicted, but relative high/low strain regions and global deformation modes were reasonably approximated. |
| `EV-P13-L` | P13 | `DO/AI` | Human material/geometry and controlled loading differ from fossils; absolute magnitude mismatch remains. |
| `EV-P13-R` | P13 | `SYN` | Strong validation analogue for calibrating claims to patterns vs magnitudes. |
| `EV-P13-N` | P13 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P14-Q` | P14 | `DO` | How sensitive are skull stresses to inclusion of a cranial suture? |
| `EV-P14-F` | P14 | `DO/AI` | Simplified BCs can underestimate stress magnitude and create artificial concentration at constrained points while still producing qualitative stress patterns. |
| `EV-P14-L` | P14 | `DO/AI` | Simplified BCs limit quantitative interpretation; preliminary study. |
| `EV-P14-R` | P14 | `SYN` | Direct evidence that BC artifacts should be characterized before interpreting localized stress. |
| `EV-P14-N` | P14 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P15-Q` | P15 | `DO` | How does material-property uncertainty affect cranial stress/strain predictions? |
| `EV-P15-F` | P15 | `DO/AI` | Material variability can be propagated with LHS across competing material-model formulations; 426 deterministic runs were performed. |
| `EV-P15-L` | P15 | `DO/AI` | Distribution choices are human/monkey-specific; not fossil tissue data. |
| `EV-P15-R` | P15 | `SYN` | Direct precedent for probabilistic material uncertainty and for separating constitutive-model uncertainty from parameter uncertainty. |
| `EV-P15-N` | P15 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P16-Q` | P16 | `DO` | What can nonlinear FEA add to paleontological biomechanics? |
| `EV-P16-F` | P16 | `DO/AI` | Most published paleo FE models use linear materials in static structural problems; nonlinearities can expand the question space to contact, soft tissues, buckling and large deformation. |
| `EV-P16-L` | P16 | `DO/AI` | Nonlinear models cost more and require additional assumptions/data; “possible” does not mean required for every question. |
| `EV-P16-R` | P16 | `SYN` | Frames the boundary between current linear baseline and future model-form/UQ extensions. |
| `EV-P16-N` | P16 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P17-Q` | P17 | `DO` | What does UALVP 2 anatomy imply about locomotor and combat-related muscle function? |
| `EV-P17-F` | P17 | `DO/AI` | Authors reconstructed appendicular musculature and discussed implications for the head-butting hypothesis. |
| `EV-P17-L` | P17 | `DO/AI` | This is not a cranial FE validation or impact simulation; behavioral implications remain interpretive. |
| `EV-P17-R` | P17 | `SYN` | Important specimen-specific anatomy source for future whole-head/body load-case design and model constraints. |
| `EV-P17-N` | P17 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |
| `EV-P18-Q` | P18 | `DO` | What osteological correlates reveal soft-tissue coverings? |
| `EV-P18-F` | P18 | `DO/AI` | Identifies osteological correlates of facial integument, relevant to inferring unpreserved keratinous/soft-tissue structures. |
| `EV-P18-L` | P18 | `DO/AI` | Taxon differs from pachycephalosaurs; inferred soft-tissue morphology is not directly observed in fossils. |
| `EV-P18-R` | P18 | `SYN` | Useful for framing the epistemic status of keratin shielding assumptions. |
| `EV-P18-N` | P18 | `DO/AI/MA/UNVERIFIED` | DO/AI mixed; exact DOI requires verification. |
| `EV-P19-Q` | P19 | `DO` | Do sinus struts alter mechanical response to head impacts? |
| `EV-P19-F` | P19 | `DO/AI` | Authors reported that frontal sinuses and their trabecular structure influence stress/strain transmission during impact. |
| `EV-P19-L` | P19 | `DO/AI` | Extant goat anatomy and behavior are an analogue, not evidence of pachycephalosaur behavior; details require primary-paper verification. |
| `EV-P19-R` | P19 | `SYN` | Important analogue for interpreting cancellous/strut-bearing cranial regions. |
| `EV-P19-N` | P19 | `DO/AI/MA/UNVERIFIED` | Included because Snively & Theodor explicitly build on it; fields not retrieved in this pass are UNVERIFIED. |
| `EV-P20-Q` | P20 | `DO` | Does biologically realistic enamel material materially change comparative skull FEA? |
| `EV-P20-F` | P20 | `DO/AI` | General stress patterns were similar despite different tooth properties, with localized differences near constrained teeth. |
| `EV-P20-L` | P20 | `DO/AI` | Study is tooth-focused; transfer to cranial dome materials is indirect. |
| `EV-P20-R` | P20 | `SYN` | Supports question-specific model detail and localized-artifact reporting. |
| `EV-P20-N` | P20 | `DO/AI/MA/UNVERIFIED` | Full citation/DOI UNVERIFIED; retain for follow-up verification. |
| `EV-P21-Q` | P21 | `DO` | How does improved fossil segmentation affect biomechanical simulation? |
| `EV-P21-F` | P21 | `DO/AI` | The authors report that rock matrix in intertrabecular spaces can cause severe FEA deviations and compare deep-learning segmentation with conventional threshold/manual approaches. |
| `EV-P21-L` | P21 | `DO/AI` | Full material/mesh/load/validation details require primary-paper extraction. |
| `EV-P21-R` | P21 | `SYN` | Directly relevant to CT segmentation, fossil matrix contamination, and geometry-driven uncertainty. |
| `EV-P21-N` | P21 | `DO/AI/MA/UNVERIFIED` | DO: matrix/segmentation issue from abstract. All other detailed fields UNVERIFIED. |
| `EV-P22-Q` | P22 | `DO` | How can global UQ be integrated efficiently into patient-specific craniofacial FE? |
| `EV-P22-F` | P22 | `DO/AI` | Muscle force magnitudes and disc stiffness dominated stress variability in the studied model; high-resolution bone property classification had little effect over the tested ranges; regional sensitivity required larger N. |
| `EV-P22-L` | P22 | `DO/AI` | Human mandible and contact mechanics differ materially from a fossil skull; current DOI and full methods UNVERIFIED. |
| `EV-P22-R` | P22 | `SYN` | Very recent methodological benchmark for UQ/DoE/surrogate design and convergence of sensitivity estimates. |
| `EV-P22-N` | P22 | `DO/AI/MA/UNVERIFIED` | DO: 24 inputs, 2400 simulations, LHS/PCE/Sobol, regional sample-size issue. Results are study-specific. |
| `EV-P23-Q` | P23 | `DO` | What can paleontological FEA reliably say given uncertain inputs? |
| `EV-P23-F` | P23 | `DO/AI` | Relative stress/strain patterns may be more reliable than absolute magnitudes; validation and sensitivity are essential; unknown fossil material properties limit absolute performance claims. |
| `EV-P23-L` | P23 | `DO/AI` | No single universal accuracy criterion; usefulness depends on the scientific question. |
| `EV-P23-R` | P23 | `SYN` | Core review guiding evidence hierarchy and claim calibration. |
| `EV-P23-N` | P23 | `DO/AI/MA/UNVERIFIED` | UNVERIFIED |

Example: `EV-P09-F` is the principal finding recorded for P09 (Snively & Theodor, 2011); it is not a new claim.

## 5. Topic map

| Topic | Primary source IDs in current corpus | What the corpus contributes |
|---|---|---|
| FEA in paleontology | P01, P02, P03, P04, P08, P09, P16, P23 | Historical and current fossil FE workflows, with emphasis on CT-derived geometry and model-assumption sensitivity. |
| Validation | P06, P13, P23 | Extant specimen validation and reviews show that pattern-level agreement and absolute-magnitude agreement should be distinguished. |
| Sensitivity | P02, P05, P06, P12, P14, P15, P21, P22 | Material properties, geometry, surface resolution, sutures, and loading/constraints can alter FE outputs. |
| UQ | P05, P15, P22 | Probabilistic FE, Monte Carlo, LHS, Sobol, and surrogate approaches are established outside fossil-specific biomechanics. |
| Pachycephalosaurs | P08, P09, P10, P11, P17 | Mechanical and biological evidence relevant to dome structure, ontogeny, and head-strike interpretations. |
| Stegoceras | P09, P11, P17 | Direct biomechanical and ontogenetic evidence centered on S. validum. |
| UALVP 2 | P09, P11 | Published benchmark and ontogenetic context for the project’s lead specimen. |
| Head-strike biomechanics | P08, P09, P10, P17, P19 | FE and histological/functional literature supporting competing interpretations and parameterization issues. |
| CT / segmentation | P01, P06, P09, P11, P13, P21 | CT-derived geometry and segmentation choices can propagate into FE behavior. |
| Geometry / meshing | P01, P09, P12, P21, P23 | Surface-resolution effects, tetrahedral discretization, and fixed-geometry versus geometry-uncertainty separation. |
| Model verification | P06, P13, P23 | Validation literature supports separating numerical/solver verification from biological validation. |
| Nonlinear / model-form | P02, P16 | Nonlinear contact, soft tissue, and dynamics are identified as model-form extensions in paleontological FE review literature. |
| Comparative metrics / energy | P07, P09 | Total strain energy is explicitly discussed as a useful comparative metric. |

## 6. Open questions

| ID | Open question | Evidence status | Status flag | Project implication |
|---|---|---|---|---|
| OQ-01 | Fossil-specific probabilistic UQ precedent | No peer-reviewed fossil cranial FE paper with joint probabilistic treatment of material, loading, geometry/segmentation and numerical/model-form uncertainty was identified in this search pass. This is a search result, not a novelty claim. | TO VERIFY | Future UQ; scientific interpretation |
| OQ-02 | Material-property distributions for UALVP 2 | Snively & Theodor explicitly used manually assigned fossil properties because permineralization/beam hardening complicated CT-based mapping. The biologically defensible distribution for E and nu in an adult Stegoceras dome remains unresolved. | OPEN | Material assumptions; future UQ |
| OQ-03 | Adult internal zonation in UALVP 2 | CT/histology evidence shows structured density/vascularity, while Schott et al. report reduced relative void-space in UALVP 2 and Goodwin & Horner describe ontogenetic remodeling. The exact 3-D geometry of zones is not directly available from the published paper. | OPEN | Geometry pipeline; material assumptions; future UQ |
| OQ-04 | Impact force distribution and direction | The 1,360 N benchmark is biologically contextualized, but exact impact kinematics and contact-area geometry are uncertain. Snively & Theodor explicitly varied load spread because keratin geometry is unknown. | OPEN | Load-case design; future UQ |
| OQ-05 | Boundary-condition realism | Extant validation/sensitivity studies show constraints can produce localized stress artifacts. Fossil head-neck constraints remain model assumptions rather than directly measurable loads. | OPEN | Current Phase 4 FEM; future UQ; interpretation |
| OQ-06 | Surface/segmentation uncertainty | Surface resolution and fossil-matrix segmentation can alter FE results. The recent dinosaur-fossil segmentation study strengthens the case for formal segmentation sensitivity, but complete methodological details remain UNVERIFIED here. | OPEN | Geometry pipeline; future UQ |
| OQ-07 | Local stress vs global compliance | The literature repeatedly distinguishes stable comparative/pattern-level outputs from unstable local magnitudes. The project’s current mesh-convergence record shows the same qualitative pattern. | OPEN | Mesh convergence; scientific interpretation |
| OQ-08 | Linear-static adequacy | Most paleontological FE studies remain linear/static; nonlinear review literature identifies contact, soft tissue and buckling as model-form extensions. Whether nonlinear/dynamic effects materially change the specific Stegoceras question is not yet established. | OPEN | Current Phase 4 FEM; future UQ/model-form study |
| OQ-09 | Model discrepancy | Computational discretization, segmentation, and constitutive simplification are not automatically equivalent to biological parameter uncertainty. A principled discrepancy/error model for fossil FE remains to be verified. | TO VERIFY | Future UQ; verification |
| OQ-10 | Dedicated recent review of pachycephalosaur head-strike hypothesis | A dedicated recent peer-reviewed review was not identified in this search pass; the literature map contains primary studies and general FEA reviews instead. | UNVERIFIED | Head-strike interpretation |

## 7. Project implications

| Issue | Key literature | Affected project areas | Implication |
|---|---|---|---|
| Material properties: E, nu; homogeneous vs zonated | P06, P09, P10, P15, P23 | Current Phase 4 FEM; material assumptions; future UQ | Keep homogeneous Model A as a verification baseline, but do not treat E=17 GPa as fossil-measured. Design future distributions around explicit source provenance; include constitutive/spatial heterogeneity as a model-form branch. |
| Force magnitude | P09, P05, P15, P22 | Load-case design; future UQ | Exploit analytical linear scaling where valid, but retain biologically plausible uncertainty in the unscaled reference force and report normalized outputs where possible. |
| Force direction/contact area | P09, P19, P22 | Load-case design; future UQ | Treat contact direction/area as a separate uncertainty dimension from magnitude. Use broad vs concentrated envelopes rather than a single “true” contact patch. |
| Boundary conditions | P02, P06, P13, P14 | Current Phase 4 FEM; mesh convergence; future UQ | Track BC-induced artifact zones explicitly. Avoid interpreting peaks at rigid constraints or point-like supports as biological maxima without sensitivity evidence. |
| CT segmentation and matrix removal | P09, P11, P13, P21 | Geometry pipeline; future UQ | Preserve provenance and segmentation decisions. A targeted segmentation sensitivity study is warranted before attributing local stresses to biology. |
| Surface geometry / smoothing | P01, P09, P12, P21 | Geometry pipeline; mesh convergence | Keep geometry fixed while testing FE h-refinement; separately vary surface resolution/repair parameters to distinguish geometric from discretization uncertainty. |
| Tetrahedral mesh convergence | P09, P12, P23 | Mesh convergence; current Phase 4 FEM | Use global energy/displacement and regional stress summaries together. Local stress should be reported with convergence diagnostics and artifact masks. |
| Validation | P06, P13, P23 | Current Phase 4 FEM; scientific interpretation | Separate solver verification from biological validation. Cite extant specimen-specific experiments as methodological support, not as direct validation of a fossil. |
| Strain energy | P07, P09 | Current Phase 4 FEM; scientific interpretation | Retain total strain energy as a principal output because comparative FE methodology identifies it as relatively robust under consistent loading/modeling. |
| Nonlinearity/dynamics | P02, P16 | Future UQ/model-form | Treat nonlinear contact, soft tissue, and explicit dynamics as future model-form branches, not as mandatory modifications to the current verified linear baseline. |
| Global sensitivity / Sobol | P05, P15, P22 | Future UQ | Use a staged design: screening -> LHS/space-filling -> surrogate -> variance decomposition. Assess convergence of Sobol estimates rather than choosing N only by convention. |
| Surrogates / active learning | P22 | Future UQ | Recent patient-specific work supports surrogate-assisted global sensitivity as a way to reduce FE cost. Applicability to the fossil problem should be tested against the nonlinearity/discontinuity structure of the chosen outputs. |
| Numerical/model-form uncertainty | P12, P13, P16 | Mesh convergence; future UQ | Do not fold mesh error into biological input distributions without labeling it. Carry numerical error as a distinct uncertainty source or reporting interval. |

## 8. Candidate contribution / novelty claims — all `TO VERIFY`

| ID | Candidate claim | Verification status |
|---|---|---|
| C1 | A fossil cranial FE workflow for Stegoceras/UALVP 2 that couples a fixed CT-derived watertight geometry, solver/analytical verification, h-refinement convergence, and probabilistic sensitivity/UQ over biological and loading inputs. | TO VERIFY against fossil FEA and UQ literature. |
| C2 | A formal separation of biological parameter uncertainty, geometric/segmentation uncertainty, load/BC uncertainty, and numerical/model-form discrepancy in a fossil FE model. | TO VERIFY; no direct fossil example identified in this pass. |
| C3 | A sensitivity-aware interpretation framework that emphasizes energy and global compliance/displacement where stable, while treating local peak stress as discretization/artifact-sensitive. | TO VERIFY as a synthesis contribution; individual ingredients already exist in the literature. |
| C4 | Sample-efficient LHS/Sobol/surrogate workflow tailored to a linear-elastic fossil FE problem with analytical force/modulus scaling. | TO VERIFY; methodological feasibility is established in extant biomechanics, but fossil-specific implementation appears underrepresented in the retrieved search set. |
| C5 | A reproducible public provenance chain from CT acquisition/provenance through geometry repair, meshing, FEA, convergence, and UQ. | TO VERIFY as a community-level contribution; repository documentation is project evidence, not a literature novelty proof. |

## 9. Synthesis: literature says X vs project may contribute Y

| Evidence role | Statement | Support / status |
|---|---|---|
| Literature says X | FEA results depend strongly on geometry, material properties, loads and constraints; validation often shows better agreement for relative patterns than absolute magnitudes. | P06, P13, P23 |
| Literature says X | Localized stress peaks can be dominated by constraints, loading application or geometry/discretization artifacts. | P09, P12, P14 |
| Literature says X | Surface-resolution and material-property sensitivity can alter FE outputs; question-specific model detail matters. | P06, P12, P20 |
| Literature says X | Pachycephalosaur dome function remains interpretively contested: FE studies report mechanical plausibility under modeled impacts, whereas histology studies emphasize ontogenetic/transient internal tissues. | P08, P09, P10, P11 |
| Literature says X | Probabilistic FE, Monte Carlo, LHS, Sobol and surrogate methods are established in extant biomechanics, including craniofacial models. | P05, P15, P22 |
| Our project may contribute Y | A transparent audit trail connecting published UALVP 2 benchmark assumptions to a current reproducible FE implementation and to explicit verification artifacts. | TO VERIFY as contribution, not novelty claim |
| Our project may contribute Y | A formal UQ framework that keeps biological, geometric, loading, and numerical uncertainty conceptually distinct. | TO VERIFY |
| Our project may contribute Y | A principled choice of outputs (energy/compliance/displacement plus artifact-aware stress summaries) tied to convergence diagnostics. | TO VERIFY |

## 10. Interpretation guardrails for agents

1. Treat `Pxx` source records as bibliographic/evidence containers, not as permission to infer missing methodological details.
2. Treat any `UNVERIFIED` value as unknown. Do not autocomplete it from memory or from a similarly named paper.
3. Distinguish `DO`, `AI`, `MA`, and `SYN` when summarizing scientific claims.
4. A project-relevance statement is coordinator synthesis and should not be rewritten as though it were the cited authors’ conclusion.
5. Absence from this corpus is not evidence of absence from the scientific literature; the open-question table marks search-scope findings as `TO VERIFY` where appropriate.
6. Peer-reviewed primary papers outrank reviews for specimen-specific numerical/model details.
7. Extant validation/UQ evidence is methodological precedent, not direct biological validation of a fossil model.

## 11. Review status and limitations

- This is a **scoping-review management artifact**, not a completed systematic review or polished narrative synthesis.
- The current source corpus contains 23 scientific records and a separate deduplication management record P24.
- Some bibliography and methodological fields remain `UNVERIFIED` and require direct primary-source extraction before reuse in quantitative implementation decisions.
- The search was broad and included citation chasing, but no claim of exhaustive database coverage or literature saturation should be inferred from the current pass.
- Candidate novelty statements remain explicitly `TO VERIFY` until targeted forward/backward citation chasing establishes their scope.

## 12. Companion artifacts

- `stegoceras_biomechanics_evidence_matrix.csv` — flat, machine-readable evidence matrix corresponding to the source records in this document.
- `stegoceras_biomechanics_literature_review_management.docx` — human-facing legacy export; not canonical.
- `review_render_check/stegoceras_biomechanics_literature_review_management.pdf` — rendered human-facing export; not canonical.

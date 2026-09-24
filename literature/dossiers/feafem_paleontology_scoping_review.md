# FEA/FEM in Paleontology — Methodological Scoping Review

**Project:** *Stegoceras validum* UALVP 2 biomechanics + future UQ  
**Module:** FEA/FEM in paleontology  
**Status:** Evidence-base module; **not** a manuscript literature-review chapter  
**Search date:** 23 September 2026 (America/Los_Angeles)

## 0. Purpose and evidence rules

This module reviews finite-element analysis/finite-element modeling (FEA/FEM) as used in paleontology and closely transferable vertebrate-biomechanics validation/sensitivity studies. It emphasizes skull/cranium mechanics and extinct-vertebrate applications, while using extant validation studies where those studies constrain interpretation of fossil models.

### Evidence semantics

- `DO` — direct observation/report from a source: specimen, geometry source, model type, parameter, experimental setup, or reported result.
- `AI` — author interpretation/conclusion.
- `MA` — model assumption or simplification required by the simulation.
- `SYN` — coordinator synthesis across sources.
- `UNVERIFIED` — detail not sufficiently verified in the source/authoritative record retrieved in this pass; do not reuse as fact without checking the primary paper.

### Evidence hierarchy

1. Peer-reviewed primary research: primary evidence for methods, model inputs, and results.
2. Peer-reviewed validation/sensitivity/methodological studies: primary evidence for model reliability and transferable methodology.
3. Peer-reviewed reviews: gateway evidence and synthesis; key claims are traced to primary studies where practical.
4. Repositories/websites: bibliographic or access support only; not treated as independent scientific evidence.

---

## 1. Search protocol

### Databases / sources used

- PubMed / PubMed Central
- Publisher pages: Nature, Wiley, Elsevier/ScienceDirect, Cambridge Core, PeerJ
- University repositories for accessible versions and peer-review metadata
- Web-scale exact-title/DOI searching for discovery and citation chasing
- Existing project literature-management corpus for gateway papers and prior candidate records

### Gateway queries

- `"finite element analysis" paleontology review Rayfield`
- `"A review of paleontological finite element models and their validity"`
- `"finite element analysis of the cranium" validity sensitivity future directions`
- `"nonlinear finite element analysis" palaeontology review`
- `"sensitivity and ex vivo validation" pig cranium finite element`
- `"response of cranial biomechanical finite element models" mesh density`
- `"sensitivity" finite element skull material properties loading boundary conditions`
- `"finite-element modeling" anthropoid mandible altered boundary conditions`
- `"assessing mechanical function" zygomatic region macaques finite element validation`
- `"modelling subcortical bone" finite element macaque mandible`
- `"masticatory loadings" cranial deformation Macaca finite element sensitivity`
- `"sensitivity" surface geometry crocodilian crania finite element`
- `"probabilistic finite element analysis" craniofacial Latin hypercube`
- `"Young's Modulus and Load Complexity" finite element`
- `"validation experiments" ostrich cranium finite element`
- `"deep learning-aided segmentation" finite element dinosaur fossil`
- `"finite element" mesh generation skull tetrahedral quadratic linear`
- `"finite element" fossil skull validation strain`

### Chasing strategy

Start with Rayfield 2001/2007, Ross 2005, Bright 2014, Bright & Rayfield 2011 validation/mesh papers, and Godinho et al. 2017. Chase their references for early validation/sensitivity work, then forward-search exact titles/DOIs for later validation, surface-geometry, nonlinear, and probabilistic/UQ studies. A candidate “current practice” or novelty claim is retained as `TO VERIFY` unless forward/backward chasing has been completed to saturation.

---

# 2. Annotated bibliography

## FEA as a paleontological method

### F01 — Rayfield et al. (2001): *Allosaurus* and the early CT-to-FEA paradigm

**Citation:** Rayfield EJ, Norman DB, Horner CC, Horner JR, Smith PM, Thomason JJ, Upchurch P. 2001. Cranial design and function in a large theropod dinosaur. *Nature* 409:1033–1037.  
**DOI:** https://doi.org/10.1038/35059070  
**Type:** Peer-reviewed research article  
**Taxon/specimen:** *Allosaurus fragilis*, MOR 693  
**Structure:** Cranium  

**Method record**

- Geometry: `DO` CT-derived 3-D geometry; Nature describes the model as a geometrically complete, complex skull FE model.
- FE formulation: `DO/MA` 3-D FEA used to estimate mechanical response under loading; exact solver settings not extracted here.
- Materials: `UNVERIFIED` exact material-property table and spatial assignments require primary-paper methods extraction.
- Loads/BCs: `UNVERIFIED` exact magnitudes and constraint node sets require primary-paper methods extraction.
- Mesh: `UNVERIFIED` exact element type/count from primary methods; later methodological literature describes this as an early large 3-D fossil FE model.
- Validation: `DO` no extant experimental validation of the *Allosaurus* model; hypothesis-testing application.

**Scientific use:** `DO/AI` Tests relationships between skull form and feeding mechanics and uses computed stress/strain to evaluate functional hypotheses.

**Limitations for modern use:** `SYN` Early fossil FEA established the paradigm but did not remove uncertainty in tissue properties, loading, or constraints. Its quantitative outputs should not be transplanted as reusable parameter priors without re-checking the original assumptions.

**Project relevance:** Direct historical precedent for a CT-derived fossil skull FE workflow; supports treating geometry, load case, material model, and BCs as explicit model objects rather than implicit choices.

---

### F02 — Rayfield (2005): suture morphology in large carnivorous dinosaurs

**Citation:** Rayfield EJ. 2005. Using finite-element analysis to investigate suture morphology: a case study using large carnivorous dinosaurs. *Anatomical Record* 283A:349–365.  
**DOI:** https://doi.org/10.1002/ar.a.20168  
**Type:** Peer-reviewed research article  
**Taxon/specimen:** *Allosaurus fragilis*, MOR 693  
**Structure:** Cranium/sutures  

**Method record**

- Geometry: `DO` skull FE model used to compare suture treatments.
- FE formulation: `DO` FE analysis used to evaluate mechanical significance of sutures.
- Loads/BCs: `DO/MA` feeding-force loading and functional boundary conditions; exact formulation `UNVERIFIED` in this pass.
- Material model: `UNVERIFIED` exact suture and bone properties require primary-paper extraction.
- Validation: `DO` no direct physical validation; comparative/hypothesis-testing study.
- Sensitivity: `DO` suture representation is the manipulated modeling variable.

**Finding:** `AI` The modeled suture pattern was interpreted as mechanically compatible with the skull's predicted loading environment.

**Limitation:** `SYN` The study also illustrates that anatomical details such as sutures can be mechanically consequential, while the treatment of dynamic loading and suture tissue properties remains model-dependent.

**Project relevance:** For UALVP 2, whether the dome is treated as a fused monolithic continuum, as sutured/heterogeneous structures, or with other interfaces is a biological-model choice, not merely a meshing choice.

---

### F03 — Rayfield (2005): comparative theropod cranial mechanics

**Citation:** Rayfield EJ. 2005. Aspects of comparative cranial mechanics in the theropod dinosaurs *Coelophysis*, *Allosaurus* and *Tyrannosaurus*. *Zoological Journal of the Linnean Society* 144:309–316.  
**DOI:** https://doi.org/10.1111/j.1096-3642.2005.00176.x  
**Type:** Peer-reviewed research article  
**Structure:** Crania  

**Method record:** Comparative FE models under bite/feeding conditions; exact model-material and mesh details `UNVERIFIED` here.

**Scientific use:** `DO/AI` Uses stress/strain patterns to compare cranial mechanics across three theropod taxa and to relate shape to function.

**Project relevance:** Supports comparative output design, but also demonstrates why load normalization, size control, and common modeling conventions are necessary when differences among shapes are interpreted biologically.

---

### F04 — Ross (2005): vertebrate-biomechanics FEA review/special-issue overview

**Citation:** Ross CF. 2005. Finite element analysis in vertebrate biomechanics. *The Anatomical Record* 283A:253–258.  
**DOI:** https://doi.org/10.1002/ar.a.20177  
**Type:** Peer-reviewed review  

**Finding:** `DO` FEA was already being used for complex skeletal structures, skulls, and fossils to examine stress/strain and structure–function questions. The special issue explicitly foregrounded methodological questions around material properties, loading, and validation.

**Project relevance:** Gateway review for the methodological lineage immediately preceding the modern fossil-FEA workflow.

---

## Validation and sensitivity

### F05 — Kupczik et al. (2007): macaque zygomatic-region validation/sensitivity

**Citation:** Kupczik K, Dobson CA, Fagan MJ, Crompton RH, Oxnard CE, O'Higgins P. 2007. Assessing mechanical function of the zygomatic region in macaques: validation and sensitivity testing of finite element models. *Journal of Anatomy* 210:41–53.  
**DOI:** https://doi.org/10.1111/j.1469-7580.2006.00662.x  
**Type:** Peer-reviewed validation/sensitivity study  
**Taxon:** *Macaca fascicularis*  

**Method record**

- Validation: `DO` FE-predicted maximum principal strains were compared with ex vivo strain-gauge measurements.
- Materials: `DO` nanoindentation-derived elastic properties were tested for bone and zygomatico-temporal suture.
- Sutures: `DO` fused, separated, and suture-preserving configurations were compared.
- Loading: `DO` loading through modeled superficial masseter vs nodal loading on the arch produced different strain responses.

**Finding:** `DO/AI` The suture-preserving model and nanoindentation-derived properties improved agreement with experiments; loading application method materially influenced strains.

**Project relevance:** Strong evidence that material properties, anatomical interfaces, and how forces are applied can all change cranial FE response. For UALVP 2, force magnitude alone is not enough; force footprint/direction and contact assumptions require explicit specification.

---

### F06 — Marinescu et al. (2005): boundary-condition sensitivity

**Citation:** Marinescu R, Daegling DJ, Rapoff AJ. 2005. Finite-element modeling of the anthropoid mandible: the effects of altered boundary conditions. *The Anatomical Record* 283A:300–309.  
**DOI:** https://doi.org/10.1002/ar.a.20166  
**Type:** Peer-reviewed research/validation study  
**Taxon:** *Macaca fascicularis* mandible  

**Finding:** `DO` Small errors in load direction produced significant changes in predicted strains. The paper also found improved agreement with experimental strains for a heterogeneous orthotropic model over a simple isotropic one in the tested setup.

**Project relevance:** Direct warning against treating BCs as bookkeeping. UALVP 2 load direction, support region, and force application geometry need sensitivity treatment.

---

### F07 — Ross et al. (2005): masticatory muscle-force sensitivity

**Citation:** Ross CF, Patel BA, Slice DE, Strait DS, Dechow PC, Richmond BG, Spencer MA. 2005. Modeling masticatory muscle force in finite element analysis: sensitivity analysis using principal coordinates analysis. *The Anatomical Record* 283A:288–299.  
**DOI:** https://doi.org/10.1002/ar.a.20170  
**Type:** Peer-reviewed sensitivity study  
**Taxon:** *Macaca* skull models  

**Finding:** `DO` Thirty-six loading regimes were tested from multiple PCSA sets and force-scaling/EMG assumptions.

**Relevance:** Demonstrates that muscle-load reconstruction can be a major source of model variability even before formal probabilistic UQ exists. For head-strike UALVP 2, the analogous uncertainty is external force magnitude, direction, contact area, and timing/impact abstraction.

---

### F08 — Taddei et al. (2006): CT geometry + material uncertainty with Monte Carlo

**Citation:** Taddei F, Martelli S, Reggiani B, Cristofolini L, Viceconti M. 2006. Finite-element modeling of bones from CT data: sensitivity to geometry and material uncertainties. *IEEE Transactions on Biomedical Engineering* 53:2194–2200.  
**DOI:** https://doi.org/10.1109/TBME.2006.879473  
**Type:** Peer-reviewed stochastic FE sensitivity study  
**Taxon/specimen:** Human femur models  

**Method record**

- Sampling: `DO` Monte Carlo sensitivity analysis.
- Inputs: `DO` geometry, density, and mechanical properties treated as uncertain variables.
- Load cases: `DO` two loading conditions were applied.
- Outputs: `DO` biomechanical output variables were evaluated statistically.

**Finding:** `DO` Influence of uncertain inputs depended on load case and output; geometric errors were dominant for stresses in the tested models, while output coefficients of variation were reported as below 9% in the studied setup.

**Important limitation:** `SYN` Human-femur results are not empirical estimates of uncertainty in a fossil cranium. They are methodological precedent for propagating CT/geometry/material uncertainty.

**Project relevance:** Strong precedent for the planned UALVP 2 Monte Carlo/LHS framework and for separating uncertainty in geometry from uncertainty in material properties.

---

### F09 — Panagiotopoulou et al. (2010): subcortical modeling and validation

**Citation:** Panagiotopoulou O, Curtis N, O'Higgins P, Cobb SN. 2010. Modelling subcortical bone in finite element analyses: a validation and sensitivity study in the macaque mandible. *Journal of Biomechanics* 43:1603–1611.  
**DOI:** https://doi.org/10.1016/j.jbiomech.2009.12.027  
**Type:** Peer-reviewed validation/sensitivity study  
**Taxon:** *Macaca* mandible  

**Finding:** `DO/AI` FE predictions were validated with experimental strain data. The study found that cortical-only representation was less effective at resisting bending than coupled cortical/subcortical representation, and that fine subcortical detail could be approximated by a solid with an appropriate Young's modulus in the tested case.

**Project relevance:** Supports explicit consideration of internal architecture/heterogeneity and provides a precedent for controlled simplification when CT resolution makes fine internal structure uncertain.

---

### F10 — Bright & Rayfield (2011a): mesh convergence

**Citation:** Bright JA, Rayfield EJ. 2011. The response of cranial biomechanical finite element models to variations in mesh density. *The Anatomical Record* 294:610–620.  
**DOI:** https://doi.org/10.1002/ar.21358  
**Type:** Peer-reviewed mesh-convergence study  
**Taxon:** Domestic pig skull  

**Method record**

- `DO` Eighteen increasingly refined CT-based FE models were compared.
- `DO` Both linear and quadratic tetrahedral elements were evaluated.
- `DO` Strain and displacement were the convergence outputs.

**Findings:** `DO` Insufficient mesh density underestimated strain/displacement and could fail to resolve stress/strain hot-spots. Different skull regions converged at different rates. Linear tetrahedral models were slightly stiffer than quadratic models in the tested setup but did not converge less rapidly.

**Recommendation:** `AI` Mesh convergence should be performed before further biomechanical interpretation.

**Project relevance:** Directly supports UALVP 2 h-refinement and argues for convergence of the **actual reported outputs**, not merely element count.

---

### F11 — Bright & Rayfield (2011b): ex vivo pig-cranium validation + material sensitivity

**Citation:** Bright JA, Rayfield EJ. 2011. Sensitivity and ex vivo validation of finite element models of the domestic pig cranium. *Journal of Anatomy* 219:456–471.  
**DOI:** https://doi.org/10.1111/j.1469-7580.2011.01408.x  
**Type:** Peer-reviewed validation/sensitivity study  
**Taxon:** Domestic pig cranium  

**Findings:** `DO/AI` The models reproduced aspects of the cranial strain environment but discrepancies remained in absolute values. The model was particularly sensitive to material properties; the paper discusses CT resolution and insufficient knowledge of local heterogeneity as contributors to discrepancies. The authors caution against using such FE models for absolute breaking stress or bite-force estimates without detailed input properties.

**Project relevance:** One of the most important validation precedents for the UALVP 2 interpretation hierarchy: global/relative mechanical patterns can be defensible even when absolute local magnitudes are not.

---

### F12 — Fitton et al. (2012): loading sensitivity in macaque cranium

**Citation:** Fitton LC, Shi JF, Fagan MJ, O'Higgins P. 2012. Masticatory loadings and cranial deformation in *Macaca fascicularis*: a finite element analysis sensitivity study. *Journal of Anatomy* 221:55–68.  
**DOI:** https://doi.org/10.1111/j.1469-7580.2012.01516.x  
**Type:** Peer-reviewed sensitivity study  

**Finding:** `DO` With bite force magnitude controlled, variation in bite location produced larger effects on cranial deformation than the tested variations in muscle activation patterns; the paper also compared inclusion/exclusion of muscle groups.

**Project relevance:** Direct support for treating **load placement/direction** as an uncertainty dimension rather than assuming that magnitude dominates everything.

---

### F13 — Berthaume et al. (2012): probabilistic craniofacial FEA

**Citation:** Berthaume MA, Dechow PC, Iriarte-Diaz J, Ross CF, Strait DS, Wang Q, Grosse IR. 2012. Probabilistic finite element analysis of a craniofacial finite element model. *Journal of Theoretical Biology* 300:242–253.  
**DOI:** https://doi.org/10.1016/j.jtbi.2012.01.031  
**Type:** Peer-reviewed probabilistic FE study  
**Taxon:** *Macaca fascicularis* cranium  

**Method record**

- `DO` Cortical-bone behavior was varied among isotropic homogeneous, isotropic non-homogeneous, and orthotropic non-homogeneous treatments.
- `DO` Material properties were randomized with Gaussian distributions.
- `DO` Latin hypercube sampling was used.
- `DO` 426 deterministic FE simulations were executed.

**Scientific relevance:** Methodological precedent for moving from one deterministic material model to a distribution of plausible material states.

**Project relevance:** Direct methodological analogue for future UALVP 2 material-property UQ and sensitivity analysis; fossil-specific distributions still must be justified independently.

---

## Geometry and segmentation

### F14 — McCurry et al. (2015): surface-geometry resolution sensitivity

**Citation:** McCurry MR, Evans AR, McHenry CR. 2015. The sensitivity of biological finite element models to the resolution of surface geometry: a case study of crocodilian crania. *PeerJ* 3:e988.  
**DOI:** https://doi.org/10.7717/peerj.988  
**Type:** Peer-reviewed sensitivity study  
**Taxon:** Crocodilian crania  

**Finding:** `DO` The study explicitly tests how surface-mesh resolution, derived from the input geometry, affects ensuing FE results in a comparative cranial context.

**Project relevance:** Geometry simplification is not separate from FE uncertainty. A watertight/regularized UALVP 2 surface is a strength, but regularization itself can alter curvature, local thickness, and fine features that may influence stress fields. The geometry pipeline therefore warrants sensitivity testing independently of solid-mesh convergence.

---

### F15 — Godinho et al. (2017): cranium validity, segmentation, and material sensitivity

**Citation:** Godinho RM, Toro-Ibacache V, Fitton LC, O'Higgins P. 2017. Finite element analysis of the cranium: validity, sensitivity and future directions. *Comptes Rendus Palevol* 16:600–612.  
**DOI:** https://doi.org/10.1016/j.crpv.2016.11.002  
**Type:** Peer-reviewed validation/sensitivity study  

**Finding:** `DO` A human cadaveric cranium was experimentally tested against an equivalent FE model. Segmentation and material-property simplifications were also evaluated. `DO` The authors report that absolute deformations were not accurately predicted, but the distribution of relatively high/low strain and the global deformation mode were reasonably approximated.

**Project relevance:** Strong support for reporting multiple levels of output: deformation magnitude, deformation pattern, and spatial stress/strain summaries should not be treated as equally validated.

---

### F16 — Cuff et al. (2015): complete avian-cranium validation

**Citation:** Cuff AR, Bright JA, Rayfield EJ. 2015. Validation experiments on finite element models of an ostrich (*Struthio camelus*) cranium. *PeerJ* 3:e1294.  
**DOI:** https://doi.org/10.7717/peerj.1294  
**Type:** Peer-reviewed validation study  
**Taxon:** *Struthio camelus*  

**Method record**

- `DO` Ex vivo cranial strains were compared with convergence-tested, specimen-specific FE models.
- `DO` Cortical and trabecular bone, sutures, and rhamphotheca were segmented from micro-CT.
- `DO` Material properties were assigned from literature and nanoindentation.

**Finding:** `DO/AI` Peak-strain location and rostral deformation mode could be replicated, but absolute strain magnitude and several regional correlations remained problematic; sutures influenced strain magnitude and pattern.

**Project relevance:** Demonstrates that adding biological detail does not automatically guarantee agreement with experiment. Validation must test the **particular outputs and anatomical regions** used for interpretation.

---

## Comparative metrics and normalization

### F17 — Dumont et al. (2009): comparing FE models of biological structures

**Citation:** Dumont ER, Grosse IR, Slater GJ. 2009. Requirements for comparing the performance of finite element models of biological structures. *Journal of Theoretical Biology* 256:96–103.  
**DOI:** https://doi.org/10.1016/j.jtbi.2008.08.017  
**Type:** Peer-reviewed methodological paper  

**Finding:** `DO/AI` Total strain energy is proposed as a robust metric for comparative mechanical efficiency under appropriate scaling. The paper distinguishes scaling by force:surface-area for stress-strength comparisons from force:volume for strain-energy comparisons.

**Project relevance:** Supports reporting strain energy as a primary global output for UALVP 2, alongside displacement and stress summaries, while making force normalization explicit.

---

### F18 — Sylvester & Kramer (2018): Young's modulus and load complexity

**Citation:** Sylvester AD, Kramer PA. 2018. Young's Modulus and Load Complexity: Modeling Their Effects on Proximal Femur Strain. *The Anatomical Record* 301:1189–1202.  
**DOI:** https://doi.org/10.1002/ar.23796  
**Type:** Peer-reviewed sensitivity study  
**Taxon:** Modern human femur  

**Findings:** `DO` The study varied trabecular Young's modulus and muscle-loading complexity. Changes in loading placement substantially altered strains in the modeled greater-trochanter region, while other regions were less affected in the tested model. The authors recommended a tested Young's-modulus range for that femur application.

**Project relevance:** Reinforces that material sensitivity is structure- and output-dependent; no single “important input” can be assumed without a local sensitivity analysis.

---

## Transition to nonlinear and uncertainty-aware modeling

### F19 — Marcé-Nogué (2022): nonlinear FE review in paleontology/anthropology

**Citation:** Marcé-Nogué J. 2022. One step further in biomechanical models in palaeontology: a nonlinear finite element analysis review. *PeerJ* 10:e13890.  
**DOI:** https://doi.org/10.7717/peerj.13890  
**Type:** Peer-reviewed methodological review  

**Finding:** `DO` Most published paleontological/anthropological FE studies reviewed still used linear materials in static structural problems. The review identifies nonlinear materials, contact between separated structures, and buckling as important extensions where linear/static assumptions can become restrictive.

**Project relevance:** Current Phase 4 linear-static FEM is scientifically interpretable as a baseline model. The literature does not imply that nonlinear FE is required for every fossil problem; rather, nonlinearity should be justified by the biological/mechanical question.

---

### F20 — Zhang, Cao & Zhao (2025): deep-learning segmentation + dinosaur fossil FEA

**Citation:** Zhang L, Cao Z, Zhao Q. 2025. Deep learning-aided segmentation combined with finite element analysis reveals a more natural biomechanic of dinosaur fossil. *Scientific Reports* 15:13964.  
**DOI:** https://doi.org/10.1038/s41598-025-99131-4  
**Type:** Peer-reviewed journal article; the publisher record identifies it as an open-access research article.  
**Taxon/specimen:** *Jeholosaurus* femur specimen  

**Finding:** `DO` The study combines deep-learning segmentation with FEA to address rock matrix occupying intertrabecular spaces in a dinosaur fossil. It presents automated segmentation as a way to better represent trabecular architecture than simple threshold/manual approaches in the tested case.

**Limitation:** `SYN` This is a modern, fossil-specific segmentation/FEA study, but it does not validate a *Stegoceras* cranial model and should not be treated as proof that deep-learning segmentation is universally more accurate.

**Project relevance:** Strengthens the case for treating segmentation method as a possible model-form uncertainty, especially where CT contrast and matrix complicate internal anatomy.

---

### F21 — Baugnon et al. (2026): modern UQ/global sensitivity for mandibular FE

**Citation:** Baugnon L, Nicot R, Bethune N, Lecomte-Grosbras P, Witz J-F, Colliat J-B, Mayeur O. 2026. Uncertainty quantification and global sensitivity analysis of a patient-specific mandibular finite element model using Latin hypercube sampling and sparse polynomial chaos expansion. *Medical Engineering & Physics* 147.  
**DOI:** https://doi.org/10.1088/1873-4030/ae995b  
**Type:** Peer-reviewed journal article record; publication type listed as Journal Article.  

**Method record**

- `DO` 24 input parameters were varied over 2,400 FE simulations.
- `DO` Latin hypercube sampling, sparse polynomial chaos expansion, Spearman-rank analysis, and Sobol indices were used.
- `DO` Inputs included masticatory muscle loading, material properties, and geometric discretization.

**Finding:** `DO` The dominant stress variability in that patient-specific mandible framework came from muscle-force magnitudes and articular-disc stiffness; the influence of high-resolution bone-property classification was small over the tested ranges. Sample-size requirements differed between global and contact-sensitive regional outputs.

**Project relevance:** This is direct evidence that modern biomechanics UQ can integrate sampling, surrogate representations, and variance-based sensitivity. It is methodological precedent only: fossil-specific priors and model-form uncertainty remain open.

---

# 3. Evidence matrix

| ID | Core issue | Taxon | FE method | Key manipulated input | Validation? | Main evidence | Transfer to UALVP 2 |
|---|---|---|---|---|---|---|---|
| F01 | Early fossil FEA / CT geometry | *Allosaurus* | 3-D FE | Functional load/shape | No direct | CT-derived fossil FEA can test form–function hypotheses | High |
| F02 | Sutures / interfaces | *Allosaurus* | 3-D FE | Suture representation | No direct | Anatomical interfaces can alter stress/strain paths | High |
| F03 | Comparative skull mechanics | Theropods | Comparative FE | Taxon shape/loading | No | Shape–mechanics comparison is a core use | High, with normalization |
| F04 | Methodological framing | Extant + fossil | Review | — | Review | FEA links form, function, stress/strain | High |
| F05 | Material + suture + load application | *Macaca* | Validated FE | Materials, sutures, load path | Yes | Inputs materially affect prediction | High |
| F06 | Boundary conditions | *Macaca* mandible | FE validation | Load direction, constraints, tissue model | Yes | Small load-direction errors can matter greatly | Very high |
| F07 | Muscle/loading uncertainty | *Macaca* | FE sensitivity | PCSA/EMG/force scaling | Indirect | Many plausible loading regimes yield different responses | Very high |
| F08 | Geometry/material uncertainty | Human femur | Monte Carlo FE | Geometry, density, material | No direct | Uncertainty can be propagated statistically; effect depends on output/load | Very high |
| F09 | Internal bone representation | *Macaca* mandible | Validated FE | Subcortical geometry | Yes | Simplified internal structure can change bending response | High |
| F10 | Solid-mesh convergence | Pig skull | h-refinement FE | Element density/type | No external validation | Insufficient mesh can underresolve strain/hot-spots | Very high |
| F11 | Material sensitivity + validation | Pig cranium | Validated FE | Material heterogeneity | Yes | Patterns can agree while absolute magnitudes remain wrong | Very high |
| F12 | Load location/activation | *Macaca* | FE sensitivity | Bite location, muscle activation | Indirect | Load placement can dominate some outputs | Very high |
| F13 | Probabilistic material UQ | *Macaca* cranium | Probabilistic FE | Material distributions | No direct | LHS can propagate plausible material variability | Very high for future UQ |
| F14 | Surface geometry resolution | Crocodilian crania | FE sensitivity | Surface resolution | No direct | Geometry discretization affects FE outputs | Very high |
| F15 | Segmentation/material simplification | Human cranium | Validated FE | Segmentation + materials | Yes | Global deformation pattern can be credible despite magnitude error | Very high |
| F16 | Biological detail + validation | Ostrich cranium | Convergence-tested FE | Sutures, tissue properties | Yes | Peak location/mode may replicate while regional magnitudes remain problematic | High |
| F17 | Comparative output metrics | Biological FE | Method paper | Normalization/metric | Not primary validation | Strain energy can support comparisons under controlled scaling | High |
| F18 | E + load complexity | Human femur | FE sensitivity | Young's modulus + loading | Experimental comparison in source context | Input effects are regional/output dependent | High |
| F19 | Nonlinearity | Palaeontology/anthropology | Review | Material/contact/buckling | Review | Linear static dominates; nonlinear tools broaden questions | Medium-high |
| F20 | Segmentation of fossil matrix | Dinosaur femur | FEA + deep learning | Segmentation method | Biological realism claim, not fossil mechanical validation | Segmentation can be consequential in fossil FE | High for geometry pipeline |
| F21 | Modern global UQ | Human mandible | LHS + PCE + Sobol | 24 inputs incl. loads/material/discretization | Model framework, not fossil validation | Modern UQ can rank input contributions and quantify output variability | Very high for future Phase 5 |

---

# 4. Methodological timeline

| Period | Development | Evidence | What changed |
|---|---|---|---|
| **2001** | CT-derived 3-D fossil skull FEA becomes a practical paleontological hypothesis-testing tool | Rayfield et al. F01 | Shift from qualitative reconstruction toward quantitative stress/strain analysis |
| **2005** | FEA expands into comparative theropod mechanics, skull sutures, and vertebrate modeling methodology | F02–F04, F06–F07 | Greater explicit attention to loading, material properties, BCs, and comparative interpretation |
| **2006–2010** | Validation and sensitivity become central methodological questions; geometry/material uncertainty and internal structure are tested | F05, F08, F09 | Stronger recognition that model inputs are not neutral implementation details |
| **2011–2012** | Cranial mesh convergence, ex vivo validation, probabilistic FE, and load sensitivity become explicit study topics | F10–F13 | “How many elements?” begins to become an empirical convergence question; uncertainty propagation becomes practical |
| **2014–2017** | Paleontology-focused methodological reviews consolidate limitations; cranial validation studies emphasize pattern vs magnitude | F15 + Bright review | Fossil FEA increasingly framed as comparatively robust but absolutely uncertain |
| **2015 onward** | Surface-geometry resolution becomes an explicit numerical sensitivity variable; complete avian validation adds biological complexity | F14, F16 | Geometry processing itself becomes part of the uncertainty chain |
| **2018** | Regional/material/loading sensitivity studies quantify output-dependent effects | F18 | Importance of inputs is shown to depend on anatomical region and scientific output |
| **2022** | Nonlinear FE becomes a clearly articulated frontier in paleontology/anthropology | F19 | Linear-static models remain common, but nonlinear material/contact/buckling applications are technically accessible |
| **2025** | Fossil-specific segmentation/FE workflows use machine learning to address matrix/CT challenges | F20 | Segmentation is increasingly treated as a computational-method problem, not just manual preprocessing |
| **2026** | Patient-specific biomechanics integrates LHS, polynomial chaos, global sensitivity, and thousands of simulations | F21 | UQ can move from one-at-a-time sensitivity to global uncertainty propagation and surrogate-assisted analysis |

---

# 5. Consensus findings

### C1 — FEA is well suited to comparative form–function questions

`DO/SYN` Across the methodological reviews and primary fossil studies, FEA is consistently used to compare mechanical performance of complex 3-D skeletal shapes and to relate morphology to stress, strain, deformation, and energy. It is particularly useful when the scientific question is **comparative** rather than an attempt to reconstruct a single exact historical stress state. [F01, F03, F04, F17]

### C2 — Absolute stress/strain magnitudes are more vulnerable than spatial patterns

`DO/SYN` Validation studies repeatedly report substantial discrepancies in absolute strain/deformation magnitude even when model and experiment agree better on strain orientation, deformation mode, or location of higher/lower strain. This is especially relevant to fossil models, where tissue properties and loading cannot be measured directly. [F11, F15, F16]

### C3 — Material properties are a first-order uncertainty source

`DO/SYN` Material-property choices can materially change predicted response; experimentally informed properties and heterogeneity often improve agreement with measurements. However, the magnitude of material sensitivity is output- and model-dependent. [F05, F08, F11, F13, F18]

### C4 — Loads and boundary conditions are not implementation trivia

`DO/SYN` Loading direction, loading location, muscle-force distribution, and constraints can substantially alter FE output. In some tested cranial models, changes in loading location had larger effects than other biological loading assumptions. [F05–F07, F12]

### C5 — Mesh convergence must be demonstrated on outputs of interest

`DO/SYN` The strongest direct mesh evidence in cranial FE shows that insufficient mesh density can bias displacement/strain and fail to resolve localized features, and different regions converge at different rates. Element count alone is not a valid convergence criterion. [F10]

### C6 — Geometry has two distinct uncertainty layers

`SYN` There is a **biological geometry layer** (what anatomy is reconstructed/segmented) and a **numerical geometry layer** (how the surface is smoothed, simplified, and discretized). The literature provides separate sensitivity evidence for both. [F08, F09, F14, F20]

### C7 — Relative comparison is more defensible than unsupported absolute thresholding

`DO/SYN` Bright's paleontological review and multiple validation studies argue for caution with absolute breaking stress, absolute force, or other threshold-like values when tissue properties and loads are poorly constrained. [F11, plus Bright review described below]

### C8 — Linear static FE is a baseline, not a universal endpoint

`DO/SYN` Linear static models remain common in paleontology, largely because of computational cost and interpretive simplicity; nonlinear contact, material behavior, and buckling are recognized as important when the biological question specifically requires them. [F19]

### C9 — Uncertainty analysis can be escalated in stages

`SYN` The literature supports a progression: deterministic verification → local sensitivity → probabilistic propagation → global sensitivity/surrogates. There is no methodological requirement to begin with full Sobol/PCE workflows before the deterministic model is verified and converged. [F08, F13, F21]

---

# 6. Disagreements / limitations / unresolved issues

## D1 — “Patterns are reliable” is not universal

Validation is encouraging but not universal. Ostrich and human-cranium validation show regional pattern agreement can coexist with poor magnitude agreement, and some low-strain regions may show different deformation modes. Therefore “pattern validation” should not be generalized to every anatomical subregion. [F15, F16]

## D2 — Which inputs dominate depends on the output

Material properties, load placement, geometry, and internal structure do not have a fixed ranking across models. Their importance changes with anatomical region and chosen output. [F08, F12, F18, F21]

## D3 — Simplification can be acceptable, but only relative to the question

Subcortical bone, sutures, rhamphotheca, and heterogeneity can matter, but whether they matter scientifically depends on the output region and question. This argues for **question-dependent model complexity**, not maximum complexity by default. [F09, F16, F19]

## D4 — Mesh convergence does not validate the biological model

A converged solution is a numerical result for a specified model. It does not establish that the geometry, materials, loads, or BCs are biologically correct. `SYN` UALVP 2 should therefore treat mesh convergence, verification, and biological uncertainty as separate evidence layers.

## D5 — Fossil-specific UQ remains less developed than extant/patient-specific UQ

`SYN` The retrieved evidence contains clear fossil-specific validation/sensitivity work and clear modern probabilistic/global-UQ work, but much less evidence of a fully probabilistic **fossil skull** workflow that jointly propagates geometry, materials, loads, BCs, and model discrepancy. This is a candidate gap, **not yet a novelty claim**.

---

# 7. What the literature implies a modern fossil FEA paper should report

The following is a **reviewer-facing synthesis**, not a formal reporting standard.

### Geometry / provenance

- Specimen identifier and taxonomic assignment.
- Imaging modality, voxel dimensions, slice spacing, scan provenance, and preprocessing.
- Segmentation protocol and segmentation uncertainty/alternative masks where scientifically relevant.
- Surface reconstruction, smoothing/regularization, feature-preservation decisions, and watertightness checks.
- Any retrodeformation, symmetry reconstruction, missing-data reconstruction, or artifact removal.

### FE formulation

- Solver/software/version when relevant.
- Static vs dynamic formulation.
- Linear vs nonlinear material behavior.
- Element family/order and integration assumptions.
- Contact/interface treatment and suture/soft-tissue representations.

### Materials

- Young's modulus, Poisson's ratio, density, strength/failure assumptions where used.
- Source and rationale for every material parameter.
- Whether properties are homogeneous/isotropic/orthotropic/heterogeneous.
- Mapping procedure from CT to properties, where applicable.
- Sensitivity range or distribution for uncertain properties.

### Loads and boundary conditions

- Force magnitude, direction, location, footprint/distribution.
- Muscle force derivation where relevant.
- Support/constraint region and exact constraint strategy.
- Reaction-force checks and force/moment balance.
- Alternative plausible load cases when biological uncertainty is material.

### Mesh

- Element type/order.
- Element/node counts and size statistics.
- Quality metrics.
- Mesh-generation method and major cleanup operations.
- At least one convergence study tied to the final scientific outputs.
- Evidence that localized features used for interpretation are not numerical artifacts.

### Verification / validation

- Analytical or manufactured-solution verification where applicable.
- Force/moment/equilibrium checks.
- Mesh convergence.
- Experimental validation against extant analogues where feasible.
- Clear distinction among verification, validation, and sensitivity analysis.

### Outputs / interpretation

- Global outputs such as strain energy and displacement.
- Regional stress/strain summaries with region definitions.
- Rules for excluding singular/high-gradient boundary artifacts.
- Whether absolute magnitudes are intended as predictions or only relative comparisons.
- Sensitivity or uncertainty intervals for biologically meaningful conclusions.

---

# 8. Concrete implications for the UALVP 2 model

| Issue | Current Phase 4 FEM | Mesh convergence | Geometry pipeline | Load-case design | Material assumptions | Future UQ | Interpretation |
|---|---|---|---|---|---|---|---|
| Material properties | Use explicit documented baseline; avoid unexplained “fossil defaults” | Run same material across convergence tiers | Preserve material-region topology where possible | Include E/ν sensitivity once baseline is stable | Treat E/ν as uncertain inputs, not constants of nature | Monte Carlo/LHS; later Sobol/Morris | Avoid unsupported absolute failure/stress claims |
| Load magnitude | Document exact vector/resultant | Verify convergence under representative loads | Ensure load footprint maps cleanly to geometry | Use multiple plausible magnitudes/directions/contact areas | Do not infer one historical force as certain | Sample force magnitude and direction | Interpret load-dependent outputs conditionally |
| Boundary conditions | Encode exact constrained nodes/regions | Repeat convergence with same BCs | Avoid support surfaces that depend on mesh artifacts | Test plausible support/contact formulations | Treat BC choice as epistemic uncertainty | Include BC/load configuration as categorical or parameterized input | Reaction forces and constraint artifacts must be visible |
| Geometry/segmentation | Freeze a versioned canonical surface | Converge FE discretization independently | Preserve masks + surface revision history | Generate alternative geometries if segmentation ambiguity is material | Map uncertainty to geometry, not only material | Geometry perturbation / segmentation alternatives | Distinguish reconstruction uncertainty from numerical error |
| Surface regularization | Use only documented, reproducible filters | Confirm output stability after regularization | Compare raw-vs-regularized geometry where feasible | Avoid interpreting smoothing-induced hot-spots | N/A | Candidate model-form uncertainty | “Watertight” does not equal “biologically exact” |
| Mesh generation | TetGen workflow is appropriate for a reproducible baseline | Use h-refinement and output-specific convergence | Keep surface and volume meshes linked by version | Avoid changing geometry while testing mesh density | N/A | Include discretization only after deterministic convergence is established | Local stress peaks need extra caution |
| Stress outputs | Report robust regional summaries rather than isolated peak voxels/elements | Demonstrate local and global convergence separately | Preserve anatomical ROI definitions | Compare load cases consistently | Propagate E/ν uncertainty | Quantile/interval summaries | Peaks near supports/load contacts are especially sensitive |
| Energy | Current candidate global metric | Verify convergence | Less dependent on a single local hot-spot | Compare under controlled scaling | Still load/material dependent | Suitable UQ output | Strong candidate global output |
| Apex displacement | Current candidate global/local output | Converge directly | Sensitive to dome geometry | Useful for force-direction scenarios | Scales with stiffness | Suitable UQ output | Potentially more stable than a local stress maximum |

---

# 9. Recommended implementation order for UALVP 2

This sequence follows the literature's evidence hierarchy rather than assuming that every possible uncertainty must be modeled immediately.

1. **Verification:** analytical/simple cases; equilibrium and reaction-force checks.
2. **Canonical geometry freeze:** record segmentation, surface reconstruction, regularization, and version.
3. **Mesh convergence:** converge energy, apex displacement, and pre-defined regional stress summaries.
4. **Load-case validation-by-analogy:** justify force direction, footprint, support region, and magnitude from published head-strike/cranial biomechanics rather than treating one load case as uniquely known.
5. **Local sensitivity:** E, ν, force magnitude, force direction, BC variants, and geometry variants.
6. **Probabilistic propagation:** LHS/Monte Carlo over justified ranges/distributions.
7. **Global sensitivity:** Morris/Sobol or equivalent variance-based/global method after the response surface is demonstrably stable.
8. **Surrogate model:** only if computational cost justifies it and the surrogate is itself verified against withheld FE evaluations.
9. **Model discrepancy / numerical-form uncertainty:** carry persistent discretization, segmentation, and biological-model ambiguity into interpretation rather than collapsing them into parameter noise.

---

# 10. Candidate contributions — `TO VERIFY`

These are **hypotheses for literature gap checking**, not novelty claims.

- `TO VERIFY-01`: A reproducible, open CT-to-watertight-geometry-to-TetGen-to-FEM workflow for UALVP 2 with explicit analytical verification and output-specific mesh convergence may be uncommon in pachycephalosaur biomechanics.
- `TO VERIFY-02`: A fossil cranial FE study that jointly quantifies uncertainty in material properties, force magnitude, force direction, geometry/segmentation, and numerical discretization may be rare or absent; this requires a broader systematic citation chase.
- `TO VERIFY-03`: A pachycephalosaur-specific study that reports UQ distributions for energy, apex displacement, and regional stress summaries may be absent from the literature retrieved here.
- `TO VERIFY-04`: Explicit treatment of mesh/discretization uncertainty as a component of model-form uncertainty, rather than only demonstrating a single converged mesh, may be underdeveloped in fossil cranial FEA.

**Do not convert any of the above into a novelty statement until a saturation-level forward/backward citation search has been completed.**

---

# 11. Source-to-question index

| User question | Primary evidence in this module |
|---|---|
| 1. How has FEA been used in paleontology? | F01–F04, F19–F20 |
| 2. What biological questions is it suited to answer? | F01, F03, F04, F17 |
| 3. Major methodological assumptions? | F05–F07, F11–F16, F19 |
| 4. Validation studies? | F05, F06, F09, F11, F15, F16 |
| 5. Sensitivity studies? | F05–F14, F18, F21 |
| 6a. Material properties? | F05, F08, F11, F13, F18 |
| 6b. Loading? | F05–F07, F12, F18, F21 |
| 6c. Boundary conditions? | F06, F12 |
| 6d. Geometry? | F08, F09, F14, F15, F20 |
| 6e. Segmentation? | F14, F15, F20 |
| 6f. Mesh density? | F10 |
| 6g. Mesh-generation method? | F10, F14; broader solver-specific evidence still `TO VERIFY` |
| 7. Limits of absolute stress/strain? | F11, F15, F16 + Bright 2014 review |
| 8. Recurring recommendations? | Section 7 + F10–F17 |
| 9. Early vs current practice? | Timeline + F19–F21 |
| 10. What should a modern fossil-FEA study report? | Section 7 |

---

# 12. High-priority references to add in the next citation-chasing pass

These topics are important enough that the current module should be expanded before being considered saturated:

- More **extant cranium validations** spanning mammals, crocodilians, and birds, especially papers cited by Bright 2014 and Cuff 2015.
- More direct **fossil skull FE studies** after 2017 to determine how reporting practice has changed.
- Specific **mesh-generation algorithm / element-topology comparisons** in biological skull FE beyond mesh density alone.
- **Segmentation reproducibility** studies that quantify inter-segmenter or algorithmic uncertainty and then propagate it through FE.
- Fossil-specific **probabilistic/global UQ**, especially studies that vary loads + materials + geometry jointly.
- Formal **model discrepancy / Bayesian calibration** methods from computational mechanics that can be adapted to fossil biomechanics.
- Recent **dynamic head-impact FE validation** in extant skulls, because this bears directly on whether static head-strike abstractions are adequate.

---

## 13. Citation verification notes

The following bibliographic details were directly verified against authoritative publisher/PubMed/repository records during this pass: Rayfield et al. 2001 DOI; Rayfield 2005 suture DOI; Rayfield 2005 comparative DOI; Ross 2005 review DOI; Kupczik et al. 2007 DOI; Marinescu et al. 2005 DOI; Ross et al. 2005 muscle-force sensitivity DOI; Taddei et al. 2006 DOI/pages; Panagiotopoulou et al. 2010 DOI; Bright & Rayfield 2011 mesh DOI; Bright & Rayfield 2011 validation DOI; Fitton et al. 2012 DOI; Berthaume et al. 2012 DOI; McCurry et al. 2015 DOI; Cuff et al. 2015 DOI; Godinho et al. 2017 DOI; Sylvester & Kramer 2018 DOI; Marcé-Nogué 2022 DOI; Zhang et al. 2025 DOI; Baugnon et al. 2026 DOI.

Where a method detail is not explicit in the retrieved authoritative record, this module labels it `UNVERIFIED` rather than filling it from secondary summaries.

---

## 14. Bottom line for the project — evidence synthesis, not a verdict

`SYN` The methodological literature supports a defensible sequence in which **verification and mesh convergence precede biological interpretation**, while **material properties, loads, BCs, and geometry are treated as uncertainty-bearing inputs rather than fixed truths**. Extant validation studies support caution about absolute stress/strain magnitudes; they do not imply that all fossil-FEA outputs are unreliable. The most defensible UALVP 2 interpretation therefore appears to be a layered one: establish numerical correctness for the implemented model, quantify the sensitivity of biologically meaningful outputs, then propagate the largest justified sources of biological and modeling uncertainty.

That synthesis is the methodological basis for the project's current Phase 4 baseline and future UQ design; it is not a claim that the project has yet demonstrated a novel contribution.

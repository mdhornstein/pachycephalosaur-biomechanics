# *Stegoceras* Biomechanics + UQ — Integrated Literature Synthesis
> **Status:** Evidence-based synthesis of four literature modules. This is a literature review, not a final manuscript discussion chapter.
> **Search/update context:** review materials searched/updated in September 2026; recent 2026 literature was checked separately because it falls after the project's earlier evidence modules.
> **Epistemic rule:** `DO` = direct observation/report; `AI` = author interpretation; `MA` = model assumption; `IN` = inference; `SYN` = reviewer synthesis; `UNVERIFIED` = not sufficiently checked; `TO VERIFY` = candidate contribution requiring further citation chasing.

## 1. Scope and review methodology

### Research questions
This synthesis asks how finite-element methods have developed in paleontology; what biological questions fossil FEA can answer reliably; how CT-derived geometry, materials, loading and numerical discretization affect inference; what the *Stegoceras validum* / UALVP 2 literature actually established; how uncertainty and sensitivity should be represented; and what a defensible modern UALVP 2 FEM/UQ study can contribute without overstating behavioral inference.

### Search strategy
The four component reviews searched PubMed/PMC, publisher platforms, university/repository sources, and web-scale exact-title/DOI searches. Gateway papers included Rayfield's early dinosaur FEA, the Bright/Rayfield validation and mesh studies, major paleontological FEA reviews, the Snively/Cox and Snively/Theodor pachycephalosaur studies, and methodological UQ/VVUQ papers. Searches used combinations of `finite element analysis`, `paleontology`, `cranial biomechanics`, `validation`, `mesh density`, `material properties`, `loading`, `boundary conditions`, `segmentation`, `surface geometry`, `probabilistic finite element`, `uncertainty quantification`, `Morris`, `Sobol`, `Latin hypercube`, `Gaussian process`, `Bayesian calibration`, and fossil/dinosaur/Stegoceras/UALVP 2 terms. Backward and forward-oriented citation chasing was used to identify primary validation and sensitivity studies.

### Source-selection rules
Peer-reviewed primary studies were prioritized for empirical observations, model inputs and reported results; peer-reviewed methodological studies/reviews were used for field-wide or transferable methodological conclusions; institutional museum pages were used only for specimen provenance; non-peer-reviewed or repository copies were not treated as equivalent scientific evidence. When a paper-level detail was not verified from the primary source or authoritative metadata, it remains `UNVERIFIED` rather than being reconstructed from memory.

### Review limitations
This is a scoping synthesis rather than a formal PRISMA systematic review. The citation chase is broad but not exhaustive across every branch of computational biomechanics. Some older papers have incomplete bibliographic/parameter extraction in the component dossiers. Fossil-specific validation and formal probabilistic UQ remain sparse compared with extant/patient-specific biomechanics. Recent 2026 studies may not yet have extensive follow-on literature. Absence from this corpus is not evidence of absence, so novelty statements below are deliberately conservative.

## 2. FEA in paleontology

### 2.1 Historical development
The modern paleontological FEA trajectory is anchored by Rayfield et al. (2001), who used a CT-derived three-dimensional *Allosaurus* cranium to move vertebrate paleobiomechanics toward quantitative stress/strain analysis. Subsequent work used FEA to examine cranial form-function relationships, sutures, comparative feeding mechanics, and other structural questions. [FE-01–FE-04]
By the mid-2000s, the methodological question was no longer simply whether fossils could be modeled, but how sensitive conclusions were to the assumptions required to make a fossil solvable: material properties, muscle/load application, constraints, geometry simplification and internal structure. Validation studies on extant cranial models and CT-derived bones made that issue explicit. [FE-05–FE-09]
The 2011 Bright & Rayfield papers were especially influential for cranial FEA because they separately examined mesh-density effects and ex vivo validation/sensitivity. Their results showed that under-resolved meshes can change displacement/strain magnitudes and miss localized high-strain regions, while validation can show better agreement in broad deformation or spatial patterns than in absolute magnitudes. [FE-10, FE-11]
Later work expanded the uncertainty chain upstream to surface geometry and segmentation, and downstream to probabilistic FE, nonlinear formulations, and global sensitivity analysis. [FE-13, FE-14, FE-15, FE-18–FE-21]

### 2.2 What fossil FEA is well suited to answer
The literature supports FEA most strongly as a **comparative, mechanistic tool**: it can test whether differences in morphology can plausibly alter stress, strain, deformation, energy, or load transfer under specified loading conditions. It is particularly useful for irregular 3-D skeletal structures whose behavior is difficult to derive analytically. [FE-01, FE-03, FE-04, FE-17]
The literature provides weaker support for using fossil FEA to recover a unique historical force, stress state, failure threshold, or exact behavior when those quantities are not directly constrained. Those outputs depend on assumptions about materials, loads, constraints and model form. [FE-11, FE-15, FE-18]

### 2.3 Recurring methodological assumptions

| Assumption | What the literature says | Traceability |
|---|---|---|
| Geometry is an adequate reconstruction of the living anatomy | CT and digital restoration provide a solvable geometry, but segmentation, damage repair, smoothing, missing anatomy and surface resolution are additional assumptions. | [CT-03, CT-04, CT-08, FE-14, FE-15] |
| Materials can be represented by simplified constitutive laws | Linear elastic, isotropic or regionally homogeneous materials remain common even though fossil tissue properties are not directly known. | [FE-11, FE-18, BIO-06, BIO-07] |
| CT density can inform stiffness | Extant models sometimes map Hounsfield/density values to elastic modulus; in fossils, permineralization and beam hardening complicate this mapping. | [BIO-07, FE-08] |
| Loads can be represented as static forces | Impact questions are often approximated by steady-state/static loading; this is useful for a baseline but is not equivalent to a transient collision. | [BIO-07, BIO-06] |
| Constraints approximate the rest of the skeleton/body | Cranial BCs are necessary but uncertain; rigid condyle/neck constraints can create local artifacts. | [FE-06, FE-07, BIO-07] |
| Mesh refinement can resolve the model | Only a documented convergence study demonstrates numerical adequacy for the chosen outputs. | [FE-10, CT-09] |

### 2.4 Validation and sensitivity
Validation studies provide the strongest evidence about what FE outputs can mean. Bright & Rayfield's pig-cranium work compared model predictions with ex vivo strain data; other cranial studies examined simplification, loading, internal-bone representation, and material-property sensitivity. Across these studies, spatial patterns and comparative trends can be more stable than absolute local magnitudes, but that is not universal and depends on the output and model. [FE-05, FE-09, FE-11, FE-12, FE-15, FE-16]
Mesh convergence is a **verification** result, not validation. A numerically converged model can still be biologically wrong if geometry, materials, loads or constraints are wrong. Conversely, a biologically plausible model can be numerically under-resolved. [FE-10, UQ-04, UQ-07, CT-09]

### 2.5 Common failure modes

| Failure mode | Why it matters | Traceability |
|---|---|---|
| Overinterpreting absolute stress | Absolute magnitudes inherit uncertainty from E, ν, constitutive law, load magnitude/contact, BCs and geometry. | [FE-11, FE-15, FE-18] |
| Treating peak stress as a biological measurement | Local maxima can occur near point loads, rigid constraints, holes/canals and mesh singularities. | [BIO-07, FE-10] |
| Confounding geometry and discretization | Changing segmentation/smoothing/decimation while changing element density makes it impossible to attribute output changes uniquely to mesh resolution. | [FE-14, CT-08] |
| Using one mesh-size number as proof of convergence | Different regions and outputs can converge at different rates. | [FE-10] |
| Treating behavioral interpretation as equivalent to mechanical capability | A skull can be mechanically capable of an impact under a model without proving that the behavior occurred or was its evolutionary function. | [BIO-06, BIO-07, BIO-09] |
| Calling a model 'validated' because it is converged | Verification, validation and uncertainty quantification answer different questions. | [UQ-04, UQ-07, CT-09] |

### 2.6 Current methodological standards implied by the literature
A defensible fossil FEA paper should report geometry provenance and preprocessing; segmentation and repair decisions; material regions and constitutive assumptions; exact load application and BC definitions; element type and mesh-generation settings; mesh-quality diagnostics; output-specific convergence; verification checks; validation evidence or the absence of specimen-specific validation; sensitivity/UQ methods; and the interpretive limits of absolute outputs. [CT-09, FE-10, FE-11, FE-13, FE-15]

## 3. CT-derived fossil FEA: uncertainty along the full chain

| Transition | What changes | Scientific consequence | Sources |
|---|---|---|---|
| **CT acquisition** | Voxel size, artifacts, beam hardening, contrast, reconstruction filters and fossil/matrix properties determine what anatomy is observable. | Geometry and material evidence can already be biased before segmentation. | [BIO-07, CT-06, FE-20] |
| **Segmentation** | Thresholds, manual labels and AI predictions decide what is classified as bone, matrix, void, trabeculae and cortex. | Segmentation error changes volume, surfaces, interfaces and potentially stress pathways. | [CT-06, CT-07, FE-20] |
| **Digital repair** | Crack closure, hole filling, interpolation, mirroring and reconstruction insert anatomical assumptions. | Restored regions are epistemic/model-form uncertainty, not numerical noise. | [CT-03, CT-04] |
| **Surface processing** | Smoothing, decimation, remeshing and regularization alter the FE boundary geometry. | Surface resolution itself can affect FE output independently of volume-mesh density. | [CT-08, FE-14] |
| **Watertight geometry** | Non-manifold edges, self-intersections and invalid normals can prevent valid volume tetrahedralization. | Topology repair is prerequisite QA; it is not convergence. | [CT-05, CT-06, FE-20] |
| **Volume mesh** | Element size, quality, type/order and mesher settings determine the discrete approximation. | Discretization error should be isolated by holding the upstream model fixed while refining the FE mesh. | [FE-10, CT-01, CT-10] |
| **FEM/solver** | Material laws, loads, constraints and numerical tolerances determine the solved response. | A converged numerical solution is conditional on the chosen mathematical model. | [FE-11, BIO-07, UQ-07] |
| **Interpretation** | Stress, strain, energy and displacement are model outputs, not measurements of the fossil's historical loading state. | Interpretation must carry the uncertainty of all upstream decisions. | [FE-11, FE-15, BIO-07, UQ-05] |

### Mesh-convergence terminology for UALVP 2
The evidence supports the project's principle that **meshes used for convergence should be generated from the same fixed FE-ready geometry/modeling pipeline**. The point is causal identification: if geometry, segmentation, surface processing, materials, loads, BCs, element formulation and solver are held constant, output changes across a refinement ladder can be attributed primarily to discretization. By contrast, changing segmentation, smoothing, surface resolution, mesher or model form answers a different question and should be described as geometry-processing sensitivity, mesh-generation-method sensitivity, or model-form sensitivity. [FE-10, FE-14, CT-01, CT-08, CT-10]
A converged quantity must also be named. Energy, apex displacement and regional stress summaries can converge differently; a global scalar can appear stable while local maxima remain mesh-sensitive. The literature therefore supports output-specific convergence rather than a single universal 'converged mesh' label. [FE-10, CT-09, CT-10]

## 4. Pachycephalosaurs and *Stegoceras*

### 4.1 Why UALVP 2?
UALVP 2 is historically important and unusually complete for *Stegoceras*. The University of Alberta records its 1921 collection by George F. Sternberg and describes it as the most complete specimen to that point; Sullivan's taxonomic treatment describes it as a nearly complete skull with both lower jaws and parts of the postcranial skeleton and notes that the lectotype frontoparietal conforms readily to it. [BIO-12, BIO-03]
It is also the key specimen for the present computational question because Snively & Theodor directly used 'UA 2' (*UALVP 2*) in their CT-derived FE model, creating a rare opportunity to compare a new reproducible pipeline against a published specimen-specific benchmark rather than inventing a specimen from a generic skull. [BIO-07]

### 4.2 Anatomy, CT and histology
The dome is formed by major thickening of the cranial roof. UALVP 2's CT data show dense superficial and deep compact layers separated by lower-density/trabecular tissue, with trabeculae approximately perpendicular to the external dome surface; dense structures around neurovascular canals extend toward the outer surface. The 2011 authors explicitly noted that beam hardening could inflate superficial CT density and therefore did not treat every Hounsfield value as literal fossil-bone density. [BIO-07]
Histological work by Goodwin & Horner identified three dome zones and found that vascularity and radiating tissue structures changed substantially through ontogeny, with those structures diminishing in mature/adult domes. They interpreted this tissue history as inconsistent with treating the radiating trabecular architecture as a simple adult head-butting adaptation and instead favored display/species-recognition interpretations. That is an **author interpretation**, not a direct behavioral observation. [BIO-05]
Schott et al. used morphology, allometry, histology and high-resolution CT across a stratigraphically constrained *Stegoceras validum* sample. They found positive allometry of the dome and a transition from flat-headed juveniles to domed individuals; their growth series explicitly includes UALVP 2. Thus UALVP 2's geometry must be interpreted in ontogenetic context, even though the present evidence base does not provide a single independent age measurement that should be treated as a precise chronological age. [BIO-04]

### 4.3 Proposed functions and competing hypotheses

| Hypothesis | Supporting evidence | What prevents a stronger conclusion | Computational consequence |
|---|---|---|---|
| Impact/combat | Dome morphology, CT architecture, extant analogues, FE mechanical competence, and apex-clustered pathology have all been used as evidence. | FEA demonstrates modeled mechanical plausibility rather than observed behavior; pathology records trauma but not exact mechanism; analogues differ in contact geometry and behavior. | [BIO-06, BIO-07, BIO-08, BIO-09] |
| Sociosexual display / sexual selection | Dome development, cranial ornamentation and histological ontogeny have been interpreted as display structures. | A display function does not preclude incidental mechanical consequences or secondary agonistic behavior. | [BIO-05, BIO-09, BIO-11] |
| Species recognition / communication | Goodwin & Horner explicitly favored display/communication interpretations based on histology; later literature has continued to consider signaling. | Functional significance is evolutionary and behavioral, so FEM can test mechanics but cannot by itself establish signaling. | [BIO-05, BIO-09] |
| Feeding trade-off | A 2026 study proposes that dome development constrained jaw-adductor space/geometry and reduced feeding performance in modeled pachycephalosaurs. | This is a recent hypothesis and does not resolve impact behavior. | [BIO-11] |
| Protective / energy-dissipative role | Layered architecture and prior FE models support load spreading/dissipation under selected impact conditions. | Mechanical energy dissipation is not equivalent to proof of evolutionary function. | [BIO-06, BIO-07] |

### 4.4 Extant analogues
Snively & Theodor compared *Stegoceras* with several artiodactyls, especially the head-striking duiker (*Cephalophus leucogaster*), musk ox (*Ovibos moschatus*) and bighorn sheep (*Ovis canadensis*), while also including taxa with substantially different cranial architectures such as giraffe, pronghorn and llama. The 2026 review stresses that 'headbutting' is behaviorally heterogeneous among extant taxa: sheep, warthogs and bison can all engage in cranial combat but use different striking surfaces and mechanics. Therefore no single extant analogue should be treated as the unique behavioral template for UALVP 2. [BIO-07, BIO-09]

## 5. Prior *Stegoceras*/UALVP 2 biomechanical models

### 5.1 Snively & Cox 2008
**Geometry/model:** lateral photographs were traced into 2-D profiles; a 2-D sagittal model of *Homalocephale* and a revolved 3-D model of *Pachycephalosaurus* were constructed in COMSOL. A separate subadult pachycephalosaurine model was based on a histological section and included three material zones plus variable keratin thickness. [BIO-06]

**Materials:** compact bone was assigned approximately E=20 GPa, ν=0.4, density 2000 kg/m³; the modeled cancellous zone used E=8 GPa and half the compact density; keratin scenarios used E=2.5 GPa, density 1300 kg/m³, ν=0.4. These are **model inputs**, not fossil-specific measurements. [BIO-06]

**Loads/BCs:** impact forces were calculated from animal mass, closing speed and assumed deceleration distance. Closing speeds of 3 and 6.7 m/s were explored, with point and distributed/edge load scenarios; the ventral/base surfaces were constrained in the dorsal-region models. [BIO-06]

**Mesh/verification:** meshes were varied in COMSOL; the paper reports approximately 20,736 elements for *Homalocephale* and 13,732 for the *Pachycephalosaurus* dome, with solutions at sampled node positions converging at about 5,000 elements or more in the tested models. This is useful historical convergence evidence, but it is not UALVP 2 and does not provide a modern multi-output convergence framework for a CT-derived specimen. [BIO-06]

**Outputs/conclusion:** stresses, strains, impact-force effects and safety-factor-style comparisons were evaluated. The authors concluded that the modeled domes could withstand substantial impacts under much of the tested range, while high-speed/short-deceleration cases could be more problematic for some geometries. This establishes **model-based mechanical capability**, not behavioral occurrence. [BIO-06]

### 5.2 Snively & Theodor 2011 — the critical UALVP 2 benchmark
**Specimen/geometry:** the model used *Stegoceras validum* UA 2 (= UALVP 2) and a high-resolution Austin CT dataset. The paper states that the Austin scan had twice the transverse resolution and 4.5× the anteroposterior resolution of the original medical scan. The primary Stegoceras model was a 2.2-million-element tetrahedral mesh generated in Avizo; a separate ~200,000-hexahedra approach was also produced from density masks/hollowed CT data for Stegoceras and Ovibos. [BIO-07]

**Segmentation/surface processing:** density-based masks were created in Mimics; matrix had to be removed manually from the cranial sinuses and endocranial cavity for Stegoceras; STL surfaces were remeshed/error-corrected using Mimics and Geomagic before FE meshing. [BIO-07]

**Materials:** for Stegoceras, CT density-to-stiffness mapping could not be fully automated because permineralization was unknown. The authors manually assigned properties, treated values above 2500 HU as influenced by beam hardening, and assigned the cancellous dome a conservative E=1 GPa. Keratin properties were assigned explicitly in the musk ox model (E=3.9 GPa, ν=0.28, ρ=1300 kg/m³); the Stegoceras model tested several keratin-pad geometries because the living covering was unknown. [BIO-07]

**Loads:** the baseline Stegoceras force was 1360 N, derived from a similarly sized *Homalocephale* at 3 m/s closing speed. Separate analyses applied the load over different areas of the Stegoceras dome because the size/spread of an unknown keratin pad was uncertain. [BIO-07]

**Constraints:** occipital condyles were constrained against translation and rotation, and additional constraints were placed along the nuchal crest to represent neck-muscle restraint; the authors explicitly reported artificial high stresses at some constraints. [BIO-07]

**Outputs:** von Mises stress, strain/safety factors, energy distribution and comparative morphology/behavior correlations were used. For the 1360 N baseline, modeled cancellous-dome stresses were around 1 MPa and compact bone around the braincase peaked around 5 MPa in their selected representation; concentrated versus distributed loading changed local maxima substantially, and artifacts occurred near constraints and neurovascular-canals. [BIO-07]

**Interpretation:** Snively & Theodor concluded that the anatomical, biomechanical and statistical pattern in their comparative dataset was consistent with head-strike capability and that *Stegoceras* fit extant head-striking taxa. Their conclusion is explicitly an inference from anatomy/biomechanics/statistical correlation, not an observation of behavior. [BIO-07]

### 5.3 Prior-model comparison

| Study | Geometry | Materials | Loads | Constraints | Mesh/solver | Main outputs | Validation / sensitivity | What it establishes | Key limitation |
|---|---|---|---|---|---|---|---|---|---|
| Snively & Cox 2008 | 2-D/3-D idealized pachycephalosaur dome models; photos/histology-derived | compact/cancellous bone + variable keratin; explicit E/ν assumptions | 3 and 6.7 m/s closing-speed-derived forces; point/distributed/edge loads | ventral/base constraints in dorsal models | COMSOL; variable mesh; historical convergence check | stress, strain, safety factors, load dissipation | mesh-resolution checks + scenario sensitivity | mechanical plausibility of selected dome geometries under selected impacts | not UALVP 2; idealized geometry; behavior/load history assumed |
| Snively & Theodor 2011 | CT-derived UALVP 2; high-res Austin CT; primary 2.2M tetra model; comparative artiodactyl CT models | CT-informed, manually adjusted fossil stiffness; E=1 GPa for Stegoceras cancellous region; keratin scenarios in comparative models | baseline 1360 N; multiple dome load patches | occipital-condyle + nuchal-crest/neck-muscle constraints | Avizo/Mimics/Geomagic/Strand7; 2.2M tet primary model and ~200k voxel-hex comparison | von Mises stress, strain/safety factors, energy, pattern correlations | comparative validation by extant analogues; keratin/load-area sensitivity; no direct specimen-level physical validation | UALVP 2 can distribute the selected simulated load and shares several modeled correlates with extant head-strikers | load magnitude/direction, CT-density mapping, BCs, behavior analogues and keratin are assumed; local stress artifacts acknowledged |

### 5.4 What a modern UALVP 2 reproduction should and should not claim
Reproducing the 2011 baseline is scientifically useful as a **benchmark/reproducibility exercise**, but it would not by itself answer whether that model is the unique or biologically correct UALVP 2 model. The published paper itself identifies uncertainty in keratin-pad geometry, fossil CT density, constraint artifacts and force scaling. A modern implementation can therefore add value by making the computational provenance explicit, verifying the implementation, demonstrating output-specific mesh convergence, and then exploring the major unresolved assumptions separately. [BIO-07, FE-10, CT-09]

## 6. Uncertainty and UQ

### 6.0 Fossil-specific sensitivity precedent

The fossil-specific literature identified in the UQ dossier is dominated by **scenario and local sensitivity analysis rather than fully probabilistic UQ**, and those studies are directly relevant to how UALVP 2 should be parameterized. Snively & Theodor (2011) varied load-spread/keratin-pad scenarios; Cox et al. (2015) varied muscle-force magnitude and orientation and found that different quantities of interest responded differently; Taylor et al. (2017) found bite position to be especially influential among the tested variables in *Psittacosaurus*; and Jannel et al. (2022) used explicit branches for material, soft-tissue, loading and boundary-condition assumptions. Together, these studies support treating **load/contact geometry and model-form branches as first-class uncertainty sources**, rather than assuming Young's modulus is the only meaningful uncertain parameter. [BIO-07, UQ-14, UQ-15, UQ-16]

Adjacent biomechanics provides the methodological bridge to full UQ: Berthaume et al. (2012) demonstrate probabilistic craniofacial FE with LHS; Kerr et al. (2011) use a Gaussian-process-assisted Bayesian sensitivity analysis; Biehler et al. (2015) use a multi-fidelity strategy for expensive nonlinear FE; Römer et al. (2022) combine surrogate modeling, Bayesian calibration and Sobol sensitivity; and Kote et al. (2026) combine probabilistic FE with geometry/material variability and a response-surface model. [UQ-09, UQ-11, UQ-12, UQ-13, UQ-17]

### 6.1 Recommended uncertainty taxonomy for UALVP 2

| Uncertainty source | UALVP 2 example | Preferred representation | Outputs most affected | Source |
|---|---|---|---|---|
| Numerical uncertainty | Tet discretization, element quality, solver tolerance, element formulation | Convergence/refinement, not a biological probability distribution | Energy; apex displacement; regional stress | [FE-10, CT-10, UQ-04] |
| Geometry/data uncertainty | Segmentation, matrix removal, surface smoothing/repair, ambiguous internal regions | Plausible geometry scenarios/ensembles or bounded perturbations | Volume; displacement; energy; stress field | [FE-08, FE-14, CT-06, CT-07, FE-20] |
| Material uncertainty | E, ν, spatial heterogeneity, CT-to-stiffness mapping | Bounds/distributions only when evidence supports them; otherwise discrete material scenarios | Stress/strain; energy; displacement | [FE-08, FE-11, FE-18, BIO-07] |
| Load uncertainty | force magnitude, direction, contact patch, load spreading | Continuous RVs when a defensible distribution exists; otherwise discrete load scenarios | Stress; displacement; energy | [FE-07, FE-12, FE-18, BIO-07] |
| Boundary-condition uncertainty | occipital/neck support, constrained regions, coupling to the rest of body | Discrete plausible BC models; local artifact diagnostics | Displacement; regional stress; energy | [FE-06, FE-11, BIO-07] |
| Model-form uncertainty | linear/static vs nonlinear/contact/dynamic; homogeneous vs zonated/anisotropic materials | Discrete model ensemble; do not automatically smear into one parameter RV | All QoIs, especially impact-local fields | [UQ-07, FE-19, BIO-07] |
| Biological variability | ontogenetic stage or population/behavioral variability, if the question is population-level | Distribution only when the scientific target genuinely includes population variability | All outputs, potentially including geometry | [BIO-04, BIO-10] |

### 6.2 Which methods fit which questions?

| Method | Appropriate when | Computational burden | UALVP 2 question | Main caution | Source |
|---|---|---|---|---|---|
| OAT/local sensitivity | Small, interpretable input set; baseline debugging and directional effects | Low | Does this output move materially if E, force magnitude, angle, or ν is perturbed? | Misses interactions; baseline-dependent | [UQ-04] |
| Morris | Many candidate inputs; need screening for nonlinear/interactive importance | Low–moderate | Which variables should survive into expensive UQ? | Not a full variance decomposition | [UQ-02, UQ-10] |
| LHS | Need a space-filling ensemble with expensive FE solves | Moderate | What output distributions arise across plausible inputs? | Requires defensible input ranges/distributions | [UQ-01, UQ-09, FE-13] |
| Monte Carlo | Direct propagation once input distributions are specified | Moderate–high; sample-size dependent | What is the propagated distribution of a QoI? | Can be expensive without a surrogate | [UQ-01, UQ-05] |
| Sobol/global variance sensitivity | Need quantitative main/total effects and interactions | High without surrogate | Which uncertainty sources explain output variance? | Requires many model evaluations and stable estimators | [UQ-03, FE-13, FE-21] |
| Surrogate / GP / PCE | Forward FE is the computational bottleneck | Up-front training cost; low marginal cost later | How can large propagation/global sensitivity be made tractable? | Surrogate error must be separately validated | [UQ-06, UQ-08, FE-21] |
| Bayesian calibration | Informative observational data exist and calibration/model discrepancy are scientifically meaningful | High conceptual/implementation cost | What parameter/posterior model is compatible with data, with discrepancy modeled? | Not justified by a single fossil FE model lacking informative validation data | [UQ-06, UQ-07] |
| Active learning | Surrogate or sampling uncertainty concentrates in important regions | Adaptive cost | Where should the next expensive FE runs go? | Only useful once an adaptive surrogate/sampling problem is demonstrated | [FE-21] |

### 6.3 Evaluation of the proposed UQ roadmap
The originally proposed roadmap — deterministic verification → mesh convergence → local sensitivity → global sensitivity → Monte Carlo/LHS → surrogate modeling → Sobol/Morris → active learning — is directionally sound but should be **reordered into a decision tree** rather than a mandatory staircase.
Recommended order: **(0)** deterministic verification; **(1)** output-specific mesh convergence; **(2)** uncertainty inventory and representation decisions; **(3)** local OAT; **(4)** Morris only if the input count warrants screening; **(5)** LHS/space-filling FE ensemble for propagation; **(6)** direct MC-style propagation or a validated surrogate if the forward model is expensive; **(7)** Sobol/global sensitivity when interactions/variance attribution are actually needed; **(8)** active learning only if surrogate cost/error demonstrates value. Bayesian calibration should be a separate branch activated only by informative validation/calibration data. [UQ-02–UQ-08, FE-21]
A particularly useful recent benchmark is Baugnon et al. (2026), which used 24 mandibular FE inputs, 2,400 simulations, LHS, sparse polynomial chaos and Sobol analysis, and showed that contact-sensitive regions required larger sample sizes for stable sensitivity estimates than global metrics. That supports treating sensitivity-index convergence as a result that itself needs verification. [FE-21]

## 7. Evidence-to-model mapping

| Literature evidence | Model decision | Confidence | What remains uncertain | UQ implication |
|---|---|---|---|---|
| UALVP 2 was directly modeled in the 2011 CT/FE study. [BIO-07] | Use UALVP 2 as the specimen-specific benchmark and preserve the published provenance. | High | Current project CT dataset may differ in acquisition/processing from the published scan. | Benchmark the published model, but treat input reproduction as a separate provenance question. |
| UALVP 2 shows layered compact/trabecular architecture. [BIO-07] | Use heterogeneous/zonated material representation where the current CT and evidence support it. | High for architecture; lower for mechanics | Fossil-specific E/ν and CT-to-stiffness mapping are not directly known. | Material zonation and E/ν become sensitivity/UQ variables/scenarios. |
| Schott et al. show strong ontogenetic changes in dome morphology and include UALVP 2 in the growth series. [BIO-04] | Do not silently generalize UALVP 2 mechanics to all growth stages. | High | Exact ontogenetic stage and biological age are not equivalent concepts. | Ontogenetic variability is separate from uncertainty about a single specimen. |
| Goodwin & Horner find vascular/radiating tissues are transient through growth. [BIO-05] | Do not interpret current adult CT trabeculae as a simple direct 'impact adaptation' without qualification. | High as histological observation | Functional meaning of vascular architecture remains contested. | Treat tissue architecture as empirical geometry/material evidence, not behavioral proof. |
| Snively & Theodor used 1360 N as a UALVP 2 baseline force. [BIO-07] | Use 1360 N as a literature benchmark load case, not a unique biological truth. | High | Actual impact force, impulse, contact duration and direction. | Force magnitude/direction/contact should be separate uncertainty/scenario variables. |
| 2011 model used occipital and nuchal constraints and reported constraint artifacts. [BIO-07] | Retain explicit BC definitions and diagnose local stresses near constrained interfaces. | High | Real head-neck support and muscle recruitment. | BC alternatives should be discrete model-form scenarios. |
| Bright & Rayfield show mesh density changes cranial displacement/strain and hotspot resolution. [FE-10] | Perform controlled same-geometry mesh refinement before interpreting Phase 4 outputs. | High | Exact convergence rate of the UALVP 2 geometry. | Numerical uncertainty quantified separately from biological uncertainty. |
| McCurry et al. show surface-resolution sensitivity. [CT-08] | Freeze surface-processing pipeline during mesh convergence. | High | How much current smoothing/decimation affects the UALVP 2 results. | Geometry-processing sensitivity should be a separate experiment. |
| 2025 dinosaur segmentation+FEA study shows matrix handling can change stress field. [FE-20] | Document matrix/trabecular treatment and test plausible alternatives where biologically justified. | High for precedent | Effect size for UALVP 2 depends on its internal anatomy and scan quality. | Segmentation/matrix treatment is a geometry/model-form uncertainty layer. |
| Validation literature shows broad patterns can be more stable than absolute magnitudes. [FE-11, FE-15] | Prioritize comparative/spatially robust outputs and avoid unsupported absolute thresholds. | High as a general caution | Which UALVP 2 local regions are genuinely robust. | Report sensitivity envelope and spatially defined regional outputs. |
| 2026 mandibular UQ demonstrates LHS/PCE/Sobol at 24 inputs and 2400 runs. [FE-21] | Adopt global UQ only if the UALVP 2 parameter count/cost makes it useful. | Moderate–high transferability; extant mandible | Whether UALVP 2 needs that sample count or surrogate architecture. | Estimate convergence of sampling/sensitivity statistics before claiming stable rankings. |
| 2026 headbutting review stresses behavioral heterogeneity among extant analogues. [BIO-09] | Do not encode 'headbutting' as one load case. | High for conceptual caution | Which contact geometry, direction and event type are biologically plausible for *Stegoceras*. | Represent load case as a scenario family, not a single behavioral truth. |

## 8. Scientific gap analysis

### Established

| Claim | Evidence |
|---|---|
| UALVP 2 is a key, unusually complete *Stegoceras* specimen with established taxonomic history and documented CT/FEA use. | [BIO-03, BIO-07, BIO-12] |
| Its cranial dome has heterogeneous internal architecture visible in CT, including compact and trabecular regions and neurovascular structures. | [BIO-07] |
| *Stegoceras* dome morphology changes strongly through ontogeny and UALVP 2 appears in a quantitative growth series. | [BIO-04] |
| Fossil FEA is established as a useful tool for comparative structural/form-function questions. | [FE-01, FE-04] |
| Mesh density, geometry, loading, BCs and materials can materially alter biomechanical FE outputs. | [FE-06–FE-15, FE-18] |
| Mesh convergence is a verification task distinct from physical validation. | [FE-10, UQ-04, UQ-07] |
| Segmentation and surface geometry are part of the numerical/biological model chain, not neutral preprocessing. | [CT-06, CT-08, FE-20] |

### Reasonably supported

| Claim | Evidence / caveat |
|---|---|
| Under specified static loading, the UALVP 2 dome can distribute/dissipate load without reaching the failure criteria used in the 2011 model. | [BIO-07] |
| Comparative FEA can distinguish mechanical behavior among cranial geometries even when absolute tissue properties are uncertain. | [FE-11, FE-15] |
| The 2011 UALVP 2 model's layered architecture and chosen load case provide a reproducible benchmark for modern reanalysis. | [BIO-07] |
| A staged sensitivity/UQ workflow is scientifically better matched to fossil constraints than immediate full Bayesian calibration. | [UQ-04–UQ-08, FE-21] |

### Contested

| Issue | Evidence landscape |
|---|---|
| Whether pachycephalosaurs actually engaged in head-to-head combat using the dome. | Snively/Cox and Snively/Theodor interpret mechanical capability and comparative morphology as consistent with head-strike behavior; Goodwin/Horner interpret developmental histology as inconsistent with head-butting as the primary function; Peterson et al. interpret apex-clustered pathology as evidence consistent with agonistic butting; Woodruff/Ackermans emphasize that 'headbutting' bundles different behaviors and analogues. [BIO-05–BIO-09] |
| Whether the dome's primary evolutionary function was combat, display/communication, or a combination. | Multiple functions are compatible with the available evidence; the literature does not reduce the question to mechanical competence alone. [BIO-05, BIO-08, BIO-09, BIO-11] |
| How much confidence should be placed in absolute local stress/strain values from cranial FEA. | Validation studies show useful pattern-level agreement but magnitude discrepancies; local values may additionally be affected by singularities, constraints and geometry. [FE-10, FE-11, FE-15, BIO-07] |
| Which uncertain input is most important. | Sensitivity is output- and model-dependent; recent UQ studies demonstrate that dominant factors differ by QoI and region. [FE-08, FE-18, FE-21] |

### Unknown

| Unknown | Why it remains unknown |
|---|---|
| The exact force magnitude, impulse duration, rate and direction that a living UALVP 2-equivalent *Stegoceras* would have experienced in a real cranial collision. | No direct behavioral measurement exists; prior FE forces are modeled scenarios. |
| The living thickness, geometry and material properties of any keratinous covering over the dome. | Prior models tested hypothetical keratin pads; the living soft tissue is not directly preserved. |
| The exact constitutive properties of UALVP 2 fossilized bone and how CT HU should map to living mechanical properties. | The 2011 study explicitly identified permineralization and beam-hardening problems. |
| The biologically correct head/neck boundary conditions during any impact event. | Existing models use necessary but simplified constraints. |
| Whether the current UALVP 2 CT dataset captures all internal architecture needed for a mechanically faithful model. | Depends on scan quality, segmentation, matrix, reconstruction and unresolved regions. |
| Whether a static linear solution is adequate for the specific scientific question beyond a baseline structural comparison. | The 2011 authors themselves identified transient analyses as a future direction. |

## 9. Contribution opportunities
These are deliberately phrased as contribution opportunities, not novelty claims.

| Status | Candidate contribution | Verification needed |
|---|---|---|
| Established in literature | Specimen-specific CT/FEM analysis of UALVP 2 under a published impact benchmark. | [BIO-07] |
| Candidate contribution | A fully reproducible UALVP 2 geometry-to-TetGen-to-FEM pipeline with machine-readable provenance, explicit verification, and frozen inputs across mesh tiers. | Requires verification against the existing project and exhaustive comparison with published workflows. |
| Candidate contribution | A same-geometry, same-model multi-tier mesh-convergence study using multiple scientific outputs rather than element count alone. | Requires confirmation that an equivalent multi-output UALVP 2 study has not already been published. |
| Candidate contribution | Explicit separation of numerical, geometry/segmentation, material, loading/BC and model-form uncertainty in a fossil cranial FE workflow. | Requires exhaustive fossil-specific citation chasing before any novelty claim. |
| Appears uncommon | A specimen-specific UALVP 2 uncertainty workflow that moves from deterministic verification to local/global sensitivity while keeping discrete model-form alternatives separate from scalar parameter distributions. | Requires further verification. |
| Candidate contribution | A load-case family for UALVP 2 that treats magnitude, direction and contact area/spread as explicit scenarios rather than collapsing them into one 'headbutting' load. | Requires comparison with the full prior pachycephalosaur modeling literature. |
| Candidate contribution | A validated surrogate/global-sensitivity workflow only if the direct FE ensemble proves computationally expensive. | Conditional; not needed a priori. |

## 10. Implications for project phases

| Project area | Literature-derived implication |
|---|---|
| **Phase 4 deterministic FEM** | Use the literature benchmark, but do not treat the 2011 1360 N load or its BCs as uniquely correct. Make every model input explicit and reproducible. Use linear static FEM as a baseline verification model, not as a full reconstruction of transient impact mechanics. [BIO-07, FE-19] |
| **Mesh convergence** | Freeze the FE-ready geometry/modeling pipeline. Build a 4–6 tier refinement ladder if computationally feasible, keeping geometry, material map, loads, BCs, element formulation and solver settings fixed. Monitor energy, apex displacement and predefined regional stress metrics separately. [FE-10, CT-09, CT-10] |
| **Geometry/provenance** | Retain raw/source, cleaned, and FE-ready geometry as separate versioned states. Record segmentation method, matrix treatment, repairs, smoothing, watertightness checks and surface resolution. [CT-03–CT-06, CT-09] |
| **Force/loading assumptions** | Use the 1360 N literature case as a benchmark. Add a small, biologically explicit family of force magnitudes, directions and contact areas instead of calling one case 'the headbutt'. [BIO-07, BIO-09] |
| **Material assumptions** | Document E and ν explicitly, distinguish CT-informed zonation from experimentally measured fossil properties, and later vary E/ν/zonation separately. [BIO-07, FE-08, FE-11, FE-18] |
| **Later UQ** | Start with OAT; use Morris if the input set becomes large; use LHS for propagation; use Sobol/global sensitivity when interaction attribution is scientifically needed; use surrogates only when computational cost warrants them. [UQ-01–UQ-03, FE-13, FE-21] |
| **Interpretation of outputs** | Treat energy/displacement/regional stress as model outputs. Do not convert a single peak stress into a behavioral verdict. Separate 'mechanically withstands this modeled load' from 'the animal engaged in this behavior' and from 'the dome evolved for this function'. [BIO-07–BIO-11, FE-11, FE-15] |

## 11. Recommended next experiments/analyses

| Experiment/analysis | Purpose | Priority |
|---|---|---|
| **1. Benchmark reproduction** | Reproduce the published UALVP 2 baseline as closely as current data permit: geometry provenance, internal zoning, 1360 N load, constraints and major outputs. Treat any mismatch as a provenance/model-difference diagnostic, not as a failure of the new model. | Highest priority |
| **2. Deterministic verification** | Run analytical and implementation tests before interpreting the fossil model. Record reaction-force balance, solver residuals and known-solution checks. | Highest priority |
| **3. Controlled mesh ladder** | Generate same-geometry/model meshes over several refinement tiers. Plot convergence for elastic/strain energy, apex displacement and regional stress statistics. Record quality distributions. | Highest priority |
| **4. Constraint artifact map** | Create a spatial mask/annotation of constrained regions and load application zones. Quantify how outputs change when only local artifact-prone regions are excluded from summaries. | High |
| **5. Load-direction/contact experiment** | Keep the baseline force magnitude fixed initially and vary direction and contact patch/spread. This separates geometric/load orientation effects before adding broad probabilistic UQ. | High |
| **6. Material sensitivity** | Vary E and ν over defensible ranges, and compare homogeneous versus evidence-based zonation. Track which QoIs change appreciably. | High |
| **7. Segmentation/model-form audit** | Construct at least a small set of plausible segmentation/repair variants in the most ambiguous internal regions. Compare geometry-derived metrics before solving and FE outputs afterward. | High |
| **8. Local-to-global sensitivity bridge** | Use OAT first. If more than roughly a handful of influential continuous variables remain, use Morris to screen and then LHS/Sobol on the reduced set. | Medium–high |
| **9. Surrogate only if needed** | Measure actual forward-solve cost. If thousands of runs are impractical, train and validate a GP/PCE/other surrogate with held-out FE runs before using it for global sensitivity. | Conditional |
| **10. Dynamic/nonlinear branch** | Only after the baseline question is answered and a specific biological question demands it. A transient impact analysis should be framed as a new model-form study, not as a routine upgrade to linear static FEM. | Future |

## 12. What the literature says vs what this project may contribute

### The literature says
- CT-derived FEA can meaningfully test comparative cranial mechanics, but the model's conclusions are conditional on geometry, material, loads, BCs and numerical resolution. [FE-01–FE-04, FE-11]
- UALVP 2 has been directly modeled with CT-based FEA, including a 1360 N benchmark and explicit recognition of fossil-density, keratin, loading-area and constraint uncertainty. [BIO-07]
- *Stegoceras* dome morphology is ontogenetically dynamic and histology/CT provide evidence about changing internal architecture. [BIO-04, BIO-05, BIO-07]
- The behavioral meaning of a mechanically competent dome remains an inference and is contested across the literature. [BIO-05, BIO-08, BIO-09, BIO-11]
- Mesh density, surface geometry, segmentation, materials and loading can all materially alter FE outputs. [FE-10, FE-14, FE-15, FE-18, FE-20]
- Modern computational biomechanics supports staged sensitivity/UQ rather than requiring maximal algorithmic sophistication from the outset. [UQ-01–UQ-08, FE-21]

### This project may contribute
- a reproducible, specimen-specific UALVP 2 computational chain whose numerical and biological assumptions are separately auditable;
- a controlled same-geometry mesh-convergence study that isolates discretization uncertainty;
- explicit sensitivity of load direction/contact, material assumptions and geometry-processing choices;
- a later UQ framework that distinguishes scalar parameter uncertainty from discrete geometry/BC/model-form alternatives;
- and a clearer statement of which conclusions are robust across the tested uncertainty envelope versus scenario-dependent.

These should remain **candidate contributions** until the citation chase is extended sufficiently to rule out close prior examples.

## 13. Traceability and reference key

Every major claim in this synthesis points to one or more source IDs. The source key below is the canonical mapping for this document. `UNVERIFIED` metadata are intentionally retained rather than filled from secondary memory.

| ID | Citation | Identifier / stable URL |
|---|---|---|
| **FE-01** | Rayfield et al. 2001. *Cranial design and function in a large theropod dinosaur*. Nature 409:1033–1037. | [10.1038/35059070](https://doi.org/10.1038/35059070) |
| **FE-02** | Rayfield 2005. *Using finite-element analysis to investigate suture morphology: a case study using large carnivorous dinosaurs*. The Anatomical Record 283A:349–365. | [10.1002/ar.a.20168](https://doi.org/10.1002/ar.a.20168) |
| **FE-03** | Rayfield 2005. *Aspects of comparative cranial mechanics in the theropod dinosaurs Coelophysis, Allosaurus and Tyrannosaurus*. Zoological Journal of the Linnean Society 144:309–316. | [10.1111/j.1096-3642.2005.00176.x](https://doi.org/10.1111/j.1096-3642.2005.00176.x) |
| **FE-04** | Ross 2005. *Finite element analysis in vertebrate biomechanics*. The Anatomical Record 283A:253–258. | [10.1002/ar.a.20177](https://doi.org/10.1002/ar.a.20177) |
| **FE-05** | Kupczik et al. 2007. *Assessing mechanical function of the zygomatic region in macaques with finite element analysis*. The Anatomical Record. | [10.1002/ar.20510](https://doi.org/10.1002/ar.20510) |
| **FE-06** | Marinescu et al. 2005. *Boundary condition sensitivity in finite element models of cranial biomechanics*. The Anatomical Record. | `UNVERIFIED exact DOI in current synthesis` |
| **FE-07** | Ross et al. 2005. *Effects of masticatory loadings and boundary conditions on deformation in primate crania*. The Anatomical Record. | `UNVERIFIED exact DOI in current synthesis` |
| **FE-08** | Taddei et al. 2006. *Finite-element modeling of bones from CT data: sensitivity to geometry and material uncertainties*. IEEE Transactions on Biomedical Engineering 53:2194–2200. | [10.1109/TBME.2006.879473](https://doi.org/10.1109/TBME.2006.879473) |
| **FE-09** | Panagiotopoulou et al. 2010. *Modelling subcortical bone in finite element models of the mandible*. Journal of Biomechanics. | `UNVERIFIED exact DOI in current synthesis` |
| **FE-10** | Bright & Rayfield 2011. *The response of cranial biomechanical finite element models to variations in mesh density*. The Anatomical Record 294:610–620. | [10.1002/ar.21358](https://doi.org/10.1002/ar.21358) |
| **FE-11** | Bright & Rayfield 2011. *Sensitivity and ex vivo validation of finite element models of the domestic pig cranium*. Journal of Anatomy 219:456–471. | [10.1111/j.1469-7580.2011.01408.x](https://doi.org/10.1111/j.1469-7580.2011.01408.x) |
| **FE-12** | Fitton et al. 2012. *The influence of loading conditions on finite element models of the macaque cranium*. The Anatomical Record. | `UNVERIFIED exact DOI in current synthesis` |
| **FE-13** | Berthaume et al. 2012. *Probabilistic finite element analysis of a craniofacial finite element model*. Journal of Theoretical Biology 300:242–253. | [10.1016/j.jtbi.2012.01.031](https://doi.org/10.1016/j.jtbi.2012.01.031) |
| **FE-14** | McCurry, Evans & McHenry 2015. *The sensitivity of biological finite element models to the resolution of surface geometry: a case study of crocodilian crania*. PeerJ 3:e988. | [10.7717/peerj.988](https://doi.org/10.7717/peerj.988) |
| **FE-15** | Godinho et al. 2017. *Finite element modelling of the cranium: sensitivity to segmentation and material properties / validation*. Comptes Rendus Palevol. | [10.1016/j.crpv.2016.11.002](https://doi.org/10.1016/j.crpv.2016.11.002) |
| **FE-16** | Cuff et al. 2015. *Complete avian-cranium finite element modelling and validation*. The Anatomical Record. | `UNVERIFIED exact DOI in current synthesis` |
| **FE-17** | Dumont et al. 2009. *Comparing finite element models of biological structures*. Journal of Experimental Biology / related comparative methods record. | `UNVERIFIED exact DOI in current synthesis` |
| **FE-18** | Sylvester & Kramer 2018. *Young's Modulus and Load Complexity: Modeling Their Effects on Proximal Femur Strain*. The Anatomical Record 301:1189–1202. | [10.1002/ar.23796](https://doi.org/10.1002/ar.23796) |
| **FE-19** | Marcé-Nogué 2022. *Nonlinear finite element analysis in palaeontology/anthropology: review*. Review source in FE module. | `UNVERIFIED exact DOI in current synthesis` |
| **FE-20** | Zhang, Cao & Zhao 2025. *Deep learning-aided segmentation combined with finite element analysis reveals a more natural biomechanic of dinosaur fossil*. Scientific Reports 15:13964. | [10.1038/s41598-025-99131-4](https://doi.org/10.1038/s41598-025-99131-4) |
| **FE-21** | Baugnon et al. 2026. *Uncertainty quantification and global sensitivity analysis of a patient-specific mandibular finite element model using Latin hypercube sampling and sparse polynomial chaos expansion*. Medical Engineering & Physics 147:085011 / article. | [10.1088/1873-4030/ae995b](https://doi.org/10.1088/1873-4030/ae995b) |
| **BIO-01** | Gilmore 1924. *On a new species of Stegoceras, a genus of dome-headed dinosaurs from the Cretaceous of Alberta*. University / museum publication record. | `UNVERIFIED exact identifier` |
| **BIO-02** | Sues & Galton 1987. *Anatomy and taxonomy of Stegoceras and related pachycephalosaurs*. peer-reviewed taxonomic study. | `UNVERIFIED exact identifier` |
| **BIO-03** | Sullivan 2006. *A taxonomic review / revision of the Pachycephalosaurs; treatment of Stegoceras*. New Mexico Museum / taxonomy monograph. | `UNVERIFIED exact DOI; source copy located` |
| **BIO-04** | Schott et al. 2011. *Cranial Ontogeny in Stegoceras validum: A Quantitative Model of Pachycephalosaur Dome Growth and Variation*. PLOS ONE 6:e21092. | [10.1371/journal.pone.0021092](https://doi.org/10.1371/journal.pone.0021092) |
| **BIO-05** | Goodwin & Horner 2004. *Cranial histology of pachycephalosaurs reveals transitory structures inconsistent with head-butting behavior*. Paleobiology 30:253–267. | [10.1666/0094-8373(2004)030<0253:CHOPOM>2.0.CO;2](https://doi.org/10.1666/0094-8373(2004)030<0253:CHOPOM>2.0.CO;2) |
| **BIO-06** | Snively & Cox 2008. *Structural Mechanics of Pachycephalosaur Crania Permitted Head-Butting Behavior*. Palaeontologia Electronica 11(1):3A. | [UNVERIFIED DOI / stable article page](http://palaeo-electronica.org/2008_1/140/index.html) |
| **BIO-07** | Snively & Theodor 2011. *Common Functional Correlates of Head-Strike Behavior in the Pachycephalosaur Stegoceras validum and Combative Artiodactyls*. PLOS ONE 6:e21422. | [10.1371/journal.pone.0021422](https://doi.org/10.1371/journal.pone.0021422) |
| **BIO-08** | Peterson, Dischler & Longrich 2013. *Distributions of Cranial Pathologies Provide Evidence for Head-Butting in Dome-Headed Dinosaurs*. PLOS ONE 8:e68620. | [10.1371/journal.pone.0068620](https://doi.org/10.1371/journal.pone.0068620) |
| **BIO-09** | Woodruff & Ackermans 2024 (issue 2026). *Headbutting through time: A review of this hypothesized behavior in “dome-headed” fossil taxa*. The Anatomical Record 309:1235–1256. | [10.1002/ar.25526](https://doi.org/10.1002/ar.25526) |
| **BIO-10** | Moore et al. 2022. *The appendicular myology of Stegoceras validum and implications for the head-butting hypothesis*. PLOS ONE. | [10.1371/journal.pone.0268144](https://doi.org/10.1371/journal.pone.0268144) |
| **BIO-11** | Bateman & Larsson 2026. *On Pachycephalosaurs, Trade-Offs, and the Historical Genesis of Sociosexual Display Structures*. The American Naturalist 208:9–29. | [10.1086/740811](https://doi.org/10.1086/740811) |
| **BIO-12** | University of Alberta Dino Lab. *History of Paleontology at the U of A — UALVP 2*. Institutional provenance record. | [UNVERIFIED bibliographic identifier](https://grad.biology.ualberta.ca/dino-lab/history/) |
| **UQ-01** | McKay, Beckman & Conover 1979. *Comparison of three methods for selecting values of input variables in the analysis of output from a computer code*. Technometrics. | [10.1080/00401706.1979.10489755](https://doi.org/10.1080/00401706.1979.10489755) |
| **UQ-02** | Morris 1991. *Factorial sampling plans for preliminary computational experiments*. Technometrics. | [10.1080/00401706.1991.10484804](https://doi.org/10.1080/00401706.1991.10484804) |
| **UQ-03** | Sobol 2001. *Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates*. Mathematics and Computers in Simulation. | [10.1016/S0378-4754(00)00270-6](https://doi.org/10.1016/S0378-4754(00)00270-6) |
| **UQ-04** | Henninger et al. 2010. *Validation, verification, and sensitivity studies in computational biomechanics*. Computer Methods in Biomechanics and Biomedical Engineering. | [10.1243/09544119JEIM649](https://doi.org/10.1243/09544119JEIM649) |
| **UQ-05** | Laz & Browne 2010. *A review of probabilistic analysis in biomechanics*. Computer Methods in Biomechanics and Biomedical Engineering. | [10.1243/09544119JEIM739](https://doi.org/10.1243/09544119JEIM739) |
| **UQ-06** | Kennedy & O'Hagan 2001. *Bayesian calibration of computer models*. Journal of the Royal Statistical Society: Series B. | [10.1111/1467-9868.00294](https://doi.org/10.1111/1467-9868.00294) |
| **UQ-07** | Roy & Oberkampf 2011. *A comprehensive framework for verification, validation, and uncertainty quantification in scientific computing*. Computer Methods in Applied Mechanics and Engineering. | [10.1016/j.cma.2011.03.016](https://doi.org/10.1016/j.cma.2011.03.016) |
| **UQ-08** | Ling, Mullins & Mahadevan 2014. *Selection of methods for uncertainty quantification of models with multiple sources of uncertainty*. Journal of Computational Physics. | [10.1016/j.jcp.2014.08.005](https://doi.org/10.1016/j.jcp.2014.08.005) |
| **UQ-09** | Berthaume et al. 2012. *Probabilistic finite element analysis of a craniofacial finite element model*. Journal of Theoretical Biology. | [10.1016/j.jtbi.2012.01.031](https://doi.org/10.1016/j.jtbi.2012.01.031) |
| **UQ-10** | Valerio & Dall'Ara 2026. *Sensitivity analysis of musculoskeletal parameters and motion variability on the mouse tibial loading*. Journal of Biomechanics 204:113377. | [10.1016/j.jbiomech.2026.113377](https://doi.org/10.1016/j.jbiomech.2026.113377) |
| **UQ-11** | Kerr et al. 2011. *Bayesian sensitivity analysis of a model of the aortic valve*. Journal of Biomechanics 44:1499–1506. | [10.1016/j.jbiomech.2011.03.008](https://doi.org/10.1016/j.jbiomech.2011.03.008) |
| **UQ-12** | Biehler, Gee & Wall 2015. *Towards efficient uncertainty quantification in complex and large-scale biomechanical problems based on a Bayesian multi-fidelity scheme*. Biomechanics and Modeling in Mechanobiology 14:489–513. | [10.1007/s10237-014-0618-0](https://doi.org/10.1007/s10237-014-0618-0) |
| **UQ-13** | Römer, Liu & Böl 2022. *Surrogate-based Bayesian calibration of biomechanical models with isotropic material behavior*. International Journal for Numerical Methods in Biomedical Engineering 38:e3575. | [10.1002/cnm.3575](https://doi.org/10.1002/cnm.3575) |
| **UQ-14** | Cox, Rinderknecht & Blanco 2015. *Predicting bite force and cranial biomechanics in the largest fossil rodent using finite element analysis*. Journal of Anatomy 226:215–223. | [10.1111/joa.12282](https://doi.org/10.1111/joa.12282) |
| **UQ-15** | Taylor, Lautenschlager, Qi & Rayfield 2017. *Biomechanical Evaluation of Different Musculoskeletal Arrangements in Psittacosaurus and Implications for Cranial Function*. The Anatomical Record 300:49–61. | [10.1002/ar.23489](https://doi.org/10.1002/ar.23489) |
| **UQ-16** | Jannel, Salisbury & Panagiotopoulou 2022. *Softening the steps to gigantism in sauropod dinosaurs through the evolution of a pedal pad*. Science Advances 8:eabm8280. | [10.1126/sciadv.abm8280](https://doi.org/10.1126/sciadv.abm8280) |
| **UQ-17** | Kote et al. 2026. *Probabilistic Finite Element Analysis of Human Rib Biomechanics: A Framework for Improved Generalizability*. Annals of Biomedical Engineering 54:1053–1067. | [10.1007/s10439-024-03571-4](https://doi.org/10.1007/s10439-024-03571-4) |
| **CT-01** | Viceconti et al. 1998. *A comparative study on different methods of automatic mesh generation of human femurs*. Medical Engineering & Physics 20:1–10. | [10.1016/S1350-4533(97)00049-0](https://doi.org/10.1016/S1350-4533(97)00049-0) |
| **CT-02** | Camacho et al. 1997. *An improved method for finite element mesh generation of geometrically complex structures with application to the skullbase*. Journal of Biomechanics 30:1067–1070. | `UNVERIFIED exact DOI in current synthesis` |
| **CT-03** | Lautenschlager 2016. *Reconstructing the past: methods and techniques for the digital restoration of fossils*. peer-reviewed review. | [UNVERIFIED exact DOI in current synthesis](https://pmc.ncbi.nlm.nih.gov/articles/PMC5098973/) |
| **CT-04** | Lautenschlager 2017. *From bone to pixel—fossil restoration and reconstruction with digital techniques*. Geology Today 33:155–159. | [10.1111/gto.12194](https://doi.org/10.1111/gto.12194) |
| **CT-05** | Chatar et al. 2023. *'Fossils': A new, fast and open-source protocol to simulate muscle-driven biomechanical loading of bone*. Methods in Ecology and Evolution. | [10.1111/2041-210X.14051](https://doi.org/10.1111/2041-210X.14051) |
| **CT-06** | Knutsen & Konovalov 2024. *Accelerating segmentation of fossil CT scans through Deep Learning*. Scientific Reports 14:20943. | [10.1038/s41598-024-71245-1](https://doi.org/10.1038/s41598-024-71245-1) |
| **CT-07** | Follet et al. 2024. *Finite element models with automatic computed tomography bone segmentation for failure load computation*. Scientific Reports 14:16576. | [10.1038/s41598-024-66934-w](https://doi.org/10.1038/s41598-024-66934-w) |
| **CT-08** | McCurry et al. 2015. *The sensitivity of biological finite element models to the resolution of surface geometry*. PeerJ 3:e988. | [10.7717/peerj.988](https://doi.org/10.7717/peerj.988) |
| **CT-09** | Erdemir et al. 2012. *Considerations for reporting finite element analysis studies in biomechanics*. Journal of Biomechanics 45:625–633. | [10.1016/j.jbiomech.2011.11.038](https://doi.org/10.1016/j.jbiomech.2011.11.038) |
| **CT-10** | Fraterrigo et al. 2026. *Tetrahedral microFE models of human trabecular bone can be a valid alternative to voxel-based hexahedral models*. Journal of the Mechanical Behavior of Biomedical Materials 176:107326. | [10.1016/j.jmbbm.2025.107326](https://doi.org/10.1016/j.jmbbm.2025.107326) |

## 14. Traceability audit of the integrated synthesis

A cross-check was performed against the four component Markdown evidence modules used as the research basis for this synthesis.

### Audit result

- **All in-text source IDs used by this synthesis resolve to an entry in its source key.** No orphan `FE-*`, `BIO-*`, `UQ-*`, or `CT-*` citation IDs were found.
- The four source modules remain the underlying evidence base: FEA/FEM methodology, *Stegoceras*/UALVP 2 biology, UQ/sensitivity, and CT/segmentation/geometry/mesh/validation.
- The audit identified two correctable presentation issues: the Woodruff & Ackermans paper was more precisely dated as **first published 4 July 2024, issue online May 2026**, and several fossil/adjacent-UQ sources in the UQ module had not been carried visibly into the synthesis. Both are corrected above. [BIO-09, UQ-14–UQ-20]
- The synthesis intentionally **does not reproduce every source from every module**. The omitted entries are peripheral to the final argument rather than evidence that the source module was ignored; the source modules remain the more exhaustive evidence records.
- This was a **traceability and coherence audit, not a fresh systematic-review audit of every sentence**. Claims that remain marked `UNVERIFIED` in the component modules are not silently upgraded in this synthesis.

### Evidence-basis rule
The synthesis should therefore be read as a second-order product:

`primary/authoritative source → component evidence module → integrated synthesis`

When a high-stakes claim is reused in future project documents, the component module or primary paper should be checked rather than relying on the synthesis alone.

## 15. Final synthesis

### Why this specimen?
UALVP 2 combines unusual specimen completeness, established taxonomic provenance, documented internal cranial CT anatomy, and direct use in the classic 2011 Stegoceras FEA. That makes it an unusually strong bridge between paleontological morphology and computational-method verification. [BIO-03, BIO-04, BIO-07, BIO-12]

### Why this scientific question?
The dome is mechanically distinctive and its biological function remains multi-hypothesis. FEA can test the mechanical consequences of anatomy under explicitly defined scenarios without pretending that mechanical performance alone reveals behavior or evolutionary purpose. [BIO-05–BIO-11]

### Why FEM?
The skull's irregular three-dimensional geometry, internal density/architecture and spatially heterogeneous response make FEA an appropriate computational framework for comparing stress, strain, energy and deformation across model variants. The literature's strongest use case is comparative/mechanistic analysis rather than recovery of a unique historical stress state. [FE-01, FE-04, FE-11]

### Why this model formulation?
A linear-static FE baseline is scientifically defensible for the project's current deterministic phase because it is computationally tractable, analytically verifiable and suitable for isolating the effects of geometry/material/load assumptions. It should be described explicitly as a **baseline model**, not as a full physical simulation of a dynamic collision. The 2011 authors themselves described transient impact analysis as a future extension. [BIO-07, FE-19]

### What earlier researchers established
The prior literature already established the main mechanical benchmark: UALVP 2 can be modeled from CT data; under the published 1360 N static impact approximation and chosen material/constraint assumptions, the dome remained below the failure criteria used by the authors and showed load attenuation through the dome. [BIO-07] Earlier and independent work also established that mesh resolution, material properties, loading, BCs and geometry matter to FE results. [FE-10–FE-18]

### What remains uncertain
The major unresolved variables are not primarily whether the solver can produce a number. They are the biological and representational inputs: fossil-specific constitutive properties; CT-to-material mapping; segmentation and matrix treatment; repaired/smoothed geometry; contact area and force direction; head/neck constraints; transient vs static loading; and the behavioral interpretation assigned to any load case. [BIO-07, BIO-09, CT-06, CT-07, FE-18]

### Why mesh convergence is necessary
Without a controlled refinement study, changes in energy, displacement or stress could reflect numerical discretization rather than the biological model. Bright & Rayfield's cranial mesh-density study directly demonstrates this problem, including output- and region-specific convergence behavior. [FE-10]

### Why UQ is scientifically justified
The evidence base contains multiple independent uncertainty sources that cannot be measured directly from the fossil: materials, geometry/segmentation, loading, BCs and model form. UQ is therefore not added merely for sophistication; it is a way to determine which of those assumptions actually control the scientific outputs and whether the conclusions remain stable across plausible alternatives. [FE-08, FE-13, FE-18, UQ-04–UQ-08, FE-21]

### What could this project add beyond reproducing an existing Stegoceras FEA?
The strongest candidate contribution is not another single stress map. It is a **reproducible and uncertainty-aware specimen-specific analysis** in which numerical convergence is demonstrated independently, upstream geometry/segmentation choices are recorded and tested separately, force/material/BC assumptions are explicitly parameterized or scenarized, and the final biological interpretation is limited to conclusions that survive those tests. This remains a `candidate contribution` rather than an established novelty claim until the literature chase is exhaustive.

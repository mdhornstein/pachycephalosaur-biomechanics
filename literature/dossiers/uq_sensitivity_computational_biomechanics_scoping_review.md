# UQ / Sensitivity / Computational Biomechanics — Evidence Module for Stegoceras / UALVP 2

**Status:** Evidence-base scoping module; not a final literature-review chapter.  
**Search date:** 2026-09-23 (America/Los_Angeles).  
**Scope:** uncertainty quantification (UQ), sensitivity analysis, probabilistic finite-element analysis (FEA/FEM), computational biomechanics, and fossil/paleontological applications relevant to a specimen-specific CT-derived *Stegoceras validum* UALVP 2 model.

## 0. Purpose and evidence semantics

This module answers the UQ/sensitivity questions without assuming that a more sophisticated method is automatically superior. The governing principle is to match the method to the scientific question, the uncertainty type, the output of interest, the availability of empirical evidence, and the computational budget.

Evidence labels:

- **DO** — direct observation or explicit methodological fact reported by the source.
- **AI** — author interpretation or conclusion.
- **MA** — model assumption made by the study.
- **SYN** — synthesis by this review module across sources.
- **UNVERIFIED** — not verified from the primary source or an authoritative bibliographic record during this pass.
- **TO VERIFY** — candidate claim requiring a later exhaustive citation chase before being described as novel or field-wide.

A key distinction used throughout is between **parameter uncertainty** and **model-form/numerical uncertainty**. They should not be silently merged into one probability distribution.

---

## 1. Search protocol

### 1.1 Databases / search engines used

- PubMed / PubMed Central for computational biomechanics, craniofacial FE, probabilistic FE, and recent 2026 papers.
- Cross-disciplinary web search for biomechanics, computational mechanics, sensitivity/UQ, and paleontology-specific studies.
- Publisher and institutional pages (Wiley, ASME, ScienceDirect, Sage, PeerJ, PLOS/PMC, university repositories) for primary-paper metadata and abstracts.
- Backward citation chasing from major reviews and validation/UQ papers.
- Forward-oriented searches using exact titles/DOIs and topic terms for fossil sensitivity and recent UQ methods.

### 1.2 Exact search strings used (representative)

- `uncertainty quantification computational biomechanics finite element sensitivity review biomechanics`
- `finite element biomechanics uncertainty quantification sensitivity material properties loading boundary conditions`
- `paleontological finite element sensitivity analysis uncertainty biomechanics fossil`
- `uncertainty quantification fossil biomechanics finite element`
- `probabilistic finite element paleontology biomechanics`
- `sensitivity analysis paleontological finite element`
- `global sensitivity finite element biomechanics`
- `Sobol biomechanics finite element uncertainty`
- `Morris biomechanics finite element sensitivity`
- `Gaussian process surrogate finite element biomechanics`
- `model discrepancy computational mechanics validation uncertainty`
- `verification validation computational biomechanics uncertainty quantification`
- `sensitivity analysis fossil cranium finite element biomechanics`
- `probabilistic finite element fossil skull`
- `Latin hypercube fossil biomechanics finite element`
- `Monte Carlo fossil skull finite element`
- `dinosaur sensitivity analysis finite element skull`
- `global sensitivity paleontological finite element`
- `UALVP 2 Stegoceras finite element sensitivity uncertainty`
- `Stegoceras load sensitivity finite element`

### 1.3 Inclusion criteria

Include:

1. Peer-reviewed methodological papers, standards/guidance, and reviews defining UQ/V&V/sensitivity terminology or methods.
2. Peer-reviewed biomechanics studies applying probabilistic, global/local sensitivity, Bayesian, surrogate, polynomial-chaos, or related methods to finite-element or closely coupled computational biomechanical models.
3. Fossil/paleontological biomechanical studies with explicit sensitivity analyses, even when they are not full probabilistic UQ.
4. Extant cranial/osseous studies that directly test the assumptions most likely to transfer to a fossil FEA workflow: material properties, loading, boundary conditions, geometry/segmentation, and discretization.
5. Recent studies (including 2026) where methodological advances materially alter the feasible UQ workflow.

Exclude or downgrade:

- Purely statistical studies with no computational-biomechanics relevance.
- General uncertainty papers that do not inform model construction, propagation, sensitivity, validation, or interpretation.
- Websites/blogs/tutorials as scientific evidence (used only for software or terminology orientation when needed).
- Conference abstracts as primary scientific evidence when a peer-reviewed article exists; conference-only material is explicitly labeled if retained.

### 1.4 Source priority

**Highest:** primary peer-reviewed study with methods/results available.  
**High:** methodological review/standard from a recognized mechanics/biomechanics organization or peer-reviewed methods review.  
**Moderate:** peer-reviewed adjacent-domain study with strong methodological transferability but different biological system.  
**Low:** repository metadata or secondary summaries used only to verify bibliographic details.

---

# 2. UQ concepts and uncertainty taxonomy

## 2.1 What is uncertainty in computational biomechanics?

Computational biomechanics generally treats uncertainty as the lack of exact knowledge about model inputs, model structure, observations, or numerical realization, with the intent of understanding how those uncertainties affect model outputs. Reviews emphasize that uncertainty can arise from parameter values, biological/anatomical variability, simplified geometry, uncertain boundary/loading conditions, constitutive assumptions, and numerical/modeling choices. [Henninger et al. 2010; Laz & Browne 2010; Teixeira et al. 2016]

### 2.2 Recommended taxonomy for UALVP 2

| Uncertainty class | Meaning for UALVP 2 | Recommended representation | Example | Do not silently treat as |
|---|---|---|---|---|
| **Parameter uncertainty** | Numeric quantity uncertain within a selected model form | Probability distribution or bounded interval, justified by evidence | E, ν, force magnitude | Model-form error |
| **Biological variability** | Variation among individuals, ontogenetic states, or behaviors if the scientific question treats them as a population/process | Distribution only when population variation is actually relevant | Adult-to-adult force magnitude or cranial properties | Uncertainty about UALVP 2 itself |
| **Aleatory uncertainty** | Irreducible/random variability under the chosen model framing | Probability distribution | Scenario-to-scenario load direction if interpreted as behavioral variability | Lack of knowledge |
| **Epistemic uncertainty** | Lack of knowledge that could in principle be reduced | Interval, scenario ensemble, or probability distribution only with defensible elicitation | Exact material assignment from fossil CT | Random biological variability |
| **Model-form uncertainty** | Competing mathematical/physical representations | Discrete model ensemble/scenario comparison; Bayesian model averaging only if data support it | Linear elastic vs nonlinear/contact; isotropic vs zonated materials | E-distribution inflation |
| **Numerical uncertainty** | Discretization/solver approximation | Convergence study, numerical error estimate, or refinement envelope | Tet mesh density, element quality, solver tolerance | Biological UQ |
| **Geometry/data uncertainty** | Uncertainty in segmentation/reconstruction/repair or CT-derived anatomy | Plausible geometry ensemble or perturbation study; not necessarily a scalar RV | Segmentation threshold, smoothing, matrix removal, watertight repair | Pure mesh error |
| **Boundary/loading uncertainty** | Uncertain force magnitude, direction, contact area, or constraints | Continuous distributions for genuinely variable quantities; discrete scenario sets for qualitatively different load/BC models | Force direction; head/neck constraints; contact patch | A single “best guess” with narrow error bars |

**Synthesis:** For UALVP 2, much of the uncertainty is expected to be **epistemic/model-form rather than cleanly aleatory** because we have one fossil specimen and incomplete knowledge of fossil material properties, impact kinematics, contact mechanics, and biologically correct constraints. This argues for a mixture of distributions, bounded scenarios, and model ensembles rather than a single monolithic probability model.

---

# 3. Sensitivity-analysis methods

## 3.1 One-at-a-time (OAT) / local sensitivity

**Best use:** a small number of interpretable parameters around a baseline model; debugging; physical intuition; identifying whether an output is locally stable. It is inexpensive and transparent but can miss interaction effects and depends strongly on the chosen baseline/range. Henninger et al. describe sensitivity studies as a practical part of V&V and note that Monte Carlo becomes useful when many parameters are considered together. [Henninger et al. 2010]

**UALVP 2 role:** first-pass perturbation of E, ν, force magnitude, force angle, and selected BC choices after deterministic verification and mesh convergence.

## 3.2 Morris elementary-effects screening

Morris designs evaluate elementary effects across the input space and can identify influential variables plus clues to nonlinearity/interaction at lower cost than a full variance-based global analysis. The original method was explicitly designed for complicated deterministic computational models with moderate-to-large numbers of inputs. [Morris 1991]

**Use when:** parameter count is too large for direct Sobol analysis or when the first question is “which variables are worth carrying forward?”

**UALVP 2 role:** strong candidate if the input list grows beyond a small set, especially when geometry/segmentation descriptors and load variables are included.

## 3.3 Global variance-based sensitivity / Sobol indices

Sobol methods decompose output variance into contributions from individual inputs and interactions. They are global over a specified input space rather than local to one baseline point. [Sobol 1993; Sobol 2001; Saltelli et al. 2008]

**Use when:** the scientific question is “which uncertain inputs explain output variance?” and enough model evaluations are available.

**UALVP 2 role:** use for a reduced set of scientifically defensible uncertain variables after screening, ideally on surrogate or carefully designed FE ensembles.

## 3.4 Rank/correlation screening

Spearman rank correlations or related monotonic association measures are computationally simple and interpretable, and recent mandibular FE UQ uses them alongside Sobol indices. [Baugnon et al. 2026]

**Use when:** a robust low-cost global screen is needed and monotonicity is plausible enough for interpretation.

## 3.5 Design of experiments / Latin hypercube sampling (LHS)

LHS stratifies each input dimension and was introduced as a variance-reduction alternative to simple random Monte Carlo for computer-code studies. [McKay et al. 1979]

**Use when:** running a finite ensemble of expensive deterministic FE analyses and wanting broad space-filling coverage.

**Important:** LHS is a **sampling design**, not a sensitivity index by itself. It can feed global sensitivity, regression, surrogate construction, or uncertainty propagation.

## 3.6 Monte Carlo propagation

Straight Monte Carlo is the baseline forward-UQ method: sample uncertain inputs from their specified distributions, solve the model, and estimate output distributions/statistics. It is conceptually simple and flexible but may require many expensive runs, especially for tails, nonlinearities, or localized outputs. [Taddei et al. 2006; Laz & Browne 2010]

**UALVP 2 role:** useful once the input distributions/scenarios are defensible, especially for a small-to-moderate number of uncertain variables.

## 3.7 Surrogate / emulator models

Surrogates approximate the expensive FE model so that millions of virtual evaluations, sensitivity analysis, or Bayesian sampling become practical. Gaussian-process (GP) emulators are one established option for smooth deterministic model responses; polynomial-chaos (PC/PCE) expansions are another. [Kennedy & O'Hagan 2001; Biehler et al. 2015; Römer et al. 2022; Baugnon et al. 2026]

**UALVP 2 role:** warranted only if the high-fidelity model is expensive enough that direct LHS/MC/Sobol is computationally prohibitive. The surrogate itself must be validated against withheld FE runs.

## 3.8 Gaussian processes

GPs are particularly useful for relatively low-dimensional, smooth response surfaces and for uncertainty-aware emulation. They become less attractive when the response is strongly discontinuous, has sharp regime transitions, or combines qualitatively different model classes. Bayesian biomechanical sensitivity studies have used GP emulators specifically to reduce FE evaluation cost. [Kerr et al. 2011; Römer et al. 2022]

## 3.9 Polynomial chaos expansion (PCE)

PCE approximates stochastic model response in a basis adapted to the input random variables. It can provide output moments and sensitivity measures efficiently when the response is sufficiently smooth and the stochastic dimension is manageable. Recent biomedical FE work uses sparse PCE specifically to make global UQ tractable. [Rupp et al. 2020/2021; Römer et al. 2022; Baugnon et al. 2026]

## 3.10 Bayesian methods

Bayesian calibration is most useful when **observational/experimental data can inform uncertain parameters and model predictions**. Kennedy & O'Hagan explicitly distinguish remaining parameter uncertainty from model discrepancy and use data to infer both. [Kennedy & O'Hagan 2001]

For UALVP 2, Bayesian calibration should **not** be treated as mandatory forward UQ. The project presently lacks direct experimental validation data for the fossil model sufficient to identify posterior distributions for E, ν, impact force, BCs, etc. Bayesian methods become more compelling if the project acquires informative extant/fossil experimental analog data or a validated calibration target.

---

# 4. Uncertainty-propagation methods and computational tradeoffs

| Method | Core question | Typical strengths | Main cost/limitation | UALVP 2 fit |
|---|---|---|---|---|
| OAT/local perturbation | Does a small plausible change matter near baseline? | Cheap, transparent, easy to debug | Misses interactions; baseline-dependent | **High** for initial sensitivity |
| Morris | Which inputs merit attention? | Efficient screening; detects nonlinearity hints/interactions | Not a full variance decomposition; interpretation depends on trajectories/ranges | **High** if input count grows |
| MC | What is the output distribution under specified input distributions? | Simple, flexible, distribution-aware | Can require many FE solves | **Moderate–high** for low-dimensional UQ |
| LHS | How can finite samples cover input space efficiently? | Better stratification/coverage than simple random sampling for many estimators | Still requires many evaluations; not itself a sensitivity metric | **High** |
| Sobol | How much variance is attributable to each input and interactions? | Global, interaction-aware, interpretable | Requires many model evaluations; convergence must be checked | **High** after screening/surrogate |
| PCE | Can output statistics/sensitivity be represented compactly? | Efficient for smooth stochastic response; moments/indices readily derived | Basis/truncation choices; poor fit to discontinuous responses | **Conditional** |
| GP surrogate | Can FE evaluations be emulated accurately? | Flexible, uncertainty-aware; useful for adaptive designs | Training scales poorly with sample count; poor with discontinuities/model switching | **Conditional–high** |
| Bayesian calibration | What parameter posterior is consistent with observed data? | Explicit prior/data updating and posterior uncertainty | Requires informative data; identifiability/model-discrepancy issues | **Low now; potentially high later** |
| Active learning | Where should the next expensive simulations be placed? | Can target surrogate error / tails / decision boundaries | Added design complexity; only worthwhile after a surrogate need is demonstrated | **Conditional** |

---

# 5. Validation, verification, and model discrepancy

## 5.1 Verification comes before validation and UQ

Henninger et al. explicitly distinguish verification (“solving the equations right”) from validation (“solving the right equations”) and recommend that verification precede validation. Calculation verification includes discretization/mesh convergence. [Henninger et al. 2010]

For UALVP 2 this supports:

1. analytical/benchmark solver verification;
2. mesh-convergence verification on the frozen geometry/modeling pipeline;
3. only then parameter sensitivity and probabilistic propagation.

## 5.2 What constitutes good validation?

Good validation is tied to the intended use and to measured quantities that can actually test the model. Henninger et al. stress that validation should use well-defined boundary conditions, prioritized quantities of interest, and explicit comparison criteria. [Henninger et al. 2010]

For fossil biomechanics, direct specimen-specific validation is generally unavailable. Extant validation studies therefore provide **methodological precedent rather than direct biological validation of the fossil**. [Bright & Rayfield 2011; Godinho et al. 2017]

## 5.3 Model discrepancy

Model discrepancy is the difference between the computational model and the real system that remains even after best-fitting parameter values are considered. Kennedy & O'Hagan introduced a Bayesian calibration framework that explicitly represents discrepancy; later work emphasizes that discrepancy priors are themselves difficult to specify and can interact with parameter identifiability. [Kennedy & O'Hagan 2001; Ling et al. 2014]

**UALVP 2 recommendation:** do not create a broad “discrepancy distribution” merely to absorb every model weakness. Where no fossil validation data exist, use explicit **model-form scenario branches** (e.g., homogeneous vs zonated material, broad vs concentrated load, alternative BCs) and report them separately from parameter-distribution UQ. A formal statistical discrepancy model should be considered only when there is an actual validation dataset and a defensible validation domain.

---

# 6. Fossil-specific UQ / sensitivity bibliography

> The fossil-specific literature identified here is dominated by **sensitivity analysis and scenario comparison**, not full probabilistic UQ. This is an important result of the search rather than an assertion that no other study exists. The strongest examples below are directly relevant to material properties, loading, geometry, boundary conditions, and model simplification.

### F01 — Snively & Theodor (2011)

**Citation:** Snively E, Theodor JM. 2011. Common functional correlates of head-strike behavior in the pachycephalosaur *Stegoceras validum* and combative artiodactyls. *PLoS ONE* 6(6): e21422.  
**DOI:** 10.1371/journal.pone.0021422  
**Method:** CT-derived fossil FE, static impact-style loading, alternative load-spread/keratin-pad scenarios.  
**UQ relevance:** direct Stegoceras precedent for load-distribution sensitivity; not full probabilistic UQ.  
**UALVP 2 relevance:** benchmark for distinguishing force magnitude from contact/force-spread assumptions.

### F02 — Cox et al. (2015)

**Citation:** Cox PG, Rinderknecht A, Blanco RE. 2015. Predicting bite force and cranial biomechanics in the largest fossil rodent using finite element analysis. *Journal of Anatomy* 226:215–223.  
**DOI:** 10.1111/joa.12282  
**Method:** fossil cranial FE; muscle-force magnitude and orientation altered sequentially.  
**DO:** ±20% muscle-force magnitude and ±10° orientation perturbations were used; bite-force predictions changed more than stress patterns, with the reported bite-force effect remaining below 35% at the teeth.  
**UQ relevance:** local load sensitivity in a fossil; shows that selected force uncertainties can have different effects on different QoIs.

### F03 — Taylor et al. (2017)

**Citation:** Taylor AC, Lautenschlager S, Qi Z, Rayfield EJ. 2017. Biomechanical Evaluation of Different Musculoskeletal Arrangements in *Psittacosaurus* and Implications for Cranial Function. *Anatomical Record* 300:49–61.  
**DOI:** 10.1002/ar.23489  
**Method:** CT/digital cranial reconstruction + FE; geometric-morphometric-informed sensitivity analysis.  
**DO:** bite position had a greater effect on loading-induced deformation than the tested muscle-loading or material-property variation.  
**UQ relevance:** supports treating load location/contact position as a potentially high-priority uncertain variable rather than focusing only on E.

### F04 — McCurry et al. (2015)

**Citation:** McCurry MR, Evans AR, McHenry CR. 2015. The sensitivity of biological finite element models to the resolution of surface geometry: a case study of crocodilian crania. *PeerJ* 3:e988.  
**DOI:** 10.7717/peerj.988  
**Method:** seven high-resolution crocodilian cranial surfaces down-sampled to different resolutions while holding solid-element count constant.  
**DO:** decreasing surface resolution caused fluctuations in strain magnitudes, but stable comparative results were obtainable at lower resolutions.  
**UQ relevance:** surface geometry resolution and solid-mesh density are separable uncertainty sources.

### F05 — Godinho et al. (2017)

**Citation:** Godinho RM, Toro-Ibacache V, Fitton LC, O’Higgins P. 2017. Finite element analysis of the cranium: Validity, sensitivity and future directions. *Comptes Rendus Palevol* 16:600–612.  
**DOI:** 10.1016/j.crpv.2016.11.002  
**Method:** cadaveric human cranium validation; segmentation/material-property simplification sensitivity.  
**DO:** absolute deformations were not accurately predicted, whereas the distribution of relatively high/low strains and global deformation modes were reasonably approximated.  
**UQ relevance:** supports cautious interpretation of absolute quantities and stronger emphasis on robust spatial/comparative outputs.

### F06 — Jannel et al. (2022)

**Citation:** Jannel A, Salisbury SW, Panagiotopoulou O. 2022. Softening the steps to gigantism in sauropod dinosaurs through the evolution of a pedal pad. *Science Advances* 8(32): eabm8280.  
**DOI:** 10.1126/sciadv.abm8280  
**Method:** multiple dinosaur FE models with explicit sensitivity branches for material properties, soft-tissue properties, loads, and boundary conditions.  
**DO:** sensitivity branches produced broadly similar stress patterning but substantial changes in stress magnitude for some boundary-condition/property choices.  
**UQ relevance:** strong precedent for treating model-form/scenario choices separately and reporting pattern vs magnitude.

### F07 — Sylvester & Kramer (2018)

**Citation:** Sylvester AD, Kramer PA. 2018. Young's Modulus and Load Complexity: Modeling Their Effects on Proximal Femur Strain. *Anatomical Record* 301:1189–1202.  
**DOI:** 10.1002/ar.23796  
**Scope:** extant femur, explicitly motivated by implications for fossil FEA.  
**Method:** material-property and load-complexity sensitivity in FE.  
**UQ relevance:** useful adjacent/fossil-methodology bridge; exact quantitative sensitivity findings were not fully re-extracted in this pass.

### F08 — Anderson et al. (2012)

**Citation:** Anderson PSL, Bright JA, Gill PG, Palmer C, Rayfield EJ. 2012. Models in palaeontological functional analysis. *Biology Letters* 8:119–122.  
**DOI:** 10.1098/rsbl.2011.0674  
**UQ relevance:** review-level synthesis stating that fossil skull FE models with sparse input data can reproduce strain patterns/orientations more reliably than absolute numerical values, and that sensitivity/validation should accompany model interpretation.

---

# 7. Adjacent biomechanics UQ bibliography

### B01 — Taddei et al. (2006)

**Citation:** Taddei F, Martelli S, Reggiani B, Cristofolini L, Viceconti M. 2006. Finite-element modeling of bones from CT data: sensitivity to geometry and material uncertainties. *IEEE Transactions on Biomedical Engineering*.  
**DOI:** 10.1109/TBME.2006.879473  
**Method:** Monte Carlo sensitivity analysis on CT-derived femur models; geometry, density and mechanical properties treated as uncertain inputs; two loading conditions.  
**DO:** geometric representation errors were reported as dominant variables for stress in the studied cases; the influence of geometry/material errors could not be assumed a priori.  
**UALVP 2 use:** direct methodological precedent for separating geometry and material uncertainty.

### B02 — Bright & Rayfield (2011)

**Citation:** Bright JA, Rayfield EJ. 2011. Sensitivity and ex vivo validation of finite element models of the domestic pig cranium. *Journal of Anatomy* 219:456–471.  
**DOI:** 10.1111/j.1469-7580.2011.01408.x  
**Method:** specimen-specific validation against ex vivo strain gauges; material sensitivity, loading-direction and gauge-placement sensitivity.  
**DO:** models were especially sensitive to material properties; CT resolution and missing local heterogeneity were identified as likely contributors to discrepancy. Absolute breaking stress/bite-force estimates warrant caution, whereas relative strain environments may be more robust.  
**UALVP 2 use:** major basis for material sensitivity and pattern-vs-magnitude interpretation.

### B03 — Berthaume et al. (2012)

**Citation:** Berthaume MA, Dechow PC, Iriarte-Diaz J, Ross CF, Strait DS, Wang Q, Grosse IR. 2012. Probabilistic finite element analysis of a craniofacial finite element model. *Journal of Theoretical Biology* 300:242–253.  
**DOI:** 10.1016/j.jtbi.2012.01.031  
**Method:** probabilistic craniofacial FE; cortical material treated under several homogeneous/non-homogeneous and orthotropic assumptions; Gaussian randomization and LHS; 426 deterministic FE simulations.  
**UALVP 2 use:** strong precedent for probabilistic material-property propagation in cranial FE.

### B04 — Kerr et al. (2011)

**Citation:** Kerr IM, ... 2011. Bayesian sensitivity analysis of a model of the aortic valve. *Journal of Biomechanics* 44:1499–1506.  
**DOI:** 10.1016/j.jbiomech.2011.03.008  
**Method:** global sensitivity analysis on uncertain loading, material properties, and model dimensions using a Bayesian/GP emulator.  
**DO:** the study found output standard deviations up to 44% of the mean in tested quantities and used the emulator to reduce FE cost.  
**UALVP 2 use:** methodological precedent for GP-assisted global sensitivity; not directly transferable to fossil model-form uncertainty.

> **Bibliographic note:** full author list and some implementation details were not fully re-extracted here; retain this entry as a high-priority primary-paper retrieval target.

### B05 — Biehler, Gee & Wall (2015)

**Citation:** Biehler J, Gee MW, Wall WA. 2015. Towards efficient uncertainty quantification in complex and large-scale biomechanical problems based on a Bayesian multi-fidelity scheme. *Biomechanics and Modeling in Mechanobiology* 14:489–513.  
**DOI:** 10.1007/s10237-014-0618-0  
**Method:** uncertainty quantification for large nonlinear patient-specific FE models of abdominal aortic aneurysms; random-field constitutive parameter; direct Monte Carlo used as reference; multi-fidelity scheme reduced computational cost.  
**UALVP 2 use:** precedent for reducing UQ cost when nonlinear FE becomes too expensive.

### B06 — Römer et al. (2022)

**Citation:** Römer U, Liu J, Böl M. 2022. Surrogate-based Bayesian calibration of biomechanical models with isotropic material behavior. *International Journal for Numerical Methods in Biomedical Engineering* 38:e3575.  
**DOI:** 10.1002/cnm.3575  
**Method:** reduced-order response representation + polynomial-chaos surrogate + Bayesian inference + Sobol sensitivity.  
**DO:** surrogate modeling was used to make sampling-intensive MCMC practical and to quantify surrogate approximation/truncation effects.  
**UALVP 2 use:** strong precedent for a future surrogate-assisted UQ stage, but not evidence that Bayesian calibration is needed now.

### B07 — Rupp et al. (2020/2021)

**Citation:** Rupp LC, Liu Z, Bergquist JA, et al. Using UncertainSCI to Quantify Uncertainty in Cardiac Simulations. *Computing in Cardiology* 2020.  
**DOI:** 10.22489/CinC.2020.275  
**Publication type:** conference proceedings; **downgraded relative to peer-reviewed journal papers**.  
**Method:** non-intrusive polynomial-chaos framework for FE/BEM cardiac simulations; sensitivity and output statistics.  
**UALVP 2 use:** software/method precedent only; not a primary biological evidence source.

### B08 — Razu et al. (2023)

**Citation:** Razu SS, Jahandar H, Zhu A, et al. 2023. Bayesian Calibration of Computational Knee Models to Estimate Subject-Specific Ligament Properties, Tibiofemoral Kinematics, and Anterior Cruciate Ligament Force With Uncertainty Quantification. *Journal of Biomechanical Engineering* 145:071003.  
**DOI:** 10.1115/1.4056968  
**Method:** Bayesian calibration of a computational knee model to estimate subject-specific properties/outputs with UQ.  
**UALVP 2 use:** demonstrates that Bayesian inference is most valuable when observed data can constrain unknown model parameters.

### B09 — Kote et al. (2026)

**Citation:** Kote VB, Frazer LL, Shukla A, et al. 2026. Probabilistic Finite Element Analysis of Human Rib Biomechanics: A Framework for Improved Generalizability. *Annals of Biomedical Engineering* 54:1053–1067.  
**DOI:** 10.1007/s10439-024-03571-4  
**Method:** probabilistic FE + statistical shape modeling; uncertainty in cortical material properties and rib shape; response-surface model for rapid exploration.  
**UALVP 2 use:** important current precedent for geometry + material variation plus surrogate response surfaces.

### B10 — Baugnon et al. (2026)

**Citation:** Baugnon L, Nicot R, Bethune N, Lecomte-Grosbras P, Witz J-F, Colliat J-B, Mayeur O. 2026. Uncertainty quantification and global sensitivity analysis of a patient-specific mandibular finite element model using Latin hypercube sampling and sparse polynomial chaos expansion. *Medical Engineering & Physics* 147(8).  
**DOI:** 10.1088/1873-4030/ae995b  
**Method:** 24 uncertain inputs; 2,400 FE simulations; LHS + sparse PCE; Spearman and Sobol sensitivity; convergence assessment for regional/global outputs.  
**DO:** muscle-force magnitudes and articular-disc stiffness dominated the stress variability within the explored ranges; high-resolution bone-property classification had negligible effect in that model; contact-sensitive regional estimates required >2,000 samples for stable sensitivity estimates.  
**UALVP 2 use:** strongest recent direct methodological precedent for the project’s proposed staged global UQ workflow, including explicit sample-size convergence.

### B11 — Valerio & Dall’Ara (2026)

**Citation:** Valerio T, Dall’Ara E. 2026. Sensitivity analysis of musculoskeletal parameters and motion variability on the mouse tibial loading. *Journal of Biomechanics* 204:113377.  
**DOI:** 10.1016/j.jbiomech.2026.113377  
**Method:** Morris global sensitivity analysis of 173 inputs, including muscle properties, joint angles, and ground-reaction-force parameters.  
**DO:** a subset of 19 parameters significantly affected tibial load magnitude when the force-length-velocity relationship was excluded.  
**UALVP 2 use:** excellent recent precedent for Morris as a first-stage screening tool when input dimension becomes large.

---

# 8. Foundational UQ / sensitivity / VVUQ bibliography

### M01 — McKay, Beckman & Conover (1979)

**Citation:** McKay MD, Beckman RJ, Conover WJ. 1979. Comparison of three methods for selecting values of input variables in the analysis of output from a computer code. *Technometrics* 21:239–245.  
**DOI:** 10.1080/00401706.1979.10489755  
**Role:** foundational LHS sampling reference.

### M02 — Morris (1991)

**Citation:** Morris MD. 1991. Factorial Sampling Plans for Preliminary Computational Experiments. *Technometrics* 33:161–174.  
**DOI:** 10.1080/00401706.1991.10484804  
**Role:** foundational Morris elementary-effects screening reference.

### M03 — Sobol (1993)

**Citation:** Sobol IM. 1993. Sensitivity estimates for nonlinear mathematical models. *Mathematical Modelling and Computational Experiments* 1(4):407–414.  
**Stable identifier:** CiNii record; title/metadata verified.  
**Role:** variance-decomposition sensitivity foundation.

### M04 — Sobol (2001)

**Citation:** Sobol IM. 2001. Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates. *Mathematics and Computers in Simulation* 55:271–280.  
**DOI:** 10.1016/S0378-4754(00)00270-6  
**Role:** global sensitivity indices and Monte Carlo estimation.

### M05 — Saltelli et al. (2008)

**Citation:** Saltelli A, Ratto M, Andres T, et al. 2008. *Global Sensitivity Analysis: The Primer*. John Wiley & Sons.  
**ISBN:** 978-0-470-72517-7  
**Role:** practical global-sensitivity methods, screening/variance-based framing, and computational-design guidance.

### M06 — Henninger et al. (2010)

**Citation:** Henninger HB, Reese SP, Anderson AE, Weiss JA. 2010. Validation of Computational Models in Biomechanics. *Proceedings of the Institution of Mechanical Engineers, Part H* 224:801–812.  
**DOI:** 10.1243/09544119JEIM649  
**Role:** V&V ordering, mesh convergence, sensitivity, validation design, and intended-use framing.

### M07 — Laz & Browne (2010)

**Citation:** Laz PJ, Browne M. 2010. A review of probabilistic analysis in orthopaedic biomechanics. *Proceedings of the Institution of Mechanical Engineers, Part H* 224:801–812.  
**DOI:** 10.1243/09544119JEIM739  
**Role:** review of probabilistic methods across orthopaedic biomechanics, including geometry, material properties, kinematics and loading.

> **Note:** bibliographic pagination metadata on publisher pages overlaps with the adjacent Henninger review; DOI is the stable identifier used here.

### M08 — Kennedy & O'Hagan (2001)

**Citation:** Kennedy MC, O'Hagan A. 2001. Bayesian calibration of computer models. *Journal of the Royal Statistical Society: Series B* 63:425–464.  
**DOI:** 10.1111/1467-9868.00294  
**Role:** Bayesian calibration, parameter uncertainty, and explicit model discrepancy.

### M09 — Roy & Oberkampf (2011)

**Citation:** Roy CJ, Oberkampf WL. 2011. A comprehensive framework for verification, validation, and uncertainty quantification in scientific computing. *Computer Methods in Applied Mechanics and Engineering* 200:2131–2144.  
**DOI:** 10.1016/j.cma.2011.03.016  
**Role:** integrated VVUQ, aleatory vs epistemic uncertainty, model-form uncertainty, and numerical error.

### M10 — Ling, Mullins & Mahadevan (2014)

**Citation:** Ling Y, Mullins J, Mahadevan S. 2014. Selection of model discrepancy priors in Bayesian calibration. *Journal of Computational Physics* 276:665–680.  
**DOI:** 10.1016/j.jcp.2014.08.005  
**Role:** cautions around discrepancy-prior specification, identifiability, calibration, and validation.

---

# 9. Evidence matrix

| ID | Domain | Method | Uncertain inputs | Output/QoI | Key evidence | Primary limitation / transfer issue | UALVP 2 relevance |
|---|---|---|---|---|---|---|---|
| F01 | Fossil | FE scenario sensitivity | Force spread/contact/keratin | Stress/strain | Load-spread assumptions affect response | Static fossil impact model; no full probability model | Direct |
| F02 | Fossil | OAT/local sensitivity | Muscle force, force angle | Bite force/stress | Bite force more sensitive than stress | Load perturbations selected by authors | Direct |
| F03 | Fossil | Geometry-informed sensitivity | Bite position, muscle loading, material variation | Deformation/stress/bite force | Bite position greater effect than tested material/loading variation | Psittacosaurus cranial system | High |
| F04 | Extant comparative | Geometry sensitivity | Surface resolution | Strain | Geometry resolution changes strain magnitudes; comparative patterns can stabilize | Crocodilian crania, not fossil | High |
| F05 | Extant cranial validation | Validation + sensitivity | Segmentation/material simplification | Deformation/strain | Absolute deformation weak; spatial strain pattern more robust | Human cranium | High |
| F06 | Fossil | Scenario sensitivity | Material, pad properties, BCs, loads | Stress | BC/property choices can alter magnitudes while patterns may remain similar | Sauropod feet, not cranium | Moderate–high |
| F07 | Adjacent fossil-method | Parameter/load sensitivity | E, load complexity | Strain | Explicit fossil-method motivation | Extant femur | Moderate |
| F08 | Fossil-method review | Review | General model assumptions | Pattern vs absolute output | Sparse-input fossil FE better for relative/pattern inference | Review-level synthesis | High |
| B01 | Bone FE | Monte Carlo | Geometry, density, material | Stress/FE outputs | Geometry errors dominant for stress in studied cases | Human femur CT | High |
| B02 | Cranial validation | Sensitivity + experiment | Material, loading direction, gauge placement | Strain | Material properties major sensitivity; absolute values caution | Pig cranium | High |
| B03 | Cranial probabilistic FE | LHS + probabilistic FE | Cortical material properties | Stress/strain | 426 FE runs; material distributions propagated | Macaque cranium | High |
| B04 | Cardiovascular FE | Bayesian/GP global sensitivity | Loading, materials, dimensions | Stress | GP emulator enables global sensitivity; large output variability possible | Aortic valve | Moderate |
| B05 | Nonlinear biomech | Multi-fidelity UQ | Constitutive random field | Stress/strain/energy | MC benchmark; cost reduction with multi-fidelity | Aneurysm mechanics | Moderate |
| B06 | Biomech | PCE + Bayesian + Sobol | Hyperelastic material parameters | Force response | Surrogate makes MCMC practical; surrogate error explicitly considered | Soft-tissue/material model | Moderate |
| B07 | Biomech | PCE UQ | Conductivities/geometry | Cardiac potentials | Non-intrusive PC emulator | Conference paper; cardiac system | Moderate |
| B08 | Biomech | Bayesian calibration | Ligament/material/kinematic parameters | Kinematics/force | Posterior UQ from observed data | Requires informative calibration data | Conditional |
| B09 | Biomech | Probabilistic FE + shape model | Rib shape, cortical properties | Impact response | Population geometry + material variability with response surface | Human rib | High methodological precedent |
| B10 | Biomech | LHS + sparse PCE + Sobol | 24 loading/material/discretization inputs | Von Mises stress | 2400 FE runs; sensitivity-estimate convergence assessed | Human mandible | Very high |
| B11 | Biomech | Morris GSA | 173 musculoskeletal inputs | Tibial forces | 19 important inputs in reduced case | Mouse locomotion model | High for screening |
| M01 | Methods | LHS | Sampling design | Generic outputs | Better variance properties than simple random sampling for many estimators | Not a UQ model by itself | Foundational |
| M02 | Methods | Morris | Many inputs | Generic output | Efficient screening; elementary effects | Not full variance decomposition | Foundational |
| M03 | Methods | Sobol | Input distributions | Output variance | Global variance decomposition | Requires appropriate sampling/convergence | Foundational |
| M04 | Methods | Sobol + MC | Input distributions | Output variance | Monte Carlo estimation of global indices | Computationally expensive for high-cost models | Foundational |
| M05 | Methods | Global sensitivity | Model/input space | Generic output | Practical method-selection framework | Book-level guidance | Foundational |
| M06 | VVUQ | Verification/validation | Numerical/model assumptions | Intended QoIs | Verification before validation; mesh convergence | General biomechanics | Foundational |
| M07 | Biomech review | Probabilistic UQ | Geometry/material/loading/kinematics | Performance | Probability methods can characterize impact of variability | Orthopaedic rather than fossil | Foundational |
| M08 | UQ foundations | Bayesian calibration | Parameter + discrepancy | Prediction | Explicitly separates parameter uncertainty and discrepancy | Requires data for calibration | Foundational |
| M09 | UQ foundations | Integrated VVUQ | Aleatory/epistemic/model/numerical | Predictive uncertainty | Treats multiple uncertainty classes separately | General scientific computing | Foundational |
| M10 | UQ foundations | Bayesian discrepancy | Model discrepancy | Prediction/validation | Discrepancy priors can be difficult and affect identifiability | Requires validation framework | Foundational |

---

# 10. What the literature supports about each proposed method

## 10.1 One-at-a-time sensitivity

**Supported.** Appropriate as a transparent first pass around a verified baseline. It is especially useful for determining whether an uncertainty source deserves more formal treatment. It should not be presented as a complete global uncertainty analysis because interactions can be missed. [Henninger et al. 2010]

## 10.2 Monte Carlo

**Supported.** Direct propagation is conceptually clean and remains a reference method in biomechanics. Its main weakness is cost. [Taddei et al. 2006; Biehler et al. 2015]

## 10.3 LHS

**Supported.** Strong candidate for efficient FE ensembles. It improves space-filling/variance characteristics relative to simple random sampling but does not solve the problem of choosing defensible input distributions. [McKay et al. 1979]

## 10.4 Morris

**Supported and especially attractive for UALVP 2 if input count expands.** The 2026 mouse musculoskeletal study demonstrates modern biomechanical use at 173 inputs. [Valerio & Dall’Ara 2026]

## 10.5 Sobol

**Supported, but best after screening or on a surrogate.** Sobol is appropriate when the scientific question is variance attribution and interactions, not merely ranking a few perturbations. Convergence diagnostics are essential. The 2026 mandibular study explicitly assessed sensitivity-estimate convergence. [Sobol 2001; Baugnon et al. 2026]

## 10.6 Surrogate models

**Supported conditionally.** Surrogates become useful when repeated FE evaluation is the dominant cost. The literature shows successful use of GP and PCE approaches in biomechanics, including Bayesian calibration and global sensitivity. [Kerr et al. 2011; Biehler et al. 2015; Römer et al. 2022; Baugnon et al. 2026]

## 10.7 Gaussian processes

**Supported conditionally.** Best when the response is reasonably smooth and the dimension is modest. Validate prediction error against withheld FE evaluations. Do not assume GP uncertainty equals physical/model-form uncertainty; emulator error is a separate numerical/statistical layer.

## 10.8 Bayesian methods

**Supported only when the question is calibration/inference and informative data exist.** They are not automatically an improvement over forward Monte Carlo/LHS for UALVP 2. Without data, a Bayesian posterior can simply encode subjective priors rather than empirical information. Model discrepancy adds another identifiability problem. [Kennedy & O'Hagan 2001; Ling et al. 2014]

## 10.9 Active learning

**Supported as a cost-control strategy, not as a required UQ method.** It becomes justified when an initial surrogate is demonstrably inaccurate or when decision-relevant output regions are poorly sampled. It should follow, not precede, basic surrogate validation.

---

# 11. Recommended uncertainty taxonomy for UALVP 2

## Tier 1 — numerical uncertainty

### 1A. Tetrahedral discretization

**Treatment:** mesh-convergence study; report global and regional QoIs across refinement levels.  
**Not:** random biological variable.  
**Outputs:** energy, apex displacement, regional stress summary, local peak stress with artifact mask.

### 1B. Element quality / solver tolerance

**Treatment:** calculation-verification checks; deterministic unless evidence shows meaningful residual uncertainty.  
**Outputs:** displacement/energy/residuals.

## Tier 2 — geometry/data uncertainty

### 2A. Segmentation / matrix-removal threshold

**Treatment:** discrete set of plausible segmentations or controlled segmentation perturbations.  
**Outputs:** geometry metrics, energy, displacement, regional stress.

### 2B. Surface smoothing / repair / watertight regularization

**Treatment:** discrete geometry variants or parameter perturbation ranges; keep separate from h-refinement.  
**Outputs:** same as above.

### 2C. Missing/ambiguous internal zones

**Treatment:** explicit alternative geometry/material-zone branches rather than forcing a scalar distribution where no evidence supports one.  
**Outputs:** regional stress/energy/displacement.

## Tier 3 — constitutive/material uncertainty

### 3A. Young's modulus E

**Treatment:** probability distribution only if evidence supports parameterization; otherwise bounded scenario distribution with sensitivity analysis. Do not treat literature values as measured UALVP 2 values.  
**Outputs:** stress, strain, energy, displacement.

### 3B. Poisson's ratio ν

**Treatment:** bounded distribution/scenario; consider correlation with E only when justified.  
**Outputs:** stress/deformation/energy.

### 3C. Spatial heterogeneity / zonation

**Treatment:** model-form branch: homogeneous vs zonated; potentially probabilistic zonal parameters later.  
**Outputs:** regional stress/strain, energy, displacement.

## Tier 4 — load and boundary-condition uncertainty

### 4A. Force magnitude

**Treatment:** continuous distribution or bounded scenarios around a biologically justified reference force.  
**Outputs:** displacement, stress, energy; use linear-scaling shortcuts only after verifying linear static assumptions.

### 4B. Force direction

**Treatment:** bounded angular distribution or scenario grid.  
**Outputs:** displacement/stress patterns and regional summaries.

### 4C. Contact/load area and distribution

**Treatment:** discrete scenario family unless sufficient evidence exists to assign a continuous distribution.  
**Outputs:** local/regional stress and energy.

### 4D. Boundary constraints / head-neck support

**Treatment:** scenario ensemble, not a generic probability distribution unless biologically interpretable.  
**Outputs:** especially local stress near constraints and global displacement/energy.

## Tier 5 — model-form uncertainty

### 5A. Linear vs nonlinear/contact

**Treatment:** separate model branch; not “noise” on a linear-model parameter.  
**Outputs:** stress, energy, deformation, contact behavior.

### 5B. Static vs dynamic impact

**Treatment:** future model-form comparison if the scientific question demands impact dynamics.  
**Outputs:** transient energy, peak stress/strain, deformation rate; far more computationally expensive.

### 5C. Isotropic vs anisotropic material model

**Treatment:** scenario/model-class comparison; probabilistic anisotropy only if data support it.  
**Outputs:** local and regional stress/strain patterns.

---

# 12. Proposed mapping: uncertainty source → variable/model choice → FEM output

| Uncertainty source | Variable / model choice | Suggested initial treatment | Primary FEM outputs | Priority |
|---|---|---|---|---|
| Mesh discretization | element size / element count | convergence sequence | energy, apex displacement, regional stress | **Critical now** |
| Segmentation | segmentation threshold / plausible surface | scenario ensemble | volume, surface metrics, energy, regional stress | **High** |
| Surface repair | smoothing/remeshing parameters | controlled variants | energy/displacement/regional stress | **High** |
| E | Young's modulus | bounded/probabilistic range if justified | stress, strain, energy, displacement | **High** |
| ν | Poisson ratio | bounded/probabilistic range | displacement/stress | **Moderate** |
| Material zonation | homogeneous vs zonated mapping | discrete model branch | regional stress/strain, energy | **High** |
| Force magnitude | F | bounded distribution/scenario | displacement, energy, stress | **High** |
| Force direction | θ/φ | angular scenario/distribution | displacement/stress map | **High** |
| Contact area | patch size/shape | discrete load scenarios | local/regional stress | **High** |
| Boundary condition | constraint set | discrete model scenarios | displacement, energy, constraint-region stress | **High** |
| Solver/numerical settings | tolerances/element order | deterministic verification | numerical residuals/output convergence | **Critical now** |
| Constitutive law | linear elastic / nonlinear/contact | model-form branch | all relevant QoIs | **Future / question-dependent** |
| Dynamic formulation | static vs explicit transient | model-form branch | transient deformation/stress/energy | **Future / question-dependent** |

**Important:** Not every row should become a random variable. Some are better represented as **model alternatives or bounded scenarios**. This is particularly true for segmentation choices, BC formulations, and constitutive model classes.

---

# 13. Proposed roadmap — evaluation and modification

## Original proposed roadmap

> initial deterministic verification → mesh convergence → local sensitivity → global sensitivity → Monte Carlo/LHS → surrogate modeling → Sobol/Morris → active learning if computational cost warrants it

## Literature-supported modified roadmap

### Stage 0 — deterministic verification

**Keep.** Verify the implementation with analytical/benchmark problems and project-specific sanity checks before stochastic analysis. [Henninger et al. 2010]

### Stage 1 — mesh convergence / numerical uncertainty

**Keep and elevate.** Numerical convergence is not merely preparation for UQ; it is its own uncertainty layer. Do not compare parameter-driven ensembles before the baseline numerical solution is stable enough for the intended QoIs.

### Stage 2 — uncertainty inventory + input triage

**Add.** Explicitly classify each possible uncertainty source as parameter, variability, epistemic, model-form, geometry/data, or numerical. Decide whether it should be represented probabilistically, by bounds, or by model scenarios.

### Stage 3 — local sensitivity

**Keep.** Use OAT/local perturbations on the small initial parameter set to confirm output directions, identify obviously inactive variables, and reveal artifact-prone regions.

### Stage 4 — Morris screening if dimensionality is high

**Move before full global UQ when needed.** If the uncertain-input set expands substantially, Morris can screen variables before expensive variance-based analysis. The 2026 mouse study provides strong modern biomechanical precedent. [Valerio & Dall’Ara 2026]

### Stage 5 — LHS/space-filling ensemble for forward propagation

**Keep.** Use LHS to cover the defensible input space efficiently. Keep distributions/scenarios fixed before interpreting the resulting output spread. [McKay et al. 1979]

### Stage 6 — surrogate model, only if FE cost demands it

**Conditional.** Build a GP, PCE, response surface, or other emulator only when direct FE propagation becomes computationally limiting. Validate the surrogate against held-out FE runs.

### Stage 7 — Sobol/global sensitivity

**Keep, but do not place it conceptually after the surrogate as if they were independent stages.** Sobol analysis can use direct FE runs for small problems or a validated surrogate for large problems. Convergence of Sobol estimates must be demonstrated. [Sobol 2001; Baugnon et al. 2026]

### Stage 8 — Monte Carlo propagation

**Keep, but it can share the same sampling infrastructure as Stage 5.** Once the input distributions are established, MC/LHS ensembles can produce output distributions directly. Do not run a second massive ensemble merely to call it “Monte Carlo” if the LHS ensemble already supports the intended estimator.

### Stage 9 — Bayesian calibration

**Make optional and data-dependent.** Add only if the project obtains informative validation/calibration data. It should not be required for forward UQ of a fossil model with no direct experimental calibration target. [Kennedy & O'Hagan 2001]

### Stage 10 — active learning

**Keep as an optional cost-control layer.** Use only if surrogate error or decision-relevant regions justify adaptive resampling.

### Recommended compact workflow

```text
Deterministic verification
        ↓
Mesh convergence / numerical uncertainty
        ↓
Uncertainty taxonomy + defensible ranges/scenarios
        ↓
Local OAT sensitivity
        ↓
Morris screening (only if input count warrants)
        ↓
LHS / space-filling FE ensemble
        ├──→ direct output distributions (MC-style propagation)
        └──→ validated surrogate (GP / PCE / response surface)
                    ↓
               Sobol / global sensitivity
                    ↓
          Adaptive sampling only if needed

Bayesian calibration = separate branch, activated only when informative data exist.
Model-form uncertainty = separate scenario/model ensemble, not automatically folded into one RV.
```

---

# 14. What should be reported for scientifically defensible UALVP 2 UQ?

At minimum:

1. **Every uncertain input:** name, units, baseline value, lower/upper bounds or distribution, source, and rationale.
2. **Dependence structure:** identify correlations or justify independence assumptions.
3. **Model alternatives:** explicitly list discrete branches such as material zonation, BC sets, contact/load-spread models, and constitutive assumptions.
4. **Numerical convergence:** mesh sequence, element counts/characteristic sizes, QoIs tested, convergence criterion, and any local/nonlocal differences.
5. **Sampling design:** random seed, sampler, sample size, replication/independence strategy, and convergence diagnostics.
6. **Sensitivity estimator:** method, estimator definition, confidence/uncertainty of sensitivity indices, and convergence of the indices themselves.
7. **Surrogate validation:** training design, hold-out FE points, prediction error, and failure regions.
8. **QoI definitions:** exact energy definition, apex displacement location/direction, regional stress definition, and treatment of pathological/local peaks.
9. **Numerical vs biological uncertainty:** report separately where possible.
10. **Interpretation scope:** identify which conclusions are robust across the uncertainty envelope and which are scenario-dependent.
11. **Reproducibility:** source geometry hash/version, material table, load/BC definitions, mesh settings, random seeds, and scripts/configuration needed to regenerate the ensemble.

---

# 15. Consensus findings

### C01 — Verification and convergence precede UQ

**Supported:** numerical verification and mesh convergence should be established before attributing output variation to biological/model-input uncertainty. [Henninger et al. 2010]

### C02 — Material properties can strongly affect FE magnitude outputs

**Supported:** cranial validation/sensitivity studies repeatedly identify material-property assumptions as important, especially for absolute strain/stress magnitudes. [Bright & Rayfield 2011; Berthaume et al. 2012]

### C03 — Geometry/segmentation is an independent uncertainty source

**Supported:** CT geometry representation and surface-resolution choices can affect FE outputs; geometry uncertainty should not be conflated with solid-mesh refinement. [Taddei et al. 2006; McCurry et al. 2015; Godinho et al. 2017]

### C04 — Loading and contact assumptions can dominate selected QoIs

**Supported:** fossil and extant cranial studies show sensitivity to load magnitude, direction, bite position, contact distribution, or other loading variables. [Cox et al. 2015; Taylor et al. 2017; Snively & Theodor 2011]

### C05 — Relative/comparative patterns can be more stable than absolute values

**Supported:** validation studies show that simplified models may reproduce broad strain/deformation patterns while missing absolute magnitudes. [Bright & Rayfield 2011; Godinho et al. 2017; Anderson et al. 2012]

### C06 — Global sensitivity is useful when interactions matter

**Supported:** Sobol methods explicitly capture interaction contributions; Morris can screen many variables first. [Morris 1991; Sobol 2001]

### C07 — LHS is a practical FE ensemble design

**Supported:** LHS is an established variance-reduction/space-filling design for expensive computational experiments and is used in craniofacial and recent mandibular FE UQ. [McKay et al. 1979; Berthaume et al. 2012; Baugnon et al. 2026]

### C08 — Surrogates are cost-control tools, not scientific ends

**Supported:** GP/PCE/multi-fidelity approaches can make repeated FE UQ practical, but the surrogate introduces its own approximation uncertainty and must be validated. [Biehler et al. 2015; Römer et al. 2022; Baugnon et al. 2026]

### C09 — Bayesian calibration requires informative data

**Supported:** Bayesian calibration explicitly combines priors with observations and can represent model discrepancy, but it is not a substitute for having informative validation data. [Kennedy & O'Hagan 2001; Ling et al. 2014]

---

# 16. Disagreements, limitations, and unresolved questions

| Question | Current evidence | Status |
|---|---|---|
| Is there a single best UQ taxonomy for fossil FE? | General VVUQ distinguishes aleatory/epistemic/model/numerical uncertainty, but fossil studies often use practical scenario sensitivity instead of formal taxonomy. | **Open / synthesis** |
| Should UALVP 2 treat force magnitude probabilistically? | Could be defensible if the biological force uncertainty can be bounded/characterized; otherwise use scenario ranges. | **Open** |
| Should BCs be random variables? | Often better represented as discrete plausible model branches because they correspond to qualitatively different physical hypotheses. | **Open** |
| Should segmentation be probabilistic? | Plausible geometry ensembles are attractive, but a defensible probability law may be unavailable. | **Open** |
| Is Sobol necessary? | Useful when interaction-aware variance attribution is a scientific goal; unnecessary if the model is low-dimensional and OAT/Morris already answer the question. | **Decision-dependent** |
| Is a surrogate necessary? | Only if direct FE runs become too expensive. | **Decision-dependent** |
| Is Bayesian calibration necessary? | Not without informative calibration data. | **No — unless data acquisition changes** |
| Is active learning necessary? | Only if surrogate error/cost warrants it. | **Decision-dependent** |
| Can model-form uncertainty be folded into one continuous UQ distribution? | Not cleanly; doing so can obscure which physical assumption caused differences. | **Discouraged** |
| Are local peak stresses suitable primary QoIs? | They are likely sensitive to mesh, geometry and boundary artifacts; global/regionally aggregated measures are generally more defensible. | **Strong caution** |

---

# 17. Concrete implications for the UALVP 2 program

| Literature-derived issue | Current Phase 4 FEM | Mesh convergence | Geometry pipeline | Load cases | Material assumptions | Future UQ | Interpretation |
|---|---|---|---|---|---|---|---|
| Numerical convergence | **Required** | Primary | — | — | — | Baseline for all UQ | Do not attribute numerical drift to biology |
| Material property uncertainty | Baseline assumption must be documented | — | CT/material map provenance | — | **High priority** | E, ν, zonation | Distinguish magnitude uncertainty from pattern robustness |
| Force magnitude | Keep deterministic baseline | — | — | **High** | — | Continuous propagation | Report normalized and physical-force outputs separately |
| Force direction/contact | Scenario-based | — | — | **High** | — | Angular/contact ensemble | Important because local and regional response may change differently |
| BC uncertainty | Explicit current model | Maybe artifact-zone diagnostics | — | **High** | — | Scenario ensemble | Mask/flag stress near rigid constraints |
| Segmentation/surface repair | Frozen baseline | Separate from h-refinement | **High** | — | — | Geometry ensemble | Prevent geometry and mesh uncertainty from being conflated |
| Model-form uncertainty | Linear/static baseline | — | — | — | — | Nonlinear/contact/dynamic branches | Do not claim linear FE answers the full impact problem |
| Output definition | Energy/apex displacement/stress summaries | Use all in convergence | — | — | — | Propagate all primary QoIs | Avoid single-number peak stress as sole endpoint |
| Sensitivity workflow | — | — | — | — | — | OAT → Morris (if needed) → LHS/MC → Sobol/surrogate | Method should follow parameter dimension/cost |
| Surrogate/active learning | — | — | — | — | — | Conditional | Verify emulator before using it to infer global sensitivity |
| Bayesian UQ | — | — | — | — | — | Conditional on data | Not required for initial forward UQ |

---

# 18. Candidate contribution claims — `TO VERIFY`

These are candidate contribution statements, **not novelty claims**:

1. **TO VERIFY:** a fossil-cranial FE workflow that explicitly separates numerical, geometry, material, load/BC, and model-form uncertainty rather than treating all uncertainty as parameter noise.
2. **TO VERIFY:** a UALVP 2 uncertainty workflow that keeps mesh convergence outside the biological parameter distribution and reports numerical convergence independently.
3. **TO VERIFY:** a staged fossil UQ workflow in which Morris/LHS/Sobol/surrogate methods are selected according to input dimension and FE cost rather than applied as a fixed recipe.
4. **TO VERIFY:** explicit convergence testing of global sensitivity estimates and surrogate predictions as first-class numerical results in a fossil FE study.

These require an exhaustive fossil-specific forward-citation search before being stated publicly as novel.

---

# 19. Bottom-line recommendation for Phase 5

The evidence supports the project **continuing with a staged, economical UQ strategy** rather than jumping directly to the most sophisticated methods.

### Recommended Phase 5A — screening

- Start from the verified, mesh-converged deterministic baseline.
- Run local OAT sensitivity on E, ν, force magnitude, force direction, and a small set of BC/contact variants.
- If the input set grows substantially, use Morris screening.

### Recommended Phase 5B — probabilistic propagation

- Define defensible ranges/distributions with explicit provenance.
- Use LHS for a space-filling ensemble.
- Propagate to energy, apex displacement, and regional stress metrics.
- Track local stress separately because it may have different convergence behavior.

### Recommended Phase 5C — global sensitivity

- For a manageable number of uncertain variables, compute Sobol indices directly from a suitable design.
- If FE cost is high, build and validate a GP/PCE/response-surface surrogate first and compute Sobol indices on the validated emulator.
- Demonstrate sensitivity-index convergence.

### Recommended Phase 5D — advanced UQ only when justified

- Add active learning when surrogate error or computational cost demonstrates a need.
- Add Bayesian calibration only when informative data exist.
- Add model-discrepancy quantification only in a validation setting where the discrepancy can be informed empirically.

**Key methodological conclusion:** the most defensible UALVP 2 UQ study is not necessarily the one with the most algorithms. It is the one that makes the uncertainty taxonomy explicit, uses evidence-backed input ranges/scenarios, demonstrates numerical convergence, validates any surrogate, and reports which scientific conclusions remain stable across the uncertainty envelope.

---

# 20. Reference links / stable identifiers

1. McKay et al. 1979 — https://doi.org/10.1080/00401706.1979.10489755
2. Morris 1991 — https://doi.org/10.1080/00401706.1991.10484804
3. Sobol 2001 — https://doi.org/10.1016/S0378-4754(00)00270-6
4. Saltelli et al. 2008 — https://doi.org/10.1111/j.1751-5823.2008.00062_17.x (review record for the book)
5. Henninger et al. 2010 — https://doi.org/10.1243/09544119JEIM649
6. Laz & Browne 2010 — https://doi.org/10.1243/09544119JEIM739
7. Kennedy & O'Hagan 2001 — https://doi.org/10.1111/1467-9868.00294
8. Roy & Oberkampf 2011 — https://doi.org/10.1016/j.cma.2011.03.016
9. Ling et al. 2014 — https://doi.org/10.1016/j.jcp.2014.08.005
10. Taddei et al. 2006 — https://doi.org/10.1109/TBME.2006.879473
11. Bright & Rayfield 2011 — https://doi.org/10.1111/j.1469-7580.2011.01408.x
12. Berthaume et al. 2012 — https://doi.org/10.1016/j.jtbi.2012.01.031
13. Kerr et al. 2011 — https://doi.org/10.1016/j.jbiomech.2011.03.008
14. Biehler et al. 2015 — https://doi.org/10.1007/s10237-014-0618-0
15. Römer et al. 2022 — https://doi.org/10.1002/cnm.3575
16. Rupp et al. 2020 — https://doi.org/10.22489/CinC.2020.275
17. Razu et al. 2023 — https://doi.org/10.1115/1.4056968
18. Kote et al. 2026 — https://doi.org/10.1007/s10439-024-03571-4
19. Baugnon et al. 2026 — https://doi.org/10.1088/1873-4030/ae995b
20. Valerio & Dall'Ara 2026 — https://doi.org/10.1016/j.jbiomech.2026.113377
21. Snively & Theodor 2011 — https://doi.org/10.1371/journal.pone.0021422
22. Cox et al. 2015 — https://doi.org/10.1111/joa.12282
23. Taylor et al. 2017 — https://doi.org/10.1002/ar.23489
24. McCurry et al. 2015 — https://doi.org/10.7717/peerj.988
25. Godinho et al. 2017 — https://doi.org/10.1016/j.crpv.2016.11.002
26. Jannel et al. 2022 — https://doi.org/10.1126/sciadv.abm8280
27. Sylvester & Kramer 2018 — https://doi.org/10.1002/ar.23796
28. Anderson et al. 2012 — https://doi.org/10.1098/rsbl.2011.0674

---

# 21. Review limitations

- This is a scoping evidence module, not a formal PRISMA systematic review.
- Citation chasing was targeted rather than exhaustive across every branch of the biomechanics literature.
- Some primary papers were available only through abstracts or publisher metadata during this pass; those entries are explicitly marked for additional extraction where necessary.
- The fossil-specific literature is especially heterogeneous: many studies use sensitivity analysis but do not frame the work using modern UQ terminology.
- Recent 2026 literature was included because the current date is 2026-09-23; these sources may not yet have accumulated broad follow-on literature.
- Absence of a paper from this module is not evidence that no such paper exists; novelty claims remain `TO VERIFY`.

# Literature → Model Decisions: Canonical Bridge Specification

**Document Role**: Scientific Requirements & Canonical Bridge Specification  
**Status**: ACTIVE STANDARD (Model Decision Basis v1)  
**Prepared**: 2026-09-24  
**Literature Baseline**: Commit `2662be0` (Literature Basis v1)  
**Specimen**: *Stegoceras validum* UALVP 2  
**Target Codebase**: `src/stegoceras_biomechanics/fea/`, `models/`, `simulations/`, `PLAN.md`  
**Purpose**: Translate the frozen evidence base into explicit computational decisions and experimental gates.  

---

1. What this document is for

The literature synthesis answers scientific questions; the code and data answer computational questions. A bridge is needed so that a literature statement cannot silently become a model assumption.

This document therefore uses a stricter chain:

Evidence → permitted model representation → discriminating test → interpretation limit

The bridge is intentionally not a literature review and not a full Phase 5 UQ design. It is a decision specification for deciding what the next model should contain, what must be measured or verified before adding complexity, and what claims remain out of scope.

The central rule is:

A literature observation earns representation in the model only when the representation is explicit, auditable, and accompanied by a test that could show the representation matters. Each decision below is also assigned a status and, where applicable, a failure/branch condition so that unresolved evidence produces an explicit next path rather than an implicit assumption.

2. Epistemic rules

The frozen synthesis distinguishes direct observation/report (DO), author interpretation (AI), model assumption (MA), inference (IN), synthesis (SYN), and unresolved/unchecked material. This document adds an operational rule to that distinction:

Observed anatomy may define geometry or regions. It does not automatically define mechanical properties.

A published model input is a benchmark input, not a biological measurement.

Continuous distributions require evidence for the distribution. A plausible range alone is a sensitivity envelope, not a probability law.

Discrete model-form choices remain scenarios. Homogeneous vs. zonated material, rigid vs. alternative BCs, and static vs. dynamic formulations should not be blurred into one scalar random-variable framework.

Numerical discretization is not biological uncertainty. Mesh-to-mesh differences are reported as output-specific numerical discrepancy unless a formal error estimator justifies stronger language.

No specimen-specific physical validation exists for UALVP 2. Solver correctness, equilibrium, benchmark reproduction, or mesh stabilization must not be called biological validation.

Mechanical capability is not behavioral observation. A model can establish conditional mechanical response without establishing that an animal performed a particular behavior or that the structure evolved for that behavior.

3. The current model that this bridge must interrogate

The repository currently freezes a homogeneous linear-elastic Model A on a canonical UALVP 2 surface. The current configuration uses $E=17$ GPa, $\nu=0.30$, a 1,000 N downward load over an approximately 3,000 mm² dorsal patch, rigid translational fixation at the occipital condyle, and translational restraint at the nuchal crest. The Phase 4 mesh ladder is pure volumetric refinement on a fixed surface.

The current results show a useful split in numerical behavior: total strain energy, apex displacement, and dorsal-dome stress summaries are comparatively stable, whereas global and endocranial/braincase 95th-percentile stress remain materially mesh-sensitive. That means the next scientific problem is not simply "run more meshes" or "sample more inputs"; it is to determine whether the internal biological model itself changes the conclusions.

Repository baseline/configuration: models/phase4/baseline.yaml
Repository current-state record: docs/CURRENT_STATE.md

4. Decision register

D01 — Treat UALVP 2 as a specimen-specific benchmark, not a generic skull

Status: established

Evidence

UALVP 2 is directly represented in the published Stegoceras FE literature, making it possible to compare a new pipeline against a specimen-specific prior model rather than an idealized generic dome.

Model decision

Keep UALVP 2 as the fixed reference specimen for the near-term computational program. Preserve specimen, CT, geometry, and processing provenance as separate objects.

Required action

Build a provenance record connecting the DICOM volume, surface reconstruction, canonical surface, FE-ready geometry, and every subsequent material/load model.

Discriminating test

Determine whether the current project volume/geometry is physically registered to the dataset underlying the 2011 model closely enough that differences can be attributed to modeling choices rather than specimen/data mismatch.

Interpretation limit

Do not use UALVP 2 as a proxy for every ontogenetic stage or every Stegoceras individual.

Failure / branch condition

If a proposed conclusion requires population-level or ontogenetic inference, the project must explicitly add evidence and models for that broader target rather than extrapolating from UALVP 2.

D02 — Resolve CT scale and coordinate registration before treating geometry as quantitative

Evidence

The current project has an explicit scale assumption in its Phase 4 model configuration, while the literature emphasizes that CT acquisition and surface processing propagate into FE geometry.

Status: required_gate

Model decision

The physical scale relationship between the DICOM grid and the canonical surface becomes a Phase 5 data-validation gate, not a permanently adjustable uncertainty parameter. Resolve arbitrary global scale uncertainty arising from an unknown CT-to-surface unit relationship while retaining independently justified geometric uncertainties from segmentation, reconstruction, repair, or taphonomic distortion.

Required action

Register the CT voxel grid to the canonical surface and document voxel spacing, orientation, origin/affine information, and registration residuals.

Discriminating test

Quantify landmark or surface correspondence at multiple anatomical locations. Report the residual rather than merely stating that the datasets "align."

Interpretation limit

Do not carry an arbitrary ±5% geometric scale distribution after the scan-to-surface relationship has been directly established. Registration does not eliminate all geometric uncertainty.

Failure / branch condition

If the CT-to-surface correspondence is poor, do not immediately absorb the residual into a generic scale distribution. First determine whether the mismatch arises from provenance, segmentation, reconstruction, deformation, or registration error; only then define any remaining uncertainty explicitly.

D03 — Freeze the outer geometry during material-model comparison

Status: planned_experiment

Evidence

Surface representation, segmentation, smoothing, repair, and FE discretization can each change model outputs. The literature requires these effects to be distinguished rather than combined.

Model decision

The decisive material A/B experiment must hold the outer FE-ready geometry, mesh topology, load definition, and BC definition fixed.

Required action

If internal material zoning can be assigned directly to existing elements, prefer that implementation. If volumetric remeshing becomes necessary, treat the remeshing change as a separate confound and do not call the result a pure material A/B experiment.

Discriminating test

Verify node/element correspondence or provide an explicit mapping showing that the only intended change is material assignment.

Interpretation limit

An A/B result contaminated by simultaneous geometry or mesh changes cannot identify the effect of material architecture alone.

Failure / branch condition

If material assignment cannot be changed on the same FE mesh, create matched meshes and treat the mesh change as a separate numerical sensitivity experiment before interpreting the material comparison.

D04 — Represent the observed internal architecture before attempting CT-to-modulus mapping

Status: planned_experiment

Evidence

The frozen synthesis identifies compact superficial/deep layers, a lower-density/trabecular region, a dense basicranial region, and neurovascular canal architecture. This structural heterogeneity is an observation; the living constitutive properties are not directly measured.

Model decision

Build a simple anatomy-informed zonated model before attempting voxelwise $E(x)$. Keep the following hierarchy explicit:

observed anatomy / histology
        ↓
mechanically meaningful region hypothesis
        ↓
engineering material assignment

An observed or histological region is not itself an engineering property assignment.

Initial representation

A first heterogeneous model should distinguish the major mechanically meaningful zones supported by the evidence, while treating unresolved microscopic canals as architectural context unless the scan genuinely resolves them at a scale appropriate for continuum FE.

Required action

Create explicit zone definitions, segmentation provenance, interface rules, and a machine-readable element-to-zone map.

Discriminating test

Compare Model A (homogeneous) against Model B (zoned) under otherwise identical conditions.

Interpretation limit

The existence of internal architecture does not by itself establish its mechanical function or evolutionary purpose. A region label does not imply a particular modulus, strength, anisotropy, or constitutive law.

Failure / branch condition

If anatomy or histology supports a region but no defensible engineering assignment can be made, preserve the region as structural evidence and do not force a numerical property into the model.

D05 — Treat CT intensity as evidence about architecture, not as a direct modulus measurement

Status: required_gate

Evidence

The 2011 UALVP 2 work explicitly recognized permineralization and beam-hardening problems. The literature synthesis therefore rejects automatic clinical HU-to-stiffness transfer for this fossil.

Model decision

Characterize the DICOM intensity field first; do not implement an unverified voxelwise density-to-$E$ calibration.

Required action

Record pixel representation, intensity range, orientation, beam-hardening patterns, matrix/bone contrast, saturation/truncation behavior, and the spatial visibility of internal architecture.

Discriminating test

Determine whether intensity differences track anatomical regions consistently enough to support a defensible discrete classification. If quantitative CT-to-property calibration is not defensible, retain morphology/histology-informed zoning and use CT intensity as corroborating structural evidence rather than constitutive calibration.

Interpretation limit

CT-informed classification is not equivalent to measurement of fossilized or living elastic modulus.

Failure / branch condition

If intensity cannot reproducibly distinguish the proposed regions, do not force CT-derived material distinctions. If anatomy is supported but property calibration is not, retain the morphology-informed zoning branch; if neither is reproducible, keep Model A as the control and report the unresolved architecture explicitly.

D06 — Keep the 17 GPa homogeneous value as a control parameter

Status: established

Evidence

The synthesis explicitly classifies the homogeneous $E=17$ GPa, $\nu=0.30$ model as a project baseline used to isolate geometric and numerical effects. It is not a UALVP 2 specimen measurement.

Model decision

Retain Model A as the control arm. Do not silently replace it with a "better" material value merely because internal architecture is known.

Required action

Use the same Model A for regression/verification comparisons after Model B is introduced.

Discriminating test

Quantify how much each chosen QoI changes when moving A → B.

Interpretation limit

A change relative to 17 GPa establishes model sensitivity; it does not establish that either model is biologically exact.

D07 — Use literature material ranges as sensitivity envelopes, not probability distributions

Status: required_gate

Evidence

The synthesis identifies broad vertebrate constitutive ranges, but no specimen-specific probability law for fossil UALVP 2 material properties.

Model decision

For early material analysis, use bounded deterministic scenarios and/or one-at-a-time sensitivity around explicit nominal values. Do not assign arbitrary probability densities to $E$ or $\nu$.

Required action

Separate at least: (a) homogeneous compact-bone control; (b) anatomy-informed zonation; (c) bounded material sensitivity within defensible literature envelopes.

Discriminating test

Identify which QoIs actually move enough to justify adding probabilistic propagation later.

Interpretation limit

A plausible interval answers "what happens across this assumption envelope?" It does not answer "what is the probability that the fossil had this value?"

D08 — Treat 1,360 N as a benchmark scenario, not a measured impact force

Status: established

Evidence

Snively & Theodor's 1,360 N UALVP 2 force is a modeled benchmark derived from assumed animal mass, closing speed, and deceleration distance. The frozen synthesis explicitly rejects treating it as an empirically measured living impact force.

Model decision

Retain the published 1,360 N case as a reproducibility benchmark. Retain the current 1,000 N project case as a separate computational baseline.

Required action

Document exactly which quantity is being benchmarked: total force, spatial load distribution, direction, contact area, and support conditions.

Discriminating test

Reconstruct the published benchmark logic to the extent current data permit and identify every mismatch.

Interpretation limit

Neither 1,000 N nor 1,360 N should be described as "the" biological impact force.

Failure / branch condition

If a downstream analysis treats force magnitude as uncertain, keep the force scenario separate from behavioral interpretation and exploit analytical scaling while the linear assumptions remain valid.

D09 — Do not spend FE solves sampling force magnitude when the current model is linear

Status: established

Evidence

The current baseline is small-displacement linear elasticity with fixed stiffness and fixed load/contact geometry. In such a model, force scaling is analytical.

Model decision

For a fixed model and load pattern, use analytical scaling rather than repeated FE solves over force magnitude.

Scaling rule

For $F_2=kF_1$ under the same linear model:

$$
u_2=k u_1, \qquad \sigma_2=k\sigma_1, \qquad U_2=k^2U_1.
$$

Required action

Reserve actual FE solves for changes in load direction, contact geometry, support, material architecture, or constitutive law.

Interpretation limit

This shortcut applies only while the stated linear model assumptions hold. It does not remove uncertainty in the biological force itself.

D10 — Treat contact geometry as a scenario family, not a single behavioral truth

Status: planned_experiment

Evidence

The prior literature varied load area, and recent synthesis emphasizes that extant "head-striking" behaviors differ substantially in surface, direction, and kinematics.

Model decision

Represent contact patch size, orientation, and distribution as explicit model scenarios. The existing 3,000 mm² patch is a project assumption/benchmark, not a measured biological contact area distribution.

Required action

Hold total force fixed initially while varying only contact geometry and/or direction to isolate load-placement effects.

Discriminating test

Determine whether regional braincase/dome QoIs are stable across a small, mechanistically motivated family of load placements.

Interpretation limit

A load case should be labeled by its modeled geometry (for example, dorsal distributed compression) rather than by a claimed behavior such as "the headbutt."

Failure / branch condition

If a load placement materially changes the conclusion, retain multiple scenario labels rather than selecting the scenario that best supports a preferred biological narrative.

D11 — Keep current rigid constraints as a benchmark, then audit boundary-condition sensitivity

Status: planned_experiment

Evidence

The 2011 model used occipital and nuchal constraints and reported artificial local stress near constraints. Cranial BCs are known to affect FE results.

Model decision

Preserve the current BCs as the reproducibility/control case. Introduce alternatives as discrete model-form scenarios rather than a continuous random field.

Required action

Generate a spatial mask of constrained and load-application regions. Report primary QoIs both with and without artifact-prone local regions when scientifically appropriate.

Discriminating test

Change only the BC formulation and quantify the effect on the predefined QoIs.

Interpretation limit

A local stress hotspot adjacent to a hard constraint cannot be interpreted as a biological hotspot without a BC-sensitivity check.

D12 — Define convergence by output, not by element count

Status: required_gate

Evidence

Mesh studies show that different QoIs converge at different rates. The present Phase 4 results already demonstrate stabilization of some global/dome quantities alongside persistent braincase-stress sensitivity.

Model decision

Track convergence separately for at least: strain energy, apex displacement, dome stress summary, braincase stress summary, and any spatially defined comparison metric that will be used in the paper.

Required action

Freeze geometry, element formulation, materials, loads, BCs, and solver settings during the convergence series.

Discriminating test

Report stepwise changes and stopping criteria per QoI. Do not collapse the outcome to a single "converged mesh" statement.

Interpretation limit

The existing finite-mesh difference should remain a numerical discretization discrepancy; it must not automatically become a biological UQ distribution.

D13 — Choose primary outputs that support comparative inference

Status: provisional

Evidence

Validation literature shows that broad patterns/comparative trends can be more stable than local absolute magnitudes, while pointwise maxima are especially vulnerable to singularities, constraints, and mesh effects.

Model decision

Prioritize regionally defined and comparative outputs over unconstrained global maxima.

Primary QoIs

Total strain energy.

Apex displacement.

Dorsal-dome regional stress summary.

Endocranial/braincase-roof regional stress summary.

A predeclared attenuation/comparison metric relating dome response to braincase response, where mathematically appropriate; the exact metric remains provisional until its numerical stability and scientific interpretation are established.

Spatial pattern maps with constraint/load artifact regions explicitly marked.

Required action

Freeze the QoI definitions before the A/B experiment so that output selection does not follow the result.

Interpretation limit

Do not convert one local peak stress into a behavioral or evolutionary verdict.

D14 — Separate numerical verification, benchmark reproduction, and biological validation

Status: established

Evidence

The literature synthesis explicitly distinguishes code/analytical verification, mesh/discretization analysis, reproduction of earlier FE models, and physical validation against experimental data.

Model decision

The project should report four separate labels rather than a single generic "validated" status.

Required action

Maintain separate records for: (1) analytical/solver verification; (2) numerical convergence; (3) prior-study benchmark reproduction; and (4) physical validation, with (4) currently marked unavailable for UALVP 2.

Interpretation limit

A model can be computationally verified and still lack specimen-specific biological validation.

Failure / branch condition

If a claim would require physical validation that does not exist, downgrade the claim to computational/model-comparison language rather than substituting solver checks for biological validation.

D15 — Make Model A vs. Model B the first scientific contrast after CT characterization

Status: planned_experiment

Evidence

The literature establishes internal architectural heterogeneity in UALVP 2 but leaves its constitutive consequences unresolved. This creates a direct testable question.

Model decision

The first biological-model experiment should be:

Does evidence-based internal material architecture materially alter the mechanical conclusions obtained from the homogeneous control?

Required action

Use the same outer geometry, mesh, force resultant, load footprint, and BCs. Change only the material-region assignment.

Decision criteria

Predefine the effect metrics and decision criteria for the selected QoIs before running the comparison. Interpret the magnitude of A→B differences relative to numerical discretization discrepancy and other established uncertainty scales rather than imposing a universal percentage threshold.

Interpretation limit

A small A/B difference would show robustness to this specific architectural refinement. A large difference would show model-form importance. Neither result alone determines the biological function of the dome.

Failure / branch condition

If A and B cannot be compared without changing geometry, mesh, loading, or BCs, pause the biological interpretation and redesign the comparison so those confounds are either fixed or separately quantified.

D16 — Defer full probabilistic UQ until the uncertainty inventory is reduced

Status: required_gate

Evidence

The literature supports a staged workflow: verification → convergence → uncertainty classification → local sensitivity → screening if needed → propagation/global sensitivity as warranted. Recent studies also show that stable global sensitivity indices can require substantial sample sizes and depend on the QoI.

Model decision

Do not lock in an arbitrary LHS size, Sobol budget, or surrogate architecture before the model-form and data questions have been interrogated.

Required action

After the A/B and focused load/BC/material tests, count the remaining genuinely uncertain continuous inputs and estimate the cost of a single trustworthy solve.

Discriminating test

Use OAT first. Use Morris only if the continuous input set becomes large enough that screening has value. Use LHS/MC/Sobol only after input ranges/distributions and QoIs are justified.

Interpretation limit

A larger sample size is not inherently more scientifically rigorous if the input distributions or model forms are not defensible.

Failure / branch condition

If the uncertainty inventory reduces to a small number of well-characterized inputs, use the simplest defensible analysis. If it expands substantially, document why screening or probabilistic propagation is required before selecting the computational design.

D17 — Treat dynamic/nonlinear contact as a separate model-form project

Status: deferred

Evidence

The existing FE formulation is linear static. The literature recognizes that real collision mechanics can be transient and nonlinear, but also that the current biological inputs do not uniquely constrain such a model.

Model decision

Do not present dynamic/contact FEA as a routine refinement of the current model. Activate it only for a specific biological question that the static model cannot answer.

Required action

Document the new physics, new inputs, and new validation requirements before opening that branch.

Interpretation limit

A dynamic model would answer a different question; it should not retrospectively erase limitations of the static benchmark.

Failure / branch condition

If a project question can be answered within the current static framework, keep the dynamic/nonlinear branch deferred. If the static model is demonstrably incapable of answering the question, open a separate model-form specification with its own inputs, verification, and validation gates.

5. Phase 5 experimental sequence derived from the decisions

Gate A — Acquire and preserve the volume

Deliverables

Immutable DICOM archive.

File inventory and cryptographic checksums.

DICOM header extraction.

Explicit voxel spacing, image orientation, coordinate transform, and pixel-value interpretation.

Provenance linking the volume to the specimen and current surface model.

Gate to continue: the volume can be reconstructed deterministically and its physical coordinate system is known.

Gate B — Establish CT-to-surface registration

Deliverables

Anatomical landmarks used for registration.

Transformation matrix.

Registration residuals.

Statement of whether the canonical outer surface is an appropriate boundary derived from the same scan.

Gate to continue: scale/coordinate mismatch is either resolved or explicitly quantified and handled as a defined model change.

Gate C — Characterize image semantics before segmentation

Questions

What exactly do the stored voxel values represent?

What is the observed intensity range and dynamic range?

Where are beam-hardening or reconstruction artifacts visible?

Can matrix, compact bone, lower-density/trabecular regions, and major internal structures be distinguished reproducibly?

Which internal features are actually resolved at the scan's spatial scale?

Gate to continue: an auditable statement exists about what the CT can and cannot justify.

Gate D — Reconstruct the published material-inference logic

This is not a demand to copy the 2011 model. The goal is to separate:

information directly visible in the scan;

thresholds or masks selected by the authors;

material values imported from other literature;

model-specific assumptions;

and places where the published workflow is not reproducible from the available data.

Gate to continue: every Model B input has a declared evidence class.

Gate E — Build Model B

Minimum intended structure

Outer compact/cortical-like region.

Lower-density/trabecular region.

Dense basicranial/support region where defensible.

Explicit treatment of major canals/cavities according to the resolution actually available.

Model B should be deliberately simple. Complexity that cannot be traced to evidence is postponed.

Gate to continue: the same benchmark load, BCs, and fixed outer geometry can be applied to A and B.

Gate F — Execute the decisive A/B experiment

Run A and B using identical:

canonical outer geometry;

FE mesh topology;

load resultant and footprint;

boundary conditions;

solver tolerances;

output definitions.

The scientific comparison is the difference in the predefined QoIs, not which model produces a more visually complicated stress field.

Gate G — Only then branch into focused sensitivity/model-form experiments

Recommended first branches:

Load direction/contact placement.

Material magnitude within explicit non-probabilistic bounds.

Boundary-condition alternatives.

Segmentation/repair alternatives in demonstrably ambiguous internal regions.

Only after those effects are characterized should the project decide whether a probabilistic UQ campaign is justified.

6. What should not happen next

The following actions are explicitly deferred by this bridge:

A precommitted 48-point LHS or any other arbitrary sample count.

A probability distribution for fossil $E$ or $\nu$ without empirical justification.

A probability distribution for contact area merely because a range such as 2,500–4,000 mm² has been chosen as a sensitivity envelope.

A claim that 17 GPa is a measured UALVP 2 property.

Automatic conversion of CT intensity to elastic modulus.

Treating the current mesh discrepancy as a biological uncertainty distribution.

Declaring the UALVP 2 model "validated" from numerical equilibrium or mesh stabilization alone.

Interpreting the 1,000 N project load or 1,360 N literature benchmark as the historical impact force.

Treating "headbutting" as one uniquely defined force direction/contact geometry.

Launching dynamic/contact FEA before a specific question requires it.

Using FE outputs alone to decide the evolutionary function of the dome.

7. Suggested machine-readable decision schema

The project can represent each future modeling choice with a small record like:

id: D15
claim_class: observed_architecture
literature_basis:
  - BIO-05
  - BIO-07
  - BIO-13
model_change:
  from: Model_A_homogeneous
  to: Model_B_zoned
continuous_parameter: false
scenario_type: model_form
status: planned_experiment
required_data:
  - DICOM_characterization
  - zone_definition
  - element_zone_map
paired_control: Model_A
primary_qois:
  - strain_energy
  - apex_displacement
  - dome_regional_stress
  - braincase_regional_stress
interpretation_limit: "Mechanical model response only; not direct evidence of behavior or evolutionary function."
failure_branch: "If A/B cannot be isolated to material assignment, redesign the comparison before interpreting the result."

The important property is not the exact YAML syntax. It is that a future model input should always be traceable to: why it exists, what evidence supports it, how it will be tested, and what the result is allowed to mean.

8. Decision gates for the research program

Gate 1 — Data gate

Do not make a CT-derived material decision until the volume's semantics, scale, orientation, and artifacts are characterized.

Gate 2 — Representation gate

Do not implement voxelwise material mapping until discrete architecture can be extracted reproducibly and the CT-to-property problem is separately justified.

Gate 3 — Model-form gate

Do not start broad UQ until the homogeneous-versus-zoned comparison has established whether internal architecture materially affects the selected QoIs.

Gate 4 — Uncertainty gate

Do not assign probability distributions until each uncertain quantity has a scientific reason to be represented probabilistically. Keep model-form alternatives discrete.

Gate 5 — Interpretation gate

Do not turn mechanical output into a behavioral or evolutionary claim unless the required biological evidence exists outside the FE calculation.

9. Minimal publication-grade audit trail

Before the project leaves the deterministic/material-characterization stage, the repository should contain:

immutable source DICOM + manifest;

CT metadata extraction;

CT-to-surface registration record;

segmentation/repair provenance;

Model A configuration frozen;

Model B region definition + mapping;

benchmark reconstruction notes for the 2011 UALVP 2 study;

deterministic verification results;

output-specific mesh-convergence records;

A/B comparison table;

artifact masks for loads and constraints;

explicit list of interpretation claims that remain unsupported.

10. Source basis

This document was independently derived from the following project materials and does not use the legacy agent draft (now archived at docs/archive/2026-09-24_literature_to_model_decisions_v1_legacy.md) as its conceptual source:

Literature Basis v1: literature/stegoceras_biomechanics_literature_synthesis.md at commit 2662be0.

Current computational baseline: models/phase4/baseline.yaml on main.

Current scientific state: docs/CURRENT_STATE.md on main.

Repository overview: README.md on main.

The review memo supplied with this task, which identifies 2662be0 as the stopping point for the literature-review loop and calls for a literature-to-model bridge followed by UALVP 2 CT/material characterization.

Key literature claims carried into the bridge

UALVP 2 was modeled directly in the 2011 Stegoceras FE study and is therefore an unusually useful specimen-specific benchmark.

UALVP 2 has heterogeneous internal architecture visible in CT/histological evidence.

The 2011 study did not treat fossil CT intensity as a simple direct living-bone stiffness measurement because of permineralization and beam hardening.

The 2011 1,360 N force is a modeled benchmark scenario, not a measured impact force.

Cranial FE outputs depend on geometry, materials, loading, BCs, and numerical resolution.

Mesh convergence is numerical verification, not biological validation.

Model-form uncertainty and discretization discrepancy should not be collapsed into one probability distribution.

Sensitivity/UQ should be staged and justified by the actual remaining uncertain inputs and computational cost.

11. Bottom line

The immediate scientific question is narrower than the project's eventual UQ ambition:

Once the actual UALVP 2 CT data are characterized, does an evidence-based internal material architecture change the mechanical conclusions of the homogeneous control enough to justify treating material model form as a first-order source of uncertainty?

That question is experimentally tractable with the existing pipeline. It also creates a clean decision point for everything downstream: load/contact sensitivity, BC scenarios, probabilistic propagation, surrogate modeling, and—only if scientifically required—a dynamic/nonlinear branch.

Until that decision is made, the appropriate output is not a large uncertainty ensemble. It is a traceable data characterization, a reproducible material inference, and a controlled A/B mechanical test.
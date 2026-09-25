# Phase 3 Design (Retrospective Reconstruction): Published Model Audit & Provisional Benchmark Specification

> [!NOTE]
> **Retrospective Reconstruction**: This document reconstructs the scientific design intent for Phase 3 based on contemporaneous milestone artifacts, commits `79c8cb6`, `925809c`, and `255ee46`, [`reports/phase3_recommended_benchmark.md`](../../reports/phase3_recommended_benchmark.md), [`reports/snively_theodor_model_reconstruction.md`](../../reports/snively_theodor_model_reconstruction.md), and Decisions `D001`–`D002`. It was codified during the Research Design & Traceability Milestone to preserve design intent without rewriting history.

**Document Role**: Retrospectively Reconstructed Phase Design  
**Status**: RETROSPECTIVELY RECONSTRUCTED & FROZEN  
**Governing Standard**: Phase 3 Milestone Specification / Decisions `D001`, `D002`  
**Specimen**: *Stegoceras validum* UALVP 2  
**Target Architecture**: Model A (Minimal Surface-Derived Homogeneous-Material Approximation)  

---

## 1. Scientific Question
*What are the empirically grounded model parameters, boundary conditions, loading scenarios, and validation targets for a minimal surface-derived finite element benchmark of Stegoceras validum (UALVP 2) inspired by Snively & Theodor (2011), and how can verifiable linear structural compliance be separated from unverified biological impact assumptions?*

Specifically:
1. Which parameters from Snively & Theodor (2011) are directly documented from empirical specimen measurements versus inferred, calibrated, or assumed?
2. Can a simplified, surface-derived homogeneous model (Model A) provide a meaningful biomechanical baseline before introducing complex internal material heterogeneity?
3. How should validation be structured when exact numerical replication of a heterogeneous CT model is unattainable with a surface mesh?

---

## 2. Motivation / Prior Evidence
- **Published Benchmark**: Snively & Theodor (2011) *PLoS ONE* 6(6): e21412 published 2D and 3D FEA simulations of dome impact in *Stegoceras validum* (specimen UALVP 2), reporting peak von Mises stresses of $\approx 3\text{--}8\text{ MPa}$ under broad apex loading and localized stress concentrations of $\approx 30\text{--}60\text{ MPa}$ under concentrated loading, with endocranial roof stresses $< 5\text{ MPa}$.
- **Phase 1 & 2 Discoveries**: Phase 1 verified UALVP 2 mesh assets on MorphoSource. Phase 2 demonstrated that the 32 articulated cranial elements and whole-skull composite share a common coordinate system and scale, but revealed that the raw CT volume was not deposited with the surface meshes.
- **Problem**: Attempting to build a multi-zoned heterogeneous model directly from surface meshes risks fabricating internal boundaries. A rigorous audit of published inputs and an uncompromised homogeneous baseline are required first.

---

## 3. Hypothesis or Competing Expectations
- **Hypothesis A (Qualitative Robustness of Dome Geometry)**: The gross mechanical protection of the braincase and steep stress attenuation from the dome apex into the cranial vault are primarily governed by the global external dome geometry and will emerge even in a simplified homogeneous-material baseline (Model A).
- **Hypothesis B (Heterogeneity-Dominated Behavior)**: Stress dissipation and braincase protection require internal histological zonation (cancellous core absorbing energy); a homogeneous baseline will fail to shield the endocranial cavity or will exhibit fundamentally inverted stress distributions.

---

## 4. Scope
- **In Scope**:
  - Comprehensive 8-stage dependency audit of the Snively & Theodor (2011) computational pipeline.
  - Construction of an explicit input parameter matrix classifying every parameter by epistemic tier (Direct Empirical, Derived, Literature Inferred, Arbitrary Assumption).
  - Formulation of Model A benchmark specification (geometry, loading, boundary constraints, constitutive properties).
  - Definition of a three-tier validation hierarchy.
- **Explicitly Out of Scope**:
  - 3D solid mesh generation and FEA solver execution (deferred to Phase 4).
  - Micro-CT internal zonation extraction (deferred to Phase 5).
  - Non-linear contact mechanics or dynamic explicit transient impact.

---

## 5. Experimental / Computational Design

### 5.1 Variables Being Changed (Independent Variables for Downstream Benchmark)
- **Loading Contact Patch**: Broad contact envelope ($25\text{--}40\text{ cm}^2$ / frontoparietal dome summit) versus concentrated apex patch ($< 2\text{ cm}^2$).
- **Load Scaling**: Standardized linear reference load ($F_{\text{ref}} = 1.0\text{ kN}$) versus published biological impact estimate ($F_{\text{bio}} = 1360\text{ N}$).

### 5.2 Variables Being Held Fixed (Controls)
- **External Surface Geometry**: Canonical watertight surface of UALVP 2 cranium ($G_0$).
- **Constitutive Law**: Linear elastic isotropic material model.
- **Baseline Material Properties**: Homogeneous compact bone modulus ($E = 17.0\text{ GPa}$), Poisson's ratio ($\nu = 0.30$).
- **Boundary Restraints**: Fixed occipital condyle (articular surface) and spring-supported / fixed nuchal crest rim (restraining cervical muscle attachment).

### 5.3 Inputs & Upstream Artifacts
- **Primary Reference**: Snively & Theodor (2011), Figures 12, 13, and Table S1.
- **Surface Mesh**: MorphoSource Media `000018284` (UALVP 2 whole skull composite) and component neurocranium elements (`000043121`–`000043162`).
- **Input Matrix**: [`data/metadata/biomechanics_input_matrix.csv`](../../data/metadata/biomechanics_input_matrix.csv).

### 5.4 Model Assumptions & Simplifications
- The cranium is modeled as a single contiguous solid, omitting patent sutures (justified by adult fusion in UALVP 2; Schott et al. 2011).
- Complex internal bone architecture (Zone 2 cancellous core, vascular canals) is omitted in Model A and replaced by homogeneous compact bone ($E = 17\text{ GPa}$).
- Loading is treated as quasi-static dorsal compression, neglecting dynamic inertia effects during initial benchmark verification.

### 5.5 Numerical & Computational Methods
- Formalized analytical scaling: linear elastostatics ensures that stresses scale directly as $\sigma(F) = (F / F_{\text{ref}}) \cdot \bar{\sigma}$, allowing compliance fields ($\text{MPa/kN}$) to be evaluated independently of biological force assumptions.

---

## 6. Acceptance / Discrimination Criteria
Model A does not seek exact numerical identity with the published heterogeneous model. Acceptance is structured into three tiers:
1. **Tier 1 (Qualitative / Topological Reproduction)**:
   - High von Mises stress on the dorsal dome apex dissipates steeply toward the ventral cranium (>70% reduction).
   - Broad loading produces low, diffuse stress; concentrated loading produces sharp local apex notch singularities.
   - Endocranial braincase roof remains shielded with low relative stress.
2. **Tier 2 (Quantitative Order-of-Magnitude Agreement)**:
   - Broad loading peak dome stress falls within $4.4\text{--}6.0\text{ MPa/kN}$ ($6.0\text{--}8.0\text{ MPa}$ at $1360\text{ N}$).
   - Concentrated loading apex stress reaches $25.0\text{--}40.0\text{ MPa/kN}$ ($35.0\text{--}55.0\text{ MPa}$ at $1360\text{ N}$).
   - Endocranial braincase roof stress remains $< 3.7\text{ MPa/kN}$ ($< 5.0\text{ MPa}$ at $1360\text{ N}$).
3. **Tier 3 (Exact Numerical Replication)**:
   - Explicitly recognized as unattainable for Model A due to deliberate homogeneous simplification; deferred to future CT-informed models.

---

## 7. Interpretation Limits
- Model A cannot validate or refute whether internal histological zonation was mechanically advantageous; it can only determine whether external dome geometry alone is sufficient to produce qualitative stress shielding.
- The biological load ($1360\text{ N}$) is an inferred estimate from head-butting acceleration models, not a direct measurement.

---

## 8. Planned Computational Implementation
- **Specification Document**: [`reports/phase3_recommended_benchmark.md`](../../reports/phase3_recommended_benchmark.md).
- **Feasibility & Input Audit**: [`reports/snively_theodor_model_reconstruction.md`](../../reports/snively_theodor_model_reconstruction.md).
- **Machine-Readable Registry**: [`data/metadata/biomechanics_input_matrix.csv`](../../data/metadata/biomechanics_input_matrix.csv).
- **Verification Tests**: [`tests/test_phase3_model_audit.py`](../../tests/test_phase3_model_audit.py).

---

## 9. Planned Verification
- Automated validation of input matrix structure, uniqueness, schema compliance, and citation tracking via `pytest tests/test_phase3_model_audit.py`.
- Invariant: Zero parameters from unavailable CT data may be marked as "Available Direct".

---

## 10. Planned Outputs & Artifacts
- **Report 1**: Detailed workflow reconstruction ([`reports/snively_theodor_model_reconstruction.md`](../../reports/snively_theodor_model_reconstruction.md)).
- **Report 2**: Benchmark specification and acceptance criteria ([`reports/phase3_recommended_benchmark.md`](../../reports/phase3_recommended_benchmark.md)).
- **Dataset Artifact**: Input parameter database ([`data/metadata/biomechanics_input_matrix.csv`](../../data/metadata/biomechanics_input_matrix.csv)).

---

## 11. Expected Decision Point
- Approve Decision `D001` (UALVP 2 primary specimen) and Decision `D002` (Establish Model A as first computational benchmark).
- Authorize transition to Phase 4 (Mesh Generation & FEA Solve).

---

## 12. Traceability
```text
Scientific Question (Published FEA audit & Model A definition)
       ↓
Reconstructed Design (docs/phase_design/PHASE3_DESIGN_RECONSTRUCTED.md)
       ↓
Implementation & Input Matrix (data/metadata/biomechanics_input_matrix.csv)
       ↓
Verification Tests (tests/test_phase3_model_audit.py)
       ↓
Benchmark Specification (reports/phase3_recommended_benchmark.md)
       ↓
Decisions D001, D002 (docs/DECISIONS.md)
```

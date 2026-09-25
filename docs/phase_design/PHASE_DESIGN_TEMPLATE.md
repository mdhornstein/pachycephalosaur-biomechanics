# Phase/Gate Design: [Phase/Gate Title]

**Document Role**: Prospective Scientific Research & Computational Design  
**Status**: DRAFT | APPROVED | FROZEN  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md))  
**Date Formulated**: [YYYY-MM-DD]  
**Author(s)**: [Investigation Team / Lead]  

---

## 1. Scientific Question
*State clearly and specifically what biological, biomechanical, or numerical question this phase/gate is designed to resolve.*
- What specific physical, anatomical, or computational uncertainty is being interrogated?
- Why can this question not be answered by existing literature or prior phases without new computation?

## 2. Motivation / Prior Evidence
*Contextualize the question against frozen project milestones and literature evidence.*
- What findings from prior phases (or literature synthesis) directly motivate this experiment?
- What are the relevant literature citations, specimen observations, or preliminary metrics?

## 3. Hypothesis or Competing Expectations
*Formulate distinct, falsifiable hypotheses or competing interpretations.*
- **Hypothesis A / Null Expectation**: [Specific expected behavior or baseline outcome]
- **Hypothesis B / Alternative**: [Alternative outcome and what physical/numerical mechanism it would imply]
- What observable signatures distinguish these hypotheses?

## 4. Scope
*Define explicit boundaries to prevent scope creep.*
- **In Scope**:
  - [Specific tasks, analyses, and parameter spaces covered]
- **Explicitly Out of Scope**:
  - [Tasks deferred to downstream gates, out-of-scope sensitivity sweeps, or premature generalizations]

## 5. Experimental / Computational Design
*Detail the controlled experimental design, isolating comparative factors.*

### 5.1 Variables Being Changed (Independent Variables)
- [List variables systematically varied, their ranges, and step increments]

### 5.2 Variables Being Held Fixed (Controls)
- [List all parameters, meshes, boundary conditions, and solver tolerances held strictly constant to isolate the independent variables]

### 5.3 Inputs & Upstream Artifacts
- **Geometry / Data**: [Input file paths, dataset IDs, SHA-256 hashes]
- **Configuration / Parameters**: [YAML baseline files, parameter tables]

### 5.4 Model Assumptions & Simplifications
- [State all material, geometric, kinematic, and constitutive assumptions explicitly]
- [Distinguish empirical measurements from provisional control parameters]

### 5.5 Numerical & Computational Methods
- **Algorithms**: [e.g., SVD Kabsch, point-to-plane ICP, CG linear solver, Otsu thresholding]
- **Tolerances & Cutoffs**: [Convergence tolerances, distance cutoffs, iteration limits]
- **Coordinate Conventions**: [e.g., zero-based DICOM patient coordinate mapping, standard mesh axes]

## 6. Acceptance / Discrimination Criteria
*Define objective, quantitative pass/fail or discrimination thresholds before running the computation.*
- **Criterion 1**: [Quantitative threshold, e.g., residual RMS < 1.0 mm]
- **Criterion 2**: [Equilibrium or convergence threshold, e.g., relative residual < 1e-6]
- **Criterion 3**: [Sanity / invariance check, e.g., volume conservation, zero rigid translation shift]

## 7. Interpretation Limits
*Declare the epistemic boundaries of what this computation can and cannot conclude.*
- What does a successful outcome prove vs. what does it merely remain consistent with?
- What alternative interpretations cannot be ruled out by this test alone?
- Safeguards against over-interpreting numerical artifacts as biological reality.

## 8. Planned Computational Implementation
*Identify the code architecture and execution pathway.*
- **Primary Executable Entry Point**: [`scripts/...`](../../scripts/) or CLI runner.
- **Reusable Source Modules**: [`src/stegoceras_biomechanics/...`](../../src/stegoceras_biomechanics/)
- **Configuration Files**: [`models/...`](../../models/)
- **Dependencies & Environment**: [e.g., Python 3.12, uv, specific scientific packages]

## 9. Planned Verification & Automated Testing
*Specify regression tests and invariant checks that must pass to freeze this gate.*
- **Unit / Verification Tests**: [`tests/test_...py`](../../tests/)
- **Analytical / Manufactured Benchmarks**: [If applicable, e.g., patch tests, synthetic geometries]
- **Data Integrity Tests**: [Checksum verification, manifest synchronization]

## 10. Planned Outputs & Artifacts
*Enumerate all expected machine-readable results, figures, and reports.*
- **Machine-Readable Metrics**: [`results/.../*.json`](../../results/)
- **Spatial / Array Outputs**: [`simulations/.../*.npz` or `data/.../*.vtp`]
- **Scientific Report**: [`reports/..._report.md`](../../reports/)
- **Metadata & Manifests**: [`data/metadata/...`](../../data/metadata/)

## 11. Expected Decision Point
*Specify what governance or model decision will be triggered upon gate completion.*
- Which entry in [`docs/DECISIONS.md`](../DECISIONS.md) or [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md) will be updated or resolved?
- What are the branching criteria for subsequent gates?

## 12. Traceability
*Maintain links across the research lifecycle:*
```text
Scientific Question (Section 1)
       ↓
Computational Design (Section 5)
       ↓
Implementation & Tests (Sections 8 & 9)
       ↓
Execution & Result Artifacts (Section 10)
       ↓
Scientific Report (reports/)
       ↓
Decision & Living State (docs/DECISIONS.md, docs/CURRENT_STATE.md)
```

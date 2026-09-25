# Scientific & Architectural Decision Log

This document records key scientific, modeling, and architectural decisions made throughout the project. It is **append-only**. When a decision is revised, log a new decision that explicitly supersedes the earlier one.

---

## D001 — Use *Stegoceras validum* UALVP 2 as Primary Computational Specimen
- **Date**: 2026-09-10
- **Status**: ACCEPTED
- **Decision**: Select specimen UALVP 2 (University of Alberta Laboratory for Vertebrate Paleontology) as the primary geometric subject for finite element model construction.
- **Rationale**: UALVP 2 is the most completely preserved, high-resolution micro-CT scanned pachycephalosaur cranium in the public paleontological record. It was the subject of foundational histological and biomechanical literature (Snively & Theodor 2011, Schott et al. 2011), enabling direct comparison.
- **Evidence**: Complete 3D micro-CT scan data and watertight surface reconstruction documented in [`reports/phase1_data_and_geometry_report.md`](../reports/phase1_data_and_geometry_report.md).

---

## D002 — Establish Model A as First Computational Benchmark
- **Date**: 2026-09-12
- **Status**: ACCEPTED
- **Decision**: Construct and solve **Model A** (surface-derived, homogeneous isotropic compact bone: $E = 17.0\text{ GPa}, \nu = 0.30$) before introducing multi-zone internal histological zonation (Model B) or continuous CT density mapping (Model C).
- **Rationale**: Internal histological boundaries and trabecular architectures cannot be uniquely resolved from surface meshes alone. Establishing a mathematically uncompromised homogeneous baseline ensures that mesh convergence, numerical stability, solver scalability, and boundary sensitivities are fully verified before introducing complex histological partitioning.
- **Evidence**: Decision taxonomy documented in [`reports/snively_theodor_model_reconstruction.md`](../reports/snively_theodor_model_reconstruction.md) and [`reports/phase3_recommended_benchmark.md`](../reports/phase3_recommended_benchmark.md).

---

## D003 — Enforce Pure Volumetric $h$-Refinement on Identical Canonical Master Surface
- **Date**: 2026-09-15
- **Status**: ACCEPTED
- **Decision**: Freeze a single canonical watertight boundary surface $G_0$ (`stegoceras_ualvp2_canonical_master.stl`, SHA-256: `5adcf53696268578f083ea29f7f4665c0faf1b41e6362ac858c8a5a7a50d62e2`) and enforce `decimate_reduction: 0.0` across all production convergence tiers.
- **Rationale**: Prior convergence attempts decimated surface triangles per tier to accelerate meshing. A dedicated diagnostic proved that surface decimation introduces boundary slivers ($AR > 25,000$) and alters the physical volume by up to $1.15\%$, conflating geometric boundary approximation with volumetric discretization error. Holding $G_0$ strictly constant ensures that mesh refinement reflects pure volumetric discretization ($h$-refinement).
- **Evidence**: Diagnostic mesh analysis in Section 2.2 of [`reports/phase4_fea_benchmark_report.md`](../reports/phase4_fea_benchmark_report.md).

---

## D004 — Surface Dual-Graph Dijkstra Wavefront Load Patch
- **Date**: 2026-09-18
- **Status**: ACCEPTED
- **Supersedes**: Cylindrical $X$-$Y$ spatial bounding box load selection
- **Decision**: Replace cylindrical spatial windowing with a surface dual-graph Dijkstra wavefront expansion starting from the dorsal apex seed facet, with edge costs equal to Euclidean distance between adjacent triangle centroids, restricted to $Z \ge 60.0\text{ mm}$ and verified with a hard invariant that 100% of loaded nodes satisfy $Z \ge 80.0\text{ mm}$.
- **Rationale**: The earlier cylindrical selection ($X^2 + Y^2 \le R^2$) projected downwards through the entire cranial vault, inadvertently loading ventral, palate, and internal endocranial cavity surfaces ($55.9\%$ of total load applied to non-dorsal nodes). The dual-graph formulation guarantees surface connectedness, strictly dorsal application, and zero ventral penetration.
- **Evidence**: Implemented in [`src/stegoceras_biomechanics/fea/loads.py`](../src/stegoceras_biomechanics/fea/loads.py); verified by unit tests in [`tests/test_phase4_fea.py`](../tests/test_phase4_fea.py).

---

## D005 — Strict Decoupling of Simulation Execution and Visualization
- **Date**: 2026-09-19
- **Status**: ACCEPTED
- **Decision**: Enforce a hard architectural invariant: [`plot_results.py`](../src/stegoceras_biomechanics/fea/plot_results.py) is strictly an artifact consumer and may never call `solve_linear_elasticity()` or generate meshes. All FE solves are driven exclusively by [`solve_production.py`](../src/stegoceras_biomechanics/fea/solve_production.py) in isolated, single-solve subprocesses.
- **Rationale**: An out-of-memory (OOM) crash occurred when `plot_results.py` held multiple large meshes and full solution objects in Python RAM while launching a 498k-DOF direct sparse solve, triggering massive swap thrashing (>70M pageouts) on macOS. Isolated single-solve subprocesses return 100% of memory to the OS upon termination, reducing Tier 3 solve time from 88 minutes down to 34 minutes with zero swap pressure.
- **Evidence**: Benchmarked in commit `b7aa8d0` and documented in [`results/phase4/mesh_convergence_comparison.json`](../results/phase4/mesh_convergence_comparison.json).

---

## D006 — Propagate Internal Stress Discretization Sensitivity into Phase 5 UQ
- **Date**: 2026-09-19
- **Status**: ACCEPTED (Terminology clarified by Literature Basis v1 AF-19)
- **Decision**: Freeze the Phase 4 deterministic FEA baseline at the 825k-element medium mesh. Formally document that while global compliance ($U$), whole-skull displacement, and dorsal dome stress are stabilized ($<2\%$ net shift), global 95th% stress ($-18.10\%$) and endocranial braincase 95th% stress ($-28.64\%$) remain discretization-sensitive. Carry this characterized sensitivity forward into Phase 5 as numerical discretization discrepancy ($\epsilon_{\text{num}} \approx \pm 28.6\%$) rather than asserting false global convergence or attempting intractable laptop direct solves.
- **Rationale**: Pursuing a 1.4M $\to$ 3M $\to$ 5M element direct solve exceeds workstation RAM and direct solver scalability, while iterative PCG requires complex preconditioning on irregular non-convex geometries. Treating the observed stress sensitivity honestly as a known uncertainty component allows Phase 5 global sensitivity analysis to evaluate whether biological uncertainties (e.g. bone modulus, animal size, strike angle) dominate over residual numerical discretization effects.
- **Evidence**: Documented in Section 7 of [`reports/phase4_fea_benchmark_report.md`](../reports/phase4_fea_benchmark_report.md) and [`docs/CURRENT_STATE.md`](../docs/CURRENT_STATE.md).

---

## D007 — Adopt Literature-to-Model Decisions Specification and Realign Computational Gates
- **Date**: 2026-09-24
- **Status**: ACCEPTED
- **Decision**: Formally freeze the literature review layer as **Literature Basis v1** (commit `2662be0`), adopt [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](LITERATURE_TO_MODEL_DECISIONS.md) as the authoritative bridge specification, and realign the computational roadmap to prioritize empirical CT characterization and a decisive material A/B test over an unmotivated 48-point LHS campaign.
- **Rationale**: The audited literature review establishes that:
  1. UALVP 2 has demonstrated internal histological/CT zonation, making our homogeneous Model A strictly a baseline control rather than a final biological endpoint.
  2. In linear elasticity, force magnitude $F$ and base Young's modulus $E$ exhibit closed-form analytical scaling ($\mathbf{u} \propto F/E$, $\boldsymbol{\sigma} \propto F$, $U \propto F^2/E$). Repeated numerical solves over $F$ and $E$ in a homogeneous linear model are mathematically redundant.
  3. Specimen scale is an imaging audit check, not a continuous aleatory biological distribution.
  4. Model-form alternatives (homogeneous vs. zoned) are discrete scenario branches that must not be smeared into arbitrary continuous distributions.
  5. The decisive next scientific question is empirical: *What does the actual UALVP 2 DICOM volume allow us to say about internal architecture, and does introducing evidence-based material zonation (Model B) materially alter cranial compliance, strain-energy distribution, and stress transmission/redistribution to the endocranial braincase relative to Model A?*
- **Evidence**: [`literature/stegoceras_biomechanics_literature_synthesis.md`](../literature/stegoceras_biomechanics_literature_synthesis.md), [`literature/LITERATURE_CORRECTIONS.md`](../literature/LITERATURE_CORRECTIONS.md), and [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](LITERATURE_TO_MODEL_DECISIONS.md) (Model Decision Basis v1).

---

## D008 — Adopt Independent Canonical Bridge Specification (Model Decision Basis v1)
- **Date**: 2026-09-24
- **Status**: ACCEPTED
- **Decision**: Adopt the independent 17-decision, 7-gate bridge specification as the authoritative canonical [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](LITERATURE_TO_MODEL_DECISIONS.md), formally supplanting the prior agent-authored draft (which is preserved in [`docs/archive/2026-09-24_literature_to_model_decisions_v1_legacy.md`](archive/2026-09-24_literature_to_model_decisions_v1_legacy.md)).
- **Rationale**: The independent specification establishes an auditable, rigorous decision register (D01–D17) connecting literature evidence to computational models:
  1. *Specimen Provenance (D01)*: Explicit provenance tracking linking DICOM volume to canonical surface.
  2. *Empirical Verification Gates (D02, D05)*: Direct data-validation gates for physical CT scale registration and image intensity semantics before segmentation.
  3. *Controlled Material A/B Experiment (D03, D04, D06, D15)*: Holding outer geometry, mesh topology, loads, and BCs invariant while evaluating evidence-based internal architecture against the Model A homogeneous control.
  4. *Analytical Shortcuts & Scenario Discipline (D07, D08, D09, D10, D11)*: Analytical scaling of force magnitude ($u \propto F/E, \sigma \propto F, U \propto F^2/E$); discrete scenario branching for contact patch geometry and boundary compliance rather than arbitrary probability distributions.
  5. *Output-Specific Convergence & Comparative QoIs (D12, D13)*: Convergence tracked per-QoI; prioritizing regional energy and stress distributions over local singularity-dominated peak stresses.
  6. *Strict Verification vs. Validation Boundaries (D14)*: Separate tracking for solver verification, numerical convergence, prior benchmark reproduction, and biological validation (marked unavailable for UALVP 2).
  7. *Staged UQ & Deferred Complexities (D16, D17)*: Deferring broad LHS sampling and dynamic/contact FEA until continuous uncertainty inventory and model forms are experimentally justified.
- **Evidence**: [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](LITERATURE_TO_MODEL_DECISIONS.md) and [`literature/stegoceras_biomechanics_literature_synthesis.md`](../literature/stegoceras_biomechanics_literature_synthesis.md).

---

## D009 — Epistemic Clarification of Discretization Discrepancy (Supersedes D006 Terminology)
- **Date**: 2026-09-24
- **Status**: ACCEPTED (Supersedes D006 terminology per Model Decision Basis v1 D12, D14)
- **Decision**: Formally clarify the epistemic representation of the observed mesh-to-mesh difference in endocranial braincase roof 95th-percentile stress ($-28.64\%$ net across $h_1 \to h_3$). This quantity must strictly be treated as an **observed output-specific numerical discretization discrepancy** ($\Delta_{\text{num}}$), explicitly superseding the prior symmetric interval notation ($\pm 28.6\%$) and any interpretation of discretization error as an aleatory or biological uncertainty distribution.
- **Rationale**: In rigorous computational mechanics and verification/validation (V&V):
  1. *Observed Numerical Discrepancy ($\Delta_{\text{num}}$)*: The deterministic, signed difference between discrete solutions across mesh tiers ($2.823 \to 2.383 \to 2.015\text{ MPa}$; net $-28.64\%$). It measures the incomplete spatial resolution of complex internal cranial cavities under the current discrete linear tetrahedral approximation.
  2. *Formal Numerical Error Bound*: An analytical or asymptotic bound (e.g., via Richardson extrapolation or GCI) that requires the solution to be within the asymptotic convergence regime for that specific QoI. Where asymptotic convergence is not yet demonstrated, quoting a symmetric interval ($\pm 28.6\%$) creates the false impression of a verified error bound.
  3. *Biological Uncertainty Distribution*: A probability measure $\theta \sim p(\theta)$ representing physical variation across individuals, tissues, or loading events. Under Rule 4 and Decision D12 of the canonical bridge specification, numerical discretization differences must **never** be smeared into or treated as biological probability distributions.

---

## D010 — Empirical Physical Scale Verification & Zero-Based DICOM Coordinate Convention (Gate B)
- **Date**: 2026-09-25
- **Status**: ACCEPTED (Governing Gate B of Model Decision Basis v1)
- **Decision**: 
  1. Execute the official Gate B registration as a rigid transform at unit scale ($s = 1.000000$), supported by an independent free-scale similarity diagnostic fit ($\hat{s} = 1.00494$, $\Delta s = +0.49\%$, $\Delta \text{RMS} = 0.0785\text{ mm}$); remaining geometric uncertainty is therefore no longer represented as an arbitrary global $\pm 5\%$ scale parameter, but supported by unit scale subject to the quantified registration/modeling residuals.
  2. Adopt the standard DICOM zero-based voxel center mapping directly from `ImagePositionPatient`:
     $$\mathbf{P}(c, r, k) = \mathbf{P}_0 + [c \cdot \Delta x, r \cdot \Delta y, k \cdot \Delta z]^T$$
     without an artificial $+0.5$ half-voxel offset, ensuring exact sub-voxel alignment.
  3. Freeze the objective full-volume Otsu threshold ($T_{\text{primary}} = 20,864$) derived from the 396.8M voxel histogram strictly prior to and independent of comparison with $G_0$.
  4. Separate landmark-only rigid registration (RMS $0.7959\text{ mm}$) from ICP refinement (translation norm $0.2472\text{ mm}$, Euler angles $< 0.05^\circ$), with landmark provenance documented in [`data/metadata/gate_b_landmark_provenance.json`](../data/metadata/gate_b_landmark_provenance.json).
  5. Quantify bidirectional surface distance distributions: forward $G_0 \to S_{\text{CT}}$ ($0.1633\text{ mm}$ median, $86.99\% < 0.5\text{ mm}$) and reverse $S_{\text{CT}} \to G_0$ ($1.0928\text{ mm}$ median, $4.6529\text{ mm}$ RMS; bidirectional mean $1.5704\text{ mm}$), documenting that reverse tail elevations reflect internal trabecular/endocranial surfaces in the CT volume absent from the outer boundary shell $G_0$.
  6. Formally record that the sub-millimeter median forward surface residual ($0.1633\text{ mm}$) and sub-voxel translation provide decisive geometric evidence consistent with $G_0$ being derived directly from this micro-CT volume, distinguishing geometric correspondence from archival provenance proof.
- **Evidence**: [`reports/phase5_gate_b_registration_report.md`](../reports/phase5_gate_b_registration_report.md), [`results/phase5/gate_b_registration_metrics.json`](../results/phase5/gate_b_registration_metrics.json), [`data/metadata/gate_b_landmark_provenance.json`](../data/metadata/gate_b_landmark_provenance.json), and [`tests/test_gate_b_registration.py`](../tests/test_gate_b_registration.py).


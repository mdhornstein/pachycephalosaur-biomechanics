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
  5. The decisive next scientific question is empirical: *What does the actual UALVP 2 DICOM volume allow us to say about internal architecture, and does introducing evidence-based material zonation (Model B) materially change the mechanical response and braincase stress attenuation relative to Model A?*
- **Evidence**: [`literature/stegoceras_biomechanics_literature_synthesis.md`](../literature/stegoceras_biomechanics_literature_synthesis.md), [`literature/LITERATURE_CORRECTIONS.md`](../literature/LITERATURE_CORRECTIONS.md), and [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](LITERATURE_TO_MODEL_DECISIONS.md).

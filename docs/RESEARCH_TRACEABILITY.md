# Research Traceability & Computational Reproducibility Map

**Document Role**: Master Scientific & Computational Traceability Matrix  
**Status**: ACTIVE STANDARD  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](LITERATURE_TO_MODEL_DECISIONS.md)) & Repository Documentation System ([`docs/DOCUMENTATION_SYSTEM.md`](DOCUMENTATION_SYSTEM.md))  
**Last Updated**: 2026-09-25  

---

## 🏛️ 1. Purpose & Core Philosophy

This document serves as the **single authoritative entry point** linking every scientific question in this project to its executable computational evidence and reproduction recipe.

To maintain scientific integrity and auditability, the repository enforces a strict separation of computational and epistemic layers across the entire research lifecycle:

```text
       What we intended to test  ──►  Scientific Design (docs/phase_design/)
                  ↓
          Where it ran  ──►  Environment (Python runtime & dependencies)
                  ↓
       How it was executed  ──►  Exact Execution Commands (CLI invocations)
                  ↓
   What primary code solved it  ──►  Primary Computational Entry Points (src/, scripts/)
                  ↓
  What transformed raw output  ──►  Post-Processing & Derived Analysis (metric extraction)
                  ↓
      What plotted the fields  ──►  Figure-Generation Entry Points (visualization)
                  ↓
   What numbers were generated  ──►  Machine-Readable Results (results/, simulations/)
                  ↓
        What we conclude  ──►  Formal Milestone Reports (reports/)
                  ↓
        What decision follows   ──►  Decision Register & Living State (docs/DECISIONS.md, docs/CURRENT_STATE.md)
```

No document collapses these distinct layers into one.

---

## 🗺️ 2. Master Research Traceability Matrix

The table below maps each major completed, active, and planned phase/gate across the entire research lifecycle. All links are repository-relative.

| Phase / Gate | Scientific Question | Scientific Design | Primary Execution Command(s) | Primary Solver / Entry Point | Post-Processing & Derived Analysis | Figure Generation | Results (Machine-Readable) | Formal Report | Commits & Decisions |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 3** (Model Audit & Benchmark Specification) | What are defensible inputs, boundary conditions, and validation targets for a minimal surface-derived FEA benchmark of UALVP 2 based on Snively & Theodor (2011), separating linear compliance from biological assumptions? | [`docs/phase_design/PHASE3_DESIGN_RECONSTRUCTED.md`](phase_design/PHASE3_DESIGN_RECONSTRUCTED.md) *(Retrospective)* | `uv run pytest tests/test_phase3_model_audit.py -v` | Data matrix schema & dimensional analysis | Parameter status, evidence scoring, and dimensional validation | *None* | [`data/metadata/biomechanics_input_matrix.csv`](../data/metadata/biomechanics_input_matrix.csv) | [`reports/phase3_recommended_benchmark.md`](../reports/phase3_recommended_benchmark.md), [`reports/snively_theodor_model_reconstruction.md`](../reports/snively_theodor_model_reconstruction.md) | Decisions [`D001`, `D002`](DECISIONS.md)<br>• **Exec**: `79c8cb6`<br>• **Report**: `255ee46` |
| **Phase 4** (Surface-Derived FEA Benchmark & Discretization Sensitivity) | Under standardized compressive loading on canonical surface $G_0$, does the 3D linear elastic FEA pipeline achieve static equilibrium, energy balance, and stable global metrics under pure volumetric $h$-refinement, and how do localized stresses respond? | [`docs/phase_design/PHASE4_DESIGN_RECONSTRUCTED.md`](phase_design/PHASE4_DESIGN_RECONSTRUCTED.md) *(Retrospective)* | 1. `uv run python -m stegoceras_biomechanics.fea.solve_production --tier all`<br>2. `uv run python -m stegoceras_biomechanics.fea.plot_results` | `stegoceras_biomechanics.fea.solve_production` | `stegoceras_biomechanics.fea.plot_results` (derives aspect ratios, apex displacements, regional stress sensitivities, and convergence comparison) | `stegoceras_biomechanics.fea.plot_results` (Figures 08–12) | [`results/phase4/mesh_convergence_comparison.json`](../results/phase4/mesh_convergence_comparison.json), [`results/phase4/metrics_*.json`](../results/phase4/), `simulations/phase4/solution_*.npz` | [`reports/phase4_fea_benchmark_report.md`](../reports/phase4_fea_benchmark_report.md) | Decisions [`D003`–`D006`](DECISIONS.md)<br>• **Exec**: `b7aa8d0`<br>• **Report**: `15a342f` |
| **Phase 5 Gate A** (DICOM Ingestion & Header Audit) | Is the MorphoSource UALVP 2 cranium series (Media 000018283) an intact, uncorrupted, geometrically documented micro-CT series matching the physical specimen, and what are its precise spatial and intensity semantics? | [`docs/phase_design/PHASE5_GATE_A_DESIGN.md`](phase_design/PHASE5_GATE_A_DESIGN.md) *(Retrospective)* | 1. `uv run python scripts/ingest_data.py audit`<br>2. `uv run pytest tests/test_gate_a_dicom.py -v` | `stegoceras_biomechanics.io.ingest` | Per-slice cryptographic hashing, geometric metadata extraction, and intensity dynamic range auditing | *None* | [`data/metadata/dataset_manifest.yaml`](../data/metadata/dataset_manifest.yaml), [`data/metadata/dicom_slice_manifest.json`](../data/metadata/dicom_slice_manifest.json) | [`reports/phase5_gate_a_dicom_report.md`](../reports/phase5_gate_a_dicom_report.md) | Model Decision Basis v1 §4.1<br>• **Exec**: `5f575d8`<br>• **Report**: `1c7a125` |
| **Phase 5 Gate B** (CT-to-Surface Registration & Empirical Scale Verification) | What is the physical scale and spatial registration relationship between canonical surface $G_0$ and the micro-CT volume, does empirical registration support unit scale ($s = 1.000000$), and does $G_0$ match the outer periosteal bone boundary? | [`docs/phase_design/PHASE5_GATE_B_DESIGN.md`](phase_design/PHASE5_GATE_B_DESIGN.md) *(Retrospective)* | 1. `uv run python scripts/register_ct_to_surface.py`<br>2. `uv run pytest tests/test_gate_b_registration.py -v` | `scripts/register_ct_to_surface.py` | Integrated in registration script: Umeyama free-scale diagnostic, forward surface distance, reverse interface diagnostic, normal signed distance | *None* (JSON metric export) | [`results/phase5/gate_b_registration_metrics.json`](../results/phase5/gate_b_registration_metrics.json) | [`reports/phase5_gate_b_registration_report.md`](../reports/phase5_gate_b_registration_report.md) | Decision [`D010`](DECISIONS.md)<br>• **Exec**: `ca32eba`<br>• **Report**: `fa0cf58` |
| **Phase 5 Gate C** (Image Semantics & Attenuation Characterization) *(ACTIVE NEXT)* | What are the numerical image semantics, attenuation dynamic range, artifact profiles, and tissue contrast distributions in the CT volume, and do they support or refute discrete radiological zonation in the dome? | [`docs/phase_design/PHASE5_GATE_C_DESIGN.md`](phase_design/PHASE5_GATE_C_DESIGN.md) *(Prospective)* | 1. `uv run python scripts/characterize_image_semantics.py`<br>2. `uv run pytest tests/test_gate_c_semantics.py -v` | `scripts/characterize_image_semantics.py` *(planned)* | Attenuation histogram profiling, beam-hardening transect analysis, tissue contrast gradient analysis | Attenuation profiles, intensity histograms, artifact transects in `reports/figures/` | `results/phase5/gate_c_semantics_metrics.json` *(planned)* | `reports/phase5_gate_c_semantics_report.md` *(planned)* | Expected Decision `D011`<br>• **Exec**: *(Pending)*<br>• **Report**: *(Pending)* |

---

## 🔬 3. The Minimal Reproduction Schema

Starting from the frozen repository state and documented inputs, every reported result must allow a future researcher to answer:
> **"What exact sequence of operations do I execute to regenerate the evidence used by this report?"**

Each phase/gate documents the following minimal tuple:

1. **Scientific Design**: The prospective design document in [`docs/phase_design/`](phase_design/) (or explicitly marked retrospective reconstruction).
2. **Environment / Dependencies**: Exact Python runtime version and dependencies from `pyproject.toml` / `uv.lock`.
3. **Execution Commit**: Git commit SHA at which the computation was executed.
4. **Report / Documentation Commit**: Git commit SHA containing the finalized scientific report.
5. **Execution Command(s)**: Copy-pasteable CLI commands to reproduce the run.
6. **Primary Computational Entry Point(s)**: The script, module, or CLI entry point that drives the primary simulation or calculation.
7. **Reusable Source Modules**: Core packages in `src/stegoceras_biomechanics/` providing mathematical routines.
8. **Post-processing / Analysis Entry Point(s)**: The code transforming raw simulation outputs into derived comparison metrics.
9. **Figure-generation Entry Point(s)**: The code creating visual figures from raw or derived data.
10. **Input Artifacts & Cryptographic Checksums**: Input files with SHA-256 hashes.
11. **Machine-Readable Result Artifacts**: Raw simulation outputs (`simulations/`) and derived summary metrics (`results/`).
12. **Figure Artifacts**: Visual artifacts in `reports/figures/`.
13. **Automated Verification Tests**: Test suite in `tests/` verifying invariants and tolerances.
14. **Formal Report & Decision Record**: Report in `reports/` and resulting entries in `docs/DECISIONS.md`.

> [!IMPORTANT]
> **Core Provenance Rule**: Numerical results must identify the commit that generated them; reports must separately identify the commit containing the final report. Because scientific interpretation and report prose can be refined after computation completes, conflating execution commits with documentation commits is strictly avoided.

---

## 📋 4. Detailed Phase-by-Phase Traceability & Reproduction Records

### Phase 4: Surface-Derived FEA Benchmark & Discretization Sensitivity

- **Scientific Question**: Under standardized compressive loading on canonical surface $G_0$, does the 3D linear elastic FEA pipeline achieve static equilibrium, energy balance, and stable global metrics under pure volumetric $h$-refinement, and how do localized stresses respond?
- **Design Document**: [`docs/phase_design/PHASE4_DESIGN_RECONSTRUCTED.md`](phase_design/PHASE4_DESIGN_RECONSTRUCTED.md) *(Retrospective Reconstruction)*
- **Environment**: Python 3.12 (managed via `uv`), dependencies in [`pyproject.toml`](../pyproject.toml) (`numpy`, `scipy`, `matplotlib`, `trimesh`, `pyvista`, `pytest`)
- **Execution Commit**: `b7aa8d0` (Solver decoupling, production execution of 3-tier hierarchy, and convergence verification)
- **Report / Documentation Commit**: `15a342f` (Phase 4 Freeze, benchmark report reconciliation, and documentation system freeze)
- **Execution Command(s)**:
  ```bash
  # Step 1: Run production FEA solver across all 3 discretization tiers in isolated processes
  uv run python -m stegoceras_biomechanics.fea.solve_production --tier all

  # Step 2: Run post-processing derived numerical analysis and generate publication figures
  uv run python -m stegoceras_biomechanics.fea.plot_results

  # Step 3: Run automated verification tests
  uv run pytest tests/test_phase4_fea.py -v
  ```
- **Primary Computational Entry Point(s)**:
  - [`src/stegoceras_biomechanics/fea/solve_production.py`](../src/stegoceras_biomechanics/fea/solve_production.py): `run_all_tiers_isolated()` sequentially spawning isolated subprocesses calling `solve_tier()` for `coarse`, `medium_coarse`, and `medium`.
- **Reusable Source Modules**:
  - [`src/stegoceras_biomechanics/fea/solver.py`](../src/stegoceras_biomechanics/fea/solver.py): `solve_linear_elasticity()`
  - [`src/stegoceras_biomechanics/fea/meshing.py`](../src/stegoceras_biomechanics/fea/meshing.py): `extract_boundary_surface()`, `inspect_mesh_quality()`
  - [`src/stegoceras_biomechanics/fea/loads.py`](../src/stegoceras_biomechanics/fea/loads.py): `generate_dome_load_patch()`
  - [`src/stegoceras_biomechanics/fea/boundary_conditions.py`](../src/stegoceras_biomechanics/fea/boundary_conditions.py): `generate_boundary_constraints()`
  - [`src/stegoceras_biomechanics/fea/results.py`](../src/stegoceras_biomechanics/fea/results.py): `extract_subregion_metrics()`
- **Post-processing / Analysis Entry Point(s)**:
  - [`src/stegoceras_biomechanics/fea/plot_results.py`](../src/stegoceras_biomechanics/fea/plot_results.py): `generate_all_phase4_results_and_plots()`
  - *Derived Analysis Performed*:
    - Computes tetrahedral aspect ratio percentiles (p50, p95, max, mean) directly from mesh geometry files.
    - Evaluates apex node displacement for each mesh tier.
    - Computes global 95th and 99th percentile von Mises stress.
    - Extracts dome apex and endocranial braincase roof stress sensitivities from subregion metrics.
    - Derives cross-tier convergence metrics and writes the authoritative derived comparison artifact: [`results/phase4/mesh_convergence_comparison.json`](../results/phase4/mesh_convergence_comparison.json).
- **Figure-generation Entry Point(s)**:
  - [`src/stegoceras_biomechanics/fea/plot_results.py`](../src/stegoceras_biomechanics/fea/plot_results.py) renders Figures 08–12.
- **Input Artifacts & Cryptographic Checksums**:
  - Canonical master surface $G_0$: [`data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`](../data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl) (SHA-256: `5adcf53696268578f083ea29f7f4665c0faf1b41e6362ac858c8a5a7a50d62e2`)
  - Cleaned tetrahedral meshes:
    - `data/meshes/cleaned/stegoceras_tetmesh_coarse.npz` (SHA-256: `c1aa2c28...`)
    - `data/meshes/cleaned/stegoceras_tetmesh_medium_coarse.npz` (SHA-256: `5ee31339...`)
    - `data/meshes/cleaned/stegoceras_tetmesh_medium.npz` (SHA-256: `78a2f8b5...`)
  - Model configuration: [`models/phase4/baseline.yaml`](../models/phase4/baseline.yaml)
- **Machine-Readable Result Artifacts**:
  - Raw Simulation Binaries:
    - `simulations/phase4/solution_coarse.npz`
    - `simulations/phase4/solution_medium_coarse.npz`
    - `simulations/phase4/solution_medium.npz`
  - Raw Regional Metrics:
    - `results/phase4/metrics_coarse.{json,csv}`
    - `results/phase4/metrics_medium_coarse.{json,csv}`
    - `results/phase4/metrics_medium.{json,csv}`
    - `results/phase4/ualvp2_1kn_subregion_metrics.{json,csv}` (canonical medium primary benchmark)
    - `results/phase4/summary_{coarse,medium_coarse,medium}.json`
  - Derived Analysis Artifact:
    - [`results/phase4/mesh_convergence_comparison.json`](../results/phase4/mesh_convergence_comparison.json)
- **Figure Artifacts**:
  - [`reports/figures/08_mesh_resolutions_comparison.png`](../reports/figures/08_mesh_resolutions_comparison.png)
  - [`reports/figures/09_fe_von_mises_stress_1kn.png`](../reports/figures/09_fe_von_mises_stress_1kn.png)
  - [`reports/figures/10_fe_displacement_and_strain.png`](../reports/figures/10_fe_displacement_and_strain.png)
  - [`reports/figures/11_mesh_convergence_curves.png`](../reports/figures/11_mesh_convergence_curves.png)
  - [`reports/figures/12_linearity_scaling_validation.png`](../reports/figures/12_linearity_scaling_validation.png)
- **Automated Verification Tests**:
  - [`tests/test_phase4_fea.py`](../tests/test_phase4_fea.py) (53 tests verifying analytical solution, manufactured displacement field, work-energy identity, and convergence rates)
- **Formal Report**:
  - [`reports/phase4_fea_benchmark_report.md`](../reports/phase4_fea_benchmark_report.md)
- **Resulting Decision / State Update**:
  - Decisions `D003`, `D004`, `D005`, `D006` in [`docs/DECISIONS.md`](DECISIONS.md); Phase 4 Freeze in [`docs/CURRENT_STATE.md`](CURRENT_STATE.md) and [`HANDOFF.md`](../HANDOFF.md).

---

### Phase 5 Gate B: CT-to-Surface Registration & Empirical Scale Verification

- **Scientific Question**: What is the physical scale and spatial registration relationship between canonical surface $G_0$ and the micro-CT volume, does empirical registration support unit scale ($s = 1.000000$), and does $G_0$ match the outer periosteal bone boundary?
- **Design Document**: [`docs/phase_design/PHASE5_GATE_B_DESIGN.md`](phase_design/PHASE5_GATE_B_DESIGN.md) *(Retrospective Reconstruction)*
- **Environment**: Python 3.12 (`uv`), dependencies in [`pyproject.toml`](../pyproject.toml) (`numpy`, `scipy`, `pydicom`, `pyvista`, `trimesh`, `pytest`)
- **Execution Commit**: `ca32eba` (Primary 6-DOF Kabsch registration, Free-Scale similarity diagnostic, ICP refinement, and metric generation)
- **Report / Documentation Commit**: `fa0cf58` (Refinement of diagnostic terminology, whole-volume interface diagnostic, and dimensional translation description)
- **Execution Command(s)**:
  ```bash
  # Step 1: Run registration solver, scale diagnostic, and boundary residual evaluation
  uv run python scripts/register_ct_to_surface.py

  # Step 2: Run automated verification tests
  uv run pytest tests/test_gate_b_registration.py -v
  ```
- **Primary Computational Entry Point(s)**:
  - [`scripts/register_ct_to_surface.py`](../scripts/register_ct_to_surface.py): `execute_gate_b_registration()`
- **Reusable Source Modules**:
  - Embedded registration algorithms: 6-DOF Kabsch SVD rigid alignment, 7-DOF Umeyama SVD similarity scale diagnostic, point-to-plane ICP, Flying Edges isosurface extraction (`pyvista.ImageData.contour`), KDTree spatial distance evaluation (`scipy.spatial.KDTree`).
- **Post-processing / Analysis Entry Point(s)**:
  - Integrated in [`scripts/register_ct_to_surface.py`](../scripts/register_ct_to_surface.py):
    - Evaluates forward surface distance residuals ($G_0 \to S_{\text{CT}}$).
    - Evaluates reverse whole-volume internal interface diagnostic ($S_{\text{CT}} \to G_0$).
    - Computes signed normal distance distribution along outward vertex normals.
    - Evaluates anatomical subregion differential accuracy (dome apex, skull roof, occipital condyle, etc.).
- **Figure-generation Entry Point(s)**:
  - *None* (Gate B outputs are machine-readable JSON metrics; visual figures not compiled into `reports/figures/`).
- **Input Artifacts & Cryptographic Checksums**:
  - Canonical master surface $G_0$: [`data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`](../data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl) (SHA-256: `5adcf536...`)
  - 514 Cranium micro-CT slices: `data/raw/dicom/cranium/` (SHA-256 verified in [`data/metadata/dicom_slice_manifest.json`](../data/metadata/dicom_slice_manifest.json))
  - Landmark provenance database: [`data/metadata/gate_b_landmark_provenance.json`](../data/metadata/gate_b_landmark_provenance.json)
- **Machine-Readable Result Artifacts**:
  - [`results/phase5/gate_b_registration_metrics.json`](../results/phase5/gate_b_registration_metrics.json)
- **Figure Artifacts**:
  - *None*
- **Automated Verification Tests**:
  - [`tests/test_gate_b_registration.py`](../tests/test_gate_b_registration.py) (10 tests: mandated rigid scale, free-scale diagnostic, zero-based DICOM mapping, boundary residuals, ICP convergence, signed normal symmetry, subregion distributions)
- **Formal Report**:
  - [`reports/phase5_gate_b_registration_report.md`](../reports/phase5_gate_b_registration_report.md)
- **Resulting Decision / State Update**:
  - Decision [`D010`](DECISIONS.md) in [`docs/DECISIONS.md`](DECISIONS.md); Phase 5 Gate B Freeze in [`docs/CURRENT_STATE.md`](CURRENT_STATE.md) and [`HANDOFF.md`](../HANDOFF.md).

---

### Phase 5 Gate A: DICOM Ingestion & Cryptographic Header Audit

- **Scientific Question**: Is the MorphoSource UALVP 2 cranium series (Media 000018283) an intact, uncorrupted, geometrically documented micro-CT series matching the physical specimen, and what are its precise spatial and intensity semantics?
- **Design Document**: [`docs/phase_design/PHASE5_GATE_A_DESIGN.md`](phase_design/PHASE5_GATE_A_DESIGN.md) *(Retrospective Reconstruction)*
- **Environment**: Python 3.12 (`uv`), `pydicom`, `pyyaml`, `pytest`
- **Execution Commit**: `5f575d8` (Initial DICOM archive extraction, per-slice SHA-256 computation, and slice manifest generation)
- **Report / Documentation Commit**: `1c7a125` (Refinement of Gate A epistemic language, coordinate semantics, and regression tests)
- **Execution Command(s)**:
  ```bash
  # Step 1: Audit local dataset inventory against dataset manifest
  uv run python scripts/ingest_data.py audit

  # Step 2: Run automated DICOM integrity and metadata verification tests
  uv run pytest tests/test_gate_a_dicom.py -v
  ```
  *(Note on historical command provenance: The original outer ZIP extraction and per-slice SHA-256 hash generation were executed in Python via `pydicom`/`hashlib` during commit `5f575d8`; regression verification is automated via `pytest tests/test_gate_a_dicom.py`)*
- **Primary Computational Entry Point(s)**:
  - [`scripts/ingest_data.py`](../scripts/ingest_data.py)
  - [`src/stegoceras_biomechanics/io/ingest.py`](../src/stegoceras_biomechanics/io/ingest.py): `ingest_file()`
  - [`src/stegoceras_biomechanics/io/manifest.py`](../src/stegoceras_biomechanics/io/manifest.py): `audit_local_inventory()`, `compute_sha256()`
- **Reusable Source Modules**:
  - `stegoceras_biomechanics.io.manifest`
  - `stegoceras_biomechanics.io.ingest`
- **Post-processing / Analysis Entry Point(s)**:
  - Header inspection, per-slice SHA-256 cataloging, and coordinate metadata verification ([`tests/test_gate_a_dicom.py`](../tests/test_gate_a_dicom.py))
- **Figure-generation Entry Point(s)**:
  - *None*
- **Input Artifacts & Cryptographic Checksums**:
  - Outer MorphoSource ZIP: `data/raw/dicom/morphosource_media-id-000018283_download-bde34772.zip` (SHA-256: `bde347726487e411032df4c4fb3158c4dd4d2fe948ff1129f12df08233e79e6c`)
  - Inner DICOM ZIP: `18283_CRANIAL_DICOM.zip` (SHA-256: `03f0d2cba50b074a1ea13e710815152fe14316d29668d29b1be7010484eb3b1c`)
- **Machine-Readable Result Artifacts**:
  - [`data/metadata/dataset_manifest.yaml`](../data/metadata/dataset_manifest.yaml)
  - [`data/metadata/dicom_slice_manifest.json`](../data/metadata/dicom_slice_manifest.json) (514 slices cataloged with individual SHA-256 hashes)
- **Figure Artifacts**:
  - *None*
- **Automated Verification Tests**:
  - [`tests/test_gate_a_dicom.py`](../tests/test_gate_a_dicom.py) (7 tests: nested archive integrity, slice count, per-slice SHA-256 full integrity, spatial geometry, orientation tags absence, intensity semantics, boundary slice headers)
- **Formal Report**:
  - [`reports/phase5_gate_a_dicom_report.md`](../reports/phase5_gate_a_dicom_report.md)
- **Resulting Decision / State Update**:
  - Model Decision Basis v1 §4.1; Decision `D008` in [`docs/DECISIONS.md`](DECISIONS.md); updated [`docs/CURRENT_STATE.md`](CURRENT_STATE.md) and [`HANDOFF.md`](../HANDOFF.md).

---

### Phase 3: Published Model Audit & Provisional Benchmark Specification

- **Scientific Question**: What are the defensible inputs, boundary conditions, and validation targets for a minimal surface-derived FEA benchmark of UALVP 2 based on Snively & Theodor (2011), separating linear compliance from biological assumptions?
- **Design Document**: [`docs/phase_design/PHASE3_DESIGN_RECONSTRUCTED.md`](phase_design/PHASE3_DESIGN_RECONSTRUCTED.md) *(Retrospective Reconstruction)*
- **Environment**: Python 3.12 (`uv`), `pandas`, `pytest`, `jupyter`
- **Execution Commit**: `79c8cb6` (Phase 3 input audit, dimensional check, and benchmark specification execution)
- **Report / Documentation Commit**: `255ee46` (Final Phase 3 specification refinement and validation hierarchy freeze)
- **Execution Command(s)**:
  ```bash
  # Step 1: Run automated verification tests on input parameter matrix and evidence taxonomy
  uv run pytest tests/test_phase3_model_audit.py -v
  ```
  *(Note on historical command provenance: Phase 3 established the parameter audit and validation hierarchy through structured data compilation into `data/metadata/biomechanics_input_matrix.csv` and exploratory evaluation in `notebooks/05_model_input_dimensional_audit.ipynb`. The exact exploratory shell commands used during initial data entry at commit `79c8cb6` were not preserved contemporaneously; automated validation was codified in `tests/test_phase3_model_audit.py`)*
- **Primary Computational Entry Point(s)**:
  - `notebooks/05_model_input_dimensional_audit.ipynb`
  - [`tests/test_phase3_model_audit.py`](../tests/test_phase3_model_audit.py)
- **Reusable Source Modules**:
  - `src/stegoceras_biomechanics`
- **Post-processing / Analysis Entry Point(s)**:
  - Input categorization, evidence-level scoring, dimensional scaling verification, and validation tier partitioning
- **Figure-generation Entry Point(s)**:
  - *None*
- **Input Artifacts & Cryptographic Checksums**:
  - Snively & Theodor (2011) *PLoS ONE* 6(6): e21412 publication data
  - MorphoSource Media `000018284` & `000043121`–`000043162`
- **Machine-Readable Result Artifacts**:
  - [`data/metadata/biomechanics_input_matrix.csv`](../data/metadata/biomechanics_input_matrix.csv)
- **Figure Artifacts**:
  - *None*
- **Automated Verification Tests**:
  - [`tests/test_phase3_model_audit.py`](../tests/test_phase3_model_audit.py) (6 tests: deliverable existence, schema/uniqueness, status validity, CT variable availability constraint, literature citations, defensibility)
- **Formal Report**:
  - [`reports/phase3_recommended_benchmark.md`](../reports/phase3_recommended_benchmark.md)
  - [`reports/snively_theodor_model_reconstruction.md`](../reports/snively_theodor_model_reconstruction.md)
- **Resulting Decision / State Update**:
  - Decisions [`D001`, `D002`](DECISIONS.md) in [`docs/DECISIONS.md`](DECISIONS.md).

---

### Phase 5 Gate C: Image Semantics & Attenuation Characterization *(ACTIVE NEXT)*

- **Scientific Question**: What are the numerical image semantics, attenuation dynamic range, artifact profiles, and tissue contrast distributions in the CT volume, and do they support or refute discrete radiological zonation in the dome?
- **Design Document**: [`docs/phase_design/PHASE5_GATE_C_DESIGN.md`](phase_design/PHASE5_GATE_C_DESIGN.md) *(Prospective)*
- **Environment**: Python 3.12 (`uv`), dependencies in [`pyproject.toml`](../pyproject.toml) (`numpy`, `scipy`, `pydicom`, `pyvista`, `matplotlib`, `pytest`)
- **Execution Commit**: *(Pending execution)*
- **Report / Documentation Commit**: *(Pending report)*
- **Execution Command(s)**:
  ```bash
  # Step 1: Run attenuation characterization and profile extraction
  uv run python scripts/characterize_image_semantics.py

  # Step 2: Run automated verification tests
  uv run pytest tests/test_gate_c_semantics.py -v
  ```
- **Primary Computational Entry Point(s)**:
  - `scripts/characterize_image_semantics.py` *(planned)*
- **Reusable Source Modules**:
  - `stegoceras_biomechanics.ct.semantics` *(planned)*
- **Post-processing / Analysis Entry Point(s)**:
  - Histogram dynamic range extraction, beam-hardening transect analysis, tissue contrast gradient analysis
- **Figure-generation Entry Point(s)**:
  - Frontoparietal attenuation profile curves, full-volume intensity histogram, and beam-hardening transects in `reports/figures/`
- **Input Artifacts & Cryptographic Checksums**:
  - 514 Cranium micro-CT slices: `data/raw/dicom/cranium/`
  - Gate B composite transformation $\mathbf{T}_{\text{composite}}$: [`results/phase5/gate_b_registration_metrics.json`](../results/phase5/gate_b_registration_metrics.json)
  - Canonical master surface $G_0$: [`data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`](../data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl)
- **Machine-Readable Result Artifacts**:
  - `results/phase5/gate_c_semantics_metrics.json` *(planned)*
- **Figure Artifacts**:
  - Planned: `reports/figures/13_ct_intensity_histogram.png`, `reports/figures/14_dome_attenuation_transects.png`
- **Automated Verification Tests**:
  - `tests/test_gate_c_semantics.py` *(planned)*
- **Formal Report**:
  - `reports/phase5_gate_c_semantics_report.md` *(planned)*
- **Resulting Decision / State Update**:
  - Planned Decision `D011`.

---

## 🚫 5. Architectural Invariants

1. **No Conflation of Scientific Interpretation and Code**:
   Scientific conclusions belong in `reports/` and `docs/DECISIONS.md`. Source code docstrings in `src/` describe computational capabilities, algorithms, inputs, outputs, and mathematical formulas—not biological conclusions.
2. **Derived Numerical Analysis Must Be Explicitly Documented**:
   When post-processing scripts compute summary statistics, fit curves, or derive cross-tier metrics, their role as scientific analysis must be documented in this matrix and in the corresponding report's `## Reproduction` section.
3. **No Orphan Results**:
   Every JSON, CSV, or NPZ file in `results/` or `simulations/` must be generated by an identifiable script or test, documented in a formal report, and referenced in this traceability matrix.
4. **No Phantom Inputs**:
   No computation may rely on untracked manual GUI clicks, uncommitted local scratch files, or undocumented external APIs. All inputs must reside in `data/` with cryptographic hashes logged in `data/metadata/`.
5. **Separation of Design and Execution**:
   Design documents in `docs/phase_design/` record the prospective experimental design and hypotheses *before* execution. When retrospective reconstructions are necessary for historical phases, they are explicitly labeled as retrospective.


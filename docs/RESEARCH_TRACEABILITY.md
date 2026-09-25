# Research Traceability & Computational Reproducibility Map

**Document Role**: Master Scientific & Computational Traceability Matrix  
**Status**: ACTIVE STANDARD  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](LITERATURE_TO_MODEL_DECISIONS.md)) & Repository Documentation System ([`docs/DOCUMENTATION_SYSTEM.md`](DOCUMENTATION_SYSTEM.md))  
**Last Updated**: 2026-09-25  

---

## 🏛️ 1. Purpose & Core Philosophy

This document serves as the **single entry point** linking every scientific question in this project to its executable computational evidence.

To maintain scientific integrity and auditability, the repository enforces a strict separation of computational and epistemic layers:

```text
       What we intended to test  ──►  Scientific Design (docs/phase_design/)
                  ↓
   What we actually implemented  ──►  Computational Implementation (src/, scripts/, models/)
                  ↓
             What actually ran  ──►  Verification Tests & Execution (tests/, commits)
                  ↓
             What was observed  ──►  Machine-Readable Results (results/, data/metadata/)
                  ↓
             What we conclude  ──►  Formal Milestone Reports (reports/)
                  ↓
       What decision follows   ──►  Decision Register & Living State (docs/DECISIONS.md, docs/CURRENT_STATE.md)
```

No document collapses these distinct layers into one.

---

## 🗺️ 2. Master Research Traceability Matrix

The table below maps each major completed, active, and planned phase/gate across the entire research lifecycle. All links are repository-relative.

| Phase / Gate | Scientific Question | Scientific Design | Computational Implementation | Automated Tests | Inputs & Upstream Data | Results (Machine-Readable) | Formal Report | Decision & Provenance Commits |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 3** (Model Audit & Benchmark Specification) | What are the defensible inputs, boundary conditions, and validation targets for a minimal surface-derived FEA benchmark of UALVP 2 based on Snively & Theodor (2011), separating linear compliance from biological assumptions? | [`docs/phase_design/PHASE3_DESIGN_RECONSTRUCTED.md`](phase_design/PHASE3_DESIGN_RECONSTRUCTED.md) *(Retrospective)* | Parameter matrix schema and dimensional analysis in [`src/stegoceras_biomechanics/`](../src/stegoceras_biomechanics/) | [`tests/test_phase3_model_audit.py`](../tests/test_phase3_model_audit.py) | Snively & Theodor (2011); MorphoSource Media `000018284` & `000043121`–`43162` | [`data/metadata/biomechanics_input_matrix.csv`](../data/metadata/biomechanics_input_matrix.csv) | [`reports/phase3_recommended_benchmark.md`](../reports/phase3_recommended_benchmark.md), [`reports/snively_theodor_model_reconstruction.md`](../reports/snively_theodor_model_reconstruction.md) | Decisions [`D001`, `D002`](DECISIONS.md)<br>• **Exec**: `79c8cb6`<br>• **Report**: `255ee46` |
| **Phase 4** (Surface-Derived FEA Benchmark & Discretization Sensitivity) | Under standardized compressive loading on canonical surface $G_0$, does the 3D linear elastic FEA pipeline achieve static equilibrium, energy balance, and stable global metrics under pure volumetric $h$-refinement, and how do localized stresses respond? | [`docs/phase_design/PHASE4_DESIGN_RECONSTRUCTED.md`](phase_design/PHASE4_DESIGN_RECONSTRUCTED.md) *(Retrospective)* | [`models/phase4/baseline.yaml`](../models/phase4/baseline.yaml), [`src/stegoceras_biomechanics/fea/`](../src/stegoceras_biomechanics/fea/) (`solver.py`, `meshing.py`, `loads.py`, `boundary_conditions.py`, `solve_production.py`) | [`tests/test_phase4_fea.py`](../tests/test_phase4_fea.py) (manufactured displacement field, work-energy identity, mesh Jacobian audit) | Canonical master surface $G_0$ ([`data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`](../data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl), SHA-256 `5adcf536...`) | [`results/phase4/mesh_convergence_comparison.json`](../results/phase4/mesh_convergence_comparison.json), [`data/metadata/phase4_mesh_metrics_*.json`](../data/metadata/) | [`reports/phase4_fea_benchmark_report.md`](../reports/phase4_fea_benchmark_report.md) | Decisions [`D003`–`D006`](DECISIONS.md)<br>• **Exec**: `b7aa8d0`<br>• **Report**: `15a342f` |
| **Phase 5 Gate A** (DICOM Ingestion & Header Audit) | Is the MorphoSource UALVP 2 cranium series (Media 000018283) an intact, uncorrupted, geometrically documented micro-CT series matching the physical specimen, and what are its precise spatial and intensity semantics? | [`docs/phase_design/PHASE5_GATE_A_DESIGN.md`](phase_design/PHASE5_GATE_A_DESIGN.md) *(Retrospective)* | Extraction & verification routines; [`data/metadata/dataset_manifest.yaml`](../data/metadata/dataset_manifest.yaml) | [`tests/test_gate_a_dicom.py`](../tests/test_gate_a_dicom.py) (per-slice SHA-256, geometry, 16-bit semantics, archive integrity) | MorphoSource Media `000018283` download ZIP (`bde34772...`); inner DICOM ZIP (`03f0d2c...`) | [`data/metadata/dicom_slice_manifest.json`](../data/metadata/dicom_slice_manifest.json) (514 slices cataloged) | [`reports/phase5_gate_a_dicom_report.md`](../reports/phase5_gate_a_dicom_report.md) | Model Decision Basis v1 §4.1<br>• **Exec**: `5f575d8`<br>• **Report**: `1c7a125` |
| **Phase 5 Gate B** (CT-to-Surface Registration & Empirical Scale Verification) | What is the physical scale and spatial registration relationship between canonical surface $G_0$ and the micro-CT volume, does empirical registration support unit scale ($s = 1.000000$), and does $G_0$ match the outer periosteal bone boundary? | [`docs/phase_design/PHASE5_GATE_B_DESIGN.md`](phase_design/PHASE5_GATE_B_DESIGN.md) *(Retrospective)* | [`scripts/register_ct_to_surface.py`](../scripts/register_ct_to_surface.py) (Kabsch rigid fit, Umeyama scale diagnostic, point-to-plane ICP, Flying Edges isosurface, KDTree distance metrics) | [`tests/test_gate_b_registration.py`](../tests/test_gate_b_registration.py) (mandated rigid scale, free-scale diagnostic, zero-based DICOM mapping, boundary residuals) | Canonical surface $G_0$; 514 cranium DICOM slices; [`data/metadata/gate_b_landmark_provenance.json`](../data/metadata/gate_b_landmark_provenance.json) | [`results/phase5/gate_b_registration_metrics.json`](../results/phase5/gate_b_registration_metrics.json) | [`reports/phase5_gate_b_registration_report.md`](../reports/phase5_gate_b_registration_report.md) | Decision [`D010`](DECISIONS.md)<br>• **Exec**: `ca32eba`<br>• **Report**: `fa0cf58` |
| **Phase 5 Gate C** (Image Semantics & Attenuation Characterization) *(ACTIVE NEXT)* | What are the numerical image semantics, attenuation dynamic range, artifact profiles, and tissue contrast distributions in the CT volume, and do they support or refute discrete radiological zonation in the dome? | [`docs/phase_design/PHASE5_GATE_C_DESIGN.md`](phase_design/PHASE5_GATE_C_DESIGN.md) *(Prospective)* | `scripts/characterize_image_semantics.py` *(planned)* | `tests/test_gate_c_semantics.py` *(planned)* | 514 cranium DICOM slices; Gate B coordinate alignment $\mathbf{T}_{\text{composite}}$; canonical mesh $G_0$ | `results/phase5/gate_c_semantics_metrics.json` *(planned)* | `reports/phase5_gate_c_semantics_report.md` *(planned)* | Expected Decision `D011`<br>• **Exec**: *(Pending)*<br>• **Report**: *(Pending)* |

---

## 🔬 3. Computational Reproducibility Standard

For every computational phase or gate reported in this repository, enough information must be preserved to answer the fundamental audit question:
> **"What exact computation produced this reported result?"**

Every reported scientific result must be traceable to the following minimal tuple:

1. **Exact Execution Commit**: The repository commit SHA at which the simulation, extraction, or registration code ran and generated the machine-readable results.
2. **Exact Report / Documentation Commit**: The repository commit SHA containing the finalized scientific report and interpretation.
3. **Executable Entry Point**: The exact script, test, or CLI command run to execute the computation (e.g. `scripts/register_ct_to_surface.py` or `python -m stegoceras_biomechanics.fea.solve_production --tier fine`).
4. **Reusable Source Modules**: The specific packages in `src/stegoceras_biomechanics/` that provided the mathematical algorithms (e.g. `fea/solver.py`, `fea/meshing.py`).
5. **Input Artifacts & Provenance**: Absolute or repo-relative paths to all input datasets, surface meshes, and landmark databases, including their cryptographic SHA-256 hashes.
6. **Configuration & Parameters**: Explicit YAML configuration files (e.g. `models/phase4/baseline.yaml`) recording material constants, solver tolerances, mesh volume bounds, and boundary node selections.
7. **Automated Verification Tests**: The regression tests in `tests/` that verify the computational invariants and numerical tolerances.
8. **Machine-Readable Result Artifacts**: The raw, unformatted JSON or NPZ files in `results/` or `simulations/` holding the exact floating-point outputs.
9. **Formal Report**: The markdown document in `reports/` analyzing and interpreting the computational results in light of the original scientific design.
10. **Decision Record**: The durable entry in `docs/DECISIONS.md` establishing the architectural or scientific policy following from the results.

> [!IMPORTANT]
> **Core Provenance Rule**: Numerical results must identify the commit that generated them; reports must separately identify the commit containing the final report. Because scientific interpretation and report prose can be refined after computation completes, conflating execution commits with documentation commits is strictly avoided.

---

## 🚫 4. Architectural Invariants

1. **No Conflation of Scientific Interpretation and Code**:
   Scientific conclusions belong in `reports/` and `docs/DECISIONS.md`. Source code docstrings in `src/` describe computational capabilities, algorithms, inputs, outputs, and mathematical formulas—not biological conclusions.
2. **No Orphan Results**:
   Every JSON or NPZ file in `results/` must be generated by an identifiable script or test, documented in a formal report, and referenced in this traceability matrix.
3. **No Phantom Inputs**:
   No computation may rely on untracked manual GUI clicks, uncommitted local scratch files, or undocumented external APIs. All inputs must reside in `data/` with cryptographic hashes logged in `data/metadata/`.
4. **Separation of Design and Execution**:
   Design documents in `docs/phase_design/` record the prospective experimental design and hypotheses *before* execution. When retrospective reconstructions are necessary for historical phases, they are explicitly labeled as retrospective.

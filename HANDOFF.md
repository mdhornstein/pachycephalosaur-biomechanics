# PROJECT HANDOFF

**Date**: 2026-09-24  
**Phase Transition Baseline**: `15a342f` (Phase 4 FE Freeze) & `2662be0` (Literature Basis v1 Freeze)  
**Current Git State**: Dynamic — interrogate directly via `git rev-parse HEAD`  
**Current Phase**: Phase 4, Literature Basis v1, Phase 5 Gate A & Gate B **FROZEN**; Phase 5 Gate C (Image Semantics & Attenuation Characterization) **ACTIVE NEXT GATE**  
**Lead Specimen**: *Stegoceras validum* UALVP 2 (Cast from micro-CT reconstructed cranium)

> [!IMPORTANT]
> **Authority & Orientation Notice**:
> This document is the fast, living operational entry point for incoming humans and AI agents. It reflects current reality at HEAD. For historical milestones, see [`docs/snapshots/`](docs/snapshots/). For repository documentation conventions and rules, see [`docs/DOCUMENTATION_SYSTEM.md`](docs/DOCUMENTATION_SYSTEM.md). For the formal scientific requirements translating literature into computational models, see [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](docs/LITERATURE_TO_MODEL_DECISIONS.md). Do not infer the current computational implementation from historical phase reports. For scientific review, independently inspect current code, configurations, and numerical artifacts rather than treating this handoff text as proof.

---

## 🎯 Scientific Objective
Quantify cranial stress distribution, compliance, and strain energy absorption in *Stegoceras validum* under dome impact loading using 3D finite element analysis (FEA), and evaluate whether introducing evidence-based internal material architecture materially alters compliance, strain energy distribution, and stress transmission/redistribution to the endocranial braincase relative to a homogeneous control. In accordance with Model Decision Basis v1, conditional mechanical response is evaluated across structured loading and boundary scenarios, strictly distinguishing computational mechanics from behavioral or evolutionary inferences.

---

## 📍 Current State
1. **Phase 4 Baseline Complete & Frozen (`15a342f`)**:
   - **Model A** (surface-derived, homogeneous isotropic compact bone: $E = 17.0\text{ GPa}, \nu = 0.30$) verified and solved across a 3-tier pure volumetric $h$-refinement hierarchy (423k, 540k, 825k tetrahedral elements).
   - **All Solves Complete**: Free DOFs up to 497,907 solved via direct sparse LU factorization (`scipy.sparse.linalg.spsolve`) without out-of-memory errors or swap thrashing.
   - **Dorsal Load Patch Verified**: Surface-connected dual-graph Dijkstra wavefront algorithm strictly confined to the dorsal dome ($Z \ge 80.0\text{ mm}$, single connected component, zero ventral/internal penetration).
   - **Static Equilibrium Confirmed**: Normalized force and moment residuals $\le 1.53 \times 10^{-12}$ (machine precision).
2. **Literature Basis v1 & Model Decision Basis v1 Frozen**:
   - Core literature citations and the evidence chain have been audited and corrected sufficiently to freeze Literature Basis v1 ([`literature/stegoceras_biomechanics_literature_synthesis.md`](literature/stegoceras_biomechanics_literature_synthesis.md), [`literature/LITERATURE_CORRECTIONS.md`](literature/LITERATURE_CORRECTIONS.md)); residual peripheral records remain explicitly marked where verification is incomplete.
   - Model decisions bridge specification codified in [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](docs/LITERATURE_TO_MODEL_DECISIONS.md) as **Model Decision Basis v1** (17-decision register D01–D17 and 7 experimental gates A–G; legacy draft preserved in [`docs/archive/`](docs/archive/)).

---

## ✅ What is Verified
- **Boundary Surface Integrity**: Single immutable canonical surface $G_0$ (`data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`, SHA-256: `5adcf53696268578f083ea29f7f4665c0faf1b41e6362ac858c8a5a7a50d62e2`). Zero per-tier decimation (`decimate_reduction: 0.0`).
- **Global Compliance & Displacement Stabilization**:
  - Total strain energy ($U$): $15.614 \to 15.713 \to 15.746\text{ mJ}$ ($+0.85\%$ net, $+0.21\%$ final step).
  - Apex displacement ($u_{\text{apex}}$): $37.41 \to 37.68 \to 37.93\ \mu\text{m}$ ($+1.39\%$ net, $+0.66\%$ final step).
- **Dorsal Dome Stress Stabilization**:
  - Frontoparietal dome apex 95th% von Mises stress: $3.399 \to 3.355 \to 3.334\text{ MPa}$ ($-1.92\%$ net, $-0.63\%$ final step, converging smoothly).
- **Pipeline Architecture Decoupled**:
  - [`src/stegoceras_biomechanics/fea/solve_production.py`](src/stegoceras_biomechanics/fea/solve_production.py): Standalone CLI driver executing one solve per isolated subprocess, writing `.npz` and `.json` artifacts before exiting.
  - [`src/stegoceras_biomechanics/fea/plot_results.py`](src/stegoceras_biomechanics/fea/plot_results.py): Pure visualization consumer (<10s, <250 MB RAM). Hard invariant: never calls the solver or generates meshes.
- **Automated Tests**: 100% passing test suite in [`tests/test_phase4_fea.py`](tests/test_phase4_fea.py).

---

## ⚠️ Known Limitations & Open Questions
- **Localized Stress Discretization Sensitivity**:
  - Unlike the dorsal dome and global compliance, internal stress fields remain discretization-sensitive:
    - Global 95th% von Mises stress shifted $-18.10\%$ across tiers ($2.493 \to 2.290 \to 2.042\text{ MPa}$).
    - Endocranial braincase roof 95th% stress shifted $-28.64\%$ across tiers ($2.823 \to 2.383 \to 2.015\text{ MPa}$; step deltas $-15.59\%$ and $-15.46\%$).
  - **Scientific Decision**: Do not pursue intractable multi-million element solves on workstation hardware. Rather, carry this characterized numerical sensitivity forward as an output-specific numerical discretization discrepancy ($\Delta_{\text{num}} = -28.64\%$ across $h_1 \to h_3$), avoiding symmetric error-bound notation or treating discretization error as biological uncertainty (Decisions D006, D009).
- **Homogeneous Material Simplification**:
  - Model A treats the cranium as a uniform compact bone block ($E = 17.0\text{ GPa}$). The audited literature demonstrates internal anatomical heterogeneity (cortex, vascular cancellous core, dense basicranium). Model A serves strictly as a geometric control baseline.

---

## 🔮 Next Recommended Action
**Do NOT deploy an unmotivated 48-point LHS campaign.**  
Per [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](docs/LITERATURE_TO_MODEL_DECISIONS.md), execute **Phase 5: UALVP 2 CT Characterization & The Decisive Material A/B Experiment**:
1. **Gate A — Acquire & Ingest DICOM Volume**: **VERIFIED & FROZEN** ([`reports/phase5_gate_a_dicom_report.md`](reports/phase5_gate_a_dicom_report.md); 514 slices verified, true voxel spacing $0.207572 \times 0.207572 \times 0.250000\text{ mm}$, unsigned 16-bit intensity $[0, 65535]$, manifest in [`data/metadata/dicom_slice_manifest.json`](data/metadata/dicom_slice_manifest.json)).
2. **Gate B — Verify Physical Scale & Coordinates**: **VERIFIED & FROZEN** ([`reports/phase5_gate_b_registration_report.md`](reports/phase5_gate_b_registration_report.md); rigid registration at unit scale $s = 1.000000$ supported by free-scale diagnostic $\hat{s} = 1.00494$, primary forward median surface residual $0.1633\text{ mm}$, whole-volume reverse diagnostic median $1.0928\text{ mm}$, translation magnitude $0.2472\text{ mm}$ [below $0.25\text{-mm}$ through-plane spacing], zero-based DICOM voxel-center convention directly from `ImagePositionPatient`, objective Otsu threshold $T = 20,864$, metrics in [`results/phase5/gate_b_registration_metrics.json`](results/phase5/gate_b_registration_metrics.json)).
3. **Gate C — Characterize Image Data Semantics (ACTIVE NEXT GATE)**: Quantify stored pixel values, dynamic range, beam hardening, rock matrix vs. bone contrast, and internal architecture visibility (without assuming values are Hounsfield Units) per design in [`docs/phase_design/PHASE5_GATE_C_DESIGN.md`](docs/phase_design/PHASE5_GATE_C_DESIGN.md).
4. **Gate D — Reconstruct Published Material Inference Logic**: Document what Snively & Theodor (2011) directly observed from CT vs. what was assumed or thresholded.
5. **Gate E — Formulate Minimal Model B**: Define candidate 3-zone architecture supported by evidence; assign elementwise properties to $h_3$ volume mesh.
6. **Gate F — Execute Decisive Model A vs. Model B Test**: Compare Model A against Model B under identical $h_3$ mesh, loads, and BCs to evaluate stress redistribution to the endocranial braincase roof and strain energy partitioning.
7. **Gate G — Effect-Size & Model-Form Evaluation**: Branch into structured sensitivity scenarios (impact angle, material contrast ratios, cervical compliance).

---

## 📚 Information Architecture & Authority Hierarchy
*(Detailed specifications in [`docs/DOCUMENTATION_SYSTEM.md`](docs/DOCUMENTATION_SYSTEM.md))*

Never make the same technical fact authoritative in two places:
1. **Level 1: Technical Truth (Code, Configs, & Data Artifacts)**:
   - Executable baseline: [`models/phase4/baseline.yaml`](models/phase4/baseline.yaml)
   - Mesh metadata: [`data/metadata/phase4_mesh_metrics_*.json`](data/metadata/)
   - Authoritative solve results: [`results/phase4/mesh_convergence_comparison.json`](results/phase4/mesh_convergence_comparison.json)
   - Solution arrays: `simulations/phase4/solution_*.npz`
2. **Level 2: Current Scientific Interpretation**:
   - Comprehensive living state: [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md)
   - Master research traceability: [`docs/RESEARCH_TRACEABILITY.md`](docs/RESEARCH_TRACEABILITY.md)
   - Phase/gate scientific designs: [`docs/phase_design/`](docs/phase_design/)
3. **Level 3: Operational Handoff & Roadmap**:
   - Living entry point: [`HANDOFF.md`](HANDOFF.md)
   - Forward research roadmap: [`PLAN.md`](PLAN.md)
4. **Level 4: Historical Record & Scientific Archive**:
   - Append-only decision log: [`docs/DECISIONS.md`](docs/DECISIONS.md)
   - Milestone snapshots: [`docs/snapshots/2026-09-19-phase4-freeze.md`](docs/snapshots/2026-09-19-phase4-freeze.md)
   - Formal milestone reports: [`reports/phase4_fea_benchmark_report.md`](reports/phase4_fea_benchmark_report.md)
   - Preserved archives: [`reports/archive/phase4_walkthrough_legacy.md`](reports/archive/phase4_walkthrough_legacy.md)

---

## 👥 How to Work
- **Coding Agent**: Start by reading [`HANDOFF.md`](HANDOFF.md), then check [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md). Always ensure tests pass. When completing a milestone, update `CURRENT_STATE.md`, `HANDOFF.md`, log decisions in `docs/DECISIONS.md`, and generate a snapshot in `docs/snapshots/`.
- **Review Agent**: Treat `HANDOFF.md` as orientation, not ground truth. Independently verify claims against current git HEAD, test executions, and JSON/NPZ data artifacts. Check for stale numbers and internal consistency.
- **Human**: Direct high-level priorities and review proposed specifications in `docs/` before authorizing new simulation campaigns.

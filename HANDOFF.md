# PROJECT HANDOFF

**Date**: 2026-09-24  
**Phase Transition Baseline**: `15a342f` (Phase 4 FE Freeze) & `2662be0` (Literature Basis v1 Freeze)  
**Current Git State**: Dynamic — interrogate directly via `git rev-parse HEAD`  
**Current Phase**: Phase 4 & Literature Basis v1 **FROZEN**; Phase 5 (UALVP 2 CT Characterization & Material A/B Experiment) **ACTIVE NEXT GATE**  
**Lead Specimen**: *Stegoceras validum* UALVP 2 (Cast from micro-CT reconstructed cranium)

> [!IMPORTANT]
> **Authority & Orientation Notice**:
> This document is the fast, living operational entry point for incoming humans and AI agents. It reflects current reality at HEAD. For historical milestones, see [`docs/snapshots/`](docs/snapshots/). For repository documentation conventions and rules, see [`docs/DOCUMENTATION_SYSTEM.md`](docs/DOCUMENTATION_SYSTEM.md). For the formal scientific requirements translating literature into computational models, see [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](docs/LITERATURE_TO_MODEL_DECISIONS.md). Do not infer the current computational implementation from historical phase reports. For scientific review, independently inspect current code, configurations, and numerical artifacts rather than treating this handoff text as proof.

---

## 🎯 Scientific Objective
Quantify cranial stress distribution, compliance, and energy absorption in *Stegoceras validum* under dome impact loading using 3D finite element analysis (FEA), and rigorously determine via Uncertainty Quantification (UQ) and Global Sensitivity Analysis (Sobol indices) whether the frontoparietal dome acts as a protective shock-absorbing helmet shielding the endocranial braincase, or if stress concentrations favor alternative biological hypotheses (flank-butting, visual sexual display).

---

## 📍 Current State
1. **Phase 4 Baseline Complete & Frozen (`15a342f`)**:
   - **Model A** (surface-derived, homogeneous isotropic compact bone: $E = 17.0\text{ GPa}, \nu = 0.30$) verified and solved across a 3-tier pure volumetric $h$-refinement hierarchy (423k, 540k, 825k tetrahedral elements).
   - **All Solves Complete**: Free DOFs up to 497,907 solved via direct sparse LU factorization (`scipy.sparse.linalg.spsolve`) without out-of-memory errors or swap thrashing.
   - **Dorsal Load Patch Verified**: Surface-connected dual-graph Dijkstra wavefront algorithm strictly confined to the dorsal dome ($Z \ge 80.0\text{ mm}$, single connected component, zero ventral/internal penetration).
   - **Static Equilibrium Confirmed**: Normalized force and moment residuals $\le 1.53 \times 10^{-12}$ (machine precision).
2. **Literature Basis v1 Complete & Frozen (`2662be0`)**:
   - Canonical synthesis ([`literature/stegoceras_biomechanics_literature_synthesis.md`](literature/stegoceras_biomechanics_literature_synthesis.md)), dossiers, and audit-to-correction ledger ([`literature/LITERATURE_CORRECTIONS.md`](literature/LITERATURE_CORRECTIONS.md)) fully resolved.
   - Model decisions bridge specification codified in [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](docs/LITERATURE_TO_MODEL_DECISIONS.md).

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
  - **Scientific Decision**: Do not pursue intractable multi-million element solves on workstation hardware. Rather, carry this characterized numerical sensitivity forward as a formal numerical discretization discrepancy ($\epsilon_{\text{num}} \approx \pm 28.6\%$).
- **Homogeneous Material Simplification**:
  - Model A treats the cranium as a uniform compact bone block ($E = 17.0\text{ GPa}$). The audited literature proves that UALVP 2 has structured internal architecture (cortex, vascular cancellous core, dense basicranium). Model A serves strictly as a geometric control baseline.

---

## 🔮 Next Recommended Action
**Do NOT deploy an unmotivated 48-point LHS campaign.**  
Per [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](docs/LITERATURE_TO_MODEL_DECISIONS.md), execute **Phase 5: UALVP 2 CT Characterization & The Decisive Material A/B Experiment**:
1. **Acquire & Ingest DICOM Volume**: Ingest the 514-slice, $0.210 \times 0.210 \times 0.250\text{ mm}$ primary micro-CT scan of UALVP 2.
2. **Verify Physical Scale & Coordinates**: Register the voxel grid against the canonical surface mesh ($G_0$).
3. **Characterize Image Data Semantics**: Quantify pixel values, beam hardening, rock matrix vs. bone contrast, and internal architecture visibility.
4. **Reconstruct Published Material Inference Logic**: Document what Snively & Theodor (2011) inferred from CT vs. what was assumed.
5. **Execute Decisive Model A vs. Model B Test**: Compare Model A against Model B (histology-informed 3-zone model) under identical mesh, loads, and BCs to determine if internal zonation materially alters braincase stress attenuation.

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

# PROJECT HANDOFF

**Date**: 2026-09-19  
**Phase Transition Baseline**: `15a342f` (Phase 4 Freeze & Scientific Baseline)  
**Current Git State**: Dynamic — interrogate directly via `git rev-parse HEAD`  
**Current Phase**: Phase 4 **FROZEN**; Phase 5 (Uncertainty Quantification & Sensitivity Design) **DESIGN PENDING — NEXT GATE**  
**Lead Specimen**: *Stegoceras validum* UALVP 2 (Cast from micro-CT reconstructed cranium)

> [!IMPORTANT]
> **Authority & Orientation Notice**:
> This document is the fast, living operational entry point for incoming humans and AI agents. It reflects current reality at HEAD. For historical milestones, see [`docs/snapshots/`](docs/snapshots/). For repository documentation conventions and rules, see [`docs/DOCUMENTATION_SYSTEM.md`](docs/DOCUMENTATION_SYSTEM.md). Do not infer the current computational implementation from historical phase reports. For scientific review, independently inspect current code, configurations, and numerical artifacts rather than treating this handoff text as proof.

---

## 🎯 Scientific Objective
Quantify cranial stress distribution, compliance, and energy absorption in *Stegoceras validum* under dome impact loading using 3D finite element analysis (FEA), and rigorously determine via Uncertainty Quantification (UQ) and Global Sensitivity Analysis (Sobol indices) whether the frontoparietal dome acts as a protective shock-absorbing helmet shielding the endocranial braincase, or if stress concentrations favor alternative biological hypotheses (flank-butting, visual sexual display).

---

## 📍 Current State
1. **Phase 4 Baseline Complete & Frozen**:
   - **Model A** (surface-derived, homogeneous isotropic compact bone: $E = 17.0\text{ GPa}, \nu = 0.30$) verified and solved across a 3-tier pure volumetric $h$-refinement hierarchy (423k, 540k, 825k tetrahedral elements).
   - **All Solves Complete**: Free DOFs up to 497,907 solved via direct sparse LU factorization (`scipy.sparse.linalg.spsolve`) without out-of-memory errors or swap thrashing.
   - **Dorsal Load Patch Verified**: Surface-connected dual-graph Dijkstra wavefront algorithm strictly confined to the dorsal dome ($Z \ge 80.0\text{ mm}$, single connected component, zero ventral/internal penetration).
   - **Static Equilibrium Confirmed**: Normalized force and moment residuals $\le 1.53 \times 10^{-12}$ (machine precision).

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
  - **Scientific Decision**: Do not pursue intractable multi-million element solves on workstation hardware. Rather, carry this characterized numerical sensitivity forward into Phase 5 as a formal numerical model-form uncertainty component ($\epsilon_{\text{num}} \approx \pm 28.6\%$) to assess whether biological variation dominates over numerical discretization error.

---

## 🔮 Next Recommended Action
**Do NOT jump into brute-force Monte Carlo simulations.**  
Author the formal **Phase 5 UQ & Sensitivity Specification** (`docs/phase5_uq_specification.md`):
1. Define biologically defensible distributions for uncertain parameters ($E, \nu, s, A, \alpha$).
2. Factorize linear dimensions (scale $F$ and $E$ analytically without solver re-runs).
3. Design a sample-efficient Design of Experiments (DoE) (e.g. 20–32 LHS / Sobol points) across the non-linear geometric/boundary dimensions ($A, \alpha, \nu, s$).
4. Plan the Gaussian Process surrogate modeling and Sobol variance decomposition.

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

# Milestone Snapshot: Phase 4 Baseline Freeze

**Date**: 2026-09-19  
**Git Commit**: `e3ba976`  
**Milestone**: Phase 4 Deterministic FEA Benchmark Frozen for Phase 5 UQ Transition  
**Specimen**: *Stegoceras validum* UALVP 2  

---

## 1. Scientific & Computational State at Freeze
Phase 4 (Surface-Derived Finite Element Benchmark) is formally verified and frozen. The baseline computational model (**Model A**) has been implemented, verified against analytical mechanics (Hookean linearity and quadratic strain energy scaling), and solved across a 3-tier pure volumetric $h$-refinement hierarchy.

Static equilibrium is satisfied to machine precision ($r_F \le 1.53 \times 10^{-12}, r_M \le 3.13 \times 10^{-12}$). The loading formulation has been corrected to a surface dual-graph Dijkstra wavefront algorithm, eliminating the historical ventral penetration failure mode.

---

## 2. Frozen Model Definition (Model A)
- **Geometry**: Canonical master surface $G_0$ (`stegoceras_ualvp2_canonical_master.stl`, SHA-256: `5adcf53696268578f083ea29f7f4665c0faf1b41e6362ac858c8a5a7a50d62e2`).
- **Material**: Homogeneous isotropic compact bone ($E = 17.0\text{ GPa}, \nu = 0.30$).
- **Boundary Constraints**:
  - Occipital condyle: Rigid translational fixity ($u_x = u_y = u_z = 0$) across 139 nodes within $R = 12.0\text{ mm}$ sphere at the posterior-ventral articular condyle margin (centroid $[104.64, 178.06, 40.13]\text{ mm}$).
  - Nuchal crest rim: Translational restraint in longitudinal and vertical DOFs ($u_y = u_z = 0$) across 702 posterior nuchal nodes at the squamosal-parietal shelf (centroid $[116.98, 190.23, 82.40]\text{ mm}$).
- **Load Patch**:
  - Dual-graph Dijkstra wavefront starting from dorsal apex seed facet ($[106.14, 110.51, 110.37]\text{ mm}$), restricted to candidate facets $Z \ge 60.0\text{ mm}, Y \ge 70.0\text{ mm}$.
  - Target area: $3,000.0\text{ mm}^2$; realized area: $3,000.02\text{ mm}^2$ (1,406 triangles, 808 loaded nodes; centroid $[108.40, 104.33, 101.97]\text{ mm}$).
  - Hard constraint: 100% of loaded nodes have $Z \ge 80.0\text{ mm}$; 1 connected component; 0% ventral load.
  - Resultant Force: $F_z = -1,000.0\text{ N}$ ($1.0\text{ kN}$ broad compressive load).

---

## 3. Numerical Verification Results

| Observable ($Q$) | Coarse ($h_1$, 423k) | Med-Coarse ($h_2$, 540k) | Medium ($h_3$, 825k) | Step $\Delta_{1 \to 2}$ | Step $\Delta_{2 \to 3}$ | Total Net $\Delta$ | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Nodes ($N_{\text{node}}$)** | 99,614 | 118,577 | 165,969 | $+19.0\%$ | $+40.0\%$ | $+66.6\%$ | Production grid |
| **Elements ($N_{\text{elem}}$)** | 422,573 | 540,310 | 825,277 | $+27.9\%$ | $+52.7\%$ | $+95.3\%$ | Pure $h$-refinement |
| **Free DOFs** | 298,842 | 355,731 | 497,907 | $+19.0\%$ | $+40.0\%$ | $+66.6\%$ | Direct sparse solve |
| **Total Strain Energy ($U$)** | **$15.614\text{ mJ}$** | **$15.713\text{ mJ}$** | **$15.746\text{ mJ}$** | **$+0.64\%$** | **$+0.21\%$** | **$+0.85\%$** | **STABILIZED** ($\le 1\%$) |
| **Apex Disp. ($u_{\text{apex}}$)** | **$37.41\ \mu\text{m}$** | **$37.68\ \mu\text{m}$** | **$37.93\ \mu\text{m}$** | **$+0.72\%$** | **$+0.66\%$** | **$+1.39\%$** | **STABILIZED** ($\le 2\%$) |
| **Max Disp. ($\delta_{\max}$)** | **$59.07\ \mu\text{m}$** | **$59.12\ \mu\text{m}$** | **$59.75\ \mu\text{m}$** | **$+0.08\%$** | **$+1.07\%$** | **$+1.15\%$** | **STABILIZED** ($\le 2\%$) |
| **Dome Apex 95th% Stress** | **$3.399\text{ MPa}$** | **$3.355\text{ MPa}$** | **$3.334\text{ MPa}$** | **$-1.30\%$** | **$-0.63\%$** | **$-1.92\%$** | **STABILIZED** |
| **Global 95th% Stress** | **$2.493\text{ MPa}$** | **$2.290\text{ MPa}$** | **$2.042\text{ MPa}$** | **$-8.14\%$** | **$-10.84\%$** | **$-18.10\%$** | **DISCRETIZATION-SENSITIVE** |
| **Braincase Roof 95th% Stress** | **$2.823\text{ MPa}$** | **$2.383\text{ MPa}$** | **$2.015\text{ MPa}$** | **$-15.59\%$** | **$-15.46\%$** | **$-28.64\%$** | **DISCRETIZATION-SENSITIVE** |
| **Force Residual ($r_F$)** | **$8.91 \times 10^{-13}$** | **$9.20 \times 10^{-13}$** | **$1.53 \times 10^{-12}$** | Machine prec. | Machine prec. | Machine prec. | **EXACT EQUILIBRIUM** |
| **Moment Residual ($r_M$)**| **$3.13 \times 10^{-12}$** | **$7.87 \times 10^{-13}$** | **$7.23 \times 10^{-13}$** | Machine prec. | Machine prec. | Machine prec. | **EXACT EQUILIBRIUM** |
| **Solver Runtime** | **$72.7\text{ s}$** | **$310.9\text{ s}$** | **$2,055.3\text{ s}$ (34 min)**| $4.28\times$ | $6.61\times$ | $28.28\times$ | Clean isolated process |

---

## 4. Known Limitations Carried into Phase 5
- Global compliance ($U$), displacement ($u_{\text{apex}}, \delta_{\max}$), and dorsal dome stress are stabilized to $<2\%$ across the tested hierarchy.
- Localized stress in internal cavities (endocranial braincase roof and global p95) has not asymptotically converged ($-18.1\%$ and $-28.6\%$ net shifts).
- Rather than pursuing intractable laptop-scale direct solves on multi-million-element meshes, this characterized sensitivity is carried forward into Phase 5 as numerical model-form uncertainty ($\epsilon_{\text{num}} \approx \pm 28.6\%$).

---

## 5. Decisions Enacted at Freeze
- `D001`: Primary specimen UALVP 2.
- `D002`: Model A homogeneous benchmark established.
- `D003`: Canonical master surface $G_0$ with zero decimation.
- `D004`: Dual-graph Dijkstra wavefront load patch.
- `D005`: Architectural separation of `solve_production.py` and `plot_results.py`.
- `D006`: Propagate internal stress discretization sensitivity into Phase 5 UQ.

---

## 6. Authoritative Artifacts at Freeze
- Model Baseline Config: [`models/phase4/baseline.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/baseline.yaml)
- Mesh Convergence JSON: [`results/phase4/mesh_convergence_comparison.json`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/results/phase4/mesh_convergence_comparison.json)
- Subregion Metrics JSON: [`results/phase4/ualvp2_1kn_subregion_metrics.json`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/results/phase4/ualvp2_1kn_subregion_metrics.json)
- Milestone Synthesis Report: [`reports/phase4_fea_benchmark_report.md`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/phase4_fea_benchmark_report.md)
- Solution Arrays: `simulations/phase4/solution_{coarse,medium_coarse,medium}.npz`

# Phase 4 Design (Retrospective Reconstruction): Surface-Derived FEA Benchmark & Discretization Sensitivity

> [!NOTE]
> **Retrospective Reconstruction**: This document reconstructs the scientific design intent for Phase 4 based on contemporaneous milestone artifacts, commits `8c94bbe` through `15a342f`, [`reports/phase4_fea_benchmark_report.md`](../../reports/phase4_fea_benchmark_report.md), [`models/phase4/baseline.yaml`](../../models/phase4/baseline.yaml), [`results/phase4/mesh_convergence_comparison.json`](../../results/phase4/mesh_convergence_comparison.json), and Decisions `D003`–`D006`. It was codified during the Research Design & Traceability Milestone to preserve design intent without rewriting history.

**Document Role**: Retrospectively Reconstructed Phase Design  
**Status**: RETROSPECTIVELY RECONSTRUCTED & FROZEN  
**Governing Standard**: Model A Benchmark Specification / Decisions `D003`–`D006`  
**Specimen**: *Stegoceras validum* UALVP 2  
**Target Architecture**: Deterministic Linear Elastic FEM Pipeline  

---

## 1. Scientific Question
*Can a reproducible, mathematically verified 3D linear elastic finite element solver be constructed for the complex anatomical geometry of Stegoceras validum (UALVP 2) that satisfies strict static equilibrium and energy conservation, and how do global compliance versus localized internal stress fields respond under pure volumetric $h$-refinement on an immutable boundary surface?*

Specifically:
1. Does the numerical FEA implementation reproduce analytical solutions and manufactured displacement fields?
2. Does mesh refinement demonstrate asymptotic stabilization of global compliance ($U, u_{\text{apex}}$) and dorsal dome stress?
3. How sensitive are localized internal stress concentrations (e.g., endocranial braincase roof) to tetrahedral mesh density, and can that sensitivity be quantitatively characterized rather than concealed?

---

## 2. Motivation / Prior Evidence
- Phase 3 established the qualitative and quantitative target bounds for Model A under dorsal compression ($1.0\text{ kN}$ reference compliance and $1360\text{ N}$ biological load).
- Real anatomical geometries with complex curvature, thin basicranial arches, and internal foramina present severe meshing challenges (poor aspect ratios, inverted elements, non-physical boundary penetrations).
- A robust, verified numerical foundation is necessary before evaluating biological or material uncertainty.

---

## 3. Hypothesis or Competing Expectations
- **Hypothesis A (Standard Asymptotic Convergence)**: As element volume $-a$ is systematically reduced, all global and local displacement, strain energy, and stress fields will monotonically converge within standard engineering tolerances ($<5\%$).
- **Hypothesis B (Differentiated Observables Behavior)**: Global compliance ($U$) and dorsal dome summit stresses will stabilize rapidly, but localized internal stress concentrations around geometric notches and complex endocranial foramina will exhibit persistent discretization sensitivity, requiring explicit characterization as numerical discrepancy.

---

## 4. Scope
- **In Scope**:
  - Watertight 2-manifold surface repair of UALVP 2 cranium creating canonical master surface $G_0$.
  - Implementation of linear tetrahedral (Tet4) 3D elastostatics solver in Python/SciPy.
  - Surface dual-graph Dijkstra wavefront load patch restricted to the dorsal summit ($Z \ge 80\text{ mm}$).
  - Rigid multi-node kinematic boundary constraints at the occipital condyle and nuchal shelf.
  - 3-tier pure volumetric $h$-refinement hierarchy ($h_1$: 423k, $h_2$: 540k, $h_3$: 825k tets) under fixed surface boundary $G_0$.
  - Verification of static force/moment equilibrium, work-energy identity, and patch tests.
- **Explicitly Out of Scope**:
  - Non-linear material models, plasticity, or fracture mechanics.
  - Dynamic transient impact (quasi-static compression only).
  - Heterogeneous material property assignment (deferred to Phase 5).

---

## 5. Experimental / Computational Design

### 5.1 Variables Being Changed (Independent Variables)
- **Volumetric Discretization Density ($-a$)**: Maximum element volume constraint in TetGen:
  - Tier 1 Coarse ($h_1$): $-a = 0.50\text{ mm}^3$ ($\approx 423\text{k}$ elements)
  - Tier 2 Medium-Coarse ($h_2$): $-a = 0.35\text{ mm}^3$ ($\approx 540\text{k}$ elements)
  - Tier 3 Medium ($h_3$): $-a = 0.20\text{ mm}^3$ ($\approx 825\text{k}$ elements)

### 5.2 Variables Being Held Fixed (Controls)
- **Boundary Surface**: Canonical master surface $G_0$ (`stegoceras_ualvp2_canonical_master.stl`, SHA-256 `5adcf536...`) held strictly constant across all tiers (`decimate_reduction: 0.0`).
- **TetGen Quality Constraints**: Radius-edge ratio constraint $q = 1.5$, minimum dihedral angle $\theta_{\min} = 10.0^\circ$ held identical across all tiers.
- **Material Constants**: Homogeneous isotropic compact bone ($E = 17.0\text{ GPa}$, $\nu = 0.30$).
- **Load Patch**: Exactly identical surface facet and node cluster selected via dual-graph Dijkstra wavefront ($Z \ge 80.0\text{ mm}$).
- **Boundary Restraints**: Fixed displacement ($\mathbf{u} = \mathbf{0}$) on occipital condyle articular facet cluster and nuchal shelf rim.

### 5.3 Inputs & Upstream Artifacts
- **Canonical Mesh $G_0$**: [`data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`](../../data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl).
- **Executable Configuration**: [`models/phase4/baseline.yaml`](../../models/phase4/baseline.yaml).

### 5.4 Model Assumptions & Simplifications
- Linear elasticity with small displacement and infinitesimal strain assumptions (${\boldsymbol \varepsilon} = \frac{1}{2}(\nabla \mathbf{u} + \nabla \mathbf{u}^T)$).
- Linear tetrahedral elements (constant strain / stress within each element).

### 5.5 Numerical & Computational Methods
- **Solid Meshing**: TetGen Delaunay tetrahedralization constrained by PLC boundary.
- **Assembly**: Element stiffness matrix via 1-point Gauss quadrature (exact for linear tetrahedron).
- **Global Linear Solver**: SciPy direct sparse solver (`scipy.sparse.linalg.spsolve`) and preconditioned conjugate gradient (PCG) validation.

---

## 6. Acceptance / Discrimination Criteria
- **Static Equilibrium**: Net reaction force residual $r_F = \|\sum \mathbf{f}_{\text{ext}} + \sum \mathbf{r}\| / \|\sum \mathbf{f}_{\text{ext}}\| < 10^{-10}$; net moment residual $r_M < 10^{-10}$.
- **Work-Energy Identity**: Closeness of external work to internal strain energy: $|W_{\text{ext}} - U| / U < 10^{-6}$, where $W_{\text{ext}} = \frac{1}{2} \mathbf{F}^T \mathbf{u}$.
- **Mesh Quality**: Positive Jacobian determinants across 100% of solid elements ($V_{\text{tet}} > 0$).
- **Global Stability**: Shift in total strain energy ($U$) and peak displacement between successive refinement tiers $< 2.0\%$.

---

## 7. Interpretation Limits
- Phase 4 demonstrates numerical verification of the solver and characterizes discretization sensitivity on geometry $G_0$. It does **not** evaluate biological realism or validate against physical bone strain measurements.
- Localized stress concentrations in linear elasticity at concave sharp reentrant corners are theoretical singularities; element refinement increases peak stress. This is a known continuum mechanics limitation, not a numerical code defect.

---

## 8. Planned Computational Implementation
- **Configuration**: [`models/phase4/baseline.yaml`](../../models/phase4/baseline.yaml).
- **Meshing Pipeline**: [`src/stegoceras_biomechanics/fea/meshing.py`](../../src/stegoceras_biomechanics/fea/meshing.py).
- **Boundary & Load Formulation**: [`src/stegoceras_biomechanics/fea/boundary_conditions.py`](../../src/stegoceras_biomechanics/fea/boundary_conditions.py), [`src/stegoceras_biomechanics/fea/loads.py`](../../src/stegoceras_biomechanics/fea/loads.py).
- **Core Solver**: [`src/stegoceras_biomechanics/fea/solver.py`](../../src/stegoceras_biomechanics/fea/solver.py).
- **Execution Driver**: [`src/stegoceras_biomechanics/fea/solve_production.py`](../../src/stegoceras_biomechanics/fea/solve_production.py).
- **Post-Processing & Plotting**: [`src/stegoceras_biomechanics/fea/plot_results.py`](../../src/stegoceras_biomechanics/fea/plot_results.py).

---

## 9. Planned Verification
- **Unit & System Tests**: [`tests/test_phase4_fea.py`](../../tests/test_phase4_fea.py):
  - Element-level manufactured linear displacement field verification (exact recovery of constant strain tensor).
  - Analytical work-energy identity verification.
  - Strict positive Jacobian audit across all tiers.
  - Geodesic load patch dorsal confinement verification ($100\% \ge 80\text{ mm}$, zero ventral penetration).
  - Production mesh hierarchy parameterization regression test.

---

## 10. Planned Outputs & Artifacts
- **Primary Report**: [`reports/phase4_fea_benchmark_report.md`](../../reports/phase4_fea_benchmark_report.md).
- **Convergence Metrics JSON**: [`results/phase4/mesh_convergence_comparison.json`](../../results/phase4/mesh_convergence_comparison.json).
- **Mesh Metric Summaries**: [`data/metadata/phase4_mesh_metrics_*.json`](../../data/metadata/).
- **Solution Binary Arrays**: `simulations/phase4/solution_*.npz`.

---

## 11. Expected Decision Point
- Approve Decision `D003` (Pure volumetric $h$-refinement on canonical surface $G_0$).
- Approve Decision `D004` (Surface dual-graph Dijkstra wavefront load patch).
- Approve Decision `D005` (Strict decoupling of solve and plotting execution).
- Approve Decision `D006` (Propagate internal stress discretization sensitivity into Phase 5 UQ as characterized numerical discrepancy $\epsilon_{\text{num}} \approx \pm 28.6\%$).
- Freeze Phase 4 deterministic baseline at the $h_3$ tier.

---

## 12. Traceability
```text
Scientific Question (Model A FEA solver verification & discretization response)
       ↓
Reconstructed Design (docs/phase_design/PHASE4_DESIGN_RECONSTRUCTED.md)
       ↓
Implementation (src/stegoceras_biomechanics/fea/, models/phase4/baseline.yaml)
       ↓
Verification Suite (tests/test_phase4_fea.py)
       ↓
Result Artifacts (results/phase4/mesh_convergence_comparison.json)
       ↓
Scientific Report (reports/phase4_fea_benchmark_report.md)
       ↓
Decisions D003, D004, D005, D006 (docs/DECISIONS.md)
```

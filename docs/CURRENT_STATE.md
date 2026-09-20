# Current Scientific & Computational State

**Document Status**: Canonical Living State Document  
**Last Updated**: 2026-09-19  
**Corresponding Commit**: `15a342f`  
**Current Phase**: Phase 4 **FROZEN**; Phase 5 (UQ & Sensitivity Design) **PENDING DESIGN**

---

## 1. Scientific Objective
This investigation quantifies the mechanical behavior of the pachycephalosaur cranium under impact loading. The central evolutionary and biomechanical question is:

> **Did the hypertrophied frontoparietal dome of *Stegoceras validum* function as an effective shock-absorbing structure protecting the endocranial braincase during intra-specific head-strikes, or do stress concentrations and compliance characteristics support alternative behavioral hypotheses (flank-butting or visual display)?**

To answer this defensively, we must quantify not only deterministic stress fields, but also whether biological and kinematic uncertainties dominate over numerical discretization error.

---

## 2. Current Computational Model (Model A)
The project currently executes **Model A**:
- **Representation**: Surface-derived, fused monolithic continuum approximation inspired by Snively & Theodor (2011).
- **Material Assumption**: Homogeneous isotropic compact bone. (Serves as the uncompromised computational baseline to verify geometry, solver execution, load application, and discretization sensitivity before introducing multi-zone internal histological layering in later phases).

---

## 3. Geometry & Coordinate System
- **Specimen**: *Stegoceras validum* UALVP 2 (subadult/adult cranium).
- **Source Geometry**: High-resolution micro-CT scan surface repair.
- **Canonical Master Boundary Surface ($G_0$)**:
  - File: `data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`
  - Array SHA-256 (`source_surface_arrays_sha256`): `5adcf53696268578f083ea29f7f4665c0faf1b41e6362ac858c8a5a7a50d62e2`
  - Watertight 2-manifold surface, 0 non-manifold edges, 0 self-intersections.
  - Mesh Extents (mm):
    - $X \in [37.91, 169.20]$ (Mediolateral width $\approx 131.30\text{ mm}$, midsagittal symmetry plane centered at $X \approx 103.6\text{ mm}$)
    - $Y \in [4.20, 204.88]$ (Anteroposterior snout-to-occiput span $\approx 200.68\text{ mm}$; $Y \approx 4.2\text{ mm}$ anterior snout, $Y \approx 204.9\text{ mm}$ posterior condyle)
    - $Z \in [0.31, 128.15]$ (Dorsoventral palate-to-apex span $\approx 127.84\text{ mm}$; $Z \approx 0.3\text{ mm}$ ventral palate, $Z \approx 128.15\text{ mm}$ dorsal apex)
  - Anatomical Apex Seed: $X \approx 106.14\text{ mm}, Y \approx 110.51\text{ mm}, Z \approx 110.37\text{ mm}$ (identified within $Y \in [80, 150]\text{ mm}$ along midsagittal plane $X \approx 103.6\text{ mm}$).
  - Coordinate System: $+X$ right, $+Y$ posterior, $+Z$ dorsal.

---

## 4. Boundary Conditions & Support
- **Occipital Condyle**: Rigid translational fixity in all three DOFs ($u_x = u_y = u_z = 0$) across 139 nodes within a $12.0\text{ mm}$ radius sphere at the posterior-ventral condylar articular margin (centroid: $[104.64, 178.06, 40.13]\text{ mm}$).
- **Nuchal Crest Rim**: Translational restraint in longitudinal and vertical DOFs ($u_y = u_z = 0$) across 702 posterior nuchal nodes (centroid: $[116.98, 190.23, 82.40]\text{ mm}$) to represent cervical muscular and ligamentous bracing (m. complexus, lig. nuchae).
- **Equilibrium Verification**: Reaction forces and moments are computed via direct sparse matrix-vector multiplication $\mathbf{R} = \mathbf{K}\mathbf{u} - \mathbf{F}_{\text{ext}}$ across all restrained DOFs.

---

## 5. Loading Formulation
- **Algorithm**: Surface dual-graph Dijkstra wavefront algorithm starting from dorsal apex seed facet.
  - Edge cost: Euclidean distance between centroids of adjacent surface triangles.
  - Elevation restriction: All candidate facets restricted to $Z \ge 60.0\text{ mm}$ and $Y \ge 70.0\text{ mm}$.
  - Node assertion: Hard invariant that 100% of loaded nodes satisfy $Z \ge 80.0\text{ mm}$.
  - Connectivity assertion: Selected facets form exactly one connected topological component on the dorsal surface.
  - Ventral penetration: `0.00%` (verified eliminated).
- **Patch Properties**:
  - Target Area: $3,000.0\text{ mm}^2$ (Literature broad contact zone).
  - Selected Area: $3,000.02\text{ mm}^2$ ($+0.0007\%$ error).
  - Selected Faces: 1,406 triangles (808 loaded nodes on canonical surface).
  - Centroid: $[X=108.40, Y=104.33, Z=101.97]\text{ mm}$.
- **Load Vector**:
  - Total Compressive Force: $F_z = -1,000.0\text{ N}$ distributed uniformly by tributary nodal area.
  - Resultant Load: $[F_x = 0, F_y = 0, F_z = -1000.0\text{ N}]$.

---

## 6. Material Properties
- **Young's Modulus ($E$)**: $17.0\text{ GPa}$ ($17,000.0\text{ MPa}$). Standard vertebrate compact bone baseline (Rayfield 2007, Snively & Theodor 2011).
- **Poisson's Ratio ($\nu$)**: $0.30$. Standard isotropic bone value.
- **Epistemic Status**: Parameter-limited literature borrowing. Compact bone modulus across mammals/archosaurs spans $10\text{--}22\text{ GPa}$; this variation is explicitly scheduled for propagation in Phase 5 UQ.

---

## 7. Numerical Formulation & Pipeline Architecture
- **Element Formulation**: 4-node linear tetrahedral elements (Tet1, constant strain).
- **Constitutive Law**: Small-displacement, linear isotropic Hookean elasticity.
- **Solver**: Direct sparse LU decomposition via SuperLU (`scipy.sparse.linalg.spsolve`).
- **Discretization Hierarchy (Pure $h$-Refinement on Identical $G_0$)**:
  - Radius-edge ratio $q = 1.5$, minimum dihedral angle $\theta_{\min} = 10.0^\circ$ held strictly constant.
  - Decimation reduction: `0.0` (zero surface approximation across tiers).
  - Refinement driver: Max element volume constraint ($a_{\max} = \infty \to 5.0 \to 2.0 \to 1.0\text{ mm}^3$).
- **Software Architecture**:
  - [`solve_production.py`](../src/stegoceras_biomechanics/fea/solve_production.py): Standalone CLI executing one tier per isolated process. Writes `.npz` and `.json` artifacts, then terminates.
  - [`plot_results.py`](../src/stegoceras_biomechanics/fea/plot_results.py): Pure post-processing consumer. Never invokes the solver or Gmsh/TetGen.

---

## 8. Authoritative Empirical Results (1.0 kN Broad Load)

From [`results/phase4/mesh_convergence_comparison.json`](../results/phase4/mesh_convergence_comparison.json):

| Observable ($Q$) | Coarse ($h_1$, 423k) | Med-Coarse ($h_2$, 540k) | Medium ($h_3$, 825k) | Step $\Delta_{1 \to 2}$ | Step $\Delta_{2 \to 3}$ | Total Net $\Delta$ | Numerical Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Nodes ($N_{\text{node}}$)** | 99,614 | 118,577 | 165,969 | $+19.0\%$ | $+40.0\%$ | $+66.6\%$ | Production grid |
| **Elements ($N_{\text{elem}}$)** | 422,573 | 540,310 | 825,277 | $+27.9\%$ | $+52.7\%$ | $+95.3\%$ | Pure $h$-refinement |
| **Free DOFs** | 298,842 | 355,731 | 497,907 | $+19.0\%$ | $+40.0\%$ | $+66.6\%$ | Direct solve |
| **Total Strain Energy ($U$)** | **$15.614\text{ mJ}$** | **$15.713\text{ mJ}$** | **$15.746\text{ mJ}$** | **$+0.64\%$** | **$+0.21\%$** | **$+0.85\%$** | **STABILIZED** ($\le 1\%$) |
| **Apex Disp. ($u_{\text{apex}}$)** | **$37.41\ \mu\text{m}$** | **$37.68\ \mu\text{m}$** | **$37.93\ \mu\text{m}$** | **$+0.72\%$** | **$+0.66\%$** | **$+1.39\%$** | **STABILIZED** ($\le 2\%$) |
| **Max Disp. ($\delta_{\max}$)** | **$59.07\ \mu\text{m}$** | **$59.12\ \mu\text{m}$** | **$59.75\ \mu\text{m}$** | **$+0.08\%$** | **$+1.07\%$** | **$+1.15\%$** | **STABILIZED** ($\le 2\%$) |
| **Dome Apex 95th% Stress** | **$3.399\text{ MPa}$** | **$3.355\text{ MPa}$** | **$3.334\text{ MPa}$** | **$-1.30\%$** | **$-0.63\%$** | **$-1.92\%$** | **STABILIZED** (Shrinking $\Delta$) |
| **Global 95th% Stress** | **$2.493\text{ MPa}$** | **$2.290\text{ MPa}$** | **$2.042\text{ MPa}$** | **$-8.14\%$** | **$-10.84\%$** | **$-18.10\%$** | **DISCRETIZATION-SENSITIVE** |
| **Braincase Roof 95th% Stress** | **$2.823\text{ MPa}$** | **$2.383\text{ MPa}$** | **$2.015\text{ MPa}$** | **$-15.59\%$** | **$-15.46\%$** | **$-28.64\%$** | **DISCRETIZATION-SENSITIVE** |
| **Force Residual ($r_F$)** | **$8.91 \times 10^{-13}$** | **$9.20 \times 10^{-13}$** | **$1.53 \times 10^{-12}$** | Machine prec. | Machine prec. | Machine prec. | **EXACT EQUILIBRIUM** |
| **Moment Residual ($r_M$)**| **$3.13 \times 10^{-12}$** | **$7.87 \times 10^{-13}$** | **$7.23 \times 10^{-13}$** | Machine prec. | Machine prec. | Machine prec. | **EXACT EQUILIBRIUM** |
| **Solver Runtime** | **$72.7\text{ s}$** | **$310.9\text{ s}$** | **$2,055.3\text{ s}$** | $4.28\times$ | $6.61\times$ | $28.28\times$ | Zero swap thrashing |

---

## 9. Known Limitations & Discretization Sensitivities
1. **Stress Field Discretization Sensitivity**:
   - Total compliance ($U$), whole-skull displacement, and dorsal dome stress are stabilized ($<2\%$ net variation).
   - In contrast, global 95th% stress ($-18.1\%$) and endocranial braincase 95th% stress ($-28.6\%$) exhibit non-decaying step differences across the tested mesh range.
   - This reflects ongoing geometric resolution of complex internal cranial cavities and boundary gradients away from the dorsal impact zone.
2. **Stopping Rule**:
   - The 825k-element medium mesh represents the practical upper limit for direct sparse LU solves on 16 GB hardware without out-of-core thrashing.
   - We do not chase a 1.4M $\to$ 3M mesh solve. Instead, the characterized numerical sensitivity ($\approx 28.6\%$ on braincase stress) is formally carried forward as numerical model-form uncertainty into Phase 5.

---

## 10. Scientific Interpretation
- **What is Established**:
  - The deterministic FEM pipeline is numerically verified, stable, and statically balanced.
  - The dome acts as a stiff structural buffer, keeping dome peak stresses remarkably low ($\sim 3.3\text{ MPa}$ under $1.0\text{ kN}$; $\sim 4.5\text{ MPa}$ under biological $1.36\text{ kN}$).
  - Hookean linearity and quadratic energy scaling are exact (`0.000000%` error).
- **What is NOT Established**:
  - We have **not** established asymptotic convergence of localized internal braincase stress.
  - We have **not** established whether the skull remains safe under off-axis oblique impacts or under low-stiffness bone conditions.

---

## 11. Phase Status & Next Decisions
- **Phase 4 Status**: **VERIFIED & FROZEN**.
- **Phase 5 Status**: **PENDING DESIGN**.
- **Next Decision (D007)**: Formal specification of the Phase 5 Uncertainty Quantification & Sensitivity Design of Experiments (DoE) before running any new simulations.

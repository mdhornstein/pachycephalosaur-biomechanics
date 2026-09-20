# Phase 4 Walkthrough: Surface-Derived Finite Element Benchmark (Stegoceras validum, UALVP 2)

This document provides a comprehensive walkthrough of the verified **Phase 4: Surface-Derived Finite Element Benchmark** for *Stegoceras validum* (specimen **UALVP 2**), implementing a fully reproducible, decoupled, numerically validated linear-elastic FEA pipeline.

---

## 🏛️ Taxonomic & Specimen Context
* **Taxonomic Lectotype**: **CMN 515** (Canadian Museum of Nature, Ottawa; isolated frontoparietal dome)
* **Study Specimen**: **UALVP 2** (University of Alberta, Edmonton; articulated referred skull, cited as "UA 2" in Snively & Theodor 2011)
* **Primary Reference**: Snively, E. & Theodor, J. M. (2011) *PLoS ONE* 6(6): e21412. [PMC3125168](https://pmc.ncbi.nlm.nih.gov/articles/PMC3125168/)
* **Primary Scan Mesh**: MorphoSource Media `000018284` (segmented skull surface STL from high-resolution micro-CT)

---

## 📦 Pipeline Deliverables & Technical Architecture

### 1. Canonical Master Surface ($G_0$) & Zero Decimation
- **Immutable Canonical Surface**: [`data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl)
- **Canonical Array SHA-256**: `5adcf53696268578f083ea29f7f4665c0faf1b41e6362ac858c8a5a7a50d62e2`
- **Zero Decimation Across Production Tiers**: Every production mesh tier is generated directly from the identical canonical surface without quadric simplification (`decimate_reduction = 0.0`), preventing artificial boundary sliver creation.
- **Topological Integrity**: 100% 2-manifold watertight solid with positive enclosed volume ($+646,423.1\text{ mm}^3$) conserving specimen volume within $0.024\%$.

### 2. Multi-Tier Production Mesh Hierarchy
Generated via TetGen holding quality constraints strictly invariant ($q = 1.5, \theta_{\min} = 10.0^\circ$) and systematically varying only maximum allowable element volume:
1. **Tier 1 (Coarse, $h_1$)**: `-pq1.5/10` (natural Delaunay volume base) $\to$ 99,614 nodes, 422,573 tets, 298,842 DOFs.
2. **Tier 2 (Med-Coarse, $h_2$)**: `-pq1.5/10a5.0` ($a_{\max} = 5.0\text{ mm}^3$) $\to$ 118,577 nodes, 540,310 tets, 355,731 DOFs.
3. **Tier 3 (Medium, $h_3$)**: `-pq1.5/10a2.0` ($a_{\max} = 2.0\text{ mm}^3$) $\to$ 165,969 nodes, 825,277 tets, 497,907 DOFs (Primary Benchmark).
4. **Tier 4 (Fine Baseline, $h_4$)**: `-pq1.5/10a1.0` ($a_{\max} = 1.0\text{ mm}^3$) $\to$ 261,858 nodes, 1,389,116 tets (computational upper boundary, exceeds 16 GB direct solver memory).
- **Element Quality**: **0 inverted elements** ($V_e > 0$ for all elements across all tiers). Median aspect ratios refine smoothly from $1.44 \to 1.34 \to 1.26$.

### 3. Anatomical Coordinates & Verified Load Formulation
- **Coordinate Alignment**: Midsagittal symmetry plane at $X \approx 103.6\text{ mm}$ (span $[38.0, 169.1]$ mm); anteroposterior snout-to-occiput span $Y \in [4.3, 204.8]\text{ mm}$; dorsoventral palate-to-apex span $Z \in [0.4, 128.1]\text{ mm}$.
- **Physiological Boundary Conditions**: Occipital condyle constrained in 3 translational DOFs ($u_x = u_y = u_z = 0$); nuchal shelf constrained in 2 translational DOFs ($u_y = u_z = 0$).
- **Dual-Graph Geodesic Wavefront Load Patch**:
  - Seed facet identified at dorsal apex along midsagittal plane ($X \approx 103.6\text{ mm}, Y \in [80, 150]\text{ mm}$).
  - Dijkstra wavefront search over the face-adjacency dual graph using facet centroid distances.
  - Strict topological single-component connectivity (0 fragmentation).
  - Strict dorsal summit floor: 100% of loaded nodes have $Z \ge 80.0\text{ mm}$ (**0% ventral cranium penetration**).
  - Target area: $3000.0\text{ mm}^2$; Achieved area: $3000.6\text{ mm}^2$ ($+0.02\%$).

### 4. Decoupled Simulation & Visualization Architecture
- **Hard Invariant**: [`src/stegoceras_biomechanics/fea/plot_results.py`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/plot_results.py) never calls `solve_linear_elasticity()` and never generates meshes. It strictly loads saved `.npz` and `.json` artifacts from disk (<10 seconds, <250 MB RAM).
- **Standalone Simulation Driver**: [`src/stegoceras_biomechanics/fea/solve_production.py`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/solve_production.py) solves one tier at a time in an isolated process, writing immutable numerical artifacts directly to `simulations/phase4/solution_{tier}.npz` and `results/phase4/metrics_{tier}.json` before terminating to return 100% of RAM to the operating system.

---

## 📊 Discretization Progression & Sensitivity Analysis ($1.0\text{ kN}$ Broad Load)

All three production tiers were solved independently with the reference direct sparse solver:

| Observable ($Q$) | Coarse ($h_1$, 423k) | Med-Coarse ($h_2$, 540k) | Medium ($h_3$, 825k) | Step $\Delta_{h_1 \to h_2}$ | Step $\Delta_{h_2 \to h_3}$ | Total Net $\Delta_{h_1 \to h_3}$ | Status |
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
| **Solver Runtime** | **$72.7\text{ s}$** | **$310.9\text{ s}$** | **$2,055.3\text{ s}$ (34 min)**| $4.28\times$ | $6.61\times$ | $28.28\times$ | Clean isolated process |

---

## 🔬 Scientific Interpretation & Findings

1. **Global Compliance & Dorsal Impact Zone**:
   - Total strain energy ($U$) exhibits classic monotonic convergence from below ($15.614 \to 15.713 \to 15.746\text{ mJ}$), with the step delta dropping from $+0.64\%$ to $+0.21\%$.
   - Apex displacement and cranial maximum displacement are tightly bounded ($<1.4\%$ net variation).
   - Frontoparietal dome apex 95th percentile stress converges smoothly with shrinking step differences ($-1.30\% \to -0.63\%$), stabilizing at $3.33\text{ MPa}$.
2. **Internal Cranial Stress Gradients (Braincase Roof & Global)**:
   - In contrast to the dome, internal cranial stresses remain sensitive to mesh resolution across this range.
   - Braincase roof 95th percentile stress decreases systematically ($2.823 \to 2.383 \to 2.015\text{ MPa}$, $-28.64\%$ net shift) with step differences that do not shrink ($-15.59\%$ and $-15.46\%$).
   - This reflects ongoing resolution of intricate internal bony geometries and stress gradients away from the broad dorsal contact zone.

---

## 🎯 Phase 4 Gate Status: Baseline Verified & Frozen for Phase 5 UQ Transition

> **Deterministic FEM baseline verified; displacement/energy and dorsal dome stress stabilized; localized internal stress remains discretization-sensitive and is carried forward into Phase 5 UQ as characterized numerical model-form uncertainty.**

Rather than asserting premature global stress convergence or attempting intractable multi-million-element direct solves on laptop hardware:
- **Phase 4 is verified and frozen**: Static equilibrium is exact, the load formulation is geometrically verified, and same-geometry discretization sensitivity is rigorously quantified.
- **Phase 5 UQ Transition**: The observed numerical discretization sensitivities ($\approx 1.9\%$ dome stress, $\approx 18.1\%$ global stress, $\approx 28.6\%$ braincase stress) are carried forward into the global sensitivity analysis to formally assess whether biological uncertainties (e.g. dome thickness, keratin elasticity, bone modulus) dominate over or interact with residual numerical discretization effects.

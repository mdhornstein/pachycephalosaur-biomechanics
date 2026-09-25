# Current Scientific & Computational State

**Document Status**: Canonical Living State Document  
**Last Updated**: 2026-09-24  
**Phase Transition Baselines**: `15a342f` (Phase 4 Freeze & FE Baseline) & `2662be0` (Literature Basis v1 Freeze)  
**Authoritative Bridge**: [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](LITERATURE_TO_MODEL_DECISIONS.md) (Model Decision Basis v1; Decisions D007, D008, D009)  
**Current Git State**: Dynamic — interrogate directly via `git rev-parse HEAD`  
**Current Phase**: Phase 4, Literature Basis v1, Model Decision Basis v1, Phase 5 Gate A & Gate B **FROZEN**; Phase 5 Gate C (Image Semantics & Attenuation Characterization) **ACTIVE NEXT GATE**

---

## 1. Scientific Objective
This investigation quantifies cranial stress distribution, compliance, and strain energy absorption in the pachycephalosaur *Stegoceras validum* under dome impact loading using 3D finite element analysis (FEA).

The immediate computational question is:
> **Does introducing evidence-based internal material architecture (Model B) materially alter cranial compliance, strain energy distribution, and stress transmission/redistribution to the endocranial braincase relative to our frozen homogeneous baseline (Model A)?**

### Epistemic Invariants & Scope Boundaries (Model Decision Basis v1)
1. **Conditional Mechanical Evaluation**: Finite element results quantify comparative structural response under explicitly modeled geometric, material, and kinematic scenarios. Mechanical competence under modeled conditions does not by itself establish the occurrence of fighting behavior or the evolutionary function of the dome (Decisions D10, D15).
2. **Zero Biological Ground-Truth Validation**: In vivo bone strain and impact force measurements are physically impossible for extinct non-avian dinosaurs. Solver verification, numerical equilibrium, and benchmark reproduction must never be conflated with specimen-specific biological validation (Decision D14).
3. **Strict Separation of Uncertainty Scales**: Output-specific numerical discretization discrepancies ($\Delta_{\text{num}}$) arising from finite-element mesh resolution are rigorously separated from parametric sensitivity envelopes and discrete model-form scenario branches (Decisions D07, D12, D14, D009).

---

## 2. Current Computational Model (Model A)
The project currently executes **Model A**:
- **Representation**: Surface-derived continuum model on the canonical boundary surface ($G_0$).
- **Material Assumption**: Homogeneous isotropic compact bone ($E = 17.0\text{ GPa}, \nu = 0.30$). Per Decision D06, Model A serves strictly as a geometric and numerical baseline control to isolate geometric effects before introducing internal material zonation. It is not an assertion of biological bone homogeneity in the living animal.

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
- **Equilibrium Verification**: Reaction forces and moments are computed via direct sparse matrix-vector multiplication $\mathbf{R} = \mathbf{K}\mathbf{u} - \mathbf{F}_{\text{ext}}$ across all restrained DOFs. Normalized residuals $\le 1.53 \times 10^{-12}$ (machine precision).

---

## 5. Loading Formulation
- **Algorithm**: Surface dual-graph Dijkstra wavefront algorithm starting from dorsal apex seed facet.
  - Edge cost: Euclidean distance between centroids of adjacent surface triangles.
  - Elevation restriction: All candidate facets restricted to $Z \ge 60.0\text{ mm}$ and $Y \ge 70.0\text{ mm}$.
  - Node assertion: Hard invariant that 100% of loaded nodes satisfy $Z \ge 80.0\text{ mm}$.
  - Connectivity assertion: Selected facets form exactly one connected topological component on the dorsal surface.
  - Ventral penetration: `0.00%` (verified eliminated).
- **Patch Properties**:
  - Target Area: $3,000.0\text{ mm}^2$ (literature broad contact scenario).
  - Selected Area: $3,000.02\text{ mm}^2$ ($+0.0007\%$ error).
  - Selected Faces: 1,406 triangles (808 loaded nodes on canonical surface).
  - Centroid: $[X=108.40, Y=104.33, Z=101.97]\text{ mm}$.
- **Load Vector**:
  - Total Compressive Force: $F_z = -1,000.0\text{ N}$ distributed uniformly by tributary nodal area.
  - Resultant Load: $[F_x = 0, F_y = 0, F_z = -1000.0\text{ N}]$.

---

## 6. Material Properties
- **Young's Modulus ($E$)**: $17.0\text{ GPa}$ ($17,000.0\text{ MPa}$). Chosen project control parameter (Rayfield 2007, Snively & Theodor 2011; Decision D06).
- **Poisson's Ratio ($\nu$)**: $0.30$. Standard isotropic bone control value.
- **Epistemic Status (Decisions D07, D09, D16)**:
  - Vertebrate skeletal tissue spans broad plausible property ranges (compact bone $E \in [10, 25]\text{ GPa}$, cancellous bone $E \in [0.5, 5.0]\text{ GPa}$). These intervals define candidate sensitivity envelopes, not established probability distributions for fossil UALVP 2.
  - In linear homogeneous models, scalar modulus variations scale analytically ($u \propto 1/E, \sigma \propto E^0, U \propto 1/E$) and do not require repeated finite element solves (Decision D09).
  - Modulus sensitivity will be evaluated as candidate stiffness-contrast ratios ($E_{\text{cortex}}/E_{\text{core}}$) in Model B rather than premature probabilistic Monte Carlo sampling.

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

## 9. Characterized Discretization Sensitivity & Mesh Disciplines
1. **Output-Specific Discrepancy ($\Delta_{\text{num}}$)**:
   - Total compliance ($U$), whole-skull displacement, and dorsal dome stress are stabilized across the refinement tiers ($<2\%$ net variation).
   - In contrast, internal stress fields exhibit non-decaying mesh-tier differences: global 95th% stress shifted $-18.10\%$ and endocranial braincase 95th% stress shifted $-28.64\%$ ($2.823 \to 2.383 \to 2.015\text{ MPa}$).
   - This reflects ongoing discrete geometric resolution of complex non-convex internal cavities away from the dorsal load zone.
   - **Epistemic Classification (Decisions D12, D009)**: This is reported deterministically as an output-specific numerical discretization discrepancy ($\Delta_{\text{num}} = -28.64\%$). Per Decision D009, it must **never** be treated as a biological uncertainty distribution or a symmetric error bound ($\pm 28.6\%$).
2. **Stopping Rule & Model A/B Mesh Invariant**:
   - The 825k-element medium mesh ($h_3$) represents the practical computational limit for direct sparse LU solves on 16 GB workstation hardware without out-of-core memory thrashing.
   - Rather than pursuing intractable multi-million element solves, Phase 5 enforces the **Mesh Invariant Principle** (Decisions D03, D15): Model A and Model B will use the identical canonical geometry, identical $h_3$ volume mesh (generated from frozen canonical boundary surface $G_0$), loads, and boundary conditions via elementwise material assignment. Holding the discretization fixed prevents differences in mesh resolution from being a changing factor in the A/B comparison; it controls mesh resolution as an experimental variable without implying zero discretization error or identical numerical error across differing constitutive fields.

---

## 10. Scientific Interpretation
- **What is Established**:
  - The deterministic FEM pipeline is numerically verified, statically balanced, and executes closed-form analytical scaling.
  - Under baseline normal loading on the dorsal apex, peak von Mises stress in the compact dome remains low ($\sim 3.3\text{ MPa}$ under $1.0\text{ kN}$ compressive force; scaling to $\sim 4.5\text{ MPa}$ under the $1.36\text{ kN}$ literature benchmark).
- **What is NOT Established**:
  - Asymptotic convergence of localized internal braincase stress is not demonstrated.
  - Structural performance under internal material zonation, oblique loading, or compliant cervical restraints remains to be quantified.
  - No specimen-specific biological validation exists for UALVP 2 (Decision D14).
  - Finite element outputs under modeled load cases do not determine the living behavior or evolutionary function of the pachycephalosaur dome (Decisions D10, D15).

---

## 11. Phase Status & Next Scientific Actions
- **Phase 4 Status**: **VERIFIED & FROZEN** (commit `15a342f`).
- **Literature Basis v1**: **FROZEN** (commit `2662be0`).
- **Model Decision Basis v1**: **FROZEN** ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](LITERATURE_TO_MODEL_DECISIONS.md); Decisions D007, D008, D009).
- **Phase 5 Status**: **ACTIVE** — UALVP 2 CT Characterization & Material A/B Experiment.
- **Phase 5 Gate A (DICOM Ingestion & Header Audit)**: **VERIFIED & FROZEN** ([`reports/phase5_gate_a_dicom_report.md`](../reports/phase5_gate_a_dicom_report.md); 514 slices verified, true voxel spacing $0.207572 \times 0.207572 \times 0.250000\text{ mm}$, unsigned 16-bit intensity $[0, 65535]$, manifest in [`data/metadata/dicom_slice_manifest.json`](../data/metadata/dicom_slice_manifest.json)).
- **Phase 5 Gate B (CT-to-Surface Registration & Empirical Scale Verification)**: **VERIFIED & FROZEN** ([`reports/phase5_gate_b_registration_report.md`](../reports/phase5_gate_b_registration_report.md); rigid registration at unit scale $s = 1.000000$ supported by free-scale diagnostic $\hat{s} = 1.00494$, forward median surface residual $0.1633\text{ mm}$, reverse median $1.0928\text{ mm}$, sub-voxel translation norm $0.2472\text{ mm}$, zero-based DICOM voxel-center convention directly from `ImagePositionPatient`, objective Otsu threshold $T = 20,864$, metrics in [`results/phase5/gate_b_registration_metrics.json`](../results/phase5/gate_b_registration_metrics.json)).
- **Immediate Next Action (Gate C)**: Characterize image data semantics, audit attenuation histogram across cranial tissues (air, matrix, compact dome bone, cancellous bone), and evaluate radial/depth attenuation gradients in the dome to inform Model B zonation boundaries.

# Phase 4 Walkthrough: Surface-Derived Finite Element Benchmark (Stegoceras validum, UALVP 2)

We have completed the numerical verification and discretization sensitivity study for **Phase 4: Surface-Derived Finite Element Benchmark** (*Stegoceras validum*, specimen **UALVP 2**), implementing a fully reproducible, numerically validated, linear-elastic finite element analysis workflow.

---

## 🏛️ Taxonomic & Specimen Context
* **Taxonomic Lectotype**: **CMN 515** (Canadian Museum of Nature, Ottawa; isolated frontoparietal dome)
* **Study Specimen**: **UALVP 2** (University of Alberta, Edmonton; articulated referred specimen, cited as "UA 2" in Snively & Theodor 2011)
* **Primary Reference**: Snively, E. & Theodor, J. M. (2011) *PLoS ONE* 6(6): e21412. [PMC3125168](https://pmc.ncbi.nlm.nih.gov/articles/PMC3125168/)
* **Primary Mesh**: MorphoSource Media `000018284` (segmented surface STL from micro-CT)

---

## 📦 Summary of Completed Phase 4 Deliverables

### 1. Non-Invasive Preprocessing & Single Immutable Surface Provenance
- [**`src/stegoceras_biomechanics/fea/geometry.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/geometry.py): Automated repair of raw STL non-manifold edges to generate a 100% watertight, 2-manifold surface.
- **Source Surface SHA-256**: `46b11f7e8afbae667ab5ce235714ea790e4d91f0e80eb01263228d41a2ddafd3`
- **Fidelity Verified**:
  - Enclosed Volume: $646,576.2\text{ mm}^3 \rightarrow 646,628.3\text{ mm}^3$ (**$+0.0081\%$ change**, well within $\pm 0.05\%$ tolerance).
  - Surface Area: $120,512.2\text{ mm}^2 \rightarrow 120,383.2\text{ mm}^2$ (**$-0.1070\%$ change**, well within $\pm 0.20\%$ tolerance).
  - Mean Surface Shift: **$0.0040\text{ mm}$ ($4.0\ \mu\text{m}$)**.
  - Maximum Surface Deviation: **$4.8531\text{ mm}$** localized to an internal pterygoid/palatal seam, with $>64\text{ mm}$ clearance to the dome load patch and $>69\text{ mm}$ clearance to boundary constraints.
  - Cleaned STL: `data/meshes/cleaned/stegoceras_ualvp2_watertight.stl`.

### 2. Multi-Tier Solid Tetrahedral Mesh Hierarchy & Exact Regeneration Parameters
- [**`src/stegoceras_biomechanics/fea/meshing.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/meshing.py): Solid 3D tetrahedral meshing via TetGen with explicit reproduction parameters:
  - **Tier 1 Coarse** (`models/phase4/mesh_coarse.yaml`): `reduction=0.97`, `mindihedral=10.0`, `minratio=1.5` $\to$ 55,728 nodes, 229,427 tets, median $AR = 1.46$, max $AR = 4,277.21$, mean $AR = 2.16$, **0 inverted elements**.
  - **Tier 2 Med-Coarse** (`models/phase4/mesh_medium_coarse.yaml`): `reduction=0.95`, `mindihedral=10.0`, `minratio=1.5` $\to$ 99,542 nodes, 421,856 tets, median $AR = 1.44$, max $AR = 21,259.23$, mean $AR = 2.06$, **0 inverted elements**.
  - **Tier 3 Medium** (`models/phase4/mesh_medium.yaml`): `reduction=0.92`, `mindihedral=10.0`, `minratio=1.5` $\to$ 147,735 nodes, 606,363 tets, median $AR = 1.50$, max $AR = 674.56$, mean $AR = 2.01$, **0 inverted elements**.
  - **Tier 4 Fine Direct Baseline** (`models/phase4/mesh_fine.yaml`): `reduction=0.00` $\to$ 698,960 nodes, 2,267,738 tets, median $AR = 1.86$, max $AR = 5,477.85$, mean $AR = 2.25$, **0 inverted elements** (16 GB memory limit).
  - **Decimated Diagnostic Mesh**: `reduction=0.85` (standard quadric) $\to$ 189,696 nodes, 601,025 tets, median $AR = 5.53$, max $AR = 25,327.12$, mean $AR = 10.88$, $26.50\%$ elements with $AR > 10$.
  - **A/B Diagnostic Finding**: Proved surface decimation creates needle-thin boundary triangles that force TetGen to create boundary slivers. Excluded from production convergence models.

### 3. Epistemic YAML Model Configurations
- [`models/phase4/baseline.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/baseline.yaml)
- [`models/phase4/mesh_coarse.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/mesh_coarse.yaml)
- [`models/phase4/mesh_medium_coarse.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/mesh_medium_coarse.yaml)
- [`models/phase4/mesh_medium.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/mesh_medium.yaml)
- [`models/phase4/mesh_fine.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/mesh_fine.yaml)

### 4. Algorithmic Loading & Physiological Boundary Constraints
- [**`src/stegoceras_biomechanics/fea/loads.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/loads.py): Algorithmic bisection patch search on the frontoparietal dome ($3000.0\text{ mm}^2$ target, $3014.2\text{ mm}^2$ actual, dorsal normal filter $n_z \ge 0.30$, tributary force distribution of $1.0\text{ kN}$ in $-Z$).
- [**`src/stegoceras_biomechanics/fea/boundary_conditions.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/boundary_conditions.py): Occipital condyle ($u_x = u_y = u_z = 0$, 740 nodes) and Nuchal shelf ($u_y = u_z = 0$, 4,185 nodes).

### 5. Python FEA Engine & Detailed Telemetry
- [**`src/stegoceras_biomechanics/fea/solver.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/solver.py): 3D linear isotropic elasticity assembly via `skfem` with SciPy direct (`spsolve`) and iterative (`cg`) solvers, with explicit telemetry fields (`requested_solver`, `actual_solver`, `cg_iterations`, `cg_converged`, `cg_final_residual`, `fallback_attempted`, `fallback_status`).
- [**`src/stegoceras_biomechanics/fea/results.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/results.py): Partitioning and stress/strain extraction across 6 anatomical subregions.
- [**`src/stegoceras_biomechanics/fea/validation.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/validation.py): Analytical Hookean tension bar verification ($<0.2\%$ error), static force/moment equilibrium, and load linearity.

### 6. Automated Unit Test Suite
- [`tests/test_phase4_fea.py`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/tests/test_phase4_fea.py): **10/10 passing tests** covering analytical verification, surface repair fidelity, tetrahedral Jacobians, boundary extraction, load patch, equilibrium, linearity, subregion extraction, SHA-256 surface provenance, and 100% artifact consistency.

---

## 📊 3-Tier Discretization Sensitivity Progression (UALVP 2, 1.0 kN Broad Load)

| Metric | Tier 1 (Coarse, 229k) | Tier 2 (Med-Coarse, 422k) | Tier 3 (Medium, 606k) | Step $\Delta_{h_1 \to h_2}$ | Step $\Delta_{h_2 \to h_3}$ | Convergence Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Strain Energy ($U$)** | **$8.0075\text{ mJ}$** | **$8.1841\text{ mJ}$** | **$7.7902\text{ mJ}$** | $+2.21\%$ | $-4.81\%$ | **STABILIZED** ($\le 5\%$) |
| **Apex Displacement ($u_{\text{apex}}$)** | **$27.66\ \mu\text{m}$** | **$30.13\ \mu\text{m}$** | **$29.10\ \mu\text{m}$** | $+8.93\%$ | $-3.42\%$ | **STABILIZED** ($\le 5\%$) |
| **Max Displacement ($\delta_{\max}$)**| **$35.46\ \mu\text{m}$** | **$38.40\ \mu\text{m}$** | **$39.62\ \mu\text{m}$** | $+8.29\%$ | $+3.18\%$ | **STABILIZED** ($\le 5\%$) |
| **Global 95th% von Mises Stress** | **$1.6688\text{ MPa}$** | **$1.7200\text{ MPa}$** | **$1.7575\text{ MPa}$** | $+3.07\%$ | $+2.18\%$ | **MONOTONIC CONVERGENCE** ($\Delta_2 < \Delta_1$) |
| **Dome Apex 95th% Stress** | **$2.2932\text{ MPa}$** | **$2.3436\text{ MPa}$** | **$2.4962\text{ MPa}$** | $+2.20\%$ | $+6.51\%$ | **UNCONVERGED / SENSITIVE** ($\Delta_2 > \Delta_1$) |
| **Braincase Roof 95th% Stress**| **$1.9703\text{ MPa}$** | **$2.1036\text{ MPa}$** | **$2.3258\text{ MPa}$** | $+6.77\%$ | $+10.56\%$ | **UNCONVERGED / SENSITIVE** ($\Delta_2 > \Delta_1$) |
| **Normalized Force Residual ($r_F$)** | **`7.03e-13`** | **`3.85e-13`** | **`1.52e-12`** | Exact | Exact | Machine precision |
| **Normalized Moment Residual ($r_M$)**| **`2.38e-12`** | **`1.38e-12`** | **`5.70e-12`** | Exact | Exact | Machine precision |

---

## 🛑 Phase 4 Gate Status: OPEN (Carried Forward to Phase 5 UQ)
- **Gate Finding**: Phase 4 numerical verification, solver integrity, static equilibrium, and discretization sensitivity characterization are fully completed and verified.
- **Convergence Decision**: In strict accordance with scientific standards, **the Phase 4 convergence gate is held OPEN** because asymptotic convergence is not yet established for localized cranial stresses (dome $+8.85\%$, braincase $+18.04\%$).
- **Transition Protocol**: Rather than chasing unresolvable multi-million-element meshes on available hardware, this localized discretization sensitivity is formally designated as an **active numerical uncertainty component** ($\epsilon_{\text{discretization}}$) to be explicitly propagated into the Phase 5 Uncertainty Quantification framework.

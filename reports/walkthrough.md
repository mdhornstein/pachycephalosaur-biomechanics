# Phase 4 Walkthrough: Surface-Derived Finite Element Benchmark (Stegoceras validum, UALVP 2)

We have completed **Phase 4: Surface-Derived Finite Element Benchmark** for *Stegoceras validum* (specimen **UALVP 2**), implementing a fully reproducible, numerically validated, linear-elastic finite element analysis workflow.

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

### 2. Multi-Tier Solid Tetrahedral Mesh Hierarchy & Quality Audit (100% Reconciled)
- [**`src/stegoceras_biomechanics/fea/meshing.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/meshing.py): Solid 3D tetrahedral meshing via TetGen with strict element quality checks.
- **Mesh Quality & A/B Findings**:
  - **Tier 1 Coarse** (`stegoceras_tetmesh_coarse.npz`): 55,728 nodes, 229,427 tets, median $AR = 1.46$, max $AR = 4,277.21$, mean $AR = 2.16$, **0 inverted elements**.
  - **Tier 2 Med-Coarse** (`stegoceras_tetmesh_medium_coarse.npz`): 99,542 nodes, 421,856 tets, median $AR = 1.44$, max $AR = 21,259.23$, mean $AR = 2.06$, **0 inverted elements**.
  - **Tier 3 Medium** (`stegoceras_tetmesh_medium.npz`): 147,735 nodes, 606,363 tets, median $AR = 1.50$, max $AR = 674.56$, mean $AR = 2.01$, **0 inverted elements**.
  - **Tier 4 Fine Direct Baseline** (`stegoceras_tetmesh_fine.npz`): 698,960 nodes, 2,267,738 tets, median $AR = 1.86$, max $AR = 5,477.85$, mean $AR = 2.25$, **0 inverted elements**.
  - **Decimated Diagnostic Mesh** (`stegoceras_tetmesh_decimated_diagnostic.npz`): 189,696 nodes, 601,025 tets, median $AR = 5.53$, max $AR = 25,327.12$, mean $AR = 10.88$, $26.50\%$ elements with $AR > 10$.
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

| Metric | Tier 1 (Coarse, 229k) | Tier 2 (Med-Coarse, 422k) | Tier 3 (Medium, 606k) | Total Net Progression |
| :--- | :--- | :--- | :--- | :--- |
| **Total Strain Energy ($U$)** | **$8.0075\text{ mJ}$** | **$8.1841\text{ mJ}$** | **$7.7902\text{ mJ}$** | **$-2.71\%$** |
| **Apex Displacement ($u_{\text{apex}}$)** | **$27.66\ \mu\text{m}$** | **$30.13\ \mu\text{m}$** | **$29.10\ \mu\text{m}$** | **$+5.19\%$** |
| **Max Displacement ($\delta_{\max}$)**| **$35.46\ \mu\text{m}$** | **$38.40\ \mu\text{m}$** | **$39.62\ \mu\text{m}$** | **$+11.73\%$** |
| **Global 95th% von Mises Stress** | **$1.6688\text{ MPa}$** | **$1.7200\text{ MPa}$** | **$1.7575\text{ MPa}$** | **$+5.31\%$** |
| **Dome Apex 95th% Stress** | **$2.2932\text{ MPa}$** | **$2.3436\text{ MPa}$** | **$2.4962\text{ MPa}$** | **$+8.85\%$** |
| **Braincase Roof 95th% Stress**| **$1.9703\text{ MPa}$** | **$2.1036\text{ MPa}$** | **$2.3258\text{ MPa}$** | **$+18.04\%$** |
| **Normalized Force Residual ($r_F$)** | **`7.03e-13`** | **`3.85e-13`** | **`1.52e-12`** | Machine precision |
| **Normalized Moment Residual ($r_M$)**| **`2.38e-12`** | **`1.38e-12`** | **`5.70e-12`** | Machine precision |

---

## 🛑 Phase 4 Gate Stop Directive
In accordance with project guidelines:
* No internal CT material heterogeneity has been assigned.
* No dynamic impact or transient dynamic simulation has been performed.
* No Monte Carlo / UQ sampling has been executed.
* All work is strictly confined to Phase 4 deliverables.

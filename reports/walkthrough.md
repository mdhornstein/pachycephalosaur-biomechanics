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

### 2. Multi-Tier Solid Tetrahedral Mesh Hierarchy & Quality Audit
- [**`src/stegoceras_biomechanics/fea/meshing.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/meshing.py): Solid 3D tetrahedral meshing via TetGen with strict element quality checks.
- **Mesh Quality & A/B Findings**:
  - **Coarse Verification Tier** (`stegoceras_tetmesh_coarse.npz`): 76,152 nodes, 318,339 tets, median $AR = 1.45$, mean $AR = 1.92$, **0 inverted elements** ($V_e > 0$).
  - **Direct Baseline Mesh** (`stegoceras_tetmesh_fine.npz`): 698,960 nodes, 2,267,738 tets, median $AR = 1.86$, mean $AR = 2.25$, $99.32\%$ elements with $AR \le 10$, **0 inverted elements** ($V_e > 0$).
  - **Decimated Diagnostic Mesh** (`stegoceras_tetmesh_decimated_diagnostic.npz`): 189,696 nodes, 601,025 tets, median $AR = 5.53$, mean $AR = 10.88$, $26.50\%$ elements with $AR > 10$.
  - **A/B Diagnostic Finding**: Proved surface decimation creates needle-thin boundary triangles that force TetGen to create boundary slivers. The direct un-decimated surface provides vastly superior shape quality ($99.32\% \le 10$) and is the single source for production models.

### 3. Epistemic YAML Model Configurations
- [`models/phase4/baseline.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/baseline.yaml)
- [`models/phase4/mesh_coarse.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/mesh_coarse.yaml)
- [`models/phase4/mesh_fine.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/mesh_fine.yaml)

### 4. Algorithmic Loading & Physiological Boundary Constraints
- [**`src/stegoceras_biomechanics/fea/loads.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/loads.py): Algorithmic bisection patch search on the frontoparietal dome ($3000.0\text{ mm}^2$ target, $3014.2\text{ mm}^2$ actual, dorsal normal filter $n_z \ge 0.30$, tributary force distribution of $1.0\text{ kN}$ in $-Z$).
- [**`src/stegoceras_biomechanics/fea/boundary_conditions.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/boundary_conditions.py): Occipital condyle ($u_x = u_y = u_z = 0$, 740 nodes) and Nuchal shelf ($u_y = u_z = 0$, 4,185 nodes).

### 5. Python FEA Engine & Verification
- [**`src/stegoceras_biomechanics/fea/solver.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/solver.py): 3D linear isotropic elasticity assembly via `skfem` with SciPy direct (`spsolve`) and iterative (`cg`) solvers.
- [**`src/stegoceras_biomechanics/fea/results.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/results.py): Partitioning and stress/strain extraction across 6 anatomical subregions.
- [**`src/stegoceras_biomechanics/fea/validation.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/validation.py): Analytical Hookean tension bar verification ($<0.2\%$ error), static force/moment equilibrium, and load linearity.

### 6. Automated Unit Test Suite
- [`tests/test_phase4_fea.py`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/tests/test_phase4_fea.py): **9/9 passing tests** covering analytical verification, surface repair fidelity, tetrahedral Jacobians, boundary extraction, load patch, equilibrium, linearity, subregion extraction, and immutable SHA-256 surface provenance.

### 7. Comprehensive Synthesis Report
- [**`reports/phase4_fea_benchmark_report.md`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/phase4_fea_benchmark_report.md): Authoritative scientific synthesis report with full tabular metrics, biomechanical interpretation, and Phase 4 gate assessment.

---

## 📊 Summary of Primary Benchmark Metrics (UALVP 2, 1.0 kN Broad Load)

| Parameter | Primary Benchmark ($1.0\text{ kN}$) | Derived Biological ($1360\text{ N}$) | Notes / Classification |
| :--- | :--- | :--- | :--- |
| **Max Displacement** | **$36.28\ \mu\text{m}$** ($0.0363\text{ mm}$) | **$49.34\ \mu\text{m}$** | Linear scaling ($1.36 \times$) |
| **Apex Displacement ($u_{\text{apex}}$)** | **$28.65\ \mu\text{m}$** | **$38.96\ \mu\text{m}$** | Dorsal apex landmark |
| **Global 95th% von Mises Stress** | **$1.672\text{ MPa}$** | **$2.274\text{ MPa}$** | Global cranial vault |
| **Global 99th% von Mises Stress** | **$2.791\text{ MPa}$** | **$3.796\text{ MPa}$** | Upper tail |
| **Dome Apex 95th% Stress** | **$2.246\text{ MPa}$** | **$3.055\text{ MPa}$** | Frontoparietal apex zone |
| **Sub-Dome Vault Core 95th% Stress** | **$1.920\text{ MPa}$** | **$2.611\text{ MPa}$** | Sub-dome core zone |
| **Endocranial Braincase 95th% Stress**| **$2.037\text{ MPa}$** (Mean $0.85\text{ MPa}$) | **$2.770\text{ MPa}$** | Endocranial ceiling (shielded) |
| **Total Strain Energy** | **$7.7957\text{ mJ}$** | **$14.419\text{ mJ}$** | Quadratic scaling ($1.36^2 \times$) |
| **Normalized Force Residual ($r_F$)** | **`1.59e-13`** | **`1.59e-13`** | Static equilibrium verified |
| **Normalized Moment Residual ($r_M$)**| **`6.59e-13`** | **`6.59e-13`** | Static equilibrium verified |
| **Absolute Moment Residual** | **`5.00e-09 N·mm`** | **`6.80e-09 N·mm`** | Guarded denominator |

---

## 🛑 Phase 4 Gate Stop Directive
In accordance with project guidelines:
* No internal CT material heterogeneity has been assigned.
* No dynamic impact or transient dynamic simulation has been performed.
* No Monte Carlo / UQ sampling has been executed.
* All work is strictly confined to Phase 4 deliverables.

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

### 1. Non-Invasive Preprocessing & Topological Repair
- [**`src/stegoceras_biomechanics/fea/geometry.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/geometry.py): Automated repair of raw STL non-manifold edges to generate a 100% watertight, 2-manifold surface.
- **Fidelity Verified**:
  - Enclosed Volume: $646,575.6\text{ mm}^3 \rightarrow 646,628.3\text{ mm}^3$ (**$+0.0081\%$ change**, well within $\pm 0.05\%$ tolerance).
  - Surface Area: $189,458.2\text{ mm}^2 \rightarrow 189,255.4\text{ mm}^2$ (**$-0.1070\%$ change**, well within $\pm 0.20\%$ tolerance).
  - Cleaned STL: `data/meshes/cleaned/stegoceras_ualvp2_watertight.stl`.

### 2. Multi-Tier Solid Tetrahedral Mesh Hierarchy
- [**`src/stegoceras_biomechanics/fea/meshing.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/meshing.py): Solid 3D tetrahedral meshing via TetGen with strict element quality checks.
- **Mesh Quality**:
  - **Coarse Tier** (`stegoceras_tetmesh_coarse.npz`): 76,152 nodes, 318,339 tets, **0 inverted elements** ($V_e > 0$).
  - **Medium Tier** (`stegoceras_tetmesh_medium.npz`): 189,696 nodes, 601,025 tets, **0 inverted elements** ($V_e > 0$).
  - **Fine Tier** (`stegoceras_tetmesh_fine.npz`): 698,960 nodes, 2,267,738 tets, **0 inverted elements** ($V_e > 0$).

### 3. Epistemic YAML Model Configurations
- [`models/phase4/baseline.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/baseline.yaml)
- [`models/phase4/mesh_coarse.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/mesh_coarse.yaml)
- [`models/phase4/mesh_medium.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/mesh_medium.yaml)
- [`models/phase4/mesh_fine.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/models/phase4/mesh_fine.yaml)

### 4. Algorithmic Loading & Physiological Boundary Constraints
- [**`src/stegoceras_biomechanics/fea/loads.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/loads.py): Algorithmic bisection patch search on the frontoparietal dome ($3000.0\text{ mm}^2$ target, $3014.2\text{ mm}^2$ actual, dorsal normal filter $n_z \ge 0.30$, tributary force distribution of $1.0\text{ kN}$ in $-Z$).
- [**`src/stegoceras_biomechanics/fea/boundary_conditions.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/boundary_conditions.py): Occipital condyle ($u_x = u_y = u_z = 0$, 740 nodes) and Nuchal shelf ($u_y = u_z = 0$, 4,185 nodes).

### 5. Python FEA Engine & CLI
- [**`src/stegoceras_biomechanics/fea/solver.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/solver.py): 3D linear isotropic elasticity assembly via `skfem` with SciPy direct (`spsolve`) and iterative (`cg`) solvers.
- [**`src/stegoceras_biomechanics/fea/results.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/results.py): Partitioning and stress/strain extraction across 6 anatomical subregions.
- [**`src/stegoceras_biomechanics/fea/validation.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/validation.py): Analytical Hookean tension bar verification, static force/moment equilibrium, and load linearity.
- [**`src/stegoceras_biomechanics/fea/cli.py`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/src/stegoceras_biomechanics/fea/cli.py): CLI interface (`prepare`, `mesh`, `solve`, `analyze`).

### 6. Diagnostic & Result Visualizations
- [`reports/figures/05_anatomical_coordinate_axes.png`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/figures/05_anatomical_coordinate_axes.png): Anatomical axes, symmetry midline ($X=103.6\text{ mm}$), and load vector orientation.
- [`reports/figures/06_load_patch_diagnostic.png`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/figures/06_load_patch_diagnostic.png): Algorithmic $3000\text{ mm}^2$ patch centered on the frontoparietal dome apex.
- [`reports/figures/07_boundary_conditions_diagnostic.png`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/figures/07_boundary_conditions_diagnostic.png): Condyle and nuchal shelf constraint landmarks.
- [`reports/figures/08_mesh_resolutions_comparison.png`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/figures/08_mesh_resolutions_comparison.png): Element volume and aspect ratio histograms across tiers.
- [`reports/figures/09_fe_von_mises_stress_1kn.png`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/figures/09_fe_von_mises_stress_1kn.png): Sagittal stress field and subregion stress bar chart.
- [`reports/figures/10_fe_displacement_and_strain.png`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/figures/10_fe_displacement_and_strain.png): Cranial displacement field (max $25.5\ \mu\text{m}$) and principal tensile strain field ($\epsilon_1$).
- [`reports/figures/11_mesh_convergence_curves.png`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/figures/11_mesh_convergence_curves.png): Convergence trends between Coarse and Medium meshes ($\Delta \sigma_{p95} = 5.1\%$).
- [`reports/figures/12_linearity_scaling_validation.png`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/figures/12_linearity_scaling_validation.png): Proof of linear displacement scaling and quadratic strain energy scaling ($U \propto F^2$).

### 7. Executed Jupyter Notebooks
- [`notebooks/06_fe_geometry_preparation.ipynb`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/notebooks/06_fe_geometry_preparation.ipynb): Geometry healing & tetrahedralization.
- [`notebooks/07_fe_baseline_analysis.ipynb`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/notebooks/07_fe_baseline_analysis.ipynb): Baseline solve, equilibrium verification, and subregion metrics.
- [`notebooks/08_fe_mesh_convergence.ipynb`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/notebooks/08_fe_mesh_convergence.ipynb): Spatial discretization convergence.
- [`notebooks/09_fe_linearity_validation.ipynb`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/notebooks/09_fe_linearity_validation.ipynb): Linearity validation and analytical biological scaling.

### 8. Automated Unit Test Suite
- [`tests/test_phase4_fea.py`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/tests/test_phase4_fea.py): **8/8 passing tests** covering analytical verification, surface repair fidelity, tetrahedral Jacobians, boundary extraction, load patch, equilibrium, linearity, and subregion extraction.

### 9. Comprehensive Synthesis Report
- [**`reports/phase4_fea_benchmark_report.md`**](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/phase4_fea_benchmark_report.md): Scientific synthesis report with full tabular metrics, biomechanical interpretation, and Phase 4 gate assessment.

---

## 📊 Summary of Primary Benchmark Metrics (UALVP 2, 1.0 kN Broad Load)

| Parameter | Primary Benchmark ($1.0\text{ kN}$) | Derived Biological ($1360\text{ N}$) | Notes / Classification |
| :--- | :--- | :--- | :--- |
| **Max Displacement** | **$25.49\ \mu\text{m}$** ($0.0255\text{ mm}$) | **$34.67\ \mu\text{m}$** | Linear scaling ($1.36 \times$) |
| **95th% von Mises Stress** | **$1.26\text{ MPa}$** | **$1.72\text{ MPa}$** | Global cranial vault |
| **99th% von Mises Stress** | **$1.96\text{ MPa}$** | **$2.66\text{ MPa}$** | Global cranial vault |
| **Peak Stress (Constraint)**| **$11.01\text{ MPa}$** | **$14.97\text{ MPa}$** | Localized to basicranial boundary |
| **Dome Apex 95th% Stress** | **$1.00\text{ MPa}$** | **$1.36\text{ MPa}$** | Frontoparietal apex zone |
| **Vault Core 95th% Stress** | **$1.58\text{ MPa}$** | **$2.14\text{ MPa}$** | Sub-dome core zone |
| **Braincase 95th% Stress** | **$1.47\text{ MPa}$** (Mean $0.68\text{ MPa}$) | **$2.00\text{ MPa}$** | Endocranial ceiling (shielded) |
| **Total Strain Energy** | **$5.3818\text{ mJ}$** | **$9.9545\text{ mJ}$** | Quadratic scaling ($1.36^2 \times$) |
| **Force Residual Error** | **`0.000000%`** ($0.000000\text{ N}$) | **`0.000000%`** | Static equilibrium verified |
| **Moment Residual Error**| **`0.000000%`** ($0.0000\text{ N}\cdot\text{mm}$) | **`0.000000%`** | Static equilibrium verified |

---

## 🛑 Phase 4 Gate Stop Directive
In accordance with project guidelines:
* No internal CT material heterogeneity has been assigned.
* No dynamic impact or transient dynamic simulation has been performed.
* No Monte Carlo / UQ sampling has been executed.
* All work is strictly confined to Phase 4 deliverables.

# Phase 2 Design (Retrospective Reconstruction): Digital Anatomy Inventory, Topological Validation & Multi-Part Assembly Verification

> [!IMPORTANT]
> **RETROSPECTIVE RECONSTRUCTION — CREATED AFTER EXECUTION**  
> This document reconstructs the methodological intent and execution logic of Phase 2 from the surviving project record (commits `02d2f28`, `76ae2c4`, `83ed5b0`, `d736b61`, and `8e9903d`; [`reports/phase2_digital_anatomy_report.md`](../../reports/phase2_digital_anatomy_report.md); [`data/metadata/geometry_inventory.csv`](../../data/metadata/geometry_inventory.csv); and Decision D02 / D001). It is not a contemporaneous pre-execution design and must not be interpreted as evidence that these criteria were predeclared.

**Document Role**: Retrospectively Reconstructed Phase Design  
**Status**: RETROSPECTIVELY RECONSTRUCTED & FROZEN  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md) §4.4, Decision D02; [`docs/DECISIONS.md`](../DECISIONS.md), Decision D001)  
**Specimen**: *Stegoceras validum* UALVP 2  
**Target Codebase / Pipeline**: `src/stegoceras_biomechanics/geometry/inventory.py`, `src/stegoceras_biomechanics/geometry/assembly.py`, `tests/test_phase2_geometry.py`, `tests/test_geometry.py`  
**Historical Execution Baseline**: Commits `02d2f28` $\to$ `8e9903d` (August 29, 2026)  

---

### Epistemic Status Taxonomy
To maintain strict scientific auditability, every methodological item, requirement, parameter, and criterion in this retrospective document is labeled with one of four explicit epistemic categories:

| Status Tag | Operational Definition |
| :--- | :--- |
| `[DOCUMENTED BEFORE EXECUTION]` | Directly attested in contemporaneous pre-execution commits, initial code comments, or external repository metadata prior to milestone completion. |
| `[INFERRED FROM EXECUTION RECORD]` | Derived deterministically from surviving execution scripts, test assertions, and synthesis reports produced during Phase 2 execution. |
| `[RETROSPECTIVE RECONSTRUCTION]` | Formulated during post-execution documentation synthesis to reconstruct the implicit scientific logic and decision criteria. |
| `[NOT ESTABLISHED]` | Deliberately marked as unmeasured, unverified, or explicitly deferred to downstream phases to prevent retroactive fabrication. |

---

## 1. Scientific Question
*Do the 32 individual segmented cranial bone surface meshes and the composite whole-skull mesh for Stegoceras validum (UALVP 2) share an identical native coordinate frame, can they be assembled into an articulated cranium with zero rigid transformation, what are their topological manifoldness and boundary closure properties, and how quantitatively congruent is the multi-part assembly to the fused whole-skull STL?* `[INFERRED FROM EXECUTION RECORD]`

Specifically:
1. What anatomical elements are represented in the MorphoSource UALVP 2 collection, and are expected bilateral pairs present? `[DOCUMENTED BEFORE EXECUTION]`
2. Are the deposited STL files clean manifold geometries, and which meshes possess open boundary loops vs. non-manifold edges? `[DOCUMENTED BEFORE EXECUTION]`
3. Do component bounding boxes and centroids support a common coordinate origin and unit scale without artificial alignment? `[INFERRED FROM EXECUTION RECORD]`
4. What is the residual spatial distance distribution between the independent component assembly and the outer whole-skull shell? `[INFERRED FROM EXECUTION RECORD]`
5. What baseline degree of bilateral symmetry is exhibited across paired dermatocranial and splanchnocranial bones across a candidate midsagittal plane? `[INFERRED FROM EXECUTION RECORD]`

---

## 2. Motivation / Prior Evidence
- **Acquired Mesh Dataset**: Following Phase 1 ingestion, two archives were downloaded from MorphoSource containing **33 surface STL files**:
  - Media `000018284`: Whole-skull composite mesh (`WitmerLab_Stegoceras_UALVP2-000018284.stl`, $1,200,102$ faces). `[DOCUMENTED BEFORE EXECUTION]`
  - Media `000043121`–`000043162`: 32 individual cranial bone meshes segmented by WitmerLab. `[DOCUMENTED BEFORE EXECUTION]`
- **Provenance Disambiguation**: The downloaded files represent 3D surface meshes segmented from micro-CT; the raw volumetric micro-CT slice stack itself was not publicly deposited on MorphoSource with the STLs (clarified in commit `d736b61`). `[DOCUMENTED BEFORE EXECUTION]`
- **Prerequisite for Biomechanical Meshing**: Before any solid tetrahedral meshing or finite element analysis can proceed, the coordinate alignment, closure, and mutual consistency of these 33 meshes must be mathematically established. `[DOCUMENTED BEFORE EXECUTION]`

---

## 3. Hypotheses & Competing Expectations
- **Hypothesis A (Common Native Coordinate Frame)**: All 32 component bone meshes and the whole skull were exported from a single unified segmentation scene in identical coordinates and unit scale. Consequently, assembling them with zero translation, rotation, or scaling produces a coherent articulated skull whose spatial extents match the whole-skull STL within sub-millimeter tolerances ($\Delta \le 0.05$ coordinate units). `[INFERRED FROM EXECUTION RECORD]`
- **Hypothesis B (Disjoint Local Component Frames)**: The individual component bones were exported in localized bone-centered coordinates or arbitrary display poses, requiring multi-body surface registration (e.g. Iterative Closest Point) to reconstruct the articulated skull. `[RETROSPECTIVE RECONSTRUCTION]`
- **Observable Signature**: Evaluating bounding box extents and centroid containment directly discriminates between Hypothesis A ($\Delta \approx 0$) and Hypothesis B ($\Delta \gg 1.0$). `[INFERRED FROM EXECUTION RECORD]`

---

## 4. Scope
- **In Scope**:
  - Complete geometric and topological characterization of all 33 STL files: vertex counts, face counts, boundary edges, non-manifold edges, watertightness, surface areas, and bounding boxes. `[DOCUMENTED BEFORE EXECUTION]`
  - Auditing repository web metadata against binary file contents to identify discrepancies. `[DOCUMENTED BEFORE EXECUTION]`
  - Evaluation of coordinate frame sharing via bounding box alignment and centroid containment. `[INFERRED FROM EXECUTION RECORD]`
  - Multi-part zero-transformation assembly and point-cloud distance comparison against the whole-skull STL ($N = 50,000$ points). `[INFERRED FROM EXECUTION RECORD]`
  - Bilateral symmetry diagnostic measuring geometric deviation across 14 paired elements reflected about candidate midsagittal plane $x = x_{\text{centroid}}$ ($N = 1,000$ points per pair). `[INFERRED FROM EXECUTION RECORD]`
  - Generation of machine-readable inventory [`data/metadata/geometry_inventory.csv`](../../data/metadata/geometry_inventory.csv) and high-resolution 3D renders (PyVista engine). `[DOCUMENTED BEFORE EXECUTION]`
  - Milestone Synthesis Report: [`reports/phase2_digital_anatomy_report.md`](../../reports/phase2_digital_anatomy_report.md). `[DOCUMENTED BEFORE EXECUTION]`
- **Explicitly Out of Scope**:
  - Watertight solid repair of open component boundaries (deferred to Phase 4 for whole skull). `[DOCUMENTED BEFORE EXECUTION]`
  - Volumetric tetrahedral mesh generation (deferred to Phase 4). `[DOCUMENTED BEFORE EXECUTION]`
  - Finite element simulation or constitutive material assignment. `[DOCUMENTED BEFORE EXECUTION]`
  - Internal radiological density extraction (deferred to Phase 5). `[DOCUMENTED BEFORE EXECUTION]`

---

## 5. Methodological & Computational Design

### 5.1 Variables Being Evaluated (Independent Observables)
- 33 individual mesh geometries; point-cloud spatial distance distributions; bilateral reflection deviations. `[DOCUMENTED BEFORE EXECUTION]`

### 5.2 Controls & Invariant Processing
- **No In-Place Modification**: Original STL files in `data/meshes/original/` are strictly read-only and immutable. `[DOCUMENTED BEFORE EXECUTION]`
- **Raw Geometry Loading**: Meshes are loaded via Trimesh with automatic healing disabled (`process=False`) to preserve raw vertex coordinates, duplicate vertices, and open boundary edges exactly as exported by WitmerLab. `[DOCUMENTED BEFORE EXECUTION]`
- **Zero-Transformation Rule**: Assembly concatenation is performed strictly via identity transformations ($T = I$). No manual translation, rotation, or scaling is applied. `[DOCUMENTED BEFORE EXECUTION]`

### 5.3 Software Modules & Computational Methods
- **Inventory Engine**: `src/stegoceras_biomechanics/geometry/inventory.py`
  - `compute_boundary_and_manifold_edges()`: Evaluates face adjacency via edge occurrence counting; edges shared by 1 face are boundary edges, edges shared by $>2$ faces are non-manifold. `[DOCUMENTED BEFORE EXECUTION]`
  - `analyze_mesh_file()`: Derives bounding boxes, coordinate extents, centroids, and surface areas. `[DOCUMENTED BEFORE EXECUTION]`
- **Assembly & Spatial Analysis**: `src/stegoceras_biomechanics/geometry/assembly.py`
  - `assemble_components()`: Concatenates 32 component meshes into a unified multi-body Trimesh object. `[DOCUMENTED BEFORE EXECUTION]`
  - `compare_assembly_with_whole_skull()`: Samples $N = 50,000$ random points independently across both surfaces; queries nearest-point Euclidean distances using a SciPy $k$-d tree (`scipy.spatial.cKDTree`). `[INFERRED FROM EXECUTION RECORD]`
  - `evaluate_bilateral_symmetry()`: For each of 14 anatomical pairs, reflects Left element vertices across plane $x = x_{\text{centroid}}$:
    $$x_{\text{refl}} = 2 x_{\text{centroid}} - x$$
    and measures nearest-point distances onto the corresponding Right element ($N = 1,000$). `[INFERRED FROM EXECUTION RECORD]`
- **Visualization Engine**: Upgraded in commit `76ae2c4` to PyVista (`pyvista`) with smooth Phong lighting and multi-view orthographic camera angles. `[DOCUMENTED BEFORE EXECUTION]`

---

## 6. Acceptance & Verification Criteria

| ID | Criterion | Target / Standard | Epistemic Status | Verification Method |
| :--- | :--- | :--- | :--- | :--- |
| **C2.1** | Inventory Completeness | Exactly 33 rows in `geometry_inventory.csv` with 22 non-null columns. | `[DOCUMENTED BEFORE EXECUTION]` | `pytest tests/test_phase2_geometry.py::test_geometry_inventory_exists_and_complete` |
| **C2.2** | Whole-Skull Checksum | SHA-256 matches `aa994f41df3a7763a048f93339345dd68ea91f475386b8ae129ec80fd226c7c3`. | `[DOCUMENTED BEFORE EXECUTION]` | `pytest tests/test_phase2_geometry.py::test_whole_skull_mesh_integrity` |
| **C2.3** | Whole-Skull Topology | Exactly $1,200,102$ faces, $599,948$ vertices, $0$ boundary edges, $2$ non-manifold edges. | `[DOCUMENTED BEFORE EXECUTION]` | `pytest tests/test_phase2_geometry.py::test_whole_skull_mesh_integrity` |
| **C2.4** | Coordinate Frame Alignment | Assembly bounding box min/max bounds match whole skull within tolerance $\Delta \le 0.05$ units. | `[DOCUMENTED BEFORE EXECUTION]` | `pytest tests/test_phase2_geometry.py::test_component_assembly_coordinate_congruence` |
| **C2.5** | Component Containment | All 32 component bounding boxes strictly reside within the whole-skull spatial envelope. | `[INFERRED FROM EXECUTION RECORD]` | `test_component_assembly_coordinate_congruence` |
| **C2.6** | Spatial Correspondence | Whole skull $\to$ assembly median point distance $< 3.0$ coordinate units (empirical result: $0.850$). | `[INFERRED FROM EXECUTION RECORD]` | `pytest tests/test_phase2_geometry.py::test_surface_distance_and_bilateral_symmetry` |
| **C2.7** | Bilateral Pair Inventory | Exactly 14 bilateral pairs verified ($28$ meshes) plus $4$ unpaired midline elements. | `[DOCUMENTED BEFORE EXECUTION]` | `pytest tests/test_phase2_geometry.py::test_surface_distance_and_bilateral_symmetry` |
| **C2.8** | Physical Unit Calibration | Coordinate units calibrated to verified SI units (mm). | `[NOT ESTABLISHED]` | Uncalibrated in Phase 2; designated `candidate millimeter scale (uncalibrated)` with formal status `UNKNOWN`. Resolved downstream in Phase 5 Gate B. |
| **C2.9** | Component Watertightness | 100% of individual component meshes closed as watertight 2-manifolds. | `[NOT ESTABLISHED]` | Not established; 26 of 32 component meshes possess open boundary loops representing internal foramina/sinuses. |

---

## 7. Interpretation Limits
- **Coordinate Scale vs. Physical Units**: While bounding extents ($131 \times 200 \times 128$) are consistent with a candidate millimeter scale for *Stegoceras*, Phase 2 establishes coordinate-space consistency only; physical calibration requires independent scan acquisition logs or physical specimen measurements (Decision D02). `[DOCUMENTED BEFORE EXECUTION]`
- **Symmetry Deviation Interpretation**: Bilateral asymmetry metrics reflect a combined composite of biological asymmetry, taphonomic deformation during fossilization, segmentation boundary choices, and slight deviation of the candidate plane from the true anatomical midline. They must not be interpreted as pure biological fluctuating asymmetry. `[DOCUMENTED BEFORE EXECUTION]`
- **Boundary Openness**: The open boundary loops in 26 component meshes mean that the multi-part assembly cannot be directly tetrahedralized without prior surface closure and non-manifold interface resolution. `[DOCUMENTED BEFORE EXECUTION]`

---

## 8. Artifacts & Deliverables

- **Geometry Inventory**: [`data/metadata/geometry_inventory.csv`](../../data/metadata/geometry_inventory.csv) `[DOCUMENTED BEFORE EXECUTION]`
- **Milestone Synthesis Report**: [`reports/phase2_digital_anatomy_report.md`](../../reports/phase2_digital_anatomy_report.md) `[DOCUMENTED BEFORE EXECUTION]`
- **Publication Figures**:
  - Figure 01: `reports/figures/01_mesh_inventory_render.png` (Individual element mosaic) `[DOCUMENTED BEFORE EXECUTION]`
  - Figure 02: `reports/figures/02_component_assembly_render.png` (Articulated assembly) `[DOCUMENTED BEFORE EXECUTION]`
  - Figure 03: `reports/figures/03_assembly_whole_overlay.png` (Assembly vs. whole skull overlay) `[DOCUMENTED BEFORE EXECUTION]`
- **Geometry Software Modules**:
  - [`src/stegoceras_biomechanics/geometry/inventory.py`](../../src/stegoceras_biomechanics/geometry/inventory.py) `[DOCUMENTED BEFORE EXECUTION]`
  - [`src/stegoceras_biomechanics/geometry/assembly.py`](../../src/stegoceras_biomechanics/geometry/assembly.py) `[DOCUMENTED BEFORE EXECUTION]`
- **Automated Tests**: [`tests/test_phase2_geometry.py`](../../tests/test_phase2_geometry.py), [`tests/test_geometry.py`](../../tests/test_geometry.py) `[DOCUMENTED BEFORE EXECUTION]`

---

## 9. Decision Point & Programmatic Transition
- **Triggered Decision**: Decision D02 / D001 confirming that the surface meshes provide a coherent geometric baseline for Model A, while recognizing that internal material heterogeneity requires subsequent literature audit (Phase 3) and volumetric CT interrogation (Phase 5). `[DOCUMENTED BEFORE EXECUTION]`
- **Gate Outcome**: Phase 2 Gate declared **COMPLETE** (commit `8e9903d`), authorizing progression to Phase 3 Published-Model Audit. `[INFERRED FROM EXECUTION RECORD]`

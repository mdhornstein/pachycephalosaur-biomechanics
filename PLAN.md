# Master Research & Implementation Plan: Stegoceras Biomechanics & Uncertainty Quantification

**Taxon**: *Stegoceras validum* Lambe, 1902  
**Taxonomic Lectotype**: **CMN 515** (Canadian Museum of Nature, Ottawa)  
**Study Specimen**: **UALVP 2** (University of Alberta Laboratory for Vertebrate Paleontology, Edmonton; articulated skull, mandible, and postcrania)  
**Primary Biomechanics Target**: Snively, E. & Theodor, J. M. (2011). *Common functional correlates of head-strike behavior in bovid artiodactyls and pachycephalosaurs*. PLoS ONE 6(6): e21412.  
**Core Scientific Question**: *How robust are conclusions about pachycephalosaur cranial biomechanics to uncertainty in geometry, material properties, loading conditions, and modeling assumptions?*

---

## 🏛️ 1. Project Overview & Document Architecture

The objective of this project is to construct a fully reproducible, open-source computational biomechanics and uncertainty quantification (UQ) pipeline for *Stegoceras validum*. The project proceeds through systematic data ingestion, geometric validation, CT segmentation, analytical validation, finite-element reproduction, sensitivity analysis, and surrogate-based active learning.

### Repository Role Separation
To maintain clear boundaries between scientific intent, evidence authority, operational workflow, and empirical findings, project documents fulfill distinct, non-overlapping functions:

| Document Role | File Path | Core Function / Question Answered |
| :--- | :--- | :--- |
| **Research Index** | [`PLAN.md`](PLAN.md) | *Where is the research program going?* (Master roadmap & phase index) |
| **Evidence Authority** | [`docs/LITERATURE_TO_MODEL_DECISIONS.md`](docs/LITERATURE_TO_MODEL_DECISIONS.md) | *What does the published evidence permit?* (Scientific constraints & decision basis) |
| **Prospective Design** | [`docs/phase_design/*`](docs/phase_design/) | *How are we going to test the next question?* (Predeclared methods & criteria) |
| **Living State** | [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) | *What is true right now?* (Verified milestones & frozen deliverables) |
| **Empirical Results** | [`reports/*`](reports/) | *What did we actually do and observe?* (Comprehensive milestone reports) |
| **Decision Ledger** | [`docs/DECISIONS.md`](docs/DECISIONS.md) | *What did the evidence permit us to decide?* (Immutable decision register D01–D17) |
| **Operational Handoff**| [`HANDOFF.md`](HANDOFF.md) | *What does the next researcher need to do?* (Immediate commands & next step) |
| **Traceability Map** | [`docs/RESEARCH_TRACEABILITY.md`](docs/RESEARCH_TRACEABILITY.md) | *How do code, data, tests, and reports link?* (End-to-end cryptographic provenance) |

---

## 🗺️ 2. Research Program & Phase Status Index

```text
Phase 1–2   Computational foundation               HISTORICAL (Complete)
Phase 3     Scientific / model audit               COMPLETE
Phase 4     Controlled FE verification (Model A)   COMPLETE
Phase 5A    CT acquisition & integrity             COMPLETE
Phase 5B    CT ↔ G₀ registration                  COMPLETE
Phase 5C    CT image semantics & intensity audit   COMPLETE (Frozen)
Phase 5D    Published material-inference logic     NEXT (Active Design)
Phase 5E    Model B volume construction            FUTURE
Phase 5F    Model B solve & verification           FUTURE
Phase 6     A/B mechanical comparison              FUTURE
Phase 7     Focused sensitivity & scenario bounds  FUTURE
Phase 8     UQ / uncertainty propagation           FUTURE
Phase 9     Comparative pachycephalosaur analysis  FUTURE
```

### Master Phase Index Table

| Phase / Gate | Focus | Governing Design | Report / Artifact | Key Decision | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | Digital Ingestion & Provenance | [`reports/phase1_data_and_geometry_report.md`](reports/phase1_data_and_geometry_report.md) | [`data/metadata/dataset_manifest.yaml`](data/metadata/dataset_manifest.yaml) | D01 | **COMPLETE** |
| **Phase 2** | Anatomy Inventory & Coordinate Alignment | [`reports/phase2_digital_anatomy_report.md`](reports/phase2_digital_anatomy_report.md) | [`data/metadata/geometry_inventory.csv`](data/metadata/geometry_inventory.csv) | D02 | **COMPLETE** |
| **Phase 3** | Published-Model Audit & Input Matrix | [`docs/phase_design/PHASE3_DESIGN_RECONSTRUCTED.md`](docs/phase_design/PHASE3_DESIGN_RECONSTRUCTED.md) | [`reports/snively_theodor_model_reconstruction.md`](reports/snively_theodor_model_reconstruction.md) | D04–D07 | **COMPLETE** |
| **Phase 4** | Surface FEA Benchmark (Model A Baseline) | [`reports/phase4_fea_benchmark_report.md`](reports/phase4_fea_benchmark_report.md) | [`models/phase4/`](models/phase4/), Figures 08–12 | D03, D08–D10 | **COMPLETE** |
| **Phase 5 Gate A** | Micro-CT DICOM Integrity & Spatial Mapping | [`docs/phase_design/PHASE5_GATE_A_DESIGN.md`](docs/phase_design/PHASE5_GATE_A_DESIGN.md) | [`reports/phase5_gate_a_dicom_report.md`](reports/phase5_gate_a_dicom_report.md) | D11 | **COMPLETE** |
| **Phase 5 Gate B** | Volumetric CT ↔ $G_0$ Rigid Registration | [`docs/phase_design/PHASE5_GATE_B_DESIGN.md`](docs/phase_design/PHASE5_GATE_B_DESIGN.md) | [`reports/phase5_gate_b_registration_report.md`](reports/phase5_gate_b_registration_report.md) | D11 | **COMPLETE** |
| **Phase 5 Gate C** | Reconstructed CT Intensity Semantics & Zonation | [`docs/phase_design/PHASE5_GATE_C_DESIGN.md`](docs/phase_design/PHASE5_GATE_C_DESIGN.md) | [`reports/phase5_gate_c_semantics_report.md`](reports/phase5_gate_c_semantics_report.md), Figs 13 & 14 | D011 (Frozen) | **COMPLETE** |
| **Phase 5 Gate D** | Published Material Inference Logic | [`docs/phase_design/PHASE5_GATE_D_DESIGN.md`](docs/phase_design/PHASE5_GATE_D_DESIGN.md) | `reports/phase5_gate_d_material_report.md` | D012 | **NEXT** |
| **Phase 5 Gate E** | Model B 3-Zone Mesh Construction | `docs/phase_design/PHASE5_GATE_E_DESIGN.md` | `results/phase5/gate_e_mesh_metrics.json` | D013 | FUTURE |
| **Phase 5 Gate F** | Model B FEA Solving & Verification | `docs/phase_design/PHASE5_GATE_F_DESIGN.md` | `reports/phase5_gate_f_solve_report.md` | D014 | FUTURE |
| **Phase 6** | Decisive Model A vs. Model B Comparison | `docs/phase_design/PHASE6_DESIGN.md` | `reports/phase6_material_comparison_report.md` | D015 | FUTURE |
| **Phase 7** | Focused Sensitivity & Scenario Analysis | `docs/phase_design/PHASE7_DESIGN.md` | `reports/phase7_sensitivity_report.md` | D016 | FUTURE |
| **Phase 8** | Probabilistic UQ & Active Learning Surrogates | `docs/phase_design/PHASE8_DESIGN.md` | `reports/phase8_uq_surrogate_report.md` | D017 | FUTURE |
| **Phase 9** | Comparative Pachycephalosaur Biomechanics | `docs/phase_design/PHASE9_DESIGN.md` | `reports/phase9_comparative_report.md` | — | FUTURE |

---

## 🔬 3. Phase Descriptions & Execution Flow

### Phase 1: Data Acquisition & Provenance Manifest *(Complete)*
- Comprehensive inventory of public UALVP 2 digital records identified across MorphoSource, WitmerLab, and Sketchfab.
- Implementation of 4-tier provenance taxonomy (`primary_scan`, `segmented_from_primary_scan`, `researcher_derived`, `secondary_reference`).
- Machine-readable manifest [`data/metadata/dataset_manifest.yaml`](data/metadata/dataset_manifest.yaml) and checksum verification tooling.
- Milestone Synthesis Report: [`reports/phase1_data_and_geometry_report.md`](reports/phase1_data_and_geometry_report.md).

### Phase 2: Digital Anatomy Inventory & Geometry Validation *(Complete)*
- Ingested and inventoried 33 MorphoSource surface STLs (Whole Skull `000018284` + 32 Component Bones `000043121-000043162`).
- Verified common native coordinate system alignment ($\Delta \le 0.029$ coordinate units) and zero-transformation assembly.
- Characterized 14 bilateral symmetry pairs and sampled nearest-point distance distributions.
- Milestone Synthesis Report: [`reports/phase2_digital_anatomy_report.md`](reports/phase2_digital_anatomy_report.md).

### Phase 3: Published-Model Audit & Input Matrix *(Complete)*
- Line-by-line model parameter and methodology extraction from primary reference Snively & Theodor (2011) ([`literature/snively_theodor_2011_model_audit.md`](literature/snively_theodor_2011_model_audit.md)).
- Constructed formal Biomechanics Input Matrix ([`data/metadata/biomechanics_input_matrix.csv`](data/metadata/biomechanics_input_matrix.csv)) with 5-tier evidence levels and 7 availability categories.
- Reconstructed published computational workflow and separated geometry-limited, parameter-limited, and model-form uncertainties ([`reports/snively_theodor_model_reconstruction.md`](reports/snively_theodor_model_reconstruction.md)).
- Formulated Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](docs/LITERATURE_TO_MODEL_DECISIONS.md)).

### Phase 4: Surface FEA Benchmark & Discretization Sensitivity *(Complete)*
- Immutable canonical master surface $G_0$ (`stegoceras_ualvp2_canonical_master.stl`, processed geometry-array SHA-256 `5adcf5369626...`).
- Volumetric tetrahedral mesh hierarchy ($h_1, h_2, h_3, h_4$) generated via TetGen with volume refinement.
- Geodesic load patch on dorsal dome apex ($3000.0\text{ mm}^2$, $1000.0\text{ N}$) and anatomical boundary restraints.
- Solved Model A baseline (homogeneous isotropic linear elasticity, $E = 17.0\text{ GPa}, \nu = 0.30$).
- Milestone Synthesis Report: [`reports/phase4_fea_benchmark_report.md`](reports/phase4_fea_benchmark_report.md); Figures 08–12 in [`reports/figures/`](reports/figures/).

### Phase 5: UALVP 2 CT Characterization & Material A/B Experiment *(Active Phase)*
- **Gate A (CT Ingestion & Integrity)** *(Complete)*: Ingested 514 micro-CT DICOM slices (`UALVP2-CT-DICOM-CRAN-01`), established zero-based indexing, confirmed uncalibrated 16-bit intensity values ([`reports/phase5_gate_a_dicom_report.md`](reports/phase5_gate_a_dicom_report.md)).
- **Gate B (CT ↔ $G_0$ Registration)** *(Complete)*: Rigid registration establishing sub-voxel outer cranial alignment ($0.2472\text{ mm}$ translation) and approximately unit scale ([`reports/phase5_gate_b_registration_report.md`](reports/phase5_gate_b_registration_report.md)).
- **Gate C (Reconstructed Intensity Semantics & Zonation Audit)** *(Complete / Frozen)*: Full-volume dynamic range audit ($396.8\text{M}$ voxels, Otsu $20,864$). Established that reconstructed CT image intensity alone does not recover the hypothesized Zone 2/Zone 3 boundary in sampled dome regions ($\text{CNR} = 0.0616 \ll 1.0$, descriptive $\text{AUC} = 0.5132$). Identified $16.2\%$ low-intensity voxels in core compatible with internal void/partial-volume structure. Decision D011 mandating literature-informed geometric rules for Model B ([`reports/phase5_gate_c_semantics_report.md`](reports/phase5_gate_c_semantics_report.md); Figures 13 & 14).
- **Gate D (Published Material Inference Logic)** *(Next Action)*: Formalize explicit mathematical and spatial rules from Snively & Theodor (2011) and Schott et al. (2011) into executable code mapping onto canonical frame $G_0$ ([`docs/phase_design/PHASE5_GATE_D_DESIGN.md`](docs/phase_design/PHASE5_GATE_D_DESIGN.md)).
- **Gate E (Model B Mesh Construction)** *(Future)*: Map 3-zone architecture onto frozen $h_3$ volume mesh without altering surface boundary geometry.
- **Gate F (Model B Solve & Verification)** *(Future)*: Solve Model B under identical loading and boundary conditions.

### Phase 6: Decisive Model A vs. Model B Mechanical Comparison *(Future)*
- Compare compliance, strain-energy partitioning, and stress redistribution to the endocranial cavity between homogeneous Model A and heterogeneous Model B.

### Phase 7: Focused Sensitivity & Discrete Scenario Analysis *(Future)*
- Impact inclination variations ($\alpha \in [0^\circ, 20^\circ]$), contact patch variations ($A \in [500, 3000]\text{ mm}^2$), cervical foundation compliance (springs vs. rigid).

### Phase 8: Probabilistic UQ & Active Learning Surrogates *(Future)*
- Rigorous parameter distributions strictly for continuous variables that cannot be factored out analytically.
- Sized sampling design (Sobol variance decomposition) and surrogate modeling (Gaussian Processes).

### Phase 9: Comparative Pachycephalosaur Biomechanics *(Future)*
- Expand validated pipeline across comparative taxa (*Acrotholus audeti*, *Prenocephale prenes*, *Homalocephale calathoceros*, *Ovibos moschatus*, *Ovis canadensis*).

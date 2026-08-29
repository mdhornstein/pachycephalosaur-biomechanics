# Stegoceras Biomechanics + Uncertainty Quantification

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Package Manager: uv](https://img.shields.io/badge/environment-uv-purple.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A reproducible, open-source computational biomechanics pipeline for the pachycephalosaur dinosaur *Stegoceras validum*, focusing on **UALVP 2** (an exceptionally complete referred specimen with articulated skull and postcrania; taxonomic lectotype is CMN 515).

---

## 🎯 1. Project Objective & Scope

The central scientific question investigated by this project is:
> **How robust are conclusions about pachycephalosaur cranial biomechanics to uncertainty in geometry, material properties, loading conditions, and modeling assumptions?**

Rather than asserting or disputing behavioral hypotheses (e.g., head-butting vs. flank-butting vs. display), this project establishes a rigorous, transparent computational pipeline:
1. **Acquisition & Documentation** of public CT/3D morphology (WitmerLab, MorphoSource, Sketchfab).
2. **Geometry Inspection & Validation** (topological checks, scale verification, manifold inspection).
3. **Cranial Anatomical Reconstruction** from CT volumes.
4. **Finite Element Modeling (FEA)** reproducing target benchmarks from primary literature (*Snively & Theodor, 2011*).
5. **Uncertainty Quantification (UQ) & Global Sensitivity Analysis** (Monte Carlo, Latin Hypercube Sampling, Sobol indices).
6. **Surrogate Modeling & Active Learning** (Gaussian processes / probabilistic surrogates) to reduce the cost of computational simulations.

---

## 📁 2. Repository Layout

```text
pachycephalosaurus-biomechanics/
├── README.md                           # Project overview and quickstart
├── PLAN.md                             # Master 18-phase implementation roadmap
├── DATA_SOURCES.md                     # Comprehensive UALVP 2 data catalog & provenance audit
├── LICENSE                             # MIT License
├── CITATION.cff                        # Citation File Format metadata
├── pyproject.toml                      # Project package & dependency specifications (hatchling build)
├── environment.yml                     # Conda/Mamba environment specification
├── .gitignore                          # Excludes raw scans, binary meshes, and virtualenvs
│
├── data/
│   ├── raw/
│   │   ├── dicom/                      # Raw DICOM slices (immutable, not committed to git)
│   │   └── downloads/                  # Staging area for user-downloaded archive files
│   ├── intermediate/                   # Segmented masks & threshold volumes
│   ├── meshes/
│   │   ├── original/                   # Original un-altered 3D surface files
│   │   ├── cleaned/                    # Standardized, watertight, scale-verified meshes
│   │   └── fe/                         # Solid tetrahedral / hexahedral meshes for FEA
│   ├── reference/                      # 3D PDFs and animation reference files
│   ├── metadata/
│   │   ├── dataset_manifest.yaml       # Machine-readable provenance & SHA-256 checksum manifest
│   │   ├── geometry_inventory.csv      # 33-mesh quantitative topological & coordinate catalog
│   │   └── biomechanics_input_matrix.csv # Formally audited model input & evidence matrix
│   │
│   └── meshes/                         # Raw and cleaned 3D surface models
│       └── original/                   # 33 acquired MorphoSource STLs
│
├── literature/                         # Parameter audits and methodology logs
│   ├── snively_theodor_2011_model_audit.md # Line-by-line model input audit
│   └── missing_input_sources.md        # Alternative source & gap resolution strategy
│
├── notebooks/
│   ├── 01_data_inventory.ipynb         # Interactive dataset audit & provenance inspector
│   ├── 02_load_skull_mesh.ipynb        # Mesh loading, topology, scale hint, and manifold analysis
│   ├── 03_component_geometry_inventory.ipynb # Multi-bone inventory & topological audit
│   ├── 04_skull_component_assembly.ipynb     # Coordinate congruence & bilateral symmetry
│   └── 05_model_input_dimensional_audit.ipynb # Dimensional & unit consistency verification
│
├── src/
│   └── stegoceras_biomechanics/        # Reusable scientific Python package
│       ├── io/                         # Manifest parsers, checksum validators, secure ingestion tools
│       ├── geometry/                   # Inventory engines, assembly metrics, coordinate checkers
│       └── visualization/              # Publication 3D multi-view PyVista rendering engine
│
├── reports/                            # Formal milestone synthesis reports & figures
│   ├── phase1_data_and_geometry_report.md
│   ├── phase2_digital_anatomy_report.md
│   ├── snively_theodor_model_reconstruction.md
│   ├── phase3_recommended_benchmark.md
│   ├── walkthrough.md
│   └── figures/                        # Publication 3D multi-panel renders
├── tests/                              # Automated Pytest validation suite (19 passing tests)
```

---

## ⚡ 3. Quickstart & Environment Setup

This project uses [`uv`](https://github.com/astral-sh/uv) for fast, deterministic Python environment management.

```bash
# 1. Clone the repository
git clone git@github-mdhornstein:mdhornstein/pachycephalosaur-biomechanics.git
cd pachycephalosaur-biomechanics

# 2. Sync virtual environment and install dependencies
uv sync --all-extras

# 3. Run automated tests
uv run pytest -v

# 4. Launch JupyterLab for interactive notebooks
uv run jupyter lab
```

---

## 🔬 4. Current Milestone: Phase 1 (Infrastructure & Data Inventory Complete)

This repository is currently holding at the **Phase 1 Gate**:
- Data sources cataloged in [`DATA_SOURCES.md`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/DATA_SOURCES.md).
- Manifest and provenance codified in [`data/metadata/dataset_manifest.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/data/metadata/dataset_manifest.yaml).
- Checksum validation and secure ingestion tooling ready (`scripts/ingest_data.py`).
- Phase 1 synthesis documented in [`reports/phase1_data_and_geometry_report.md`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/reports/phase1_data_and_geometry_report.md).

*The next milestone is the physical acquisition and inspection of primary CT data and reference meshes before proceeding to geometric validation and FEA preprocessing.*

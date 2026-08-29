# Stegoceras Biomechanics + Uncertainty Quantification

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Package Manager: uv](https://img.shields.io/badge/environment-uv-purple.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A reproducible, open-source computational biomechanics pipeline for the pachycephalosaur dinosaur *Stegoceras validum* (specimen **UALVP 2**, holotype cranium).

---

## 🎯 1. Project Objective & Scope

The long-term scientific question investigated by this project is:
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
stegoceras-biomechanics/
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
│   └── metadata/
│       └── dataset_manifest.yaml       # Machine-readable provenance & SHA-256 checksum manifest
│
├── literature/                         # Reference documentation, notes, and methodology logs
├── notebooks/
│   ├── 01_data_inventory.ipynb         # Interactive dataset audit & provenance inspector
│   └── 02_load_skull_mesh.ipynb        # Mesh loading, topology, scale, and manifold analysis
│
├── src/
│   └── stegoceras_biomechanics/        # Reusable scientific Python package
│       ├── __init__.py
│       ├── io/                         # Manifest parsers, checksum validators, ingestion tools
│       ├── geometry/                   # Mesh operations, topological checks, scale conversions
│       ├── segmentation/               # CT volume thresholding & Slicer integration (placeholder)
│       ├── meshing/                    # Surface and volume meshing pipelines (placeholder)
│       ├── fea/                        # Finite element model configs & solver runners (placeholder)
│       ├── uq/                         # Sampling, uncertainty propagation & SALib tools (placeholder)
│       └── visualization/              # 3D PyVista plotting & slice rendering utilities
│
├── models/                             # Pre-configured simulation models & solver input files
├── simulations/                        # Local FE simulation outputs
├── results/                            # Consolidated post-processed data, metrics, and plots
├── reports/                            # Formal phase reports and scientific synthesis
│   └── phase1_data_and_geometry_report.md
├── scripts/
│   └── ingest_data.py                  # CLI tool for validating, checksumming, and ingesting raw data
└── tests/                              # Automated Pytest validation suite
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

## 🔬 4. Current Phase: Phase 0 & Phase 1

This repository is currently at the **Phase 1 Gate**:
- Data sources cataloged and audited in [`DATA_SOURCES.md`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/DATA_SOURCES.md).
- Manifest and provenance codified in [`data/metadata/dataset_manifest.yaml`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/data/metadata/dataset_manifest.yaml).
- Interactive exploratory workflows in `notebooks/01_data_inventory.ipynb` and `notebooks/02_load_skull_mesh.ipynb`.
- Phase 1 findings documented in `reports/phase1_data_and_geometry_report.md`.

*Per project principles, finite element simulations will not be executed until Phase 1 data and geometry gates are reviewed and validated.*

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
├── HANDOFF.md                          # Fast living operational entry point for humans and agents
├── PLAN.md                             # Master research and implementation roadmap
├── DATA_SOURCES.md                     # Comprehensive UALVP 2 data catalog & provenance audit
├── LICENSE                             # MIT License
├── CITATION.cff                        # Citation File Format metadata
├── pyproject.toml                      # Project package & dependency specifications (hatchling build)
├── environment.yml                     # Conda/Mamba environment specification
├── .gitignore                          # Excludes raw scans, binary meshes, and virtualenvs
│
├── docs/                               # Canonical living state, decision logs, snapshots, & documentation system
│   ├── CURRENT_STATE.md                # Canonical living scientific and numerical model definition
│   ├── DECISIONS.md                    # Append-only architectural and scientific decision log
│   ├── DOCUMENTATION_SYSTEM.md         # Two-dimensional authority and documentation governance system
│   └── snapshots/                      # Immutable milestone freeze records
│
├── data/
│   ├── raw/
│   │   ├── dicom/                      # Raw DICOM slices (immutable, not committed to git)
│   │   └── downloads/                  # Staging area for user-downloaded archive files
│   ├── meshes/
│   │   ├── original/                   # Original un-altered 3D surface files
│   │   ├── cleaned/                    # Standardized, watertight, scale-verified meshes
│   │   └── fe/                         # Solid tetrahedral meshes for FEA
│   ├── reference/                      # 3D PDFs and animation reference files
│   └── metadata/
│       ├── dataset_manifest.yaml       # Machine-readable provenance & SHA-256 checksum manifest
│       ├── geometry_inventory.csv      # 33-mesh quantitative topological & coordinate catalog
│       └── biomechanics_input_matrix.csv # Formally audited model input & evidence matrix
│
├── literature/                         # Parameter audits, scoping reviews, and evidence matrices
│   ├── stegoceras_biomechanics_literature_synthesis.md # Master scoping review & gap analysis
│   ├── stegoceras_biomechanics_evidence_matrix.csv     # Master consolidated evidence matrix
│   ├── snively_theodor_2011_model_audit.md # Line-by-line model input audit
│   ├── missing_input_sources.md        # Alternative source & gap resolution strategy
│   ├── protocols/                      # Search methodology, queries, & review design
│   └── dossiers/                       # Specialist evidence dossiers (FEA, Pachycephalosauria, UQ, CT)
│
├── notebooks/
│   ├── 01_data_inventory.ipynb         # Interactive dataset audit & provenance inspector
│   ├── 02_load_skull_mesh.ipynb        # Mesh loading, topology, scale hint, and manifold analysis
│   ├── 03_component_geometry_inventory.ipynb # Multi-bone inventory & topological audit
│   ├── 04_skull_component_assembly.ipynb     # Coordinate congruence & bilateral symmetry
│   ├── 05_model_input_dimensional_audit.ipynb # Dimensional & unit consistency verification
│   ├── 06_fe_geometry_preparation.ipynb # Watertight repair & volumetric tetrahedralization
│   ├── 07_fe_baseline_analysis.ipynb   # FEA solve, equilibrium, & von Mises stresses
│   ├── 08_fe_mesh_convergence.ipynb    # Multi-tier h-refinement & discretization analysis
│   └── 09_fe_linearity_validation.ipynb # Hookean linearity & strain energy scaling
│
├── src/
│   └── stegoceras_biomechanics/        # Reusable scientific Python package
│       ├── io/                         # Manifest parsers, checksum validators, secure ingestion tools
│       ├── geometry/                   # Inventory engines, assembly metrics, coordinate checkers
│       ├── visualization/              # Publication 3D multi-view PyVista rendering engine
│       ├── fea/                        # 3D finite element elasticity solver, loads, BCs, & metrics
│       ├── uq/                         # Uncertainty quantification, sampling, & sensitivity (Phase 5–7)
│       └── segmentation/               # CT volume density masking (Phase 8, deferred to DICOM acquisition)
│
├── reports/                            # Formal milestone synthesis reports & figures
│   ├── phase1_data_and_geometry_report.md
│   ├── phase2_digital_anatomy_report.md
│   ├── snively_theodor_model_reconstruction.md
│   ├── phase3_recommended_benchmark.md
│   ├── phase4_fea_benchmark_report.md
│   ├── walkthrough.md
│   └── figures/                        # Publication 3D multi-panel renders
├── tests/                              # Automated Pytest validation suite
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

## 🔬 4. Current Status & State Architecture

To eliminate documentation drift and maintain a verifiable scientific audit trail across multi-session research, this repository separates high-level project documentation from living computational state:

- **Operational Entry Point**: [`HANDOFF.md`](HANDOFF.md) — What the active research milestone is, what is verified, and the single immediate next action.
- **Canonical Living State**: [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md) — The active scientific, geometric, boundary condition, and numerical model definition.
- **Documentation Conventions**: [`docs/DOCUMENTATION_SYSTEM.md`](docs/DOCUMENTATION_SYSTEM.md) — The two-dimensional state system and authority hierarchy.
- **Decision History**: [`docs/DECISIONS.md`](docs/DECISIONS.md) — Append-only scientific and architectural rationale log.
- **Milestone Snapshots**: [`docs/snapshots/`](docs/snapshots/) — Immutable historical time-capsules tied to milestone commit SHAs.
- **Master Research Roadmap**: [`PLAN.md`](PLAN.md) — Forward-looking multi-phase computational roadmap.

*For current project phase, computational status, and recent empirical results, refer to [`HANDOFF.md`](HANDOFF.md) and [`docs/CURRENT_STATE.md`](docs/CURRENT_STATE.md).*

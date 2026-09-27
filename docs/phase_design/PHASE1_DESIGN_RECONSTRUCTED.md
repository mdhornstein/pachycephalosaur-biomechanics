# Phase 1 Design (Retrospective Reconstruction): Digital Morphology Data Acquisition, Provenance Manifest & Ingestion Infrastructure

> [!IMPORTANT]
> **RETROSPECTIVE RECONSTRUCTION — CREATED AFTER EXECUTION**  
> This document reconstructs the methodological intent and execution logic of Phase 1 from the surviving project record (commits `53492a2`, `516274a`, `570dded`, and `bd6f4ee`; [`reports/phase1_data_and_geometry_report.md`](../../reports/phase1_data_and_geometry_report.md); [`data/metadata/dataset_manifest.yaml`](../../data/metadata/dataset_manifest.yaml); and Decision D001 / D01). It is not a contemporaneous pre-execution design and must not be interpreted as evidence that these criteria were predeclared.

**Document Role**: Retrospectively Reconstructed Phase Design  
**Status**: RETROSPECTIVELY RECONSTRUCTED & FROZEN  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md) §4.4, Decision D01; [`docs/DECISIONS.md`](../DECISIONS.md), Decision D001)  
**Specimen**: *Stegoceras validum* UALVP 2 (referred specimen comprising cranium, mandible, postcrania; lectotype CMN 515)  
**Target Codebase / Pipeline**: `scripts/ingest_data.py`, `src/stegoceras_biomechanics/io/manifest.py`, `tests/test_manifest.py`, `tests/test_ingest.py`  
**Historical Execution Baseline**: Commits `53492a2` $\to$ `bd6f4ee` (August 28, 2026)  

---

### Epistemic Status Taxonomy
To maintain strict scientific auditability, every methodological item, requirement, parameter, and criterion in this retrospective document is labeled with one of four explicit epistemic categories:

| Status Tag | Operational Definition |
| :--- | :--- |
| `[DOCUMENTED BEFORE EXECUTION]` | Directly attested in contemporaneous pre-execution commits, initial code comments, or external repository metadata prior to milestone completion. |
| `[INFERRED FROM EXECUTION RECORD]` | Derived deterministically from surviving execution scripts, test assertions, and synthesis reports produced during Phase 1 execution. |
| `[RETROSPECTIVE RECONSTRUCTION]` | Formulated during post-execution documentation synthesis to reconstruct the implicit scientific logic and decision criteria. |
| `[NOT ESTABLISHED]` | Deliberately marked as unmeasured, unverified, or explicitly deferred to downstream phases to prevent retroactive fabrication. |

---

## 1. Scientific Question
*What digital morphological and radiological assets for Stegoceras validum (specimen UALVP 2) can actually be obtained from public repositories, what are their modalities, resolutions, and licensing constraints, and how can they be placed under strict cryptographic version control under an uncompromising zero-fabrication metadata policy?* `[INFERRED FROM EXECUTION RECORD]`

Specifically:
1. Which digital assets in the public paleontological record represent primary volumetric radiological scans vs. researcher-derived polygonal surface meshes? `[INFERRED FROM EXECUTION RECORD]`
2. What licensing constraints govern downstream academic reproduction and public computational dissemination? `[DOCUMENTED BEFORE EXECUTION]`
3. How can an automated data ingestion engine guarantee cryptographic integrity (SHA-256) and safeguard local filesystem environments against malicious archive structures (path traversal)? `[DOCUMENTED BEFORE EXECUTION]`
4. Which anatomical parameters and physical units can be certified from raw data vs. which must be marked `UNKNOWN` prior to empirical inspection? `[DOCUMENTED BEFORE EXECUTION]`

---

## 2. Motivation / Prior Evidence
- **Published Computational Baseline**: Snively & Theodor (2011) *PLoS ONE* 6(6): e21412 published 2D and 3D FEA simulations of cranial impact in *Stegoceras validum* based on specimen UALVP 2, reporting that the cranium was scanned via micro-CT at the University of Texas High-Resolution X-ray CT Facility (UTCT). However, the raw 2.2M element Strand7 finite element mesh was not deposited in a public repository. `[DOCUMENTED BEFORE EXECUTION]`
- **Public Repository Fragmentation**: UALVP 2 digital records were identified across multiple disparate repositories (MorphoSource, Sketchfab, WitmerLab pachycephalosaur 3D portal), each presenting distinct file formats, coordinate states, and metadata descriptors. `[INFERRED FROM EXECUTION RECORD]`
- **Zero-Fabrication Imperative**: Prior to performing biomechanical modeling, all input assets must be cryptographically cataloged, their provenance tiers certified, and unmeasured values held as `UNKNOWN` rather than populated with placeholder assumptions. `[DOCUMENTED BEFORE EXECUTION]`

---

## 3. Hypotheses & Competing Expectations
- **Expectation A (Public CT Availability)**: Public morphological repositories (e.g. MorphoSource) contain discrete, directly downloadable primary micro-CT slice stacks (DICOM or TIFF volume stacks) for UALVP 2 under standard academic open access. `[RETROSPECTIVE RECONSTRUCTION]`
- **Expectation B (Segmented Surface Meshes Only)**: Downloadable public files from MorphoSource comprise researcher-derived polygonal surface meshes (STLs) segmented from CT, while primary volumetric radiological data remain undeposited or require separate institutional authorization. `[RETROSPECTIVE RECONSTRUCTION]`
- **Observable Signature**: Physical download inspection and manifest extraction either yield volumetric image series with DICOM headers or yield discrete surface geometry files (STLs). `[INFERRED FROM EXECUTION RECORD]`

---

## 4. Scope
- **In Scope**:
  - Comprehensive inventory of public digital assets for *Stegoceras validum* UALVP 2 across MorphoSource, WitmerLab, and Sketchfab. `[DOCUMENTED BEFORE EXECUTION]`
  - Implementation of a 4-tier provenance taxonomy: `primary_scan`, `segmented_from_primary_scan`, `researcher_derived`, and `secondary_reference`. `[DOCUMENTED BEFORE EXECUTION]`
  - Implementation of safe archive extraction tooling with path-traversal prevention (`scripts/ingest_data.py`). `[DOCUMENTED BEFORE EXECUTION]`
  - Generation of machine-readable cryptographic manifest [`data/metadata/dataset_manifest.yaml`](../../data/metadata/dataset_manifest.yaml) recording file sizes, SHA-256 digests, URLs, and licenses. `[DOCUMENTED BEFORE EXECUTION]`
  - Identification of manual/human authentication requirements for protected media. `[INFERRED FROM EXECUTION RECORD]`
  - Milestone Synthesis Report: [`reports/phase1_data_and_geometry_report.md`](../../reports/phase1_data_and_geometry_report.md). `[DOCUMENTED BEFORE EXECUTION]`
- **Explicitly Out of Scope**:
  - 3D mesh geometric inspection, manifold edge audit, or surface repair (deferred to Phase 2). `[DOCUMENTED BEFORE EXECUTION]`
  - Volumetric CT voxel spacing extraction or Hounsfield density inspection (deferred to Phase 5 Gate A / Gate C). `[DOCUMENTED BEFORE EXECUTION]`
  - Finite element meshing, material property assignment, or solver execution (deferred to Phase 4 / Phase 5). `[DOCUMENTED BEFORE EXECUTION]`

---

## 5. Methodological & Computational Design

### 5.1 Variables Being Evaluated (Independent Inventory Targets)
- Digital asset identity, source repository, download URL, access mechanism, licensing tier, and declared morphological content. `[DOCUMENTED BEFORE EXECUTION]`

### 5.2 Controls & Invariant Policies
- **Zero-Fabrication Policy**: Any dimension, polygon count, slice thickness, or pixel spacing not directly measured from an ingested file must be explicitly recorded as `UNKNOWN` or null in manifests and reports. Placeholder defaults are strictly prohibited. `[DOCUMENTED BEFORE EXECUTION]`
- **Taxonomic Grounding**: The study specimen is referred specimen UALVP 2 (University of Alberta); the taxonomic lectotype is CMN 515 (Canadian Museum of Nature). Model claims apply specifically to UALVP 2 and must not conflate the two specimens. `[DOCUMENTED BEFORE EXECUTION]`
- **Filesystem Isolation**: Ingestion scripts must operate within repository data boundaries (`data/raw/`, `data/metadata/`) and prevent writes outside workspace roots. `[DOCUMENTED BEFORE EXECUTION]`

### 5.3 Provenance Tier Classification
Every candidate dataset is assigned to one of four mutually exclusive provenance tiers: `[DOCUMENTED BEFORE EXECUTION]`
1. `primary_scan`: Raw volumetric X-ray computed tomography slice stacks or unedited scanner projections.
2. `segmented_from_primary_scan`: 3D polygonal surface meshes generated directly from primary scan volumes via thresholding or manual segmentation (e.g. WitmerLab STLs).
3. `researcher_derived`: Secondary computational models, finite element meshes, or transformed reconstructions modified by researchers (e.g. published Strand7 FE meshes).
4. `secondary_reference`: Visualization models, 3D PDFs, comparative literature figures, or external reference tables.

### 5.4 Software Architecture & Ingestion Tooling
- **Primary CLI Ingestion Engine**: `scripts/ingest_data.py` `[DOCUMENTED BEFORE EXECUTION]`
- **Reusable Core Modules**:
  - `src/stegoceras_biomechanics/io/manifest.py`: `load_manifest()`, `get_dataset_entry()`, `compute_sha256()`, `audit_local_inventory()`. `[DOCUMENTED BEFORE EXECUTION]`
- **Archive Extraction Security**: Extraction algorithm in `scripts/ingest_data.py` inspects every member in `.zip` archives to reject absolute paths, `..` directory traversals, or filesystem links before extracting to `data/raw/downloads/`. `[DOCUMENTED BEFORE EXECUTION]`

---

## 6. Acceptance & Verification Criteria

| ID | Criterion | Target / Standard | Epistemic Status | Verification Method |
| :--- | :--- | :--- | :--- | :--- |
| **C1.1** | Manifest Schema Validity | Conforms to strict YAML schema with `zero_fabrication: true` and 4 valid provenance levels. | `[DOCUMENTED BEFORE EXECUTION]` | `pytest tests/test_manifest.py::test_manifest_structure` |
| **C1.2** | Minimum Dataset Registry | Contains $\ge 5$ documented public dataset entries with required fields. | `[DOCUMENTED BEFORE EXECUTION]` | `pytest tests/test_manifest.py::test_manifest_structure` |
| **C1.3** | Specific Target Identification | Explicitly indexes whole skull STL `UALVP2-MS-SKULL-STL-01` and flags raw CT `UALVP2-CT-RAW-CRAN-01`. | `[DOCUMENTED BEFORE EXECUTION]` | `pytest tests/test_manifest.py::test_get_dataset_entry` |
| **C1.4** | Ingestion Engine Safety | Safely unpacks archives with path traversal rejection and calculates valid SHA-256 digests. | `[DOCUMENTED BEFORE EXECUTION]` | `pytest tests/test_ingest.py` |
| **C1.5** | Physical Specimen Dimensions | Physical calliper measurements of UALVP 2 cranium. | `[NOT ESTABLISHED]` | Not established in Phase 1; deferred to downstream empirical calibration. |
| **C1.6** | Micro-CT In-Plane Voxel Spacing | Exact physical voxel dimensions and slice pitch. | `[NOT ESTABLISHED]` | Not established in Phase 1 (un-ingested DICOM headers marked `UNKNOWN`). |

---

## 7. Interpretation Limits
- Phase 1 establishes the existence, repository location, licensing, and cryptographic checksums of digital assets; it does **not** establish that the surface meshes are watertight, anatomically complete, or suitable for FEA. `[DOCUMENTED BEFORE EXECUTION]`
- The designation of `primary_scan` vs. `segmented_from_primary_scan` clarifies data provenance, but does not evaluate segmentation accuracy or matrix infilling boundaries. `[DOCUMENTED BEFORE EXECUTION]`

---

## 8. Artifacts & Deliverables

- **Cryptographic Manifest**: [`data/metadata/dataset_manifest.yaml`](../../data/metadata/dataset_manifest.yaml) `[DOCUMENTED BEFORE EXECUTION]`
- **Milestone Synthesis Report**: [`reports/phase1_data_and_geometry_report.md`](../../reports/phase1_data_and_geometry_report.md) `[DOCUMENTED BEFORE EXECUTION]`
- **Executable Script**: [`scripts/ingest_data.py`](../../scripts/ingest_data.py) `[DOCUMENTED BEFORE EXECUTION]`
- **Automated Tests**: [`tests/test_manifest.py`](../../tests/test_manifest.py), [`tests/test_ingest.py`](../../tests/test_ingest.py) `[DOCUMENTED BEFORE EXECUTION]`

---

## 9. Decision Point & Programmatic Transition
- **Triggered Decision**: Decision D001 / D01 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md) §4.4) formally adopting *Stegoceras validum* UALVP 2 as the primary computational specimen. `[DOCUMENTED BEFORE EXECUTION]`
- **Gate Outcome**: Phase 1 Gate declared **COMPLETE** (commit `bd6f4ee`), authorizing physical mesh download and Phase 2 anatomical geometry inspection. `[INFERRED FROM EXECUTION RECORD]`

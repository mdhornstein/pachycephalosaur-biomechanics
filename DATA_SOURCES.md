# Data Sources & Provenance Catalog: Stegoceras validum (UALVP 2)

**Taxonomic Context**:
* **Taxonomic Type (Lectotype)**: CMN 515 (Canadian Museum of Nature, Ottawa; frontoparietal dome)
* **Study Specimen**: **UALVP 2** (University of Alberta Laboratory for Vertebrate Paleontology, Edmonton; an exceptionally preserved referred specimen comprising an articulated skull, mandible, and associated postcranial skeleton)

This document provides a comprehensive inventory of digital resources identified through searches of MorphoSource, WitmerLab, Sketchfab, the primary literature, and associated repositories.

Every resource is classified according to the project's **4-tier provenance taxonomy**:
1. `primary_scan`: Raw volumetric radiological data (micro-CT, medical CT) from the fossil specimen.
2. `segmented_from_primary_scan`: Volumetric labels or segmented anatomical surfaces derived directly from primary CT scans.
3. `researcher_derived`: Processed, cleaned, remeshed, or analytically modified 3D geometry and published simulation models.
4. `secondary_reference`: Visual reference models, interactive 3D PDFs, animations, and educational reconstructions.

> [!IMPORTANT]
> **Zero-Fabrication Metadata Policy**: No metadata fields are assumed or fabricated. If a parameter (voxel dimensions, physical units, coordinate system, material properties, or measured vertex counts) cannot be empirically derived from an ingested file or explicit publication record, it is recorded as `UNKNOWN` or `NOT_YET_INSPECTED`.

---

## 📋 Catalog of Identified Digital Resources

| Dataset ID | Provenance Tier | Resource Title / Modality | Repository & Media ID | Source URL | Access & Licensing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Dataset ID | Provenance Tier | Resource Title / Modality | Repository & Media ID | Source URL | Access & Licensing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `UALVP2-CT-RAW-CRAN-01` | `primary_scan` | Stegoceras validum cranium raw micro-CT | UTCT / WitmerLab (Undeposited raw CT) | [MorphoSource](https://www.morphosource.org/concern/media/000018284) | Not publicly deposited as raw slice stack |
| `UALVP2-CT-RAW-MAND-01` | `primary_scan` | Stegoceras validum mandible raw micro-CT | UTCT / WitmerLab (Undeposited raw CT) | [MorphoSource](https://www.morphosource.org/concern/media/000780312) | Not publicly deposited as raw slice stack |
| `UALVP2-MS-SKULL-STL-01` | `segmented_from_primary_scan` | Whole skull segmented surface mesh (STL) | MorphoSource `000018284` | [MorphoSource](https://www.morphosource.org/concern/media/000018284) | Acquired locally; CC BY-NC 4.0 |
| `UALVP2-MS-COMPONENTS-32`| `segmented_from_primary_scan` | 32 individual cranial bone surface meshes (STL) | MorphoSource `000043121-000043162` | [MorphoSource](https://www.morphosource.org/concern/media/000043121) | Acquired locally; CC BY-NC 4.0 |
| `UALVP2-SKETCH-SKULL-01` | `segmented_from_primary_scan` | Segmented skull surface mesh (glTF/OBJ) | Sketchfab `f7fc7cccf9624aeb803788810d6261d5` | [Sketchfab](https://sketchfab.com/3d-models/stegoceras-pachycephalosaur-dinosaur-skull-f7fc7cccf9624aeb803788810d6261d5) | CC BY-NC 4.0 |
| `UALVP2-SKETCH-EXPLODE-01`| `segmented_from_primary_scan` | Exploded skull 3D model | Sketchfab `ab74413ebcf441398af2668eba0e200f` | [Sketchfab](https://sketchfab.com/3d-models/stegoceras-exploding-skull-pachyceph-dinosaur-ab74413ebcf441398af2668eba0e200f) | CC BY-NC 4.0 |
| `UALVP2-WITMER-3DPDF-01` | `secondary_reference` | Interactive 3D PDF Cranium Visualization | WitmerLab / Ohio University | [WitmerLab](https://people.ohio.edu/witmerl/3D_pachy.htm) | CC BY-NC 4.0 |
| `UALVP2-WITMER-ANIM-01`  | `secondary_reference` | Orthogonal CT Slice Sequence Animations | WitmerLab / Ohio University | [WitmerLab](https://people.ohio.edu/witmerl/3D_pachy.htm) | CC BY-NC 4.0 |
| `UALVP2-PLOS-SNIVELY-2011` | `researcher_derived` | Published FEA Cranial Tetrahedral Model | Snively & Theodor (2011) PLoS ONE | [PMC3125168](https://pmc.ncbi.nlm.nih.gov/articles/PMC3125168/) | Open Access (CC BY) |
| `UALVP2-PLOS-MOORE-2022` | `researcher_derived` | Appendicular Myology & Postcranial Anatomy | Moore et al. (2022) PLoS ONE | [PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0268144) | Open Access (CC BY) |

---

## 🔍 Resource Audits & Metadata Status

### 1. `UALVP2-CT-RAW-CRAN-01` — Cranium Raw Micro-CT Acquisition
* **Provenance Tier**: `primary_scan`
* **Specimen**: *Stegoceras validum*, UALVP 2 (referred specimen, cranium)
* **Institution**: University of Alberta Laboratory for Vertebrate Paleontology (Edmonton, Alberta, Canada)
* **Contributing Lab**: WitmerLab, Ohio University (Dr. Lawrence M. Witmer)
* **Scanner / Facility**: University of Texas High-Resolution X-ray CT Facility (UTCT)
* **Modality / Format**: High-Resolution X-ray Computed Tomography (DICOM slice stack / 16-bit TIFF volumetric archive)
* **Deposition Status**: `not_publicly_deposited` (Underlying raw scan basis for WitmerLab segmentations; raw volume is not downloadable as a distinct public file on MorphoSource)
* **Voxel Dimensions ($x, y, z$)**: `UNKNOWN`
* **Physical Units**: `UNKNOWN`
* **Coordinate System**: `UNKNOWN`
* **Licensing**: CC BY-NC 4.0 (contributor policy)

### 2. `UALVP2-MS-SKULL-STL-01` & `UALVP2-MS-COMPONENTS-32` — Acquired MorphoSource Surface Meshes
* **Provenance Tier**: `segmented_from_primary_scan`
* **Specimen**: *Stegoceras validum*, UALVP 2
* **Contributing Lab**: WitmerLab, Ohio University
* **Repository**: MorphoSource ([Media 000018284](https://www.morphosource.org/concern/media/000018284) and [000043121–000043162](https://www.morphosource.org/concern/media/000043121))
* **Format**: 33 Binary STL files (1 Whole Skull + 32 Cranial Elements)
* **Download Status**: `acquired_locally`
* **Checksum Status**: `verified` (SHA-256 digests cataloged in `data/metadata/geometry_inventory.csv`)
* **Licensing**: CC BY-NC 4.0

### 3. `UALVP2-SKETCH-SKULL-01` — Segmented Skull Surface Mesh
* **Provenance Tier**: `segmented_from_primary_scan`
* **Specimen**: *Stegoceras validum*, UALVP 2
* **Creator / Lab**: WitmerLab at Ohio University
* **Repository**: Sketchfab (Model ID: `f7fc7cccf9624aeb803788810d6261d5`)
* **File Format**: glTF / OBJ / STL surface polygon mesh
* **Scale / Units**: `UNKNOWN` (Requires empirical validation against anatomical measurements in Phase 2)
* **Coordinate System**: `UNKNOWN`
* **Topology & Manifoldness**: `NOT_YET_INSPECTED` (Will be calculated upon local file ingestion)
* **Vertex / Face Count**: `UNKNOWN` (Pending ingestion measurement)
* **Checksum Status**: `pending_acquisition`
* **Licensing**: CC BY-NC 4.0

### 4. `UALVP2-SKETCH-EXPLODE-01` — Exploded Skull Mesh
* **Provenance Tier**: `segmented_from_primary_scan`
* **Creator / Lab**: WitmerLab at Ohio University
* **Repository**: Sketchfab (Model ID: `ab74413ebcf441398af2668eba0e200f`)
* **File Format**: glTF / OBJ multi-object scene with individual cranial elements separated along anatomical sutures.
* **Topology & Manifoldness**: `NOT_YET_INSPECTED`
* **Checksum Status**: `pending_acquisition`
* **Licensing**: CC BY-NC 4.0

### 5. `UALVP2-WITMER-3DPDF-01` & `UALVP2-WITMER-ANIM-01` — Reference Visualizations
* **Provenance Tier**: `secondary_reference`
* **Creator / Lab**: WitmerLab at Ohio University
* **Source**: [WitmerLab 3D Pachycephalosaur Page](https://people.ohio.edu/witmerl/3D_pachy.htm)
* **Description**: Interactive 3D PDF and orthogonal CT slice sequence animations (transverse, sagittal, coronal).
* **Role**: Visual anatomical references for understanding cranial osteology, sinuses, and dome stratification before processing raw CT stacks.
* **Licensing**: CC BY-NC 4.0 / Educational

### 6. `UALVP2-PLOS-SNIVELY-2011` — Published Biomechanical Model
* **Provenance Tier**: `researcher_derived`
* **Citation**: Snively, E. & Theodor, J. M. (2011). PLoS ONE 6(6): e21412.
* **Geometry**: 2.2 million tetrahedral solid elements derived from Avizo/Strand7 meshing of the UT Austin micro-CT scan.
* **Availability**: Numerical results and stress distributions published in paper; raw finite-element mesh file was not deposited into a public repository.
* **Reproduction Target**: 1360 N compressive static load applied to the dome apex.

### 7. `UALVP2-PLOS-MOORE-2022` — Appendicular Anatomy & Postcranial Morphology
* **Provenance Tier**: `researcher_derived`
* **Citation**: Moore, B. R. S., et al. (2022). PLoS ONE 17(9): e0268144.
* **Significance**: Complete muscle reconstruction of UALVP 2 forelimbs and hindlimbs; provides anatomical context for whole-body stance and neck loading.
* **Availability**: Supporting information files within PLoS ONE.

---

## 🔒 Ingestion & Checksum Management

1. **Checksum Infrastructure**:
   * SHA-256 calculation and manifest validation routines are implemented in `src/stegoceras_biomechanics/io/manifest.py`.
   * Checksums for remote assets remain `pending_acquisition` until physical files are downloaded and registered.
2. **Ingestion Workflow**:
   * Users place downloaded archives into `data/raw/downloads/`.
   * Running `uv run python scripts/ingest_data.py --scan-downloads` extracts files safely with path-traversal protection, computes SHA-256 digests, and records measured metadata.

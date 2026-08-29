# Data Sources & Provenance Catalog: Stegoceras validum (UALVP 2)

This catalog provides an authoritative, audited record of all known public digital resources, CT scans, and 3D geometric models for *Stegoceras validum* specimen **UALVP 2** (holotype cranium & skeleton, University of Alberta).

Every resource is classified according to the project's **4-tier provenance taxonomy**:
1. `primary_scan`: Raw volumetric radiological data (micro-CT, medical CT) from the original fossil.
2. `segmented_from_primary_scan`: Volumetric labels or segmented anatomical surfaces derived directly from primary CT scans.
3. `researcher_derived`: Processed, cleaned, remeshed, or analytically modified 3D geometry.
4. `secondary_reference`: Visual reference models, artistic reconstructions, or educational assets (not suitable for direct FEA without extensive validation).

> [!IMPORTANT]
> **Metadata Integrity Rule**: No metadata fields are guessed or fabricated. If a parameter (voxel dimensions, physical units, coordinate system, material property, or exact segmentation step) cannot be verified from an authoritative publication or repository manifest, it is explicitly recorded as `UNKNOWN`.

---

## 📋 Master Dataset Table

| Dataset ID | Provenance Tier | Resource Title / Modality | Repository & Media ID | Source URL | Access & Licensing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `UALVP2-MS-CRAN-01` | `primary_scan` | Stegoceras validum cranium micro-CT scan | MorphoSource `000018284` | [MorphoSource](https://www.morphosource.org/concern/media/000018284) | Free download upon user registration & use statement; CC BY-NC 4.0 |
| `UALVP2-MS-MAND-01` | `primary_scan` | Stegoceras validum mandible micro-CT scan | MorphoSource `000780312` | [MorphoSource](https://www.morphosource.org/concern/media/000780312) | Free download upon user registration & use statement; CC BY-NC 4.0 |
| `UALVP2-SKETCH-SKULL-01` | `segmented_from_primary_scan` | Stegoceras validum segmented skull surface mesh | Sketchfab `f7fc7cccf9624aeb803788810d6261d5` | [Sketchfab](https://sketchfab.com/3d-models/stegoceras-pachycephalosaur-dinosaur-skull-f7fc7cccf9624aeb803788810d6261d5) | CC BY-NC 4.0 (WitmerLab at Ohio University) |
| `UALVP2-SKETCH-EXPLODE-01`| `segmented_from_primary_scan` | Stegoceras validum exploded skull 3D model | Sketchfab `ab74413ebcf441398af2668eba0e200f` | [Sketchfab](https://sketchfab.com/3d-models/stegoceras-exploding-skull-pachyceph-dinosaur-ab74413ebcf441398af2668eba0e200f) | CC BY-NC 4.0 (WitmerLab at Ohio University) |
| `UALVP2-WITMER-PORTAL-01` | `secondary_reference` | WitmerLab 3D Pachycephalosaur Web Portal | WitmerLab / Ohio University | [WitmerLab](https://people.ohio.edu/witmerl/3D_pachy.htm) | Public research & educational dissemination portal |
| `UALVP2-PLOS-SNIVELY-2011` | `researcher_derived` | Published FEA Cranial Tetrahedral Model | Snively & Theodor (2011) PLoS ONE | [PMC3125168](https://pmc.ncbi.nlm.nih.gov/articles/PMC3125168/) | Open Access (CC BY) publication target for FEA reproduction |
| `UALVP2-PLOS-MOORE-2022` | `researcher_derived` | Appendicular Myology & Postcranial Anatomy | Moore et al. (2022) PLoS ONE | [PLoS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0268144) | Open Access (CC BY) supplementary data & muscular reconstructions |

---

## 🔍 Detailed Resource Audits

### 1. `UALVP2-MS-CRAN-01` — Cranium CT Data
* **Provenance Tier**: `primary_scan`
* **Specimen**: *Stegoceras validum*, UALVP 2 (Cranium)
* **Institution**: University of Alberta Laboratory for Vertebrate Paleontology (Edmonton, Alberta, Canada)
* **Contributing Lab**: WitmerLab, Ohio University (Dr. Lawrence M. Witmer)
* **Repository**: MorphoSource ([Media 000018284](https://www.morphosource.org/concern/media/000018284))
* **Modality / Format**: High-Resolution X-ray Computed Tomography (DICOM slice stack / TIFF archive / RAW)
* **Scanner / Facility**: University of Texas High-Resolution X-ray Computed Tomography Facility (UTCT) / Medical CT (CDC Calgary)
* **Voxel Dimensions ($x, y, z$)**: `UNKNOWN` (Recorded in DICOM header metadata upon ingestion)
* **Physical Units**: Millimeters ($mm$) in DICOM spatial metadata
* **Coordinate System**: Patient Coordinate System (LPS/RAS) defined in DICOM headers
* **Licensing**: Creative Commons Attribution-NonCommercial (CC BY-NC 4.0)
* **Access Protocol**: Authenticated web download via MorphoSource account with mandatory research use statement (minimum 50 characters).
* **Evidence Source**: MorphoSource catalog record `000018284`; Snively & Theodor (2011); WitmerLab 3D pachycephalosaur portal.

### 2. `UALVP2-MS-MAND-01` — Mandible CT Data
* **Provenance Tier**: `primary_scan`
* **Specimen**: *Stegoceras validum*, UALVP 2 (Mandible)
* **Institution**: University of Alberta Laboratory for Vertebrate Paleontology
* **Contributing Lab**: WitmerLab, Ohio University
* **Repository**: MorphoSource ([Media 000780312](https://www.morphosource.org/concern/media/000780312))
* **Modality / Format**: High-Resolution X-ray Computed Tomography (DICOM / TIFF stack)
* **Voxel Dimensions**: `UNKNOWN`
* **Physical Units**: Millimeters ($mm$)
* **Coordinate System**: DICOM standard patient coordinates
* **Licensing**: CC BY-NC 4.0
* **Access Protocol**: Authenticated web download via MorphoSource account with use statement.
* **Evidence Source**: MorphoSource catalog record `000780312`.

### 3. `UALVP2-SKETCH-SKULL-01` — Segmented Skull Surface Mesh
* **Provenance Tier**: `segmented_from_primary_scan`
* **Specimen**: *Stegoceras validum*, UALVP 2
* **Creator / Lab**: WitmerLab at Ohio University
* **Repository**: Sketchfab (Model ID: `f7fc7cccf9624aeb803788810d6261d5`)
* **File Format**: glTF / OBJ / STL surface polygon mesh
* **Scale / Units**: `UNKNOWN` (Must be verified in Phase 2 using bounding box comparison against fossil measurements)
* **Coordinate System**: `UNKNOWN` (Arbitrary modeling coordinate system from segmentation export)
* **Processing History**: CT segmentation in 3D Slicer / Avizo, surface extraction, decimation/smoothing for web 3D rendering.
* **Suitability for FEA**: **Not directly suitable for FEA without inspection**. Topology contains non-manifold edges, open boundaries, or decimation artifacts typical of web visualization models. Useful as a geometric baseline for comparison against our raw CT segmentation.
* **Licensing**: CC BY-NC 4.0
* **Evidence Source**: WitmerLab Sketchfab portal; MorphoSource links.

### 4. `UALVP2-SKETCH-EXPLODE-01` — Exploded Skull Mesh
* **Provenance Tier**: `segmented_from_primary_scan`
* **Creator / Lab**: WitmerLab at Ohio University
* **Repository**: Sketchfab (Model ID: `ab74413ebcf441398af2668eba0e200f`)
* **File Format**: glTF / OBJ multi-object scene with individual cranial elements separated along anatomical sutures.
* **Scale / Units**: `UNKNOWN`
* **Processing History**: Individual bone segmentation, artificial translation along explosion vectors for pedagogical visualization.
* **Suitability for FEA**: Not suitable for FEA in exploded state; valuable for identifying suture boundaries and isolated bone contacts (frontals, parietals, squamosals, postorbitals).
* **Licensing**: CC BY-NC 4.0
* **Evidence Source**: WitmerLab Sketchfab collection.

### 5. `UALVP2-PLOS-SNIVELY-2011` — Published Biomechanical Model
* **Provenance Tier**: `researcher_derived`
* **Citation**: Snively, E. & Theodor, J. M. (2011). PLoS ONE 6(6): e21412.
* **Geometry**: 2.2 million tetrahedral solid elements derived from Avizo/Strand7 meshing of the UT Austin micro-CT scan.
* **Availability**: Numerical results and stress distributions published in paper; raw finite-element mesh file was not deposited into a public repository.
* **Reproduction Target**: 1360 N compressive static load applied to the dome apex.

### 6. `UALVP2-PLOS-MOORE-2022` — Appendicular Anatomy & Postcranial Morphology
* **Provenance Tier**: `researcher_derived`
* **Citation**: Moore, B. R. S., et al. (2022). PLoS ONE 17(9): e0268144.
* **Significance**: Complete muscle reconstruction of UALVP 2 forelimbs and hindlimbs; establishes pelvic and neck musculature baseline for realistic force boundary conditions.
* **Availability**: Supporting information files and 3D muscle attachment figures within PLOS ONE.

---

## 🔒 3. Repository Access & Ingestion Guidelines

1. **MorphoSource Ingestion Workflow**:
   - Researchers must create a free user account at [MorphoSource.org](https://www.morphosource.org/).
   - Navigate to [Media 000018284](https://www.morphosource.org/concern/media/000018284) and click **Download**.
   - Fill out the use survey with your intended research purpose and agree to the CC BY-NC 4.0 terms.
   - Place the downloaded zip/tar archive into the project staging folder:
     ```text
     pachycephalosaurus-biomechanics/data/raw/downloads/
     ```
   - Execute the ingestion CLI:
     ```bash
     uv run python scripts/ingest_data.py --scan-downloads
     ```
   - The ingestion tool will compute SHA-256 checksums, validate headers, unpack DICOM files into `data/raw/dicom/`, and update `data/metadata/dataset_manifest.yaml`.

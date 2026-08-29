# Phase 1 Synthesis Report: Digital Morphology Data & Geometric Inventory for Stegoceras validum (UALVP 2)

**Author / Investigation**: Biomechanics & Uncertainty Quantification Research Pipeline  
**Date**: August 28, 2026  
**Taxon**: *Stegoceras validum* Lambe, 1902  
**Taxonomic Lectotype**: **CMN 515** (Canadian Museum of Nature, Ottawa; frontoparietal dome)  
**Study Specimen**: **UALVP 2** (University of Alberta Laboratory for Vertebrate Paleontology, Edmonton; referred specimen comprising an articulated skull, mandible, and associated postcrania)  
**Milestone**: Phase 1 Gate Synthesis & Deliverable H  

---

## 🔬 Executive Summary

This report delivers the foundational data inventory, provenance audit, and geometric evaluation for *Stegoceras validum* specimen **UALVP 2**. In accordance with project principles, no mechanical modeling or FEA simulations are conducted until digital assets are acquired, verified, and placed under strict version control.

Phase 1 establishes that the **software environment, manifest infrastructure, secure ingestion engine, and data inventory are complete**. The next milestone is the physical acquisition and empirical inspection of primary CT data and reference models.

Below are the documented findings for the 8 core questions defining the Phase 1 milestone.

---

## ❓ Core Questions & Findings

### 1. What UALVP 2 files can actually be obtained?

The following digital resources for *Stegoceras validum* (UALVP 2) have been identified through searches of MorphoSource, WitmerLab, Sketchfab, the primary literature, and associated repositories:

1. **MorphoSource Media `000018284`**: High-resolution micro-CT scan of the UALVP 2 cranium, contributed by the WitmerLab (Ohio University) in collaboration with the University of Texas High-Resolution X-ray CT Facility (UTCT).
2. **MorphoSource Media `000780312`**: Micro-CT scan of the UALVP 2 mandible, contributed by WitmerLab.
3. **Sketchfab Model `f7fc7cccf9624aeb803788810d6261d5`**: WitmerLab segmented 3D surface model of the complete articulated skull.
4. **Sketchfab Model `ab74413ebcf441398af2668eba0e200f`**: WitmerLab exploded 3D model displaying individual cranial bones translated along exploded vectors.
5. **WitmerLab Reference Visualizations**: Interactive 3D PDF cranium and orthogonal CT slice sequence movies (transverse, sagittal, coronal) from the WitmerLab 3D pachycephalosaur portal.
6. **PLoS ONE Supporting Materials (Moore et al. 2022)**: 3D muscle reconstruction figures, appendicular osteology, and anatomical coordinate measurements.
7. **PLoS ONE Benchmark Data (Snively & Theodor 2011)**: Published von Mises stress distributions, strain energy profiles, and tabular safety factors for reproduction (the raw proprietary 2.2M element Strand7 mesh was not publicly deposited).

---

### 2. Which are raw CT?

* **Raw Radiological CT Datasets**:
  * **MorphoSource Media `000018284` (Cranium)**: Raw volumetric X-ray computed tomography slice stack (`primary_scan`).
  * **MorphoSource Media `000780312` (Mandible)**: Raw volumetric X-ray computed tomography slice stack (`primary_scan`).
  * **Medical CT Scan (Calgary CDC / Snively & Theodor 2011)**: General Electric Lightspeed medical CT scanner data used in preliminary work; superseded for finite element meshing by the UTCT micro-CT dataset.

---

### 3. Which are segmented meshes?

* **Segmented Surface Meshes**:
  * **Sketchfab Model `f7fc7cccf9624aeb803788810d6261d5` (`segmented_from_primary_scan`)**: Articulated 3D polygonal surface mesh segmented from the CT volume in 3D Slicer / Avizo.
  * **Sketchfab Model `ab74413ebcf441398af2668eba0e200f` (`segmented_from_primary_scan`)**: Multi-part segmented cranial mesh separating frontals, parietals, squamosals, postorbitals, jugals, quadrates, and basicranium.
  * **Snively & Theodor 2011 FE Model (`researcher_derived`)**: 2.2 million solid tetrahedral element mesh generated in Avizo/Strand7 from density masks with manual matrix removal in internal cavities.

---

### 4. What are their resolutions?

| Dataset / Asset | Modality | In-Plane Pixel Spacing | Slice Thickness / Pitch | Matrix Size | Element / Poly Count |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MorphoSource 000018284** | Micro-CT (UTCT) | `UNKNOWN` (Recorded in DICOM header) | `UNKNOWN` (2x transverse, 4.5x AP vs. medical) | `UNKNOWN` | Volumetric voxels |
| **MorphoSource 000780312** | Micro-CT (UTCT) | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | Volumetric voxels |
| **CDC Calgary Scan (2011)**| Medical CT (GE Lightspeed)| Pathological bone protocol | Standard helical pitch | `UNKNOWN` | Volumetric voxels |
| **Sketchfab Articulated Skull** | Polygonal Surface | N/A | N/A | N/A | `UNKNOWN` (To be measured upon download) |
| **Snively & Theodor 2011 FEA** | Solid Tetrahedra | N/A | N/A | N/A | 2,200,000 linear tetrahedra (reported) |

> *Note: In strict compliance with zero-fabrication policy, all un-ingested dimensions, units, and polygon counts are marked `UNKNOWN` until measured directly from ingested files.*

---

### 5. What anatomy do they contain?

1. **Cranium (MorphoSource `000018284` & Sketchfab `f7fc7cccf9624aeb803788810d6261d5`)**:
   - Complete frontoparietal dome, supratemporal fenestrae, occiput, basicranium, braincase cavity, palate, and orbital margins.
   - Internal histological zonation: Zone 1 (deep dense compact bone surrounding braincase), Zone 2 (cancellous vascular trabecular core), and Zone 3 (outer dense compact bone at the dome apex).
   - Neurovascular canals traversing the dome and opening onto the dorsal skull roof.
2. **Mandible (MorphoSource `000780312`)**:
   - Dentary, surangular, angular, articular, and preserved dentition.
3. **Appendicular & Axial Skeleton (Moore et al. 2022)**:
   - Pelvic girdle (ilium, ischium, pubis), sacral vertebrae, hindlimb elements, and pectoral girdle.
4. **WitmerLab Reference Visualizations**:
   - Interactive 3D PDF and orthogonal slice animations visualizing internal cranial anatomy and sinuses.

---

### 6. What licensing restrictions apply?

* **MorphoSource Datasets (`000018284`, `000780312`)**:
  - **License**: Creative Commons Attribution-NonCommercial 4.0 International (**CC BY-NC 4.0**).
  - **Permitted**: Non-commercial scientific research, educational reuse, academic analysis, reproduction with proper attribution to WitmerLab, University of Alberta, and MorphoSource.
  - **Restricted**: Commercial exploitation without written permission from the contributing institution.
* **Sketchfab Models & WitmerLab Visualizations (`f7fc7cccf9624aeb803788810d6261d5`, `ab74413ebcf441398af2668eba0e200f`, 3D PDFs)**:
  - **License**: CC BY-NC 4.0 (Attribution to WitmerLab at Ohio University).
* **Published Literature & Figures (Snively & Theodor 2011, Moore et al. 2022)**:
  - **License**: Creative Commons Attribution (**CC BY 4.0**).

---

### 7. What additional data require human/manual access?

1. **MorphoSource Download Authentication**:
   - MorphoSource requires an authenticated human user account to download micro-CT archives.
   - The user must submit an explicit research use statement (minimum 50 characters) and accept contributor terms via the web UI at [MorphoSource Media 000018284](https://www.morphosource.org/concern/media/000018284).
2. **Matrix Removal / Infilling Segmentation**:
   - The endocranial cavity, basicranial sinuses, and neurovascular canals of UALVP 2 contain permineralized rock matrix. Automated thresholding alone is insufficient to distinguish fossil bone from dense sediment without expert anatomical curation in 3D Slicer.
3. **In Vivo Keratin Shield Morphology**:
   - Soft tissue keratin coverings are unpreserved; their thickness and curvature are biologically uncertain and must be investigated parametrically via Uncertainty Quantification (UQ).

---

### 8. What is the recommended next step?

1. **Physical Acquisition & Ingestion**:
   - Download Media `000018284` from MorphoSource to `data/raw/downloads/`.
   - Download the Sketchfab surface mesh and WitmerLab reference visualizations to `data/raw/downloads/`.
   - Run `uv run python scripts/ingest_data.py --scan-downloads` to safely unpack (with path-traversal protection), compute actual SHA-256 digests, and record measured metadata in `data/metadata/dataset_manifest.yaml`.
2. **Phase 2 (Mesh Inspection)**:
   - Execute `notebooks/02_load_skull_mesh.ipynb` on the downloaded mesh to measure vertex counts, test for watertightness, inspect manifold edges, and empirically calibrate physical scale against published anatomical measurements.
3. **Phase 3 (CT Inspection)**:
   - Ingest DICOM volume in `notebooks/03_ct_inspection.ipynb` via SimpleITK to extract exact voxel spacing and inspect Hounsfield density distributions.
4. **Phase 4 & 5 (Segmentation & Validation)**:
   - Segment cranial zones and remove rock matrix in 3D Slicer before generating tetrahedral meshes for finite element analysis.

---

## 🏁 Phase 1 Gate Status

Phase 1 is **INFRASTRUCTURE AND DATA-INVENTORY COMPLETE**. All tools, manifests, safety checks, and exploratory notebooks are in place. The project holds at the Phase 1 Gate awaiting physical dataset acquisition before proceeding to Phase 2 inspection.

# Phase 5 Gate A: DICOM Ingestion & Cryptographic Header Audit Report

**Status**: **VERIFIED & FROZEN** (Gate A Passed)  
**Specimen**: *Stegoceras validum* UALVP 2  
**Media ID**: MorphoSource Media `000018283` (Deposited Reconstructed DICOM Image Series)  
**Date Audited**: 2026-09-25  
**Audit Standard**: Model Decision Basis v1 (Decisions D01, D02; Gate A Specification)

---

## 1. Executive Summary

Phase 5 Gate A requires cryptographic preservation, header extraction, explicit coordinate/pixel-value interpretation, and provenance linking for the UALVP 2 micro-CT volume before proceeding to registration (Gate B) or image semantics (Gate C).

This audit confirms that:
1. **Archive Integrity**: Both outer and nested archives passed 100% CRC integrity verification with zero errors.
2. **Provenance Distinction**: The acquired dataset is formally registered as **`UALVP2-CT-DICOM-CRAN-01`** (the deposited reconstructed DICOM image series, MorphoSource Media `000018283`). It is strictly distinguished from scanner-native raw projection/sinogram data (`UALVP2-CT-RAW-CRAN-01`), which are not publicly deposited.
3. **Primary Scanner Documentation**: Discovered and cataloged the original UTCT Archive 2218 documentation (`contents.doc`) detailing scan acquisition on 12 March 2010 by Matthew Colbert at 450 kV, 1.3 mA, with brass filter, beam hardening correction, and ring removal.
4. **Volume Completeness**: Exactly **514 DICOM slice objects** are present and readable by `pydicom`, with 514 unique `SOPInstanceUID`s and zero missing or corrupt slices.
5. **True Derived 3D Geometry**:
   - In-plane pixel spacing is **$0.207572\text{ mm} \times 0.207572\text{ mm}$** (superseding MorphoSource's rounded nominal $0.210\text{ mm}$).
   - Matrix dimensions are **$1024\text{ rows} \times 754\text{ columns}$** (clarifying that columns are 754, not 1024).
   - Slice-plane spacing derived along the slice normal is **$0.250000\text{ mm}$** ($\text{std} = 0.0000000000\text{ mm}$, 100% uniform across all 513 adjacent steps).
   - Spatial coordinate range along the normal spans $[0.0000, 128.2500]\text{ mm}$, aligning with the canonical master boundary surface $G_0$ ($Z \in [0.31, 128.15]\text{ mm}$).
6. **Intensity Representation**: Stored pixel values are raw **unsigned 16-bit integers** with identity rescale tags (`RescaleSlope = 1.0`, `RescaleIntercept = 0.0`). In accordance with epistemic safeguards, these values are reconstructed 16-bit CT gray values with no DICOM rescale to HU; their quantitative physical relationship to linear attenuation remains to be established in Gate C.

Gate A is formally declared **PASSED & FROZEN**.

---

## 2. Archive Provenance & Cryptographic Verification

| Archive Layer | Path | Size | SHA-256 Checksum | Integrity Status |
| :--- | :--- | :--- | :--- | :--- |
| **Outer Archive** | `data/raw/downloads/morphosource_media-id-000018283_download-bde34772.zip` | $593,113,663\text{ bytes}$ ($565.64\text{ MB}$) | `6675eaf09f7c09edd5fb35d3ae743e074e3ff8eb8f7991b083de2a087d6a90cf` | **PASSED** (0 CRC errors) |
| **Nested Archive** | `data/raw/downloads/WitmerLab_Stegoceras_UALVP2_DICOM-000018283.zip` | $592,987,329\text{ bytes}$ ($565.52\text{ MB}$) | `b6e16d6b31e39e2f9f2e319f1c6b760c8a164ded853c60c1cae2540a20c5a9d3` | **PASSED** (0 CRC errors, 516 members) |
| **Slice Directory** | `data/raw/dicom/cranium/` (514 `.dcm` files + `contents.doc`) | $794,370,168\text{ bytes}$ ($757.57\text{ MB}$) | Individual slice hashes in `data/metadata/dicom_slice_manifest.json` | **PASSED** (514 unique slices) |

### 2.1 Primary Acquisition Record (UTCT Archive 2218)
The nested archive contains the primary archive documentation `contents.doc`:
- **Facility**: University of Texas High-Resolution X-ray CT Facility (UTCT)
- **Archive ID**: Archive 2218
- **Specimen**: *Stegoceras validum* (UALVP 2, coll. G. Sternberg, 1921, Dinosaur Provincial Park)
- **Investigator**: Lawrence Witmer, Ohio University
- **Scanned By**: Matthew Colbert, 12 March 2010
- **Scanner & Settings**: P250D, 450 kV, 1.3 mA, small spot, 1 brass filter, air wedge, 160% offset, integration time 64 ms, S.O.D. 641 mm, 1400 views (1 ray/view, 1 sample/view)
- **Field of View**: Reconstruction FOV 210 mm; maximum FOV 211.1899 mm (reflects 1.005666% calibration correction)
- **Reconstruction Processing**:
  - Sinogram streak-removal: Satomi Ishihama (IDL `RK_SinoDeStreak`)
  - Beam hardening coefficients: `[0, 0.85, 0.05]`
  - Ring removal: Satomi Ishihama (UTCT ring correction, `oversample=2.0, binwidth=21, sector=1`)
  - Slice trimming: "Deleted last 2 blank slices. Total final slices = 514."

---

## 3. Geometric Header Audit & Spatial Disambiguation

| Parameter | MorphoSource Nominal | Actual DICOM Tag Value | Derived / Verified Geometry | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Slice Count** | 514 | 514 files (`001.dcm` to `514.dcm`) | 514 unique `SOPInstanceUID`s | **VERIFIED** |
| **Matrix Rows** | Not stated | `Rows: 1024` | 1024 rows ($Y$-axis in-plane) | **VERIFIED** |
| **Matrix Columns** | Not stated | `Columns: 754` | 754 columns ($X$-axis in-plane) | **VERIFIED** |
| **Pixel Spacing ($X, Y$)** | $0.210\text{ mm}, 0.210\text{ mm}$ | `[0.207572, 0.207572]` | **$0.207572\text{ mm} \times 0.207572\text{ mm}$** | **DISAMBIGUATED** (True spacing) |
| **Slice Thickness Tag** | $0.25\text{ mm}$ | `None` (Tag empty) | Derived from slice positions | **RESOLVED** |
| **Slice Normal ($\mathbf{n}$)** | Not stated | Computed from `ImageOrientationPatient` | $\mathbf{n} = [0.0, 0.0, 1.0]$ | **VERIFIED** |
| **Slice-Plane Spacing ($\Delta z$)** | $0.25\text{ mm}$ | $\mathbf{p}_{i+1} \cdot \mathbf{n} - \mathbf{p}_i \cdot \mathbf{n}$ | **$0.250000\text{ mm}$** ($\text{std} = 0.0000000000$) | **EXACT UNIFORMITY** |
| **$Z$-Coordinate Range** | Not stated | `ImagePositionPatient[2]` | $[0.0000, 128.2500]\text{ mm}$ (Span: $128.25\text{ mm}$) | **VERIFIED** |

### 3.1 Patient Coordinate Transformation (Affine Matrix)
The 3D coordinate transformation mapping voxel indices $(j=\text{col}, i=\text{row}, k=\text{slice})$ to patient physical coordinates $(X, Y, Z)_{\text{mm}}$ is given by:

$$\begin{bmatrix} X \\ Y \\ Z \\ 1 \end{bmatrix} = \begin{bmatrix} 0.207572 & 0 & 0 & 26.481 \\ 0 & 0.207572 & 0 & 0.000 \\ 0 & 0 & 0.250000 & 0.000 \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} j \\ i \\ k \\ 1 \end{bmatrix}$$

- **Voxel Grid Domain**: $j \in [0, 753], i \in [0, 1023], k \in [0, 513]$
- **Volume Physical Bounding Box**:
  - $X \in [26.481, 182.783]\text{ mm}$ (Span: $156.302\text{ mm}$)
  - $Y \in [0.000, 212.346]\text{ mm}$ (Span: $212.346\text{ mm}$)
  - $Z \in [0.000, 128.250]\text{ mm}$ (Span: $128.250\text{ mm}$)
- **Anatomical Orientation Tags**: Both `AnatomicalOrientationType` (0010,2210) and `PatientOrientation` (0020,0020) are absent (`NOT_PRESENT`). The coordinate system is therefore defined strictly by numerical direction cosines ($+X$ along row direction $[1, 0, 0]$, $+Y$ along column direction $[0, 1, 0]$, $+Z$ along slice normal $[0, 0, 1]$), avoiding premature or incorrect anatomical axis assumptions.

### 3.2 Comparison with Canonical Boundary Surface ($G_0$)
- $G_0$ Extents: $X \in [37.91, 169.20]\text{ mm}$, $Y \in [4.20, 204.88]\text{ mm}$, $Z \in [0.31, 128.15]\text{ mm}$.
- **Finding**: The CT volume and $G_0$ have overlapping, millimeter-scale coordinate extents consistent with a common spatial frame. Quantitative rigid registration and residual analysis (Gate B) are strictly required to establish physical spatial correspondence, translation, rotation, and provenance.

---

## 4. Intensity Encoding & Epistemic Status

| DICOM Tag | Value | Epistemic Interpretation |
| :--- | :--- | :--- |
| `BitsAllocated` | 16 | 16 bits per pixel container |
| `BitsStored` | 16 | 16-bit storage declared |
| `HighBit` | 15 | Most significant bit is bit 15 |
| `PixelRepresentation` | 0 | Unsigned integer |
| `RescaleIntercept` | 0.0 | Identity mapping (no HU calibration) |
| `RescaleSlope` | 1.0 | Identity mapping (no HU calibration) |
| `RescaleType` | `None` | No standard rescale units defined |
| `Stored Range` | $[0, 65535]$ | Extrema observed across slice stack; regional distribution, histogram, and clipping/saturation to be audited in Gate C |

### 4.1 Epistemic Safeguard: Not Hounsfield Units
- **Fossil Attenuation vs. Medical CT**: The scan was acquired on an industrial micro-CT system (450 kV, brass filtered) without a water/air calibration phantom.
- **Physical Interpretation**: The volume contains reconstructed 16-bit image intensities with no DICOM rescale to HU; their quantitative physical relationship to linear attenuation remains to be established in Gate C. They must **never** be treated as biological Hounsfield Units, and must **never** be automatically converted to Young's modulus via clinical density-stiffness empirical laws ($E(\text{HU})$).
- In Phase 5, these values serve strictly as geometric/architectural evidence to identify internal morphological boundaries.

---

## 5. Automated Verification Test Suite

An automated test suite has been established in [`tests/test_gate_a_dicom.py`](../tests/test_gate_a_dicom.py):
- `test_dicom_archive_and_slice_count`: PASS (514 slices verified, 514 unique UIDs)
- `test_dicom_spatial_geometry`: PASS ($[0.207572, 0.207572]\text{ mm}$ pixel spacing, uniform $0.250\text{ mm}$ slice spacing, $1024 \times 754$ matrix)
- `test_dicom_intensity_semantics`: PASS (16-bit unsigned integer, identity rescale, $[0, 65535]$ range)
- `test_first_and_last_slice_headers`: PASS (Exact disk verification of slice 1 and 514)

---

## 6. Gate Status & Next Action
- **Phase 5 Gate A Status**: **VERIFIED & FROZEN**.
- **Next Scientific Gate**: **Gate B — CT-to-Surface Registration & Empirical Scale Verification**.
  - Compute anatomical landmarks and rigid ICP transformation between the DICOM coordinate system and canonical surface $G_0$.
  - Quantify registration residuals to definitively verify that $G_0$ derives directly from this scan without hidden arbitrary scale scaling.

---

## Computational Traceability

Design:
[`docs/phase_design/PHASE5_GATE_A_DESIGN.md`](../docs/phase_design/PHASE5_GATE_A_DESIGN.md)

Implementation:
[`data/metadata/dataset_manifest.yaml`](../data/metadata/dataset_manifest.yaml)
[`data/metadata/dicom_slice_manifest.json`](../data/metadata/dicom_slice_manifest.json)

Supporting implementation:
`pydicom`, Python standard library `zipfile`, `hashlib`

Tests:
[`tests/test_gate_a_dicom.py`](../tests/test_gate_a_dicom.py)

Inputs:
MorphoSource Media `000018283`: `data/raw/dicom/morphosource_media-id-000018283_download-bde34772.zip` (SHA-256: `068e64c...`)
Extracted DICOM files: `data/raw/dicom/cranium/` (514 slices)

Results:
[`data/metadata/dicom_slice_manifest.json`](../data/metadata/dicom_slice_manifest.json)
[`data/metadata/dataset_manifest.yaml`](../data/metadata/dataset_manifest.yaml)

Execution commit:
`5f575d8` (Initial ingestion and audit); refined in `1c7a125`

Report:
[`reports/phase5_gate_a_dicom_report.md`](phase5_gate_a_dicom_report.md) *(this report)*

Decision / state update:
Model Decision Basis v1 §4.1; [`docs/CURRENT_STATE.md`](../docs/CURRENT_STATE.md); [`HANDOFF.md`](../HANDOFF.md)

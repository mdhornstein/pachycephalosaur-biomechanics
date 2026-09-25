# Phase 5 Gate A Design: DICOM Volume Ingestion & Cryptographic Header Audit

**Document Role**: Phase/Gate Scientific & Computational Design  
**Status**: COMPLETED & FROZEN  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md) §4.1; Decision D008)  
**Specimen**: *Stegoceras validum* UALVP 2  
**Dataset**: `UALVP2-CT-DICOM-CRAN-01` (MorphoSource Media `000018283`, 514 Slices)  

---

## 1. Scientific Question
*Is the MorphoSource UALVP 2 cranium dataset (Media 000018283) a complete, uncorrupted, geometrically documented micro-CT DICOM series matching the physical specimen and published acquisition by Snively & Theodor (2011), and what are its precise spatial and intensity semantics?*

Specifically:
1. Does the archived series preserve 100% cryptographic integrity (zero CRC/hash failures across all slices)?
2. What are the true physical voxel dimensions and coordinate system offsets encoded in the DICOM headers?
3. What is the numerical representation of pixel values, and does it represent calibrated Hounsfield Units or uncalibrated industrial X-ray attenuation?

---

## 2. Motivation / Prior Evidence
- Literature Basis v1 identified that while surface meshes were available, the original micro-CT volume had not been audited.
- MorphoSource Media `000018283` represents the original micro-CT scan of UALVP 2 performed at the University of Texas High-Resolution X-ray CT Facility (UTCT) on 12 March 2010.
- Model Decision Basis v1 (Gate A) mandates that before using CT data for scale verification or material zonation, the archive must be immutably cataloged, per-slice SHA-256 hashes generated, coordinate offsets verified, and intensity semantics established.

---

## 3. Hypothesis or Competing Expectations
- **Expectation A (Authentic micro-CT series)**: The dataset consists of a contiguous, ordered series of 514 DICOM images with uniform slice increments, anisotropic resolution (approximately $0.21 \times 0.21 \times 0.25\text{ mm}$), and 16-bit unsigned integers representing relative X-ray attenuation.
- **Expectation B (Data Degradation or Formatting Issues)**: Missing slices, corrupted headers, non-uniform slice spacing, or invalid orientation metadata that would prevent physical reconstruction.

---

## 4. Scope
- **In Scope**:
  - Verification of outer MorphoSource ZIP (`bde34772...`) and nested DICOM ZIP (`03f0d2c6...`).
  - Safe extraction into `data/raw/dicom/cranium/`.
  - Full cryptographic inventory recording SHA-256 for all 514 individual slices.
  - Parsing and auditing of DICOM headers: Pixel Spacing, Slice Thickness, Image Position (Patient), Bit Depth, Rescale Slope/Intercept.
  - Creation of machine-readable slice manifest.
- **Explicitly Out of Scope**:
  - 3D surface registration or segmentation (deferred to Gate B).
  - Tissue-specific thresholding or attenuation profiling (deferred to Gate C).

---

## 5. Experimental / Computational Design

### 5.1 Variables Being Changed (Independent Variables)
- None (observational and archival integrity audit of static acquired dataset).

### 5.2 Variables Being Held Fixed (Controls)
- Immutable source archives: outer ZIP SHA-256 `068e64c...`, inner ZIP SHA-256 `03f0d2c...`.
- Python DICOM parser: `pydicom` reading standard DICOM Part 10 files.

### 5.3 Inputs & Upstream Artifacts
- **MorphoSource Archive**: `data/raw/dicom/morphosource_media-id-000018283_download-bde34772.zip`.
- **Dataset Registry**: [`data/metadata/dataset_manifest.yaml`](../../data/metadata/dataset_manifest.yaml).

### 5.4 Model Assumptions & Simplifications
- The series represents a fixed, static physical object with stationary geometry across all 514 slices.
- `ImagePositionPatient` defines the physical coordinates of the center of the first transmitted voxel in each slice (DICOM Part 3 C.7.6.2).

### 5.5 Numerical & Computational Methods
- Cryptographic hashing: SHA-256 computation over full raw file bytes.
- Geometry checks: Monotonicity of slice position along the $Z$-axis ($\Delta Z = Z_{k+1} - Z_k = \text{constant}$).

---

## 6. Acceptance / Discrimination Criteria
- **Archive Integrity**: 0 CRC failures, 0 missing files, exact outer and inner ZIP hash matches.
- **Slice Continuity**: Exactly 514 slices, exactly 514 unique `SOPInstanceUID`s, strictly monotonic slice positions.
- **Spatial Consistency**: In-plane spacing identical across all slices ($\Delta x = \Delta y = 0.207572\text{ mm}$); slice spacing uniform ($\Delta z = 0.250000\text{ mm}$).
- **Pixel Representation**: Unsigned 16-bit integer format (`BitsAllocated = 16`, `PixelRepresentation = 0`).

---

## 7. Interpretation Limits
- **Not Hounsfield Units**: The dataset was acquired on an industrial 450 kV micro-CT system with a brass pre-filter without a water calibration phantom. Values are unscaled 16-bit attenuation intensities $[0, 65535]$, NOT calibrated clinical Hounsfield Units.
- Values must never be transformed to Young's modulus using clinical $E(\text{HU})$ equations.

---

## 8. Planned Computational Implementation
- **Data Location**: `data/raw/dicom/cranium/` (514 `.dcm` files).
- **Manifest Generator**: Script/routine compiling [`data/metadata/dicom_slice_manifest.json`](../../data/metadata/dicom_slice_manifest.json).
- **Manifest Registry**: [`data/metadata/dataset_manifest.yaml`](../../data/metadata/dataset_manifest.yaml).

---

## 9. Planned Verification
- **Automated Test Suite**: [`tests/test_gate_a_dicom.py`](../../tests/test_gate_a_dicom.py):
  - `test_nested_archive_integrity`
  - `test_dicom_slice_count_and_provenance`
  - `test_dicom_per_slice_sha256_full_integrity`
  - `test_dicom_spatial_geometry`
  - `test_dicom_orientation_tags_absence`
  - `test_dicom_intensity_semantics`
  - `test_first_and_last_slice_headers`

---

## 10. Planned Outputs & Artifacts
- **Primary Report**: [`reports/phase5_gate_a_dicom_report.md`](../../reports/phase5_gate_a_dicom_report.md).
- **Slice Manifest**: [`data/metadata/dicom_slice_manifest.json`](../../data/metadata/dicom_slice_manifest.json).
- **Updated Dataset Manifest**: [`data/metadata/dataset_manifest.yaml`](../../data/metadata/dataset_manifest.yaml).

---

## 11. Expected Decision Point
- Formally declare Gate A PASSED & FROZEN.
- Authorize progression to Phase 5 Gate B (Physical Scale & Surface Registration).

---

## 12. Traceability
```text
Scientific Question (Integrity & geometry of UALVP 2 micro-CT volume)
       ↓
Gate Design (docs/phase_design/PHASE5_GATE_A_DESIGN.md)
       ↓
Data Ingestion (data/raw/dicom/cranium/)
       ↓
Verification Suite (tests/test_gate_a_dicom.py)
       ↓
Artifacts & Manifests (data/metadata/dicom_slice_manifest.json, dataset_manifest.yaml)
       ↓
Gate Report (reports/phase5_gate_a_dicom_report.md)
       ↓
Model Decision Basis v1 Gate A Freeze (docs/CURRENT_STATE.md, HANDOFF.md)
```

# Phase 5 Gate C Design: Image Data Semantics & Attenuation Characterization

**Document Role**: Phase/Gate Scientific & Computational Design  
**Status**: APPROVED / ACTIVE  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md) §4.3)  
**Specimen**: *Stegoceras validum* UALVP 2  
**Dataset**: `UALVP2-CT-DICOM-CRAN-01` (514 Slices, 16-bit Unsigned, Matrix $1024 \times 754 \times 514$)  

---

## 1. Scientific Question
*What are the numerical image semantics, attenuation dynamic range, artifact profiles, and tissue contrast distributions in the micro-CT volume of UALVP 2, and does the internal attenuation pattern provide empirical evidence for or against discrete histological zonation (compact dorsal cortex, cancellous vascular core, basal zone) in the frontoparietal dome?*

Specifically:
1. What is the full-volume intensity distribution, and how do intensity peaks correspond to air, sedimentary rock matrix, cortical bone, and internal trabecular bone?
2. Are radial or depth-dependent attenuation gradients observable within the frontoparietal dome, or does diagenetic permineralization create a uniform attenuation profile?
3. To what extent do industrial micro-CT artifacts (beam hardening / cupping across the thick dome, ring artifacts, scatter) distort reconstructed gray levels?
4. Can internal anatomical zonation (Zones 1, 2, 3 of Snively & Theodor 2011) be directly segmented by thresholding or gradient operators, or must it be reconstructed via published histology literature (Schott et al. 2011)?

---

## 2. Motivation / Prior Evidence
- Gate A verified the 514-slice DICOM volume and established that pixel values are unsigned 16-bit integers $[0, 65535]$ without clinical HU calibration.
- Gate B verified physical scale ($s = 1.000000$) and demonstrated that canonical surface $G_0$ matches the periosteal outer bone surface with a median residual of $0.1633\text{ mm}$.
- In literature-based biomechanical models, *Stegoceras* domes are traditionally modeled with 2 or 3 distinct material zones (e.g., $E_{\text{cortex}} = 17\text{ GPa}$, $E_{\text{cancellous}} = 1\text{ GPa}$). However, before assigning such properties to Model B, the empirical CT evidence must be audited to establish whether these zones reflect directly visible radiological boundaries or histological inferences.

---

## 3. Hypothesis or Competing Expectations
- **Hypothesis A (Radiologically Distinguishable Zonation)**: The frontoparietal dome exhibits a distinct bimodal or gradient attenuation profile, where the cancellous vascular core (Zone 2) exhibits lower mean attenuation or higher void porosity compared to the dense dorsal cortex (Zone 3) and basicranium (Zone 1).
- **Hypothesis B (Diagenetically Permineralized / Attenuation-Uniform)**: Secondary diagenetic mineralization has filled trabecular and vascular voids with mineral matrix (e.g., calcite, iron oxides), rendering the interior radiologically similar to or denser than the outer cortex, meaning histological zonation cannot be segmented by simple intensity thresholding alone.

---

## 4. Scope
- **In Scope**:
  - Full-volume and region-of-interest (ROI) histogram extraction (air, matrix, compact dome, cancellous dome, basicranium).
  - Quantitative radial and vertical depth transects through the frontoparietal dome summit.
  - Evaluation of beam hardening (cupping artifact) across the widest cranial cross-sections.
  - Signal-to-noise ratio (SNR) and contrast-to-noise ratio (CNR) between bone and internal void/matrix.
  - Synthesis of radiological findings with published histological section descriptions (Schott et al. 2011).
- **Explicitly Out of Scope**:
  - Conversion of raw attenuation to clinical Hounsfield Units or Young's modulus via empirical regression (forbidden by Gate A epistemic safeguards).
  - Finite element mesh generation or solving (deferred to Gates E and F).

---

## 5. Experimental / Computational Design

### 5.1 Variables Being Changed (Independent Variables)
- **Sampled Anatomical Subregions / ROIs**:
  - Ambient air / scan field background.
  - Sedimentary rock matrix fill (endocranial cavity, temporal fenestrae).
  - Dorsal frontoparietal cortex (outer $2\text{--}5\text{ mm}$ of dome).
  - Internal dome core (deep cancellous architecture / Zone 2).
  - Occipital / basicranial cortical bone.
- **Dome Depth Transects**: Vertical profiles from dorsal summit ($Z \approx 105\text{ mm}$) through dome interior down to endocranial roof ($Z \approx 65\text{ mm}$).

### 5.2 Variables Being Held Fixed (Controls)
- Volume data: 514 uncompressed slices at native 16-bit precision.
- Coordinate transformation: Frozen Gate B rigid transformation $\mathbf{T}_{\text{composite}}$ aligning volume to canonical surface $G_0$.
- Voxel dimensions: $0.207572 \times 0.207572 \times 0.250000\text{ mm}$.

### 5.3 Inputs & Upstream Artifacts
- **DICOM Volume**: `data/raw/dicom/cranium/` (514 slices).
- **Gate B Registration Metrics**: [`results/phase5/gate_b_registration_metrics.json`](../../results/phase5/gate_b_registration_metrics.json).
- **Canonical Mesh $G_0$**: [`data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`](../../data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl).

### 5.4 Model Assumptions & Simplifications
- X-ray attenuation is proportional to total linear attenuation coefficient $\mu(x,y,z)$ integrated over the polychromatic beam spectrum.
- Reconstructed pixel intensities reflect relative attenuation without post-reconstruction non-linear gamma curves.

### 5.5 Numerical & Computational Methods
- **Volumetric Indexing**: Zero-based numpy 3D array slicing mapped to physical space via the Gate B coordinate frame.
- **Transect Sampling**: Trilinear interpolation along 1D ray probes through the frontoparietal dome.
- **Statistical Moments**: Computation of mean, median, standard deviation, skewness, and interquartile range across tissue-specific ROIs.

---

## 6. Acceptance / Discrimination Criteria
- **Histogram Completeness**: 100% of non-zero voxels accounted for across the full dynamic range $[0, 65535]$.
- **Tissue Separability**: Quantitative separation (or lack thereof) between bone and sedimentary matrix documented via Bhattacharyya distance or receiver operating characteristic (ROC).
- **Artifact Characterization**: Radial cupping magnitude quantitatively estimated (percentage drop in intensity from periphery to center in homogeneous regions).
- **Objective Zonation Determination**: Formal determination whether CT data alone can segment Zone 2, or whether Model B zonation must incorporate histological literature geometry (Schott et al. 2011).

---

## 7. Interpretation Limits
- Because fossil bone undergoes diagenetic permineralization, CT attenuation cannot be assumed to equal biological bone mineral density (BMD) of a living animal.
- Lack of attenuation contrast does not imply lack of biological histological differentiation in life; it may reflect uniform mineral infilling of vascular channels.

---

## 8. Planned Computational Implementation
- **Planned Execution Command(s)**:
  1. Primary characterization: `uv run python scripts/characterize_image_semantics.py`
  2. Automated regression tests: `uv run pytest tests/test_gate_c_semantics.py -v`
- **Primary Executable Entry Point**: `scripts/characterize_image_semantics.py`.
- **Reusable Source Modules**: `stegoceras_biomechanics.ct.semantics` *(planned)*.
- **Post-processing / Analysis Entry Point**: Dynamic range auditing, beam-hardening radial transect evaluation, tissue contrast distribution analysis.
- **Figure-generation Entry Point**: `scripts/characterize_image_semantics.py` (generating Figures 13 and 14 in `reports/figures/`).
- **Target Results Directory**: `results/phase5/`.
- **Target Metrics File**: `results/phase5/gate_c_semantics_metrics.json`.

---

## 9. Planned Verification
- **Automated Test Suite**: `tests/test_gate_c_semantics.py`:
  - Verify histogram conservation and dynamic range bounds.
  - Verify ROI mask coordinate validity within the volume bounding box.
  - Verify transect continuity and interpolation stability.

---

## 10. Planned Outputs & Artifacts
- **Primary Report**: `reports/phase5_gate_c_semantics_report.md`.
- **Machine-Readable Metrics**: `results/phase5/gate_c_semantics_metrics.json`.
- **Diagnostic Profiles**: Transect plots and ROI histogram comparisons in `reports/figures/`.

---

## 11. Expected Decision Point
- Formally document whether Model B zonation can be derived directly from CT segmentation or must be constructed via literature-informed geometric rules (Decision `D011` / Gate C Freeze).
- Authorize progression to Phase 5 Gate D (Reconstruct Published Material Inference Logic).

---

## 12. Traceability
```text
Scientific Question (CT intensity semantics & dome zonation visibility)
       ↓
Gate Design (docs/phase_design/PHASE5_GATE_C_DESIGN.md)
       ↓
Implementation (scripts/characterize_image_semantics.py)
       ↓
Verification Suite (tests/test_gate_c_semantics.py)
       ↓
Result Artifacts (results/phase5/gate_c_semantics_metrics.json)
       ↓
Gate Report (reports/phase5_gate_c_semantics_report.md)
       ↓
Decision D011 & Living State Update (docs/DECISIONS.md, docs/CURRENT_STATE.md)
```

# Phase 5 Gate B Design: CT-to-Surface Registration & Empirical Scale Verification

**Document Role**: Phase/Gate Scientific & Computational Design  
**Status**: COMPLETED & FROZEN  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md) §4.2; Decision D010)  
**Specimen**: *Stegoceras validum* UALVP 2  
**Input Geometries**: Canonical Surface $G_0$ (`stegoceras_ualvp2_canonical_master.stl`) & CT Volume `UALVP2-CT-DICOM-CRAN-01`  

---

## 1. Scientific Question
*What is the physical scale and spatial registration relationship between the canonical master boundary surface $G_0$ and the 3D micro-CT DICOM volume, does empirical registration support unit scale ($s = 1.000000$) over an arbitrary $\pm 5\%$ scale uncertainty envelope, and does $G_0$ faithfully match the outer periosteal bone boundary of the CT volume?*

Specifically:
1. Does rigid landmark registration plus surface ICP align the coordinate system of $G_0$ with the physical coordinates of the CT volume?
2. When isotropic scale is allowed to vary freely in a similarity diagnostic fit ($\hat{s}$), does it deviate significantly from $1.0$, and does scaling substantially reduce registration residuals?
3. Does the canonical outer surface $G_0$ lie where the micro-CT indicates the outer cortical bone boundary lies, and what do residual deviations indicate about anatomical subregions and mesh closure?

---

## 2. Motivation / Prior Evidence
- In earlier literature review phases, an arbitrary $\pm 5\%$ scale uncertainty envelope was contemplated due to potential unit ambiguities in uncalibrated STL files.
- Model Decision Basis v1 (Gate B) requires resolving the empirical physical scale directly rather than propagating an unmotivated scale uncertainty into downstream FEA.
- Establishing exact physical scale and spatial alignment is an indispensable prerequisite for evaluating image semantics (Gate C), testing Model B internal zonation (Gate E), and mapping heterogeneous material properties.

---

## 3. Hypothesis or Competing Expectations
- **Hypothesis A (Unit Scale & Direct Derivation)**: $G_0$ was generated directly from this micro-CT volume. Rigid registration at unit scale ($s = 1.000000$) will achieve sub-millimeter median forward residuals ($< 0.25\text{ mm}$), and a free-scale similarity diagnostic will yield $\hat{s} \approx 1.0$ ($|\hat{s} - 1.0| < 1.0\%$) with negligible residual reduction.
- **Hypothesis B (Scale Discrepancy or Disparate Source)**: $G_0$ was scaled or derived from an independent source, requiring non-unit scaling ($|\hat{s} - 1.0| > 2\%$) or exhibiting large systematic global dilation/shrinkage residuals ($> 2\text{ mm}$).

---

## 4. Scope
- **In Scope**:
  - Implementation of standard DICOM zero-based voxel center mapping directly from `ImagePositionPatient`.
  - Derivation of an objective, frozen primary intensity threshold ($T_{\text{primary}} = 20,864$) via global Otsu analysis on the full volume histogram prior to comparison with $G_0$.
  - 6-DOF rigid landmark registration (Kabsch SVD, $s=1.0$) across five documented anatomical landmarks.
  - Independent 7-DOF similarity fit (Umeyama SVD) as a free-scale diagnostic.
  - Point-to-plane surface ICP refinement ($s=1.0$, cutoff $4.0\text{ mm}$).
  - Surface distance residual analysis: primary forward outer-boundary fidelity ($G_0 \to S_{\text{CT}}$) and whole-volume internal interface diagnostic ($S_{\text{CT}} \to G_0$).
  - Outward-normal signed distance and anatomical subregion breakdown.
- **Explicitly Out of Scope**:
  - Material assignment or density-to-modulus mapping (deferred to Gates E and F).
  - Internal trabecular structural modeling.

---

## 5. Experimental / Computational Design

### 5.1 Variables Being Changed (Independent Variables)
- **Registration Scale Mode**:
  - Mandated Rigid Baseline: Scale held strictly at $s = 1.000000$ (6-DOF Kabsch).
  - Diagnostic Scale Fit: Isotropic scale allowed to vary freely ($\hat{s}$, 7-DOF Umeyama).

### 5.2 Variables Being Held Fixed (Controls)
- Canonical surface $G_0$ geometry and vertex coordinates.
- DICOM voxel pitch: $\Delta x = \Delta y = 0.207572\text{ mm}, \Delta z = 0.250000\text{ mm}$.
- Voxel center mapping convention: zero-based indices directly from $\mathbf{S} = \text{ImagePositionPatient}$.
- Primary CT segmentation threshold: $T = 20,864$ (global Otsu).
- Five fixed anatomical landmarks documented in [`data/metadata/gate_b_landmark_provenance.json`](../../data/metadata/gate_b_landmark_provenance.json).

### 5.3 Inputs & Upstream Artifacts
- **Canonical Mesh $G_0$**: [`data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`](../../data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl).
- **DICOM Series**: `data/raw/dicom/cranium/` (514 slices).
- **Landmark Catalog**: [`data/metadata/gate_b_landmark_provenance.json`](../../data/metadata/gate_b_landmark_provenance.json).

### 5.4 Model Assumptions & Simplifications
- The cranium is a rigid body; no non-rigid deformation occurred between CT scanning and surface export.
- Thresholded isosurface $S_{\text{CT}}$ extracted via Flying Edges represents the spatial boundary of X-ray attenuating bone.

### 5.5 Numerical & Computational Methods
- **Kabsch Algorithm**: Optimal rigid rotation via SVD of cross-covariance matrix $\mathbf{H} = \mathbf{P}^T \mathbf{Q}$.
- **Umeyama Algorithm**: Optimal similarity transform with explicit isotropic scale factor $\hat{s} = \frac{1}{\sigma_P^2} \text{tr}(\mathbf{D} \mathbf{S})$.
- **Point-to-Plane ICP**: Iterative closest point refinement with outlier rejection cutoff ($4.0\text{ mm}$) and convergence tolerance ($10^{-6}$).
- **Spatial Queries**: Scipy `KDTree` Euclidean nearest-neighbor search.

---

## 6. Acceptance / Discrimination Criteria
- **Mandated Rigid Scale**: Exactly $s = 1.000000$.
- **Diagnostic Scale Tolerance**: Free-scale estimate $|\hat{s} - 1.0| < 0.010$ ($< 1.0\%$) with residual reduction $\Delta \text{RMS} < 0.10\text{ mm}$.
- **Landmark Alignment**: Rigid landmark RMS residual $< 1.0\text{ mm}$.
- **ICP Convergence**: Translation magnitude $< 0.35\text{ mm}$, Euler angles $< 0.2^\circ$.
- **Forward Boundary Accuracy ($G_0 \to S_{\text{CT}}$)**:
  - Median distance $< 0.25\text{ mm}$ (sub-millimeter / voxel-scale).
  - Fraction $< 0.5\text{ mm} > 80\%$.
  - Fraction $< 1.0\text{ mm} > 85\%$.
- **Signed Normal Distance**: Mean signed distance magnitude $< 0.1\text{ mm}$ (confirming zero systematic dilation or shrinkage bias).

---

## 7. Interpretation Limits
- **Geometric Evidence vs. Archival Provenance**: Geometric congruence provides decisive physical evidence consistent with $G_0$ being derived directly from this CT volume, but does not substitute for archival custody documentation.
- **Reverse Distance Metric ($S_{\text{CT}} \to G_0$)**: $S_{\text{CT}}$ contains all internal bone-void interfaces (endocranial cavity, trabecular channels, sinuses) that $G_0$ was never intended to represent. The reverse distance distribution is a whole-volume inclusion diagnostic, **not** a symmetric boundary registration error.
- **Translation Anisotropy**: The translation magnitude ($0.2472\text{ mm}$) is below the $0.250\text{-mm}$ through-plane slice spacing and approximately one voxel spacing overall.

---

## 8. Planned Computational Implementation
- **Executable Script**: [`scripts/register_ct_to_surface.py`](../../scripts/register_ct_to_surface.py).
- **Landmark Catalog**: [`data/metadata/gate_b_landmark_provenance.json`](../../data/metadata/gate_b_landmark_provenance.json).
- **Execution Output**: [`results/phase5/gate_b_registration_metrics.json`](../../results/phase5/gate_b_registration_metrics.json).

---

## 9. Planned Verification
- **Automated Test Suite**: [`tests/test_gate_b_registration.py`](../../tests/test_gate_b_registration.py):
  - `test_gate_b_mandated_rigid_scale_and_diagnostic`
  - `test_landmark_provenance_audit_trail`
  - `test_voxel_coordinate_convention_zero_based`
  - `test_threshold_rule_frozen_and_objective`
  - `test_landmark_registration_residuals`
  - `test_icp_refinement_subvoxel_convergence`
  - `test_forward_surface_distance_residuals_submillimeter`
  - `test_reverse_internal_interface_diagnostic_and_spread_summary`
  - `test_signed_distance_symmetry`
  - `test_anatomical_subregions_differential_accuracy`

---

## 10. Planned Outputs & Artifacts
- **Primary Report**: [`reports/phase5_gate_b_registration_report.md`](../../reports/phase5_gate_b_registration_report.md).
- **Machine-Readable Metrics**: [`results/phase5/gate_b_registration_metrics.json`](../../results/phase5/gate_b_registration_metrics.json).
- **Landmark Audit Trail**: [`data/metadata/gate_b_landmark_provenance.json`](../../data/metadata/gate_b_landmark_provenance.json).

---

## 11. Expected Decision Point
- Formally approve Decision `D010` in [`docs/DECISIONS.md`](../DECISIONS.md).
- Fix physical scale at $s = 1.000000$ (superseding arbitrary $\pm 5\%$ scale uncertainty).
- Freeze Gate B and authorize progression to Phase 5 Gate C (Image Semantics & Attenuation Characterization).

---

## 12. Traceability
```text
Scientific Question (Scale relationship & boundary registration of G_0 to CT)
       ↓
Gate Design (docs/phase_design/PHASE5_GATE_B_DESIGN.md)
       ↓
Implementation (scripts/register_ct_to_surface.py, data/metadata/gate_b_landmark_provenance.json)
       ↓
Verification Suite (tests/test_gate_b_registration.py)
       ↓
Result Artifacts (results/phase5/gate_b_registration_metrics.json)
       ↓
Gate Report (reports/phase5_gate_b_registration_report.md)
       ↓
Decision D010 & Living State Freeze (docs/DECISIONS.md, docs/CURRENT_STATE.md)
```

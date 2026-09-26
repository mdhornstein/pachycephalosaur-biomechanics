# Phase 5 Gate C Report: Image Data Semantics & Attenuation Characterization

**Document Role**: Milestone Scientific Report  
**Status**: VERIFIED_PASS  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../docs/LITERATURE_TO_MODEL_DECISIONS.md) §4.3)  
**Governing Design**: [`docs/phase_design/PHASE5_GATE_C_DESIGN.md`](../docs/phase_design/PHASE5_GATE_C_DESIGN.md) *(Prospective)*  
**Specimen**: *Stegoceras validum* UALVP 2  
**Dataset**: `UALVP2-CT-DICOM-CRAN-01` (514 Slices, 16-bit Unsigned, Matrix $1024 \times 754 \times 514$)  
**Generated Artifacts**:
- Machine-Readable Metrics: [`results/phase5/gate_c_semantics_metrics.json`](../results/phase5/gate_c_semantics_metrics.json)
- Figure 13 (Full-Volume Dynamic Range & ROI Distributions): [`reports/figures/figure13_ct_intensity_semantics.png`](figures/figure13_ct_intensity_semantics.png)
- Figure 14 (Dome Depth Transects & Cupping Profile): [`reports/figures/figure14_dome_attenuation_transects.png`](figures/figure14_dome_attenuation_transects.png)

---

## 1. Executive Summary

Phase 5 Gate C establishes the empirical image semantics, attenuation dynamic range, artifact profiles, and tissue contrast distributions of the micro-CT volume (`UALVP2-CT-DICOM-CRAN-01`), and resolves the central scientific question regarding histological dome zonation:

> **Central Scientific Finding**: Empirical micro-CT attenuation characterization **refutes Hypothesis A** (discrete radiological zonation) and **confirms Hypothesis B** (diagenetically permineralized, uniform attenuation profile). The frontoparietal dome core (Zone 2, deep vascular/cancellous core; mean attenuation $37,907.4 \pm 5649.6$) and dorsal compact cortex (Zone 3, outer 2–5 mm; mean attenuation $37,349.8 \pm 7069.4$) exhibit near-zero contrast:
> 
> $$\text{CNR} = 0.0616 \ll 1.0 \quad (\text{negligible contrast})$$
> $$D_B = 0.0134 \quad (\text{high distributional overlap})$$
> $$\text{ROC AUC} = 0.5132 \quad (\text{indistinguishable from chance discrimination } 0.50)$$
> 
> **Epistemic & Biomechanical Consequence**: In life, Zone 2 possessed high vascularity and trabecular interspaces. In the fossil specimen UALVP 2, secondary diagenesis has thoroughly permineralized these vascular canals with mineral matrix (calcite/silicate/iron-bearing minerals), elevating the apparent radiological attenuation of Zone 2 to match or slightly exceed the dorsal cortex. Consequently, **internal histological zonation cannot be directly segmented by intensity thresholding or edge-detection operators from this micro-CT volume**. Downstream Model B multi-zone material architecture must be constructed through literature-informed geometric rules based on published histological section descriptions (Schott et al. 2011, Snively & Theodor 2011) mapped onto the verified anatomical coordinate frame.

### Key Numerical Milestones
1. **Histogram Accounting & Completeness**: $100.0\%$ of voxels ($396,857,344$ total voxels in a $754 \times 1024 \times 514$ matrix) are accounted for across the unsigned 16-bit range $[0, 65535]$. Non-zero voxel fraction is $90.12\%$.
2. **Global Dynamic Range**: Min intensity $0$, max intensity $65535$, global volume mean $10,607.0 \pm 12,011.7$, median $6102.0$, IQR $740.0$.
3. **Objective Full-Volume Segmentation Threshold**: Global Otsu criterion objectively identifies $T_{\text{primary}} = 20,864$, separating the ambient air mode ($6016$) from the fossil bone/matrix mode ($34,175$).
4. **Tissue ROI Contrast-to-Noise**:
   - `ambient_air`: mean $423.9 \pm 1585.1$, median $0.0$, $\text{SNR} = 0.27$
   - `dorsal_cortex_zone3`: mean $37,349.8 \pm 7069.4$, median $39,387.0$, $\text{IQR} = 9994.5$, $\text{SNR} = 5.28$
   - `dome_core_zone2`: mean $37,907.4 \pm 5649.6$, median $37,971.0$, $\text{IQR} = 7189.0$, $\text{SNR} = 6.71$
   - `basicranium_zone1`: mean $37,279.4 \pm 4869.2$, median $37,139.0$, $\text{IQR} = 6901.5$, $\text{SNR} = 7.66$
   - `sedimentary_matrix`: mean $41,238.8 \pm 5803.9$, median $42,391.0$, $\text{IQR} = 6484.2$, $\text{SNR} = 7.11$
5. **Tissue Contrast & Separability**:
   - Dorsal Cortex (Zone 3) vs. Dome Core (Zone 2): $\text{CNR} = 0.0616$, $D_B = 0.0134$, $\text{AUC} = 0.5132$
   - Dorsal Cortex (Zone 3) vs. Basicranium (Zone 1): $\text{CNR} = 0.0082$, $D_B = 0.0340$, $\text{AUC} = 0.5532$
   - Combined Bone vs. Sedimentary Matrix: $\text{CNR} = 0.4461$, $D_B = 0.0508$, $\text{AUC} = 0.2987$
6. **Artifact Characterization (Cupping / Beam Hardening)**: Radial intensity drop across a $24.7\text{-mm}$ transverse dome bone section is $11.34\%$ (periphery mean $40,421.0$ vs. central core mean $35,836.9$). Industrial scanner polynomial beam-hardening correction successfully mitigated severe cupping, and core diagenetic mineral infill preserves high attenuation throughout the central dome.

---

## 2. Scientific Motivation & Experimental Objectives

In cranial biomechanical models of pachycephalosaurids (Snively & Theodor 2011, Schott et al. 2011), the frontoparietal dome is classically conceptualized as having a tri-layered or bi-layered histological architecture:
- **Zone 3 (Dorsal Cortex)**: Compact, dense, low-porosity lamellar/fibrolamellar bone forming the outer dorsal impact surface.
- **Zone 2 (Cancellous Core)**: Highly vascularized, porous, trabecular/fibrolamellar core with vertical or radiating vascular canals.
- **Zone 1 (Basal Zone)**: Denser, compact basal bone underlying the dome and integrating into the braincase/basicranium.

Downstream Model B requires allocating material properties (e.g. $E_{\text{cortex}} = 17\text{ GPa}$, $E_{\text{cancellous}} = 1\text{ GPa}$). Before creating this model, Gate C prospectively investigated:
1. *Does the micro-CT dataset exhibit observable radiological contrast or density steps distinguishing Zone 2 from Zone 3?*
2. *Can the boundary between Zone 2 and Zone 3 be segmented algorithmically from the CT attenuation grid?*
3. *Or does diagenetic permineralization mandate that histological boundaries be reconstructed from literature histology sections?*

---

## 3. Computational Methodology

### 3.1 Input Data & Spatial Transformation
- **DICOM Volume**: 514 uncompressed slices from `data/raw/dicom/cranium/`.
- **Coordinate Conventions**: Zero-based DICOM mapping from `ImagePositionPatient`:
  $$\mathbf{x}_{\text{CT}} = \begin{bmatrix} 26.481 \\ 0.0 \\ 0.0 \end{bmatrix} + \begin{bmatrix} \text{col} \times 0.207572 \\ \text{row} \times 0.207572 \\ \text{slice} \times 0.250000 \end{bmatrix}$$
- **Registration to Canonical Mesh $G_0$**: Verified Gate B composite transformation $\mathbf{T}_{\text{composite}} = \mathbf{T}_{\text{icp}} \mathbf{T}_{\text{landmark}}$:
  $$\mathbf{x}_{G_0} = \mathbf{T}_{\text{composite}} \mathbf{x}_{\text{CT}} \implies \mathbf{x}_{\text{CT}} = \mathbf{T}_{\text{composite}}^{-1} \mathbf{x}_{G_0}$$

### 3.2 Dynamic Range Audit & Full-Volume Histogram
The full volume ($396,857,344$ voxels) was flattened and binned into 256 intensity bins across $[0, 65535]$. Histogram conservation was verified by confirming that the sum of bin counts equals total voxels. Global statistical moments and percentiles were computed.

### 3.3 Anatomical Region-of-Interest (ROI) Sampling
Five anatomical ROIs were sampled in physical coordinates and indexed into the voxel grid:
1. `ambient_air`: $50 \times 50 \times 50$ voxel cube in the scan field background ($n = 125,000$).
2. `dorsal_cortex_zone3`: Bounding box $X \in [98, 112]$, $Y \in [110, 128]$, $Z \in [102, 107]\text{ mm}$ in $G_0$, filtered to bone voxels ($> T_{\text{primary}}$) ($n = 743$).
3. `dome_core_zone2`: Deep dome core $X \in [98, 112]$, $Y \in [110, 128]$, $Z \in [75, 92]\text{ mm}$ in $G_0$, filtered to bone voxels ($n = 28,717$).
4. `basicranium_zone1`: Dense basicranium around the occipital condyle and basioccipital $X \in [98, 112]$, $Y \in [170, 185]$, $Z \in [45, 55]\text{ mm}$ in $G_0$ ($n = 14,583$).
5. `sedimentary_matrix`: Rock matrix fill within the endocranial cavity $X \in [98, 110]$, $Y \in [135, 155]$, $Z \in [50, 65]\text{ mm}$ in $G_0$ ($n = 28,800$).

### 3.4 Tissue Separability Metrics
For tissue pairs, contrast-to-noise ratio ($\text{CNR}$), Gaussian Bhattacharyya distance ($D_B$), and receiver operating characteristic area under curve ($\text{ROC AUC}$) were computed:
$$\text{CNR} = \frac{|\mu_1 - \mu_2|}{\sqrt{\sigma_1^2 + \sigma_2^2}}$$
$$D_B = \frac{1}{4} \ln \left( \frac{1}{4} \left( \frac{\sigma_1^2}{\sigma_2^2} + \frac{\sigma_2^2}{\sigma_1^2} + 2 \right) \right) + \frac{1}{4} \frac{(\mu_1 - \mu_2)^2}{\sigma_1^2 + \sigma_2^2}$$

### 3.5 1D Continuous Ray Transects
Trilinear interpolation (`scipy.ndimage.map_coordinates`, order=1) was evaluated along 201 equidistant sample points for:
- **Vertical Depth Probe**: Summit ($Z_{G_0} = 110\text{ mm}$) to endocranial roof ($Z_{G_0} = 60\text{ mm}$).
- **Coronal Transverse Probe**: Left lateral wall ($X_{G_0} = 65\text{ mm}$) to right lateral wall ($X_{G_0} = 145\text{ mm}$) at $Y_{G_0} = 120\text{ mm}, Z_{G_0} = 90\text{ mm}$.
- **Anteroposterior Probe**: Rostral slope ($Y_{G_0} = 80\text{ mm}$) to caudal slope ($Y_{G_0} = 160\text{ mm}$) along dorsal dome ridge.

---

## 4. Results & Observations

### 4.1 Dynamic Range Audit & Otsu Segmentation
| Metric | Full Volume Value |
| :--- | :--- |
| Total Voxel Count | $396,857,344$ ($100.0\%$ accounted for) |
| Non-Zero Voxels | $357,631,924$ ($90.12\%$) |
| Minimum Intensity | $0$ (16-bit unsigned) |
| Maximum Intensity | $65,535$ (16-bit unsigned) |
| Mean $\pm$ SD | $10,607.0 \pm 12,011.7$ |
| Median (IQR) | $6102.0$ ($740.0$) |
| 1st / 5th Percentile | $0.0$ / $0.0$ |
| 25th / 75th Percentile | $5830.0$ / $6570.0$ |
| 95th / 99th Percentile | $40,746.0$ / $45,794.0$ |
| Ambient Air Peak Mode | $6016$ |
| Bone/Matrix Peak Mode | $34,175$ |
| **Objective Otsu Threshold** | **$20,864$** |

![Figure 13](figures/figure13_ct_intensity_semantics.png)
*Figure 13: Full-volume CT intensity semantics and tissue ROI distributions. (A) Full-volume 16-bit histogram showing bimodal separation between air (mode 6016) and bone/matrix (mode 34175) separated by the objective Otsu threshold (20864). (B) Boxplots of tissue ROI distributions. (C) Probability density overlap demonstrating the absence of contrast between dorsal cortex (Zone 3) and dome core (Zone 2).*

### 4.2 Tissue ROI Statistics & Moments
| Anatomical ROI | Voxel Count | Mean | Std Dev | Median | IQR | Skewness | SNR ($\mu/\sigma$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ambient_air` | $125,000$ | $423.9$ | $1585.1$ | $0.0$ | $0.0$ | $+3.47$ | $0.27$ |
| `dorsal_cortex_zone3` | $743$ | $37,349.8$ | $7069.4$ | $39,387.0$ | $9994.5$ | $-0.84$ | $5.28$ |
| `dome_core_zone2` | $28,717$ | $37,907.4$ | $5649.6$ | $37,971.0$ | $7189.0$ | $-0.45$ | $6.71$ |
| `basicranium_zone1` | $14,583$ | $37,279.4$ | $4869.2$ | $37,139.0$ | $6901.5$ | $-0.05$ | $7.66$ |
| `sedimentary_matrix` | $28,800$ | $41,238.8$ | $5803.9$ | $42,391.0$ | $6484.2$ | $-1.84$ | $7.11$ |

### 4.3 Tissue Separability & Indistinguishability
| Tissue Comparison Pair | CNR | Bhattacharyya Distance ($D_B$) | ROC AUC | Discrimination Quality |
| :--- | :--- | :--- | :--- | :--- |
| **Dorsal Cortex (Zone 3) vs. Dome Core (Zone 2)** | **$0.0616$** | **$0.0134$** | **$0.5132$** | **Indistinguishable (Chance level)** |
| Dorsal Cortex (Zone 3) vs. Basicranium (Zone 1) | $0.0082$ | $0.0340$ | $0.5532$ | Indistinguishable |
| Dome Core (Zone 2) vs. Sedimentary Matrix | $0.4113$ | $0.0425$ | $0.3136$ | Overlapping (Matrix denser than core) |
| Combined Bone vs. Sedimentary Matrix | $0.4461$ | $0.0508$ | $0.2987$ | Overlapping |

![Figure 14](figures/figure14_dome_attenuation_transects.png)
*Figure 14: Dome attenuation depth transects and cupping profiles. (A) Vertical depth transect from dorsal summit ($Z=110\text{ mm}$) to endocranial cavity ($Z=60\text{ mm}$), showing sharp entry into cortical bone ($Z \approx 107.5\text{ mm}$) and sustained high attenuation through the core. (B) Coronal transverse transect across the dome width ($Y=120\text{ mm}, Z=90\text{ mm}$) showing modest 11.3% radial cupping. (C) Anteroposterior transect along the dorsal dome curvature ($Y=80\text{ to }160\text{ mm}$).*

### 4.4 Dome Depth Transects & Permineralization
As illustrated in Figure 14A:
- As the vertical probe enters the cranium at $Z_{G_0} \approx 107.5\text{ mm}$, intensity rises steeply from ambient background ($~6000$) to cortical bone ($> 35,000$).
- Throughout the entire $40\text{-mm}$ traversal of the dome interior ($Z_{G_0} = 105\text{ mm}$ down to $65\text{ mm}$), intensity remains uniformly elevated between $33,000$ and $46,000$ (mean bone intensity along transect is $38,049.5$).
- There is no intensity drop corresponding to a hollow or low-attenuation cancellous vascular core.
- The endocranial rock matrix ($41,238.8 \pm 5803.9$) is slightly *denser* in X-ray attenuation than the surrounding bone ($37,690.1 \pm 5440.0$), reflecting heavy silicate and iron-bearing diagenetic permineralization.

---

## 5. Epistemic Synthesis & Biological Determination

### 5.1 Resolution of Competing Hypotheses
- **Hypothesis A (Radiologically Distinguishable Zonation)**: *Rejected*. The micro-CT volume exhibits no bimodal distribution within the bone mask, no low-attenuation vascular zone, and no distinct intensity gradient between the cortex and the deep core ($\text{CNR} = 0.0616$, $\text{AUC} = 0.5132$).
- **Hypothesis B (Diagenetically Permineralized / Attenuation-Uniform)**: *Confirmed*. Secondary mineral matrix (e.g. calcite, quartz, iron oxides) has completely infiltrated the vascular spaces and trabecular interspaces during fossilization.

### 5.2 Architectural Rule for Downstream Model B
Because diagenetic permineralization masks histological zonation in the raw CT attenuation numbers, attempting to segment Zone 2 by applying an arbitrary intensity threshold would produce unscientific, spurious geometry.

Therefore:
1. **Rule of Histological Reconstruction**: Model B multi-zone material properties must be allocated using **literature-informed geometric rules** derived from published thin-section histology (Schott et al. 2011, Snively & Theodor 2011).
2. **Geometric Mapping**: Histological depth ratios (e.g., dorsal cortex occupying the outer 2–5 mm or 10–15% of dome thickness, cancellous core occupying the central 70–80%, and basicranial zone occupying the basal region) will be mapped onto the registered canonical mesh frame ($G_0$) rather than inferred from CT gray levels.
3. **Epistemic Honesty**: The repository explicitly documents that Model B zonation is an *inferred histological reconstruction*, not a direct radiological segmentation.

---

## 6. Reproduction

This milestone is computationally reproducible under the project's standard environment and prospective workflow.

### Environment
- **Platform**: macOS (arm64, Apple Silicon)
- **Python Version**: Python 3.12 (`.venv` managed by `uv`)
- **Core Dependencies**: `numpy>=1.26.0`, `scipy>=1.12.0`, `pydicom>=2.4.0`, `matplotlib>=3.8.0`, `scikit-learn>=1.4.0`, `pytest>=8.0.0` (frozen in [`pyproject.toml`](../pyproject.toml))

### Provenance Commits
- **Governing Design**: [`docs/phase_design/PHASE5_GATE_C_DESIGN.md`](../docs/phase_design/PHASE5_GATE_C_DESIGN.md) *(Prospective)*
- **Execution Commit**: `acccb96` *(Primary characterization pipeline, metrics derivation, and figure generation)*
- **Report / Documentation Commit**: `acccb96` *(Formal report, decision D011, and living state updates)*

### Command-line Recipe
```bash
# 1. Execute the primary computational pipeline and figure generation
uv run python scripts/characterize_image_semantics.py

# 2. Execute automated verification test suite
uv run pytest tests/test_gate_c_semantics.py -v
```

### Primary Entry Points
- **Primary Executable Entry Point**: [`scripts/characterize_image_semantics.py`](../scripts/characterize_image_semantics.py)
- **Reusable Source Module**: [`src/stegoceras_biomechanics/ct/semantics.py`](../src/stegoceras_biomechanics/ct/semantics.py)
- **Automated Verification Test**: [`tests/test_gate_c_semantics.py`](../tests/test_gate_c_semantics.py)

### Generated Result Artifacts
- **Metrics JSON**: [`results/phase5/gate_c_semantics_metrics.json`](../results/phase5/gate_c_semantics_metrics.json)
- **Figure 13**: [`reports/figures/figure13_ct_intensity_semantics.png`](figures/figure13_ct_intensity_semantics.png)
- **Figure 14**: [`reports/figures/figure14_dome_attenuation_transects.png`](figures/figure14_dome_attenuation_transects.png)

### Governing Decision
- **Decision D011**: Model B Histological Zonation via Literature-Informed Geometric Rules (Phase 5 Gate C Freeze) in [`docs/DECISIONS.md`](../docs/DECISIONS.md).

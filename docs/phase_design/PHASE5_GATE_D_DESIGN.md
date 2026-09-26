# Phase 5 Gate D Design: Reconstruct Published Material Inference Logic

**Document Role**: Prospective Scientific Research & Computational Design  
**Status**: APPROVED / ACTIVE  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md) §4.4)  
**Specimen**: *Stegoceras validum* UALVP 2  
**Date Formulated**: 2026-09-25  

---

## 1. Scientific Question
*What explicit mathematical, anatomical, and spatial rules were used in published cranial biomechanics literature (Snively & Theodor 2011, Schott et al. 2011) to assign heterogeneous material properties to pachycephalosaur skull models, and can they be formalized as reproducible, deterministic code mapping onto the registered canonical mesh coordinate frame ($G_0$)?*

Specifically:
1. What exact constitutive parameters (Young's modulus $E$, Poisson's ratio $\nu$) were applied to the dorsal compact cortex (Zone 3), cancellous core (Zone 2), and basal basicranium (Zone 1) in Snively & Theodor (2011)?
2. What spatial rules (cortex thickness in mm, depth ratios, elevation thresholds) govern the boundary between Zone 3, Zone 2, and Zone 1 based on histological thin-sections of *Stegoceras* domes (Schott et al. 2011)?
3. How can these histological rules be projected deterministically onto the frozen 3-tier tetrahedral volume meshes ($h_1, h_2, h_3$) generated from canonical surface $G_0$, satisfying the **Mesh Invariant Principle** (Decision D03)?

---

## 2. Motivation / Prior Evidence
- Gate C demonstrated that empirical micro-CT attenuation cannot directly separate Zone 2 from Zone 3 due to diagenetic permineralization ($\text{CNR} = 0.0616 \ll 1.0$, $D_B = 0.0134$, $\text{AUC} = 0.5132$).
- Decision D011 mandates that Model B histological material allocation must strictly be constructed through literature-informed geometric rules from thin-section histology rather than unassisted CT thresholding.
- Before generating Model B volume material assignments in Gate E, Gate D must formalize the exact literature rules into deterministic code, preventing ad-hoc or unrecorded modeling choices.

---

## 3. Hypothesis or Competing Expectations
- **Hypothesis A (Simple Depth-Ratio Partitioning)**: A 3-zone architecture parameterized by normalized radial/vertical depth ratios (e.g. outer 15% cortex, central 70% cancellous, basal 15% compact) captures the primary mechanical stiffness gradient described in Snively & Theodor (2011) and Schott et al. (2011).
- **Hypothesis B (Absolute Cortical Shell Partitioning)**: An absolute distance offset (e.g., constant 3.0 mm outer cortical shell) is required to represent the dorsal impact envelope regardless of local dome thickness.

---

## 4. Scope
- **In Scope**:
  - Formalizing literature parameter registers: $E$ and $\nu$ for Zones 1, 2, and 3.
  - Spatial mapping algorithm: projecting depth from canonical surface $G_0$ to classify internal points.
  - Sensitivity bounds: literature-supported modulus variations ($E_{\text{cortex}} \in [10, 20]\text{ GPa}$, $E_{\text{core}} \in [0.5, 4.5]\text{ GPa}$).
  - Standalone verification script and unit tests.
- **Explicitly Out of Scope**:
  - Full FEA solving of Model B (deferred to Gate F).
  - Oblique or dynamic impact simulations (deferred to Gate G).

---

## 5. Experimental / Computational Design

### 5.1 Variables Being Formalized
- **Constitutive Properties**:
  - Zone 3 (Dorsal Cortex): $E = 17.0\text{ GPa}, \nu = 0.30$
  - Zone 2 (Cancellous Core): $E = 1.0\text{ GPa}, \nu = 0.25$
  - Zone 1 (Basal Bone / Basicranium): $E = 17.0\text{ GPa}, \nu = 0.30$
- **Spatial Boundary Rules**:
  - Cortical depth threshold: $d_{\text{cort}} = 3.0\text{ mm}$ (outer shell).
  - Basal boundary: $Z_{G_0} \le 65.0\text{ mm}$ or ventral endocranial proximity.
  - Core region: interior frontoparietal dome elements ($Z_{G_0} > 65.0\text{ mm}$ and $d_{\text{cort}} > 3.0\text{ mm}$).

### 5.2 Inputs & Upstream Artifacts
- **Canonical Mesh $G_0$**: `data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl`
- **Gate C Report & Metrics**: `reports/phase5_gate_c_semantics_report.md`
- **Literature Evidence Matrix**: `data/metadata/biomechanics_input_matrix.csv`

---

## 6. Acceptance / Discrimination Criteria
- **Criterion 1 (Element Accounting)**: 100% of volume mesh elements uniquely classified into Zone 1, 2, or 3 without unassigned or multi-assigned elements.
- **Criterion 2 (Topological Contiguity)**: Zone 3 forms a contiguous outer shell across the dorsal frontoparietal dome ($Z \ge 80\text{ mm}$).
- **Criterion 3 (Deterministic Reproducibility)**: Re-running the classification script produces identical element material tags across all refinement tiers ($h_1, h_2, h_3$).

---

## 7. Planned Computational Implementation
- **Command(s)**:
  1. `uv run python scripts/reconstruct_material_logic.py`
  2. `uv run pytest tests/test_gate_d_materials.py -v`
- **Primary Script**: `scripts/reconstruct_material_logic.py`
- **Reusable Module**: `stegoceras_biomechanics.materials.inference`
- **Target Output**: `results/phase5/gate_d_material_metrics.json`
- **Target Report**: `reports/phase5_gate_d_material_report.md`

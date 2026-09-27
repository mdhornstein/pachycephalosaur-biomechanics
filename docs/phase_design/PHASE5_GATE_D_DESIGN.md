# Phase 5 Gate D Design: Reconstruct Published Material Inference Logic

**Document Role**: Prospective Scientific Research & Computational Design  
**Status**: APPROVED / ACTIVE (Prospective Design Complete; Implementation Pending User Instruction)  
**Governing Standard**: Model Decision Basis v1 ([`docs/LITERATURE_TO_MODEL_DECISIONS.md`](../LITERATURE_TO_MODEL_DECISIONS.md) §4.4, Decision D012)  
**Specimen**: *Stegoceras validum* UALVP 2  
**Date Formulated**: 2026-09-25 (Updated 2026-09-26)  

---

## 1. Scientific Question

*How did published cranial biomechanics literature (Snively & Theodor 2011, Schott et al. 2011) turn radiological and histological observations into a heterogeneous 3-zone material model, and which parts of that inference chain can be independently and deterministically reconstructed in executable code?*

### Epistemic Transition from Gate C to Gate D
Phase 5 Gate C and Gate D address fundamentally different questions within the research program:

| Gate | Core Question | Scientific Target | Primary Finding / Method |
| :--- | :--- | :--- | :--- |
| **Gate C** | *What does the CT image actually show?* | Empirical fossil imaging data | Reconstructed CT intensity alone does not separate Zone 2 from Zone 3 ($\text{CNR} = 0.0616$, descriptive $\text{AUC} = 0.5132$). Unassisted CT thresholding cannot segment material zones. |
| **Gate D** | *How did published work infer material zonation, and what can we reconstruct?* | Published scientific inference chain | Dissect published literature (Snively & Theodor 2011, Schott et al. 2011) into explicit constitutive values, spatial geometric partitioning rules, and parameter sensitivity envelopes. |

### Specific Research Inquiries
1. **Constitutive Parameter Register**: What exact numerical values for Young's modulus ($E$), Poisson's ratio ($\nu$), and shear modulus ($G$) were assigned to each zone in Snively & Theodor (2011)? What empirical comparative analogues (bovid horncore, human/bovine cranial bone) justified those choices?
2. **Spatial Boundary Rules**: By what spatial criteria did Snively & Theodor (2011) and Schott et al. (2011) delineate the boundaries between:
   - **Zone 3**: Dorsal compact cortex (outer dome shell);
   - **Zone 2**: Deep cancellous / vascular core (frontoparietal interior);
   - **Zone 1**: Dense basal bone (basicranium, occipital condyle, skull roof base)?
3. **Reproducibility vs. Underspecification Audit**: Which steps of the published material assignment were mathematically explicit, and which steps relied on interactive visual thresholding or manual editing in proprietary software (Mimics) that cannot be perfectly reproduced from published text alone?
4. **Deterministic Formalization**: How can the published inference chain be formalized as a fully deterministic, reproducible geometric rule that maps onto the canonical coordinate frame ($G_0$) and satisfies the **Mesh Invariant Principle** (Decision D03) across refinement tiers ($h_1, h_2, h_3$)?

---

## 2. Motivation / Prior Evidence

- **Gate C Empirical Empirical Baseline**: Gate C established that reconstructed CT intensity is poorly separable between the dorsal cortex and cancellous core in UALVP 2 ($\text{CNR} = 0.0616 \ll 1.0$, Bhattacharyya distance $D_B = 0.0134$, descriptive $\text{ROC AUC} = 0.5132$). This empirical reality rules out automated CT thresholding as a defensible basis for Model B zonation.
- **Decision D011 Requirement**: Decision [`D011`](../DECISIONS.md) mandates that downstream Model B material zonation must not be segmented by CT thresholding, but must instead be constructed via literature-informed geometric rules derived from published histological thin sections (Schott et al. 2011, Snively & Theodor 2011).
- **Preventing Ad-Hoc Drift**: Before generating Model B volume elements in Gate E, Gate D must formalize the exact literature rules into audited, deterministic code, preventing unrecorded or arbitrary modeling choices.

---

## 3. Dissection of the Published Inference Chain

The published material model of Snively & Theodor (2011) rests on a four-stage inference chain:

```text
[Stage 1: Biological Observation]
Qualitative histology: compact outer cortex, trabecular cancellous core, dense basicranium
(Goodwin & Horner 2004, Schott et al. 2011, Snively & Theodor 2011)
        ↓
[Stage 2: Spatial Demarcation in Mimics]
CT visualization with narrow display windowing + interactive manual segmentation of internal cavity
(Reproducibility status: UNDERSPECIFIED / INTERACTIVE)
        ↓
[Stage 3: Modulus Assignment from Comparative Analogues]
E_cortex = 17.0 GPa (compact bone), E_core = 1.0 GPa (trabecular), E_base = 17.0 GPa
(Reproducibility status: EXPLICIT & AUDITED)
        ↓
[Stage 4: Parameter Sensitivity Bounds]
E_core ∈ [0.5, 4.5] GPa, E_cortex ∈ [10.0, 20.0] GPa
(Reproducibility status: EXPLICIT & AUDITED)
```

### Reproducible vs. Underspecified Elements
- **Reproducible Elements**:
  - The numerical constitutive values ($E = 17\text{ GPa}, \nu = 0.30$ for compact bone; $E = 1.0\text{ GPa}, \nu = 0.25$ for cancellous bone).
  - The nominal 3-zone architecture (basal, core, cortex).
  - The parameter sensitivity ranges tested in published sensitivity sweeps.
- **Underspecified Elements**:
  - The exact voxel-level spatial boundary between Zone 2 and Zone 3 in UALVP 2 was created in Mimics using visual thresholding and manual hollowing. Because Gate C showed that native CT voxel values lack strong cortex–core contrast, this boundary was sensitive to user windowing and manual editing.
  - To make the model scientifically reproducible, Gate D replaces interactive visual selection with an **explicit, parameterized geometric rule** (e.g. cortical shell depth $d_{\text{cort}} \le 3.0\text{ mm}$ on the dorsal dome, basal cutoff $Z \le 65.0\text{ mm}$, interior core).

---

## 4. Hypotheses & Model-Form Alternatives

Gate D evaluates two alternative spatial formulations for the Zone 3 / Zone 2 boundary:

- **Hypothesis A (Constant Cortical Shell Offset)**:
  An absolute distance offset from the dorsal canonical surface ($d_{\text{cort}} = 3.0\text{ mm}$) across the dorsal dome ($Z \ge 80.0\text{ mm}$) accurately reflects the average histological cortex thickness reported by Schott et al. (2011) ($2\text{--}4\text{ mm}$) and maintains a uniform structural impact envelope regardless of local dome curvature.
- **Hypothesis B (Proportional Depth Partitioning)**:
  A relative depth ratio (e.g., outer $15\%$ of local vertical thickness is cortex, central $70\%$ is cancellous core, basal $15\%$ is basicranium) reflects allometric dome scaling across different regions of the frontoparietal vault.

---

## 5. Scope

- **Explicitly In Scope**:
  - Formalizing the literature parameter register into machine-readable JSON.
  - Implementing deterministic spatial classification functions mapping 3D coordinates $(X, Y, Z)_{G_0}$ to Zone IDs $\{1, 2, 3\}$.
  - Defining the explicit sensitivity envelope for Model B Young's moduli ($E_{\text{cortex}} \in [10, 20]\text{ GPa}$, $E_{\text{core}} \in [0.5, 4.5]\text{ GPa}$).
  - Developing automated unit tests verifying deterministic classification, 100% element accounting, and domain validity.
- **Explicitly Out of Scope**:
  - Tetrahedral volume mesh generation or modification (deferred to Gate E).
  - FEA boundary-value problem solving (deferred to Gate F).
  - Asserting that Model B represents a directly measured biological tissue distribution rather than a literature-informed model-form scenario.

---

## 6. Mathematical & Spatial Formulation

### 6.1 Constitutive Parameter Register (Snively & Theodor 2011)

| Zone ID | Anatomical Material | Young's Modulus ($E$) | Poisson's Ratio ($\nu$) | Shear Modulus ($G$) | Comparative Biological Justification |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Zone 3** | Dorsal Compact Cortex | $17.0\text{ GPa}$ ($17,000\text{ MPa}$) | $0.30$ | $6.538\text{ GPa}$ | Mammalian / bovid cranial compact bone |
| **Zone 2** | Cancellous / Trabecular Core | $1.0\text{ GPa}$ ($1,000\text{ MPa}$) | $0.25$ | $0.400\text{ GPa}$ | Artiodactyl horncore cancellous bone |
| **Zone 1** | Dense Basal / Basicranium | $17.0\text{ GPa}$ ($17,000\text{ MPa}$) | $0.30$ | $6.538\text{ GPa}$ | Dense basicranial / basioccipital bone |

### 6.2 Deterministic Spatial Classification Rule
For any internal point $\mathbf{x} = (X, Y, Z)$ in the canonical coordinate frame $G_0$:
1. **Zone 1 (Basicranium / Basal Bone)**:
   $$\mathbf{x} \in \text{Zone 1} \iff Z \le Z_{\text{base}} \quad (Z_{\text{base}} = 65.0\text{ mm})$$
2. **Zone 3 (Dorsal Compact Cortex)**:
   $$\mathbf{x} \in \text{Zone 3} \iff Z > Z_{\text{base}} \quad \text{and} \quad d(\mathbf{x}, \partial G_0) \le d_{\text{cort}} \quad (d_{\text{cort}} = 3.0\text{ mm})$$
   where $d(\mathbf{x}, \partial G_0)$ is the Euclidean distance from $\mathbf{x}$ to the nearest triangle on the canonical outer surface $G_0$.
3. **Zone 2 (Cancellous Core)**:
   $$\mathbf{x} \in \text{Zone 2} \iff Z > Z_{\text{base}} \quad \text{and} \quad d(\mathbf{x}, \partial G_0) > d_{\text{cort}}$$

---

## 7. Acceptance & Discrimination Criteria

- **Criterion 1 (Exhaustive Element Partitioning)**:
  Every point or mesh element evaluated must be assigned strictly one Zone ID $\in \{1, 2, 3\}$. Unassigned, orphan, or multi-assigned elements are prohibited ($100.0\%$ accounting).
- **Criterion 2 (Spatial Topology & Shell Contiguity)**:
  Zone 3 must form a continuous external layer of nominal thickness $3.0\text{ mm}$ across the entire dorsal dome surface ($Z \ge 80\text{ mm}$).
- **Criterion 3 (Deterministic Invariance)**:
  Evaluating the spatial rule repeatedly or across different mesh resolutions ($h_1, h_2, h_3$) must produce identical spatial boundary contours, satisfying Decision D03.
- **Criterion 4 (Parameter Completeness)**:
  The parameter register must include both baseline values and bounded sensitivity ranges supported by literature citations.

---

## 8. Interpretation Limits

- **Model-Form Scenario, Not Direct Measurement**: Model B represents an evidence-based model-form scenario reconstructing published literature hypotheses, NOT a direct patient-specific segmentation of preserved fossil tissue.
- **Histological Approximation**: The $3.0\text{-mm}$ uniform cortical shell is an idealized mathematical abstraction of the variable $2\text{--}4\text{ mm}$ cortex observed in physical thin sections (Schott et al. 2011).
- **Diagenetic Reality**: The assignment of $E = 1.0\text{ GPa}$ to the cancellous core reflects the hypothesized in vivo condition of the living dinosaur, not the physical stiffness of the permineralized rock matrix present in the museum fossil today.

---

## 9. Planned Computational Implementation

- **Planned Execution Command(s)**:
  ```bash
  uv run python scripts/reconstruct_material_logic.py
  uv run pytest tests/test_gate_d_materials.py -v
  ```
- **Primary Script**: `scripts/reconstruct_material_logic.py`
- **Reusable Source Module**: `stegoceras_biomechanics.materials.inference`
- **Verification Test Suite**: `tests/test_gate_d_materials.py`
- **Target Output Metrics**: `results/phase5/gate_d_material_metrics.json`
- **Target Report**: `reports/phase5_gate_d_material_report.md`

---

## 10. Traceability & Decision Authority

```text
Scientific Question (How did published work assign material properties?)
       ↓
Gate D Design (docs/phase_design/PHASE5_GATE_D_DESIGN.md)
       ↓
Implementation (scripts/reconstruct_material_logic.py, stegoceras_biomechanics.materials.inference)
       ↓
Verification Suite (tests/test_gate_d_materials.py)
       ↓
Result Artifacts (results/phase5/gate_d_material_metrics.json)
       ↓
Gate D Report (reports/phase5_gate_d_material_report.md)
       ↓
Decision D012 (Model B Material Zonation Formalization)
```

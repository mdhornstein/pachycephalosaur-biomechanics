# Phase 3 Benchmark Specification: Provisional Parameterized Surface-Derived Benchmark for Stegoceras validum (UALVP 2)

**Author / Investigation**: Computational Biomechanics Research Pipeline  
**Specimen**: *Stegoceras validum* (UALVP 2, referred specimen)  
**Primary Reference Inspiration**: Snively & Theodor (2011) *PLoS ONE* 6(6): e21412, Figures 12 & 13  
**Benchmark Characterization**: Surface-Derived Homogeneous-Material Approximation (Model A)  
**Milestone**: Phase 3 Benchmark Specification (Provisional Parameterized Benchmark)  

---

## 🎯 1. Scientific Objective & Qualitative Benchmark Targets

### 1.1 Scope & Modeling Intent
This document defines a **provisional, explicitly parameterized benchmark specification** for a **minimal surface-derived homogeneous-material model (Model A)**. 

Because Snively & Theodor (2011) incorporated CT-derived internal material heterogeneity, Model A is **not an exact 1:1 numerical replication** of the published model. Instead, it serves as a **surface-derived approximation inspired by the published study**, establishing an uncompromised computational baseline to verify mesh generation, solver execution, load sensitivity, and global stress dissipation before introducing complex internal material partitioning or uncertainty quantification.

### 1.2 Core Research Question:
> *Under a standardized compressive load ($1.0\text{ kN}$ normalized reference, and $1360\text{ N}$ derived biological impact) applied to the dorsal frontoparietal dome apex of Stegoceras validum (UALVP 2), what are the resulting cranial von Mises stress fields, principal strains, and stress attenuation patterns across the braincase and basicranium under broad vs. concentrated contact patch envelopes?*

### 1.3 Three-Tier Validation Hierarchy:
Rather than demanding an arbitrary $\pm 20\%$ exact numerical match for a model with deliberately simplified material architecture, we establish a formal three-tier validation hierarchy:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       THREE-TIER VALIDATION HIERARCHY                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 1: Qualitative / Topological Reproduction (Primary Milestone Gate)     │
│ • Spatial distribution of stress concentrations matches published patterns. │
│ • High stress on dorsal dome apex dissipates steeply toward the braincase.  │
│ • Broad loading yields low diffuse stress; concentrated loading produces    │
│   intense local apex stresses at geometric notch singularities.             │
│ • Endocranial roof remains protected with low relative stress and strain.   │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 2: Quantitative Order-of-Magnitude Comparison                          │
│ • Peak and modal stress magnitudes fall within published literature orders  │
│   under nominal parameter values (e.g., peak broad stress ~3-10 MPa,        │
│   concentrated peak stress ~30-60 MPa, endocranial roof < 5 MPa).           │
│ • Normalized linear compliance (MPa/kN) established as reference baseline.  │
├─────────────────────────────────────────────────────────────────────────────┤
│ TIER 3: Exact Numerical Replication                                         │
│ • Explicitly recognized as UNATTAINABLE with Model A due to deliberate      │
│   simplifications (homogeneous vs. CT-zoned material, unified STL vs.       │
│   original Avizo solid mesh). Deferred to high-fidelity CT models (Model C).│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📐 2. Geometry & Explicit Scale Parameterization

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODEL A BENCHMARK GEOMETRY & BOUNDARIES                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                   ↓↓↓↓↓↓  NORMALIZED REFERENCE LOAD (1.0 kN)               │
│                 ┌─────────┐  [Broad Envelope vs Concentrated Apex Patch]    │
│             .-'´           `'-.                                             │
│          .-'   FRONTOPARIETAL  `'-.                                         │
│        .'          DOME            '.                                       │
│       /                              \                                      │
│      |   [Unified Monolithic Solid]   |                                     │
│      |   (Homogeneous Isotropic Bone) |◄─── NUCHAL CREST CONSTRAINT         │
│     /      [ENDOCRANIAL CAVITY]        \    (Translational restraint)       │
│    |              (Void)                |                                   │
│     \                                  /                                    │
│      '--.            PALATE       .--'                                      │
│          `'-.                  .-'                                          │
│              `'--.________.--'                                              │
│                     ▲                                                       │
│                     └─── OCCIPITAL CONDYLE CONSTRAINT                       │
│                          (Fixed: Ux=Uy=Uz=0)                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Geometric Domain
* **Base Anatomy**: Articulated cranium derived from `data/meshes/original/whole_skull/WitmerLab_Stegoceras_UALVP2-000018284.stl` (repaired to watertight manifold solid) or composite assembly of the 32 component STLs.
* **Internal Void**: Endocranial braincase cavity and nasal passages hollowed as void boundaries.
* **Sutural Formulation**: Fused monolithic continuum (following Snively & Theodor 2011).

### 2.2 Explicit Physical Scale Parameter ($s_{\text{mm/unit}}$)
Rather than fixing coordinate scale as an uncalibrated empirical fact, physical scale is treated as an **explicit modeling parameter**:
* **Scale Parameter**: $s_{\text{mm/unit}}$ (ratio of physical millimeters to STL coordinate units).
* **Nominal Assumption**: $s_{\text{nominal}} = 1.0\text{ mm/unit}$ (based on literature basal skull length $L \approx 200\text{ mm}$ vs. STL extent $\Delta y = 200.50\text{ units}$).
* **Sensitivity Envelope**: $s_{\text{mm/unit}} \in [0.95, 1.05]$ (to be formally propagated in downstream UQ).
* *Note on Scaling Physics*: In linear elasticity, holding applied force $F$ constant while scaling geometry by $s$ causes surface area to scale as $s^2$, volume as $s^3$, and stress as $\sigma \propto F / s^2$. Documenting $s$ explicitly ensures complete mathematical transparency.

---

## 🧱 3. Constitutive Material Properties

* **Constitutive Model**: Linear-elastic, isotropic, homogeneous compact bone.
* **Young's Modulus ($E$)**: **$17.0\text{ GPa}$** ($17,000\text{ MPa}$; baseline mammalian/bovine cortical bone from Cowin 2001, Hellmich et al. 2008, Bell et al. 2009).
  * *Sensitivity Range*: $E \in [10.0, 20.0]\text{ GPa}$.
* **Poisson's Ratio ($\nu$)**: **$0.30$** (dimensionless).
* **Mass Density ($\rho$)**: **$1.90\times 10^{-9}\text{ tonne/mm}^3$** ($1900\text{ kg/m}^3$; inactive in static linear FEA).
* **Compressive Yield Strength ($\sigma_y$)**: **$140.0\text{ MPa}$** (for nominal safety factor reporting).
* **Compressive Ultimate Strength ($\sigma_{\text{ult}}$)**: **$190.0\text{ MPa}$**.

---

## 🎯 4. Boundary Constraints

1. **Occipital Condyle (Atlas Articulation)**:
   * *Selection*: Articular facets of the occipital condyle on the posterior neurocranium.
   * *Prescription*: Rigid translational constraint:
     $$u_x = 0, \quad u_y = 0, \quad u_z = 0$$
2. **Nuchal Crest Rim (Dorsal Cervical Musculature)**:
   * *Selection*: Posterior dorsal rim of the squamosals and parietosquamosal nuchal shelf.
   * *Prescription*: Translational constraint along anteroposterior and dorsoventral axes ($u_y = 0, u_z = 0$) representing tensile restraint from *m. transversospinalis capitis* and *m. complexus* (Tsuihiji 2005; McHenry et al. 2007).

---

## ⚡ 5. Loading Protocols: Normalized Reference & Biological Cases

### 5.1 Linear Scaling Principle
Under linear elasticity with small displacements (${\mathbf K}{\mathbf u} = {\mathbf F}$):
$${\mathbf u}(\alpha {\mathbf F}) = \alpha {\mathbf u}({\mathbf F}), \quad {\boldsymbol \sigma}(\alpha {\mathbf F}) = \alpha {\boldsymbol \sigma}({\mathbf F})$$
Stress, strain, and displacement scale strictly linearly with load magnitude. Therefore, we define the **$1.0\text{ kN}$ unit load as the primary numerical benchmark**, and derive the $1360\text{ N}$ case as an exact linear scalar multiple:
$${\boldsymbol \sigma}_{1360} = 1.36 \times {\boldsymbol \sigma}_{1000}$$

### 5.2 Contact Patch Envelopes & Nominal Values
Rather than hardcoding arbitrary single-point contact areas, we define parameterized contact patch envelopes reflecting literature ranges:

1. **Broad "Keratin Cap" Load Case (Primary Benchmark)**:
   * *Literature Envelope*: $A_{\text{broad}} \in [2500, 4000]\text{ mm}^2$ ($25\text{--}40\text{ cm}^2$, representing wide distribution through a compliant keratin shield; Snively & Theodor 2011, p. 7).
   * *Nominal Benchmark Area*: **$A_{\text{broad}} = 3000.0\text{ mm}^2$**.
   * *Reference Traction ($1.0\text{ kN}$)*: $T_{\text{ref}} = 1000\text{ N} / 3000\text{ mm}^2 = 0.3333\text{ MPa}$.
   * *Biological Traction ($1360\text{ N}$)*: $T_{\text{bio}} = 1360\text{ N} / 3000\text{ mm}^2 = 0.4533\text{ MPa}$.

2. **Concentrated "Point Impact" Load Case**:
   * *Literature Envelope*: $A_{\text{conc}} \in (0, 200]\text{ mm}^2$ ($< 2\text{ cm}^2$, representing impact on bare bone or thin worn keratin; Snively & Theodor 2011, p. 7).
   * *Nominal Benchmark Area*: **$A_{\text{conc}} = 150.0\text{ mm}^2$**.
   * *Reference Traction ($1.0\text{ kN}$)*: $T_{\text{ref}} = 1000\text{ N} / 150\text{ mm}^2 = 6.6667\text{ MPa}$.
   * *Biological Traction ($1360\text{ N}$)*: $T_{\text{bio}} = 1360\text{ N} / 150\text{ mm}^2 = 9.0667\text{ MPa}$.

---

## 📊 6. Output Quantities & Acceptance Criteria

### Measured Computational Outputs:
1. **Normalized Stress Compliance Field**: $\bar{\boldsymbol \sigma}(x,y,z) = {\boldsymbol \sigma}(x,y,z) / F_{\text{ref}}$ ($\text{MPa/kN}$).
2. **Von Mises Stress Field**: $\sigma_{\text{vM}}(x,y,z)$ at $F = 1.0\text{ kN}$ and $F = 1360\text{ N}$.
3. **Principal Strains**: $\varepsilon_1, \varepsilon_3$ ($\mu\varepsilon$ and $\mu\varepsilon/\text{kN}$).
4. **Total Strain Energy**: $U = \frac{1}{2} \int_\Omega {\boldsymbol \sigma} : {\boldsymbol \varepsilon} \, dV$ ($\text{mJ}$ and $\text{mJ/kN}^2$).
5. **Nominal Safety Factor Field**: $\text{SF}(x,y,z) = \sigma_y / \sigma_{\text{vM}}(x,y,z)$.

### Acceptance Criteria:

| Benchmark Output | Target Behavior (Tier 1 & Tier 2) | Reference Comparison (Snively & Theodor 2011) |
| :--- | :--- | :--- |
| **Broad Load Dome Apex Stress** | Peak $\sigma_{\text{vM}} \approx 4.4\text{--}6.0\text{ MPa/kN}$ ($6.0\text{--}8.0\text{ MPa}$ at $1360\text{ N}$); modal $\sim 2.2\text{ MPa/kN}$ ($3.0\text{ MPa}$ at $1360\text{ N}$) | Qualitative and order-of-magnitude agreement with Fig 13A |
| **Concentrated Apex Stress** | Peak $\sigma_{\text{vM}} \approx 25.0\text{--}40.0\text{ MPa/kN}$ ($35.0\text{--}55.0\text{ MPa}$ at $1360\text{ N}$) at geometric notch singularities; deep cortex $\sim 1.0\text{--}1.5\text{ MPa/kN}$ | Qualitative agreement with Fig 13C |
| **Endocranial Roof Protection** | Stresses lining braincase roof remain $< 3.7\text{ MPa/kN}$ ($< 5.0\text{ MPa}$ at $1360\text{ N}$); nominal safety factor $> 25$ | Protective shielding consistent with Fig 12A |
| **Stress Attenuation Gradient** | $> 70\%$ reduction in von Mises stress from dorsal apex to braincase roof | Severe stress attenuation deep to impact |

---

## ⚖️ 7. Unresolved Choices & Explicit Assumptions

The following modeling decisions are explicitly documented as **provisional assumptions** to be investigated and quantified in subsequent phases:
1. **Load Patch Facet Selection**: Exact morphological boundary of the apex facet cluster.
2. **Global Axis & Orientation**: Coordinate alignment of vertical dorsal compression relative to anatomical neutral head posture.
3. **Boundary Node Selection**: Precise nodal cluster chosen for the occipital condyle and nuchal shelf.
4. **Mesh Discretization Strategy**: Tetrahedral solid element type (linear vs. quadratic) and local mesh density around neurovascular canals.
5. **Physical Scale Sensitivity**: Parameter $s_{\text{mm/unit}} = 1.0$ treated as nominal baseline pending direct caliper verification.
6. **Internal Histology Omission**: Zone 2 cancellous core omitted from Model A baseline, to be evaluated in Model B sensitivity tier.

---

## 🏁 8. Phase 3 Gate Summary

This document establishes a **provisional, explicitly parameterized benchmark specification** for the first computational experiment. It formalizes a three-tier validation hierarchy and separates linear structural compliance ($1.0\text{ kN}$) from biological load assumptions ($1360\text{ N}$).

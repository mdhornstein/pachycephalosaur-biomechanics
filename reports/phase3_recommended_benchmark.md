# Phase 3 Benchmark Specification: First Defensible Biomechanical Experiment for Stegoceras validum (UALVP 2)

**Author / Investigation**: Computational Biomechanics Research Pipeline  
**Specimen**: *Stegoceras validum* (UALVP 2, referred specimen)  
**Primary Reproduction Target**: Snively & Theodor (2011) *PLoS ONE* 6(6): e21412, Figures 12 & 13  
**Milestone**: Phase 3 Benchmark Experiment Specification  

---

## 🎯 1. Scientific Objective & Research Question

### Core Research Question:
> *Under a quasi-static compressive impact load ($1360\text{ N}$) applied to the dorsal apex of the frontoparietal dome of Stegoceras validum (UALVP 2), what are the resulting cranial von Mises stress magnitudes, principal strain distributions, and stress attenuation patterns across the braincase and basicranium under broad vs. concentrated contact regimes?*

### Specific Reproduction Target:
Reproduce the baseline structural response and stress dissipation patterns documented in **Snively & Theodor (2011)**:
* **Target 1 (Broad Load Regime, Fig 13A)**: Peak von Mises stress on the dorsal dome apex of **$6.0\text{--}8.0\text{ MPa}$**, with a modal stress of **$\sim 3.0\text{ MPa}$**.
* **Target 2 (Concentrated Load Regime, Fig 13C)**: Peak von Mises stress at notch singularities (edges of neurovascular canals) of **$\sim 46.0\text{ MPa}$**, rapidly attenuating to **$1.5\text{--}2.0\text{ MPa}$** deep in the cortex.
* **Target 3 (Braincase Protection, Fig 12A)**: Stresses lining the dorsal roof of the endocranial cavity remaining below **$5.0\text{ MPa}$** (safety factor $> 25$).
* **Target 4 (Linear Force Normalization)**: Report both absolute metrics at $F = 1360\text{ N}$ and normalized linear compliance metrics ($\text{MPa} / \text{kN}$).

---

## 📐 2. Geometry Specification: Model A (Minimal Surface-Derived Homogeneous Model)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODEL A BENCHMARK GEOMETRY & BOUNDARIES                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                   ↓↓↓↓↓↓  APPLIED COMPRESSIVE LOAD (1360 N)                │
│                 ┌─────────┐  Broad Cap vs Concentrated Apex Patch           │
│             .-'´           `'-.                                             │
│          .-'   FRONTOPARIETAL  `'-.                                         │
│        .'          DOME            '.                                       │
│       /                              \                                      │
│      |   [Unified Monolithic Solid]   |                                     │
│      |                                |◄─── NUCHAL CREST CONSTRAINT         │
│     /      [ENDOCRANIAL CAVITY]        \    (Translational restraint)       │
│    |              (Void)                |                                   │
│     \                                  /                                    │
│      '--.            PALATE       .--'                                      │
│          `'-.                  .-'                                          │
│              `'--.________.--'                                              │
│                     ▲                                                       │
│                     └─── OCCIPITAL CONDYLE CONSTRAINT                       │
│                          (Fixed: Ux=Uy=Uz=0, Rx=Ry=Rz=0)                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Geometric Domain**: Complete articulated cranium derived from `data/meshes/original/whole_skull/WitmerLab_Stegoceras_UALVP2-000018284.stl` (or watertight composite of the 32 component STLs).
* **Internal Boundaries**: Endocranial cavity and nasal passage hollowed as void boundaries.
* **Sutural Formulation**: Fused monolithic continuum (following Snively & Theodor 2011).
* **Physical Scale**: $1.0\text{ coordinate unit} = 1.0\text{ mm}$ ($L = 200.50\text{ mm}$, $W = 131.13\text{ mm}$, $H = 127.71\text{ mm}$).

---

## 🧱 3. Constitutive Material Properties

* **Constitutive Model**: Linear-elastic, isotropic, homogeneous compact bone.
* **Young's Modulus ($E$)**: **$17.0\text{ GPa}$** ($17,000\text{ MPa}$; baseline bovine/mammalian cortical bone from Cowin 2001, Hellmich et al. 2008, Bell et al. 2009).
* **Poisson's Ratio ($\nu$)**: **$0.30$** (dimensionless).
* **Mass Density ($\rho$)**: **$1.90\times 10^{-9}\text{ tonne/mm}^3$** ($1900\text{ kg/m}^3$; consistent with mm-tonne-s unit system).
* **Compressive Yield Strength ($\sigma_y$)**: **$140.0\text{ MPa}$** (for safety factor evaluation).
* **Compressive Ultimate Strength ($\sigma_{\text{ult}}$)**: **$190.0\text{ MPa}$**.

---

## 🎯 4. Boundary Constraints

1. **Occipital Condyle (Atlas Articulation)**:
   * *Selection*: Articular facets of the occipital condyle on the posterior basicranium.
   * *Prescription*: Fixed in all 3 translational degrees of freedom:
     $$u_x = 0, \quad u_y = 0, \quad u_z = 0$$
2. **Nuchal Crest Rim (Dorsal Neck Extensors)**:
   * *Selection*: Posterior dorsal rim of the squamosals and parietosquamosal shelf.
   * *Prescription*: Constrained in translation along the anteroposterior and dorsoventral axes ($u_y = 0, u_z = 0$) to represent tensile restraint of *m. transversospinalis capitis* and *m. complexus*.

---

## ⚡ 5. Loading Protocols

Two distinct spatial load cases will be applied under a resultant compressive force $F = 1360.0\text{ N}$ directed along the global vertical axis ($\mathbf{f} = [0, 0, 1360]\text{ N}$ in native STL orientation):

1. **Load Case 1 — Broad "Keratin Cap" Load (Primary Validation Target)**:
   * *Contact Area*: Distributed uniformly across a broad dorsal facet patch ($A \approx 3000\text{ mm}^2$) on the frontoparietal dome apex.
   * *Traction*: Uniform surface traction $T_z = F / A \approx 0.45\text{ MPa}$.
2. **Load Case 2 — Concentrated "Point Impact" Load**:
   * *Contact Area*: Restricted to a narrow apex facet cluster ($A \approx 150\text{ mm}^2$).
   * *Traction*: Surface traction $T_z \approx 9.0\text{ MPa}$.
3. **Load Case 3 — Unit Benchmark Load ($F = 1.0\text{ kN}$)**:
   * Normalized $1000\text{ N}$ load to yield linear compliance maps ($\text{MPa/kN}$ stress and $\mu\varepsilon / \text{kN}$ strain).

---

## 📊 6. Output Quantities & Acceptance Criteria

### Measured Computational Outputs:
1. **Von Mises Equivalent Stress Field**:
   $$\sigma_{\text{vM}} = \sqrt{\frac{1}{2}\left[(\sigma_1 - \sigma_2)^2 + (\sigma_2 - \sigma_3)^2 + (\sigma_3 - \sigma_1)^2\right]}$$
2. **Maximum & Minimum Principal Strains** ($\varepsilon_1, \varepsilon_3$).
3. **Total Strain Energy ($U$)**:
   $$U = \frac{1}{2} \int_\Omega {\boldsymbol \sigma} : {\boldsymbol \varepsilon} \, dV$$
4. **Cranial Safety Factor Distribution**:
   $$\text{SF}(x,y,z) = \frac{\sigma_y}{\sigma_{\text{vM}}(x,y,z)}$$

### Quantitative Literature Agreement Criteria:

| Output Metric | Benchmark Target (Broad Load) | Benchmark Target (Concentrated Load) | Literature Target (Snively & Theodor 2011) | Acceptance Threshold |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Dome Apex von Mises Stress** | $6.0\text{--}8.0\text{ MPa}$ | $35.0\text{--}50.0\text{ MPa}$ | $6\text{--}8\text{ MPa}$ (Broad) / $46\text{ MPa}$ (Conc.) | Within $\pm 20\%$ of published range |
| **Modal Dome Apex von Mises Stress** | $2.5\text{--}3.5\text{ MPa}$ | $5.0\text{--}10.0\text{ MPa}$ | $\sim 3.0\text{ MPa}$ | Within $\pm 20\%$ |
| **Endocranial Roof Peak Stress** | $< 5.0\text{ MPa}$ | $< 6.0\text{ MPa}$ | $< 5.0\text{ MPa}$ | $< 6.0\text{ MPa}$ (Safety Factor $> 20$) |
| **Global Stress Dissipation Ratio** | $> 70\%$ attenuation from apex to braincase | $> 85\%$ attenuation from apex to braincase | Pronounced attenuation deep to impact | $> 70\%$ reduction |

---

## ⚖️ 7. Explicit Uncertainty Accounting

### Excluded from First Benchmark (Intentionally Deferred to Phase 4 / UQ):
1. **Internal Histological Zonation (Zone 2 Cancellous Core)**: Handled separately in Model B sensitivity testing.
2. **Sutural Compliance**: Modeled as fused solid (exact Snively & Theodor 2011 formulation).
3. **Explicit In Vivo Keratin Layer**: Represented via broad load distribution envelope rather than discrete solid mesh.
4. **Anisotropic Trabecular Radiance**: Modeled as isotropic continuum.
5. **Nonlinear Elasticity / Plasticity**: Linear static small-displacement formulation.

---

## 🏁 8. Phase 3 Gate Summary

This benchmark specification provides an unambiguous, fully constrained, and reproducible finite element experiment. It establishes exact numerical validation targets derived directly from the primary literature without implementing premature FEA code.

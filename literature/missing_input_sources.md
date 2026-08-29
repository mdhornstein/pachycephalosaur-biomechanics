# Investigation of Alternative Sources for Missing Biomechanical Inputs

**Author / Investigation**: Computational Biomechanics Research Pipeline  
**Specimen**: *Stegoceras validum* (UALVP 2, referred specimen)  
**Deliverable**: Literature & Data Gap Resolution Strategy  

---

## 🔍 Overview

This document systematically investigates alternative scientific sources, published paleohistological studies, comparative biomechanics literature, and surrogate modeling strategies for all model parameters identified as `UNAVAILABLE` or `LITERATURE_ONLY` in [`data/metadata/biomechanics_input_matrix.csv`](file:///Users/michael/Library/CloudStorage/GoogleDrive-mdhornstein@gmail.com/My%20Drive/AA%20Projects/pachycephalosaurus-biomechanics/data/metadata/biomechanics_input_matrix.csv).

---

## 📋 Strategy & Classification Matrix

| Input ID | Parameter | Status in Current Dataset | Potential External Source(s) | Proposed Resolution Category | Feasibility & Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INP-GEO-03** | Physical Scale Calibration ($mm$) | `INFERABLE_WITH_ASSUMPTION` | Specimen UALVP 2 osteological descriptions (Lambe 1918; Gilmore 1924; Sues & Galton 1987); published skull length ($200\text{ mm}$) in Snively & Theodor (2011) Table 1. | **Direct measurement possible** (via published anatomical measurements) | Measure basal skull length and dome width in literature descriptions to verify candidate $1.0\text{ mm/unit}$ scale factor to within $\pm 2\%$. |
| **INP-GEO-05** | Internal Histological Zonation (Zones 1, 2, 3) | `UNAVAILABLE` | Goodwin & Horner (2004) *Paleobiology*; Schott et al. (2011) *PLoS ONE*; Snively & Cox (2008) *Palaeontologia Electronica*. | **Biologically informed assumption possible** (as sensitivity model) / **Omitted from simplified model** | In adult *Stegoceras* (UALVP 2), Zone 2 is reduced relative to juveniles. A 3-zone model can be parameterized geometrically via internal shell offsets for sensitivity analysis, or omitted in a homogeneous baseline model. |
| **INP-GEO-06** | Cortical Thickness Distribution | `UNAVAILABLE` | Snively & Theodor (2011) transverse CT slice figures (Fig 2, 5, 6); physical sectioning of comparative domes. | **Biologically informed assumption possible** / **Requires new data** for high precision | Approximate thickness ($5\text{--}15\text{ mm}$ cortex over dome apex) can be estimated from published CT figures, but full 3D distribution requires raw CT slices. |
| **INP-GEO-07** | In Vivo Keratin Shield Morphology | `UNAVAILABLE` | Hieronymus et al. (2009) *Anat Rec*; Snively & Cox (2008); modern bovid horn sheath morphology (Kitchener 1988; Farke 2008). | **Biologically informed assumption possible** | Soft-tissue keratin is 100% unpreserved in fossils. Standard practice is to test bounding load distribution envelopes (broad distributed cap vs. narrow point load). |
| **INP-MAT-01** | Cortical Bone Elastic Modulus ($E_{\text{cort}}$) | `LITERATURE_ONLY` | Cowin (2001) *Bone Mechanics*; Erickson et al. (2002) *Nature* (osteocyte lacunae & dinosaur bone properties); Currey (2002); Jasinoski et al. (2009). | **Literature substitution possible** | Dinosaur bone tissue is histologically fibrolamellar/osteonal, mechanically comparable to bovine haversian cortical bone ($E = 10.0\text{--}20.0\text{ GPa}$, standard baseline $17.0\text{--}18.0\text{ GPa}$). |
| **INP-MAT-02** | Cortical Poisson's Ratio ($\nu_{\text{cort}}$) | `LITERATURE_ONLY` | Cowin (2001); Standard vertebrate biomechanics literature. | **Literature substitution possible** | Standard isotropic constant $\nu = 0.30$ ($0.28\text{--}0.33$ range) universally adopted across vertebrate cranial FEA. |
| **INP-MAT-03** | Cancellous Bone Modulus ($E_{\text{canc}}$) | `LITERATURE_ONLY` | Turner et al. (1990) *J Biomech*; Vahey et al. (1987); Kuhn et al. (1989); Snively & Theodor (2011). | **Literature substitution possible** / **Biologically informed assumption** | Mammalian/bovine trabecular bone ranges $0.5\text{--}4.5\text{ GPa}$. Snively & Theodor (2011) adopted $1.0\text{ GPa}$ as a conservative baseline. |
| **INP-MAT-04** | Cancellous Poisson's Ratio ($\nu_{\text{canc}}$) | `LITERATURE_ONLY` | Turner et al. (1990); Cowin (2001). | **Literature substitution possible** | Standard value $\nu = 0.25$ ($0.20\text{--}0.30$). |
| **INP-MAT-05** | Cortical Mass Density ($\rho_{\text{cort}}$) | `LITERATURE_ONLY` | Cowin (2001); Currey (2002). | **Literature substitution possible** | Standard value $\rho = 1900\text{--}2000\text{ kg/m}^3$. Inactive in static linear FEA (${\mathbf K}{\mathbf u} = {\mathbf F}$). |
| **INP-MAT-06** | Cancellous Mass Density ($\rho_{\text{canc}}$) | `LITERATURE_ONLY` | Turner et al. (1990); Cowin (2001). | **Literature substitution possible** | Apparent density $\rho = 800\text{--}1200\text{ kg/m}^3$. Inactive in static linear FEA. |
| **INP-MAT-07** | Keratin Pad Elastic Modulus ($E_{\text{ker}}$) | `LITERATURE_ONLY` | Kitchener (1988, 1992); Tombolato et al. (2010) *Acta Biomater*. | **Literature substitution possible** | Measured bovid horn keratin exhibits $E = 1.5\text{--}4.5\text{ GPa}$ ($3.9\text{ GPa}$ baseline). |
| **INP-LOAD-01** | Impact Force Magnitude ($1360\text{ N}$) | `LITERATURE_ONLY` | Snively & Cox (2008) *Palaeontol Electron*; Snively & Theodor (2011) Table 1. | **Literature substitution possible** (as standard benchmark load) | Derived from $40\text{ kg}$ body mass at $3.0\text{ m/s}$ closing velocity. In linear elasticity, stresses scale strictly linearly ($\sigma \propto F$), allowing normalized reporting ($\text{MPa/kN}$). |
| **INP-BC-02** | Nuchal Muscle Restraint Stiffness | `AVAILABLE_DIRECT` / `LITERATURE_ONLY` | Tsuihiji (2005); Snively & Russell (2007); McHenry et al. (2007). | **Biologically informed assumption possible** | Modeled either as kinematic zero-displacement constraints or compliant linear spring elements ($k \approx 10^4\text{--}10^6\text{ N/m}$) along the nuchal crest rim. |

---

## 🔬 Detailed Analysis of Key Ambiguities

### 1. Histological Zonation Evidence in *Stegoceras* (Goodwin & Horner 2004)
* **Goodwin & Horner (2004)** identified three histological zones in pachycephalosaur domes:
  * *Zone 1*: Basal compact bone lining the braincase.
  * *Zone 2*: Middle vascular, cancellous bone.
  * *Zone 3*: Superficial dense compact bone with radiating vascular canals.
* **Ontogenetic Nuance**: Goodwin & Horner demonstrated that **Zone 2 regresses during ontogeny**, with older adult individuals exhibiting extensive secondary remodeling and consolidation into dense compact bone throughout the dome apex.
* **Implication for UALVP 2**: UALVP 2 is a mature adult specimen with a heavily ossified dome. The cancellous Zone 2 core is relatively thin and restricted compared to juvenile specimens. Modeling UALVP 2 as a homogeneous compact structure (Model A) is therefore a biologically defensible baseline representation of an adult cranial vault, while a 3-zone partitioned model (Model B) serves as a conservative sensitivity test for lower internal stiffness.

### 2. Physical Unit Calibration Strategy
* Rather than guessing or assuming millimeter scaling, we calibrate the coordinate system by cross-referencing anatomical landmarks in the 3D surface mesh against published caliper measurements of UALVP 2:
  * Total basal skull length (premaxilla to occipital condyle): $\approx 195\text{--}205\text{ mm}$ (Gilmore 1924; Sues & Galton 1987).
  * STL coordinate extent in Y-axis: $\Delta y = 200.50\text{ units}$.
  * Conclusion: $1.0\text{ coordinate unit} \equiv 1.0\text{ mm}$ with a scaling uncertainty of $< 2.5\%$.

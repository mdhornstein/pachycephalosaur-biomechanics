# Comprehensive Model Parameter & Methodology Audit: Snively & Theodor (2011)

**Reference**:  
Snively, E. & Theodor, J. M. (2011). "Common functional correlates of head-strike behavior in the pachycephalosaur *Stegoceras validum* (Ornithischia, Dinosauria) and combative artiodactyls." *PLoS ONE* 6(6): e21412. [doi:10.1371/journal.pone.0021422](https://doi.org/10.1371/journal.pone.0021422) | [PMC3125168](https://pmc.ncbi.nlm.nih.gov/articles/PMC3125168/)

**Purpose**:  
This document provides a line-by-line extraction and methodological audit of every computational model parameter, geometric entity, boundary condition, material assignment, loading formulation, and empirical result reported by Snively & Theodor (2011) for the *Stegoceras validum* specimen **UALVP 2** (cited in the paper as **UA 2**) and comparative artiodactyl taxa.

---

## 🏛️ 1. Taxonomic, Specimen & Scanning Provenance

### 1.1 Study Specimen Identity
* **Taxon**: *Stegoceras validum* Lambe, 1902
* **Taxonomic Lectotype**: CMN 515 (Canadian Museum of Nature, Ottawa; isolated frontoparietal dome)
* **Study Specimen**: UALVP 2 (University of Alberta Laboratory for Vertebrate Paleontology, Edmonton; referred specimen comprising articulated skull, mandible, and postcrania; cited as "UA 2" in Snively & Theodor 2011).
* **Ontogenetic Stage**: Adult (frontoparietal dome fully fused, sutures largely obliterated, squamosal nodes well-developed).
* **Evidence Level**: **Level A** (Direct specimen observation).

### 1.2 CT Acquisition Modalities
Snively & Theodor (2011) scanned UALVP 2 on two distinct CT systems (Section *Materials and Methods*, p. 9 / lines 394–399):
1. **Medical Scanner**: General Electric Lightspeed CT scanner at Canada Diagnostics Centre (Calgary, Alberta). Used for initial diagnostic density evaluation.
2. **High-Resolution Industrial Micro-CT**: Scanned at the University of Texas High-Resolution X-ray CT Facility (UTCT, Austin, Texas).
   - *Reported Resolution*: "twice the transverse resolution and 4.5 times the anteroposterior resolution of the original medical scan" (p. 10).
   - *Voxel Dimensions*: Specific numerical voxel pitch ($x, y, z$ in $\mu m$) is **not explicitly stated** in the text (recorded as `AMBIGUOUS` in input matrix).
   - *Artifacts Documented*: Beam hardening inflated apparent density of the superficial dome cortex (approaching 3000 Hounsfield Units, HU); permineralization obscured original bone mineral density (p. 6, 10).

---

## 📐 2. Geometry & Segmentation Methodology

### 2.1 3D Surface Reconstruction & Cleaning
* **Software Tools**:
  * *Mimics®* (Materialise): Density-based threshold segmentation masks on CT slices (after Arbour & Snively 2009; Bell et al. 2009).
  * *Manual Matrix Removal*: "For the *Stegoceras* models, imaged matrix had to be removed manually within the cranial sinuses and endocranial cavity" (p. 10).
  * *Surface Optimization*: Cyclic error detection and repair in Mimics® remesher and *Geomagic® Studio* (Geomagic Inc.).
  * *Avizo®* (Visage Imaging): Final surface smoothing and solid meshing.
* **Geometric Entity Modeled**:
  * The cranium was modeled as a **unified, fused solid structure**. Sutures between individual cranial bones (e.g., frontoparietal, squamosals, postorbitals, basicranium) were **not modeled as explicit contact interfaces or compliant elements**.
* **Internal Cavities**:
  * Endocranial cavity (braincase) and nasal/sinus passages were hollowed out as internal void boundaries.
* **Neurovascular Canals**:
  * Tubular canals traversing the dome cortex and opening onto the dorsal surface were preserved in the high-resolution geometry (visible in Figures 1, 2, 13).

### 2.2 Volumetric Mesh Specifications
Snively & Theodor (2011) constructed two distinct finite element meshes for *Stegoceras* (p. 10):
1. **Primary High-Resolution Tetrahedral Solid Model**:
   * *Mesh Size*: **2.2 million solid elements** (generated in Avizo®).
   * *Element Type*: 4-node linear or 10-node quadratic solid tetrahedra (exact polynomial order not explicitly stated; recorded as `AMBIGUOUS`).
   * *Purpose*: Primary analysis model for stress/strain distributions and keratin pad comparison (Figure 13).
2. **Voxel-Based Hexahedral Model**:
   * *Mesh Size*: ~**200,000 hexahedral elements** (grouped voxels in Mimics®).
   * *Purpose*: Methodological comparison with voxel-based artiodactyl models.

---

## 🧱 3. Material Properties & Constitutive Formulations

### 3.1 Material Constitutive Model
* **Formulation**: Linear-elastic, isotropic, small-displacement (${\boldsymbol \sigma} = {\mathbf C} : {\boldsymbol \varepsilon}$).
* **Spatial Heterogeneity**: Multi-region partitioning based on CT Hounsfield Units and literature-derived moduli.

### 3.2 Material Property Assignments for *Stegoceras*

| Anatomical / Histological Region | Young's Modulus ($E$) | Poisson's Ratio ($\nu$) | Mass Density ($\rho$) | Source / Citation | Measurement Type | Evidence Level | Notes & Uncertainty |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Zone 3 / Outer Cortex (Dome Peak)** | $17.0\text{--}20.0\text{ GPa}$ (indexed to 2500 HU) | $0.30\text{--}0.38$ (typical bone) | $\sim 1800\text{--}2000\text{ kg/m}^3$ | Hellmich et al. (2008); Cowin (2001); Bell et al. (2009) | Borrowed from bovine/human cortical bone | **Level C** | Manual cap at 2500 HU applied to suppress CT beam-hardening artifacts. Value not measured in dinosaur bone. |
| **Zone 2 / Cancellous Core (Internal Dome)** | **$1.0\text{ GPa}$** | $0.25\text{--}0.30$ | $\sim 800\text{--}1200\text{ kg/m}^3$ | Turner et al. (1990); Cowin (2001) | Borrowed from mammalian/human cancellous bone | **Level C** | Explicitly chosen as a "conservatively low elastic modulus". Cattle/human trabecular bone ranges 0.5–4.5 GPa. |
| **Zone 1 / Basal Compact Bone (Braincase Roof)** | $17.0\text{--}20.0\text{ GPa}$ (dense compacta) | $0.30\text{--}0.38$ | $\sim 1800\text{--}2000\text{ kg/m}^3$ | Cowin (2001) | Borrowed from mammalian cortical bone | **Level C** | Dense compact layer lining the dorsal margin of the endocranial cavity. |
| **Braincase, Palate & Basicranium** | $10.0\text{--}15.0\text{ GPa}$ (variable compacta) | $\sim 0.30$ | $\sim 1600\text{--}1800\text{ kg/m}^3$ | Snively & Theodor (2011) | Inferred from lower CT Hounsfield values | **Level D** | Moderately lower stiffness assigned to palate and basicranium relative to dome apex. |
| **Keratinous Covering / Dome Pad** | **$3.9\text{ GPa}$** (when modeled directly in *Ovibos*) | **$0.28$** | **$1300\text{ kg/m}^3$** | Kitchener (1992); Kitchener (1988) | Measured on bovid horn keratin | **Level C** | In *Stegoceras*, keratin geometry was unpreserved; its mechanical effect was modeled by varying the applied load area (broad vs. concentrated). |

### 3.3 Strength & Failure Criteria Cited in Paper
* **Cortical Bone Compressive Strength**: $\sigma_{\text{ult}} = 180\text{--}200\text{ MPa}$; yield stress $\sigma_y \approx 130\text{--}150\text{ MPa}$ (Cowin 2001).
* **Cortical Bone Ultimate Strain**: $\varepsilon_{\text{ult}} = 0.6\% = 0.0060$ (p. 6).
* **Cancellous Bone Compressive Strength**: $\sigma_{\text{ult}} = 6\text{--}12\text{ MPa}$ (Vahey et al. 1987; Kuhn et al. 1989).
* **Cancellous Bone Ultimate Strain**: $\varepsilon_{\text{ult}} = 0.52\%\text{--}1.21\%$ ($0.0052\text{--}0.0121$) (Cowin 2001).

---

## 🎯 4. Boundary Constraints & Muscle Attachments

Snively & Theodor (2011) applied multi-point kinematic boundary conditions to replicate head-neck articulation and muscular restraint (Section *Methods*, p. 10 / lines 407–408):

1. **Occipital Condyle Constraint**:
   * *Location*: Articular surface of the occipital condyle (articulating with the atlas vertebra).
   * *Formulation*: Rigidly fixed in all translational and rotational degrees of freedom ($U_x = U_y = U_z = 0$, $R_x = R_y = R_z = 0$).
   * *Artifacts*: Authors note that rigid pinning produces local stress concentration singularities (up to $52\text{ MPa}$), but these do not affect stresses in the dorsal dome.
2. **Nuchal Musculature Constraint**:
   * *Location*: Rim of the nuchal crest (posterior margin of parietosquamosal shelf).
   * *Anatomical Target*: Insertion zone of dorsal neck extensors (*m. transversospinalis capitis* / *m. complexus* after Tsuihiji 2005; Snively & Russell 2007; Maryańska & Osmólska 1974).
   * *Formulation*: Translationally constrained to simulate tension from neck musculature restraining offset forces (after McHenry et al. 2007).
   * *Effect*: Adding nuchal constraints dramatically reduced artificial stress at the occipital condyle and floor of the endocranial cavity.
3. **Basitubera Constraint (Evaluated but discarded)**:
   * *Location*: Basipterygoid processes / basal tubera.
   * *Outcome*: Produced severe artificial ventral stress singularities without influencing dome stresses; excluded from final primary reporting.

---

## ⚡ 5. Loading Conditions & Collision Physics

### 5.1 Load Magnitude
* **Applied Force ($F$)**: **$1,360\text{ N}$** ($1.36\text{ kN}$).
* **Biological / Scaling Rationale**:
  * Calculated from kinetic energy and momentum of an impact between two similarly sized pachycephalosaurs (*Homalocephale calathoceros*, body mass $\approx 40\text{ kg}$) closing at $v = 3.0\text{ m/s}$ (Snively & Cox 2008).
  * *Evidence Level*: **Level D** (Biologically informed scaling assumption, borrowed from *Homalocephale* calculation).

### 5.2 Load Direction & Application Modes
Compressive forces were applied in three distinct spatial distributions on the dorsal frontoparietal dome (Figure 13, p. 7):
1. **Broad "Cap" Distribution (Mode A)**:
   * Distributed across a wide surface area ($\approx 25\text{--}40\text{ cm}^2$) over the dome apex.
   * *Biological Meaning*: Represents impact through a thick, compliant in vivo cornified keratin shield that deforms and distributes contact pressure.
   * *Result*: Peak von Mises stress $6\text{--}8\text{ MPa}$, modal stress $3\text{ MPa}$.
2. **Intermediate Distribution (Mode B)**:
   * Distributed across a moderately restricted contact patch ($\approx 10\text{--}15\text{ cm}^2$).
   * *Result*: Peak von Mises stress $12\text{--}18\text{ MPa}$.
3. **Concentrated Point Load (Mode C)**:
   * Applied directly to a narrow cluster of apex facets ($< 2\text{ cm}^2$).
   * *Biological Meaning*: Represents direct impact on bare bone or under a thin, worn keratin layer.
   * *Result*: Local peak stress up to $46\text{ MPa}$ at mesh notch singularities (edges of neurovascular canals), attenuating to $1.5\text{--}2.0\text{ MPa}$ deep in the cortex.

### 5.3 Static vs. Dynamic Impact Formulation
* **Formulation**: **Quasi-static linear analysis** (${\mathbf K} {\mathbf u} = {\mathbf F}$).
* **Justification by Authors**: Stress and strain scale linearly with force magnitude in elastic regimes. True dynamic explicit impact was considered computationally unnecessary for comparative peak stress and safety factor evaluation (p. 9).

---

## 📊 6. Reported Quantitative Results & Validation Targets

### 6.1 Published Stress, Strain & Safety Factor Targets for *Stegoceras* (UALVP 2)

| Metric | Region / Location | Reported Value in Paper | Units | Source in Paper |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Cortical von Mises Stress (Broad Load)** | Dorsal Dome Apex | $6.0\text{--}8.0$ | $\text{MPa}$ | Figure 13A, p. 7 |
| **Modal Cortical von Mises Stress (Broad Load)** | Dorsal Dome Apex | $\sim 3.0$ | $\text{MPa}$ | Figure 13A, p. 7 |
| **Peak Cortical von Mises Stress (Concentrated Load)** | Notch singularities at neurovascular canals | $46.0$ | $\text{MPa}$ | Figure 13C, p. 7 |
| **Deep Cortical von Mises Stress (Concentrated Load)** | Deep to superficial notch singularities | $1.5\text{--}2.0$ | $\text{MPa}$ | Text p. 6, 7 |
| **Cancellous Core von Mises Stress (Zone 2)** | Internal frontoparietal dome | $\sim 1.0$ | $\text{MPa}$ | Figure 12A, p. 6 |
| **Cancellous Core Strain** | Internal frontoparietal dome | $\sim 0.02\%$ ($0.0002$) | Dimensionless | Text p. 6, 8 |
| **Braincase / Endocranial Roof Stress** | Dorsal margin of brain cavity | Peak $5.0$ | $\text{MPa}$ | Figure 12A, p. 6 |
| **Cortical Safety Factor (Yield)** | Zone 3 / Dome Apex | $20\text{--}30+$ (up to $100$ in transect) | Dimensionless ($\sigma_y / \sigma$) | Figure 12B, p. 6 |
| **Cancellous Safety Factor (Yield)** | Zone 2 / Cancellous Core | $8\text{--}10$ | Dimensionless ($\sigma_y / \sigma$) | Figure 12A, p. 6 |
| **Occipital Condyle Peak Stress (Artifact)** | Fixed constraint boundary | Up to $52.0$ | $\text{MPa}$ | Text p. 6 |

---

## 🔍 7. Evaluation of Ambiguities & Unresolved Methodological Details

1. **Uncalibrated Physical Scale / Dimensions**:
   The paper does not state the explicit length, width, and height bounding extents ($mm$) assigned to the Strand7 mesh nodes, relying implicitly on the UTCT voxel scale.
2. **Volumetric Internal Mesh Geometry Undeposited**:
   Neither the 2.2-million-element tetrahedral mesh file nor the segmented internal cancellous boundaries are included in the open-access supplementary materials or on MorphoSource.
3. **Exact Equation Linking Hounsfield Units to Modulus in Stegoceras**:
   While Bell et al. (2009) is cited for extant taxa ($E = f(\text{HU})$), the text explicitly notes that *Stegoceras* could not use this automated curve due to fossil permineralization, and instead used manual zone thresholding (p. 10). The exact geometric coordinates of those internal partition surfaces are unrecorded.

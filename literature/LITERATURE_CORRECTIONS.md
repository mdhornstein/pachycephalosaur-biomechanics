# Literature Review Audit Corrections & Integration Matrix

> **Context:** Formal tracking log mapping every finding from the independent literature audit at commit [`673a222`](https://github.com/mdhornstein/pachycephalosaur-biomechanics/commit/673a222) (`literature/independent_literature_audit.md`) to specific corrective actions across the repository's literature synthesis, dossiers, and evidence matrices.  
> **Status:** All findings systematically addressed with statuses: `corrected`, `partially corrected`, `unresolved`, or `rejected with justification`.

---

## 1. Audit Finding to Correction Mapping

| Audit Finding ID | Audit Finding Summary | Category | Action Taken | Source / Evidence | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AF-01** | Sullivan citation in dossier P03 conflates Sullivan (2003) *Stegoceras* revision with Sullivan (2006) pachycephalosaur family review. | Bibliography | Split into distinct records. Cited Sullivan (2003) for *Stegoceras* genus revision, UALVP 2 description, and lectotype comparison. Separately cited Sullivan (2006) for family-level taxonomy. | Sullivan, R. M. (2003). *JVP* 23(1):181–207, DOI: `10.1671/0272-4634(2003)23[181:ROTDSL]2.0.CO;2`. Sullivan, R. M. (2006). *NMMNHS Bull.* 35:347–365. | `corrected` |
| **AF-02** | Wrong authors for cranial pathology study in P07 / `UALVP2-18` / `UALVP2-19` (“Peterson & Vittore 2013”). | Bibliography | Corrected authors to Joseph E. Peterson, Collin Dischler, and Nicholas R. Longrich across dossier P07, evidence matrix, and synthesis text. Kept DOI `10.1371/journal.pone.0068620`. | Peterson, J. E., Dischler, C., & Longrich, N. R. (2013). *PLOS ONE* 8(7):e68620. DOI: `10.1371/journal.pone.0068620`. | `corrected` |
| **AF-03** | Dumont et al. (2009) journal mislabeled as *Journal of Experimental Biology* in synthesis reference key (`FE-17`). | Bibliography | Corrected journal to *Journal of Theoretical Biology* 256:96–103, verified exact title, and resolved DOI `10.1016/j.jtbi.2008.08.017`. Upgraded from `UNVERIFIED` to verified. | Dumont, E. R., Grosse, I. R., & Slater, G. J. (2009). *J. Theor. Biol.* 256:96–103. DOI: `10.1016/j.jtbi.2008.08.017`. | `corrected` |
| **AF-04** | Use of “comparative validation” in prior-model table (§5.3) and text for Snively & Theodor (2011). | Terminology / V&V | Replaced “comparative validation” with “comparative extant-taxon support / comparative functional corroboration.” Explicitly noted that UALVP 2 has no specimen-specific physical strain-gauge validation. | Snively & Theodor (2011); Henninger et al. (2010); Bright & Rayfield (2011). | `corrected` |
| **AF-05** | Material-property discussion risks treating scalar Young's modulus ($E$) as the primary material problem rather than spatial architecture. | Material Modeling / UQ | Formulated explicit 3-step material hierarchy: (1) internal spatial architecture/zonation, (2) region-specific constitutive properties ($E, \nu$), (3) CT-to-stiffness mapping under permineralization. Framed homogeneous $E$ strictly as a baseline control branch. | Snively & Theodor (2011); Goodwin & Horner (2004); Nirody et al. (2022). | `corrected` |
| **AF-06** | Prescriptive “4–6 tier refinement ladder” in synthesis §10–11 presented as a methodological requirement. | Numerical / FEM | Removed arbitrary tier count. Defined convergence stopping criteria based on predefined tolerances across multiple scientific quantities of interest (energy, displacement, regional stress). | Bright & Rayfield (2011); Erdemir et al. (2012). | `corrected` |
| **AF-07** | CT evidence matrix row `EV-018` / `S19` references “Recent 2026 microFE evidence” without traceable bibliographic citation. | Bibliography / Traceability | Linked row `EV-018` explicitly to Fraterrigo et al. (2026) with full journal, volume, page, and DOI metadata. | Fraterrigo, G., et al. (2026). *J. Mech. Behav. Biomed. Mater.* 176:107326. DOI: `10.1016/j.jmbbm.2025.107326`. | `corrected` |
| **AF-08** | Decision logic for heterogeneous/zonated representation in evidence-to-model mapping (§7) lacks explicit decomposition. | Material Modeling | Decomposed into: (a) anatomical architecture/regions from CT & histology, (b) constitutive parameters per region, and (c) CT density-to-stiffness mapping uncertainty. | Snively & Theodor (2011); Goodwin & Horner (2004). | `corrected` |
| **AF-09** | Statement that “comparative FEA can distinguish mechanical behavior ... even when absolute tissue properties are uncertain” is too broad. | Epistemic Discipline | Qualified as a conditional claim: comparative inference holds only if the tested parameter uncertainty does not reverse rankings for the specified QoI and load scenario. | Bright & Rayfield (2011); Godinho et al. (2017); Sylvester & Kramer (2018). | `corrected` |
| **AF-10** | Conflation of volume-mesh $h$-refinement with surface-geometry resolution sensitivity. | Numerical / FEM | Explicitly stated that volume $h$-refinement holds surface geometry, element formulation, material map, loads, BCs, and solver settings fixed to isolate discretization discrepancy. Surface-resolution sensitivity (McCurry et al. 2015) is a separate upstream geometry-processing sensitivity layer. | McCurry, Evans, & McHenry (2015); Bright & Rayfield (2011). | `corrected` |
| **AF-11** | Compressing “CT-informed” and “measured” fossil stiffness into single phrase in Snively & Theodor summary. | Epistemic / Materials | Standardized wording to “CT-informed / manually assigned material representation under fossilization and beam-hardening uncertainty.” Clarified that cancellous $E = 1.0\text{ GPa}$ was an assumed model input, not a measured property. | Snively & Theodor (2011) p. 3–4. | `corrected` |
| **AF-12** | Describing 1360 N force as an estimate of actual biological impact force experienced by living *Stegoceras*. | Loading / Epistemic | Standardized phrasing to “literature benchmark load scenario.” Clarified it was scaled from similarly sized *Homalocephale* at 3 m/s closing speed to place the model in comparative context, not an observed biological load. | Snively & Theodor (2011); Snively & Cox (2008). | `corrected` |
| **AF-13** | Woodruff & Ackermans citation date formatting is inconsistent across files. | Bibliography | Normalized citation to: *The Anatomical Record* 309(5):1235–1256 (2026 issue; first published online 4 July 2024), DOI: `10.1002/ar.25526`. | Woodruff, D. C., & Ackermans, N. L. (2026). DOI: `10.1002/ar.25526`. | `corrected` |
| **AF-14** | Unverified citations in reference key risk silent promotion to verified status. | Bibliography / Epistemic | Retained `UNVERIFIED` labels explicitly for unverified DOIs/records (Marinescu et al. 2005, Ross et al. 2005, Panagiotopoulou et al. 2010, Fitton et al. 2012, Cuff et al. 2015, Marcé-Nogué 2022, Gilmore 1924, Sues & Galton 1987). | Traceability standards; `independent_literature_audit.md` §3.1. | `corrected` |
| **AF-15** | Omission of Nirody et al. (2022) quantitative high-resolution CT vascularity study of *Stegoceras validum*. | Missing Literature | Added Nirody et al. (2022) as core reference (`BIO-13` / `P24` / `UALVP2-22`). Integrated findings on internal vascular canal networks (relative vascularity increases during dome development and decreases in late ontogeny) into dome anatomy, CT interpretation, and material zonation sections. | Nirody, J. A., et al. (2022). *JVP* 41(5):e2036991. DOI: `10.1080/02724634.2021.2036991`. | `corrected` |
| **AF-16** | Under-integration of load-case diversity highlighted by Woodruff & Ackermans (2024/2026). | Loading / Biomechanics | Upgraded from conceptual warning to explicit modeling requirement: “headbutting” across extant taxa encompasses diverse contact geometries, velocities, and striking surfaces. Mandated a family of scenario load cases (varying contact area, angle, location) rather than a single canonical headbutt. | Woodruff & Ackermans (2026). *Anat. Rec.* 309(5):1235–1256. | `corrected` |
| **AF-17** | Under-integration of Moore et al. (2022) postcranial myology of UALVP 2. | Missing Literature / Anatomy | Fully integrated Moore et al. (2022) into behavioral mechanics context: appendicular musculature and pelvic girdle adaptations provide whole-body stabilization mechanisms compatible with withstanding axial forces during agonistic butting. | Moore, B. R. S., et al. (2022). *PLOS ONE* 17(9):e0268144. DOI: `10.1371/journal.pone.0268144`. | `corrected` |
| **AF-18** | Treating peak local von Mises stress as primary convergence or behavioral endpoint. | Numerical / Biomechanics | Explicitly deprioritized point stress maxima due to known singularities at point constraints, load patch boundaries, and neurovascular canals. Replaced with strain energy, landmark displacements, and regional volume-percentile stresses. | Bright & Rayfield (2011); Snively & Theodor (2011). | `corrected` |
| **AF-19** | Describing coarse/medium mesh discrepancies as an uncertainty distribution. | Terminology / UQ | Standardized terminology: used “output-specific numerical discretization discrepancy” for observed differences among mesh tiers. Separated strictly from physical/mathematical “model-form uncertainty.” | Roy & Oberkampf (2011); Henninger et al. (2010). | `corrected` |
| **AF-20** | Smearing distinct uncertainty classes into unjustified probability distributions. | UQ Methodology | Enforced strict uncertainty taxonomy: continuous probability distributions are restricted to parameters with empirical literature distributions; unconstrained variations (BCs, dynamic vs. static, homogeneous vs. zonated) are treated as discrete scenario branches. | Laz & Browne (2010); Ling, Mullins & Mahadevan (2014). | `corrected` |
| **AF-21** | Implying that the literature establishes headbutting as an established biological fact. | Biological Interpretation | Neutralized functional claims: presented agonistic combat, sociosexual display, species recognition, and feeding performance trade-offs as competing, non-mutually-exclusive hypotheses. Maintained that mechanical competence demonstrates capability under model assumptions, not historical occurrence. | Goodwin & Horner (2004); Peterson et al. (2013); Woodruff & Ackermans (2026); Bateman & Larsson (2026). | `corrected` |
| **AF-22** | Elevating anisotropy and suture mechanics to primary UQ parameters without specimen-specific evidence. | Model-Form / UQ | Relegated anisotropy and suture compliance to conditional model-form branches. Established that isotropic zonated models must precede orthotropic formulations, and suture compliance requires demonstrated anatomical patency in UALVP 2. | Moazen et al. (2013); Rayfield (2005); `independent_literature_audit.md` §5.4–5.5. | `corrected` |
| **AF-23** | Treating cranial scale as a continuous random variable for a single specimen model. | Specimen Geometry / UQ | Clarified that for specimen-specific UALVP 2 modeling, physical dimensions are fixed by CT. Scale is an imaging provenance and segmentation audit check, not an aleatory biological distribution. | Schott et al. (2011); `independent_literature_audit.md` §5.6. | `corrected` |

---

## 2. Detailed Narrative of Key Corrections

### 2.1 Bibliographic Rectification
1. **Sullivan (2003) vs. Sullivan (2006)**:
   - *Problem*: In `pachycephalosaur_stegoceras_ualvp2_dossier.md` (P03) and the synthesis, Sullivan (2006) was cited for the genus revision of *Stegoceras* with volume `26(2)` and pages `370–383`.
   - *Resolution*: The genus revision describing UALVP 2 and establishing its conformity to the type specimen is **Sullivan, R. M. (2003)**, *Journal of Vertebrate Paleontology* 23(1):181–207, DOI: `10.1671/0272-4634(2003)23[181:ROTDSL]2.0.CO;2`. The 2006 paper is a distinct, family-wide review: **Sullivan, R. M. (2006)**, *New Mexico Museum of Natural History and Science Bulletin* 35:347–365. Both are now distinguished with accurate bibliographic metadata.
2. **Authorship of Peterson et al. (2013)**:
   - *Problem*: Dossier entry P07 and matrix rows `UALVP2-18`/`19` attributed the 22% dome pathology study (DOI `10.1371/journal.pone.0068620`) to “Peterson & Vittore (2013)”.
   - *Resolution*: The authors are **Joseph E. Peterson, Collin Dischler, and Nicholas R. Longrich (2013)**. Peterson & Vittore (2012) is a separate publication on a single specimen. The citation has been corrected across all files.
3. **Dumont et al. (2009) Journal Normalization**:
   - *Problem*: Synthesis table key `FE-17` mislabeled Dumont et al. (2009) as *Journal of Experimental Biology*.
   - *Resolution*: Corrected to **Journal of Theoretical Biology** 256:96–103, DOI: `10.1016/j.jtbi.2008.08.017`.
4. **Resolution of `EV-018` Traceability**:
   - *Problem*: Evidence row `EV-018` in the CT matrix lacked a formal bibliographic attribution.
   - *Resolution*: Explicitly attributed to **Fraterrigo et al. (2026)**, *Journal of the Mechanical Behavior of Biomedical Materials* 176:107326, DOI: `10.1016/j.jmbbm.2025.107326`.

---

### 2.2 Terminology, Verification, and Validation (V&V)
1. **Comparative Corroboration vs. Physical Validation**:
   - The term “comparative validation” has been systematically eradicated for Snively & Theodor (2011). Because no physical strain gauges or ex vivo displacement tests were performed on UALVP 2, agreement with extant combative artiodactyl trends represents **comparative functional corroboration / extant-analogue support**, not physical validation.
2. **Numerical Verification vs. Physical Validity**:
   - Mesh convergence demonstrations and manufactured-solution checks are strictly categorized as **numerical verification**. Passing numerical verification confirms that the discrete equations are solved accurately, but does not validate whether the physical model (geometry, materials, loads, BCs) represents biological reality.
3. **Discretization Discrepancy vs. Model-Form Uncertainty**:
   - Output differences between coarse ($h_1$), medium ($h_3$), and fine ($h_4$) meshes are designated as **output-specific numerical discretization discrepancies**. They are not treated as random parameter distributions or confused with alternative physical representations (such as linear vs. nonlinear kinematics, or homogeneous vs. zonated bone).

---

### 2.3 Internal Material Architecture and CT Mapping
1. **Three-Tier Material Decision Logic**:
   - *Tier 1: Internal Anatomical Architecture*: Micro-CT and histology directly demonstrate that UALVP 2 is not a uniform solid bone block, but possesses distinct compact cortical layers, a radiating trabecular core, and neurovascular canals.
   - *Tier 2: Constitutive Parameter Assignment*: Because fossil bone is permineralized, original living mechanical properties ($E, \nu$) cannot be measured directly from the fossil. Extant vertebrate bone literature informs plausible constitutive ranges (e.g., cancellous $E \in [0.5, 5.0]\text{ GPa}$, cortical $E \in [10.0, 25.0]\text{ GPa}$). From these plausible bounds, specific values are chosen as **project model parameters** (e.g., the project's $E = 17.0\text{ GPa}$ baseline, or prior literature assumptions such as cancellous $1.0\text{ GPa}$ / cortical $17.0\text{ GPa}$); every such parameter remains a modeling assumption for the fossil, not an experimentally established physical measurement.
   - *Tier 3: CT-to-Density Mapping Uncertainty*: Taphonomic mineral infilling and X-ray beam hardening prevent direct automated conversion of Hounsfield Units into elastic modulus. CT mapping is therefore an inference requiring sensitivity analysis.
2. **Role of the Homogeneous Baseline**:
   - The Phase 4 homogeneous isotropic model ($E = 17.0\text{ GPa}, \nu = 0.30$) is defined strictly as a **project modeling parameter and simplified control baseline**. It serves to isolate geometry, boundary conditions, and numerical discretization effects before introducing heterogeneous material zonation in Phase 8; it must not be interpreted as an experimentally established property of UALVP 2.

---

### 2.4 Loading, Contact Mechanics, and Boundary Conditions
1. **The 1360 N Benchmark Scenario**:
   - The 1360 N load applied by Snively & Theodor (2011) is codified as a **literature benchmark scenario** (derived from a 3 m/s collision of similarly sized *Homalocephale*), not an estimate of actual impact force in life.
2. **Load-Case Scenario Families & Sensitivity Envelopes**:
   - Incorporating the insights of Woodruff & Ackermans (2026), cranial combat among extant vertebrates encompasses diverse contact surfaces, angles, velocities, and striking kinematics rather than a single stereotyped impact. To explore this sensitivity, the project investigates a structured family of discrete load scenarios. Specific numerical bounds under consideration (e.g., candidate dorsal patch area $A \in [2500, 4000]\text{ mm}^2$ and impact inclination $\alpha \in [0^\circ, 20^\circ]$) are **candidate project design ranges / sensitivity envelopes** pending explicit morphological and biomechanical justification, not literature-established biological distributions for UALVP 2.

---

### 2.5 Incorporation of Essential Literature
1. **Nirody et al. (2022)** (*Journal of Vertebrate Paleontology* 41(5):e2036991):
   - Quantified vascular canal volume and orientation in the frontoparietal dome of *Stegoceras validum* using high-resolution CT.
   - Demonstrated that relative vascularity increases during dome development and then decreases substantially in late ontogeny, providing quantitative CT evidence for dynamic internal architecture and confirming histological observations by Goodwin & Horner (2004).
   - Provides essential constraints on the resolution of internal architecture in micro-CT and directly informs the thresholding and zonation requirements for Phase 8.
2. **Moore et al. (2022)** (*PLOS ONE* 17(9):e0268144):
   - Reconstructed pelvic and hindlimb myology from the exceptional postcranial skeleton of UALVP 2.
   - Demonstrated osteological and myological adaptations for wide-stance rotational stability and axial force transmission to the substrate, providing the postcranial anatomical context for cranial impact plausibility.

---

## 3. Verification & Compliance Checklist

- [x] All 23 findings from `literature/independent_literature_audit.md` mapped with explicit status.
- [x] DOIs, authors, titles, and journal names verified against authoritative records.
- [x] `UNVERIFIED` tags preserved where metadata cannot be independently verified.
- [x] V&V terminology strictly normalized (no improper “validation”).
- [x] Material architecture decomposed into 3-step decision logic.
- [x] Phase 4 frozen baseline and FEM solver code remain completely unmodified.

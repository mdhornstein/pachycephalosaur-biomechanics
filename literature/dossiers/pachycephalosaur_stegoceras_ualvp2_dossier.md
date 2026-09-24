# Pachycephalosaurs / *Stegoceras* / UALVP 2 — Biological & Biomechanical Evidence Dossier

**Status:** Evidence-base module; not a final literature-review chapter.

**Scope:** *Stegoceras validum*, specimen UALVP 2, broader Pachycephalosauria, dome anatomy/histology, proposed head-strike/headbutting behavior, and prior biomechanical/FEA studies.

**Epistemic rule:** Every substantive statement is classified as one of:

- **DO — Direct observation:** explicitly measured, described, imaged, or computed in the cited source.
- **AI — Author interpretation:** interpretation explicitly made by the cited authors.
- **MA — Model assumption:** an input, boundary condition, material assignment, or conceptual assumption used by a model.
- **IN — Inference:** inference made from evidence but not directly measured in the cited source.
- **SYN — Reviewer synthesis:** synthesis across sources in this dossier.
- **UNVERIFIED:** detail not sufficiently verified from the source available during this review pass.

No conclusion below is intended to decide whether headbutting occurred.

---

## 1. Executive evidence summary

### What is well established

1. **UALVP 2 is a historically important, nearly complete *Stegoceras* specimen.** The University of Alberta fossil-history page records it as found by George F. Sternberg in 1921 during the University of Alberta field program; Sullivan's (2003) revision describes UALVP 2 as a nearly complete skull with both lower jaws and parts of the postcranial skeleton and notes that the type specimen conforms to it. **[DO]**
2. **UALVP 2 has been used directly in CT-based biomechanical work.** Snively & Theodor (2011) CT-scanned UALVP 2 and used it in FEA alongside extant artiodactyl crania and another pachycephalosaur. **[DO]**
3. **Its internal cranial structure is mechanically heterogeneous.** The 2011 CT study reported denser cortical bone toward the dome apex, a lower-density trabecular region, trabeculae broadly oriented perpendicular to the outer surface, a dense deep compact layer, and numerous canals leading toward the cranial surface. Nirody et al. (2022) independently quantified this dome vascularity using high-resolution CT. **[DO]**
4. **Pachycephalosaur dome ontogeny is not simply a binary juvenile/adult switch.** Schott et al. (2011) modeled continuous cranial ontogeny in *Stegoceras validum* and showed substantial variation in dome development across the growth series. The exact biological age of UALVP 2 is not directly established here by a single independent age measurement. **[DO + SYN]**
5. **The classic biomechanical literature establishes mechanical plausibility, not behavioral proof.** Snively & Cox (2008) and Snively & Theodor (2011) found that modeled pachycephalosaur crania could sustain simulated impacts and exhibited structural correlates comparable to extant head-striking artiodactyls. These are model-based findings about mechanical capability and anatomical similarity, not direct observations of behavior. **[AI/IN]**
6. **Cranial pathology has been used as independent behavioral evidence, but remains an inference.** Peterson, Dischler & Longrich (2013) reported dome lesions in 22% of sampled pachycephalosaurid specimens and clustering toward the apex; they interpreted this as consistent with intraspecific butting. **[DO + AI]**
7. **The modern literature is broader than a binary “headbutting vs no headbutting” framing.** A 2024/2026 review argues that fossil headbutting has been described with imprecise terminology and stresses that osteological preservation of a dome does not by itself establish the exact behavior or degree of brain protection (Woodruff & Ackermans 2026). A 2026 paper proposes a feeding-performance trade-off associated with the dome (Bateman & Larsson 2026), reinforcing that dome evolution can have multiple interacting functions and constraints. Postcranial myology indicates stabilizing adaptations during axial force transmission (Moore et al. 2022). **[AI + IN]**

### Immediate implications for UALVP 2 FEM

- Treat **geometry, internal architecture, material zoning, load direction, and boundary conditions as separate scientific assumptions** rather than as one generic “model uncertainty.”
- Preserve a distinction between **mechanical competence** and **behavioral inference**.
- Avoid presenting absolute peak stresses as if they were direct measurements of fossil tissue stress; report the tested load case, stress metric, and sensitivity to assumptions.
- Use the prior *Stegoceras* model as a benchmark and provenance target, but do not assume its load case (1360 N benchmark) or material assignment is uniquely correct.
- Make the **ontogenetic status of UALVP 2 explicit** and do not silently generalize from the specimen to all pachycephalosaurs.

---

# 2. UALVP 2 evidence table

| ID | Claim | Evidence type | Source | Direct measurement vs inference | Confidence | Consequence for FEM/UQ |
|---|---|---|---|---|---|---|
| UALVP2-01 | UALVP 2 (*Stegoceras validum*) was collected in 1921 during the University of Alberta field program. | DO | University of Alberta Dino Lab history | Direct historical record | High | Provenance metadata should be retained with geometry/CT files. |
| UALVP2-02 | UALVP 2 is described as the most complete *Stegoceras* specimen available at the time of the University of Alberta historical record. | DO/AI | University of Alberta Dino Lab history | Historical institutional statement | Moderate | Supports use as a principal specimen, but completeness should not be equated with absence of preparation loss or distortion. |
| UALVP2-03 | UALVP 2 comprises a nearly complete skull, both lower jaws, and parts of the postcranial skeleton. | DO | Sullivan 2003 revision; institutional history | Direct specimen description | High | Defines the anatomical scope available for reconstruction. |
| UALVP2-04 | UALVP 2 conforms readily to the *Stegoceras* type frontoparietal and was used as a key basis for understanding the genus. | DO/AI | Sullivan 2003 | Morphological comparison | High | Supports taxonomic assignment used in biomechanical interpretation. |
| UALVP2-05 | UALVP 2 was CT-scanned for biomechanical study. | DO | Snively & Theodor 2011 | Direct methods statement | High | Establishes published CT provenance for comparative modeling. |
| UALVP2-06 | The cranial roof contains a dense superficial/cortical component that increases in thickness/density toward the dome apex. | DO | Snively & Theodor 2011 | CT-derived observation | High | Material zoning should not be treated as spatially uniform without justification. |
| UALVP2-07 | A lower-density trabecular region occurs beneath the dense cortical layer, with trabeculae broadly radiating perpendicular to the dome surface. | DO | Snively & Theodor 2011 | CT-derived observation | High | Internal architecture can affect stiffness, stress path, and energy transfer. |
| UALVP2-08 | A dense deep compact layer is present beneath the more porous region. | DO | Snively & Theodor 2011 | CT-derived observation | High | A simple homogeneous-shell model is a substantive simplification. |
| UALVP2-09 | Numerous canals/vascular traces exit toward the external cranial surface. | DO | Snively & Theodor 2011; Nirody et al. 2022 | CT-derived observation | High | Surface ornamentation/keratin assumptions and local porosity should be distinguished. |
| UALVP2-10 | Beam hardening may inflate apparent superficial density in CT data, although the authors considered the dense deep compact layer secure. | DO/AI | Snively & Theodor 2011 | Imaging limitation explicitly discussed by authors | High | CT-to-material mapping needs calibration and sensitivity analysis. |
| UALVP2-11 | A published FEA model included UALVP 2 and used a 1360 N benchmark impact load. | DO | Snively & Theodor 2011 | Direct model input | High | Provides a literature benchmark load scenario; not evidence that 1360 N is the actual biological force. |
| UALVP2-12 | The 2011 model included bone and keratin tissue types. | DO | Snively & Theodor 2011 | Direct model input | High | Future load/material scenarios should document whether keratin is modeled explicitly or omitted. |
| UALVP2-13 | The 2011 study compared UALVP 2 with extant artiodactyl skulls and *Prenocephale prenes*. | DO | Snively & Theodor 2011 | Direct study design | High | Comparative conclusions provide functional corroboration; not specimen-specific physical validation. |
| UALVP2-14 | UALVP 2 showed structural correlates that the authors associated with head-striking taxa, including dome morphology, surface canals, neck muscle attachments, and layered cranial bone. | DO + AI | Snively & Theodor 2011 | Morphology measured; behavioral meaning inferred | High for anatomy; lower for behavior | Can motivate load scenarios but cannot determine actual behavior. |
| UALVP2-15 | The study reported lower modeled stress and higher safety factors relative to chosen tissue-failure criteria for *Stegoceras* than for several comparison taxa under its chosen loading conditions. | DO/AI | Snively & Theodor 2011 | Model output | High | Comparative outputs are useful benchmarks; transferability to a different load case must be tested. |
| UALVP2-16 | *Stegoceras* dome development varies strongly across ontogeny. | DO/AI | Schott et al. 2011 | Growth-series measurement/modeling | High | Geometry from UALVP 2 should not be generalized to juvenile/subadult morphologies without evidence. |
| UALVP2-17 | Schott et al. found continuous, quantitatively modeled dome growth/variation rather than a simple taxonomic split between flat-headed and domed forms. | DO/AI | Schott et al. 2011 | Statistical/growth modeling | High | Load-bearing geometry is ontogenetically structured. |
| UALVP2-18 | The 2013 pathology study reported lesions on the domes of 22% of sampled pachycephalosaurid specimens and found clustering near the apex. | DO | Peterson, Dischler & Longrich 2013 | Specimen survey + spatial analysis | High | Pathology provides an independent evidence stream for load/impact hypotheses, not a direct force estimate. |
| UALVP2-19 | The authors of the pathology study interpreted lesion distribution as consistent with intraspecific butting behavior. | AI | Peterson, Dischler & Longrich 2013 | Author interpretation | High as an attribution; not established fact | Should not be encoded as a FEM boundary condition or behavioral certainty. |
| UALVP2-20 | A recent review emphasizes ambiguity in the term “headbutting” and cautions against equating cranial integrity with absence of brain injury. | AI | Woodruff & Ackermans 2026 | Review interpretation | High | Interpret mechanical outputs in relation to explicitly defined behaviors and failure criteria. |
| UALVP2-21 | A 2026 study proposed that dome development may impose constraints/trade-offs on jaw adductor geometry and feeding performance. | AI/IN | Bateman & Larsson 2026 | Comparative/functional model | Moderate | Avoid assuming the dome must have had one exclusive function; consider competing biomechanical hypotheses. |
| UALVP2-22 | High-resolution CT demonstrates that frontoparietal dome vascularity in *Stegoceras validum* is concentrated in internal canal networks that diminish ontogenetically. | DO | Nirody et al. 2022 | High-resolution micro-CT quantification | High | Directly constrains internal architecture and warns against treating CT HU as direct bone stiffness. |
| UALVP2-23 | Reconstructed appendicular myology of UALVP 2 indicates adaptations for rotational stabilization and axial ground-reaction force transmission. | IN | Moore et al. 2022 | Comparative myological reconstruction | High as anatomy / Moderate as behavior | Provides postcranial biomechanical context for whole-body stance and impact resistance. |

---

# 3. Annotated bibliography

## P01 — Gilmore (1924)

**Citation:** Gilmore, C. W. (1924). Original description of *Stegoceras validum* / specimen material. Stable bibliographic details require verification against the original monograph/serial record.

**Type:** Primary descriptive paleontology.

**Identifier/URL:** Historical publication; exact stable identifier **UNVERIFIED**.

**Why it matters:** Establishes the early descriptive context for *Stegoceras* and the specimen later central to its functional interpretation.

**Evidence status:** Use for historical specimen identity and morphology; do not use it as evidence for modern CT anatomy or biomechanics.

---

## P02 — Sues & Galton (1987)

**Citation:** Sues, H.-D., & Galton, P. M. (1987). *[Taxonomic/systematic treatment of pachycephalosaurs / Stegoceras; exact title and bibliographic record UNVERIFIED in this pass].*

**Type:** Primary taxonomic/anatomical literature.

**Why it matters:** Important historical step in the interpretation and comparison of *Stegoceras* material.

**Evidence status:** Relevant to taxonomic history and specimen identity; exact title/DOI should be verified before use in a final bibliography.

---

## P03 — Sullivan (2003)

**Citation:** Sullivan, R. M. (2003). Revision of the dinosaur *Stegoceras* Lambe (Ornithischia, Pachycephalosauridae). *Journal of Vertebrate Paleontology*, 23(1), 181–207.

**DOI:** https://doi.org/10.1671/0272-4634(2003)23[181:ROTDSL]2.0.CO;2

**Type:** Peer-reviewed systematic revision.

**Key evidence:** UALVP 2 is described as a nearly complete skull with both lower jaws and parts of the postcranial skeleton. The paper uses UALVP 2 as a principal comparative basis for the genus and demonstrates that the lectotype frontoparietal conforms readily to it. *(Note: Sullivan 2006, New Mexico Museum of Natural History and Science Bulletin 35:347–365, is a distinct family-level taxonomic review).*

**Interpretive value:** Authoritative primary source for specimen identity, completeness, and taxonomic context; not a biomechanical validation study.

---

## P04 — Schott et al. (2011)

**Citation:** Schott, R. K., Evans, D. C., Goodwin, M. B., Horner, J. R., Brown, C. M., & Longrich, N. R. (2011). Cranial ontogeny in *Stegoceras validum* (Dinosauria: Pachycephalosauria): A quantitative model of pachycephalosaur dome growth and variation. *PLOS ONE*, 6(6), e21092.

**DOI:** https://doi.org/10.1371/journal.pone.0021092

**Type:** Peer-reviewed primary research.

**Key finding:** Quantitative growth-series analysis supports strong ontogenetic change and variation in dome morphology.

**Biomechanical relevance:** Geometry cannot be treated as ontogenetically invariant. Comparisons between individuals of different ontogenetic stages can confound geometry with age-related structure.

**Limitation:** This study is not a direct validation of impact FEA and should not be read as evidence for a particular dome behavior.

---

## P05 — Snively & Cox (2008)

**Citation:** Snively, E., & Cox, A. (2008). Structural mechanics of pachycephalosaur crania permitted head-butting behavior. *Palaeontologia Electronica*, 11(1), Article 11.1.3A.

**URL:** https://palaeo-electronica.org/2008_1/140/index.html

**Type:** Primary biomechanical/FEA research.

**Models:** 2-D and 3-D dorsal skull models of adult *Homalocephale* and *Pachycephalosaurus*, plus a model restricted to a subadult pachycephalosaur dome with histological material zones.

**Key findings:** Modeled domes could withstand considerable impact force under some closing-speed assumptions; stresses/strains could dissipate through the dorsal skull; increasing dome vaulting permitted larger modeled impact forces. The authors also found that a trabecular region, where present, did not necessarily function as a rigid compression shield.

**Interpretive boundary:** “Permitted” describes mechanical capability under model assumptions. It does not independently demonstrate the behavior occurred.

---

## P06 — Snively & Theodor (2011)

**Citation:** Snively, E., & Theodor, J. M. (2011). Common functional correlates of head-strike behavior in the pachycephalosaur *Stegoceras validum* (Ornithischia, Dinosauria) and combative artiodactyls. *PLOS ONE*, 6(6), e21422.

**DOI:** https://doi.org/10.1371/journal.pone.0021422

**Type:** Peer-reviewed CT + FEA + comparative biomechanics.

**Models:** CT and physical-section information from ten artiodactyls plus *Stegoceras validum* (UALVP 2) and *Prenocephale prenes*; FEA incorporated bone and keratin tissue types.

**Load benchmark:** The published table includes a 1360 N benchmark load for UALVP 2, derived from a similarly sized *Homalocephale* at 3 m/s closing speed (a comparative scenario, not an observed biological load).

**Key result:** The paper identified anatomical and mechanical correlates shared by *Stegoceras* and extant head-striking taxa and reported lower modeled stress/higher safety factors relative to chosen tissue-failure criteria for *Stegoceras* than several comparison taxa under the chosen conditions.

**Limitation:** The conclusion is explicitly comparative and model-based (comparative functional corroboration). It does not constitute a direct behavioral observation or physical strain-gauge validation.

---

## P07 — Peterson, Dischler & Longrich (2013)

**Citation:** Peterson, J. E., Dischler, C., & Longrich, N. R. (2013). Distributions of cranial pathologies provide evidence for head-butting in dome-headed dinosaurs (Pachycephalosauridae). *PLOS ONE*, 8(7), e68620.

**DOI:** https://doi.org/10.1371/journal.pone.0068620

**Type:** Peer-reviewed pathology/functional morphology study.

**Key observation:** 22% of sampled pachycephalosaurid specimens had dome lesions; lesion distribution clustered near the apex.

**Interpretation:** Authors argued that the distribution was consistent with intraspecific butting matches.

**Limitation:** A lesion records trauma/pathology, not the exact behavior, impact orientation, impact energy, or force magnitude. Causal interpretation remains model-dependent.

---

## P08 — Woodruff & Ackermans (2026)

**Citation:** Woodruff, D. C., & Ackermans, N. L. (2026). Headbutting through time: A review of this hypothesized behavior in “dome-headed” fossil taxa. *The Anatomical Record*, 309(5), 1235–1256. (First published online 4 July 2024).

**DOI:** https://doi.org/10.1002/ar.25526

**Type:** Peer-reviewed review.

**Key contribution:** Reviews the headbutting hypothesis across extinct dome-headed taxa and emphasizes that “headbutting” encompasses diverse contact geometries, angles, and striking mechanics across extant analogs. It also cautions against using osteological deformation alone as a proxy for brain trauma.

**Project relevance:** Mandates defining a family of scenario load cases (contact area, angle, location) rather than a single monolithic "canonical headbutt."

---

## P09 — Bateman & Larsson (2026)

**Citation:** Bateman, L.-P., & Larsson, H. C. E. (2026). On Pachycephalosaurs, Trade-Offs, and the Historical Genesis of Sociosexual Display Structures. *The American Naturalist*, 208(1), 9–29.

**DOI:** https://doi.org/10.1086/740811

**Type:** Peer-reviewed functional/evolutionary study.

**Key idea:** Proposes that the dome can impose spatial constraints on jaw adductor musculature and reduce feeding performance, framing dome evolution in terms of trade-offs as well as display.

**Project relevance:** Adds a functional hypothesis that is not equivalent to impact loading and therefore broadens the set of biological questions a cranial FEM could address.

---

## P10 — Nirody et al. (2022)

**Citation:** Nirody, J. A., Goodwin, M. B., Horner, J. R., Huynh, T. L., Colbert, M. W., Smith, D. K., & Evans, D. C. (2022). Quantifying vascularity in the frontoparietal dome of *Stegoceras validum* (Dinosauria: Pachycephalosauridae) from high resolution CT scans. *Journal of Vertebrate Paleontology*, 41(5), e2036991.

**DOI:** https://doi.org/10.1080/02724634.2021.2036991

**Type:** Peer-reviewed high-resolution micro-CT quantification.

**Key finding:** High-resolution CT directly resolves internal vascular networks in the *Stegoceras validum* dome, showing that vascular canal volume decreases markedly with ontogenetic maturity.

**Project relevance:** Connects 2D histological zonation to 3D CT scan features for *Stegoceras*, directly informing Phase 8 CT thresholding and zonation while warning against treating raw CT HU values as direct bone stiffness.

---

## P11 — Moore et al. (2022)

**Citation:** Moore, B. R. S., Roloson, M. J., Currie, P. J., Ryan, M. J., Patterson, C. M., & Mallon, J. C. (2022). The appendicular myology of *Stegoceras validum* (Ornithischia: Pachycephalosauridae) and implications for the head-butting hypothesis. *PLOS ONE*, 17(9), e0268144.

**DOI:** https://doi.org/10.1371/journal.pone.0268144

**Type:** Peer-reviewed comparative anatomical and myological reconstruction.

**Key finding:** Reconstructed pelvic and hindlimb musculature of UALVP 2 shows adaptations for wide-stance stability and rotational resistance during ground-reaction force transmission.

**Project relevance:** Provides postcranial biomechanical context for whole-body stance and impact resistance without treating head-to-head combat as an observed certainty.

---

# 4. Prior-model reconstruction table

| Study | Taxon/specimen | Geometry | Internal/material model | Loading | Main output | Validation/comparison | Main inference | Important limitation |
|---|---|---|---|---|---|---|---|---|
| Snively & Cox 2008 | *Homalocephale*, *Pachycephalosaurus*; subadult pachycephalosaur dome model | 2-D and 3-D cranial/dome geometries | Histologically informed zones in the subadult model; keratin modeled in some scenarios | Simulated head impacts over selected closing-speed/impact scenarios | Stress, strain, force/energy transmission | Comparative geometry/model cases | Dome geometry could mechanically tolerate/distribute substantial impact loads under modeled conditions | Behavior, exact impact mode, and material properties remain assumption-dependent |
| Snively & Theodor 2011 | *Stegoceras validum* UALVP 2; *Prenocephale*; 10 artiodactyls | CT-derived / CT-informed cranial models | Bone and keratin tissue types; internal density stratification (cancellous E=1 GPa assumed) | Simulated head impacts; UALVP 2 benchmark 1360 N | Cranial stress, strain, safety-factor-type comparisons | Extant artiodactyl analogs + cross-taxon recursive partitioning (comparative functional corroboration; no specimen physical validation) | *Stegoceras* falls within a mechanical/morphological cluster associated with extant head-strikers | Analog selection and loading remain assumptions; comparative capability ≠ observed behavior |
| Peterson, Dischler & Longrich 2013 | Pachycephalosaurid comparative sample | Digital skull mapping for lesion locations | Biological/pathological evidence rather than FEA material model | Not a force simulation | Lesion frequency/distribution | Cross-specimen comparison | Apex-clustered injuries are consistent with intraspecific butting | Exact mechanism/impact orientation not observed |
| Schott et al. 2011 | Growth series of *Stegoceras validum* | 3-D cranial morphology across ontogeny | Growth/shape model rather than impact FEA | Not an impact FEM | Dome growth/variation | Ontogenetic comparative modeling | Dome morphology changes substantially through growth | Ontogeny does not by itself identify behavior |h growth | Ontogeny does not by itself identify behavior |

---

# 5. What CT and histology contribute

## 5.1 CT-derived anatomy of UALVP 2

The 2011 comparative study is especially important because it provides direct internal-structure observations from UALVP 2 rather than inferring internal anatomy solely from exterior morphology. The authors report:

- increasing cortical density/thickness toward the apex;
- a lower-density trabecular region;
- trabeculae oriented approximately perpendicular to the outer dome surface;
- a dense deep compact layer;
- dense tubular structures/canals connecting to the outer surface;
- a caveat that beam hardening can inflate apparent superficial density.

**Biomechanical implication:** these observations support spatially heterogeneous material/architecture models but do not by themselves specify Young's modulus, Poisson's ratio, failure strain, or damping. Those parameters remain model choices unless experimentally constrained.

## 5.2 Histology

The classic histological literature identifies unusual frontoparietal bone architecture in pachycephalosaurs, including fibrolamellar tissue and changing internal tissue organization across ontogeny. Snively & Cox explicitly used histological zones to motivate different material regions in one subadult biomechanical model.

**Important distinction:** histology is evidence about tissue organization and growth/remodeling; it is not a direct measurement of fossil mechanical properties. Converting histology or CT density into FE constitutive parameters requires an additional mapping assumption.

---

# 6. Competing functional hypotheses

| Hypothesis | Evidence used in support | Evidence/arguments that complicate it | FEM/UQ consequence |
|---|---|---|---|
| Head-to-head combat | Dome geometry; CT architecture; extant analogies; comparative FEA; cranial pathology | Exact behavior not observed; 2024 review notes behavioral terminology is underspecified; brain trauma can occur without gross dome deformation | Model explicit head-to-head load cases, but do not encode the behavior as established fact |
| Flank/side impact or shoving/butting | Behavioral analogs among ungulates; some historical interpretations of pachycephalosaur behavior | Different contact geometry and force transmission than head-to-head impact; prior FEA may not span all plausible orientations | Load direction/contact patch should be treated as a scenario variable |
| Sociosexual display / sexual selection | Dome size/shape variation; ontogenetic development; long-standing evolutionary interpretation | Does not explain every mechanical feature uniquely; display and combat functions are not mutually exclusive | Do not limit modeling to impact questions; geometry can also be studied as a display-related developmental trait |
| Species recognition/signaling | Distinctive dome morphology and ontogenetic change | Functional evidence is indirect and often not mechanically quantified | Low-priority FEM hypothesis unless a specific mechanical signaling mechanism is proposed |
| Feeding-performance trade-off / cranial constraint | 2026 evolutionary-functional analysis proposes altered jaw-adductor geometry and reduced feeding performance associated with the dome | Newer hypothesis; not a substitute for the full behavioral literature | Provides a non-impact functional scenario for future comparative biomechanics |
| Protective/energy-dispersive cranial function | Internal stratification; modeled energy dissipation; potential keratin layer | Protective mechanics do not establish why the structure evolved or whether impacts occurred | Report energy/displacement/stress transfer separately from behavioral interpretation |

**Synthesis:** These hypotheses are not necessarily mutually exclusive. A dome could be shaped by sociosexual selection while also possessing mechanical consequences, and a structure capable of resisting impacts need not have evolved primarily for headbutting. **[SYN]**

---

# 7. What prior studies actually establish

### Relatively robust evidence

- UALVP 2 is a key *Stegoceras* specimen with extensive cranial material and established taxonomic relevance. **[DO]**
- Its dome has heterogeneous internal architecture visible by CT. **[DO]**
- *Stegoceras* dome morphology changes during ontogeny. **[DO]**
- Under published model assumptions, the cranium can support and distribute substantial simulated impact loading. **[DO/AI]**
- Cranial pathology exists in pachycephalosaurids and is disproportionately concentrated toward the dome apex in the 2013 dataset. **[DO]**

### More assumption-sensitive interpretations

- Exact impact behavior (head-to-head vs flank/side; repeated combat vs occasional contact). **[IN]**
- Exact force magnitude and loading rate applicable to a living animal. **[MA]**
- Exact material properties of fossil bone, trabecular tissue, keratin, and internal interfaces. **[MA]**
- Extent to which modern ungulate analogs faithfully reproduce pachycephalosaur mechanics. **[IN/MA]**
- Whether successful mechanical impact tolerance demonstrates the evolutionary function of the dome. **[IN]**
- Whether dome pathology necessarily results from the hypothesized behavior. **[IN]**

---

# 8. What newer work changes the picture

## 2024 review of fossil headbutting

Woodruff & Ackermans revisit headbutting across “dome-headed” fossil taxa and explicitly problematize the use of the single word “headbutting.” Their review also emphasizes that the brain can be injured without obvious failure of the overlying cranial bone.

**Project consequence:** UALVP 2 FEA should define the mechanical event being simulated (contact orientation, force/impulse, support conditions, rate if modeled) rather than labeling a whole family of scenarios “headbutting.”

## 2026 feeding-performance trade-off hypothesis

Bateman & Larsson examine pachycephalosaur domes as sociosexual display structures while considering a biomechanical cost: reduced space/altered geometry for jaw adductors and consequent feeding-performance trade-offs.

**Project consequence:** the literature now more clearly supports treating the dome as a multifunctional evolutionary structure rather than assuming that all biomechanical questions are impact questions.

---

# 9. UALVP 2 consequences for the current project

| Literature issue | Current Phase 4 FEM | Mesh convergence | Geometry pipeline | Load-case design | Material assumptions | Future UQ | Scientific interpretation |
|---|---|---|---|---|---|---|---|
| UALVP 2 specimen provenance | **Required** | — | **Required** | — | — | **Track as metadata** | Scope claims to specimen |
| CT heterogeneity | **Required assumption audit** | — | **High** | — | **High** | **High** | Do not imply homogeneous fossil bone without sensitivity testing |
| Beam-hardening / CT-density mapping | **Document** | — | **High** | — | **High** | **High** | Separate imaging uncertainty from constitutive uncertainty |
| Ontogenetic variation | **Required** | — | **High** | **Moderate** | **Moderate** | **High** | Avoid population-wide generalization |
| Published 1360 N benchmark | **Useful reference case** | — | — | **High** | **High** | **High** | Treat as literature benchmark, not measured animal force |
| Force direction/contact mode | **Scenario definition required** | — | **Moderate** | **Very high** | **High** | **Very high** | Compare plausible orientations rather than one unqualified load case |
| Pathology evidence | — | — | — | **High conceptual relevance** | — | **Moderate** | Can motivate scenarios but cannot specify forces |
| Extant analogies | — | — | — | **High** | **Moderate** | **High** | Document analogy selection explicitly |
| Competing non-impact functions | — | — | **High** | **Moderate** | **Moderate** | **High** | Avoid single-function evolutionary interpretation |

---

# 10. Recommended evidence hierarchy for UALVP 2 interpretation

1. **Specimen-level direct observations:** CT anatomy, measured geometry, preservation/preparation state, visible pathology.
2. **Published *Stegoceras* comparative evidence:** ontogeny and prior UALVP 2 modeling.
3. **Pachycephalosaur-wide evidence:** histology, pathology, comparative morphology.
4. **Extant biomechanical analogies:** useful for generating hypotheses and plausible parameter ranges, not as direct measurements of extinct behavior.
5. **Behavioral synthesis:** lowest direct evidentiary level; must explicitly retain the chain from anatomy → mechanics → behavior.

---

# 11. Open questions / evidence gaps

### OQ-U01 — Exact ontogenetic status of UALVP 2
The specimen is morphologically advanced and has been central to adult *Stegoceras* comparisons, but a single independent age estimate should not be assumed without a source that actually measures it.

### OQ-U02 — Fossil-specific constitutive properties
The literature provides anatomical and histological guidance, but direct fossil-tissue elastic properties appropriate to UALVP 2 are not established by the sources reviewed here.

### OQ-U03 — Realistic impact loading history
Published 1360 N loading in the 2011 study is a model benchmark. The force-time history, contact mechanics, and behavioral frequency of actual impacts remain uncertain.

### OQ-U04 — Load direction and contact geometry
Head-to-head, angled impact, flank impact, and shoving produce different stress paths. This is a prime target for scenario-based sensitivity analysis.

### OQ-U05 — Boundary-condition sensitivity for the fossil cranium
Neck support and skull fixation are inferred rather than observed. Published FEA does not eliminate this uncertainty.

### OQ-U06 — Keratin pad thickness/properties
Surface canals provide anatomical motivation for a keratinous covering, but its exact thickness/material response is uncertain.

### OQ-U07 — Brain injury inference
Structural stress in cranial bone is not equivalent to neural injury. The 2024 review reinforces this distinction.

### OQ-U08 — Multi-function evolution
Current evidence permits several non-exclusive functions; a single-function evolutionary conclusion is not required for a useful mechanics study.

---

# 12. Candidate contributions — TO VERIFY

These are **candidate** claims only and must be verified against a broader literature search before any novelty statement is made:

- A specimen-specific, reproducible UALVP 2 geometry/mesh pipeline with explicit mesh-convergence evidence may fill a reporting gap in prior *Stegoceras* biomechanics.
- A systematic decomposition of uncertainty into geometry/segmentation, material properties, force magnitude, force direction, and boundary conditions may provide a clearer uncertainty framework than the largely deterministic classic studies.
- A directly comparable set of load cases run through the same frozen geometry and mesh pipeline may help separate biological uncertainty from numerical uncertainty.
- Global sensitivity/UQ applied to a fossil cranial FE model may extend methods already established in adjacent biomechanics, but fossil-specific precedent must be verified before claiming novelty.

**Novelty status for all four: `TO VERIFY`.**

---

# 13. Source URLs / identifiers

- University of Alberta Dino Lab history: https://grad.biology.ualberta.ca/dino-lab/history/
- Sullivan 2003: https://doi.org/10.1671/0272-4634(2003)23[181:ROTDSL]2.0.CO;2
- Sullivan 2006: https://econtent.unm.edu/digital/collection/bulletins/id/1119/
- Schott et al. 2011: https://doi.org/10.1371/journal.pone.0021092
- Snively & Cox 2008: https://palaeo-electronica.org/2008_1/140/index.html
- Snively & Theodor 2011: https://doi.org/10.1371/journal.pone.0021422
- Peterson, Dischler & Longrich 2013: https://doi.org/10.1371/journal.pone.0068620
- Nirody et al. 2022: https://doi.org/10.1080/02724634.2021.2036991
- Moore et al. 2022: https://doi.org/10.1371/journal.pone.0268144
- Woodruff & Ackermans 2026: https://doi.org/10.1002/ar.25526
- Bateman & Larsson 2026: https://doi.org/10.1086/740811

---

# 14. Review provenance note

This module was constructed from primary papers and authoritative institutional material retrieved during the current review pass. Details not directly recoverable from an authoritative source were intentionally marked **UNVERIFIED** rather than reconstructed from memory. The dossier is a working evidence product, not a final narrative review chapter.

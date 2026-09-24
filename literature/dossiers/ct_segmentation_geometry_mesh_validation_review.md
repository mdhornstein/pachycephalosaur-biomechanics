# CT / Segmentation / Geometry / Mesh / Validation — Literature Review Management
> Evidence-base module for the Stegoceras validum UALVP 2 project. Search/update date: 2026-09-24.
> This is a scoping/evidence module, not a final literature-review chapter. It separates direct observations (DO), author interpretations (AI), model assumptions (MA), and reviewer/project synthesis (SYN). `UNVERIFIED` marks details not sufficiently checked in the current pass.

## Executive findings
1. **The imaging-to-FEA pipeline is itself part of the model.** CT acquisition, segmentation, digital repair, surface generation, surface resolution, volume meshing, element formulation, and solver settings can each change the numerical result. The literature does not justify treating mesh generation as a neutral last step. [S01, S02, S10, S17, S18]
2. **Segmentation and geometry deserve explicit sensitivity treatment in fossils.** Modern validation/sensitivity studies show that simplifications can leave global deformation patterns comparatively stable while altering local strain magnitudes, and the 2025 *Jeholosaurus* study shows fossil-specific stress fields can change when rock matrix is removed from intertrabecular spaces. [S08, S09, S15]
3. **Mesh convergence should isolate discretization effects.** For UALVP 2, a formal mesh-convergence study should keep geometry, segmentation, repair/regularization, material mapping, loads, BCs, element formulation and solver settings fixed while refining the tetrahedral discretization. Changing the geometry branch or meshing algorithm is a different experiment and should be called geometry/mesh-method sensitivity or model-form sensitivity, not pure mesh convergence. [S03, S05, S06, S10, S16]
4. **Convergence is output-specific.** A mesh can be converged for energy or displacement while local peak stress remains mesh-sensitive. Primary project outputs should therefore be monitored separately, with local stress summaries defined in a way that is spatially repeatable and not dominated by singular or highly localized numerical artifacts. [S06, S16, S19]
5. **Watertight and topologically valid surfaces are a precondition, not a convergence result.** The cited fossil workflow explicitly requires a closed watertight surface without self-intersections/non-manifold edges for reliable tetrahedralization, while image-based meshing reviews emphasize that poor boundary geometry propagates into poor tetrahedral meshes. [S13, S18]
6. **Modern fossil segmentation is moving toward hybrid/manual + deep-learning workflows, but AI segmentation should not be treated as ground truth.** The 2024 fossil segmentation study reported a validation Dice of 0.96 and emphasized CT artifacts and fossil-matrix contrast as persistent failure modes; the 2025 *Jeholosaurus* FE study still required manual correction and manual repair of a major fissure. [S14, S15]

## 1. Imaging-to-FEM evidence matrix

| ID | Source | Evidence domain | Core observation | UALVP 2 use |
|---|---|---|---|---|
| S02 | Taddei, F., Martelli, S., Reggiani, B., Cristofolini, L., & Viceconti, M (2006) | CT-to-FEA sensitivity | Input influence depends on the load case and the output variable. | Supports treating geometry/segmentation and material assignment as separate uncertainty sources, not collapsing them into one 'mesh' parameter. |
| S03 | Viceconti, M., Bellingeri, L., Cristofolini, L., & Toni, A (1998) | mesh-generation methods | Different mesh generators have different accuracy, effort and computational tradeoffs; no single method dominates every situation. | Supports calling different meshing algorithms a 'mesh-generation method comparison' rather than a pure mesh-convergence test. |
| S04 | Camacho, D. L. A., Hopper, R. H., Lin, G. M., & Myers, B. S (1997) | CT-to-mesh | Smoothing can reduce surface stress oscillations in CT-derived FE models, but smoothing itself is a modeling intervention that can alter geometry. | Supports documenting smoothing/regularization parameters explicitly and distinguishing geometric regularization from discretization refinement. |
| S05 | Anderson, A. E., Ellis, B. J., & Weiss, J. A (2007) | verification/validation | Mesh convergence reduces numerical discretization uncertainty but does not establish physical validity. | Supports a clean Phase 4 separation of implementation verification, mesh verification, validation evidence and sensitivity. |
| S06 | Bright, J. A., & Rayfield, E. J (2011) | cranial mesh convergence | Mesh convergence should be performed before biological interpretation; graphical hotspot appearance can change with mesh density. | Direct precedent for a controlled h-refinement ladder on a fixed UALVP 2 geometry/model pipeline. |
| S08 | Fitton, L. C., Prôa, M., Rowland, C., Toro-Ibacache, V., & O'Higgins, P (2014) | segmentation/geometry sensitivity | Large-scale deformation modes were comparatively stable across simplifications, while localized strain magnitudes could change, especially near alveolar regions. | Supports separating global structural outputs from local stress hotspots when judging robustness to geometry simplification. |
| S09 | Toro-Ibacache, V., Fitton, L. C., Fagan, M. J., & O'Higgins, P (2015) | cranial validation/geometry | Absolute deformations were not accurately predicted in validation, whereas spatial distribution of relatively high/low strain and global deformation modes were better approximated. | Strong support for interpreting absolute local stress/strain values cautiously and emphasizing robust patterns/relative comparisons where validation is unavailable. |
| S10 | McCurry, M. R., Evans, A. R., & McHenry, C. R (2015) | surface geometry resolution | Input surface resolution is distinct from volume-mesh resolution and can influence FE outputs. | Strong argument for fixing geometry-generation pipeline during mesh-convergence and testing geometry/surface-resolution sensitivity separately. |
| S11 | Zollikofer, C. P. E. et al. / Lautenschlager-linked digital restoration literature. See: Gunz et al (2016) | fossil digital restoration | Digital restoration is often necessary for functional modeling, but restorative operations are interpretive and should be documented. | Supports retaining an immutable pre-repair geometry and recording each repair/regularization operation, with rationale and affected region. |
| S13 | Chatar, M., et al (2023) | fossil FE workflow | A watertight, topologically valid surface is a prerequisite for reliable tetrahedralization. | Directly supports documenting surface-topology checks and mesh-generation settings before FE solution. |
| S14 | Knutsen, E. M., & Konovalov, D. A (2024) | fossil segmentation AI | Deep learning can substantially reduce manual segmentation effort while retaining high segmentation agreement, but data-specific ambiguity remains. | Supports considering automated segmentation as a reproducibility aid, but not as an assumed ground truth; manual QA remains necessary. |
| S15 | Zhang, L., Cao, Z., & Zhao, Q (2025) | fossil CT segmentation + FEA | Removing matrix from intertrabecular spaces changed stress patterns and increased maximum stress in the example; authors argue segmented results better tracked trabecular architecture. | Very strong recent precedent that segmentation strategy can alter FE stress fields in fossil bone; supports explicit segmentation sensitivity or defensible rationale for treating matrix/trabecular spaces. |
| S16 | Follet, H., et al (2024) | segmentation sensitivity adjacent biomechanics | Failure-load outputs were comparable between automatic and expert manual segmentations in tested models, but sensitivity to small segmentation differences was still assessed. | Adjacent precedent for treating segmentation variability as a quantitative sensitivity factor rather than only a visual QC issue. |
| S17 | Erdemir, A., Guess, T. M., Halloran, J., Tadepalli, S. C., & Morrison, T. M (2011) | reproducibility | Transparent reporting improves reproducibility, reusability and model exchange. | Provides the backbone for a UALVP 2 reproducibility checklist. |
| S18 | Schaer, R. et al (2020) | image-based meshing | Mesh quality is coupled to the quality of the boundary representation and the meshing algorithm. | Supports checking surface quality before TetGen rather than assuming TetGen can fully repair poor geometry. |
| S19 | Tetrahedral microFE models of human trabecular bone can be a valid alternative to voxel-based hexahedral models: A comparative study using an open-source workflow. Journal of the Mechanical Behavior of Biomedical Materials, 176, 107326. (2026) | 2026 mesh/material comparison | Global apparent modulus could remain accurate across model choices while local stress/strain outcomes varied more strongly; mesh type and resolution matter for local fields. | Useful recent evidence that 'same global output' does not imply same local stress field; motivates multi-output convergence and cautious local stress interpretation. |

## 2. Source annotations

### [S01] Rayfield, E. J. (2007). Finite Element Analysis and Understanding the Biomechanics and Evolution of Living and Fossil Organisms. Annual Review of Earth and Planetary Sciences, 35, 541–576.
- DOI: `10.1146/annurev.earth.35.031306.140104`
- URL: https://www.annualreviews.org/doi/10.1146/annurev.earth.35.031306.140104
- Publication type: `peer_reviewed_review`
- Geometry: Digital reconstructions commonly derived from CT/3D morphology; emphasizes reconstruction choices as part of FEA.
- Segmentation: UNVERIFIED in source excerpt; review-level discussion.
- Repair / regularization: UNVERIFIED; review-level.
- Surface geometry: UNVERIFIED
- Volume mesh: FE discretization; element choice and mesh resolution recognized as modeling issues.
- Mesh QC: UNVERIFIED
- Convergence: Early methodological context; later work strengthened explicit convergence requirements.
- Sensitivity: Model assumptions in fossil FEA broadly discussed.
- Principal finding: FEA can address morphology-function-evolution questions but depends on assumptions about geometry, materials, loading and constraints.
- Limitation: Review-level synthesis; not a specimen-specific validation study.
- UALVP 2 implication: Frames the entire imaging-to-FEA chain as part of the model, not just the solver.
- Verification status: `verified_at_review_level`

### [S02] Taddei, F., Martelli, S., Reggiani, B., Cristofolini, L., & Viceconti, M. (2006). Finite-element modeling of bones from CT data: sensitivity to geometry and material uncertainties. IEEE Transactions on Biomedical Engineering, 53(11), 2194–2200.
- DOI: `10.1109/TBME.2006.879473`
- URL: https://doi.org/10.1109/TBME.2006.879473
- Publication type: `peer_reviewed_primary`
- Geometry: CT-derived femur models; geometry, density and material properties treated as uncertain inputs.
- Segmentation: Segmentation errors explicitly estimated as an input uncertainty.
- Repair / regularization: UNVERIFIED
- Surface geometry: UNVERIFIED
- Volume mesh: CT-derived FE models; exact element type not verified here.
- Mesh QC: UNVERIFIED
- Convergence: UNVERIFIED
- Sensitivity: Monte Carlo sensitivity to geometry, density and mechanical properties under two loading conditions.
- Principal finding: Input influence depends on the load case and the output variable.
- Limitation: Human femur rather than fossil; simplified loading; not a skull model.
- UALVP 2 implication: Supports treating geometry/segmentation and material assignment as separate uncertainty sources, not collapsing them into one 'mesh' parameter.
- Verification status: `verified_from_abstract_metadata`

### [S03] Viceconti, M., Bellingeri, L., Cristofolini, L., & Toni, A. (1998). A comparative study on different methods of automatic mesh generation of human femurs. Medical Engineering & Physics, 20(1), 1–10.
- DOI: `10.1016/S1350-4533(97)00049-0`
- URL: https://doi.org/10.1016/S1350-4533(97)00049-0
- Publication type: `peer_reviewed_primary`
- Geometry: Standardized human femur geometry and simplified reference geometry.
- Segmentation: Voxel-based method can bypass explicit geometry extraction; other methods require solid/surface models.
- Repair / regularization: UNVERIFIED
- Surface geometry: Surface-based tetra/hexa/mapped approaches compared.
- Volume mesh: Mapped, tetrahedral, voxel and hexahedral automatic mesh generation compared.
- Mesh QC: Accuracy assessed against analytical and experimental references.
- Convergence: Method comparison included accuracy and effort, not a single universal convergence criterion.
- Sensitivity: Sensitivity here is to mesh-generation method/representation.
- Principal finding: Different mesh generators have different accuracy, effort and computational tradeoffs; no single method dominates every situation.
- Limitation: Human femur; not fossil skull; older meshing technology.
- UALVP 2 implication: Supports calling different meshing algorithms a 'mesh-generation method comparison' rather than a pure mesh-convergence test.
- Verification status: `verified_from_abstract`

### [S04] Camacho, D. L. A., Hopper, R. H., Lin, G. M., & Myers, B. S. (1997). An improved method for finite element mesh generation of geometrically complex structures with application to the skullbase. Journal of Biomechanics, 30(10), 1067–1070.
- DOI: `10.1016/S0021-9290(97)00073-0`
- URL: https://doi.org/10.1016/S0021-9290(97)00073-0
- Publication type: `peer_reviewed_primary`
- Geometry: CT-based complex geometry including human skull base.
- Segmentation: Image-based reconstruction; details of segmentation not verified here.
- Repair / regularization: Surface smoothing was part of the proposed workflow.
- Surface geometry: Compared smoothed vs unsmoothed surfaces and showed reduced surface stress oscillation after smoothing.
- Volume mesh: Automated hexahedral mesh generation from CT images.
- Mesh QC: Surface stress error/oscillation used to assess mesh quality.
- Convergence: Evaluated across mesh densities.
- Sensitivity: Surface smoothing and mesh density affected numerical stress behavior.
- Principal finding: Smoothing can reduce surface stress oscillations in CT-derived FE models, but smoothing itself is a modeling intervention that can alter geometry.
- Limitation: Engineering/skull-base context rather than fossil biomechanics; hexahedral rather than tetrahedral.
- UALVP 2 implication: Supports documenting smoothing/regularization parameters explicitly and distinguishing geometric regularization from discretization refinement.
- Verification status: `verified_from_abstract`

### [S05] Anderson, A. E., Ellis, B. J., & Weiss, J. A. (2007). Verification, validation and sensitivity studies in computational biomechanics. Computer Methods in Biomechanics and Biomedical Engineering, 10(3), 171–184.
- DOI: `10.1080/10255840601160484`
- URL: https://doi.org/10.1080/10255840601160484
- Publication type: `peer_reviewed_review`
- Geometry: Model-specific.
- Segmentation: Model-specific.
- Repair / regularization: Model-specific.
- Surface geometry: Model-specific.
- Volume mesh: Mesh refinement is required to address spatial discretization error.
- Mesh QC: Model verification should include convergence checks and known-solution comparisons where available.
- Convergence: Refine until quantities of interest asymptote; validation-relevant output should drive mesh choice.
- Sensitivity: Sensitivity should be used to identify influential model inputs.
- Principal finding: Mesh convergence reduces numerical discretization uncertainty but does not establish physical validity.
- Limitation: General computational biomechanics; not fossil-specific.
- UALVP 2 implication: Supports a clean Phase 4 separation of implementation verification, mesh verification, validation evidence and sensitivity.
- Verification status: `verified_from_review`

### [S06] Bright, J. A., & Rayfield, E. J. (2011). The response of cranial biomechanical finite element models to variations in mesh density. The Anatomical Record, 294(4), 610–620.
- DOI: `10.1002/ar.21358`
- URL: https://doi.org/10.1002/ar.21358
- Publication type: `peer_reviewed_primary`
- Geometry: CT-derived domestic pig skull held as the underlying model while meshes were increasingly refined.
- Segmentation: CT-based skull reconstruction.
- Repair / regularization: UNVERIFIED
- Surface geometry: Underlying CT-derived geometry.
- Volume mesh: 18 increasingly refined FE models; linear and quadratic tetrahedra.
- Mesh QC: Convergence examined for strain and displacement.
- Convergence: Not all skull regions converged at the same rate; insufficiently dense models underestimated strain/displacement and missed high-strain hotspots.
- Sensitivity: Strong sensitivity to mesh density, including regional differences.
- Principal finding: Mesh convergence should be performed before biological interpretation; graphical hotspot appearance can change with mesh density.
- Limitation: Extant pig skull rather than fossil.
- UALVP 2 implication: Direct precedent for a controlled h-refinement ladder on a fixed UALVP 2 geometry/model pipeline.
- Verification status: `verified_from_abstract_and_metadata`

### [S07] Bright, J. A., & Rayfield, E. J. (2011). Sensitivity and ex vivo validation of finite element models of the domestic pig cranium. Journal of Anatomy, 219(4), 456–471.
- DOI: `10.1111/j.1469-7580.2011.01408.x`
- URL: https://doi.org/10.1111/j.1469-7580.2011.01408.x
- Publication type: `peer_reviewed_primary`
- Geometry: Specimen-specific cranium from CT.
- Segmentation: CT-derived anatomy; model simplifications investigated.
- Repair / regularization: UNVERIFIED
- Surface geometry: Specimen-specific.
- Volume mesh: FE cranium; exact mesh details not fully verified in this pass.
- Mesh QC: UNVERIFIED
- Convergence: Not the primary focus.
- Sensitivity: Material heterogeneity, loading direction, strain-gauge placement and output mapping.
- Principal finding: Models reproduced loading conditions but could miss principal strain magnitudes/ratios at some locations; absolute numerical agreement is limited.
- Limitation: Extant pig and ex vivo validation; measurement/model mapping issues.
- UALVP 2 implication: Reinforces reporting of load direction and exact locations/definitions of local outputs, not just global stress maps.
- Verification status: `verified_from_abstract`

### [S08] Fitton, L. C., Prôa, M., Rowland, C., Toro-Ibacache, V., & O'Higgins, P. (2015). The impact of simplifications on the performance of a finite element model of a Macaca fascicularis cranium. The Anatomical Record, 298(1), 107–121.
- DOI: `10.1002/ar.23075`
- URL: https://doi.org/10.1002/ar.23075
- Publication type: `peer_reviewed_primary`
- Geometry: Human-scale primate cranium; model simplifications varied.
- Segmentation: Detail of segmentation and material representation of teeth were varied.
- Repair / regularization: UNVERIFIED
- Surface geometry: Simplified models used to probe geometry effects.
- Volume mesh: FE cranium; exact element formulation not verified here.
- Mesh QC: UNVERIFIED
- Convergence: Not primary focus.
- Sensitivity: Segmentation detail and tooth material properties.
- Principal finding: Large-scale deformation modes were comparatively stable across simplifications, while localized strain magnitudes could change, especially near alveolar regions.
- Limitation: Modern macaque; comparative biting rather than fossil impact.
- UALVP 2 implication: Supports separating global structural outputs from local stress hotspots when judging robustness to geometry simplification.
- Verification status: `verified_from_abstract`

### [S09] Toro-Ibacache, V., Fitton, L. C., Fagan, M. J., & O'Higgins, P. (2015). Validity and sensitivity of a human cranial finite element model: implications for comparative studies of biting performance. Journal of Anatomy, 228(1), 70–84.
- DOI: `10.1111/joa.12384`
- URL: https://doi.org/10.1111/joa.12384
- Publication type: `peer_reviewed_primary`
- Geometry: Adult human male cranium; geometry detail deliberately simplified in multiple model versions.
- Segmentation: Variations in geometric detail including cancellous-bone representation.
- Repair / regularization: UNVERIFIED
- Surface geometry: Geometry detail varied according to voxel/model resolution.
- Volume mesh: Voxel-based FE models of the same cranium.
- Mesh QC: UNVERIFIED
- Convergence: Not primary focus.
- Sensitivity: Geometry simplification and material representation.
- Principal finding: Absolute deformations were not accurately predicted in validation, whereas spatial distribution of relatively high/low strain and global deformation modes were better approximated.
- Limitation: Human cadaver cranium; model class differs from fossil impact biomechanics.
- UALVP 2 implication: Strong support for interpreting absolute local stress/strain values cautiously and emphasizing robust patterns/relative comparisons where validation is unavailable.
- Verification status: `verified_from_abstract`

### [S10] McCurry, M. R., Evans, A. R., & McHenry, C. R. (2015). The sensitivity of biological finite element models to the resolution of surface geometry: a case study of crocodilian crania. PeerJ, 3, e988.
- DOI: `10.7717/peerj.988`
- URL: https://doi.org/10.7717/peerj.988
- Publication type: `peer_reviewed_primary`
- Geometry: Seven high-resolution crocodilian cranial surface meshes were down-sampled to varying resolutions.
- Segmentation: Starting geometry from high-resolution 3D surfaces.
- Repair / regularization: UNVERIFIED
- Surface geometry: Primary manipulated variable; surface resolution changed while solid element count was held constant.
- Volume mesh: Solid FE meshes held at comparable element counts across surface-resolution treatments.
- Mesh QC: UNVERIFIED
- Convergence: Not pure h-convergence; tests geometry-resolution sensitivity.
- Sensitivity: Surface mesh resolution caused fluctuations in strain magnitude; stable comparative results were possible at lower surface resolution.
- Principal finding: Input surface resolution is distinct from volume-mesh resolution and can influence FE outputs.
- Limitation: Crocodilian crania; comparative rather than fossil-specific.
- UALVP 2 implication: Strong argument for fixing geometry-generation pipeline during mesh-convergence and testing geometry/surface-resolution sensitivity separately.
- Verification status: `verified_from_abstract`

### [S11] Zollikofer, C. P. E. et al. / Lautenschlager-linked digital restoration literature. See: Gunz et al. (2009) and Lautenschlager (2016/2017) for virtual fossil restoration methods; this record is represented here by Lautenschlager, S. (2016). Reconstructing the past: methods and techniques for the digital restoration of fossils.
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC5098973/
- Publication type: `peer_reviewed_review`
- Geometry: Fossils often require virtual restoration because of breaks, cracks, distortion, missing or displaced elements.
- Segmentation: CT segmentation can include hole filling, grow/shrink operations and manual interpolation across cracks.
- Repair / regularization: Digital repair methods can be automatic or manual; manual repair introduces interpretation.
- Surface geometry: Remeshing can reduce surface complexity but changes the representation.
- Volume mesh: FEA/CFD downstream studies require complete/accurate morphology; reconstruction decisions propagate into functional inference.
- Mesh QC: UNVERIFIED in this review.
- Convergence: Not primary focus.
- Sensitivity: Restoration choices can introduce uncertainty/interpretation.
- Principal finding: Digital restoration is often necessary for functional modeling, but restorative operations are interpretive and should be documented.
- Limitation: Review spans virtual paleontology, not only FEA.
- UALVP 2 implication: Supports retaining an immutable pre-repair geometry and recording each repair/regularization operation, with rationale and affected region.
- Verification status: `verified_from_review`

### [S12] Lautenschlager, S. (2017). From bone to pixel—fossil restoration and reconstruction with digital techniques. Geology Today, 33, 155–159.
- DOI: `10.1111/gto.12194`
- URL: https://doi.org/10.1111/gto.12194
- Publication type: `peer_reviewed_review`
- Geometry: Digital fossil morphology needs restoration because fossilization alters morphology.
- Segmentation: Discusses digital restoration/segmentation at a high level.
- Repair / regularization: Restoration required before some downstream analyses.
- Surface geometry: UNVERIFIED
- Volume mesh: UNVERIFIED
- Mesh QC: UNVERIFIED
- Convergence: UNVERIFIED
- Sensitivity: Restoration quality can affect downstream analysis.
- Principal finding: Digital restoration is an integral part of interpreting fossil morphology, not merely cosmetic preprocessing.
- Limitation: Short review; little numerical FEA detail.
- UALVP 2 implication: Supports versioning original, cleaned and FE-ready geometry as distinct model states.
- Verification status: `verified_from_metadata_and_abstract`

### [S13] Chatar, M., et al. (2023). 'Fossils': A new, fast and open-source protocol to simulate muscle-driven biomechanical loading of bone. Methods in Ecology and Evolution.
- DOI: `10.1111/2041-210X.14051`
- URL: https://doi.org/10.1111/2041-210X.14051
- Publication type: `peer_reviewed_method`
- Geometry: Fossil bone surface meshes used as FE input.
- Segmentation: Upstream digital model assumed; protocol emphasizes FE preparation.
- Repair / regularization: Requires repair sufficient to produce a clean, usable surface.
- Surface geometry: Surface must be watertight, closed, non-self-intersecting and non-manifold; triangle size/aspect ratio matter.
- Volume mesh: Protocol uses tetrahedral meshing; example uses Gmsh, with support for TetGen and other meshers.
- Mesh QC: Element/triangle quality is recognized as important; exact acceptance thresholds vary by application.
- Convergence: Not the main study objective.
- Sensitivity: Workflow is designed to reduce barriers and improve reproducibility.
- Principal finding: A watertight, topologically valid surface is a prerequisite for reliable tetrahedralization.
- Limitation: Protocol/method paper; muscle-driven loading is broader than UALVP 2 impact.
- UALVP 2 implication: Directly supports documenting surface-topology checks and mesh-generation settings before FE solution.
- Verification status: `verified_from_article`

### [S14] Knutsen, E. M., & Konovalov, D. A. (2024). Accelerating segmentation of fossil CT scans through Deep Learning. Scientific Reports, 14, 20943.
- DOI: `10.1038/s41598-024-71245-1`
- URL: https://doi.org/10.1038/s41598-024-71245-1
- Publication type: `peer_reviewed_primary`
- Geometry: Fossil CT volume from a small vertebrate fossil in rock matrix.
- Segmentation: UNet deep-learning segmentation trained with a small manually segmented subset; final validation Dice reported as 0.96.
- Repair / regularization: Minor manual correction remained necessary.
- Surface geometry: 3D meshes generated from predicted ROIs; details of final FE suitability not primary objective.
- Volume mesh: Not an FE study.
- Mesh QC: Not applicable.
- Convergence: Not applicable.
- Sensitivity: Segmentation performance affected by artifacts, fossil/matrix contrast, cortical erosion and rapid anatomical changes across slices.
- Principal finding: Deep learning can substantially reduce manual segmentation effort while retaining high segmentation agreement, but data-specific ambiguity remains.
- Limitation: Segmentation workflow rather than FE validation; transferability across scans is not guaranteed.
- UALVP 2 implication: Supports considering automated segmentation as a reproducibility aid, but not as an assumed ground truth; manual QA remains necessary.
- Verification status: `verified_from_article`

### [S15] Zhang, L., Cao, Z., & Zhao, Q. (2025). Deep learning-aided segmentation combined with finite element analysis reveals a more natural biomechanic of dinosaur fossil. Scientific Reports, 15, 13964.
- DOI: `10.1038/s41598-025-99131-4`
- URL: https://doi.org/10.1038/s41598-025-99131-4
- Publication type: `peer_reviewed_primary`
- Geometry: Jeholosaurus femur IVPP V 15939 from micro-CT; 36.665 μm voxel size reported.
- Segmentation: 2.5D UNet segmentation of air/rock, cortical and trabecular bone; iterative training with Dice improvement; independent slice check.
- Repair / regularization: Major fissure manually realigned before biomechanics.
- Surface geometry: Porous segmented surface increased mesh-processing error risk; overlapping/intersecting triangles and inverted normals noted.
- Volume mesh: Mesh described at roughly 997,282 units and 1,338,945 nodes; millimeter-scale element size reported.
- Mesh QC: Topology errors were discussed qualitatively; no external physical validation was provided.
- Convergence: Not presented as a formal mesh-convergence study.
- Sensitivity: Primary comparison was segmented versus unrefined/unsegmented fossil representation.
- Principal finding: Removing matrix from intertrabecular spaces changed stress patterns and increased maximum stress in the example; authors argue segmented results better tracked trabecular architecture.
- Limitation: Single specimen, one taxon, no experimental validation; grayscale-to-material mapping and 30-layer stratification are additional assumptions.
- UALVP 2 implication: Very strong recent precedent that segmentation strategy can alter FE stress fields in fossil bone; supports explicit segmentation sensitivity or defensible rationale for treating matrix/trabecular spaces.
- Verification status: `verified_from_article`

### [S16] Follet, H., et al. (2024). Finite element models with automatic computed tomography bone segmentation for failure load computation. Scientific Reports, 14, 16576.
- DOI: `10.1038/s41598-024-66934-w`
- URL: https://doi.org/10.1038/s41598-024-66934-w
- Publication type: `peer_reviewed_primary`
- Geometry: Human femora and vertebrae from CT.
- Segmentation: Automatic deep-learning versus expert manual segmentation; sensitivity to small automatic-segmentation variations tested.
- Repair / regularization: Post-processing included in workflow; exact fossil relevance none.
- Surface geometry: Clinical CT geometry.
- Volume mesh: FE models for failure-load prediction.
- Mesh QC: UNVERIFIED in abstract.
- Convergence: UNVERIFIED
- Sensitivity: Segmentation choice and perturbations.
- Principal finding: Failure-load outputs were comparable between automatic and expert manual segmentations in tested models, but sensitivity to small segmentation differences was still assessed.
- Limitation: Modern clinical bone, not fossil; loading/endpoint differs.
- UALVP 2 implication: Adjacent precedent for treating segmentation variability as a quantitative sensitivity factor rather than only a visual QC issue.
- Verification status: `verified_from_abstract`

### [S17] Erdemir, A., Guess, T. M., Halloran, J., Tadepalli, S. C., & Morrison, T. M. (2012). Considerations for reporting finite element analysis studies in biomechanics. Journal of Biomechanics, 45(4), 625–633.
- DOI: `10.1016/j.jbiomech.2011.11.038`
- URL: https://doi.org/10.1016/j.jbiomech.2011.11.038
- Publication type: `peer_reviewed_reporting_guidance`
- Geometry: Report model identification and structure, including geometry source and assumptions.
- Segmentation: Not fossil-specific, but reporting of preprocessing/model structure is encouraged.
- Repair / regularization: Report model-generation decisions and any custom processing.
- Surface geometry: Report geometry-processing choices where they affect model structure.
- Volume mesh: Report mesh convergence variables and whether they represent overall or regional outputs.
- Mesh QC: Report verification analyses and numerical settings.
- Convergence: Primary outputs should be used when possible; if a proxy output is used, its relation to the primary output should be documented.
- Sensitivity: Report influence of simulation settings and numerical algorithms where tested.
- Principal finding: Transparent reporting improves reproducibility, reusability and model exchange.
- Limitation: General biomechanics; reporting framework is not fossil-specific.
- UALVP 2 implication: Provides the backbone for a UALVP 2 reproducibility checklist.
- Verification status: `verified_from_article`

### [S18] Schaer, R. et al. (2020). Image-based biomechanical models of the musculoskeletal system. European Radiology Experimental.
- DOI: `10.1186/s41747-020-00172-3`
- URL: https://doi.org/10.1186/s41747-020-00172-3
- Publication type: `peer_reviewed_review`
- Geometry: Image-based geometry reconstruction.
- Segmentation: Segmentation is an upstream requirement.
- Repair / regularization: Surface quality strongly influences tetrahedral mesh generation.
- Surface geometry: Poorly shaped boundaries can create low-quality tetrahedral meshes.
- Volume mesh: Reviews Delaunay, advancing-front, octree and quality-improvement approaches.
- Mesh QC: Mesh topology/shape and sliver control discussed.
- Convergence: General numerical principles; not fossil-specific.
- Sensitivity: Meshing method and boundary quality influence computational accuracy.
- Principal finding: Mesh quality is coupled to the quality of the boundary representation and the meshing algorithm.
- Limitation: Medical imaging context, not fossil.
- UALVP 2 implication: Supports checking surface quality before TetGen rather than assuming TetGen can fully repair poor geometry.
- Verification status: `verified_from_review`

### [S19] Fraterrigo, G., Santamaria, A. D., Iori, G., Pani, M., Crimi, G., Schileo, E., & Taddei, F. (2026). Tetrahedral microFE models of human trabecular bone can be a valid alternative to voxel-based hexahedral models: A comparative study using an open-source workflow. Journal of the Mechanical Behavior of Biomedical Materials, 176, 107326.
- DOI: `10.1016/j.jmbbm.2025.107326`
- URL: https://doi.org/10.1016/j.jmbbm.2025.107326
- Publication type: `peer_reviewed_primary`
- Geometry: MicroCT human trabecular bone cores.
- Segmentation: MicroCT-derived trabecular models.
- Repair / regularization: UNVERIFIED
- Surface geometry: Geometry-based tetrahedral models compared to voxel-based models.
- Volume mesh: Hex voxel models versus quadratic tetrahedral models at multiple resolutions.
- Mesh QC: Verification against apparent modulus/strain and experimentally calibrated behavior.
- Convergence: Multiple resolutions evaluated.
- Sensitivity: Mesh type, mesh resolution and material assignment.
- Principal finding: Global apparent modulus could remain accurate across model choices while local stress/strain outcomes varied more strongly; mesh type and resolution matter for local fields.
- Limitation: Human trabecular bone, not fossil skull; published 2026.
- UALVP 2 implication: Useful recent evidence that 'same global output' does not imply same local stress field; motivates multi-output convergence and cautious local stress interpretation.
- Verification status: `verified_from_search_metadata`

## 3. Segmentation uncertainty review

### 3.1 What the literature supports
- Fossil CT segmentation is harder than many extant clinical datasets because matrix can occupy intertrabecular spaces, fossil-to-matrix contrast can be low, cortical bone can be eroded, and artifacts can complicate boundaries. [S11, S14, S15]
- Manual segmentation can be highly accurate but is labor-intensive; deep-learning approaches can reduce manual workload but remain data- and artifact-dependent. [S14, S15]
- Geometry/segmentation simplification can be tolerable for some **global deformation patterns** while still changing **local strain magnitudes**. [S08, S09]
- The 2025 dinosaur study is particularly relevant because it directly compared a fossil model with and without removal of matrix from intertrabecular spaces and reported materially different stress patterns. It also noted the need for experimental validation and the extra mesh-processing burden produced by highly porous segmented geometry. [S15]

### 3.2 UALVP 2 recommendation
Treat segmentation/geometry as a **model-form layer** separate from FE discretization. For the current project, maintain at least three immutable geometry states where data permit:

1. `raw_or_source_geometry` — untouched input representation;
2. `cleaned_geometry` — topology/scale repairs only, with an audit trail;
3. `fe_geometry` — final watertight/regularized geometry used by TetGen.

Do not overwrite earlier states. Record voxel size, scan source, segmentation method, threshold/rules, manual edits, smoothing/decimation, hole filling, crack repair, mirrored/reconstructed regions, and volume change after each transformation.

### 3.3 Segmentation sensitivity to consider later
- Threshold/labeling tolerance (where meaningful and defensible).
- Manual versus automated/deep-learning segmentation in a limited audit region.
- Presence/absence of matrix in cancellous/intertrabecular spaces.
- Cortical/trabecular separation versus homogenized bone.
- Alternative repair choices for damaged or reconstructed regions.
- Sensitivity of geometry-derived quantities such as volume, surface area, thickness and apex curvature before any FE solve.

## 4. Geometry repair, smoothing and watertight reconstruction

The fossil-restoration literature treats cracks, breaks, missing parts and deformation as potentially consequential for downstream functional analysis rather than merely cosmetic. Automatic hole filling/grow-shrink operations are useful for small defects, while larger repairs generally require explicit manual interpolation or reconstruction. [S11, S12]

For UALVP 2, every operation should be classified before application as one of:

- **topology repair** — fixes invalid connectivity without intended anatomical change;
- **geometric regularization** — removes sub-resolution noise or artifacts but changes coordinates;
- **anatomical reconstruction** — explicitly infers missing/damaged morphology;
- **symmetry/mirroring** — replaces missing anatomy from a corresponding structure;
- **surface decimation/remeshing** — changes representation/resolution while ideally preserving macroscopic geometry.

Only the first category should be presumed numerically neutral, and even then the result should be checked. The others should be regarded as model choices and potentially sensitivity variables. [S11, S18]

## 5. Tetrahedral meshing and quality control

For the UALVP 2 pipeline, the literature supports a two-level view of FE mesh quality:

**Topological/geometric validity:** watertight closed surface, no self-intersections, no non-manifold edges, coherent normals, no inverted elements, and a valid closed volume. [S13, S18]

**Element quality / numerical adequacy:** element-size distribution, aspect/shape measures, Jacobian/volume positivity, sliver control, and a documented refinement/convergence study. TetGen's documentation emphasizes quality and size control for Delaunay tetrahedralization; radius-edge ratio is one available quality measure. [TetGen documentation]

Mesh-generation settings should therefore be recorded, not just the final element count: mesher/version, command-line or parameter settings, target element size, local refinement criteria, quality constraints, region markers, surface decimation/remeshing settings, random seeds if any, and the resulting quality summary.

### Terminology for the UALVP 2 project

| Situation | Recommended term | Do **not** call it |
|---|---|---|
| Same FE-ready geometry/model, progressively smaller tetrahedral element size | **mesh-refinement / mesh-convergence study** | geometry sensitivity |
| Same geometry but different TetGen quality/size parameters | **meshing-parameter sensitivity** | physical validation |
| Same underlying anatomy but different surface decimation/smoothing/repair branch | **geometry-resolution / geometry-processing sensitivity** | pure mesh convergence |
| Same geometry and mesh density but different meshing software/algorithm | **mesh-generation-method sensitivity** | convergence alone |
| Different segmentation of the CT volume | **segmentation sensitivity / geometry uncertainty** | mesh convergence |
| Different FE formulation (e.g., linear vs quadratic tetrahedra) | **element-formulation sensitivity** | mesh refinement |

This distinction is the strongest methodological recommendation for the requested principle. **Comparing meshes generated from the same geometry/modeling pipeline is scientifically cleaner for estimating discretization effects because the independent variable is primarily the volume discretization.** A cross-branch comparison can be valuable, but it answers a different question: how much the modeling pipeline itself changes the result. [S03, S06, S10, S16]

## 6. Mesh-convergence methodology review

### 6.1 What counts as convergence
The literature and verification guidance describe convergence as diminishing change in a defined quantity of interest under systematic refinement. Mesh convergence is therefore **quantity-specific** rather than an intrinsic property of a mesh. [S05, S06, S17]

A good UALVP 2 study should pre-specify the quantities that matter scientifically and evaluate them across a refinement ladder. The project already identifies energy, apex displacement and stress summaries as important outputs; each should have an explicit convergence trace.

### 6.2 Recommended UALVP 2 convergence outputs

| Output | Recommended convergence metric | Reason |
|---|---|---|
| Total strain/elastic energy | Relative change between successive meshes | Integral/global quantity; usually less sensitive to local point artifacts |
| Apex displacement | Displacement magnitude at a fixed anatomical reference/probe definition | Direct project output and easy to compare across meshes |
| Regional stress summary | ROI mean/median and selected upper percentile at fixed spatial definition | More reproducible than unconstrained global max |
| Local hotspot stress | Optional secondary diagnostic, not sole convergence criterion | Can be dominated by singularity/point-load/constraint effects |
| Reaction-force balance | Relative force imbalance / equilibrium check | Independent numerical sanity check |

Where a global maximum or hotspot is scientifically important, report its spatial location and how that location was compared across meshes; do not silently compare maxima occurring at different coordinates. The general reporting guidance specifically recommends stating whether convergence variables represent overall or regional responses. [S17]

### 6.3 Three-level vs many-level refinement
Three meshes can support formal Richardson/GCI-style discretization estimates when refinement ratios and asymptotic behavior are appropriate; more meshes provide a clearer empirical convergence curve and are often more useful for complex skull geometries where different outputs converge at different rates. [S06, S17]

For UALVP 2, a practical compromise is a **4–6 level h-refinement series** generated from the same geometry pipeline, with a documented refinement factor and identical model inputs at each level. The stopping criterion should be specified before interpreting the result; do not choose the final mesh solely because the element count feels 'large enough.'

### 6.4 Important limitation
Mesh convergence is **not validation**. It shows that the discretized model is becoming mesh-independent for the chosen output(s), not that the fossil skull behaves biologically as the model predicts. [S05, S17]

## 7. Reproducibility checklist for the imaging-to-FEM pipeline
- [ ] Specimen identifier and collection/catalog number.
- [ ] CT dataset accession/source and access date.
- [ ] Scanner type, acquisition mode, kV/keV, current, projections, reconstruction algorithm, voxel dimensions and any filters/artifact corrections.
- [ ] Raw-data checksum or immutable provenance identifier where possible.
- [ ] Segmentation software and version.
- [ ] Segmentation method: threshold, region growing, manual, machine learning, or hybrid.
- [ ] Thresholds/labels/classes and treatment of ambiguous voxels.
- [ ] Manual segmentation edits and QA procedure; ideally operator and review status.
- [ ] Treatment of matrix, trabecular spaces, cortical bone, cavities, air/fluid spaces and mineral infill.
- [ ] Digital repair operations: hole filling, crack repair, interpolation, mirroring, reconstruction and their affected regions.
- [ ] Smoothing/regularization method, parameter values and before/after geometric diagnostics.
- [ ] Surface format, units, coordinate system and orientation.
- [ ] Watertightness, manifoldness, self-intersection and normal checks.
- [ ] Surface decimation/remeshing algorithm and target face/edge size.
- [ ] Volume-mesh generator and version (e.g., TetGen), full settings/arguments, seed/randomness if applicable.
- [ ] Element type/order and integration formulation.
- [ ] Mesh quality statistics and acceptance thresholds.
- [ ] Element counts, node counts, degrees of freedom and characteristic element-size measure for every convergence tier.
- [ ] Material regions/assignments and mapping rule.
- [ ] Loads, load application geometry, magnitude, direction and units.
- [ ] Boundary conditions, constrained degrees of freedom and rationale.
- [ ] Solver version, numerical tolerances and relevant convergence settings.
- [ ] Verification tests and analytical/benchmark checks.
- [ ] Mesh-convergence plots/tables for every primary quantity of interest.
- [ ] Exact scripts/notebooks used to reproduce the geometry and meshes.
- [ ] SHA-256 checksums for exported geometry/mesh artifacts where practical.
- [ ] Machine/environment versions sufficient to reproduce the calculation.

## 8. Concrete implications for UALVP 2

| Issue | Recommendation | Project area |
|---|---|---|
| Geometry pipeline | Freeze one FE-ready geometry for the primary Phase 4 mesh-convergence study. Store all alternate repairs/smoothing branches separately. | Current Phase 4 / geometry |
| Mesh convergence | Use the same FE-ready geometry and identical model inputs across a multi-level h-refinement series. Record node/element counts, characteristic size and quality statistics. | Mesh convergence |
| Segmentation | Treat segmentation as a separate uncertainty/model-form layer; do not use mesh convergence to absorb segmentation changes. | Geometry pipeline / future UQ |
| Watertight repair | Run explicit topology checks before meshing; report failed checks and repair operations rather than silently fixing them. | Geometry pipeline |
| TetGen settings | Record the full meshing parameter set. Quality targets should be fixed across refinement tiers except the intended size/refinement variable. | Mesh convergence |
| Outputs | Converge energy, apex displacement and predefined stress summaries separately. Treat unconstrained maximum stress as a diagnostic unless a non-singular location/ROI is defined. | Mesh convergence / interpretation |
| Stress interpretation | Because local FE fields can remain sensitive to geometry and discretization even when global outputs are stable, report spatially robust summaries and uncertainty rather than a single 'peak stress' as the primary biological result. | Interpretation / future UQ |
| Reconstruction branches | When geometry alternatives are scientifically plausible (repair, segmentation, surface smoothing), label them as model-form/geometry sensitivity scenarios and compare them after the baseline verification/convergence study. | Future UQ |
| 2024–2025 AI segmentation | AI-assisted segmentation is a reproducibility/workflow option, not a substitute for manual anatomical QA; validate transferability on UALVP 2 before treating it as a production method. | Geometry pipeline / future UQ |
| Validation language | Use 'verification' for numerical implementation and convergence; reserve 'validation' for comparison to physical/experimental evidence, recognizing that direct specimen-level validation of fossil cranial impact models is generally unavailable. | Verification / interpretation |

## 9. Open methodological questions
- What segmentation uncertainty representation is most defensible for UALVP 2 given the actual CT voxel size, matrix contrast and internal cranial anatomy?
- Which stress summaries remain stable under local mesh refinement, especially near the dome apex and any load/constraint interfaces?
- How much of the apparent sensitivity is attributable to surface regularization versus tetrahedral discretization?
- Should geometry-processing alternatives be represented later as discrete model-form scenarios or transformed into continuous geometric variables for UQ?
- Can the project define a fixed anatomical ROI/probe framework that remains spatially comparable across mesh tiers and geometry variants?
- What element-quality thresholds are sufficient for the specific solver formulation used in Phase 4, rather than inherited generically from software defaults?

## 10. Search and source notes
- Priority was given to peer-reviewed methodological papers and fossil-specific primary studies, followed by general image-based biomechanics and software/method documentation.
- Conference abstracts and software documentation are lower-priority contextual evidence and should not be treated as equivalent to peer-reviewed validation studies.
- The 2025 *Scientific Reports* study and 2024 *Scientific Reports* segmentation study were checked directly because they are recent and directly relevant to fossil CT segmentation. [S14, S15]
- Repository context checked: the project currently distinguishes original/cleaned/FE meshes and has dedicated notebooks for FE geometry preparation and multi-tier mesh convergence; CT segmentation is currently deferred to a later phase. See repository README. [project repository]

## 11. References
- [S01] Rayfield, E. J. (2007). Finite Element Analysis and Understanding the Biomechanics and Evolution of Living and Fossil Organisms. Annual Review of Earth and Planetary Sciences, 35, 541–576. DOI: 10.1146/annurev.earth.35.031306.140104.
- [S02] Taddei, F., Martelli, S., Reggiani, B., Cristofolini, L., & Viceconti, M. (2006). Finite-element modeling of bones from CT data: sensitivity to geometry and material uncertainties. IEEE Transactions on Biomedical Engineering, 53(11), 2194–2200. DOI: 10.1109/TBME.2006.879473.
- [S03] Viceconti, M., Bellingeri, L., Cristofolini, L., & Toni, A. (1998). A comparative study on different methods of automatic mesh generation of human femurs. Medical Engineering & Physics, 20(1), 1–10. DOI: 10.1016/S1350-4533(97)00049-0.
- [S04] Camacho, D. L. A., Hopper, R. H., Lin, G. M., & Myers, B. S. (1997). An improved method for finite element mesh generation of geometrically complex structures with application to the skullbase. Journal of Biomechanics, 30(10), 1067–1070. DOI: 10.1016/S0021-9290(97)00073-0.
- [S05] Anderson, A. E., Ellis, B. J., & Weiss, J. A. (2007). Verification, validation and sensitivity studies in computational biomechanics. Computer Methods in Biomechanics and Biomedical Engineering, 10(3), 171–184. DOI: 10.1080/10255840601160484.
- [S06] Bright, J. A., & Rayfield, E. J. (2011). The response of cranial biomechanical finite element models to variations in mesh density. The Anatomical Record, 294(4), 610–620. DOI: 10.1002/ar.21358.
- [S07] Bright, J. A., & Rayfield, E. J. (2011). Sensitivity and ex vivo validation of finite element models of the domestic pig cranium. Journal of Anatomy, 219(4), 456–471. DOI: 10.1111/j.1469-7580.2011.01408.x.
- [S08] Fitton, L. C., Prôa, M., Rowland, C., Toro-Ibacache, V., & O'Higgins, P. (2015). The impact of simplifications on the performance of a finite element model of a Macaca fascicularis cranium. The Anatomical Record, 298(1), 107–121. DOI: 10.1002/ar.23075.
- [S09] Toro-Ibacache, V., Fitton, L. C., Fagan, M. J., & O'Higgins, P. (2015). Validity and sensitivity of a human cranial finite element model: implications for comparative studies of biting performance. Journal of Anatomy, 228(1), 70–84. DOI: 10.1111/joa.12384.
- [S10] McCurry, M. R., Evans, A. R., & McHenry, C. R. (2015). The sensitivity of biological finite element models to the resolution of surface geometry: a case study of crocodilian crania. PeerJ, 3, e988. DOI: 10.7717/peerj.988.
- [S11] Zollikofer, C. P. E. et al. / Lautenschlager-linked digital restoration literature. See: Gunz et al. (2009) and Lautenschlager (2016/2017) for virtual fossil restoration methods; this record is represented here by Lautenschlager, S. (2016). Reconstructing the past: methods and techniques for the digital restoration of fossils.
- [S12] Lautenschlager, S. (2017). From bone to pixel—fossil restoration and reconstruction with digital techniques. Geology Today, 33, 155–159. DOI: 10.1111/gto.12194.
- [S13] Chatar, M., et al. (2023). 'Fossils': A new, fast and open-source protocol to simulate muscle-driven biomechanical loading of bone. Methods in Ecology and Evolution. DOI: 10.1111/2041-210X.14051.
- [S14] Knutsen, E. M., & Konovalov, D. A. (2024). Accelerating segmentation of fossil CT scans through Deep Learning. Scientific Reports, 14, 20943. DOI: 10.1038/s41598-024-71245-1.
- [S15] Zhang, L., Cao, Z., & Zhao, Q. (2025). Deep learning-aided segmentation combined with finite element analysis reveals a more natural biomechanic of dinosaur fossil. Scientific Reports, 15, 13964. DOI: 10.1038/s41598-025-99131-4.
- [S16] Follet, H., et al. (2024). Finite element models with automatic computed tomography bone segmentation for failure load computation. Scientific Reports, 14, 16576. DOI: 10.1038/s41598-024-66934-w.
- [S17] Erdemir, A., Guess, T. M., Halloran, J., Tadepalli, S. C., & Morrison, T. M. (2012). Considerations for reporting finite element analysis studies in biomechanics. Journal of Biomechanics, 45(4), 625–633. DOI: 10.1016/j.jbiomech.2011.11.038.
- [S18] Schaer, R. et al. (2020). Image-based biomechanical models of the musculoskeletal system. European Radiology Experimental. DOI: 10.1186/s41747-020-00172-3.
- [S19] Tetrahedral microFE models of human trabecular bone can be a valid alternative to voxel-based hexahedral models: A comparative study using an open-source workflow. Journal of the Mechanical Behavior of Biomedical Materials, 176, 107326. DOI: 10.1016/j.jmbbm.2025.107326.

## 12. Controlled epistemic labels
- `DO` = direct observation reported by the source.
- `AI` = author interpretation.
- `MA` = model assumption.
- `SYN` = synthesis by this review.
- `UNVERIFIED` = not sufficiently checked in the current evidence pass.


### Key terminology decision for this project
> **Mesh convergence:** controlled refinement of the discretization of a fixed mathematical/physical model.
>
> **Geometry/segmentation sensitivity:** controlled alteration of the reconstructed anatomical model or its representation.
>
> **Mesh-generation-method sensitivity:** controlled comparison of different mesh-generation algorithms or branches.
>
> **Discretization uncertainty:** residual numerical uncertainty associated with finite spatial resolution after a convergence/verification study.

This terminology preserves interpretability of the Phase 4 result: if the same geometry/modeling pipeline is used across mesh tiers, observed differences can be attributed primarily to discretization. If the geometry or processing branch changes, the experiment is intentionally broader and should be labeled accordingly.

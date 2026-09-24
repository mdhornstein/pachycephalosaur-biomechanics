# Literature Corpus & Evidence Base

This directory houses the structured literature review, parameter audits, and empirical evidence base for the *Stegoceras validum* (UALVP 2) cranial biomechanics and uncertainty quantification investigation.

---

## 🧭 Fast Navigation

### 1. Executive Synthesis & Master Evidence (Primary Entry Point)
* **[`stegoceras_biomechanics_literature_synthesis.md`](stegoceras_biomechanics_literature_synthesis.md)**  
  **The Master Review**: Integrated scoping review, evidence-to-model mapping, failure-mode taxonomy, and scientific gap analysis synthesizing all four specialist literature modules.
* **[`stegoceras_biomechanics_evidence_matrix.csv`](stegoceras_biomechanics_evidence_matrix.csv)**  
  **The Master Evidence Matrix**: Consolidated CSV cataloging all reviewed studies with stable DOIs, modalities, boundary conditions, mesh strategies, epistemic codes, and direct relevance to our model.

### 2. Independent Challenge Audit & Critical Corrections
* **[`independent_literature_audit.md`](independent_literature_audit.md)**  
  **Independent Scientific Audit**: Rigorous challenge audit of the synthesis, dossiers, and evidence matrices at commit `473d978`. Evaluates bibliographic veracity (e.g., Sullivan 2003 vs. 2006, Peterson et al. 2013 authorship, Dumont et al. 2009 journal), enforces terminology discipline (comparative functional corroboration vs. physical validation), and establishes conservative parameterization guidelines for Phase 5 UQ.
* **[`LITERATURE_CORRECTIONS.md`](LITERATURE_CORRECTIONS.md)**  
  **Canonical Audit-to-Correction Tracking Ledger**: Comprehensive traceability matrix mapping every independent audit finding (AF-01 through AF-23) to concrete actions taken, evidentiary citations, and resolution statuses (`corrected`, `partially corrected`, `unresolved`, `rejected with justification`).

### 3. Historical Specimen & Parameter Audits (Phase 3 Baseline)
* **[`snively_theodor_2011_model_audit.md`](snively_theodor_2011_model_audit.md)**  
  Line-by-line model input extraction, material property mapping, and boundary constraint audit from Snively & Theodor (2011). *(Directly tested in `tests/test_phase3_model_audit.py`)*.
* **[`missing_input_sources.md`](missing_input_sources.md)**  
  Gap resolution strategy and evidence provenance for model inputs not directly constrained in primary literature. *(Directly tested in `tests/test_phase3_model_audit.py`)*.

---

## 📁 Directory Architecture

```text
literature/
├── README.md                                          # This navigation guide
│
│   # --- PRIMARY EXECUTIVE SYNTHESIS & AUDITS (Root Level) ---
├── stegoceras_biomechanics_literature_synthesis.md    # Master integrated scoping review & gap analysis
├── stegoceras_biomechanics_evidence_matrix.csv        # Master consolidated evidence matrix
├── independent_literature_audit.md                    # Independent challenge audit (commit 673a222)
├── LITERATURE_CORRECTIONS.md                          # Canonical audit-to-correction tracking ledger
├── snively_theodor_2011_model_audit.md                # Phase 3 parameter audit (pytest verified)
├── missing_input_sources.md                           # Phase 3 source resolution (pytest verified)
│
│   # --- REVIEW ARCHITECTURE & SEARCH RECORDS ---
├── protocols/                                         # Search queries, PRISMA/scoping methodology
│   ├── literature_review_design.md                    # Review protocol, prompts, & scoping framework
│   └── stegoceras_biomechanics_literature_review_management.md # Database queries & master bibliography
│
│   # --- SPECIALIST EVIDENCE STREAMS ---
└── dossiers/                                          # 4 Topic dossiers & evidence matrices
    ├── feafem_paleontology_scoping_review.md          # Topic A: FEA in Paleontology review
    ├── feafem_paleontology_evidence_matrix.csv        # Topic A: Evidence matrix
    ├── pachycephalosaur_stegoceras_ualvp2_dossier.md  # Topic B: Stegoceras & UALVP 2 dossier
    ├── pachycephalosaur_ualvp2_evidence_matrix.csv    # Topic B: Evidence matrix
    ├── uq_sensitivity_computational_biomechanics_scoping_review.md # Topic C: UQ & Sensitivity review
    ├── uq_sensitivity_computational_biomechanics_evidence_matrix.csv # Topic C: Evidence matrix
    ├── ct_segmentation_geometry_mesh_validation_review.md          # Topic D: CT & Meshing review
    └── ct_segmentation_geometry_mesh_validation_evidence_matrix.csv # Topic D: Evidence matrix
```

---

## 🔬 Specialist Dossiers & Evidence Streams (`dossiers/`)

The review was constructed using an evidence-first architecture across four specialist domains:

1. **Topic A: FEA/FEM in Paleontology**
   - Review: [`dossiers/feafem_paleontology_scoping_review.md`](dossiers/feafem_paleontology_scoping_review.md)
   - Matrix: [`dossiers/feafem_paleontology_evidence_matrix.csv`](dossiers/feafem_paleontology_evidence_matrix.csv)
   - *Focus*: Methodological lineage (Rayfield, Bright), validation on extant taxa, pattern vs. absolute stress interpretation, and recurring modeling assumptions.

2. **Topic B: Pachycephalosaurs, *Stegoceras*, & UALVP 2**
   - Dossier: [`dossiers/pachycephalosaur_stegoceras_ualvp2_dossier.md`](dossiers/pachycephalosaur_stegoceras_ualvp2_dossier.md)
   - Matrix: [`dossiers/pachycephalosaur_ualvp2_evidence_matrix.csv`](dossiers/pachycephalosaur_ualvp2_evidence_matrix.csv)
   - *Focus*: Specimen provenance, ontogenetic stage (Schott et al. 2011; subadult suture status), histology zonation, dome biomechanics, prior models (Snively & Cox 2008; Snively & Theodor 2011), and competing behavioral hypotheses (head-strikes vs. flank-butting vs. display).

3. **Topic C: UQ, Sensitivity Analysis, & Computational Biomechanics**
   - Review: [`dossiers/uq_sensitivity_computational_biomechanics_scoping_review.md`](dossiers/uq_sensitivity_computational_biomechanics_scoping_review.md)
   - Matrix: [`dossiers/uq_sensitivity_computational_biomechanics_evidence_matrix.csv`](dossiers/uq_sensitivity_computational_biomechanics_evidence_matrix.csv)
   - *Focus*: Characterization of aleatory vs. epistemic uncertainty, local vs. global sensitivity (Morris, Sobol indices), Latin Hypercube Sampling (LHS), Gaussian Process surrogates, and verification/validation/uncertainty quantification (VVUQ).

4. **Topic D: CT, Segmentation, Geometry, Meshing, & Convergence**
   - Review: [`dossiers/ct_segmentation_geometry_mesh_validation_review.md`](dossiers/ct_segmentation_geometry_mesh_validation_review.md)
   - Matrix: [`dossiers/ct_segmentation_geometry_mesh_validation_evidence_matrix.csv`](dossiers/ct_segmentation_geometry_mesh_validation_evidence_matrix.csv)
   - *Focus*: Voxel resolution effects, deep-learning/threshold segmentation uncertainty, non-invasive topological repair, volumetric tetrahedral mesh generation (TetGen/Gmsh), and output-specific mesh convergence.

---

## 🏷️ Epistemic Evidence Standards

To maintain absolute scientific transparency, all assertions in the review and evidence matrices are categorized by evidentiary status:
* **`DO` (Direct Observation)**: Directly measured from primary CT scans, physical specimens, or explicit experimental measurements.
* **`IN` (Inference)**: Deductions based on extant phylogenetic bracketing, comparative functional anatomy, or physical scaling laws.
* **`MA` (Model Assumption)**: Simplifications imposed for computational tractability (e.g., linear static elasticity, isotropic compact bone).
* **`AI` (Author Interpretation)**: Biological or behavioral hypotheses concluded by original authors (e.g., head-strikes vs. sexual display).
* **`SYN` (Reviewer Synthesis)**: Methodological integration or comparative evaluations drawn in this synthesis.
* **`UNVERIFIED`**: Bibliographic or methodological details not directly verified in the primary document.
* **`TO VERIFY`**: Candidate novelty or methodological claims requiring formal validation before publication.

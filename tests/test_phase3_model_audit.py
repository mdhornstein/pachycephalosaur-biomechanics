"""Automated verification test suite for Phase 3 Model Audit and Biomechanical Benchmark."""

from pathlib import Path
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
MATRIX_PATH = PROJECT_ROOT / "data" / "metadata" / "biomechanics_input_matrix.csv"

VALID_AVAILABILITY_STATUSES = {
    "AVAILABLE_DIRECT",
    "AVAILABLE_DERIVED",
    "LITERATURE_ONLY",
    "INFERABLE_WITH_ASSUMPTION",
    "UNAVAILABLE",
    "NOT_REQUIRED_FOR_SIMPLIFIED_MODEL",
    "AMBIGUOUS"
}

VALID_EVIDENCE_LEVELS = {"A", "B", "C", "D", "E"}
VALID_CONFIDENCE_LEVELS = {"HIGH", "MEDIUM", "LOW"}
VALID_CATEGORIES = {"Geometry", "Material", "Loading", "Boundary_Conditions", "Modeling"}


def test_phase3_deliverables_exist():
    """Verify all 6 core Phase 3 deliverable files exist and are non-empty."""
    deliverables = [
        PROJECT_ROOT / "literature" / "snively_theodor_2011_model_audit.md",
        PROJECT_ROOT / "data" / "metadata" / "biomechanics_input_matrix.csv",
        PROJECT_ROOT / "reports" / "snively_theodor_model_reconstruction.md",
        PROJECT_ROOT / "literature" / "missing_input_sources.md",
        PROJECT_ROOT / "reports" / "phase3_recommended_benchmark.md",
        PROJECT_ROOT / "notebooks" / "05_model_input_dimensional_audit.ipynb"
    ]
    for file_path in deliverables:
        assert file_path.exists(), f"Missing required Phase 3 deliverable: {file_path.name}"
        assert file_path.stat().st_size > 0, f"Phase 3 deliverable is empty: {file_path.name}"


def test_input_matrix_schema_and_uniqueness():
    """Verify input matrix has required columns and unique input_ids."""
    assert MATRIX_PATH.exists(), f"Matrix file missing at {MATRIX_PATH}"
    df = pd.read_csv(MATRIX_PATH)
    
    required_cols = [
        "input_id", "category", "parameter", "description", "value", "units",
        "uncertainty", "source", "source_location", "measurement_type",
        "availability_status", "evidence_level", "current_dataset_source",
        "confidence", "notes"
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"
        
    assert len(df) >= 20, f"Expected at least 20 parameters in input matrix, found {len(df)}"
    assert df["input_id"].is_unique, "Duplicate input_id detected in matrix!"


def test_input_matrix_status_and_evidence_validity():
    """Verify all entries adhere strictly to controlled vocabulary for availability and evidence."""
    df = pd.read_csv(MATRIX_PATH)
    
    for _, row in df.iterrows():
        inp_id = row["input_id"]
        status = row["availability_status"]
        ev_level = row["evidence_level"]
        cat = row["category"]
        conf = row["confidence"]
        
        assert status in VALID_AVAILABILITY_STATUSES, (
            f"Invalid availability_status '{status}' for {inp_id}"
        )
        assert ev_level in VALID_EVIDENCE_LEVELS, (
            f"Invalid evidence_level '{ev_level}' for {inp_id}"
        )
        assert cat in VALID_CATEGORIES, (
            f"Invalid category '{cat}' for {inp_id}"
        )
        assert conf in VALID_CONFIDENCE_LEVELS, (
            f"Invalid confidence '{conf}' for {inp_id}"
        )


def test_no_unavailable_ct_variable_marked_available():
    """Verify that unmeasured internal variables (histology, cortical map) are not falsely marked direct."""
    df = pd.read_csv(MATRIX_PATH)
    
    # Internal histology and 3D cortical thickness require raw CT / histology
    internal_histology = df[df["input_id"] == "INP-GEO-05"].iloc[0]
    cortical_thickness = df[df["input_id"] == "INP-GEO-06"].iloc[0]
    keratin_morph = df[df["input_id"] == "INP-GEO-07"].iloc[0]
    
    assert internal_histology["availability_status"] == "UNAVAILABLE"
    assert cortical_thickness["availability_status"] == "UNAVAILABLE"
    assert keratin_morph["availability_status"] == "UNAVAILABLE"


def test_literature_derived_parameters_have_citations():
    """Verify that every literature-derived parameter has non-empty citation and location fields."""
    df = pd.read_csv(MATRIX_PATH)
    lit_entries = df[df["availability_status"] == "LITERATURE_ONLY"]
    
    assert len(lit_entries) >= 5, "Expected multiple LITERATURE_ONLY parameters"
    for _, row in lit_entries.iterrows():
        inp_id = row["input_id"]
        assert pd.notna(row["source"]) and len(str(row["source"]).strip()) > 0, (
            f"Missing source citation for literature parameter {inp_id}"
        )
        assert pd.notna(row["source_location"]) and len(str(row["source_location"]).strip()) > 0, (
            f"Missing source location for literature parameter {inp_id}"
        )


def test_model_a_inputs_fully_defensible():
    """Verify that Model A (minimal homogeneous model) only requires available inputs and literature constants."""
    df = pd.read_csv(MATRIX_PATH)
    
    # Model A required input IDs
    model_a_inputs = [
        "INP-GEO-01",  # External cranial surface (AVAILABLE_DIRECT)
        "INP-GEO-03",  # Candidate scale parameter s_mm/unit (INFERABLE_WITH_ASSUMPTION)
        "INP-MAT-01",  # Cortical modulus (LITERATURE_ONLY)
        "INP-MAT-02",  # Cortical Poisson ratio (LITERATURE_ONLY)
        "INP-LOAD-01", # Primary normalized load F_ref (NOT_REQUIRED_FOR_SIMPLIFIED_MODEL)
        "INP-LOAD-02", # Derived biological impact load F_bio (LITERATURE_ONLY)
        "INP-LOAD-03", # Load location (AVAILABLE_DIRECT)
        "INP-LOAD-04", # Load direction (INFERABLE_WITH_ASSUMPTION)
        "INP-LOAD-05", # Broad load area envelope (INFERABLE_WITH_ASSUMPTION)
        "INP-BC-01",   # Occipital condyle BC (AVAILABLE_DIRECT)
        "INP-BC-02",   # Nuchal crest BC (AVAILABLE_DIRECT)
    ]
    
    for inp_id in model_a_inputs:
        match = df[df["input_id"] == inp_id]
        assert len(match) == 1, f"Missing input definition for {inp_id}"
        status = match.iloc[0]["availability_status"]
        assert status in {"AVAILABLE_DIRECT", "AVAILABLE_DERIVED", "LITERATURE_ONLY", "INFERABLE_WITH_ASSUMPTION", "NOT_REQUIRED_FOR_SIMPLIFIED_MODEL"}, (
            f"Model A contains an UNAVAILABLE input: {inp_id} (status: {status})"
        )

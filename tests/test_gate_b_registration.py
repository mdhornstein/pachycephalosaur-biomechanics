"""Automated verification test suite for Phase 5 Gate B: CT-to-Surface Registration & Scale Verification."""

import json
from pathlib import Path
import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = PROJECT_ROOT / "results" / "phase5" / "gate_b_registration_metrics.json"
PROVENANCE_PATH = PROJECT_ROOT / "data" / "metadata" / "gate_b_landmark_provenance.json"


@pytest.fixture(scope="module")
def gate_b_metrics():
    assert METRICS_PATH.exists(), f"Gate B metrics file missing at {METRICS_PATH}"
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def landmark_provenance():
    assert PROVENANCE_PATH.exists(), f"Landmark provenance missing at {PROVENANCE_PATH}"
    with open(PROVENANCE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_gate_b_mandated_rigid_scale_and_diagnostic(gate_b_metrics):
    """Verifies that mandated registration scale is 1.0 and free-scale diagnostic s_hat is near 1.0 (<1%)."""
    assert gate_b_metrics["gate"] == "Gate B"
    assert gate_b_metrics["status"] == "VERIFIED_PASS"
    assert np.isclose(gate_b_metrics["mandated_registration_scale"], 1.0, atol=1e-6)
    
    diag = gate_b_metrics["scale_diagnostic"]
    s_hat = diag["free_scale_estimate_s_hat"]
    assert abs(s_hat - 1.0) < 0.015, f"Free-scale diagnostic s_hat {s_hat} deviates more than 1.5% from 1.0"
    assert np.isclose(s_hat, 1.00494, atol=1e-4)
    assert diag["rms_residual_delta_mm"] < 0.10, "Free-scale fit does not substantially alter landmark RMS"


def test_landmark_provenance_audit_trail(landmark_provenance, gate_b_metrics):
    """Verifies that landmark provenance metadata exists, contains 5 distinct landmarks with complete audit trails."""
    assert landmark_provenance["landmark_count"] == 5
    assert len(landmark_provenance["landmarks"]) == 5
    
    lm_metrics = gate_b_metrics["landmark_registration"]
    for lm in landmark_provenance["landmarks"]:
        assert "id" in lm
        assert "anatomical_name" in lm
        assert "g0_identification_method" in lm
        assert "ct_identification_method" in lm
        assert "potential_circularity_notes" in lm
        assert lm["id"] in lm_metrics["per_landmark_residuals_mm"]


def test_voxel_coordinate_convention_zero_based(gate_b_metrics):
    """Verifies that the voxel coordinate convention is explicitly zero-based with no +0.5 offset."""
    convention_str = gate_b_metrics["voxel_coordinate_convention"]
    assert "no +0.5 offset" in convention_str
    assert "ImagePositionPatient" in convention_str


def test_threshold_rule_frozen_and_objective(gate_b_metrics):
    """Verifies that the threshold rule was derived from full-volume intensity distribution prior to registration."""
    rule = gate_b_metrics["threshold_rule"]
    assert 15000 < rule["primary_threshold"] < 25000
    assert "Otsu" in rule["derivation"]
    assert rule["background_mode"] < rule["primary_threshold"] < rule["bone_mode"]


def test_landmark_registration_residuals(gate_b_metrics):
    """Verifies landmark-only rigid registration achieves sub-millimeter RMS without deformation."""
    lm = gate_b_metrics["landmark_registration"]
    assert lm["num_landmarks"] == 5
    assert lm["rms_residual_mm"] < 1.0, f"Landmark RMS residual too large: {lm['rms_residual_mm']}"
    assert lm["mean_residual_mm"] < 1.0, f"Landmark mean residual too large: {lm['mean_residual_mm']}"
    
    for name, res in lm["per_landmark_residuals_mm"].items():
        assert res < 1.5, f"Landmark {name} residual exceeds 1.5 mm: {res}"


def test_icp_refinement_subvoxel_convergence(gate_b_metrics):
    """Verifies that ICP refinement produces sub-voxel translation and minute rotation angles."""
    icp = gate_b_metrics["icp_refinement"]
    assert icp["final_translation_norm_mm"] < 0.35, (
        f"ICP translation norm {icp['final_translation_norm_mm']} mm exceeds sub-voxel threshold"
    )
    for angle in icp["euler_angles_deg_xyz"]:
        assert abs(angle) < 0.2, f"Euler angle {angle} degrees unexpectedly large"


def test_forward_surface_distance_residuals_submillimeter(gate_b_metrics):
    """Verifies forward G_0 -> S_CT surface residual distribution."""
    res = gate_b_metrics["bidirectional_surface_distance_residuals"]["forward_g0_to_ct"]
    assert res["median_mm"] < 0.25, f"Median surface residual {res['median_mm']} exceeds 0.25 mm"
    assert res["mean_mm"] < 0.50, f"Mean surface residual {res['mean_mm']} exceeds 0.50 mm"
    assert res["rms_mm"] < 1.00, f"RMS surface residual {res['rms_mm']} exceeds 1.00 mm"
    assert res["p75_mm"] < 0.35, f"75th percentile {res['p75_mm']} exceeds 0.35 mm"
    assert res["frac_lt_05_pct"] > 80.0, f"Less than 80% within 0.5 mm: {res['frac_lt_05_pct']}%"
    assert res["frac_lt_10_pct"] > 85.0, f"Less than 85% within 1.0 mm: {res['frac_lt_10_pct']}%"


def test_reverse_surface_distance_residuals_and_bidirectional_summary(gate_b_metrics):
    """Verifies reverse S_CT -> G_0 distance metrics and symmetric bidirectional summary."""
    bidi = gate_b_metrics["bidirectional_surface_distance_residuals"]
    rev = bidi["reverse_ct_to_g0"]
    symm = bidi["symmetric_summary"]
    
    assert rev["point_count"] > 4000000
    assert rev["median_mm"] < 2.0, f"Reverse median {rev['median_mm']} unexpectedly large"
    assert rev["rms_mm"] < 6.0, f"Reverse RMS {rev['rms_mm']} unexpectedly large"
    assert rev["frac_lt_20_pct"] > 65.0, f"Less than 65% within 2.0 mm: {rev['frac_lt_20_pct']}%"
    
    assert symm["bidirectional_mean_mm"] > 0.0
    assert symm["bidirectional_rms_mm"] > 0.0
    assert symm["directed_95th_percentile_g0_to_ct_mm"] < 3.0


def test_signed_distance_symmetry(gate_b_metrics):
    """Verifies that signed distance along outward normal shows negligible global bias (< 0.1 mm)."""
    signed = gate_b_metrics["signed_normal_distance"]
    assert abs(signed["mean_mm"]) < 0.10, f"Global signed distance bias too large: {signed['mean_mm']} mm"
    assert 40.0 < signed["exterior_pct"] < 60.0
    assert 40.0 < signed["interior_pct"] < 60.0


def test_anatomical_subregions_differential_accuracy(gate_b_metrics):
    """Verifies differential residuals across anatomical subregions."""
    sub = gate_b_metrics["subregions"]
    dome = sub["frontoparietal_dome"]
    basicranium = sub["occipital_basicranium"]
    palate = sub["ventral_palate_pterygoid"]
    endocranial = sub["endocranial_braincase"]
    
    assert dome["median_mm"] < 0.25
    assert basicranium["median_mm"] < 0.25
    assert palate["median_mm"] < 0.25
    assert basicranium["frac_lt_05_pct"] > 95.0
    assert palate["frac_lt_05_pct"] > 95.0
    assert endocranial["median_mm"] > dome["median_mm"]
    assert endocranial["mean_mm"] > dome["mean_mm"]

"""Automated verification test suite for Phase 5 Gate B: CT-to-Surface Registration & Scale Verification."""

import json
from pathlib import Path
import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = PROJECT_ROOT / "results" / "phase5" / "gate_b_registration_metrics.json"


@pytest.fixture(scope="module")
def gate_b_metrics():
    assert METRICS_PATH.exists(), f"Gate B metrics file missing at {METRICS_PATH}"
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_gate_b_status_and_scale(gate_b_metrics):
    """Verifies that Gate B status is VERIFIED_PASS and empirical scale factor is exactly 1.000000."""
    assert gate_b_metrics["gate"] == "Gate B"
    assert gate_b_metrics["status"] == "VERIFIED_PASS"
    assert np.isclose(gate_b_metrics["scale_factor_empirical"], 1.0, atol=1e-6)


def test_voxel_coordinate_convention_zero_based(gate_b_metrics):
    """Verifies that the voxel coordinate convention is explicitly zero-based with no +0.5 offset."""
    convention_str = gate_b_metrics["voxel_coordinate_convention"]
    assert "no +0.5 offset" in convention_str
    assert "ImagePositionPatient" in convention_str


def test_threshold_rule_frozen_and_objective(gate_b_metrics):
    """Verifies that the threshold rule was derived from full-volume intensity distribution prior to registration."""
    rule = gate_b_metrics["threshold_rule"]
    assert rule["primary_threshold"] > 15000 and rule["primary_threshold"] < 25000
    assert "Otsu" in rule["derivation"]
    assert rule["background_mode"] < rule["primary_threshold"] < rule["bone_mode"]


def test_landmark_registration_residuals(gate_b_metrics):
    """Verifies landmark-only rigid registration achieves sub-millimeter RMS without deformation."""
    lm = gate_b_metrics["landmark_registration"]
    assert lm["num_landmarks"] == 5
    assert lm["rms_residual_mm"] < 1.0, f"Landmark RMS residual too large: {lm['rms_residual_mm']}"
    assert lm["mean_residual_mm"] < 1.0, f"Landmark mean residual too large: {lm['mean_residual_mm']}"
    
    # Check individual landmark residuals
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


def test_surface_distance_residuals_submillimeter(gate_b_metrics):
    """Verifies surface-to-surface residual distribution from G_0 to CT isosurface."""
    res = gate_b_metrics["surface_distance_residuals"]
    assert res["median_mm"] < 0.25, f"Median surface residual {res['median_mm']} exceeds 0.25 mm"
    assert res["mean_mm"] < 0.50, f"Mean surface residual {res['mean_mm']} exceeds 0.50 mm"
    assert res["rms_mm"] < 1.00, f"RMS surface residual {res['rms_mm']} exceeds 1.00 mm"
    assert res["p75_mm"] < 0.35, f"75th percentile {res['p75_mm']} exceeds 0.35 mm"
    assert res["frac_lt_05_pct"] > 80.0, f"Less than 80% within 0.5 mm: {res['frac_lt_05_pct']}%"
    assert res["frac_lt_10_pct"] > 85.0, f"Less than 85% within 1.0 mm: {res['frac_lt_10_pct']}%"


def test_signed_distance_symmetry(gate_b_metrics):
    """Verifies that signed distance along outward normal shows negligible global bias (< 0.1 mm)."""
    signed = gate_b_metrics["signed_normal_distance"]
    assert abs(signed["mean_mm"]) < 0.10, f"Global signed distance bias too large: {signed['mean_mm']} mm"
    assert 40.0 < signed["exterior_pct"] < 60.0
    assert 40.0 < signed["interior_pct"] < 60.0


def test_anatomical_subregions_differential_accuracy(gate_b_metrics):
    """Verifies that rigid registration is tightest on external compact bone (dome, basicranium, palate)
    and largest on endocranial internal surfaces.
    """
    sub = gate_b_metrics["subregions"]
    dome = sub["frontoparietal_dome"]
    basicranium = sub["occipital_basicranium"]
    palate = sub["ventral_palate_pterygoid"]
    endocranial = sub["endocranial_braincase"]
    
    # Exterior subregions have sub-0.25 mm median residuals
    assert dome["median_mm"] < 0.25
    assert basicranium["median_mm"] < 0.25
    assert palate["median_mm"] < 0.25
    
    # Palate and basicranium have near-100% agreement within 0.5 mm
    assert basicranium["frac_lt_05_pct"] > 95.0
    assert palate["frac_lt_05_pct"] > 95.0
    
    # Endocranial cavity exhibits larger residuals due to mesh filling/foramina closure
    assert endocranial["median_mm"] > dome["median_mm"]
    assert endocranial["mean_mm"] > dome["mean_mm"]

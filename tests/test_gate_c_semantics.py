"""Automated verification test suite for Phase 5 Gate C: Image Semantics & Intensity Characterization."""

import json
from pathlib import Path
import numpy as np
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_PATH = PROJECT_ROOT / "results" / "phase5" / "gate_c_semantics_metrics.json"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


@pytest.fixture(scope="module")
def gate_c_metrics():
    assert METRICS_PATH.exists(), f"Gate C metrics file missing at {METRICS_PATH}"
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_gate_c_status_and_metadata(gate_c_metrics):
    """Verifies that Gate C execution completed with status VERIFIED_PASS and correct metadata."""
    assert gate_c_metrics["gate"] == "Gate C"
    assert gate_c_metrics["status"] == "VERIFIED_PASS"
    assert gate_c_metrics["specimen"] == "Stegoceras validum UALVP 2"
    assert gate_c_metrics["dataset"] == "UALVP2-CT-DICOM-CRAN-01"

    meta = gate_c_metrics["volume_metadata"]
    assert meta["num_slices"] == 514
    assert meta["rows"] == 1024
    assert meta["cols"] == 754
    assert meta["shape_xyz"] == [754, 1024, 514]
    assert np.isclose(meta["spacing_mm"][0], 0.207572, atol=1e-5)
    assert np.isclose(meta["spacing_mm"][1], 0.207572, atol=1e-5)
    assert np.isclose(meta["spacing_mm"][2], 0.250000, atol=1e-5)


def test_dynamic_range_and_100_percent_histogram_conservation(gate_c_metrics):
    """Verifies that 100% of voxels are accounted for and intensity bounds respect 16-bit limits."""
    dr = gate_c_metrics["dynamic_range_audit"]
    assert dr["total_voxels"] == 396857344  # 754 * 1024 * 514 voxels
    assert dr["histogram_accounting_pct"] == 100.0
    assert dr["min_intensity"] >= 0
    assert dr["max_intensity"] <= 65535
    assert dr["non_zero_fraction_pct"] > 50.0

    rule = dr["threshold_rule"]
    assert rule["background_mode"] < rule["otsu_threshold"] < rule["bone_mode"]
    assert 18000 < rule["otsu_threshold"] < 25000


def test_bone_mask_distribution(gate_c_metrics):
    """Verifies that full-volume bone mask distribution and peak structure are evaluated."""
    assert "bone_mask_distribution" in gate_c_metrics
    bm = gate_c_metrics["bone_mask_distribution"]
    assert bm["total_bone_voxels"] > 50000000  # Non-trivial bone voxel count
    assert 10.0 < bm["bone_fraction_pct"] < 30.0
    assert bm["mean_intensity"] > 25000
    assert bm["median_intensity"] > 25000
    assert len(bm["detected_peaks"]) >= 1


def test_anatomical_rois_and_threshold_sensitivity(gate_c_metrics):
    """Verifies that ROIs are evaluated without threshold bias across pre-specified sensitivity range."""
    rois = gate_c_metrics["anatomical_rois"]["statistics"]
    expected_rois = [
        "ambient_air",
        "dorsal_cortex_zone3",
        "dome_core_zone2",
        "basicranium_zone1",
        "sedimentary_matrix",
    ]

    for name in expected_rois:
        assert name in rois, f"ROI '{name}' missing from statistics"
        s = rois[name]
        assert s["voxel_count"] > 100, f"ROI '{name}' voxel count unexpectedly small: {s['voxel_count']}"
        assert not np.isnan(s["mean"]), f"ROI '{name}' mean is NaN"
        assert not np.isnan(s["std"]), f"ROI '{name}' std is NaN"

    # Verify threshold sensitivity data exists and conserves fractions
    assert "threshold_sensitivity" in gate_c_metrics
    sens = gate_c_metrics["threshold_sensitivity"]
    expected_thresholds = ["15000", "18000", "20864", "23000", "25000"]

    for name in expected_rois:
        assert name in sens, f"ROI '{name}' missing from threshold sensitivity"
        t_data = sens[name]["thresholds"]
        for t_key in expected_thresholds:
            assert t_key in t_data, f"Threshold '{t_key}' missing from ROI '{name}'"
            entry = t_data[t_key]
            # Fractions must sum to 100%
            total_pct = entry["bone_fraction_pct"] + entry["low_intensity_fraction_pct"]
            assert np.isclose(total_pct, 100.0, atol=1e-3), (
                f"Fractions do not sum to 100% in {name} at T={t_key}: {total_pct}"
            )

    # Dome core must exhibit non-trivial low-intensity fraction (> 10%)
    core_sens = sens["dome_core_zone2"]["thresholds"]["20864"]
    assert core_sens["low_intensity_fraction_pct"] > 10.0


def test_tissue_separability_metrics_consistency(gate_c_metrics):
    """Verifies that tissue contrast and separability metrics are numerically consistent."""
    sep = gate_c_metrics["tissue_separability"]
    assert "dorsal_cortex_vs_dome_core" in sep

    cortex_core = sep["dorsal_cortex_vs_dome_core"]
    assert cortex_core["cnr"] >= 0.0
    assert cortex_core["bhattacharyya_distance"] >= 0.0
    assert 0.0 <= cortex_core["roc_auc"] <= 1.0

    # Sensitivity sweep for cortex vs core must exist
    assert "cortex_vs_core_sensitivity_sweep" in gate_c_metrics
    sweep = gate_c_metrics["cortex_vs_core_sensitivity_sweep"]
    for t_key in ["15000", "18000", "20864", "23000", "25000"]:
        assert t_key in sweep
        assert sweep[t_key]["cnr"] >= 0.0
        assert 0.0 <= sweep[t_key]["descriptive_roc_auc"] <= 1.0


def test_beam_hardening_cupping_profile(gate_c_metrics):
    """Verifies that residual radial intensity variation across the cross-section is quantified."""
    cupping = gate_c_metrics["beam_hardening_cupping"]
    assert cupping["status"] == "EVALUATED"
    assert cupping["bone_voxel_count"] > 20
    assert cupping["span_mm"] > 10.0
    assert cupping["periphery_mean"] > 20000
    assert cupping["center_mean"] > 20000
    assert 0.0 < cupping["cupping_drop_pct"] < 30.0


def test_transect_continuity_and_length(gate_c_metrics):
    """Verifies that 1D ray probes through the frontoparietal dome are continuous and non-empty."""
    transects = gate_c_metrics["dome_transects"]
    assert "vertical_depth_summit" in transects
    assert "coronal_transverse" in transects
    assert "anteroposterior_dorsal" in transects

    vert = transects["vertical_depth_summit"]
    assert np.isclose(vert["total_length_mm"], 50.0, atol=1e-3)
    assert vert["mean_bone_intensity"] > 20864


def test_publication_figures_exist_and_nonempty():
    """Verifies that generated publication Figures 13 and 14 exist on disk with positive size."""
    fig13 = FIGURES_DIR / "figure13_ct_intensity_semantics.png"
    fig14 = FIGURES_DIR / "figure14_dome_attenuation_transects.png"

    assert fig13.exists(), f"Figure 13 missing at {fig13}"
    assert fig14.exists(), f"Figure 14 missing at {fig14}"
    assert fig13.stat().st_size > 50000, f"Figure 13 file suspiciously small ({fig13.stat().st_size} bytes)"
    assert fig14.stat().st_size > 50000, f"Figure 14 file suspiciously small ({fig14.stat().st_size} bytes)"

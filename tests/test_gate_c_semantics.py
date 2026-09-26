"""Automated verification test suite for Phase 5 Gate C: Image Semantics & Attenuation Characterization."""

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


def test_anatomical_rois_completeness_and_moments(gate_c_metrics):
    """Verifies that all 5 target ROIs are present, populated, and have expected SNR characteristics."""
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
        assert s["iqr"] >= 0, f"ROI '{name}' IQR negative"

    # Bone and matrix ROIs must have positive dispersion (IQR > 1000)
    for name in ["dorsal_cortex_zone3", "dome_core_zone2", "basicranium_zone1", "sedimentary_matrix"]:
        assert rois[name]["iqr"] > 1000, f"ROI '{name}' IQR unexpectedly small"

    # Air SNR should be low (< 1.0), bone ROIs should have SNR > 3.0
    assert rois["ambient_air"]["snr"] < 1.0
    assert rois["dorsal_cortex_zone3"]["snr"] > 3.0
    assert rois["dome_core_zone2"]["snr"] > 3.0
    assert rois["basicranium_zone1"]["snr"] > 3.0


def test_epistemic_zonation_indistinguishability(gate_c_metrics):
    """Verifies empirical finding that Zone 2 and Zone 3 exhibit near-zero contrast (refuting Hypothesis A)."""
    sep = gate_c_metrics["tissue_separability"]
    assert "dorsal_cortex_vs_dome_core" in sep

    cortex_core = sep["dorsal_cortex_vs_dome_core"]
    # CNR must be << 1.0 (negligible contrast)
    assert cortex_core["cnr"] < 0.20, f"CNR unexpectedly high: {cortex_core['cnr']}"
    # Bhattacharyya distance must be < 0.10 (high distributional overlap)
    assert cortex_core["bhattacharyya_distance"] < 0.10, (
        f"Bhattacharyya distance unexpectedly high: {cortex_core['bhattacharyya_distance']}"
    )

    # Conclusion string must reflect diagenetic permineralization and literature-based zonation
    conclusion = gate_c_metrics["epistemic_conclusion"]
    assert "Hypothesis B" in conclusion
    assert "permineralized" in conclusion
    assert "cannot be directly segmented" in conclusion
    assert "Schott et al. 2011" in conclusion


def test_beam_hardening_cupping_profile(gate_c_metrics):
    """Verifies that beam-hardening / cupping analysis executed and documented valid metrics."""
    cupping = gate_c_metrics["beam_hardening_cupping"]
    assert cupping["status"] == "EVALUATED"
    assert cupping["bone_voxel_count"] > 20
    assert cupping["span_mm"] > 10.0
    assert cupping["periphery_mean"] > 20000
    assert cupping["center_mean"] > 20000


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

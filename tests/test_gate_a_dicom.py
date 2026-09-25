"""Automated verification test suite for Phase 5 Gate A: DICOM Ingestion & Cryptographic Header Audit."""

import json
from pathlib import Path
import numpy as np
import pytest
import pydicom

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DICOM_DIR = PROJECT_ROOT / "data" / "raw" / "dicom" / "cranium"
MANIFEST_PATH = PROJECT_ROOT / "data" / "metadata" / "dicom_slice_manifest.json"
NESTED_ZIP_PATH = PROJECT_ROOT / "data" / "raw" / "downloads" / "WitmerLab_Stegoceras_UALVP2_DICOM-000018283.zip"


@pytest.fixture(scope="module")
def slice_manifest():
    assert MANIFEST_PATH.exists(), f"Slice manifest missing at {MANIFEST_PATH}"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_dicom_archive_and_slice_count(slice_manifest):
    """Verifies that exactly 514 DICOM slices are present, readable, and cataloged."""
    assert slice_manifest["num_slices"] == 514
    assert len(slice_manifest["slices"]) == 514
    
    dcm_files = sorted(list(DICOM_DIR.glob("*.dcm")))
    assert len(dcm_files) == 514, f"Expected 514 .dcm files, found {len(dcm_files)}"
    
    # Verify unique filenames and SOPInstanceUIDs
    filenames = [s["filename"] for s in slice_manifest["slices"]]
    assert len(set(filenames)) == 514
    uids = [s["sop_instance_uid"] for s in slice_manifest["slices"]]
    assert len(set(uids)) == 514


def test_dicom_spatial_geometry(slice_manifest):
    """Verifies true 3D spatial geometry derived from DICOM headers."""
    # Rows x Columns
    assert slice_manifest["rows"] == 1024
    assert slice_manifest["columns"] == 754
    
    # Pixel spacing in-plane: 0.207572 mm (NOT rounded 0.210 mm)
    ps = slice_manifest["pixel_spacing_mm"]
    assert np.isclose(ps[0], 0.207572, atol=1e-5)
    assert np.isclose(ps[1], 0.207572, atol=1e-5)
    
    # Image orientation: row along +X, col along +Y, normal along +Z
    ori = slice_manifest["image_orientation_patient"]
    assert np.allclose(ori, [1.0, 0.0, 0.0, 0.0, 1.0, 0.0], atol=1e-6)
    normal = slice_manifest["slice_normal"]
    assert np.allclose(normal, [0.0, 0.0, 1.0], atol=1e-6)
    
    # Derived slice plane spacing: exactly 0.250000 mm
    derived_dz = slice_manifest["derived_slice_spacing_mm"]
    assert np.isclose(derived_dz, 0.250000, atol=1e-5)
    
    # Verify spatial range along Z spans exactly 128.25 mm
    z_range = slice_manifest["spatial_coordinate_range_mm"]
    assert np.isclose(z_range[0], 0.0, atol=1e-3)
    assert np.isclose(z_range[1], 128.25, atol=1e-3)


def test_dicom_intensity_semantics(slice_manifest):
    """Verifies that stored pixel values are unsigned 16-bit integers and not calibrated Hounsfield Units."""
    assert slice_manifest["bits_allocated"] == 16
    assert slice_manifest["bits_stored"] == 16
    assert slice_manifest["high_bit"] == 15
    assert slice_manifest["pixel_representation"] == 0  # Unsigned integer
    
    # Rescale values are default identity (no HU calibration phantom)
    assert slice_manifest["rescale_intercept"] == 0.0
    assert slice_manifest["rescale_slope"] == 1.0
    
    # Intensity dynamic range spans raw 16-bit detector scale
    assert slice_manifest["stored_pixel_min"] == 0
    assert slice_manifest["stored_pixel_max"] == 65535


def test_first_and_last_slice_headers():
    """Reads first and last DICOM slice directly from disk with pydicom to verify file integrity."""
    first_path = DICOM_DIR / "WitmerLab_Stegoceras_UALVP2_DICOM001.dcm"
    last_path = DICOM_DIR / "WitmerLab_Stegoceras_UALVP2_DICOM514.dcm"
    
    ds_first = pydicom.dcmread(first_path)
    ds_last = pydicom.dcmread(last_path)
    
    assert ds_first.Rows == 1024
    assert ds_first.Columns == 754
    assert np.allclose([float(x) for x in ds_first.PixelSpacing], [0.207572, 0.207572])
    assert [float(x) for x in ds_first.ImagePositionPatient] == [26.481, 0.0, 0.0]
    assert [float(x) for x in ds_last.ImagePositionPatient] == [26.481, 0.0, 128.25]

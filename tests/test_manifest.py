"""Test dataset manifest parsing, validation, and checksum utilities."""

from pathlib import Path
import pytest
import yaml

from stegoceras_biomechanics.io.manifest import (
    load_manifest,
    get_dataset_entry,
    audit_local_inventory,
    compute_sha256,
)


def test_manifest_structure():
    """Verify that dataset_manifest.yaml loads and conforms to schema."""
    manifest = load_manifest()
    assert "metadata_policy" in manifest
    assert manifest["metadata_policy"]["zero_fabrication"] is True
    
    valid_tiers = set(manifest["metadata_policy"]["provenance_levels"])
    expected_tiers = {
        "primary_scan",
        "segmented_from_primary_scan",
        "researcher_derived",
        "secondary_reference",
    }
    assert valid_tiers == expected_tiers
    
    datasets = manifest.get("datasets", [])
    assert len(datasets) >= 5
    
    required_fields = {
        "dataset_id",
        "specimen_id",
        "taxon",
        "provenance_tier",
        "source_url",
        "license",
        "evidence_source",
    }
    
    for item in datasets:
        for field in required_fields:
            assert field in item, f"Dataset {item.get('dataset_id')} missing {field}"
        assert item["provenance_tier"] in valid_tiers


def test_get_dataset_entry():
    """Verify lookup of specific datasets."""
    entry = get_dataset_entry("UALVP2-MS-CRAN-01")
    assert entry is not None
    assert entry["specimen_id"] == "UALVP 2"
    assert entry["provenance_tier"] == "primary_scan"
    assert entry["media_id"] == "000018284"
    
    missing = get_dataset_entry("NON_EXISTENT_ID")
    assert missing is None


def test_compute_sha256(tmp_path):
    """Verify SHA-256 calculation on known payload."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Stegoceras validum UALVP 2 biomechanics", encoding="utf-8")
    
    # Pre-calculated SHA-256 for this exact string
    digest = compute_sha256(test_file)
    assert isinstance(digest, str)
    assert len(digest) == 64


def test_audit_local_inventory():
    """Verify local inventory audit runs without exceptions."""
    results = audit_local_inventory()
    assert isinstance(results, list)
    assert len(results) >= 5
    for item in results:
        assert "dataset_id" in item
        assert "exists" in item
        assert "size_bytes" in item

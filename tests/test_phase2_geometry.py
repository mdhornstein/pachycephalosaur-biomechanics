"""Automated tests for Phase 2: Geometry Inventory, Topology Validation, Assembly, and Symmetry."""

from pathlib import Path
import pandas as pd
import pytest
import trimesh
import numpy as np

from stegoceras_biomechanics.geometry.inventory import (
    analyze_mesh_file,
    build_full_geometry_inventory,
    compute_boundary_and_manifold_edges
)
from stegoceras_biomechanics.geometry.assembly import (
    load_all_component_meshes,
    assemble_components,
    compare_assembly_with_whole_skull,
    evaluate_component_containment_and_proximity,
    evaluate_bilateral_symmetry
)
from stegoceras_biomechanics.io.manifest import compute_sha256


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_geometry_inventory_exists_and_complete(project_root: Path):
    """Verify geometry_inventory.csv contains 33 items with all required columns and valid metrics."""
    csv_path = project_root / "data" / "metadata" / "geometry_inventory.csv"
    assert csv_path.exists(), "geometry_inventory.csv must exist."
    
    df = pd.read_csv(csv_path)
    assert len(df) == 33, f"Expected 33 meshes in inventory, got {len(df)}"
    
    required_cols = [
        "media_id", "element_name", "side", "sha256_checksum",
        "unique_vertex_count", "face_count", "is_watertight",
        "boundary_edges", "non_manifold_edges",
        "bbox_min_x", "bbox_min_y", "bbox_min_z",
        "bbox_max_x", "bbox_max_y", "bbox_max_z",
        "extent_dx", "extent_dy", "extent_dz",
        "centroid_x", "centroid_y", "centroid_z",
        "surface_area"
    ]
    for col in required_cols:
        assert col in df.columns, f"Missing required column: {col}"
        
    assert (df["unique_vertex_count"] > 0).all()
    assert (df["face_count"] > 0).all()
    assert (df["surface_area"] > 0).all()
    assert (df["extent_dx"] > 0).all()


def test_whole_skull_mesh_integrity(project_root: Path):
    """Verify Whole Skull STL exists, has verified SHA-256 digest and valid geometry."""
    skull_path = project_root / "data" / "meshes" / "original" / "whole_skull" / "WitmerLab_Stegoceras_UALVP2-000018284.stl"
    assert skull_path.exists(), "Whole skull STL must exist."
    
    sha256 = compute_sha256(skull_path)
    expected_sha256 = "aa994f41df3a7763a048f93339345dd68ea91f475386b8ae129ec80fd226c7c3"
    assert sha256 == expected_sha256, f"SHA-256 mismatch: {sha256} != {expected_sha256}"
    
    res = analyze_mesh_file(skull_path, media_id="000018284", element_name="Whole Skull", side="Complete")
    assert res["face_count"] == 1200102
    assert res["unique_vertex_count"] == 599948
    assert res["non_manifold_edges"] == 2


def test_component_assembly_coordinate_congruence(project_root: Path):
    """Verify that the 32-component assembly bounding box matches the whole skull to within 0.05 units."""
    skull_path = project_root / "data" / "meshes" / "original" / "whole_skull" / "WitmerLab_Stegoceras_UALVP2-000018284.stl"
    components_dir = project_root / "data" / "meshes" / "original" / "components"
    
    skull_mesh = trimesh.load(str(skull_path), process=False)
    components_dict = load_all_component_meshes(components_dir)
    assert len(components_dict) == 32, f"Expected 32 component meshes, got {len(components_dict)}"
    
    assembly_mesh = assemble_components(components_dict)
    assert len(assembly_mesh.faces) == 1426145
    
    # Check bounding box deltas
    sk_min, sk_max = skull_mesh.bounds[0], skull_mesh.bounds[1]
    as_min, as_max = assembly_mesh.bounds[0], assembly_mesh.bounds[1]
    
    np.testing.assert_allclose(as_min, sk_min, atol=0.05, err_msg="Assembly min bounds do not match whole skull.")
    np.testing.assert_allclose(as_max, sk_max, atol=0.05, err_msg="Assembly max bounds do not match whole skull.")


def test_surface_distance_and_bilateral_symmetry(project_root: Path):
    """Verify distance evaluation and bilateral symmetry analysis across 14 cranial bone pairs."""
    skull_path = project_root / "data" / "meshes" / "original" / "whole_skull" / "WitmerLab_Stegoceras_UALVP2-000018284.stl"
    components_dir = project_root / "data" / "meshes" / "original" / "components"
    inventory_path = project_root / "data" / "metadata" / "geometry_inventory.csv"
    
    inventory_df = pd.read_csv(inventory_path)
    skull_mesh = trimesh.load(str(skull_path), process=False)
    components_dict = load_all_component_meshes(components_dir)
    assembly_mesh = assemble_components(components_dict)
    
    metrics = compare_assembly_with_whole_skull(assembly_mesh, skull_mesh, n_samples=5000)
    assert metrics["mean_dist_whole_to_assembly"] < 5.0
    assert metrics["median_dist_whole_to_assembly"] < 3.0
    
    sym_df = evaluate_bilateral_symmetry(inventory_df, components_dict, skull_mesh, n_samples=1000)
    assert len(sym_df) == 14, f"Expected 14 paired elements, got {len(sym_df)}"
    assert (sym_df["mean_symmetry_deviation"] > 0).all()

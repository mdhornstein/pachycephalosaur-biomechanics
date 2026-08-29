"""Test 3D surface mesh loading, topological checks, and scale inspection."""

from pathlib import Path
import pytest
import numpy as np
import trimesh

from stegoceras_biomechanics.geometry.mesh_ops import (
    inspect_mesh_topology,
    standardize_and_export_mesh,
    load_surface_mesh,
)


@pytest.fixture
def sample_box_mesh(tmp_path):
    """Create a sample watertight box mesh (180mm x 120mm x 90mm, representing Stegoceras skull bounds)."""
    box = trimesh.creation.box(extents=[180.0, 120.0, 90.0])
    mesh_path = tmp_path / "sample_skull_box.ply"
    box.export(str(mesh_path))
    return mesh_path


def test_inspect_mesh_topology(sample_box_mesh):
    """Verify topological calculation and scale inference on known geometry."""
    mesh = load_surface_mesh(sample_box_mesh)
    metrics = inspect_mesh_topology(mesh)
    
    assert metrics["num_vertices"] == 8 or metrics["num_vertices"] > 0
    assert metrics["num_faces"] == 12 or metrics["num_faces"] > 0
    assert metrics["is_watertight"] is True
    assert metrics["euler_characteristic"] == 2
    assert metrics["num_connected_components"] == 1
    
    # Check bounding extents
    extents = metrics["extents_xyz"]
    assert np.isclose(extents[0], 180.0, atol=1e-3)
    assert np.isclose(extents[1], 120.0, atol=1e-3)
    assert np.isclose(extents[2], 90.0, atol=1e-3)
    
    # Scale inference for 180mm should be millimeters
    assert "millimeters" in metrics["inferred_physical_unit"]
    
    # Volume of 180 * 120 * 90 = 1,944,000 mm^3
    expected_vol = 180.0 * 120.0 * 90.0
    assert np.isclose(metrics["enclosed_volume"], expected_vol, rtol=1e-3)


def test_standardize_and_export_mesh(sample_box_mesh, tmp_path):
    """Verify non-destructive mesh export and scaling."""
    mesh = load_surface_mesh(sample_box_mesh)
    out_path = tmp_path / "cleaned" / "standardized_skull.ply"
    
    res_path = standardize_and_export_mesh(mesh, out_path, target_unit_scale=1.0)
    assert res_path.exists()
    assert res_path == out_path
    
    # Verify original file was not altered
    orig_mesh = load_surface_mesh(sample_box_mesh)
    assert np.isclose(orig_mesh.extents[0], 180.0, atol=1e-3)

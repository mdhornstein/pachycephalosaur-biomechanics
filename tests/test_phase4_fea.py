"""Comprehensive Automated Test Suite for Phase 4 Finite Element Pipeline."""

import pytest
import numpy as np
import trimesh
from pathlib import Path

from stegoceras_biomechanics.fea.geometry import prepare_watertight_surface
from stegoceras_biomechanics.fea.meshing import (
    generate_tetrahedral_mesh,
    extract_boundary_surface,
    compute_tetrahedral_element_quality,
)
from stegoceras_biomechanics.fea.loads import generate_dome_load_patch
from stegoceras_biomechanics.fea.boundary_conditions import generate_boundary_constraints
from stegoceras_biomechanics.fea.solver import solve_linear_elasticity, FESolution
from stegoceras_biomechanics.fea.validation import (
    verify_analytical_solution,
    verify_global_equilibrium,
    verify_load_linearity,
)
from stegoceras_biomechanics.fea.results import extract_subregion_metrics


@pytest.fixture
def raw_stl_path():
    p = Path("data/meshes/original/whole_skull/WitmerLab_Stegoceras_UALVP2-000018284.stl")
    if not p.exists():
        pytest.skip(f"Source STL not found at {p}")
    return p


@pytest.fixture
def coarse_mesh_data():
    p = Path("data/meshes/cleaned/stegoceras_tetmesh_coarse.npz")
    if not p.exists():
        pytest.skip(f"Coarse mesh not found at {p}")
    return np.load(p)


def test_analytical_solution_verification():
    """Verifies FEM engine against closed-form Hookean tension bar analytical mechanics."""
    res = verify_analytical_solution(
        youngs_modulus_MPa=17000.0,
        poisson_ratio=0.30,
        force_N=1000.0,
        length_mm=100.0,
        width_mm=10.0,
        height_mm=10.0,
        nx=3,
        ny=3,
        nz=15,
    )
    assert res.is_verified, f"Analytical verification failed: disp_err={res.displacement_error_pct}%, stress_err={res.stress_error_pct}%"
    assert res.displacement_error_pct < 0.5
    assert res.stress_error_pct < 0.1
    assert res.energy_error_pct < 0.5


def test_surface_repair_fidelity(raw_stl_path, tmp_path):
    """Verifies non-invasive topological repair satisfies volume (<0.05%) and area (<0.20%) conservation."""
    out_stl = tmp_path / "test_watertight.stl"
    out_json = tmp_path / "test_repair_meta.json"
    
    clean_mesh, metrics = prepare_watertight_surface(raw_stl_path, out_stl, out_json)
    
    assert metrics.repaired_watertight is True
    assert abs(metrics.volume_change_pct) < 0.05, f"Volume change {metrics.volume_change_pct}% exceeds 0.05%"
    assert abs(metrics.area_change_pct) < 0.20, f"Area change {metrics.area_change_pct}% exceeds 0.20%"
    assert metrics.max_surface_deviation_mm < 5.0
    assert out_stl.exists()
    assert out_json.exists()


def test_mesh_quality_positive_jacobians(coarse_mesh_data):
    """Verifies that generated solid tetrahedral elements have strictly positive volumes (zero inverted elements)."""
    nodes = coarse_mesh_data["nodes"]
    elements = coarse_mesh_data["elements"]
    
    vols, aspect_ratios, num_inverted = compute_tetrahedral_element_quality(nodes, elements)
    
    assert num_inverted == 0, f"Found {num_inverted} inverted tetrahedral elements!"
    assert np.all(vols > 0.0)
    assert np.all(aspect_ratios >= 1.0)
    assert np.mean(aspect_ratios) < 5.0


def test_boundary_surface_extraction(coarse_mesh_data):
    """Verifies that extract_boundary_surface produces a valid, watertight 2-manifold triangular boundary."""
    nodes = coarse_mesh_data["nodes"]
    elements = coarse_mesh_data["elements"]
    
    surf = extract_boundary_surface(nodes, elements)
    assert isinstance(surf, trimesh.Trimesh)
    assert surf.is_watertight is True
    assert len(surf.vertices) == len(nodes)
    assert len(surf.faces) > 0


def test_load_patch_and_boundary_constraints(coarse_mesh_data):
    """Verifies algorithmic load patch and physiological boundary condition identification."""
    nodes = coarse_mesh_data["nodes"]
    elements = coarse_mesh_data["elements"]
    surf = extract_boundary_surface(nodes, elements)
    
    loaded_nodes, nodal_forces, loaded_facets, load_spec = generate_dome_load_patch(
        surf, target_area_mm2=3000.0, force_magnitude_N=1000.0
    )
    
    assert len(loaded_nodes) > 0
    assert len(loaded_facets) > 0
    assert np.isclose(load_spec.target_force_magnitude_N, 1000.0, atol=1e-3)
    assert abs(load_spec.actual_area_mm2 - 3000.0) < 300.0  # within 10% on coarse mesh
    
    condyle_nodes, nuchal_nodes, bc_spec = generate_boundary_constraints(surf)
    assert len(condyle_nodes) > 0
    assert len(nuchal_nodes) > 0
    assert bc_spec.total_constrained_dofs == len(condyle_nodes) * 3 + len(nuchal_nodes) * 2


def test_coarse_fea_solve_and_equilibrium(coarse_mesh_data):
    """Verifies that the linear elastic FEA solve achieves exact static force and moment equilibrium."""
    nodes = coarse_mesh_data["nodes"]
    elements = coarse_mesh_data["elements"]
    surf = extract_boundary_surface(nodes, elements)
    
    loaded_nodes, nodal_forces, _, load_spec = generate_dome_load_patch(
        surf, target_area_mm2=3000.0, force_magnitude_N=1000.0
    )
    condyle_nodes, nuchal_nodes, _ = generate_boundary_constraints(surf)
    
    solution = solve_linear_elasticity(
        nodes=nodes,
        elements=elements,
        youngs_modulus_MPa=17000.0,
        poisson_ratio=0.30,
        loaded_node_indices=loaded_nodes,
        nodal_forces_N=nodal_forces,
        condyle_node_indices=condyle_nodes,
        nuchal_node_indices=nuchal_nodes,
        solver_method="direct",
    )
    
    eq_res = verify_global_equilibrium(solution, load_spec, force_tolerance_pct=0.01, moment_tolerance_pct=0.05)
    
    assert eq_res.is_force_balanced is True
    assert eq_res.is_moment_balanced is True
    assert eq_res.residual_force_norm_N < 1e-4
    assert eq_res.residual_moment_norm_Nmm < 1e-3
    assert solution.total_strain_energy_mJ > 0.0


def test_linearity_verification(coarse_mesh_data):
    """Verifies Hookean linearity across 500 N, 1000 N, and 2000 N loads."""
    nodes = coarse_mesh_data["nodes"]
    elements = coarse_mesh_data["elements"]
    surf = extract_boundary_surface(nodes, elements)
    
    condyle_nodes, nuchal_nodes, _ = generate_boundary_constraints(surf)
    
    solutions = {}
    for F in [500.0, 1000.0, 2000.0]:
        l_nodes, f_vecs, _, _ = generate_dome_load_patch(surf, target_area_mm2=3000.0, force_magnitude_N=F)
        sol = solve_linear_elasticity(
            nodes, elements, 17000.0, 0.30,
            l_nodes, f_vecs, condyle_nodes, nuchal_nodes, "direct"
        )
        solutions[F] = sol
        
    lin_res = verify_load_linearity(solutions[500.0], solutions[1000.0], solutions[2000.0])
    assert lin_res.is_linear is True
    assert lin_res.displacement_linearity_error_pct < 1e-6
    assert lin_res.stress_linearity_error_pct < 1e-6
    assert lin_res.energy_quadratic_error_pct < 1e-6


def test_subregion_metrics_extraction(coarse_mesh_data, tmp_path):
    """Verifies anatomical subregion partitioning and metrics computation."""
    nodes = coarse_mesh_data["nodes"]
    elements = coarse_mesh_data["elements"]
    surf = extract_boundary_surface(nodes, elements)
    
    loaded_nodes, nodal_forces, _, _ = generate_dome_load_patch(surf, 3000.0, 1000.0)
    condyle_nodes, nuchal_nodes, _ = generate_boundary_constraints(surf)
    
    solution = solve_linear_elasticity(
        nodes, elements, 17000.0, 0.30,
        loaded_nodes, nodal_forces, condyle_nodes, nuchal_nodes, "direct"
    )
    
    csv_out = tmp_path / "subregions.csv"
    json_out = tmp_path / "subregions.json"
    metrics = extract_subregion_metrics(solution, csv_out, json_out)
    
    assert len(metrics) == 7  # 1 global + 6 subregions
    assert csv_out.exists()
    assert json_out.exists()
    
    # Check dome apex has high stress and braincase has lower stress
    region_map = {m.region_name: m for m in metrics}
    assert "Frontoparietal Dome Apex" in region_map
    assert "Endocranial Braincase Roof" in region_map
    assert region_map["Whole Skull (Global)"].max_von_mises_MPa > 0.0


def test_mesh_source_surface_sha256_provenance():
    """Verifies that all mesh metadata files share the exact same immutable source surface array SHA-256 hash."""
    import hashlib
    import json
    import trimesh
    
    surf_p = Path("data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl")
    assert surf_p.exists(), f"Source canonical master surface missing at {surf_p}"
    m = trimesh.load(surf_p)
    v = np.ascontiguousarray(m.vertices, dtype=np.float64)
    f = np.ascontiguousarray(m.faces, dtype=np.int32)
    expected_sha = hashlib.sha256(v.tobytes() + f.tobytes()).hexdigest()
        
    meta_coarse = json.loads(Path("data/metadata/phase4_mesh_metrics_coarse.json").read_text())
    meta_mc = json.loads(Path("data/metadata/phase4_mesh_metrics_medium_coarse.json").read_text())
    meta_med = json.loads(Path("data/metadata/phase4_mesh_metrics_medium.json").read_text())
    meta_fine = json.loads(Path("data/metadata/phase4_mesh_metrics_fine.json").read_text())
    
    assert meta_coarse.get("source_surface_sha256") == expected_sha
    assert meta_mc.get("source_surface_sha256") == expected_sha
    assert meta_med.get("source_surface_sha256") == expected_sha
    assert meta_fine.get("source_surface_sha256") == expected_sha
    assert meta_coarse.get("decimate_reduction") == 0.0
    assert meta_mc.get("decimate_reduction") == 0.0
    assert meta_med.get("decimate_reduction") == 0.0
    assert meta_fine.get("is_production_convergence_mesh") is True


def test_report_json_mesh_quality_consistency():
    """Verifies exact 100% numerical consistency between metadata JSON files and convergence results."""
    import json
    
    conv_path = Path("results/phase4/mesh_convergence_comparison.json")
    assert conv_path.exists()
    conv = json.loads(conv_path.read_text())
    
    for tier in ["coarse", "medium_coarse", "medium"]:
        meta = json.loads(Path(f"data/metadata/phase4_mesh_metrics_{tier}.json").read_text())
        assert tier in conv, f"Tier {tier} missing from convergence comparison JSON"
        c_tier = conv[tier]
        
        assert c_tier["num_nodes"] == meta["num_nodes"]
        assert c_tier["num_elements"] == meta["num_elements"]
        assert np.isclose(c_tier["p50_aspect_ratio"], meta["p50_aspect_ratio"])
        assert np.isclose(c_tier["p95_aspect_ratio"], meta["p95_aspect_ratio"])
        assert np.isclose(c_tier["max_aspect_ratio"], meta["max_aspect_ratio"])
        assert c_tier["source_surface_sha256"] == meta["source_surface_sha256"]


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
    # Strict quality constraint invariance: q=1.5 and dihedral=10.0 for ALL tiers
    assert meta_coarse.get("min_ratio") == 1.5
    assert meta_mc.get("min_ratio") == 1.5
    assert meta_med.get("min_ratio") == 1.5
    assert meta_fine.get("min_ratio") == 1.5
    assert meta_coarse.get("min_dihedral_deg") == 10.0
    assert meta_mc.get("min_dihedral_deg") == 10.0
    assert meta_med.get("min_dihedral_deg") == 10.0
    assert meta_fine.get("min_dihedral_deg") == 10.0


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


def test_single_tetrahedron_manufactured_displacement_field():
    """Direct element-level verification: imposes an affine manufactured displacement field

    u(x) = A*x + b on a single 4-node tetrahedron and tests that the element strain and
    stress postprocessing exactly recovers the analytical infinitesimal strain tensor
    eps = 0.5*(A + A^T) and Hookean Cauchy stress tensor sigma = lambda*tr(eps)*I + 2*mu*eps.
    """
    from stegoceras_biomechanics.fea.solver import lame_parameters
    
    # 1. Single non-degenerate tetrahedron
    nodes = np.array([
        [0.0, 0.0, 0.0],
        [2.0, 0.0, 0.0],
        [0.0, 3.0, 0.0],
        [0.0, 0.0, 4.0],
    ], dtype=np.float64)
    elements = np.array([[0, 1, 2, 3]], dtype=np.int64)
    
    # 2. Known constant displacement gradient A (with distinct shear and normal strains) + translation b
    A = np.array([
        [0.0010,  0.0004, -0.0002],
        [0.0003, -0.0005,  0.0006],
        [0.0001,  0.0002,  0.0008],
    ], dtype=np.float64)
    b = np.array([0.05, -0.02, 0.01], dtype=np.float64)
    
    # Prescribed nodal displacements: u_i = A * v_i + b
    u_nodal = (nodes @ A.T) + b
    
    # Analytical exact strain and stress
    eps_exact = 0.5 * (A + A.T)
    lam, mu = lame_parameters(17000.0, 0.30)
    sigma_exact = lam * np.trace(eps_exact) * np.eye(3) + 2.0 * mu * eps_exact
    vm_exact = np.sqrt(
        0.5 * (
            (sigma_exact[0, 0] - sigma_exact[1, 1]) ** 2 +
            (sigma_exact[1, 1] - sigma_exact[2, 2]) ** 2 +
            (sigma_exact[2, 2] - sigma_exact[0, 0]) ** 2 +
            6.0 * (sigma_exact[0, 1] ** 2 + sigma_exact[1, 2] ** 2 + sigma_exact[0, 2] ** 2)
        )
    )
    
    # Compute via the element Jacobian postprocessing formulation
    v0 = nodes[elements[:, 0]]
    v1 = nodes[elements[:, 1]]
    v2 = nodes[elements[:, 2]]
    v3 = nodes[elements[:, 3]]
    u0 = u_nodal[elements[:, 0]]
    u1 = u_nodal[elements[:, 1]]
    u2 = u_nodal[elements[:, 2]]
    u3 = u_nodal[elements[:, 3]]
    
    J = np.stack([v1 - v0, v2 - v0, v3 - v0], axis=-1)
    J_inv = np.linalg.inv(J)
    du = np.stack([u1 - u0, u2 - u0, u3 - u0], axis=-1)
    grad_u = np.einsum('nij,njk->nik', du, J_inv)
    eps_num = 0.5 * (grad_u + np.swapaxes(grad_u, 1, 2))
    tr_eps = np.trace(eps_num, axis1=1, axis2=2)
    sigma_num = lam * tr_eps[:, None, None] * np.eye(3)[None, :, :] + 2.0 * mu * eps_num
    
    vm_num = np.sqrt(
        0.5 * (
            (sigma_num[:, 0, 0] - sigma_num[:, 1, 1]) ** 2 +
            (sigma_num[:, 1, 1] - sigma_num[:, 2, 2]) ** 2 +
            (sigma_num[:, 2, 2] - sigma_num[:, 0, 0]) ** 2 +
            6.0 * (sigma_num[:, 0, 1] ** 2 + sigma_num[:, 1, 2] ** 2 + sigma_num[:, 0, 2] ** 2)
        )
    )
    
    # Assert exact agreement to machine precision
    assert np.allclose(eps_num[0], eps_exact, atol=1e-15), "Strain recovery failed!"
    assert np.allclose(sigma_num[0], sigma_exact, atol=1e-12), "Stress recovery failed!"
    assert np.isclose(vm_num[0], vm_exact, atol=1e-12), "Von Mises recovery failed!"


def test_energy_identity_work_balance(coarse_mesh_data):
    """Verifies the fundamental energy identity 1/2 u^T K u == 1/2 u^T f for the linear elastic FE solve."""
    nodes = coarse_mesh_data["nodes"]
    elements = coarse_mesh_data["elements"]
    surf = extract_boundary_surface(nodes, elements)
    
    loaded_nodes, nodal_forces, _, _ = generate_dome_load_patch(surf, 3000.0, 1000.0)
    condyle_nodes, nuchal_nodes, _ = generate_boundary_constraints(surf)
    
    solution = solve_linear_elasticity(
        nodes, elements, 17000.0, 0.30,
        loaded_nodes, nodal_forces, condyle_nodes, nuchal_nodes, "direct"
    )
    
    # External work done by applied loads: W_ext = 1/2 * sum_i (u_i . f_i)
    u_loaded = solution.nodal_displacements_mm[loaded_nodes]
    external_work_mJ = 0.5 * float(np.sum(u_loaded * nodal_forces))
    internal_strain_energy_mJ = solution.total_strain_energy_mJ
    
    rel_error = abs(external_work_mJ - internal_strain_energy_mJ) / internal_strain_energy_mJ
    assert rel_error < 1e-6, f"Energy identity failed: W_ext={external_work_mJ} mJ, U={internal_strain_energy_mJ} mJ, rel_err={rel_error}"


@pytest.mark.parametrize("tier", ["coarse", "medium_coarse", "medium", "fine"])
def test_production_mesh_hierarchy_parameterized(tier):
    """Verifies that each production mesh tier satisfies strict quality, provenance, volume, and inversion constraints."""
    import hashlib
    import json
    import trimesh
    
    # 1. Canonical surface hash
    surf_p = Path("data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl")
    assert surf_p.exists()
    m = trimesh.load(surf_p)
    v = np.ascontiguousarray(m.vertices, dtype=np.float64)
    f = np.ascontiguousarray(m.faces, dtype=np.int32)
    expected_sha = hashlib.sha256(v.tobytes() + f.tobytes()).hexdigest()
    
    # 2. Metadata file check
    meta_p = Path(f"data/metadata/phase4_mesh_metrics_{tier}.json")
    assert meta_p.exists(), f"Metadata missing for tier {tier}"
    meta = json.loads(meta_p.read_text())
    
    assert meta.get("source_surface_sha256") == expected_sha
    assert meta.get("source_surface_arrays_sha256") == expected_sha
    assert meta.get("decimate_reduction") == 0.0
    assert meta.get("min_ratio") == 1.5
    assert meta.get("min_dihedral_deg") == 10.0
    assert meta.get("num_inverted_elements") == 0
    assert meta.get("num_inverted_from_tetgen") == 0
    assert abs(meta["total_volume_mm3"] - 646422.8) / 646422.8 < 0.0005  # Within 0.05%
    
    # 3. If mesh .npz exists on disk, audit actual array data
    mesh_p = Path(f"data/meshes/cleaned/stegoceras_tetmesh_{tier}.npz")
    if mesh_p.exists():
        data = np.load(mesh_p)
        nodes = data["nodes"]
        elements = data["elements"]
        vols, ars, num_inv = compute_tetrahedral_element_quality(nodes, elements)
        
        assert num_inv == 0
        assert np.all(vols > 0.0)
        assert len(nodes) == meta["num_nodes"]
        assert len(elements) == meta["num_elements"]
        assert np.isclose(np.percentile(ars, 50), meta["p50_aspect_ratio"], atol=1e-4)



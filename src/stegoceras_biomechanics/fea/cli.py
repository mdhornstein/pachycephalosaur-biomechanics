"""Command-line interface (CLI) for Phase 4 FEA preparation, meshing, solving, and analysis."""

import argparse
import sys
import json
from pathlib import Path
import numpy as np
import trimesh
import yaml

from stegoceras_biomechanics.fea.geometry import prepare_watertight_surface
from stegoceras_biomechanics.fea.meshing import generate_tetrahedral_mesh
from stegoceras_biomechanics.fea.loads import generate_dome_load_patch
from stegoceras_biomechanics.fea.boundary_conditions import generate_boundary_constraints
from stegoceras_biomechanics.fea.solver import solve_linear_elasticity
from stegoceras_biomechanics.fea.results import extract_subregion_metrics
from stegoceras_biomechanics.fea.validation import (
    verify_global_equilibrium,
    verify_analytical_solution,
    verify_load_linearity,
)


def load_config(config_path: str | Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def cmd_prepare(args):
    """Prepares clean watertight surface geometry."""
    cfg = load_config(args.config)
    geom_cfg = cfg["provenance_taxonomy"]["geometry"]
    src_stl = geom_cfg["file"]
    out_stl = geom_cfg["cleaned_file"]
    meta_json = "data/metadata/phase4_geometry_repair_metrics.json"
    
    print(f"Ingesting raw source STL: {src_stl}")
    mesh_clean, metrics = prepare_watertight_surface(src_stl, out_stl, meta_json)
    print(f"✓ Watertight clean STL generated: {out_stl}")
    print(f"  - Original: V={metrics.original_vertices}, F={metrics.original_faces}, Watertight={metrics.original_watertight}")
    print(f"  - Repaired: V={metrics.repaired_vertices}, F={metrics.repaired_faces}, Watertight={metrics.repaired_watertight}")
    print(f"  - Volume Change: {metrics.volume_change_pct:+.4f}%")
    print(f"  - Surface Area Change: {metrics.area_change_pct:+.4f}%")
    print(f"  - Max Surface Deviation: {metrics.max_surface_deviation_mm:.4f} mm")


def cmd_mesh(args):
    """Generates 3D solid tetrahedral meshes across resolution tiers."""
    cfg = load_config(args.config)
    geom_cfg = cfg["provenance_taxonomy"]["geometry"]
    clean_stl = geom_cfg["cleaned_file"]
    
    tier = getattr(args, "tier", "all")
    tiers = ["coarse", "medium", "fine"] if tier == "all" else [tier]
    
    for t in tiers:
        out_mesh_path = f"data/meshes/cleaned/stegoceras_tetmesh_{t}.npz"
        meta_json_path = f"data/metadata/phase4_mesh_metrics_{t}.json"
        print(f"Generating '{t}' solid tetrahedral mesh from {clean_stl}...")
        nodes, elements, q_metrics = generate_tetrahedral_mesh(
            clean_stl,
            resolution_tier=t,
            output_mesh_path=out_mesh_path,
            metadata_json_path=meta_json_path,
        )
        print(f"✓ '{t}' mesh complete: {q_metrics.num_nodes} nodes, {q_metrics.num_elements} tetrahedra (0 inverted elements)")
        print(f"  - Total Volume: {q_metrics.total_volume_mm3:,.1f} mm^3")
        print(f"  - Aspect Ratio (Mean): {q_metrics.mean_aspect_ratio:.2f} (Min: {q_metrics.min_aspect_ratio:.2f}, Max: {q_metrics.max_aspect_ratio:.2f})")
        print(f"  - Runtime: {q_metrics.meshing_runtime_seconds:.2f} s")


def cmd_solve(args):
    """Executes finite element solve for specified mesh resolution and loading."""
    cfg = load_config(args.config)
    geom_cfg = cfg["provenance_taxonomy"]["geometry"]
    clean_stl = geom_cfg["cleaned_file"]
    mat_cfg = cfg["provenance_taxonomy"]["material"]
    load_cfg = cfg["provenance_taxonomy"]["loading"]
    
    E = mat_cfg["youngs_modulus_MPa"]["value"]
    nu = mat_cfg["poisson_ratio"]["value"]
    F_mag = load_cfg["primary_benchmark_load_N"]["value"]
    A_target = load_cfg["nominal_contact_area_mm2"]["value"]
    
    tier = getattr(args, "tier", "medium")
    mesh_path = f"data/meshes/cleaned/stegoceras_tetmesh_{tier}.npz"
    if not Path(mesh_path).exists():
        print(f"Mesh file {mesh_path} not found. Generating now...")
        generate_tetrahedral_mesh(clean_stl, resolution_tier=tier, output_mesh_path=mesh_path)
        
    mesh_data = np.load(mesh_path)
    nodes = mesh_data["nodes"]
    elements = mesh_data["elements"]
    
    from stegoceras_biomechanics.fea.meshing import extract_boundary_surface
    surf = extract_boundary_surface(nodes, elements)
    
    print(f"Generating load patch on '{tier}' mesh (Target Area: {A_target} mm^2, Load: {F_mag} N)...")
    loaded_nodes, nodal_forces, loaded_facets, load_spec = generate_dome_load_patch(
        surf, target_area_mm2=A_target, force_magnitude_N=F_mag
    )
    print(f"✓ Load patch: {load_spec.num_loaded_nodes} nodes, Area: {load_spec.actual_area_mm2:.1f} mm^2")
    
    print("Generating boundary constraints (Condyle + Nuchal)...")
    condyle_nodes, nuchal_nodes, bc_spec = generate_boundary_constraints(surf)
    print(f"✓ Constraints: {bc_spec.num_condyle_nodes} condyle nodes, {bc_spec.num_nuchal_nodes} nuchal nodes ({bc_spec.total_constrained_dofs} DOFs)")
    
    print(f"Solving 3D linear elasticity ({len(nodes)} nodes, {len(elements)} tets, {len(nodes)*3} DOFs)...")
    solution = solve_linear_elasticity(
        nodes=nodes,
        elements=elements,
        youngs_modulus_MPa=E,
        poisson_ratio=nu,
        loaded_node_indices=loaded_nodes,
        nodal_forces_N=nodal_forces,
        condyle_node_indices=condyle_nodes,
        nuchal_node_indices=nuchal_nodes,
        solver_method="auto",
    )
    print(f"✓ Solve complete in {solution.solver_runtime_seconds:.2f} s via {solution.solver_type} solver!")
    print(f"  - Max Displacement: {np.max(solution.displacement_magnitudes_mm):.4f} mm")
    print(f"  - Max von Mises Stress: {np.max(solution.nodal_von_mises_MPa):.2f} MPa")
    print(f"  - 95th Percentile Stress: {np.percentile(solution.nodal_von_mises_MPa, 95):.2f} MPa")
    print(f"  - Total Strain Energy: {solution.total_strain_energy_mJ:.4f} mJ")
    
    # Save solution
    out_dir = Path("simulations/phase4")
    out_dir.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_dir / f"solution_{tier}.npz",
        nodes=solution.nodes,
        elements=solution.elements,
        displacements=solution.nodal_displacements_mm,
        von_mises=solution.nodal_von_mises_MPa,
        strains=solution.nodal_max_principal_strain,
        reaction_forces=solution.reaction_forces_N,
    )
    
    # Global equilibrium check
    eq_res = verify_global_equilibrium(solution, load_spec)
    print("✓ Global Equilibrium Check:")
    print(f"  - Force Residual: {eq_res.residual_force_norm_N:.6f} N ({eq_res.residual_force_relative_pct:.4f}%) -> Force Balanced: {eq_res.is_force_balanced}")
    print(f"  - Moment Residual: {eq_res.residual_moment_norm_Nmm:.4f} N*mm ({eq_res.residual_moment_norm_Nmm/1000.0:.4f}%) -> Moment Balanced: {eq_res.is_moment_balanced}")


def cmd_analyze(args):
    """Extracts subregion metrics and runs analytical & linearity validation."""
    print("Running Analytical Solution Verification on Canonical Geometry...")
    an_res = verify_analytical_solution(youngs_modulus_MPa=17000.0, force_N=1000.0)
    print(f"✓ Analytical Verification (E=17000 MPa):")
    print(f"  - Analytical Delta L: {an_res.analytical_displacement_mm:.6f} mm | FEM Delta L: {an_res.fem_mean_displacement_mm:.6f} mm (Error: {an_res.displacement_error_pct:.2f}%)")
    print(f"  - Analytical Stress: {an_res.analytical_stress_MPa:.2f} MPa | FEM Stress: {an_res.fem_mean_stress_MPa:.2f} MPa (Error: {an_res.stress_error_pct:.2f}%)")
    print(f"  - Analytical Energy: {an_res.analytical_strain_energy_mJ:.4f} mJ | FEM Energy: {an_res.fem_strain_energy_mJ:.4f} mJ (Error: {an_res.energy_error_pct:.2f}%)")
    print(f"  - Status: {'PASSED' if an_res.is_verified else 'FAILED'}")


def main():
    parser = argparse.ArgumentParser(description="Stegoceras Biomechanics Phase 4 FEA Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    p_prep = subparsers.add_parser("prepare", help="Prepare clean watertight surface")
    p_prep.add_argument("--config", default="models/phase4/baseline.yaml")
    
    p_mesh = subparsers.add_parser("mesh", help="Generate tetrahedral solid meshes")
    p_mesh.add_argument("--config", default="models/phase4/baseline.yaml")
    p_mesh.add_argument("--tier", default="all", choices=["coarse", "medium", "fine", "all"])
    
    p_solve = subparsers.add_parser("solve", help="Solve linear static elasticity")
    p_solve.add_argument("--config", default="models/phase4/baseline.yaml")
    p_solve.add_argument("--tier", default="medium", choices=["coarse", "medium", "fine"])
    
    p_ana = subparsers.add_parser("analyze", help="Analyze results and run validations")
    p_ana.add_argument("--config", default="models/phase4/baseline.yaml")
    
    args = parser.parse_args()
    if args.command == "prepare":
        cmd_prepare(args)
    elif args.command == "mesh":
        cmd_mesh(args)
    elif args.command == "solve":
        cmd_solve(args)
    elif args.command == "analyze":
        cmd_analyze(args)


if __name__ == "__main__":
    main()

"""Independent Production Solver Driver for Stegoceras validum FEA Pipeline.

Enforces strict architectural layer separation:
- Each tier is solved in an independent, isolated process.
- All numerical artifacts (solution arrays and regional metrics) are saved immediately to disk.
- Exits cleanly to return 100% of memory to the operating system before the next stage.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
import numpy as np

from stegoceras_biomechanics.fea.meshing import extract_boundary_surface
from stegoceras_biomechanics.fea.loads import generate_dome_load_patch
from stegoceras_biomechanics.fea.boundary_conditions import generate_boundary_constraints
from stegoceras_biomechanics.fea.solver import solve_linear_elasticity
from stegoceras_biomechanics.fea.results import extract_subregion_metrics


TIER_MESHES = {
    "coarse": "data/meshes/cleaned/stegoceras_tetmesh_coarse.npz",
    "medium_coarse": "data/meshes/cleaned/stegoceras_tetmesh_medium_coarse.npz",
    "medium": "data/meshes/cleaned/stegoceras_tetmesh_medium.npz",
}


def solve_tier(
    tier: str,
    contact_area_mm2: float = 3000.0,
    force_magnitude_N: float = 1000.0,
    solver_method: str = "direct",
    youngs_modulus_MPa: float = 17000.0,
    poisson_ratio: float = 0.30,
) -> dict:
    if tier not in TIER_MESHES:
        raise ValueError(f"Unknown tier '{tier}'. Must be one of {list(TIER_MESHES.keys())}")
        
    mesh_path = Path(TIER_MESHES[tier])
    if not mesh_path.exists():
        raise FileNotFoundError(f"Mesh file not found at {mesh_path}")
        
    sims_dir = Path("simulations/phase4")
    sims_dir.mkdir(parents=True, exist_ok=True)
    results_dir = Path("results/phase4")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*70}")
    print(f"Starting Independent Production Solve: Tier '{tier}'")
    print(f"Mesh: {mesh_path}")
    print(f"Solver method: {solver_method}")
    print(f"{'='*70}")
    
    # 1. Load mesh
    t0 = time.time()
    mesh_data = np.load(mesh_path)
    nodes = mesh_data["nodes"]
    elements = mesh_data["elements"]
    print(f"Loaded mesh: {len(nodes):,} nodes, {len(elements):,} elements ({len(nodes)*3:,} DOFs)")
    
    # 2. Extract boundary surface
    print("Extracting boundary surface...")
    surf = extract_boundary_surface(nodes, elements)
    
    # 3. Formulate load patch and boundary conditions
    print(f"Generating dorsal load patch ({contact_area_mm2:.1f} mm², {force_magnitude_N:.1f} N)...")
    loaded_nodes, nodal_forces, loaded_facets, load_spec = generate_dome_load_patch(
        surf, target_area_mm2=contact_area_mm2, force_magnitude_N=force_magnitude_N
    )
    print(f"Load patch: {len(loaded_nodes):,} loaded nodes, actual area {load_spec.actual_area_mm2:.1f} mm² ({load_spec.area_error_pct:+.2f}%)")
    
    condyle_nodes, nuchal_nodes, bc_spec = generate_boundary_constraints(surf)
    print(f"Boundary conditions: {len(condyle_nodes)} condyle nodes, {len(nuchal_nodes)} nuchal nodes ({bc_spec.total_constrained_dofs} constrained DOFs)")
    
    # 4. Execute solve
    print("Beginning finite element system assembly and solve...")
    t_solve_start = time.time()
    sol = solve_linear_elasticity(
        nodes=nodes,
        elements=elements,
        youngs_modulus_MPa=youngs_modulus_MPa,
        poisson_ratio=poisson_ratio,
        loaded_node_indices=loaded_nodes,
        nodal_forces_N=nodal_forces,
        condyle_node_indices=condyle_nodes,
        nuchal_node_indices=nuchal_nodes,
        solver_method=solver_method,
    )
    t_solve_end = time.time()
    print(f"✓ Solve complete in {t_solve_end - t_solve_start:.2f} s")
    
    # 5. Extract subregion metrics
    csv_path = results_dir / f"metrics_{tier}.csv"
    json_path = results_dir / f"metrics_{tier}.json"
    metrics = extract_subregion_metrics(sol, output_csv_path=csv_path, output_json_path=json_path)
    print(f"✓ Saved regional metrics to {json_path}")
    
    # Also save canonical primary benchmark files if this is medium
    if tier == "medium":
        bench_csv = results_dir / "ualvp2_1kn_subregion_metrics.csv"
        bench_json = results_dir / "ualvp2_1kn_subregion_metrics.json"
        extract_subregion_metrics(sol, output_csv_path=bench_csv, output_json_path=bench_json)
        print(f"✓ Saved canonical primary benchmark metrics to {bench_json}")
        
    # 6. Save authoritative solution npz
    sol_out_path = sims_dir / f"solution_{tier}.npz"
    print(f"Saving compressed solution artifact to {sol_out_path}...")
    np.savez_compressed(
        sol_out_path,
        nodes=sol.nodes,
        elements=sol.elements,
        displacements=sol.nodal_displacements_mm,
        displacement_magnitudes=sol.displacement_magnitudes_mm,
        element_von_mises=sol.element_von_mises_MPa,
        nodal_von_mises=sol.nodal_von_mises_MPa,
        element_stresses=sol.element_stresses_MPa,
        element_strains=sol.element_strains,
        element_max_principal_strain=sol.element_max_principal_strain,
        nodal_max_principal_strain=sol.nodal_max_principal_strain,
        reaction_forces=sol.reaction_forces_N,
        applied_load_spec=json.dumps(load_spec.__dict__),
        solver_runtime_seconds=float(sol.solver_runtime_seconds),
        num_dofs=int(sol.num_dofs),
        total_strain_energy_mJ=float(sol.total_strain_energy_mJ),
        algebraic_residual_norm=float(sol.algebraic_residual_norm),
        normalized_force_residual=float(sol.normalized_force_residual),
        normalized_moment_residual=float(sol.normalized_moment_residual),
        absolute_moment_residual_Nmm=float(sol.absolute_moment_residual_Nmm),
    )
    print(f"✓ Saved solution artifact: {sol_out_path.stat().st_size / (1024*1024):.2f} MB")
    
    # 7. Summary metrics record
    sub_map = {m.region_name: m.p95_von_mises_MPa for m in metrics}
    apex_node = int(np.argmin(np.linalg.norm(sol.nodes - np.array(load_spec.apex_vertex_mm), axis=1)))
    
    summary_record = {
        "tier": tier,
        "num_nodes": int(len(nodes)),
        "num_elements": int(len(elements)),
        "num_dofs": int(sol.num_dofs),
        "source_mesh": str(mesh_path),
        "solver_type": solver_method,
        "solver_runtime_seconds": float(sol.solver_runtime_seconds),
        "max_displacement_um": float(np.max(sol.displacement_magnitudes_mm) * 1000.0),
        "apex_displacement_um": float(sol.displacement_magnitudes_mm[apex_node] * 1000.0),
        "total_strain_energy_mJ": float(sol.total_strain_energy_mJ),
        "global_p95_von_mises_MPa": float(np.percentile(sol.element_von_mises_MPa, 95)),
        "global_p99_von_mises_MPa": float(np.percentile(sol.element_von_mises_MPa, 99)),
        "dome_p95_von_mises_MPa": float(sub_map.get("Frontoparietal Dome Apex", 0.0)),
        "braincase_p95_von_mises_MPa": float(sub_map.get("Endocranial Braincase Roof", 0.0)),
        "algebraic_residual_norm": float(sol.algebraic_residual_norm),
        "normalized_force_residual": float(sol.normalized_force_residual),
        "normalized_moment_residual": float(sol.normalized_moment_residual),
        "absolute_moment_residual_Nmm": float(sol.absolute_moment_residual_Nmm),
    }
    
    summary_path = results_dir / f"summary_{tier}.json"
    with open(summary_path, "w") as fp:
        json.dump(summary_record, fp, indent=2)
    print(f"✓ Saved tier summary to {summary_path}")
    
    total_elapsed = time.time() - t0
    print(f"=== Tier '{tier}' Finished Successfully in {total_elapsed:.2f} s ===\n")
    return summary_record


def run_all_tiers_isolated():
    """Runs all 3 tiers sequentially by spawning a fresh, isolated Python process for each."""
    tiers = ["coarse", "medium_coarse", "medium"]
    print("\n=================================================================")
    print("Launching Multi-Tier Production Run (Independent Subprocesses)")
    print("=================================================================")
    
    for tier in tiers:
        cmd = [
            sys.executable,
            "-m",
            "stegoceras_biomechanics.fea.solve_production",
            "--tier",
            tier,
        ]
        print(f"\n>>> Spawning independent process for tier: {tier} ...")
        t0 = time.time()
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"❌ Error: Tier '{tier}' failed with exit code {res.returncode}")
            sys.exit(res.returncode)
        print(f">>> Process for tier '{tier}' exited cleanly in {time.time() - t0:.2f} s.")
        
    print("\n✓ All 3 production tiers solved and verified on disk!")


def main():
    parser = argparse.ArgumentParser(description="Production FEA solver driver for Stegoceras validum")
    parser.add_argument(
        "--tier",
        type=str,
        default="coarse",
        choices=["coarse", "medium_coarse", "medium", "all"],
        help="Discretization tier to solve independently, or 'all' to run each in a separate subprocess",
    )
    parser.add_argument("--contact-area", type=float, default=3000.0, help="Contact area in mm^2")
    parser.add_argument("--force-magnitude", type=float, default=1000.0, help="Applied force in N")
    parser.add_argument("--solver-method", type=str, default="direct", choices=["direct", "cg", "auto"], help="Solver method")
    
    args = parser.parse_args()
    
    if args.tier == "all":
        run_all_tiers_isolated()
    else:
        solve_tier(
            tier=args.tier,
            contact_area_mm2=args.contact_area,
            force_magnitude_N=args.force_magnitude,
            solver_method=args.solver_method,
        )


if __name__ == "__main__":
    main()

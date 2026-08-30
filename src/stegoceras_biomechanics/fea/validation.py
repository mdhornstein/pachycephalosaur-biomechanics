"""Finite Element verification, static equilibrium checks, analytical benchmark tests, and linearity validation."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np
import skfem as fem
from stegoceras_biomechanics.fea.solver import solve_linear_elasticity, FESolution


@dataclass
class EquilibriumCheckResult:
    applied_force_N: list[float]
    reaction_force_N: list[float]
    residual_force_N: list[float]
    residual_force_norm_N: float
    residual_force_relative_pct: float
    applied_moment_Nmm: list[float]
    reaction_moment_Nmm: list[float]
    residual_moment_Nmm: list[float]
    residual_moment_norm_Nmm: float
    reference_point_mm: list[float]
    is_force_balanced: bool
    is_moment_balanced: bool


@dataclass
class AnalyticalVerificationResult:
    benchmark_name: str
    youngs_modulus_MPa: float
    applied_force_N: float
    length_mm: float
    area_mm2: float
    analytical_displacement_mm: float
    fem_mean_displacement_mm: float
    displacement_error_pct: float
    analytical_stress_MPa: float
    fem_mean_stress_MPa: float
    stress_error_pct: float
    analytical_strain_energy_mJ: float
    fem_strain_energy_mJ: float
    energy_error_pct: float
    is_verified: bool


@dataclass
class LinearityValidationResult:
    force_cases_N: list[float]
    max_displacements_mm: list[float]
    p95_stresses_MPa: list[float]
    total_strain_energies_mJ: float
    displacement_linearity_error_pct: float
    stress_linearity_error_pct: float
    energy_quadratic_error_pct: float
    is_linear: bool


def verify_global_equilibrium(
    solution: FESolution,
    applied_load_spec,
    force_tolerance_pct: float = 0.01,
    moment_tolerance_pct: float = 0.05,
) -> EquilibriumCheckResult:
    """Verifies complete static force and moment equilibrium: Sum(F) = 0 and Sum(M) = 0."""
    f_applied = np.array(solution.applied_force_total_N, dtype=np.float64)
    f_reaction = np.array(solution.reaction_force_total_N, dtype=np.float64)
    r_force = f_applied + f_reaction
    
    m_applied = np.array(applied_load_spec.applied_moment_Nmm, dtype=np.float64)
    m_reaction = np.array(solution.reaction_moment_total_Nmm, dtype=np.float64)
    r_moment = m_applied + m_reaction
    
    force_mag = np.linalg.norm(f_applied)
    res_force_norm = float(np.linalg.norm(r_force))
    rel_force_err = (res_force_norm / force_mag) * 100.0 if force_mag > 0 else 0.0
    
    res_moment_norm = float(np.linalg.norm(r_moment))
    # Characteristic moment arm ~ 100 mm
    ref_moment = force_mag * 100.0
    rel_moment_err = (res_moment_norm / ref_moment) * 100.0 if ref_moment > 0 else 0.0
    
    is_f_bal = rel_force_err <= force_tolerance_pct
    is_m_bal = rel_moment_err <= moment_tolerance_pct
    
    return EquilibriumCheckResult(
        applied_force_N=f_applied.tolist(),
        reaction_force_N=f_reaction.tolist(),
        residual_force_N=r_force.tolist(),
        residual_force_norm_N=res_force_norm,
        residual_force_relative_pct=float(rel_force_err),
        applied_moment_Nmm=m_applied.tolist(),
        reaction_moment_Nmm=m_reaction.tolist(),
        residual_moment_Nmm=r_moment.tolist(),
        residual_moment_norm_Nmm=res_moment_norm,
        reference_point_mm=applied_load_spec.reference_point_mm,
        is_force_balanced=bool(is_f_bal),
        is_moment_balanced=bool(is_m_bal),
    )


def verify_analytical_solution(
    youngs_modulus_MPa: float = 17000.0,
    poisson_ratio: float = 0.30,
    force_N: float = 1000.0,
    length_mm: float = 100.0,
    width_mm: float = 10.0,
    height_mm: float = 10.0,
    nx: int = 5,
    ny: int = 5,
    nz: int = 21,
) -> AnalyticalVerificationResult:
    """Analytical solution verification on a 3D bar under uniaxial tension.
    
    Compares 3D linear elasticity FE solution against exact 1D Hookean mechanics:
    - Delta L = F * L / (E * A)
    - Sigma = F / A
    - U = 1/2 * F * Delta L
    """
    area = width_mm * height_mm
    u_exact = (force_N * length_mm) / (youngs_modulus_MPa * area)
    sigma_exact = force_N / area
    energy_exact = 0.5 * force_N * u_exact
    
    # Generate structured tetrahedral mesh for the bar
    mesh = fem.MeshTet1.init_tensor(
        np.linspace(0, width_mm, nx),
        np.linspace(0, height_mm, ny),
        np.linspace(0, length_mm, nz),
    )
    nodes = mesh.p.T
    elements = mesh.t.T
    
    # Fixed base at z = 0
    fixed_node_indices = np.where(np.isclose(nodes[:, 2], 0.0))[0]
    
    # Loaded face at z = L
    loaded_node_indices = np.where(np.isclose(nodes[:, 2], length_mm))[0]
    f_per_node = np.array([0.0, 0.0, force_N / len(loaded_node_indices)])
    nodal_forces = np.tile(f_per_node, (len(loaded_node_indices), 1))
    
    # Solve
    sol = solve_linear_elasticity(
        nodes=nodes,
        elements=elements,
        youngs_modulus_MPa=youngs_modulus_MPa,
        poisson_ratio=poisson_ratio,
        loaded_node_indices=loaded_node_indices,
        nodal_forces_N=nodal_forces,
        condyle_node_indices=fixed_node_indices,  # fixed in all 3 directions
        solver_method="direct",
    )
    
    # Extract tip displacement in Z
    fem_u_tip = np.mean(sol.nodal_displacements_mm[loaded_node_indices, 2])
    disp_err = abs(fem_u_tip - u_exact) / u_exact * 100.0
    
    # Extract mean axial stress in middle section (away from Poisson boundary constraint effects)
    mid_elems = np.where(
        (np.mean(nodes[elements][:, :, 2], axis=1) >= 0.3 * length_mm) &
        (np.mean(nodes[elements][:, :, 2], axis=1) <= 0.7 * length_mm)
    )[0]
    fem_sigma_zz = np.mean(sol.element_stresses_MPa[mid_elems, 2, 2])
    stress_err = abs(fem_sigma_zz - sigma_exact) / sigma_exact * 100.0
    
    energy_err = abs(sol.total_strain_energy_mJ - energy_exact) / energy_exact * 100.0
    
    is_verified = (disp_err < 5.0) and (stress_err < 2.0)
    
    return AnalyticalVerificationResult(
        benchmark_name=f"Uniaxial Tension Bar (E={youngs_modulus_MPa:.0f} MPa)",
        youngs_modulus_MPa=float(youngs_modulus_MPa),
        applied_force_N=float(force_N),
        length_mm=float(length_mm),
        area_mm2=float(area),
        analytical_displacement_mm=float(u_exact),
        fem_mean_displacement_mm=float(fem_u_tip),
        displacement_error_pct=float(disp_err),
        analytical_stress_MPa=float(sigma_exact),
        fem_mean_stress_MPa=float(fem_sigma_zz),
        stress_error_pct=float(stress_err),
        analytical_strain_energy_mJ=float(energy_exact),
        fem_strain_energy_mJ=float(sol.total_strain_energy_mJ),
        energy_error_pct=float(energy_err),
        is_verified=bool(is_verified),
    )


def verify_load_linearity(
    solution_500: FESolution,
    solution_1000: FESolution,
    solution_2000: FESolution,
) -> LinearityValidationResult:
    """Verifies that displacement, stress, and strain energy obey strict linear-elastic scaling."""
    u500 = solution_500.nodal_displacements_mm
    u1000 = solution_1000.nodal_displacements_mm
    u2000 = solution_2000.nodal_displacements_mm
    
    s500 = solution_500.element_von_mises_MPa
    s1000 = solution_1000.element_von_mises_MPa
    s2000 = solution_2000.element_von_mises_MPa
    
    e500 = solution_500.total_strain_energy_mJ
    e1000 = solution_1000.total_strain_energy_mJ
    e2000 = solution_2000.total_strain_energy_mJ
    
    # u(2000) should equal 2 * u(1000)
    disp_err = float(np.max(np.abs(u2000 - 2.0 * u1000)) / np.max(np.abs(u2000)) * 100.0)
    # sigma(2000) should equal 2 * sigma(1000)
    stress_err = float(np.max(np.abs(s2000 - 2.0 * s1000)) / np.max(np.abs(s2000)) * 100.0)
    # U(2000) should equal 4 * U(1000)
    energy_err = float(abs(e2000 - 4.0 * e1000) / e2000 * 100.0)
    
    is_linear = (disp_err < 0.01) and (stress_err < 0.01) and (energy_err < 0.01)
    
    return LinearityValidationResult(
        force_cases_N=[500.0, 1000.0, 2000.0],
        max_displacements_mm=[
            float(np.max(solution_500.displacement_magnitudes_mm)),
            float(np.max(solution_1000.displacement_magnitudes_mm)),
            float(np.max(solution_2000.displacement_magnitudes_mm)),
        ],
        p95_stresses_MPa=[
            float(np.percentile(solution_500.nodal_von_mises_MPa, 95)),
            float(np.percentile(solution_1000.nodal_von_mises_MPa, 95)),
            float(np.percentile(solution_2000.nodal_von_mises_MPa, 95)),
        ],
        total_strain_energies_mJ=[e500, e1000, e2000],
        displacement_linearity_error_pct=disp_err,
        stress_linearity_error_pct=stress_err,
        energy_quadratic_error_pct=energy_err,
        is_linear=bool(is_linear),
    )

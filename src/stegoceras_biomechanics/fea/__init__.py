"""Finite Element Analysis (FEA) module for Stegoceras validum (UALVP 2) biomechanics."""

from stegoceras_biomechanics.fea.geometry import prepare_watertight_surface
from stegoceras_biomechanics.fea.meshing import generate_tetrahedral_mesh, MeshQualityMetrics
from stegoceras_biomechanics.fea.loads import generate_dome_load_patch, AppliedLoadSpecification
from stegoceras_biomechanics.fea.boundary_conditions import generate_boundary_constraints, BoundaryConditionSpecification
from stegoceras_biomechanics.fea.solver import solve_linear_elasticity, FESolution
from stegoceras_biomechanics.fea.results import partition_anatomical_subregions, extract_subregion_metrics
from stegoceras_biomechanics.fea.validation import verify_global_equilibrium, verify_analytical_solution, verify_load_linearity

__all__ = [
    "prepare_watertight_surface",
    "generate_tetrahedral_mesh",
    "MeshQualityMetrics",
    "generate_dome_load_patch",
    "AppliedLoadSpecification",
    "generate_boundary_constraints",
    "BoundaryConditionSpecification",
    "solve_linear_elasticity",
    "FESolution",
    "partition_anatomical_subregions",
    "extract_subregion_metrics",
    "verify_global_equilibrium",
    "verify_analytical_solution",
    "verify_load_linearity",
]

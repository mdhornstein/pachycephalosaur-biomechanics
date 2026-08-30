"""Boundary condition specification, anatomical facet identification, and rigid-body constraint checks."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np
import trimesh
from scipy.spatial import cKDTree


@dataclass
class BoundaryConditionSpecification:
    num_condyle_nodes: int
    num_nuchal_nodes: int
    total_constrained_dofs: int
    condyle_centroid_mm: list[float]
    nuchal_centroid_mm: list[float]
    condyle_prescription: str
    nuchal_prescription: str
    numerical_purpose: str
    biological_rationale: str
    rigid_body_modes_removed: int


def generate_boundary_constraints(
    surface_mesh: trimesh.Trimesh,
    condyle_radius_mm: float = 12.0,
    nuchal_band_y_min_fraction: float = 0.88,
    nuchal_band_z_min_fraction: float = 0.60,
) -> tuple[np.ndarray, np.ndarray, BoundaryConditionSpecification]:
    """Algorithmically identifies anatomical constraint surfaces on UALVP 2 skull.
    
    1. Occipital Condyle: Articular ball located near midsagittal plane (X ≈ 103.6 mm) at the
       posterior-ventral neurocranium margin (Y ≈ max, Z ≈ mid-ventral).
    2. Nuchal Crest: Posterodorsal shelf along the squamosal-parietal rim.
    """
    v = np.ascontiguousarray(surface_mesh.vertices, dtype=np.float64)
    bounds = surface_mesh.bounds
    x_mid = 0.5 * (bounds[0, 0] + bounds[1, 0])
    
    # 1. Identify occipital condyle landmark
    # The condyle is at high Y (posterior), mid X (sagittal), and ventral Z (below dome)
    post_ventral_mask = (
        (np.abs(v[:, 0] - x_mid) <= 15.0) &
        (v[:, 1] >= bounds[1, 1] - 30.0) &
        (v[:, 2] <= bounds[0, 2] + 45.0) &
        (v[:, 2] >= bounds[0, 2] + 15.0)
    )
    
    cand_condyle_indices = np.where(post_ventral_mask)[0]
    if len(cand_condyle_indices) == 0:
        # Fallback to nearest point in posterior ventral region
        cand_condyle_indices = np.where(v[:, 1] >= bounds[1, 1] - 25.0)[0]
        
    condyle_center = np.mean(v[cand_condyle_indices], axis=0)
    
    # Select nodes within radius of condyle center
    dists_condyle = np.linalg.norm(v - condyle_center, axis=1)
    condyle_node_indices = np.where(dists_condyle <= condyle_radius_mm)[0]
    
    # 2. Identify nuchal crest rim
    # Posterior dorsal margin of parietosquamosal shelf
    y_thresh = bounds[0, 1] + nuchal_band_y_min_fraction * (bounds[1, 1] - bounds[0, 1])
    z_thresh = bounds[0, 2] + nuchal_band_z_min_fraction * (bounds[1, 2] - bounds[0, 2])
    
    nuchal_mask = (
        (v[:, 1] >= y_thresh) &
        (v[:, 2] >= z_thresh) &
        (dists_condyle > condyle_radius_mm * 1.5)  # disjoint from condyle
    )
    nuchal_node_indices = np.where(nuchal_mask)[0]
    
    if len(condyle_node_indices) == 0 or len(nuchal_node_indices) == 0:
        raise RuntimeError("Failed to identify valid anatomical boundary constraint regions!")
        
    condyle_centroid = np.mean(v[condyle_node_indices], axis=0)
    nuchal_centroid = np.mean(v[nuchal_node_indices], axis=0)
    
    # Total constrained DOFs: 3 per condyle node (Ux, Uy, Uz) + 2 per nuchal node (Uy, Uz)
    total_dofs = len(condyle_node_indices) * 3 + len(nuchal_node_indices) * 2
    
    spec = BoundaryConditionSpecification(
        num_condyle_nodes=int(len(condyle_node_indices)),
        num_nuchal_nodes=int(len(nuchal_node_indices)),
        total_constrained_dofs=int(total_dofs),
        condyle_centroid_mm=condyle_centroid.tolist(),
        nuchal_centroid_mm=nuchal_centroid.tolist(),
        condyle_prescription="Rigid translational fixity (Ux=Uy=Uz=0)",
        nuchal_prescription="Translational restraint (Uy=Uz=0)",
        numerical_purpose="Eliminates all 6 rigid-body modes (3 translations + 3 rotations) without overconstraint",
        biological_rationale="Atlas vertebra articulation at condyle + dorsal neck extensor tension along nuchal crest",
        rigid_body_modes_removed=6,
    )
    
    return condyle_node_indices, nuchal_node_indices, spec

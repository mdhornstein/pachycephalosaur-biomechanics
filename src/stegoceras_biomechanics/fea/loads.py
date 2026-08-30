"""Algorithmic load patch definition and force distribution for FEA modeling."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np
import trimesh
from scipy.spatial import cKDTree


@dataclass
class AppliedLoadSpecification:
    target_force_magnitude_N: float
    actual_force_vector_N: list[float]
    force_direction_unit_vector: list[float]
    target_area_mm2: float
    actual_area_mm2: float
    area_error_pct: float
    patch_radius_mm: float
    patch_centroid_mm: list[float]
    apex_vertex_mm: list[float]
    num_loaded_nodes: int
    num_loaded_facets: int
    reference_point_mm: list[float]
    applied_moment_Nmm: list[float]


def generate_dome_load_patch(
    surface_mesh: trimesh.Trimesh,
    target_area_mm2: float = 3000.0,
    area_tolerance_pct: float = 2.0,
    force_magnitude_N: float = 1000.0,
    force_direction: list[float] | np.ndarray = (0.0, 0.0, -1.0),
    reference_point: list[float] | np.ndarray | None = None,
    min_normal_z: float = 0.3,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, AppliedLoadSpecification]:
    """Algorithmically generates a reproducible dorsal load patch on the frontoparietal dome.
    
    1. Identifies the morphological apex vertex v_apex = argmax_z (v_i) on the dorsal skull.
    2. Uses bisection search on radius r to find a contiguous patch of dorsal-facing facets (n_z >= min_normal_z)
       matching target_area_mm2 within area_tolerance_pct.
    3. Fails loudly if target area is unachievable under geometric constraints.
    4. Computes tributary nodal forces and applied moments about the reference point.
    """
    v = np.ascontiguousarray(surface_mesh.vertices, dtype=np.float64)
    f = np.ascontiguousarray(surface_mesh.faces, dtype=np.int32)
    face_normals = surface_mesh.face_normals
    face_areas = surface_mesh.area_faces
    face_centroids = surface_mesh.triangles_center
    
    # 1. Identify the anatomical frontoparietal dome apex
    # The frontoparietal dome is located along the midsagittal plane (X ≈ 98.5 mm)
    # between anteroposterior limits Y ∈ [80, 150] mm and dorsal elevation Z > 80 mm.
    dome_mask = (v[:, 1] >= 80.0) & (v[:, 1] <= 150.0) & (v[:, 2] >= 80.0)
    dome_center_x = 0.5 * (np.min(v[dome_mask, 0]) + np.max(v[dome_mask, 0]))
    dome_center_y = 0.5 * (np.min(v[dome_mask, 1]) + np.max(v[dome_mask, 1]))
    
    cand_indices = np.where(dome_mask & (np.abs(v[:, 0] - dome_center_x) <= 20.0))[0]
    apex_idx = cand_indices[np.argmax(v[cand_indices, 2])]
    v_apex = v[apex_idx]
    
    # Candidate faces with dorsal outward normal
    dorsal_mask = (face_normals[:, 2] >= min_normal_z) & (face_centroids[:, 1] >= 75.0) & (face_centroids[:, 1] <= 155.0)
    if np.sum(face_areas[dorsal_mask]) < target_area_mm2:
        raise ValueError(
            f"Total available dorsal surface area ({np.sum(face_areas[dorsal_mask]):.1f} mm^2) "
            f"is less than requested target patch area ({target_area_mm2:.1f} mm^2)!"
        )
        
    # 2. Bisection search on radius r from dome center
    dists_from_center = np.linalg.norm(face_centroids[:, :2] - np.array([dome_center_x, dome_center_y]), axis=1)
    
    r_low = 1.0
    r_high = 100.0
    best_facets = None
    best_area = 0.0
    best_r = 0.0
    
    for _ in range(30):
        r_mid = 0.5 * (r_low + r_high)
        selected_facets = np.where(dorsal_mask & (dists_from_center <= r_mid))[0]
        cur_area = float(np.sum(face_areas[selected_facets]))
        
        err_pct = abs(cur_area - target_area_mm2) / target_area_mm2 * 100.0
        if err_pct <= area_tolerance_pct:
            best_facets = selected_facets
            best_area = cur_area
            best_r = r_mid
            break
            
        if cur_area < target_area_mm2:
            r_low = r_mid
        else:
            r_high = r_mid
            best_facets = selected_facets
            best_area = cur_area
            best_r = r_mid
            
    if best_facets is None or len(best_facets) == 0:
        raise RuntimeError(f"Failed to find a valid load patch matching {target_area_mm2} mm^2!")
        
    area_error_pct = (best_area - target_area_mm2) / target_area_mm2 * 100.0
    
    # 3. Extract loaded nodes and calculate tributary areas
    patch_nodes_unique = np.unique(f[best_facets].flatten())
    nodal_tributary_areas = np.zeros(len(patch_nodes_unique), dtype=np.float64)
    node_to_idx = {node_id: i for i, node_id in enumerate(patch_nodes_unique)}
    
    for facet_id in best_facets:
        f_nodes = f[facet_id]
        f_area_third = face_areas[facet_id] / 3.0
        for nid in f_nodes:
            nodal_tributary_areas[node_to_idx[nid]] += f_area_third
            
    total_trib_area = np.sum(nodal_tributary_areas)
    
    # Normalize force vector
    dir_vec = np.array(force_direction, dtype=np.float64)
    dir_unit = dir_vec / np.linalg.norm(dir_vec)
    
    # Distributed nodal force vectors: F_i = dir_unit * F_total * (A_i / A_total)
    nodal_forces = np.outer(nodal_tributary_areas / total_trib_area * force_magnitude_N, dir_unit)
    
    # Verification: sum of applied forces
    total_force_vec = np.sum(nodal_forces, axis=0)
    assert np.isclose(np.linalg.norm(total_force_vec), force_magnitude_N, rtol=1e-5), (
        f"Force magnitude mismatch: {np.linalg.norm(total_force_vec)} != {force_magnitude_N}"
    )
    
    # Calculate moments about reference point
    if reference_point is None:
        ref_pt = np.mean(v, axis=0)  # Skull centroid
    else:
        ref_pt = np.array(reference_point, dtype=np.float64)
        
    r_arms = v[patch_nodes_unique] - ref_pt
    applied_moments = np.sum(np.cross(r_arms, nodal_forces), axis=0)
    
    patch_centroid = np.average(face_centroids[best_facets], axis=0, weights=face_areas[best_facets])
    
    spec = AppliedLoadSpecification(
        target_force_magnitude_N=float(force_magnitude_N),
        actual_force_vector_N=total_force_vec.tolist(),
        force_direction_unit_vector=dir_unit.tolist(),
        target_area_mm2=float(target_area_mm2),
        actual_area_mm2=float(best_area),
        area_error_pct=float(area_error_pct),
        patch_radius_mm=float(best_r),
        patch_centroid_mm=patch_centroid.tolist(),
        apex_vertex_mm=v_apex.tolist(),
        num_loaded_nodes=int(len(patch_nodes_unique)),
        num_loaded_facets=int(len(best_facets)),
        reference_point_mm=ref_pt.tolist(),
        applied_moment_Nmm=applied_moments.tolist(),
    )
    
    return patch_nodes_unique, nodal_forces, best_facets, spec

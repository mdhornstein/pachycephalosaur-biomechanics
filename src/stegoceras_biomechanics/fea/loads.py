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


import heapq
from collections import defaultdict


def generate_dome_load_patch(
    surface_mesh: trimesh.Trimesh,
    target_area_mm2: float = 3000.0,
    force_magnitude_N: float = 1000.0,
    area_tolerance_pct: float = 2.0,
    force_direction: list[float] | np.ndarray = (0.0, 0.0, -1.0),
    reference_point: list[float] | np.ndarray | None = None,
    min_elevation_z: float = 80.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, AppliedLoadSpecification]:
    """Algorithmically generates a reproducible dorsal load patch on the frontoparietal dome.
    
    1. Identifies the morphological apex vertex v_apex on the dorsal skull within |X - X_mid| <= 6 mm.
    2. Uses geodesic dual-graph wavefront propagation (Dijkstra algorithm along face adjacency)
       originating from the apex seed facet to find a contiguous patch of exterior dorsal facets
       (Z >= min_elevation_z mm) matching target_area_mm2 within area_tolerance_pct.
    3. Guarantees 100% topological connectivity (single connected component) and 0% ventral penetration.
    4. Computes tributary nodal forces and applied moments about the reference point.
    """
    v = np.ascontiguousarray(surface_mesh.vertices, dtype=np.float64)
    f = np.ascontiguousarray(surface_mesh.faces, dtype=np.int32)
    face_normals = surface_mesh.face_normals
    face_areas = surface_mesh.area_faces
    face_centroids = surface_mesh.triangles_center
    
    # 1. Identify the anatomical frontoparietal dome apex
    bounds = surface_mesh.bounds
    x_mid = 0.5 * (bounds[0, 0] + bounds[1, 0])
    
    cand_indices = np.where(
        (v[:, 1] >= 80.0) & (v[:, 1] <= 150.0) & (v[:, 2] >= min_elevation_z) & (np.abs(v[:, 0] - x_mid) <= 6.0)
    )[0]
    if len(cand_indices) == 0:
        cand_indices = np.where((v[:, 1] >= 80.0) & (v[:, 1] <= 150.0) & (v[:, 2] >= min_elevation_z))[0]
    if len(cand_indices) == 0:
        raise RuntimeError("Failed to locate candidate apex vertices on dorsal cranium!")
        
    apex_idx = cand_indices[np.argmax(v[cand_indices, 2])]
    v_apex = v[apex_idx]
    
    # Select seed facet incident to apex vertex with dorsal normal orientation
    apex_faces = np.where((f[:, 0] == apex_idx) | (f[:, 1] == apex_idx) | (f[:, 2] == apex_idx))[0]
    dorsal_apex_faces = [fi for fi in apex_faces if face_normals[fi, 2] >= 0.2]
    if len(dorsal_apex_faces) == 0:
        dorsal_apex_faces = apex_faces
    seed_face = dorsal_apex_faces[np.argmax(face_centroids[dorsal_apex_faces, 2])]
    
    # 2. Build dorsal surface dual-graph for geodesic wavefront propagation
    face_adj = surface_mesh.face_adjacency
    adj = defaultdict(list)
    z_floor = min_elevation_z - 5.0  # slight buffer for facet centroids
    
    for (f1, f2) in face_adj:
        if (face_centroids[f1, 2] >= z_floor and face_centroids[f2, 2] >= z_floor and
            face_centroids[f1, 1] >= 65.0 and face_centroids[f1, 1] <= 165.0 and
            face_centroids[f2, 1] >= 65.0 and face_centroids[f2, 1] <= 165.0):
            cost = float(np.linalg.norm(face_centroids[f1] - face_centroids[f2]))
            adj[f1].append((f2, cost))
            adj[f2].append((f1, cost))
            
    # Dijkstra propagation from seed face
    dist = {seed_face: 0.0}
    pq = [(0.0, seed_face)]
    visited = set()
    
    while pq:
        d_val, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v_nbr, cost in adj[u]:
            if d_val + cost < dist.get(v_nbr, float("inf")):
                dist[v_nbr] = d_val + cost
                heapq.heappush(pq, (d_val + cost, v_nbr))
                
    # Sort reachable faces by geodesic distance from apex seed face
    sorted_faces = sorted(dist.keys(), key=lambda x: dist[x])
    
    cum_area = 0.0
    selected_facets_list = []
    for fi in sorted_faces:
        selected_facets_list.append(fi)
        cum_area += float(face_areas[fi])
        if cum_area >= target_area_mm2:
            break
            
    selected_facets = np.array(selected_facets_list, dtype=np.int32)
    if len(selected_facets) == 0:
        raise RuntimeError("Geodesic propagation failed to acquire facets for load patch!")
        
    area_error_pct = (cum_area - target_area_mm2) / target_area_mm2 * 100.0
    if abs(area_error_pct) > area_tolerance_pct:
        raise ValueError(
            f"Achieved area {cum_area:.2f} mm^2 deviates from target {target_area_mm2:.2f} mm^2 "
            f"by {area_error_pct:.2f}%, exceeding tolerance {area_tolerance_pct:.2f}%!"
        )
        
    patch_nodes_unique = np.unique(f[selected_facets].flatten())
    
    # Verify patch topological connectivity (single connected component)
    submesh = surface_mesh.submesh([selected_facets], append=True)
    comps = trimesh.graph.connected_components(submesh.face_adjacency)
    if len(comps) != 1:
        raise RuntimeError(f"Load patch failed connectivity assertion: found {len(comps)} connected components!")
        
    # Verify strict dorsal elevation constraint: 100% of loaded nodes have Z >= min_elevation_z
    min_z = float(np.min(v[patch_nodes_unique, 2]))
    if min_z < min_elevation_z:
        raise RuntimeError(f"Load patch penetrated below Z={min_elevation_z} mm (min Z = {min_z:.2f} mm)!")
        
    # 3. Extract loaded nodes and calculate tributary areas
    nodal_tributary_areas = np.zeros(len(patch_nodes_unique), dtype=np.float64)
    node_to_idx = {node_id: i for i, node_id in enumerate(patch_nodes_unique)}
    
    for facet_id in selected_facets:
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
    
    patch_centroid = np.average(face_centroids[selected_facets], axis=0, weights=face_areas[selected_facets])
    geodesic_radius = float(dist[selected_facets[-1]])
    
    spec = AppliedLoadSpecification(
        target_force_magnitude_N=float(force_magnitude_N),
        actual_force_vector_N=total_force_vec.tolist(),
        force_direction_unit_vector=dir_unit.tolist(),
        target_area_mm2=float(target_area_mm2),
        actual_area_mm2=float(cum_area),
        area_error_pct=float(area_error_pct),
        patch_radius_mm=float(geodesic_radius),
        patch_centroid_mm=patch_centroid.tolist(),
        apex_vertex_mm=v_apex.tolist(),
        num_loaded_nodes=int(len(patch_nodes_unique)),
        num_loaded_facets=int(len(selected_facets)),
        reference_point_mm=ref_pt.tolist(),
        applied_moment_Nmm=applied_moments.tolist(),
    )
    
    return patch_nodes_unique, nodal_forces, selected_facets, spec

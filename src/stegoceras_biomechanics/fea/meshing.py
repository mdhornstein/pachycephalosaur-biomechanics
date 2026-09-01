"""3D Solid Tetrahedral Mesh Generation and Quality Auditing using TetGen."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import time
import numpy as np
import trimesh
import pyvista as pv
import pymeshfix
import tetgen


def extract_boundary_surface(
    nodes: np.ndarray,
    elements: np.ndarray,
) -> trimesh.Trimesh:
    """Extracts the watertight 2-manifold boundary surface triangular mesh from a 3D tetrahedral mesh."""
    faces = np.vstack([
        elements[:, [0, 1, 2]],
        elements[:, [0, 2, 3]],
        elements[:, [0, 3, 1]],
        elements[:, [1, 3, 2]],
    ])
    faces_sorted = np.sort(faces, axis=1)
    _, idx, counts = np.unique(faces_sorted, axis=0, return_index=True, return_counts=True)
    boundary_faces = faces[idx[counts == 1]]
    return trimesh.Trimesh(vertices=nodes, faces=boundary_faces, process=False)


@dataclass
class MeshQualityMetrics:
    num_nodes: int
    num_elements: int
    element_type: str
    total_volume_mm3: float
    min_element_volume_mm3: float
    max_element_volume_mm3: float
    mean_element_volume_mm3: float
    min_aspect_ratio: float
    p50_aspect_ratio: float
    p90_aspect_ratio: float
    p95_aspect_ratio: float
    p99_aspect_ratio: float
    p99_9_aspect_ratio: float
    max_aspect_ratio: float
    mean_aspect_ratio: float
    num_elements_ar_gt_10: int
    num_elements_ar_gt_50: int
    num_inverted_elements: int
    meshing_runtime_seconds: float
    source_surface_file: str = ""
    source_surface_sha256: str = ""
    source_surface_arrays_sha256: str = ""
    num_inverted_from_tetgen: int = 0
    is_production_convergence_mesh: bool = True
    decimate_reduction: float = 0.0
    min_dihedral_deg: float = 10.0
    min_ratio: float = 1.5
    max_volume_mm3: float | None = None
    tetgen_flags: str = "-pq1.5/10.0"


def compute_tetrahedral_element_quality(
    nodes: np.ndarray,
    elements: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Calculates signed element volumes and normalized aspect ratios for 4-node tetrahedral elements.
    
    Element volume:
        V = (1/6) * det([v1-v0, v2-v0, v3-v0])
    
    Aspect ratio:
        AR = (r_rms^3) / (8.48528137423857 * |V|)
        where r_rms = sqrt((1/6) * sum_{i=1}^6 e_i^2)
        Normalized such that a regular tetrahedron has AR = 1.0.
    
    Returns:
        volumes: (N_elem,) signed volumes
        aspect_ratios: (N_elem,) normalized aspect ratios
        num_inverted: count of elements with volume <= 0
    """
    v0 = nodes[elements[:, 0]]
    v1 = nodes[elements[:, 1]]
    v2 = nodes[elements[:, 2]]
    v3 = nodes[elements[:, 3]]
    
    # 6 edge vectors
    e01 = v1 - v0
    e02 = v2 - v0
    e03 = v3 - v0
    e12 = v2 - v1
    e23 = v3 - v2
    e31 = v1 - v3
    
    # Volume calculation via scalar triple product det([e01, e02, e03])
    det_J = np.einsum('ij,ij->i', e01, np.cross(e02, e03))
    volumes = det_J / 6.0
    
    num_inverted = int(np.sum(volumes <= 0.0))
    abs_volumes = np.abs(volumes)
    abs_volumes = np.maximum(abs_volumes, 1e-15)  # Avoid division by zero
    
    # Sum of squared edge lengths (6 edges per tetrahedron)
    sum_e2 = (
        np.sum(e01**2, axis=1) +
        np.sum(e02**2, axis=1) +
        np.sum(e03**2, axis=1) +
        np.sum(e12**2, axis=1) +
        np.sum(e23**2, axis=1) +
        np.sum(e31**2, axis=1)
    )
    r_rms = np.sqrt(sum_e2 / 6.0)
    
    # Normalized aspect ratio (regular tet = 1.0)
    # Factor 8.48528137423857 = 6 * sqrt(2)
    aspect_ratios = (r_rms**3) / (8.48528137423857 * abs_volumes)
    
    return volumes, aspect_ratios, num_inverted


import hashlib


def generate_tetrahedral_mesh(
    surface_mesh: trimesh.Trimesh | str | Path,
    resolution_tier: str = "medium",
    max_volume: float | None = None,
    min_dihedral: float = 10.0,
    min_ratio: float = 1.5,
    switches: str | None = None,
    output_mesh_path: str | Path | None = None,
    metadata_json_path: str | Path | None = None,
) -> tuple[np.ndarray, np.ndarray, MeshQualityMetrics]:
    """Generates a solid 3D tetrahedral FE mesh directly from an immutable watertight surface geometry.
    
    In strict compliance with discretization-convergence protocols, all production convergence tiers
    are generated directly from the identical canonical surface geometry without per-tier surface
    decimation, ensuring that only volumetric discretization changes.
    
    Supported resolution tiers on canonical master surface:
    - 'coarse': switches="pq1.5/10" -> ~423k tets (99.6k nodes, natural Delaunay base)
    - 'medium_coarse': switches="pq1.5/10a5.0" -> ~540k tets (118.6k nodes, max volume 5.0 mm³)
    - 'medium': switches="pq1.5/10a2.0" -> ~825k tets (166.0k nodes, max volume 2.0 mm³)
    - 'fine': switches="pq1.5/10a1.0" -> ~1.39M tets (max volume 1.0 mm³, 16 GB computational memory boundary)
    """
    start_time = time.time()
    
    source_file_str = ""
    source_sha256 = ""
    if isinstance(surface_mesh, (str, Path)):
        source_file_str = str(surface_mesh)
        p = Path(surface_mesh)
        mesh = trimesh.load(surface_mesh)
    else:
        mesh = surface_mesh
        
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("Expected Trimesh surface geometry")
        
    v = np.ascontiguousarray(mesh.vertices, dtype=np.float64)
    f = np.ascontiguousarray(mesh.faces, dtype=np.int32)
    
    # Deterministic SHA-256 hash of exact canonical vertex and face arrays passed to TetGen
    source_sha256 = hashlib.sha256(v.tobytes() + f.tobytes()).hexdigest()
    
    tier_switch_map = {
        "coarse": "pq1.5/10",
        "medium_coarse": "pq1.5/10a5.0",
        "medium": "pq1.5/10a2.0",
        "fine": "pq1.5/10a1.0",
        "direct_fine": "pq1.5/10",
    }
    
    chosen_switches = switches if switches is not None else tier_switch_map.get(resolution_tier.lower(), f"pq{min_ratio}/{min_dihedral}")
    if max_volume is not None and "a" not in chosen_switches:
        chosen_switches += f"a{max_volume}"
        
    tet = tetgen.TetGen(v, f)
    tet.tetrahedralize(switches=chosen_switches)
    grid = tet.grid
    
    nodes = np.ascontiguousarray(grid.points, dtype=np.float64)
    cells = grid.cells.reshape(-1, 5)[:, 1:5]
    elements = np.ascontiguousarray(cells, dtype=np.int64)
    
    runtime = time.time() - start_time
    
    volumes, aspect_ratios, num_inverted_raw = compute_tetrahedral_element_quality(nodes, elements)
    num_inverted_from_tetgen = int(num_inverted_raw)
    num_inverted_final = num_inverted_from_tetgen
    
    # If any elements have inverted orientation (negative determinant), fix node ordering [0, 1, 2, 3] -> [0, 1, 3, 2]
    if num_inverted_raw > 0:
        inv_mask = volumes < 0.0
        elements[inv_mask, 2], elements[inv_mask, 3] = elements[inv_mask, 3].copy(), elements[inv_mask, 2].copy()
        volumes, aspect_ratios, num_inverted_final = compute_tetrahedral_element_quality(nodes, elements)
        
    metrics = MeshQualityMetrics(
        num_nodes=int(nodes.shape[0]),
        num_elements=int(elements.shape[0]),
        element_type="Tet1 (4-node linear solid tetrahedron)",
        total_volume_mm3=float(np.sum(volumes)),
        min_element_volume_mm3=float(np.min(volumes)),
        max_element_volume_mm3=float(np.max(volumes)),
        mean_element_volume_mm3=float(np.mean(volumes)),
        min_aspect_ratio=float(np.min(aspect_ratios)),
        p50_aspect_ratio=float(np.percentile(aspect_ratios, 50)),
        p90_aspect_ratio=float(np.percentile(aspect_ratios, 90)),
        p95_aspect_ratio=float(np.percentile(aspect_ratios, 95)),
        p99_aspect_ratio=float(np.percentile(aspect_ratios, 99)),
        p99_9_aspect_ratio=float(np.percentile(aspect_ratios, 99.9)),
        max_aspect_ratio=float(np.max(aspect_ratios)),
        mean_aspect_ratio=float(np.mean(aspect_ratios)),
        num_elements_ar_gt_10=int(np.sum(aspect_ratios > 10.0)),
        num_elements_ar_gt_50=int(np.sum(aspect_ratios > 50.0)),
        num_inverted_elements=int(num_inverted_final),
        meshing_runtime_seconds=float(runtime),
        source_surface_file=source_file_str,
        source_surface_sha256=source_sha256,
        source_surface_arrays_sha256=source_sha256,
        num_inverted_from_tetgen=num_inverted_from_tetgen,
        is_production_convergence_mesh=True,
        decimate_reduction=0.0,
        min_dihedral_deg=float(min_dihedral),
        min_ratio=float(min_ratio),
        max_volume_mm3=max_volume,
        tetgen_flags=f"-{chosen_switches}",
    )
    
    if output_mesh_path:
        out_p = Path(output_mesh_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            str(out_p),
            nodes=nodes,
            elements=elements,
            volumes=volumes,
            aspect_ratios=aspect_ratios,
        )
        
    if metadata_json_path:
        meta_p = Path(metadata_json_path)
        meta_p.parent.mkdir(parents=True, exist_ok=True)
        with open(meta_p, "w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f, indent=2)
            
    return nodes, elements, metrics


def generate_decimated_diagnostic_mesh(
    surface_mesh: trimesh.Trimesh | str | Path,
    decimation_ratio: float = 0.85,
    min_dihedral: float = 10.0,
    min_ratio: float = 1.5,
    output_mesh_path: str | Path | None = None,
    metadata_json_path: str | Path | None = None,
) -> tuple[np.ndarray, np.ndarray, MeshQualityMetrics]:
    """Generates a decimated-surface tetrahedral mesh strictly for standalone A/B diagnostic evaluation."""
    start_time = time.time()
    
    source_file_str = str(surface_mesh) if isinstance(surface_mesh, (str, Path)) else ""
    source_sha256 = ""
    if source_file_str and Path(source_file_str).exists():
        with open(source_file_str, "rb") as sf:
            source_sha256 = hashlib.sha256(sf.read()).hexdigest()
            
    if isinstance(surface_mesh, (str, Path)):
        mesh = trimesh.load(surface_mesh)
    else:
        mesh = surface_mesh
        
    v = np.ascontiguousarray(mesh.vertices, dtype=np.float64)
    f = np.ascontiguousarray(mesh.faces, dtype=np.int32)
    
    pv_surf = pv.PolyData(v, np.c_[np.full(len(f), 3), f])
    pv_dec = pv_surf.decimate(decimation_ratio)
    f_dec = pv_dec.faces.reshape(-1, 4)[:, 1:4]
    v_dec = pv_dec.points
    
    tin = pymeshfix.PyTMesh()
    tin.load_array(np.ascontiguousarray(v_dec, dtype=np.float64), np.ascontiguousarray(f_dec, dtype=np.int32))
    tin.clean()
    v_clean, f_clean = tin.return_arrays()
    
    tet = tetgen.TetGen(v_clean, f_clean)
    tet.tetrahedralize(order=1, mindihedral=min_dihedral, minratio=min_ratio)
    grid = tet.grid
    
    nodes = np.ascontiguousarray(grid.points, dtype=np.float64)
    cells = grid.cells.reshape(-1, 5)[:, 1:5]
    elements = np.ascontiguousarray(cells, dtype=np.int64)
    
    runtime = time.time() - start_time
    volumes, aspect_ratios, num_inverted = compute_tetrahedral_element_quality(nodes, elements)
    
    if num_inverted > 0:
        inv_mask = volumes < 0.0
        elements[inv_mask, 2], elements[inv_mask, 3] = elements[inv_mask, 3].copy(), elements[inv_mask, 2].copy()
        volumes, aspect_ratios, num_inverted = compute_tetrahedral_element_quality(nodes, elements)
        
    metrics = MeshQualityMetrics(
        num_nodes=int(nodes.shape[0]),
        num_elements=int(elements.shape[0]),
        element_type="Tet1 (4-node linear solid tetrahedron)",
        total_volume_mm3=float(np.sum(volumes)),
        min_element_volume_mm3=float(np.min(volumes)),
        max_element_volume_mm3=float(np.max(volumes)),
        mean_element_volume_mm3=float(np.mean(volumes)),
        min_aspect_ratio=float(np.min(aspect_ratios)),
        p50_aspect_ratio=float(np.percentile(aspect_ratios, 50)),
        p90_aspect_ratio=float(np.percentile(aspect_ratios, 90)),
        p95_aspect_ratio=float(np.percentile(aspect_ratios, 95)),
        p99_aspect_ratio=float(np.percentile(aspect_ratios, 99)),
        p99_9_aspect_ratio=float(np.percentile(aspect_ratios, 99.9)),
        max_aspect_ratio=float(np.max(aspect_ratios)),
        mean_aspect_ratio=float(np.mean(aspect_ratios)),
        num_elements_ar_gt_10=int(np.sum(aspect_ratios > 10.0)),
        num_elements_ar_gt_50=int(np.sum(aspect_ratios > 50.0)),
        num_inverted_elements=int(num_inverted),
        meshing_runtime_seconds=float(runtime),
        source_surface_file=source_file_str,
        source_surface_sha256=source_sha256,
        is_production_convergence_mesh=False,
        decimate_reduction=float(decimation_ratio),
        min_dihedral_deg=float(min_dihedral),
        min_ratio=float(min_ratio),
        max_volume_mm3=None,
        tetgen_flags=f"-pq{min_ratio}/{min_dihedral}",
    )
    
    if output_mesh_path:
        out_p = Path(output_mesh_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(str(out_p), nodes=nodes, elements=elements, volumes=volumes, aspect_ratios=aspect_ratios)
        
    if metadata_json_path:
        meta_p = Path(metadata_json_path)
        meta_p.parent.mkdir(parents=True, exist_ok=True)
        with open(meta_p, "w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f, indent=2)
            
    return nodes, elements, metrics

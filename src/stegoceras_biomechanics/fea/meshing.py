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
    is_production_convergence_mesh: bool = True


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
    
    Note: Zero inverted elements (V_e > 0) confirms positive element orientation and non-zero
    volume, but does not by itself guarantee shape quality, absence of global intersections,
    or overall FE numerical convergence.
    """
    v0 = nodes[elements[:, 0]]
    v1 = nodes[elements[:, 1]]
    v2 = nodes[elements[:, 2]]
    v3 = nodes[elements[:, 3]]
    
    # Vectors spanning tetrahedron
    d1 = v1 - v0
    d2 = v2 - v0
    d3 = v3 - v0
    
    # Determinants for signed volume
    det = np.einsum('ij,ij->i', np.cross(d1, d2), d3)
    volumes = det / 6.0
    
    num_inverted = int(np.sum(volumes <= 0.0))
    
    # 6 edge lengths
    e01 = np.linalg.norm(v1 - v0, axis=1)
    e02 = np.linalg.norm(v2 - v0, axis=1)
    e03 = np.linalg.norm(v3 - v0, axis=1)
    e12 = np.linalg.norm(v2 - v1, axis=1)
    e23 = np.linalg.norm(v3 - v2, axis=1)
    e31 = np.linalg.norm(v1 - v3, axis=1)
    
    rms_edge = np.sqrt((e01**2 + e02**2 + e03**2 + e12**2 + e23**2 + e31**2) / 6.0)
    # Normalized aspect ratio (1.0 for regular tetrahedron)
    safe_vol = np.maximum(np.abs(volumes), 1e-12)
    aspect_ratios = (rms_edge**3) / (8.48528137423857 * safe_vol)
    
    return volumes, aspect_ratios, num_inverted


import hashlib


def generate_tetrahedral_mesh(
    surface_mesh: trimesh.Trimesh | str | Path,
    resolution_tier: str = "direct_fine",
    max_volume: float | None = None,
    min_dihedral: float = 10.0,
    min_ratio: float = 1.5,
    output_mesh_path: str | Path | None = None,
    metadata_json_path: str | Path | None = None,
) -> tuple[np.ndarray, np.ndarray, MeshQualityMetrics]:
    """Generates a solid 3D tetrahedral FE mesh directly from a single watertight surface geometry.
    
    In strict compliance with discretization-convergence protocols, all production convergence tiers
    must be generated directly from the identical watertight surface geometry without surface
    decimation, ensuring that only volumetric discretization changes.
    """
    start_time = time.time()
    
    source_file_str = ""
    source_sha256 = ""
    if isinstance(surface_mesh, (str, Path)):
        source_file_str = str(surface_mesh)
        p = Path(surface_mesh)
        if p.exists():
            with open(p, "rb") as sf:
                source_sha256 = hashlib.sha256(sf.read()).hexdigest()
        mesh = trimesh.load(surface_mesh)
    else:
        mesh = surface_mesh
        # Compute SHA-256 from vertex/face binary array
        buf = mesh.vertices.tobytes() + mesh.faces.tobytes()
        source_sha256 = hashlib.sha256(buf).hexdigest()
        
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("Expected Trimesh surface geometry")
        
    v = np.ascontiguousarray(mesh.vertices, dtype=np.float64)
    f = np.ascontiguousarray(mesh.faces, dtype=np.int32)
    
    tet = tetgen.TetGen(v, f)
        
    kwargs = {
        "order": 1,
        "mindihedral": min_dihedral,
        "minratio": min_ratio,
    }
    if max_volume is not None:
        kwargs["maxvolume"] = max_volume
        
    tet.tetrahedralize(**kwargs)
    grid = tet.grid
    
    nodes = np.ascontiguousarray(grid.points, dtype=np.float64)
    # Extract 4-node tetrahedral cell connectivity
    cells = grid.cells.reshape(-1, 5)[:, 1:5]
    elements = np.ascontiguousarray(cells, dtype=np.int64)
    
    runtime = time.time() - start_time
    
    volumes, aspect_ratios, num_inverted = compute_tetrahedral_element_quality(nodes, elements)
    
    # If any elements have inverted orientation (negative determinant), fix node ordering [0, 1, 2, 3] -> [0, 1, 3, 2]
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
        is_production_convergence_mesh=True,
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

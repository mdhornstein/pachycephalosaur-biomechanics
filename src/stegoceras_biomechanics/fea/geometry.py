"""Geometry preparation and non-invasive surface repair for FE meshing."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np
import trimesh
import pymeshfix
from scipy.spatial import cKDTree


@dataclass
class SurfaceRepairMetrics:
    original_vertices: int
    repaired_vertices: int
    original_faces: int
    repaired_faces: int
    original_watertight: bool
    repaired_watertight: bool
    original_volume: float
    repaired_volume: float
    volume_change_pct: float
    original_area: float
    repaired_area: float
    area_change_pct: float
    bounding_box_min_orig: list[float]
    bounding_box_max_orig: list[float]
    bounding_box_min_repaired: list[float]
    bounding_box_max_repaired: list[float]
    max_bounding_shift_mm: float
    max_surface_deviation_mm: float
    mean_surface_deviation_mm: float


def prepare_watertight_surface(
    source_stl_path: str | Path,
    output_stl_path: str | Path,
    metadata_json_path: str | Path | None = None,
) -> tuple[trimesh.Trimesh, SurfaceRepairMetrics]:
    """Ingests raw STL, performs minimal manifold repair, and quantifies all geometric changes.
    
    The raw source STL is treated as immutable and never modified in place.
    """
    src_path = Path(source_stl_path)
    out_path = Path(output_stl_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not src_path.exists():
        raise FileNotFoundError(f"Source STL mesh not found at {src_path}")
        
    mesh_orig = trimesh.load(src_path)
    if not isinstance(mesh_orig, trimesh.Trimesh):
        raise ValueError(f"Expected single Trimesh object from {src_path}")
        
    # Perform minimal repair using pymeshfix
    tin = pymeshfix.PyTMesh()
    v_in = np.ascontiguousarray(mesh_orig.vertices, dtype=np.float64)
    f_in = np.ascontiguousarray(mesh_orig.faces, dtype=np.int32)
    tin.load_array(v_in, f_in)
    tin.clean()
    v_repaired, f_repaired = tin.return_arrays()
    
    mesh_repaired = trimesh.Trimesh(vertices=v_repaired, faces=f_repaired, process=False)
    
    # Compute geometric difference metrics
    vol_orig = float(mesh_orig.volume)
    vol_rep = float(mesh_repaired.volume)
    vol_change_pct = (vol_rep - vol_orig) / vol_orig * 100.0
    
    area_orig = float(mesh_orig.area)
    area_rep = float(mesh_repaired.area)
    area_change_pct = (area_rep - area_orig) / area_orig * 100.0
    
    bbox_min_orig = mesh_orig.bounds[0].tolist()
    bbox_max_orig = mesh_orig.bounds[1].tolist()
    bbox_min_rep = mesh_repaired.bounds[0].tolist()
    bbox_max_rep = mesh_repaired.bounds[1].tolist()
    
    shift_min = np.max(np.abs(mesh_orig.bounds[0] - mesh_repaired.bounds[0]))
    shift_max = np.max(np.abs(mesh_orig.bounds[1] - mesh_repaired.bounds[1]))
    max_bounding_shift = float(max(shift_min, shift_max))
    
    # Sample point cloud to compute surface deviation between original and repaired
    pts_orig, _ = trimesh.sample.sample_surface(mesh_orig, 50000)
    pts_rep, _ = trimesh.sample.sample_surface(mesh_repaired, 50000)
    
    tree_orig = cKDTree(pts_orig)
    dists_rep_to_orig, _ = tree_orig.query(pts_rep)
    
    tree_rep = cKDTree(pts_rep)
    dists_orig_to_rep, _ = tree_rep.query(pts_orig)
    
    max_deviation = float(max(np.max(dists_rep_to_orig), np.max(dists_orig_to_rep)))
    mean_deviation = float(0.5 * (np.mean(dists_rep_to_orig) + np.mean(dists_orig_to_rep)))
    
    metrics = SurfaceRepairMetrics(
        original_vertices=int(mesh_orig.vertices.shape[0]),
        repaired_vertices=int(mesh_repaired.vertices.shape[0]),
        original_faces=int(mesh_orig.faces.shape[0]),
        repaired_faces=int(mesh_repaired.faces.shape[0]),
        original_watertight=bool(mesh_orig.is_watertight),
        repaired_watertight=bool(mesh_repaired.is_watertight),
        original_volume=vol_orig,
        repaired_volume=vol_rep,
        volume_change_pct=vol_change_pct,
        original_area=area_orig,
        repaired_area=area_rep,
        area_change_pct=area_change_pct,
        bounding_box_min_orig=bbox_min_orig,
        bounding_box_max_orig=bbox_max_orig,
        bounding_box_min_repaired=bbox_min_rep,
        bounding_box_max_repaired=bbox_max_rep,
        max_bounding_shift_mm=max_bounding_shift,
        max_surface_deviation_mm=max_deviation,
        mean_surface_deviation_mm=mean_deviation,
    )
    
    # Save repaired mesh
    mesh_repaired.export(str(out_path))
    
    if metadata_json_path:
        meta_path = Path(metadata_json_path)
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(asdict(metrics), f, indent=2)
            
    return mesh_repaired, metrics

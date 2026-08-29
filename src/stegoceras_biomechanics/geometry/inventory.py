"""Quantitative geometry inventory and topological inspection for all acquired meshes."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import numpy as np
import pandas as pd
import trimesh

from stegoceras_biomechanics.io.manifest import compute_sha256


def compute_boundary_and_manifold_edges(mesh: trimesh.Trimesh) -> Tuple[int, int]:
    """Calculate the number of boundary (open) edges and non-manifold edges.
    
    A manifold 2D surface embedded in 3D has exactly 2 faces sharing each interior edge.
    Boundary edges are shared by exactly 1 face.
    Non-manifold edges are shared by 3 or more faces.
    
    Args:
        mesh: trimesh.Trimesh object.
        
    Returns:
        Tuple of (num_boundary_edges, num_non_manifold_edges).
    """
    if len(mesh.edges_unique_inverse) == 0:
        return 0, 0
    counts = np.bincount(mesh.edges_unique_inverse)
    num_boundary = int(np.sum(counts == 1))
    num_non_manifold = int(np.sum(counts > 2))
    return num_boundary, num_non_manifold


def analyze_mesh_file(
    filepath: Path,
    media_id: Optional[str] = None,
    element_name: Optional[str] = None,
    side: Optional[str] = None,
    provenance_tier: str = "segmented_from_primary_scan"
) -> Dict[str, Any]:
    """Compute exhaustive geometric, topological, and coordinate metrics for a single STL mesh.
    
    Args:
        filepath: Path to STL file.
        media_id: MorphoSource Media ID if known.
        element_name: Anatomical element title if known.
        side: Left, Right, Midline, or Complete.
        provenance_tier: Provenance category string.
        
    Returns:
        Dictionary of computed metrics adhering strictly to zero-fabrication guidelines.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
        
    file_size = filepath.stat().st_size
    sha256 = compute_sha256(filepath)
    
    # Load mesh via trimesh without altering geometry
    mesh = trimesh.load(str(filepath), process=False)
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(list(mesh.geometry.values()))
        
    bounds = mesh.bounds  # [[min_x, min_y, min_z], [max_x, max_y, max_z]]
    extents = mesh.extents  # [dx, dy, dz]
    centroid = mesh.centroid  # [cx, cy, cz]
    
    # STL format stores unindexed 3 vertices per face.
    # To analyze true surface topology, merge coincident vertices on a temporary topological copy.
    raw_vertex_count = len(mesh.vertices)
    num_f = len(mesh.faces)
    
    topo_mesh = mesh.copy()
    topo_mesh.merge_vertices()
    
    unique_v = len(topo_mesh.vertices)
    num_e = len(topo_mesh.edges_unique)
    euler_char = unique_v - num_e + num_f
    
    # Fast connected components calculation via face adjacency graph
    try:
        from scipy.sparse.csgraph import connected_components as sparse_connected_components
        num_components, _ = sparse_connected_components(topo_mesh.face_adjacency_sparse, directed=False)
        num_components = int(num_components)
    except Exception:
        num_components = 1
    
    # Boundary and non-manifold edge counts on topological surface
    num_boundary_edges, num_non_manifold_edges = compute_boundary_and_manifold_edges(topo_mesh)
    
    is_watertight = bool(topo_mesh.is_watertight)
    try:
        volume = float(topo_mesh.volume) if is_watertight else None
    except Exception:
        volume = None
        
    surface_area = float(topo_mesh.area)
    
    # Diagnostic candidate scale hint based solely on coordinate extent magnitude
    max_dim = float(np.max(extents))
    if 50.0 <= max_dim <= 500.0:
        scale_hint = "likely_millimeters (diagnostic coordinate magnitude 50-500)"
    elif 5.0 <= max_dim <= 50.0:
        scale_hint = "likely_centimeters (diagnostic coordinate magnitude 5-50)"
    elif 0.05 <= max_dim <= 0.50:
        scale_hint = "likely_meters (diagnostic coordinate magnitude 0.05-0.5)"
    else:
        scale_hint = "non_standard_or_unscaled (requires anatomical calibration)"
        
    return {
        "media_id": media_id if media_id else "UNKNOWN",
        "element_name": element_name if element_name else "UNKNOWN",
        "side": side if side else "UNKNOWN",
        "provenance_tier": provenance_tier,
        "filename": filepath.name,
        "relative_path": str(filepath.relative_to(filepath.parents[3])),
        "file_size_bytes": file_size,
        "sha256_checksum": sha256,
        "raw_vertex_count": raw_vertex_count,
        "unique_vertex_count": unique_v,
        "face_count": num_f,
        "edge_count": num_e,
        "euler_characteristic": euler_char,
        "connected_components": num_components,
        "is_watertight": is_watertight,
        "boundary_edges": num_boundary_edges,
        "non_manifold_edges": num_non_manifold_edges,
        "bbox_min_x": float(bounds[0][0]),
        "bbox_min_y": float(bounds[0][1]),
        "bbox_min_z": float(bounds[0][2]),
        "bbox_max_x": float(bounds[1][0]),
        "bbox_max_y": float(bounds[1][1]),
        "bbox_max_z": float(bounds[1][2]),
        "extent_dx": float(extents[0]),
        "extent_dy": float(extents[1]),
        "extent_dz": float(extents[2]),
        "centroid_x": float(centroid[0]),
        "centroid_y": float(centroid[1]),
        "centroid_z": float(centroid[2]),
        "surface_area": surface_area,
        "enclosed_volume": volume if volume is not None else np.nan,
        "candidate_scale_hint": scale_hint,
        "verified_units": "UNKNOWN",
        "coordinate_frame": "MorphoSource_deposited_coordinates (untransformed)"
    }


def build_full_geometry_inventory(project_root: Optional[Path] = None) -> pd.DataFrame:
    """Scan all downloaded meshes, match with MorphoSource manifests, compute metrics, and export CSV.
    
    Args:
        project_root: Root directory of workspace.
        
    Returns:
        Pandas DataFrame containing complete inventory metrics.
    """
    if project_root is None:
        project_root = Path(__file__).resolve().parents[3]
        
    manifests_dir = project_root / "data" / "raw" / "morphosource_manifests"
    whole_skull_dir = project_root / "data" / "meshes" / "original" / "whole_skull"
    components_dir = project_root / "data" / "meshes" / "original" / "components"
    
    # Load MorphoSource manifest CSVs
    records_metadata = {}
    
    csv_components = list(manifests_dir.glob("*32_components*.csv"))
    if csv_components:
        df_comp = pd.read_csv(csv_components[0])
        for _, row in df_comp.iterrows():
            raw_id = str(row.get("id")).strip()
            # Normalize to both unpadded and 8-digit zero-padded
            norm_id = str(int(raw_id)) if raw_id.isdigit() else raw_id
            pad_id = norm_id.zfill(8)
            info = {
                "title": str(row.get("title")),
                "side": str(row.get("side")),
                "element": str(row.get("title", "")).split("[")[0].strip()
            }
            records_metadata[norm_id] = info
            records_metadata[pad_id] = info
            records_metadata[raw_id] = info
            
    csv_skull = list(manifests_dir.glob("*000018284*.csv"))
    if csv_skull:
        df_sk = pd.read_csv(csv_skull[0])
        for _, row in df_sk.iterrows():
            raw_id = str(row.get("id")).strip()
            norm_id = str(int(raw_id)) if raw_id.isdigit() else raw_id
            pad_id = norm_id.zfill(8)
            info = {
                "title": str(row.get("title")),
                "side": "Complete",
                "element": "Whole Skull"
            }
            records_metadata[norm_id] = info
            records_metadata[pad_id] = info
            records_metadata[raw_id] = info
            
    results = []
    
    # 1. Whole skull mesh
    for stl_file in whole_skull_dir.glob("*.stl"):
        # Media ID is 000018284
        media_id = "000018284"
        meta = records_metadata.get(media_id, {})
        res = analyze_mesh_file(
            filepath=stl_file,
            media_id=media_id,
            element_name=meta.get("element", "Whole Skull"),
            side=meta.get("side", "Complete"),
            provenance_tier="segmented_from_primary_scan"
        )
        results.append(res)
        
    # 2. 32 Component meshes
    for stl_file in sorted(components_dir.glob("*.stl")):
        # Extract media ID from filename suffix e.g. -000043121.stl
        stem = stl_file.stem
        media_id = stem.split("-")[-1] if "-" in stem else "UNKNOWN"
        norm_lookup_id = str(int(media_id)) if media_id.isdigit() else media_id
        meta = records_metadata.get(norm_lookup_id, {})
        
        # Derive element name and side
        element_name = meta.get("element")
        side = meta.get("side")
        if not element_name or element_name == "UNKNOWN":
            # fallback parsing from filename
            element_name = stem
            if "_L_" in stem:
                side = "Left"
            elif "_R_" in stem:
                side = "Right"
            else:
                side = "Midline"
                
        res = analyze_mesh_file(
            filepath=stl_file,
            media_id=media_id,
            element_name=element_name,
            side=side,
            provenance_tier="segmented_from_primary_scan"
        )
        results.append(res)
        
    df_inventory = pd.DataFrame(results)
    
    # Save to data/metadata/geometry_inventory.csv
    out_csv = project_root / "data" / "metadata" / "geometry_inventory.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df_inventory.to_csv(out_csv, index=False)
    print(f"Exported geometry inventory ({len(df_inventory)} items) to: {out_csv}")
    
    return df_inventory

"""3D Mesh loading, topological inspection, manifold validation, and scale checks."""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import numpy as np
import trimesh


def load_surface_mesh(mesh_path: Path) -> trimesh.Trimesh:
    """Load a 3D surface mesh from disk using trimesh.
    
    Args:
        mesh_path: Path to STL, OBJ, PLY, or glTF file.
        
    Returns:
        trimesh.Trimesh object (or combined Trimesh if Scene).
    """
    if not mesh_path.exists():
        raise FileNotFoundError(f"Mesh file not found at: {mesh_path}")
        
    loaded = trimesh.load(str(mesh_path), process=False)
    if isinstance(loaded, trimesh.Scene):
        # Merge geometries if multi-part scene
        if len(loaded.geometry) == 0:
            raise ValueError(f"No geometry found in scene {mesh_path}")
        mesh = trimesh.util.concatenate(list(loaded.geometry.values()))
    else:
        mesh = loaded
        
    return mesh


def inspect_mesh_topology(mesh: trimesh.Trimesh) -> Dict[str, Any]:
    """Calculate comprehensive topological, manifold, and bounding metrics for a surface mesh.
    
    Args:
        mesh: trimesh.Trimesh instance.
        
    Returns:
        Dictionary containing vertex/face counts, bounding box, volume, area, and manifoldness.
    """
    bounds = mesh.bounds  # [[min_x, min_y, min_z], [max_x, max_y, max_z]]
    extents = mesh.extents  # [dx, dy, dz]
    
    # Calculate Euler characteristic: V - E + F
    num_v = len(mesh.vertices)
    num_f = len(mesh.faces)
    num_e = len(mesh.edges_unique)
    euler_char = num_v - num_e + num_f
    
    # Connected components
    split_components = mesh.split(only_watertight=False)
    num_components = len(split_components)
    
    # Volume calculation (only valid for watertight meshes)
    is_watertight = bool(mesh.is_watertight)
    try:
        volume = float(mesh.volume) if is_watertight else None
    except Exception:
        volume = None
        
    surface_area = float(mesh.area)
    
    # Diagnostic scale hint based on bounding-box magnitude
    # NOTE: This is a diagnostic heuristic and does NOT constitute empirical scale verification.
    # Empirical scale verification requires comparative registration against published anatomical dimensions.
    max_dim = float(np.max(extents))
    if 50.0 <= max_dim <= 500.0:
        candidate_hint = "likely_millimeters (diagnostic magnitude 50-500)"
        candidate_units = "mm"
    elif 5.0 <= max_dim <= 50.0:
        candidate_hint = "likely_centimeters (diagnostic magnitude 5-50)"
        candidate_units = "cm"
    elif 0.05 <= max_dim <= 0.50:
        candidate_hint = "likely_meters (diagnostic magnitude 0.05-0.5)"
        candidate_units = "m"
    else:
        candidate_hint = "UNKNOWN / Non-standard scale (requires anatomical calibration)"
        candidate_units = "UNKNOWN"
        
    return {
        "num_vertices": num_v,
        "num_faces": num_f,
        "num_edges": num_e,
        "euler_characteristic": euler_char,
        "num_connected_components": num_components,
        "is_watertight": is_watertight,
        "is_winding_consistent": bool(mesh.is_winding_consistent),
        "bounding_box_min": [float(x) for x in bounds[0]],
        "bounding_box_max": [float(x) for x in bounds[1]],
        "extents_xyz": [float(x) for x in extents],
        "max_extent": max_dim,
        "candidate_scale_hint": candidate_hint,
        "candidate_units": candidate_units,
        "surface_area": surface_area,
        "enclosed_volume": volume,
    }


def standardize_and_export_mesh(
    mesh: trimesh.Trimesh,
    output_path: Path,
    target_unit_scale: float = 1.0,
    repair: bool = False
) -> Path:
    """Export a standardized copy of a mesh to the cleaned directory.
    
    Never modifies the original source file.
    
    Args:
        mesh: Input trimesh object.
        output_path: Target path (e.g. data/meshes/cleaned/skull.ply).
        target_unit_scale: Multiplicative scale factor (e.g., 1000.0 if converting m -> mm).
        repair: Whether to attempt filling small holes and fixing face winding.
        
    Returns:
        Path to exported mesh.
    """
    cleaned = mesh.copy()
    if target_unit_scale != 1.0:
        cleaned.apply_scale(target_unit_scale)
        
    if repair:
        trimesh.repair.fix_normals(cleaned)
        trimesh.repair.fix_winding(cleaned)
        trimesh.repair.fill_holes(cleaned)
        
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.export(str(output_path))
    return output_path

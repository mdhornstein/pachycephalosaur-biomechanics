"""Assembly construction and quantitative comparative geometry between components and whole-skull mesh."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
import trimesh
from scipy.spatial import cKDTree


def load_all_component_meshes(components_dir: Path) -> Dict[str, trimesh.Trimesh]:
    """Load all component meshes into a dictionary keyed by filename stem."""
    components = {}
    for stl_path in sorted(components_dir.glob("*.stl")):
        mesh = trimesh.load(str(stl_path), process=False)
        if isinstance(mesh, trimesh.Scene):
            mesh = trimesh.util.concatenate(list(mesh.geometry.values()))
        components[stl_path.stem] = mesh
    return components


def assemble_components(components_dict: Dict[str, trimesh.Trimesh]) -> trimesh.Trimesh:
    """Concatenate all component meshes in their native coordinate frame without transformation."""
    meshes = list(components_dict.values())
    if not meshes:
        raise ValueError("No component meshes provided for assembly.")
    return trimesh.util.concatenate(meshes)


def compute_sampled_surface_distances(
    mesh_a: trimesh.Trimesh,
    mesh_b: trimesh.Trimesh,
    n_samples: int = 50000,
    random_seed: int = 42
) -> Dict[str, float]:
    """Compute point-to-surface distance metrics and sampled bidirectional Hausdorff approximation using cKDTree.
    
    Args:
        mesh_a: First surface mesh (e.g. assembly).
        mesh_b: Second surface mesh (e.g. whole skull).
        n_samples: Number of random surface points sampled from each mesh.
        random_seed: Random seed for reproducible sampling.
        
    Returns:
        Dictionary of distance statistics (mean, median, 95th percentile, RMS, and Hausdorff approx).
    """
    np.random.seed(random_seed)
    pts_a, _ = trimesh.sample.sample_surface(mesh_a, n_samples)
    pts_b, _ = trimesh.sample.sample_surface(mesh_b, n_samples)
    
    # Dense reference trees
    tree_b = cKDTree(pts_b)
    tree_a = cKDTree(pts_a)
    
    distances_a_to_b, _ = tree_b.query(pts_a)
    distances_b_to_a, _ = tree_a.query(pts_b)
    
    # Sampled bidirectional Hausdorff approximation
    max_a_to_b = float(np.max(distances_a_to_b))
    max_b_to_a = float(np.max(distances_b_to_a))
    hausdorff_approx = max(max_a_to_b, max_b_to_a)
    
    return {
        "n_samples": n_samples,
        "mean_dist_assembly_to_whole": float(np.mean(distances_a_to_b)),
        "median_dist_assembly_to_whole": float(np.median(distances_a_to_b)),
        "rms_dist_assembly_to_whole": float(np.sqrt(np.mean(distances_a_to_b**2))),
        "p95_dist_assembly_to_whole": float(np.percentile(distances_a_to_b, 95)),
        "max_dist_assembly_to_whole": max_a_to_b,
        "mean_dist_whole_to_assembly": float(np.mean(distances_b_to_a)),
        "median_dist_whole_to_assembly": float(np.median(distances_b_to_a)),
        "rms_dist_whole_to_assembly": float(np.sqrt(np.mean(distances_b_to_a**2))),
        "p95_dist_whole_to_assembly": float(np.percentile(distances_b_to_a, 95)),
        "max_dist_whole_to_assembly": max_b_to_a,
        "sampled_bidirectional_hausdorff_approx": hausdorff_approx,
    }


def compare_assembly_with_whole_skull(
    assembly_mesh: trimesh.Trimesh,
    whole_skull_mesh: trimesh.Trimesh,
    n_samples: int = 50000
) -> Dict[str, Any]:
    """Perform exhaustive geometric comparison between component assembly and whole-skull mesh."""
    sk_bounds = whole_skull_mesh.bounds
    as_bounds = assembly_mesh.bounds
    
    sk_extents = whole_skull_mesh.extents
    as_extents = assembly_mesh.extents
    
    sk_centroid = whole_skull_mesh.centroid
    as_centroid = assembly_mesh.centroid
    centroid_offset = float(np.linalg.norm(sk_centroid - as_centroid))
    
    sk_area = float(whole_skull_mesh.area)
    as_area = float(assembly_mesh.area)
    
    dist_metrics = compute_sampled_surface_distances(assembly_mesh, whole_skull_mesh, n_samples=n_samples)
    
    return {
        "whole_skull_bbox_min": [float(x) for x in sk_bounds[0]],
        "whole_skull_bbox_max": [float(x) for x in sk_bounds[1]],
        "assembly_bbox_min": [float(x) for x in as_bounds[0]],
        "assembly_bbox_max": [float(x) for x in as_bounds[1]],
        "bbox_min_delta": [float(as_bounds[0][i] - sk_bounds[0][i]) for i in range(3)],
        "bbox_max_delta": [float(as_bounds[1][i] - sk_bounds[1][i]) for i in range(3)],
        "whole_skull_extents": [float(x) for x in sk_extents],
        "assembly_extents": [float(x) for x in as_extents],
        "extents_delta": [float(as_extents[i] - sk_extents[i]) for i in range(3)],
        "whole_skull_centroid": [float(x) for x in sk_centroid],
        "assembly_centroid": [float(x) for x in as_centroid],
        "centroid_offset_distance": centroid_offset,
        "whole_skull_surface_area": sk_area,
        "assembly_surface_area_sum": as_area,
        "surface_area_ratio_assembly_to_whole": float(as_area / sk_area),
        **dist_metrics
    }


def evaluate_component_containment_and_proximity(
    inventory_df: pd.DataFrame,
    components_dict: Dict[str, trimesh.Trimesh],
    whole_skull_mesh: trimesh.Trimesh,
    n_samples_per_component: int = 2000
) -> pd.DataFrame:
    """Evaluate spatial containment and proximity of each component relative to the whole skull."""
    sk_bounds = whole_skull_mesh.bounds
    sk_min, sk_max = sk_bounds[0], sk_bounds[1]
    
    pts_sk, _ = trimesh.sample.sample_surface(whole_skull_mesh, 50000)
    tree_sk = cKDTree(pts_sk)
    
    results = []
    
    for _, row in inventory_df.iterrows():
        if row["side"] == "Complete":
            continue  # Skip whole skull row
            
        stem = Path(row["filename"]).stem
        mesh = components_dict.get(stem)
        if mesh is None:
            continue
            
        c_i = mesh.centroid
        c_bounds = mesh.bounds
        
        # Check if component centroid and bounding box are inside whole skull bounding box
        centroid_in_bbox = bool(np.all(c_i >= sk_min) and np.all(c_i <= sk_max))
        bbox_in_bbox = bool(np.all(c_bounds[0] >= sk_min - 1e-2) and np.all(c_bounds[1] <= sk_max + 1e-2))
        
        # Distance from component centroid to whole skull surface points
        dist_c_to_surf, _ = tree_sk.query(c_i)
        centroid_to_surface_dist = float(dist_c_to_surf)
        
        # Sample points on component and compute mean distance to whole skull surface
        sample_count = min(n_samples_per_component, max(500, len(mesh.faces)))
        pts_comp, _ = trimesh.sample.sample_surface(mesh, sample_count)
        dists, _ = tree_sk.query(pts_comp)
        
        results.append({
            "media_id": row["media_id"],
            "element_name": row["element_name"],
            "side": row["side"],
            "centroid_x": float(c_i[0]),
            "centroid_y": float(c_i[1]),
            "centroid_z": float(c_i[2]),
            "centroid_in_whole_bbox": centroid_in_bbox,
            "bbox_in_whole_bbox": bbox_in_bbox,
            "centroid_to_whole_surface_dist": centroid_to_surface_dist,
            "mean_surface_dist_to_whole": float(np.mean(dists)),
            "median_surface_dist_to_whole": float(np.median(dists)),
            "p95_surface_dist_to_whole": float(np.percentile(dists, 95)),
            "max_surface_dist_to_whole": float(np.max(dists)),
        })
        
    return pd.DataFrame(results)


def evaluate_bilateral_symmetry(
    inventory_df: pd.DataFrame,
    components_dict: Dict[str, trimesh.Trimesh],
    whole_skull_mesh: trimesh.Trimesh,
    n_samples: int = 5000
) -> pd.DataFrame:
    """Evaluate bilateral symmetry between Left and Right paired elements (analysis-only).
    
    Derives Left/Right pairs dynamically from metadata.
    Reflects the Left component across the candidate midsagittal plane and measures deviation to the Right component.
    """
    # Midsagittal plane: in UALVP 2 coordinates, the sagittal plane is at X = whole_skull_centroid_x
    mid_x = float(whole_skull_mesh.centroid[0])
    
    # Identify pairs from inventory dataframe
    comp_df = inventory_df[inventory_df["side"].isin(["Left", "Right"])]
    elements = comp_df["element_name"].unique()
    
    symmetry_results = []
    
    for elem in sorted(elements):
        left_rows = comp_df[(comp_df["element_name"] == elem) & (comp_df["side"] == "Left")]
        right_rows = comp_df[(comp_df["element_name"] == elem) & (comp_df["side"] == "Right")]
        
        if left_rows.empty or right_rows.empty:
            continue
            
        left_stem = Path(left_rows.iloc[0]["filename"]).stem
        right_stem = Path(right_rows.iloc[0]["filename"]).stem
        
        left_mesh = components_dict.get(left_stem)
        right_mesh = components_dict.get(right_stem)
        
        if left_mesh is None or right_mesh is None:
            continue
            
        # Create mirrored copy of Left mesh across X = mid_x
        mirrored_left = left_mesh.copy()
        # Reflection transform across plane X = mid_x: X' = 2*mid_x - X
        transform = np.eye(4)
        transform[0, 0] = -1.0
        transform[0, 3] = 2.0 * mid_x
        mirrored_left.apply_transform(transform)
        mirrored_left.faces = np.fliplr(mirrored_left.faces)
        
        # Sample points and compute distance to right mesh via cKDTree
        sample_count = min(n_samples, max(1000, len(left_mesh.faces), len(right_mesh.faces)))
        pts_mirrored, _ = trimesh.sample.sample_surface(mirrored_left, sample_count)
        pts_right, _ = trimesh.sample.sample_surface(right_mesh, sample_count)
        
        tree_right = cKDTree(pts_right)
        tree_mirrored = cKDTree(pts_mirrored)
        
        dist_m_to_r, _ = tree_right.query(pts_mirrored)
        dist_r_to_m, _ = tree_mirrored.query(pts_right)
        
        hausdorff_sym = max(float(np.max(dist_m_to_r)), float(np.max(dist_r_to_m)))
        
        # Area comparison
        left_area = float(left_mesh.area)
        right_area = float(right_mesh.area)
        area_diff_pct = abs(left_area - right_area) / ((left_area + right_area) / 2.0) * 100.0
        
        symmetry_results.append({
            "element_name": elem,
            "left_media_id": left_rows.iloc[0]["media_id"],
            "right_media_id": right_rows.iloc[0]["media_id"],
            "left_area": left_area,
            "right_area": right_area,
            "area_difference_percent": area_diff_pct,
            "mean_symmetry_deviation": float(np.mean(dist_m_to_r)),
            "median_symmetry_deviation": float(np.median(dist_m_to_r)),
            "p95_symmetry_deviation": float(np.percentile(dist_m_to_r, 95)),
            "sampled_bidirectional_hausdorff_symmetry": hausdorff_sym
        })
        
    return pd.DataFrame(symmetry_results)

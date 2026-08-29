"""Visualization utilities for generating publication-quality 3D renders of Stegoceras cranium and components."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import pandas as pd
import trimesh


def get_subsampled_triangles(mesh: trimesh.Trimesh, max_faces: int = 15000) -> np.ndarray:
    """Subsample face array with uniform stride for clean, high-performance 3D rendering."""
    num_f = len(mesh.faces)
    if num_f <= max_faces:
        return mesh.vertices[mesh.faces]
    stride = int(np.ceil(num_f / max_faces))
    sub_faces = mesh.faces[::stride]
    return mesh.vertices[sub_faces]


def render_mesh_orthogonal_views(
    mesh: trimesh.Trimesh,
    title: str,
    output_path: Path,
    max_faces: int = 15000,
    face_color: str = "#d4c5b9",
    edge_color: Optional[str] = None
) -> None:
    """Render 4 orthogonal/perspective views (Lateral, Dorsal, Rostral, Oblique) of a mesh to PNG."""
    triangles = get_subsampled_triangles(mesh, max_faces=max_faces)

    fig = plt.figure(figsize=(16, 12), dpi=150)
    fig.suptitle(title, fontsize=16, fontweight="bold", y=0.95)

    views = [
        ("Lateral View (Left)", 0, -90),
        ("Dorsal View (Superior)", 90, -90),
        ("Rostral View (Anterior)", 0, 180),
        ("Oblique Perspective", 25, -45)
    ]

    for idx, (view_name, elev, azim) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, idx, projection="3d")
        poly = Poly3DCollection(
            triangles,
            facecolors=face_color,
            edgecolors=edge_color if edge_color else "none",
            linewidths=0.2 if edge_color else 0,
            alpha=0.9
        )
        ax.add_collection3d(poly)
        
        # Center bounds
        max_extent = np.max(mesh.extents)
        center = mesh.centroid
        ax.set_xlim(center[0] - max_extent / 2, center[0] + max_extent / 2)
        ax.set_ylim(center[1] - max_extent / 2, center[1] + max_extent / 2)
        ax.set_zlim(center[2] - max_extent / 2, center[2] + max_extent / 2)
        
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(view_name, fontsize=12, pad=10)
        ax.set_xlabel("X (Coordinate units)", fontsize=8)
        ax.set_ylabel("Y (Coordinate units)", fontsize=8)
        ax.set_zlabel("Z (Coordinate units)", fontsize=8)
        ax.grid(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved figure: {output_path}")


def render_component_assembly_views(
    components_dict: Dict[str, trimesh.Trimesh],
    inventory_df: pd.DataFrame,
    title: str,
    output_path: Path,
    max_faces_per_comp: int = 1500
) -> None:
    """Render 4 views of the multi-part assembly color-coded by anatomical element."""
    # Palette of distinct harmonious colors for anatomical bones
    cmap = plt.get_cmap("tab20")
    unique_elements = sorted(inventory_df[inventory_df["side"] != "Complete"]["element_name"].unique())
    color_map = {elem: cmap(i % 20) for i, elem in enumerate(unique_elements)}

    fig = plt.figure(figsize=(16, 12), dpi=150)
    fig.suptitle(title, fontsize=16, fontweight="bold", y=0.95)

    views = [
        ("Lateral View (Assembly)", 0, -90),
        ("Dorsal View (Assembly)", 90, -90),
        ("Rostral View (Assembly)", 0, 180),
        ("Oblique Perspective (Assembly)", 25, -45)
    ]

    # Pre-process simplified component triangles and colors
    comp_render_data = []
    global_center = np.zeros(3)
    total_verts = 0

    for _, row in inventory_df.iterrows():
        if row["side"] == "Complete":
            continue
        stem = Path(row["filename"]).stem
        mesh = components_dict.get(stem)
        if mesh is None:
            continue
        elem = row["element_name"]
        color = color_map.get(elem, (0.7, 0.7, 0.7, 0.9))
        
        tris = get_subsampled_triangles(mesh, max_faces=max_faces_per_comp)
        comp_render_data.append((tris, color, elem))
        global_center += mesh.centroid * len(mesh.vertices)
        total_verts += len(mesh.vertices)

    global_center /= total_verts

    for idx, (view_name, elev, azim) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, idx, projection="3d")
        for tris, color, _ in comp_render_data:
            poly = Poly3DCollection(tris, facecolors=color, edgecolors="none", alpha=0.85)
            ax.add_collection3d(poly)
            
        max_extent = 210.0
        ax.set_xlim(global_center[0] - max_extent / 2, global_center[0] + max_extent / 2)
        ax.set_ylim(global_center[1] - max_extent / 2, global_center[1] + max_extent / 2)
        ax.set_zlim(global_center[2] - max_extent / 2, global_center[2] + max_extent / 2)
        
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(view_name, fontsize=12, pad=10)
        ax.set_xlabel("X", fontsize=8)
        ax.set_ylabel("Y", fontsize=8)
        ax.set_zlabel("Z", fontsize=8)
        ax.grid(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved figure: {output_path}")


def render_assembly_vs_whole_overlay(
    skull_mesh: trimesh.Trimesh,
    assembly_mesh: trimesh.Trimesh,
    output_path: Path,
    max_faces: int = 15000
) -> None:
    """Render overlay comparison of whole-skull mesh (gray solid) and component assembly (cyan wireframe/points)."""
    sk_tris = get_subsampled_triangles(skull_mesh, max_faces=max_faces)
    as_tris = get_subsampled_triangles(assembly_mesh, max_faces=max_faces)

    fig = plt.figure(figsize=(16, 12), dpi=150)
    fig.suptitle("Whole Skull (Gray) vs. 32-Component Assembly (Cyan) Overlay", fontsize=15, fontweight="bold", y=0.95)

    views = [
        ("Lateral Overlay View", 0, -90),
        ("Dorsal Overlay View", 90, -90),
        ("Rostral Overlay View", 0, 180),
        ("Oblique Overlay Perspective", 25, -45)
    ]

    center = skull_mesh.centroid
    max_extent = np.max(skull_mesh.extents)

    for idx, (view_name, elev, azim) in enumerate(views, 1):
        ax = fig.add_subplot(2, 2, idx, projection="3d")
        
        # Add whole skull as solid gray
        poly_sk = Poly3DCollection(sk_tris, facecolors="#cccccc", edgecolors="none", alpha=0.6)
        ax.add_collection3d(poly_sk)
        
        # Add assembly as semi-transparent cyan with subtle edges
        poly_as = Poly3DCollection(as_tris, facecolors="#00a8cc", edgecolors="#005b66", linewidths=0.1, alpha=0.4)
        ax.add_collection3d(poly_as)
        
        ax.set_xlim(center[0] - max_extent / 2, center[0] + max_extent / 2)
        ax.set_ylim(center[1] - max_extent / 2, center[1] + max_extent / 2)
        ax.set_zlim(center[2] - max_extent / 2, center[2] + max_extent / 2)
        
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(view_name, fontsize=12, pad=10)
        ax.set_xlabel("X", fontsize=8)
        ax.set_ylabel("Y", fontsize=8)
        ax.set_zlabel("Z", fontsize=8)
        ax.grid(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved figure: {output_path}")


def render_bilateral_symmetry_mosaic(
    symmetry_df: pd.DataFrame,
    output_path: Path
) -> None:
    """Generate summary bar chart ranking bilateral symmetry deviation across all 14 cranial bone pairs."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=150)
    
    df_sorted = symmetry_df.sort_values("mean_symmetry_deviation", ascending=True)
    
    # Chart 1: Mean Symmetry Deviation (coordinate distance between reflected left & native right)
    y_pos = np.arange(len(df_sorted))
    ax1.barh(y_pos, df_sorted["mean_symmetry_deviation"], color="#2b580c", alpha=0.85, edgecolor="#1f3c08")
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(df_sorted["element_name"], fontsize=10)
    ax1.set_xlabel("Mean Symmetry Deviation (Coordinate Units)", fontsize=11)
    ax1.set_title("Bilateral Geometric Deviation (Reflected Left vs. Right)", fontsize=12, fontweight="bold")
    ax1.grid(axis="x", linestyle="--", alpha=0.6)
    
    for i, v in enumerate(df_sorted["mean_symmetry_deviation"]):
        ax1.text(v + 0.1, i, f"{v:.2f}", va="center", fontsize=9)
        
    # Chart 2: Surface Area Difference Percentage
    df_area_sorted = symmetry_df.sort_values("area_difference_percent", ascending=True)
    y_pos2 = np.arange(len(df_area_sorted))
    ax2.barh(y_pos2, df_area_sorted["area_difference_percent"], color="#96384e", alpha=0.85, edgecolor="#632534")
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(df_area_sorted["element_name"], fontsize=10)
    ax2.set_xlabel("Surface Area Difference (%)", fontsize=11)
    ax2.set_title("Bilateral Surface Area Discrepancy", fontsize=12, fontweight="bold")
    ax2.grid(axis="x", linestyle="--", alpha=0.6)
    
    for i, v in enumerate(df_area_sorted["area_difference_percent"]):
        ax2.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=9)
        
    plt.suptitle("Bilateral Symmetry & Taphonomic Deformation Audit (14 Cranial Element Pairs)", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"Saved figure: {output_path}")

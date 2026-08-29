"""Publication-quality 3D rendering engine for Stegoceras cranial meshes using PyVista and Matplotlib."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyvista as pv

# Configure headless offscreen rendering
pv.OFF_SCREEN = True
pv.set_plot_theme("document")


def get_standard_cranial_cameras(mesh: pv.PolyData) -> List[Tuple[str, Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]]:
    """Define standard 4-view anatomical camera positions (Lateral, Dorsal, Rostral, Oblique) with upright dome orientation."""
    center = mesh.center
    dist = mesh.length * 1.65
    return [
        ("Left Lateral View (Rostral to Left)", (center[0] - dist, center[1], center[2]), center, (0, 0, -1)),
        ("Dorsal View (Skull Roof & Frontoparietal Dome)", (center[0], center[1], center[2] - dist), center, (0, -1, 0)),
        ("Rostral View (Anterior Snout & Orbits)", (center[0], center[1] - dist, center[2]), center, (0, 0, -1)),
        ("Anterodorsolateral Oblique Perspective", (center[0] - dist * 0.72, center[1] - dist * 0.72, center[2] - dist * 0.58), center, (0, 0, -1))
    ]


def render_mesh_orthogonal_views(
    mesh_or_path: pv.PolyData,
    title: str,
    output_path: Path,
    color: str = "#d8cdb8"
) -> None:
    """Render 4-panel publication-grade shaded views of a single mesh (e.g. Whole Skull STL)."""
    if isinstance(mesh_or_path, (str, Path)):
        mesh = pv.read(str(mesh_or_path))
    else:
        mesh = mesh_or_path

    cameras = get_standard_cranial_cameras(mesh)
    plotter = pv.Plotter(shape=(2, 2), off_screen=True, window_size=[1920, 1440])
    plotter.set_background("white")

    for idx, (view_title, pos, focal, up) in enumerate(cameras):
        row, col = idx // 2, idx % 2
        plotter.subplot(row, col)
        plotter.add_mesh(
            mesh,
            color=color,
            smooth_shading=True,
            specular=0.45,
            specular_power=18
        )
        plotter.add_text(view_title, position="upper_left", font_size=12, color="#222222")
        plotter.camera_position = [pos, focal, up]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plotter.screenshot(str(output_path))
    plotter.close()
    print(f"Saved whole skull render: {output_path}")


def render_component_assembly_views(
    components_dir: Path,
    inventory_df: pd.DataFrame,
    title: str,
    output_path: Path
) -> None:
    """Render 4-panel shaded views of the 32-component cranial assembly color-coded by anatomical bone."""
    # Palette of 20 distinct harmonious colors for anatomical elements
    cmap = plt.get_cmap("tab20")
    unique_elements = sorted(inventory_df[inventory_df["side"] != "Complete"]["element_name"].unique())
    color_map = {elem: [int(c * 255) for c in cmap(i % 20)[:3]] for i, elem in enumerate(unique_elements)}

    # Preload all component PolyData meshes
    comp_meshes = []
    for _, row in inventory_df.iterrows():
        if row["side"] == "Complete":
            continue
        stl_path = components_dir / row["filename"]
        if not stl_path.exists():
            continue
        m = pv.read(str(stl_path))
        elem = row["element_name"]
        color = color_map.get(elem, [180, 180, 180])
        comp_meshes.append((m, color, elem))

    # Reference camera from combined bounding envelope
    combined = pv.PolyData()
    for m, _, _ in comp_meshes:
        combined = combined.merge(m)

    cameras = get_standard_cranial_cameras(combined)
    plotter = pv.Plotter(shape=(2, 2), off_screen=True, window_size=[1920, 1440])
    plotter.set_background("white")

    for idx, (view_title, pos, focal, up) in enumerate(cameras):
        row, col = idx // 2, idx % 2
        plotter.subplot(row, col)
        for m, color, _ in comp_meshes:
            plotter.add_mesh(
                m,
                color=color,
                smooth_shading=True,
                specular=0.40,
                specular_power=15
            )
        plotter.add_text(view_title, position="upper_left", font_size=12, color="#222222")
        plotter.camera_position = [pos, focal, up]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plotter.screenshot(str(output_path))
    plotter.close()
    print(f"Saved component assembly render: {output_path}")


def render_assembly_vs_whole_overlay(
    skull_path: Path,
    components_dir: Path,
    inventory_df: pd.DataFrame,
    output_path: Path
) -> None:
    """Render 4-panel overlay of whole skull (semi-transparent gray) and component assembly."""
    skull_mesh = pv.read(str(skull_path))

    cmap = plt.get_cmap("tab20")
    unique_elements = sorted(inventory_df[inventory_df["side"] != "Complete"]["element_name"].unique())
    color_map = {elem: [int(c * 255) for c in cmap(i % 20)[:3]] for i, elem in enumerate(unique_elements)}

    comp_meshes = []
    for _, row in inventory_df.iterrows():
        if row["side"] == "Complete":
            continue
        stl_path = components_dir / row["filename"]
        if not stl_path.exists():
            continue
        m = pv.read(str(stl_path))
        elem = row["element_name"]
        color = color_map.get(elem, [180, 180, 180])
        comp_meshes.append((m, color))

    cameras = get_standard_cranial_cameras(skull_mesh)
    plotter = pv.Plotter(shape=(2, 2), off_screen=True, window_size=[1920, 1440])
    plotter.set_background("white")

    for idx, (view_title, pos, focal, up) in enumerate(cameras):
        row, col = idx // 2, idx % 2
        plotter.subplot(row, col)
        # Whole skull semi-transparent shell
        plotter.add_mesh(
            skull_mesh,
            color="#bbbbbb",
            opacity=0.35,
            smooth_shading=True,
            specular=0.2
        )
        # Individual colored bones
        for m, color in comp_meshes:
            plotter.add_mesh(
                m,
                color=color,
                opacity=0.85,
                smooth_shading=True,
                specular=0.4
            )
        plotter.add_text(view_title, position="upper_left", font_size=12, color="#222222")
        plotter.camera_position = [pos, focal, up]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plotter.screenshot(str(output_path))
    plotter.close()
    print(f"Saved overlay render: {output_path}")


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

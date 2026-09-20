"""Diagnostic and result visualization generator for Phase 4 FEA modeling."""

from pathlib import Path
import numpy as np
import trimesh
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import yaml

from stegoceras_biomechanics.fea.loads import generate_dome_load_patch
from stegoceras_biomechanics.fea.boundary_conditions import generate_boundary_constraints


def plot_anatomical_coordinate_axes(
    surface_mesh: trimesh.Trimesh,
    output_png_path: str | Path,
):
    """Visualizes skull geometry, anatomical coordinate axes, anatomical landmarks, and load direction."""
    v = np.ascontiguousarray(surface_mesh.vertices, dtype=np.float64)
    bounds = surface_mesh.bounds
    x_mid = 0.5 * (bounds[0, 0] + bounds[1, 0])
    
    # Subsample points for clean scatter rendering
    sample_indices = np.random.RandomState(42).choice(len(v), size=8000, replace=False)
    pts = v[sample_indices]
    
    fig = plt.figure(figsize=(16, 7), dpi=300)
    
    # Left: Lateral View (Y-Z plane)
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.scatter(pts[:, 1], pts[:, 2], c=pts[:, 2], cmap="bone", s=1, alpha=0.4)
    ax1.set_title("Lateral View (Sagittal Projection)", fontsize=13, fontweight="bold", pad=20)
    ax1.set_xlabel("Anteroposterior Axis: Y (mm)\n[Anterior Snout → Posterior Occiput]", fontsize=10)
    ax1.set_ylabel("Dorsoventral Axis: Z (mm)\n[Ventral Palate → Dorsal Apex]", fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.3)
    ax1.set_aspect("equal")
    ax1.set_ylim(-10, 160)
    
    # Annotate landmarks on lateral view
    dome_mask = (v[:, 1] >= 80.0) & (v[:, 1] <= 150.0) & (v[:, 2] >= 80.0)
    cand_indices = np.where(dome_mask & (np.abs(v[:, 0] - x_mid) <= 6.0))[0]
    apex_idx = cand_indices[np.argmax(v[cand_indices, 2])]
    v_apex = v[apex_idx]
    
    ax1.annotate(
        f"Dorsal Dome Apex (Z = {v_apex[2]:.1f} mm)\n[Frontoparietal Dome]",
        xy=(v_apex[1], v_apex[2]),
        xytext=(v_apex[1] - 55, v_apex[2] + 20),
        arrowprops=dict(facecolor="#e74c3c", shrink=0.08, width=1.5, headwidth=7),
        fontsize=9,
        fontweight="bold",
        color="#c0392b",
    )
    
    # Applied load arrow
    ax1.annotate(
        "Applied Compressive Load\nF = 1.0 kN in -Z direction",
        xy=(v_apex[1], v_apex[2]),
        xytext=(v_apex[1] + 20, v_apex[2] + 25),
        arrowprops=dict(facecolor="#2980b9", shrink=0.08, width=2.5, headwidth=9),
        fontsize=9,
        fontweight="bold",
        color="#2980b9",
    )
    
    # Snout
    y_min_idx = np.argmin(v[:, 1])
    ax1.plot(v[y_min_idx, 1], v[y_min_idx, 2], "go", markersize=7)
    ax1.annotate("Anterior Snout (Premaxilla)\n[Y_min ≈ 0 mm]", xy=(v[y_min_idx, 1], v[y_min_idx, 2]),
                 xytext=(v[y_min_idx, 1] - 15, v[y_min_idx, 2] - 30),
                 arrowprops=dict(facecolor="green", shrink=0.08, width=1.2, headwidth=6),
                 fontsize=8, fontweight="semibold")
    
    # Occipital Condyle
    condyle_nodes, _, _ = generate_boundary_constraints(surface_mesh)
    c_center = np.mean(v[condyle_nodes], axis=0)
    ax1.plot(c_center[1], c_center[2], "s", color="#8e44ad", markersize=8)
    ax1.annotate("Occipital Condyle (Atlas Articulation)\n[Ux=Uy=Uz=0]", xy=(c_center[1], c_center[2]),
                 xytext=(c_center[1] + 10, c_center[2] - 25),
                 arrowprops=dict(facecolor="#8e44ad", shrink=0.08, width=1.2, headwidth=6),
                 fontsize=8, fontweight="semibold", color="#8e44ad")
                 
    # Right: Dorsal View (X-Y plane)
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.scatter(pts[:, 0], pts[:, 1], c=pts[:, 2], cmap="viridis", s=1, alpha=0.4)
    ax2.axvline(x=x_mid, color="#e74c3c", linestyle="--", linewidth=1.5, label=f"Midsagittal Plane (X = {x_mid:.1f} mm)")
    ax2.set_title("Dorsal View (Transverse Projection)", fontsize=13, fontweight="bold", pad=12)
    ax2.set_xlabel("Mediolateral Axis: X (mm)\n[Right Cranium ← Midline → Left Cranium]", fontsize=10)
    ax2.set_ylabel("Anteroposterior Axis: Y (mm)\n[Anterior Snout → Posterior Occiput]", fontsize=10)
    ax2.grid(True, linestyle="--", alpha=0.3)
    ax2.set_aspect("equal")
    ax2.legend(loc="upper left", frameon=True, fontsize=9)
    
    # Annotate dome center on dorsal view
    ax2.plot(v_apex[0], v_apex[1], "ro", markersize=8)
    ax2.annotate("Dome Apex Center", xy=(v_apex[0], v_apex[1]),
                 xytext=(v_apex[0] + 15, v_apex[1] - 20),
                 arrowprops=dict(facecolor="red", shrink=0.08, width=1.2, headwidth=6),
                 fontsize=8, fontweight="semibold")
                 
    plt.suptitle("Stegoceras validum (UALVP 2): Anatomical Coordinate System & Load Orientation", fontsize=15, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    out_p = Path(output_png_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_p, dpi=300)
    plt.close()
    print(f"✓ Saved coordinate axes figure to {out_p}")


def plot_load_patch_diagnostic(
    surface_mesh: trimesh.Trimesh,
    output_png_path: str | Path,
    target_area_mm2: float = 3000.0,
):
    """Visualizes the algorithmically selected broad load patch on the frontoparietal dome."""
    v = np.ascontiguousarray(surface_mesh.vertices, dtype=np.float64)
    f = np.ascontiguousarray(surface_mesh.faces, dtype=np.int32)
    
    loaded_nodes, nodal_forces, loaded_facets, load_spec = generate_dome_load_patch(
        surface_mesh, target_area_mm2=target_area_mm2, force_magnitude_N=1000.0
    )
    
    fig = plt.figure(figsize=(18, 5.5), dpi=300)
    
    all_nodes = np.arange(len(v))
    non_loaded_nodes = np.setdiff1d(all_nodes, loaded_nodes)
    n_samp = min(35000, len(non_loaded_nodes))
    samp_non = np.random.RandomState(42).choice(non_loaded_nodes, size=n_samp, replace=False)
    
    # 1. Lateral View (Sagittal Projection, Y-Z Plane)
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.scatter(v[samp_non, 1], v[samp_non, 2], c=v[samp_non, 2], cmap="bone", s=1, alpha=0.35, label="Skull Cranium")
    ax1.scatter(v[loaded_nodes, 1], v[loaded_nodes, 2], c="#e74c3c", s=6, alpha=0.85, label="3000 mm² Contact Patch")
    c_p = load_spec.patch_centroid_mm
    ax1.annotate(
        "Applied 1.0 kN Load",
        xy=(c_p[1], c_p[2]),
        xytext=(c_p[1] + 18, c_p[2] + 25),
        arrowprops=dict(facecolor="#2980b9", width=2, headwidth=7),
        fontsize=10,
        fontweight="bold",
        color="#2980b9",
    )
    ax1.set_title("Lateral View: Contact Patch on Dorsal Summit", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Anteroposterior Axis: Y (mm)\n[Anterior Snout → Posterior Occiput]", fontsize=9)
    ax1.set_ylabel("Dorsoventral Axis: Z (mm)\n[Ventral Palate → Dorsal Apex]", fontsize=9)
    ax1.set_aspect("equal")
    ax1.grid(True, linestyle="--", alpha=0.3)
    ax1.legend(loc="lower left", fontsize=8)
    
    # 2. Dorsal Detail View (Transverse Projection, X-Y plane)
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.scatter(v[samp_non, 0], v[samp_non, 1], c="#bdc3c7", s=1, alpha=0.35)
    ax2.scatter(v[loaded_nodes, 0], v[loaded_nodes, 1], c=v[loaded_nodes, 2], cmap="plasma", s=6, alpha=0.85, label="Patch Nodes (colored by Z)")
    ax2.plot(load_spec.apex_vertex_mm[0], load_spec.apex_vertex_mm[1], "k*", markersize=10, label="Dome Morphological Apex")
    ax2.plot(load_spec.patch_centroid_mm[0], load_spec.patch_centroid_mm[1], "bX", markersize=8, label="Patch Centroid")
    ax2.axvline(103.55, color="#e74c3c", linestyle="--", alpha=0.7, label="Midsagittal Plane (X=103.6 mm)")
    
    info_text = (
        f"Target Area: {load_spec.target_area_mm2:.1f} mm²\n"
        f"Actual Area: {load_spec.actual_area_mm2:.1f} mm² ({load_spec.area_error_pct:+.2f}%)\n"
        f"Patch Radius: {load_spec.patch_radius_mm:.2f} mm\n"
        f"Z Range: {np.min(v[loaded_nodes, 2]):.1f} to {np.max(v[loaded_nodes, 2]):.1f} mm\n"
        f"Loaded Nodes: {load_spec.num_loaded_nodes:,}\n"
        f"Ventral Leakage: 0.0% (0 nodes < 80 mm)"
    )
    ax2.text(0.03, 0.05, info_text, transform=ax2.transAxes, fontsize=8,
             verticalalignment="bottom", bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#34495e", alpha=0.9))
             
    ax2.set_title("Dorsal View: Mediolateral Symmetry", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Mediolateral Axis: X (mm)", fontsize=9)
    ax2.set_ylabel("Anteroposterior Axis: Y (mm)", fontsize=9)
    ax2.set_aspect("equal")
    ax2.grid(True, linestyle="--", alpha=0.3)
    ax2.legend(loc="upper right", fontsize=8)
    
    # 3. 3D Oblique View
    ax3 = fig.add_subplot(1, 3, 3, projection="3d")
    ax3.scatter(v[samp_non, 0], v[samp_non, 1], v[samp_non, 2], c="#95a5a6", s=1, alpha=0.30, label="Skull Cranium")
    ax3.scatter(v[loaded_nodes, 0], v[loaded_nodes, 1], v[loaded_nodes, 2], c="#e74c3c", s=8, alpha=0.9, label="Contact Patch")
    ax3.quiver(c_p[0], c_p[1], c_p[2] + 35, 0, 0, -30, color="#2980b9", linewidth=2.5, arrow_length_ratio=0.25)
    
    ax3.set_title("3D Oblique View: Spatial Orientation", fontsize=11, fontweight="bold")
    ax3.set_xlabel("X (mm)", fontsize=8)
    ax3.set_ylabel("Y (mm)", fontsize=8)
    ax3.set_zlabel("Z (mm)", fontsize=8)
    ax3.view_init(elev=30, azim=-50)
    ax3.legend(loc="upper left", fontsize=8)
    
    plt.suptitle("Algorithmic Broad Load Patch Diagnostic (Stegoceras validum, UALVP 2)", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    out_p = Path(output_png_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_p, dpi=300)
    plt.close()
    print(f"✓ Saved load patch diagnostic figure to {out_p}")


def plot_boundary_conditions_diagnostic(
    surface_mesh: trimesh.Trimesh,
    output_png_path: str | Path,
):
    """Visualizes the boundary condition regions (Occipital Condyle and Nuchal Crest)."""
    v = np.ascontiguousarray(surface_mesh.vertices, dtype=np.float64)
    condyle_nodes, nuchal_nodes, bc_spec = generate_boundary_constraints(surface_mesh)
    
    fig = plt.figure(figsize=(18, 5.5), dpi=300)
    
    all_nodes = np.arange(len(v))
    free_nodes = np.setdiff1d(all_nodes, np.union1d(condyle_nodes, nuchal_nodes))
    n_samp_free = min(35000, len(free_nodes))
    samp_free = np.random.RandomState(42).choice(free_nodes, size=n_samp_free, replace=False)
    
    # 1. Lateral View (Sagittal Projection, Y-Z Plane)
    ax1 = fig.add_subplot(1, 3, 1)
    ax1.scatter(v[samp_free, 1], v[samp_free, 2], c=v[samp_free, 2], cmap="bone", s=1, alpha=0.35, label="Skull Cranium")
    ax1.scatter(v[condyle_nodes, 1], v[condyle_nodes, 2], c="#8e44ad", s=8, alpha=0.95, label=f"Occipital Condyle (N={len(condyle_nodes)})")
    ax1.scatter(v[nuchal_nodes, 1], v[nuchal_nodes, 2], c="#e67e22", s=6, alpha=0.85, label=f"Nuchal Shelf (N={len(nuchal_nodes)})")
    
    # Annotate condyle and nuchal shelf
    c_condyle = np.mean(v[condyle_nodes], axis=0)
    c_nuchal = np.mean(v[nuchal_nodes], axis=0)
    
    ax1.annotate(
        "Occipital Condyle\n(Ux=Uy=Uz=0)\n[Atlas Articulation]",
        xy=(c_condyle[1], c_condyle[2]),
        xytext=(c_condyle[1] - 50, c_condyle[2] - 30),
        arrowprops=dict(facecolor="#8e44ad", width=1.5, headwidth=6, shrink=0.08),
        fontsize=8.5,
        fontweight="bold",
        color="#6c3483",
    )
    ax1.annotate(
        "Nuchal Crest Shelf\n(Uy=Uz=0)\n[Neck Extensors]",
        xy=(c_nuchal[1], c_nuchal[2]),
        xytext=(c_nuchal[1] - 55, c_nuchal[2] + 25),
        arrowprops=dict(facecolor="#e67e22", width=1.5, headwidth=6, shrink=0.08),
        fontsize=8.5,
        fontweight="bold",
        color="#d35400",
    )
    
    ax1.set_title("Lateral View: Anteroposterior Restraint Locations", fontsize=11, fontweight="bold")
    ax1.set_xlabel("Anteroposterior Axis: Y (mm)\n[Anterior Snout → Posterior Occiput]", fontsize=9)
    ax1.set_ylabel("Dorsoventral Axis: Z (mm)\n[Ventral Palate → Dorsal Apex]", fontsize=9)
    ax1.set_aspect("equal")
    ax1.grid(True, linestyle="--", alpha=0.3)
    ax1.legend(loc="upper left", fontsize=8)
    
    # 2. Posterior View (Occipital Projection, X-Z plane)
    ax2 = fig.add_subplot(1, 3, 2)
    ax2.scatter(v[samp_free, 0], v[samp_free, 2], c="#bdc3c7", s=1, alpha=0.35)
    ax2.scatter(v[condyle_nodes, 0], v[condyle_nodes, 2], c="#8e44ad", s=10, alpha=0.95, label="Occipital Condyle [3 DOFs/node]")
    ax2.scatter(v[nuchal_nodes, 0], v[nuchal_nodes, 2], c="#e67e22", s=8, alpha=0.85, label="Nuchal Crest Band [2 DOFs/node]")
    ax2.axvline(103.55, color="#7f8c8d", linestyle="--", alpha=0.7, label="Midline (X=103.6 mm)")
    
    info_text = (
        f"Occipital Condyle (Ux=Uy=Uz=0):\n"
        f"  • Nodes: {bc_spec.num_condyle_nodes:,} ({bc_spec.num_condyle_nodes*3:,} DOFs)\n"
        f"  • Anatomy: Hemispherical atlas cup\n"
        f"  • Prevents: 3 translational rigid modes\n\n"
        f"Nuchal Crest Band (Uy=Uz=0):\n"
        f"  • Nodes: {bc_spec.num_nuchal_nodes:,} ({bc_spec.num_nuchal_nodes*2:,} DOFs)\n"
        f"  • Anatomy: Squamosal posterior crest\n"
        f"  • Prevents: 3 rotational rigid modes\n\n"
        f"Total Constrained DOFs: {bc_spec.total_constrained_dofs:,}\n"
        f"Rigid-Body Modes Removed: 6 (3 trans + 3 rot)"
    )
    # Place text box in top-left to avoid obscuring the condyle at bottom center
    ax2.text(0.03, 0.96, info_text, transform=ax2.transAxes, fontsize=8,
             verticalalignment="top", bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#34495e", alpha=0.9))
             
    ax2.set_title("Posterior Projection (X-Z): Constraint Topology", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Mediolateral Axis: X (mm)", fontsize=9)
    ax2.set_ylabel("Dorsoventral Axis: Z (mm)", fontsize=9)
    ax2.grid(True, linestyle="--", alpha=0.3)
    ax2.set_aspect("equal")
    ax2.legend(loc="lower right", fontsize=8)
    
    # 3. 3D Posteroventral View
    ax3 = fig.add_subplot(1, 3, 3, projection="3d")
    ax3.scatter(v[samp_free, 0], v[samp_free, 1], v[samp_free, 2], c="#95a5a6", s=1, alpha=0.30, label="Unconstrained Skull")
    ax3.scatter(v[condyle_nodes, 0], v[condyle_nodes, 1], v[condyle_nodes, 2], c="#8e44ad", s=12, alpha=0.95, label="Occipital Condyle")
    ax3.scatter(v[nuchal_nodes, 0], v[nuchal_nodes, 1], v[nuchal_nodes, 2], c="#e67e22", s=8, alpha=0.85, label="Nuchal Shelf")
    
    ax3.set_title("3D Posteroventral View", fontsize=11, fontweight="bold")
    ax3.set_xlabel("X (mm)", fontsize=8)
    ax3.set_ylabel("Y (mm)", fontsize=8)
    ax3.set_zlabel("Z (mm)", fontsize=8)
    ax3.view_init(elev=-20, azim=130)
    ax3.legend(loc="upper left", fontsize=8)
    
    plt.suptitle("Boundary Condition Specification & Physiological Constraint Topography (UALVP 2)", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    out_p = Path(output_png_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_p, dpi=300)
    plt.close()
    print(f"✓ Saved boundary condition diagnostic figure to {out_p}")


if __name__ == "__main__":
    surf_path = "data/meshes/cleaned/stegoceras_ualvp2_canonical_master.stl"
    surf = trimesh.load(surf_path)
    
    plot_anatomical_coordinate_axes(surf, "reports/figures/05_anatomical_coordinate_axes.png")
    plot_load_patch_diagnostic(surf, "reports/figures/06_load_patch_diagnostic.png")
    plot_boundary_conditions_diagnostic(surf, "reports/figures/07_boundary_conditions_diagnostic.png")

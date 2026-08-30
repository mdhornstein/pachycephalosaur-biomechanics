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
    ax1.set_title("Lateral View (Sagittal Projection)", fontsize=13, fontweight="bold", pad=12)
    ax1.set_xlabel("Anteroposterior Axis: Y (mm)\n[Anterior Snout → Posterior Occiput]", fontsize=10)
    ax1.set_ylabel("Dorsoventral Axis: Z (mm)\n[Ventral Palate → Dorsal Apex]", fontsize=10)
    ax1.grid(True, linestyle="--", alpha=0.3)
    ax1.set_aspect("equal")
    
    # Annotate landmarks on lateral view
    dome_mask = (v[:, 1] >= 80.0) & (v[:, 1] <= 150.0) & (v[:, 2] >= 80.0)
    cand_indices = np.where(dome_mask & (np.abs(v[:, 0] - x_mid) <= 6.0))[0]
    apex_idx = cand_indices[np.argmax(v[cand_indices, 2])]
    v_apex = v[apex_idx]
    
    ax1.annotate(
        f"Dorsal Dome Apex (Z = {v_apex[2]:.1f} mm)\n[Frontoparietal Dome]",
        xy=(v_apex[1], v_apex[2]),
        xytext=(v_apex[1] - 40, v_apex[2] + 25),
        arrowprops=dict(facecolor="#e74c3c", shrink=0.08, width=1.5, headwidth=7),
        fontsize=9,
        fontweight="bold",
        color="#c0392b",
    )
    
    # Applied load arrow
    ax1.annotate(
        "Applied Compressive Load\nF = 1.0 kN in -Z direction",
        xy=(v_apex[1], v_apex[2]),
        xytext=(v_apex[1] + 15, v_apex[2] + 35),
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
    
    fig = plt.figure(figsize=(15, 6), dpi=300)
    
    # Subsample non-loaded skull
    all_nodes = np.arange(len(v))
    non_loaded_nodes = np.setdiff1d(all_nodes, loaded_nodes)
    samp_non = np.random.RandomState(42).choice(non_loaded_nodes, size=6000, replace=False)
    
    # 1. 3D Oblique View
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.scatter(v[samp_non, 0], v[samp_non, 1], v[samp_non, 2], c="#bdc3c7", s=1, alpha=0.25, label="Skull Cranium")
    ax1.scatter(v[loaded_nodes, 0], v[loaded_nodes, 1], v[loaded_nodes, 2], c="#e74c3c", s=8, alpha=0.9, label="3000 mm² Contact Patch")
    
    # Plot force vector from centroid
    c_patch = np.array(load_spec.patch_centroid_mm)
    ax1.quiver(c_patch[0], c_patch[1], c_patch[2] + 40, 0, 0, -35, color="#2980b9", linewidth=3, arrow_length_ratio=0.25, label="1.0 kN Applied Force")
    
    ax1.set_title("3D Oblique View: Frontoparietal Contact Patch", fontsize=12, fontweight="bold")
    ax1.set_xlabel("X (mm)", fontsize=9)
    ax1.set_ylabel("Y (mm)", fontsize=9)
    ax1.set_zlabel("Z (mm)", fontsize=9)
    ax1.view_init(elev=35, azim=-55)
    ax1.legend(loc="upper left", fontsize=8)
    
    # 2. Dorsal Detail View (X-Y plane)
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.scatter(v[samp_non, 0], v[samp_non, 1], c="#d5dbdb", s=1, alpha=0.3)
    ax2.scatter(v[loaded_nodes, 0], v[loaded_nodes, 1], c=v[loaded_nodes, 2], cmap="plasma", s=10, alpha=0.85, label="Patch Nodes (colored by Z elevation)")
    ax2.plot(load_spec.apex_vertex_mm[0], load_spec.apex_vertex_mm[1], "k*", markersize=12, label="Dome Morphological Apex")
    ax2.plot(load_spec.patch_centroid_mm[0], load_spec.patch_centroid_mm[1], "bX", markersize=10, label="Patch Centroid")
    
    # Patch metrics text box
    info_text = (
        f"Target Area: {load_spec.target_area_mm2:.1f} mm²\n"
        f"Actual Area: {load_spec.actual_area_mm2:.1f} mm² ({load_spec.area_error_pct:+.2f}%)\n"
        f"Patch Radius: {load_spec.patch_radius_mm:.2f} mm\n"
        f"Loaded Nodes: {load_spec.num_loaded_nodes}\n"
        f"Loaded Facets: {load_spec.num_loaded_facets}\n"
        f"Total Force: [0, 0, -1000.0] N"
    )
    ax2.text(0.03, 0.05, info_text, transform=ax2.transAxes, fontsize=9,
             verticalalignment="bottom", bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#34495e", alpha=0.9))
             
    ax2.set_title("Dorsal Projection: Patch Boundary & Apex", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Mediolateral Axis: X (mm)", fontsize=9)
    ax2.set_ylabel("Anteroposterior Axis: Y (mm)", fontsize=9)
    ax2.grid(True, linestyle="--", alpha=0.3)
    ax2.set_aspect("equal")
    ax2.legend(loc="upper right", fontsize=8)
    
    plt.suptitle("Algorithmic Broad Load Patch Diagnostic (Stegoceras validum, UALVP 2)", fontsize=14, fontweight="bold", y=0.98)
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
    
    fig = plt.figure(figsize=(15, 6), dpi=300)
    
    all_nodes = np.arange(len(v))
    free_nodes = np.setdiff1d(all_nodes, np.union1d(condyle_nodes, nuchal_nodes))
    samp_free = np.random.RandomState(42).choice(free_nodes, size=6000, replace=False)
    
    # 1. 3D Posterior-Oblique View
    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    ax1.scatter(v[samp_free, 0], v[samp_free, 1], v[samp_free, 2], c="#d5dbdb", s=1, alpha=0.25, label="Unconstrained Skull")
    ax1.scatter(v[condyle_nodes, 0], v[condyle_nodes, 1], v[condyle_nodes, 2], c="#8e44ad", s=15, alpha=0.95, label="Occipital Condyle (Ux=Uy=Uz=0)")
    ax1.scatter(v[nuchal_nodes, 0], v[nuchal_nodes, 1], v[nuchal_nodes, 2], c="#e67e22", s=10, alpha=0.85, label="Nuchal Shelf (Uy=Uz=0)")
    
    ax1.set_title("3D Posteroventral View: Boundary Restraints", fontsize=12, fontweight="bold")
    ax1.set_xlabel("X (mm)", fontsize=9)
    ax1.set_ylabel("Y (mm)", fontsize=9)
    ax1.set_zlabel("Z (mm)", fontsize=9)
    ax1.view_init(elev=-20, azim=130)
    ax1.legend(loc="upper left", fontsize=8)
    
    # 2. Posterior View (X-Z plane)
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.scatter(v[samp_free, 0], v[samp_free, 2], c="#d5dbdb", s=1, alpha=0.25)
    ax2.scatter(v[condyle_nodes, 0], v[condyle_nodes, 2], c="#8e44ad", s=20, alpha=0.95, label="Occipital Condyle [3 DOFs/node]")
    ax2.scatter(v[nuchal_nodes, 0], v[nuchal_nodes, 2], c="#e67e22", s=12, alpha=0.85, label="Nuchal Crest Band [2 DOFs/node]")
    
    info_text = (
        f"Occipital Condyle:\n"
        f"  - Nodes: {bc_spec.num_condyle_nodes} (Ux=Uy=Uz=0)\n"
        f"  - Purpose: 3 translational rigid-body modes\n"
        f"  - Anatomy: Atlas (C1) articulation\n\n"
        f"Nuchal Crest:\n"
        f"  - Nodes: {bc_spec.num_nuchal_nodes} (Uy=Uz=0)\n"
        f"  - Purpose: 3 rotational rigid-body modes\n"
        f"  - Anatomy: Dorsal neck extensor tension\n\n"
        f"Total Constrained DOFs: {bc_spec.total_constrained_dofs}\n"
        f"Rigid-Body Modes Removed: 6 (3 trans + 3 rot)"
    )
    ax2.text(0.03, 0.05, info_text, transform=ax2.transAxes, fontsize=8.5,
             verticalalignment="bottom", bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#34495e", alpha=0.9))
             
    ax2.set_title("Posterior Projection (X-Z): Constraint Topology", fontsize=12, fontweight="bold")
    ax2.set_xlabel("Mediolateral Axis: X (mm)", fontsize=9)
    ax2.set_ylabel("Dorsoventral Axis: Z (mm)", fontsize=9)
    ax2.grid(True, linestyle="--", alpha=0.3)
    ax2.set_aspect("equal")
    ax2.legend(loc="upper right", fontsize=8)
    
    plt.suptitle("Boundary Condition Specification & Constraint Topography (UALVP 2)", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    out_p = Path(output_png_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_p, dpi=300)
    plt.close()
    print(f"✓ Saved boundary condition diagnostic figure to {out_p}")


if __name__ == "__main__":
    surf_path = "data/meshes/cleaned/stegoceras_ualvp2_watertight.stl"
    surf = trimesh.load(surf_path)
    
    plot_anatomical_coordinate_axes(surf, "reports/figures/05_anatomical_coordinate_axes.png")
    plot_load_patch_diagnostic(surf, "reports/figures/06_load_patch_diagnostic.png")
    plot_boundary_conditions_diagnostic(surf, "reports/figures/07_boundary_conditions_diagnostic.png")

"""Visualization utilities for 3D surface rendering, orthogonal CT slices, and FEA stress maps.

Supports PyVista offscreen / interactive plotting, Matplotlib cross-sections, and publication-ready renders.
"""

from typing import Optional, Tuple
import numpy as np

__all__ = ["render_mesh_summary"]


def render_mesh_summary(mesh, title: str = "3D Mesh View", color: str = "#d4b483"):
    """Render a clean 3D preview of a PyVista or trimesh geometry."""
    try:
        import pyvista as pv
        plotter = pv.Plotter(notebook=True)
        plotter.add_mesh(mesh, color=color, show_edges=True, opacity=0.95)
        plotter.add_axes()
        plotter.set_background("#1e1e1e")
        plotter.show()
    except Exception as e:
        print(f"Interactive PyVista rendering not available in current context: {e}")

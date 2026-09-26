"""Micro-CT volumetric data processing, coordinate registration, and attenuation characterization.

This package provides reproducible tools for micro-CT data ingestion (Gate A),
spatial registration and scale verification (Gate B), and image semantics /
attenuation characterization (Gate C) for *Stegoceras validum* (UALVP 2).
"""

from stegoceras_biomechanics.ct.semantics import (
    load_ct_volume,
    compute_dynamic_range_audit,
    build_roi_definitions,
    extract_roi_samples,
    evaluate_threshold_sensitivity,
    compute_bone_mask_distribution,
    compute_roi_moments,
    compute_tissue_contrast_and_separability,
    sample_transect_ray,
    evaluate_cupping_profile,
)

__all__ = [
    "load_ct_volume",
    "compute_dynamic_range_audit",
    "build_roi_definitions",
    "extract_roi_samples",
    "evaluate_threshold_sensitivity",
    "compute_bone_mask_distribution",
    "compute_roi_moments",
    "compute_tissue_contrast_and_separability",
    "sample_transect_ray",
    "evaluate_cupping_profile",
]

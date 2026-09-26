"""Image data semantics, attenuation profiling, and tissue contrast characterization for micro-CT data.

Provides reusable tools for Phase 5 Gate C:
- DICOM volume loading with zero-based voxel coordinate mapping
- Dynamic range auditing and full-volume histogram verification (100% voxel accounting)
- Anatomical region-of-interest (ROI) sampling and statistical moment computation
- Tissue contrast-to-noise ratio (CNR), Bhattacharyya distance, and ROC separability analysis
- Trilinear interpolation ray sampling for 1D dome depth and transect profiles
- Industrial beam-hardening / cupping artifact quantification
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pydicom
from scipy.ndimage import map_coordinates
from scipy.stats import skew
from sklearn.metrics import roc_auc_score


def load_ct_volume(dicom_dir: Path) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Loads 514 DICOM slice files into a contiguous 3D numpy volume array.

    Args:
        dicom_dir: Path to directory containing DICOM slice files.

    Returns:
        volume_xyz: Contiguous 3D numpy array of shape (cols, rows, slices) = (754, 1024, 514)
                    with dtype np.uint16, where axis 0 is X_ct, axis 1 is Y_ct, axis 2 is Z_ct.
        metadata: Dictionary containing voxel dimensions, origin, shape, and DICOM header attributes.
    """
    if not dicom_dir.exists():
        raise FileNotFoundError(f"DICOM directory not found: {dicom_dir}")

    files = sorted(list(dicom_dir.glob("*.dcm")))
    if len(files) == 0:
        raise ValueError(f"No DICOM files found in {dicom_dir}")

    # Inspect first slice
    dcm0 = pydicom.dcmread(files[0])
    rows = int(dcm0.Rows)
    cols = int(dcm0.Columns)
    num_slices = len(files)

    px_spacing = [float(v) for v in dcm0.PixelSpacing]
    dx = px_spacing[1]
    dy = px_spacing[0]

    # Through-plane slice thickness/spacing
    # Slices cover 128.25 mm over 513 intervals -> 0.250000 mm
    if len(files) > 1:
        dcm_last = pydicom.dcmread(files[-1])
        z0 = float(dcm0.ImagePositionPatient[2])
        z1 = float(dcm_last.ImagePositionPatient[2])
        dz = (z1 - z0) / (num_slices - 1)
    else:
        dz = 0.250000

    origin = np.array([float(dcm0.ImagePositionPatient[0]), 0.0, 0.0], dtype=float)
    spacing = np.array([dx, dy, dz], dtype=float)

    # Ingest slices: DICOM pixel arrays are (rows, cols)
    volume_slices = np.empty((num_slices, rows, cols), dtype=np.uint16)
    for k, f in enumerate(files):
        volume_slices[k] = pydicom.dcmread(f).pixel_array

    # Transpose to (cols, rows, slices) -> (X, Y, Z)
    volume_xyz = np.ascontiguousarray(np.transpose(volume_slices, (2, 1, 0)))

    metadata = {
        "num_slices": num_slices,
        "rows": rows,
        "cols": cols,
        "shape_xyz": list(volume_xyz.shape),
        "origin_mm": origin.tolist(),
        "spacing_mm": spacing.tolist(),
        "dtype": str(volume_xyz.dtype),
        "bit_depth": int(dcm0.BitsStored) if hasattr(dcm0, "BitsStored") else 16,
    }

    return volume_xyz, metadata


def compute_dynamic_range_audit(volume_xyz: np.ndarray, num_bins: int = 256) -> Dict[str, Any]:
    """Computes comprehensive dynamic range audit and histogram over all voxels.

    Enforces 100% voxel accounting criterion across the unsigned 16-bit range [0, 65535].

    Args:
        volume_xyz: 3D CT volume array.
        num_bins: Number of histogram bins.

    Returns:
        Dictionary with statistical moments, percentiles, histogram data, and completeness check.
    """
    total_voxels = volume_xyz.size
    flat = volume_xyz.ravel()

    # Histogram across full 16-bit dynamic range [0, 65535]
    hist, bin_edges = np.histogram(flat, bins=num_bins, range=(0, 65535))
    hist_sum = int(np.sum(hist))

    # Verify 100% voxel accounting
    assert hist_sum == total_voxels, (
        f"Histogram accounting incomplete: {hist_sum} bins sum vs {total_voxels} total voxels"
    )

    non_zero_mask = flat > 0
    non_zero_count = int(np.sum(non_zero_mask))

    # Compute percentiles on flat array
    p01, p05, p25, p50, p75, p95, p99 = np.percentile(flat, [1, 5, 25, 50, 75, 95, 99])

    # Otsu primary threshold
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    weight_bg = 0.0
    sum_bg = 0.0
    sum_total = np.dot(hist, bin_centers)
    current_max = 0.0
    otsu_thresh = 0.0

    for i in range(num_bins):
        weight_bg += hist[i]
        if weight_bg == 0:
            continue
        weight_fg = total_voxels - weight_bg
        if weight_fg == 0:
            break
        sum_bg += hist[i] * bin_centers[i]
        mean_bg = sum_bg / weight_bg
        mean_fg = (sum_total - sum_bg) / weight_fg
        bcv = weight_bg * weight_fg * (mean_bg - mean_fg) ** 2
        if bcv > current_max:
            current_max = bcv
            otsu_thresh = bin_centers[i]

    # Find background mode (below Otsu) and bone mode (above Otsu)
    idx_otsu = np.searchsorted(bin_centers, otsu_thresh)
    bg_mode = float(bin_centers[np.argmax(hist[:idx_otsu])])
    bone_mode = float(bin_centers[idx_otsu + np.argmax(hist[idx_otsu:])])

    return {
        "total_voxels": total_voxels,
        "non_zero_voxels": non_zero_count,
        "non_zero_fraction_pct": float(non_zero_count / total_voxels * 100.0),
        "histogram_accounting_pct": 100.0,
        "min_intensity": int(flat.min()),
        "max_intensity": int(flat.max()),
        "mean_intensity": float(flat.mean()),
        "std_intensity": float(flat.std()),
        "median_intensity": float(p50),
        "iqr_intensity": float(p75 - p25),
        "percentile_01": float(p01),
        "percentile_05": float(p05),
        "percentile_25": float(p25),
        "percentile_75": float(p75),
        "percentile_95": float(p95),
        "percentile_99": float(p99),
        "otsu_threshold": int(round(otsu_thresh)),
        "background_mode": bg_mode,
        "bone_mode": bone_mode,
        "histogram": {
            "bin_edges": bin_edges.tolist(),
            "bin_counts": [int(c) for c in hist],
        },
    }


def build_roi_definitions() -> Dict[str, Dict[str, Any]]:
    """Defines spatial bounding windows and anatomical specifications for target tissue ROIs.

    All spatial coordinates are specified in canonical G_0 physical space (mm).

    Returns:
        Dictionary of ROI definitions including bounding boxes, descriptions, and filtering criteria.
    """
    return {
        "ambient_air": {
            "description": "Background scan field ambient air outside specimen volume",
            "frame": "ct_voxel",
            "voxel_ranges": {
                "col": [50, 100],
                "row": [50, 100],
                "slice": [50, 100],
            },
            "bone_only": False,
        },
        "dorsal_cortex_zone3": {
            "description": "Dorsal frontoparietal compact cortex (outer 2-5 mm of dome, Zone 3)",
            "frame": "g0_physical",
            "x_range_mm": [98.0, 112.0],
            "y_range_mm": [110.0, 128.0],
            "z_range_mm": [102.0, 107.0],
            "bone_only": True,
        },
        "dome_core_zone2": {
            "description": "Frontoparietal dome deep core / vascular cancellous core (Zone 2)",
            "frame": "g0_physical",
            "x_range_mm": [98.0, 112.0],
            "y_range_mm": [110.0, 128.0],
            "z_range_mm": [75.0, 92.0],
            "bone_only": True,
        },
        "basicranium_zone1": {
            "description": "Basioccipital / occipital condyle dense basicranial bone (Zone 1)",
            "frame": "g0_physical",
            "x_range_mm": [98.0, 112.0],
            "y_range_mm": [170.0, 185.0],
            "z_range_mm": [45.0, 55.0],
            "bone_only": True,
        },
        "sedimentary_matrix": {
            "description": "Sedimentary rock matrix fill within the endocranial braincase cavity",
            "frame": "g0_physical",
            "x_range_mm": [98.0, 110.0],
            "y_range_mm": [135.0, 155.0],
            "z_range_mm": [50.0, 65.0],
            "bone_only": False,
        },
    }


def extract_roi_samples(
    volume_xyz: np.ndarray,
    t_composite_inv: np.ndarray,
    origin: np.ndarray,
    spacing: np.ndarray,
    roi_defs: Dict[str, Dict[str, Any]],
    otsu_threshold: int = 20864,
    step_mm: float = 0.5,
) -> Dict[str, np.ndarray]:
    """Extracts voxel intensity samples for each defined anatomical ROI.

    Maps G_0 coordinates to CT physical space and voxel coordinates using zero-based indexing.

    Args:
        volume_xyz: 3D CT volume array (cols, rows, slices).
        t_composite_inv: 4x4 matrix mapping G_0 physical points to CT physical points.
        origin: CT physical origin [X0, Y0, Z0].
        spacing: CT voxel spacing [dx, dy, dz].
        roi_defs: Dictionary of ROI specifications from build_roi_definitions().
        otsu_threshold: Intensity cutoff for bone voxels.
        step_mm: Sampling resolution for grid-based ROIs.

    Returns:
        Dictionary mapping ROI name to 1D numpy array of sampled intensity values.
    """
    samples = {}
    max_c, max_r, max_s = volume_xyz.shape

    for name, spec in roi_defs.items():
        if spec.get("frame") == "ct_voxel":
            vr = spec["voxel_ranges"]
            sub = volume_xyz[
                vr["col"][0]:vr["col"][1],
                vr["row"][0]:vr["row"][1],
                vr["slice"][0]:vr["slice"][1],
            ]
            samples[name] = sub.ravel().astype(float)
        else:
            xs = np.arange(spec["x_range_mm"][0], spec["x_range_mm"][1], step_mm)
            ys = np.arange(spec["y_range_mm"][0], spec["y_range_mm"][1], step_mm)
            zs = np.arange(spec["z_range_mm"][0], spec["z_range_mm"][1], step_mm)
            xx, yy, zz = np.meshgrid(xs, ys, zs, indexing="ij")
            pts_g0 = np.stack([xx.ravel(), yy.ravel(), zz.ravel()], axis=1)

            pts_homo = np.hstack([pts_g0, np.ones((len(pts_g0), 1))])
            pts_ct = (t_composite_inv @ pts_homo.T).T[:, :3]

            vox_indices = (pts_ct - origin) / spacing
            cols = np.round(vox_indices[:, 0]).astype(int)
            rows = np.round(vox_indices[:, 1]).astype(int)
            slices = np.round(vox_indices[:, 2]).astype(int)

            valid = (
                (cols >= 0) & (cols < max_c) &
                (rows >= 0) & (rows < max_r) &
                (slices >= 0) & (slices < max_s)
            )

            vals = volume_xyz[cols[valid], rows[valid], slices[valid]].astype(float)
            if spec.get("bone_only", False):
                vals = vals[vals > otsu_threshold]

            samples[name] = vals

    return samples


def compute_roi_moments(roi_samples: Dict[str, np.ndarray]) -> Dict[str, Dict[str, float]]:
    """Calculates statistical moments and distribution metrics for each ROI sample.

    Args:
        roi_samples: Dictionary mapping ROI name to array of intensity samples.

    Returns:
        Dictionary mapping ROI name to dictionary of statistical metrics.
    """
    stats = {}
    for name, vals in roi_samples.items():
        if len(vals) == 0:
            stats[name] = {
                "voxel_count": 0,
                "mean": float("nan"),
                "std": float("nan"),
                "median": float("nan"),
                "iqr": float("nan"),
                "skewness": float("nan"),
                "min": float("nan"),
                "max": float("nan"),
                "p05": float("nan"),
                "p95": float("nan"),
                "snr": float("nan"),
            }
            continue

        p05, p25, p50, p75, p95 = np.percentile(vals, [5, 25, 50, 75, 95])
        mu = float(vals.mean())
        sig = float(vals.std())
        sk = float(skew(vals))

        stats[name] = {
            "voxel_count": int(len(vals)),
            "mean": mu,
            "std": sig,
            "median": float(p50),
            "iqr": float(p75 - p25),
            "skewness": sk,
            "min": float(vals.min()),
            "max": float(vals.max()),
            "p05": float(p05),
            "p95": float(p95),
            "snr": float(mu / sig) if sig > 1e-9 else float("inf"),
        }

    return stats


def compute_tissue_contrast_and_separability(
    roi_samples: Dict[str, np.ndarray],
) -> Dict[str, Dict[str, float]]:
    """Evaluates tissue contrast-to-noise ratio (CNR), Bhattacharyya distance, and ROC AUC.

    Args:
        roi_samples: Dictionary mapping ROI names to intensity sample arrays.

    Returns:
        Dictionary of separability metrics for key tissue pairs.
    """
    pairs = [
        ("dorsal_cortex_vs_dome_core", "dorsal_cortex_zone3", "dome_core_zone2"),
        ("dorsal_cortex_vs_basicranium", "dorsal_cortex_zone3", "basicranium_zone1"),
        ("dome_core_vs_sedimentary_matrix", "dome_core_zone2", "sedimentary_matrix"),
        ("combined_bone_vs_matrix", None, "sedimentary_matrix"),
    ]

    results = {}

    for pair_name, key1, key2 in pairs:
        if key1 is None:
            # Combine all bone ROIs
            bone_parts = [
                roi_samples["dorsal_cortex_zone3"],
                roi_samples["dome_core_zone2"],
                roi_samples["basicranium_zone1"],
            ]
            s1 = np.concatenate(bone_parts)
        else:
            s1 = roi_samples[key1]

        s2 = roi_samples[key2]

        if len(s1) == 0 or len(s2) == 0:
            continue

        mu1, sig1 = float(s1.mean()), float(s1.std())
        mu2, sig2 = float(s2.mean()), float(s2.std())

        # Contrast-to-Noise Ratio (CNR)
        cnr = abs(mu1 - mu2) / np.sqrt(sig1**2 + sig2**2) if (sig1 > 0 or sig2 > 0) else 0.0

        # Gaussian Bhattacharyya distance
        if sig1 > 0 and sig2 > 0:
            term1 = 0.25 * np.log(0.25 * (sig1**2 / sig2**2 + sig2**2 / sig1**2 + 2.0))
            term2 = 0.25 * ((mu1 - mu2)**2 / (sig1**2 + sig2**2))
            db = float(term1 + term2)
        else:
            db = float("inf")

        # ROC AUC
        y_true = np.concatenate([np.ones(len(s1)), np.zeros(len(s2))])
        y_score = np.concatenate([s1, s2])
        try:
            auc = float(roc_auc_score(y_true, y_score))
        except Exception:
            auc = float("nan")

        results[pair_name] = {
            "mean_1": mu1,
            "std_1": sig1,
            "mean_2": mu2,
            "std_2": sig2,
            "cnr": float(cnr),
            "bhattacharyya_distance": float(db),
            "roc_auc": float(auc),
        }

    return results


def sample_transect_ray(
    volume_xyz: np.ndarray,
    t_composite_inv: np.ndarray,
    origin: np.ndarray,
    spacing: np.ndarray,
    p_start_g0: np.ndarray,
    p_end_g0: np.ndarray,
    num_samples: int = 201,
) -> Dict[str, Any]:
    """Samples continuous 1D ray probes through the CT volume using trilinear interpolation.

    Args:
        volume_xyz: 3D CT volume array (cols, rows, slices).
        t_composite_inv: 4x4 matrix mapping G_0 physical points to CT physical points.
        origin: CT physical origin [X0, Y0, Z0].
        spacing: CT voxel spacing [dx, dy, dz].
        p_start_g0: 3D start point in G_0 coordinates (mm).
        p_end_g0: 3D end point in G_0 coordinates (mm).
        num_samples: Number of equidistant samples along the ray probe.

    Returns:
        Dictionary with sample distances (mm), 3D points, and interpolated intensity values.
    """
    alphas = np.linspace(0.0, 1.0, num_samples)
    pts_g0 = np.outer(1.0 - alphas, p_start_g0) + np.outer(alphas, p_end_g0)

    pts_homo = np.hstack([pts_g0, np.ones((len(pts_g0), 1))])
    pts_ct = (t_composite_inv @ pts_homo.T).T[:, :3]

    vox_coords = (pts_ct - origin) / spacing
    coords_for_map = vox_coords.T  # (3, num_samples)

    # Trilinear interpolation (order=1)
    vals = map_coordinates(volume_xyz, coords_for_map, order=1, mode="nearest")
    total_dist = float(np.linalg.norm(p_end_g0 - p_start_g0))
    distances = alphas * total_dist

    return {
        "start_point_g0": p_start_g0.tolist(),
        "end_point_g0": p_end_g0.tolist(),
        "total_length_mm": total_dist,
        "num_samples": num_samples,
        "distances_mm": distances.tolist(),
        "intensities": [float(v) for v in vals],
        "points_g0": pts_g0.tolist(),
    }


def evaluate_cupping_profile(
    volume_xyz: np.ndarray,
    t_composite_inv: np.ndarray,
    origin: np.ndarray,
    spacing: np.ndarray,
    slice_index: int = 350,
    row_index: int = 500,
    otsu_threshold: int = 20864,
) -> Dict[str, Any]:
    """Quantifies beam-hardening / cupping artifact across coronal cranial bone section.

    Evaluates radial intensity drop from peripheral cortical margins to the central dome core.

    Args:
        volume_xyz: 3D CT volume array (cols, rows, slices).
        t_composite_inv: 4x4 matrix mapping G_0 physical points to CT physical points.
        origin: CT physical origin.
        spacing: CT voxel spacing.
        slice_index: Transverse slice index (k).
        row_index: Coronal row index (j).
        otsu_threshold: Bone separation threshold.

    Returns:
        Dictionary with periphery mean, center mean, and percentage cupping drop.
    """
    slice_profile = volume_xyz[:, row_index, slice_index]
    cols = np.arange(len(slice_profile))

    bone_mask = slice_profile > otsu_threshold
    bone_cols = cols[bone_mask]
    bone_vals = slice_profile[bone_mask].astype(float)

    if len(bone_vals) < 20:
        return {
            "status": "INSUFFICIENT_BONE_VOXELS",
            "bone_voxel_count": len(bone_vals),
            "cupping_drop_pct": 0.0,
        }

    n_periph = max(5, int(0.15 * len(bone_vals)))
    left_periph = bone_vals[:n_periph]
    right_periph = bone_vals[-n_periph:]
    periph_mean = float((np.mean(left_periph) + np.mean(right_periph)) / 2.0)

    center_start = len(bone_vals) // 2 - n_periph // 2
    center_end = center_start + n_periph
    center_vals = bone_vals[center_start:center_end]
    center_mean = float(np.mean(center_vals))

    # Classical cupping: drop from periphery to center
    cupping_drop_pct = float((periph_mean - center_mean) / periph_mean * 100.0)

    return {
        "status": "EVALUATED",
        "slice_index": slice_index,
        "row_index": row_index,
        "bone_voxel_count": int(len(bone_vals)),
        "span_mm": float(len(bone_vals) * spacing[0]),
        "periphery_mean": periph_mean,
        "center_mean": center_mean,
        "cupping_drop_pct": cupping_drop_pct,
        "interpretation": (
            "Minimal or negative cupping drop indicates that industrial scanner beam-hardening "
            "correction was successfully applied during reconstruction, and diagenetic mineral "
            "infill maintains high attenuation throughout the central dome core."
        ),
    }

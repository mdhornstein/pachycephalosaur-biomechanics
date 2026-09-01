"""Anatomical subregion partitioning, metric extraction, and structured result export."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import numpy as np
import pandas as pd
from stegoceras_biomechanics.fea.solver import FESolution


@dataclass
class SubregionMetrics:
    region_name: str
    num_nodes: int
    num_elements: int
    max_von_mises_MPa: float
    p95_von_mises_MPa: float
    p99_von_mises_MPa: float
    mean_von_mises_MPa: float
    max_displacement_mm: float
    p95_displacement_mm: float
    mean_displacement_mm: float
    max_principal_strain_microstrain: float
    p95_principal_strain_microstrain: float
    mean_principal_strain_microstrain: float
    regional_strain_energy_mJ: float


def partition_anatomical_subregions(
    nodes: np.ndarray,
    elements: np.ndarray,
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """Defines geometric proxy Regions of Interest (ROIs) on the UALVP 2 skull.
    
    IMPORTANT METHODOLOGICAL NOTE:
    These subregions are defined via normalized geometric bounding boxes (Y, Z extents and lateral
    X-deviation) to provide reproducible spatial sampling of cranial zones. They represent
    independent, overlapping geometric proxy ROIs rather than a mutually exclusive anatomical
    segmentation or volume partition.
    """
    elem_centroids = np.mean(nodes[elements], axis=1)
    
    # Bounding extents
    min_b = np.min(nodes, axis=0)
    max_b = np.max(nodes, axis=0)
    x_mid = 0.5 * (min_b[0] + max_b[0])
    
    # Normalized coordinates [0, 1]
    norm_y = (nodes[:, 1] - min_b[1]) / (max_b[1] - min_b[1])
    norm_z = (nodes[:, 2] - min_b[2]) / (max_b[2] - min_b[2])
    norm_x_dev = np.abs(nodes[:, 0] - x_mid) / (0.5 * (max_b[0] - min_b[0]))
    
    elem_norm_y = (elem_centroids[:, 1] - min_b[1]) / (max_b[1] - min_b[1])
    elem_norm_z = (elem_centroids[:, 2] - min_b[2]) / (max_b[2] - min_b[2])
    elem_norm_x_dev = np.abs(elem_centroids[:, 0] - x_mid) / (0.5 * (max_b[0] - min_b[0]))
    
    # 1. Frontoparietal Dome Apex (Dorsal dome apex, high Z, mid-to-posterior Y)
    mask_dome_nodes = (norm_z >= 0.82) & (norm_y >= 0.40) & (norm_y <= 0.85)
    mask_dome_elems = (elem_norm_z >= 0.82) & (elem_norm_y >= 0.40) & (elem_norm_y <= 0.85)
    
    # 2. Sub-Dome Vault Core (Deep to apex, mid-high Z)
    mask_vault_nodes = (norm_z >= 0.55) & (norm_z < 0.82) & (norm_y >= 0.40) & (norm_y <= 0.85)
    mask_vault_elems = (elem_norm_z >= 0.55) & (elem_norm_z < 0.82) & (elem_norm_y >= 0.40) & (elem_norm_y <= 0.85)
    
    # 3. Endocranial Braincase Roof (Deep floor of sub-dome vault, mid Z)
    mask_brain_nodes = (norm_z >= 0.35) & (norm_z < 0.55) & (norm_y >= 0.50) & (norm_y <= 0.85) & (norm_x_dev <= 0.40)
    mask_brain_elems = (elem_norm_z >= 0.35) & (elem_norm_z < 0.55) & (elem_norm_y >= 0.50) & (elem_norm_y <= 0.85) & (elem_norm_x_dev <= 0.40)
    
    # 4. Lateral Cranium (High X deviation, cheek and temporal bars)
    mask_lat_nodes = (norm_x_dev > 0.60) & (norm_y >= 0.30) & (norm_y <= 0.85)
    mask_lat_elems = (elem_norm_x_dev > 0.60) & (elem_norm_y >= 0.30) & (elem_norm_y <= 0.85)
    
    # 5. Posterior Skull & Nuchal Shelf (Posterior margin, high Y)
    mask_nuchal_nodes = (norm_y > 0.85) & (norm_z >= 0.40)
    mask_nuchal_elems = (elem_norm_y > 0.85) & (elem_norm_z >= 0.40)
    
    # 6. Basicranium & Condyle (Ventral posterior, low Z, high Y)
    mask_basi_nodes = (norm_z < 0.35) & (norm_y >= 0.50)
    mask_basi_elems = (elem_norm_z < 0.35) & (elem_norm_y >= 0.50)
    
    subregions = {
        "Frontoparietal Dome Apex": (np.where(mask_dome_nodes)[0], np.where(mask_dome_elems)[0]),
        "Sub-Dome Vault Core": (np.where(mask_vault_nodes)[0], np.where(mask_vault_elems)[0]),
        "Endocranial Braincase Roof": (np.where(mask_brain_nodes)[0], np.where(mask_brain_elems)[0]),
        "Lateral Cranium": (np.where(mask_lat_nodes)[0], np.where(mask_lat_elems)[0]),
        "Posterior Skull & Nuchal Shelf": (np.where(mask_nuchal_nodes)[0], np.where(mask_nuchal_elems)[0]),
        "Basicranium & Condyle": (np.where(mask_basi_nodes)[0], np.where(mask_basi_elems)[0]),
    }
    return subregions


def extract_subregion_metrics(
    solution: FESolution,
    output_csv_path: str | Path | None = None,
    output_json_path: str | Path | None = None,
) -> list[SubregionMetrics]:
    """Computes comprehensive stress, strain, displacement, and energy metrics across subregions."""
    subregions = partition_anatomical_subregions(solution.nodes, solution.elements)
    
    # Compute element volumes for energy partitioning
    v0 = solution.nodes[solution.elements[:, 0]]
    v1 = solution.nodes[solution.elements[:, 1]]
    v2 = solution.nodes[solution.elements[:, 2]]
    v3 = solution.nodes[solution.elements[:, 3]]
    detJ = np.linalg.det(np.stack([v1 - v0, v2 - v0, v3 - v0], axis=2))
    elem_vols = np.abs(detJ) / 6.0
    
    # Element strain energy density: 0.5 * sigma : eps
    elem_energy_density = 0.5 * np.einsum('nij,nij->n', solution.element_stresses_MPa, solution.element_strains)
    elem_strain_energy = elem_energy_density * elem_vols
    
    metrics_list = []
    
    # Add Whole Skull as global summary
    metrics_list.append(SubregionMetrics(
        region_name="Whole Skull (Global)",
        num_nodes=int(solution.nodes.shape[0]),
        num_elements=int(solution.elements.shape[0]),
        max_von_mises_MPa=float(np.max(solution.nodal_von_mises_MPa)),
        p95_von_mises_MPa=float(np.percentile(solution.nodal_von_mises_MPa, 95)),
        p99_von_mises_MPa=float(np.percentile(solution.nodal_von_mises_MPa, 99)),
        mean_von_mises_MPa=float(np.mean(solution.nodal_von_mises_MPa)),
        max_displacement_mm=float(np.max(solution.displacement_magnitudes_mm)),
        p95_displacement_mm=float(np.percentile(solution.displacement_magnitudes_mm, 95)),
        mean_displacement_mm=float(np.mean(solution.displacement_magnitudes_mm)),
        max_principal_strain_microstrain=float(np.max(solution.nodal_max_principal_strain) * 1e6),
        p95_principal_strain_microstrain=float(np.percentile(solution.nodal_max_principal_strain, 95) * 1e6),
        mean_principal_strain_microstrain=float(np.mean(solution.nodal_max_principal_strain) * 1e6),
        regional_strain_energy_mJ=float(solution.total_strain_energy_mJ),
    ))
    
    for name, (n_idx, e_idx) in subregions.items():
        if len(n_idx) == 0 or len(e_idx) == 0:
            continue
            
        vm_reg = solution.nodal_von_mises_MPa[n_idx]
        disp_reg = solution.displacement_magnitudes_mm[n_idx]
        eps_reg = solution.nodal_max_principal_strain[n_idx] * 1e6  # microstrain
        energy_reg = float(np.sum(elem_strain_energy[e_idx]))
        
        metrics_list.append(SubregionMetrics(
            region_name=name,
            num_nodes=int(len(n_idx)),
            num_elements=int(len(e_idx)),
            max_von_mises_MPa=float(np.max(vm_reg)),
            p95_von_mises_MPa=float(np.percentile(vm_reg, 95)),
            p99_von_mises_MPa=float(np.percentile(vm_reg, 99)),
            mean_von_mises_MPa=float(np.mean(vm_reg)),
            max_displacement_mm=float(np.max(disp_reg)),
            p95_displacement_mm=float(np.percentile(disp_reg, 95)),
            mean_displacement_mm=float(np.mean(disp_reg)),
            max_principal_strain_microstrain=float(np.max(eps_reg)),
            p95_principal_strain_microstrain=float(np.percentile(eps_reg, 95)),
            mean_principal_strain_microstrain=float(np.mean(eps_reg)),
            regional_strain_energy_mJ=energy_reg,
        ))
        
    if output_csv_path is not None:
        df = pd.DataFrame([asdict(m) for m in metrics_list])
        df_p = Path(output_csv_path)
        df_p.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(df_p, index=False)
        
    if output_json_path is not None:
        json_p = Path(output_json_path)
        json_p.parent.mkdir(parents=True, exist_ok=True)
        with open(json_p, "w", encoding="utf-8") as f:
            json.dump([asdict(m) for m in metrics_list], f, indent=2)
            
    return metrics_list

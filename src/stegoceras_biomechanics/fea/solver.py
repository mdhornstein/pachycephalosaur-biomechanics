"""Finite Element Solver for 3D Linear Isotropic Elasticity using scikit-fem and SciPy."""

from dataclasses import dataclass
import time
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import skfem as fem
from skfem.models.elasticity import linear_elasticity, lame_parameters


@dataclass
class FESolution:
    nodes: np.ndarray
    elements: np.ndarray
    nodal_displacements_mm: np.ndarray
    displacement_magnitudes_mm: np.ndarray
    element_stresses_MPa: np.ndarray
    element_von_mises_MPa: np.ndarray
    nodal_von_mises_MPa: np.ndarray
    element_strains: np.ndarray
    element_max_principal_strain: np.ndarray
    nodal_max_principal_strain: np.ndarray
    reaction_forces_N: np.ndarray
    reaction_force_total_N: list[float]
    reaction_moment_total_Nmm: list[float]
    applied_force_total_N: list[float]
    total_strain_energy_mJ: float
    solver_type: str
    solver_runtime_seconds: float
    num_dofs: int
    youngs_modulus_MPa: float
    poisson_ratio: float
    algebraic_residual_norm: float = 0.0
    normalized_force_residual: float = 0.0
    normalized_moment_residual: float = 0.0
    absolute_moment_residual_Nmm: float = 0.0
    requested_solver: str = "auto"
    actual_solver: str = "direct"
    cg_maxiter: int = 5000
    cg_iterations: int = 0
    cg_converged: bool = False
    cg_final_residual: float = 0.0
    fallback_attempted: bool = False
    fallback_status: str = "none"


def solve_linear_elasticity(
    nodes: np.ndarray,
    elements: np.ndarray,
    youngs_modulus_MPa: float = 17000.0,
    poisson_ratio: float = 0.30,
    loaded_node_indices: np.ndarray | None = None,
    nodal_forces_N: np.ndarray | None = None,
    condyle_node_indices: np.ndarray | None = None,
    nuchal_node_indices: np.ndarray | None = None,
    solver_method: str = "auto",  # 'direct', 'cg', or 'auto'
    cg_tol: float = 1e-7,
    cg_maxiter: int = 5000,
    reference_point: list[float] | np.ndarray | None = None,
) -> FESolution:
    """Assembles and solves the 3D linear isotropic elasticity system Ku = f.
    
    Captures complete algebraic and static equilibrium residual metrics as well as
    detailed solver provenance (requested solver, actual solver, CG iteration count,
    CG residual, and direct fallback status).
    """
    start_time = time.time()
    
    num_nodes = nodes.shape[0]
    num_elements = elements.shape[0]
    num_dofs = num_nodes * 3
    
    # 1. Lamé parameters from E and nu
    lam, mu = lame_parameters(youngs_modulus_MPa, poisson_ratio)
    
    # 2. skfem mesh and basis construction (P1 linear tetrahedral elements)
    elem_vec = fem.ElementVector(fem.ElementTetP1())
    mesh_sk = fem.MeshTet1(nodes.T, elements.T)
    basis = fem.Basis(mesh_sk, elem_vec)
    
    # 3. Global stiffness matrix assembly K
    K = fem.asm(linear_elasticity(lam, mu), basis).tocsc()
    
    # 4. Global load vector assembly f
    f_global = np.zeros(num_dofs, dtype=np.float64)
    if loaded_node_indices is not None and nodal_forces_N is not None:
        for nid, f_vec in zip(loaded_node_indices, nodal_forces_N):
            f_global[3 * nid : 3 * nid + 3] += f_vec
            
    # 5. Boundary constraints (Dirichlet DOFs)
    fixed_dofs = []
    if condyle_node_indices is not None and len(condyle_node_indices) > 0:
        for nid in condyle_node_indices:
            fixed_dofs.extend([3 * nid, 3 * nid + 1, 3 * nid + 2])
            
    if nuchal_node_indices is not None and len(nuchal_node_indices) > 0:
        for nid in nuchal_node_indices:
            fixed_dofs.extend([3 * nid + 1, 3 * nid + 2])
            
    fixed_dofs = np.unique(np.array(fixed_dofs, dtype=np.int64))
    
    # 6. Condense and solve system Ku = f
    u_full = np.zeros(num_dofs, dtype=np.float64)
    
    free_dofs = np.setdiff1d(np.arange(num_dofs), fixed_dofs)
    K_ff = K[free_dofs, :][:, free_dofs]
    f_f = f_global[free_dofs]
    
    requested_solver = solver_method.lower()
    chosen_solver = requested_solver
    if chosen_solver == "auto":
        # Direct solver for <= 600k DOFs (~200k nodes), CG for larger
        chosen_solver = "direct" if num_dofs <= 600000 else "cg"
        
    actual_solver = chosen_solver
    cg_iterations = 0
    cg_converged = False
    cg_final_residual = 0.0
    fallback_attempted = False
    fallback_status = "none"
    
    norm_f_f = float(np.linalg.norm(f_f))
    
    if chosen_solver == "direct":
        u_f = spla.spsolve(K_ff, f_f)
    elif chosen_solver == "cg":
        # Jacobi diagonal preconditioner (SPD compatible)
        diag_K = K_ff.diagonal()
        diag_K[np.abs(diag_K) < 1e-12] = 1.0
        M_inv = sp.diags(1.0 / diag_K)
        
        iter_counter = [0]
        def cg_callback(xk):
            iter_counter[0] += 1
            
        u_f, info = spla.cg(K_ff, f_f, M=M_inv, rtol=cg_tol, maxiter=cg_maxiter, callback=cg_callback)
        cg_iterations = iter_counter[0]
        
        if norm_f_f > 1e-12:
            cg_final_residual = float(np.linalg.norm(K_ff.dot(u_f) - f_f) / norm_f_f)
        else:
            cg_final_residual = 0.0
            
        if info == 0:
            cg_converged = True
        else:
            cg_converged = False
            fallback_attempted = True
            try:
                u_f = spla.spsolve(K_ff, f_f)
                actual_solver = "direct_fallback"
                fallback_status = "success"
            except Exception as e:
                fallback_status = f"failed: {str(e)}"
    else:
        raise ValueError(f"Unknown solver method: {solver_method}")
        
    u_full[free_dofs] = u_f
    nodal_displacements = u_full.reshape((num_nodes, 3))
    disp_magnitudes = np.linalg.norm(nodal_displacements, axis=1)
    
    # Algebraic residual norm: ||K_ff * u_f - f_f|| / ||f_f||
    if norm_f_f > 1e-12:
        algebraic_residual = float(np.linalg.norm(K_ff.dot(u_f) - f_f) / norm_f_f)
    else:
        algebraic_residual = 0.00
        
    # 7. Reaction forces
    reactions_full = K.dot(u_full) - f_global
    reaction_forces = reactions_full.reshape((num_nodes, 3))
    total_reaction_force = np.sum(reaction_forces[condyle_node_indices if condyle_node_indices is not None else []], axis=0)
    if nuchal_node_indices is not None:
        total_reaction_force += np.sum(reaction_forces[nuchal_node_indices], axis=0)
        
    applied_force_total = np.sum(nodal_forces_N, axis=0) if nodal_forces_N is not None else np.zeros(3)
    
    # Normalized force residual: ||F_applied + F_reaction|| / ||F_applied||
    norm_f_app = np.linalg.norm(applied_force_total)
    if norm_f_app > 1e-12:
        norm_force_residual = float(np.linalg.norm(applied_force_total + total_reaction_force) / norm_f_app)
    else:
        norm_force_residual = 0.0
        
    # Reaction moment about reference point
    if reference_point is None:
        ref_pt = np.mean(nodes, axis=0)
    else:
        ref_pt = np.array(reference_point, dtype=np.float64)
        
    r_condyle = nodes[condyle_node_indices] - ref_pt if condyle_node_indices is not None else np.zeros((0, 3))
    r_nuchal = nodes[nuchal_node_indices] - ref_pt if nuchal_node_indices is not None else np.zeros((0, 3))
    
    m_condyle = np.sum(np.cross(r_condyle, reaction_forces[condyle_node_indices]), axis=0) if len(r_condyle) > 0 else np.zeros(3)
    m_nuchal = np.sum(np.cross(r_nuchal, reaction_forces[nuchal_node_indices]), axis=0) if len(r_nuchal) > 0 else np.zeros(3)
    total_reaction_moment = m_condyle + m_nuchal
    
    # Applied moment about reference point
    applied_moment_total = np.zeros(3)
    if loaded_node_indices is not None and nodal_forces_N is not None:
        r_loaded = nodes[loaded_node_indices] - ref_pt
        applied_moment_total = np.sum(np.cross(r_loaded, nodal_forces_N), axis=0)
        
    abs_moment_residual = float(np.linalg.norm(applied_moment_total + total_reaction_moment))
    norm_m_app = float(np.linalg.norm(applied_moment_total))
    if norm_m_app >= 1e-6:
        norm_moment_residual = float(abs_moment_residual / norm_m_app)
    else:
        norm_moment_residual = float("nan")
    
    # 8. Compute element strain and stress tensors
    # For linear tetrahedra, strain/stress is uniform per element
    v0 = nodes[elements[:, 0]]
    v1 = nodes[elements[:, 1]]
    v2 = nodes[elements[:, 2]]
    v3 = nodes[elements[:, 3]]
    
    u0 = nodal_displacements[elements[:, 0]]
    u1 = nodal_displacements[elements[:, 1]]
    u2 = nodal_displacements[elements[:, 2]]
    u3 = nodal_displacements[elements[:, 3]]
    
    # Inverse Jacobian matrix per element
    J = np.stack([v1 - v0, v2 - v0, v3 - v0], axis=2)  # (N_elem, 3, 3)
    invJ = np.linalg.inv(J)
    
    # Displacement gradient du/dX = [u1-u0, u2-u0, u3-u0] * invJ
    du = np.stack([u1 - u0, u2 - u0, u3 - u0], axis=2)
    grad_u = np.einsum('nij,njk->nik', du, invJ)
    
    # Infinitesimal strain: epsilon = 0.5 * (grad_u + grad_u.T)
    eps = 0.5 * (grad_u + np.transpose(grad_u, (0, 2, 1)))  # (N_elem, 3, 3)
    
    # Trace of strain
    tr_eps = eps[:, 0, 0] + eps[:, 1, 1] + eps[:, 2, 2]
    
    # Cauchy stress: sigma = lambda * tr(eps) * I + 2 * mu * eps
    eye3 = np.eye(3)[np.newaxis, :, :]
    sigma = lam * tr_eps[:, np.newaxis, np.newaxis] * eye3 + 2.0 * mu * eps
    
    # Von Mises stress per element:
    # sigma_vM = sqrt(1/2 * ((sxx-syy)^2 + (syy-szz)^2 + (szz-sxx)^2 + 6*(sxy^2 + syz^2 + szx^2)))
    sxx, syy, szz = sigma[:, 0, 0], sigma[:, 1, 1], sigma[:, 2, 2]
    sxy, syz, szx = sigma[:, 0, 1], sigma[:, 1, 2], sigma[:, 2, 0]
    
    vm_element = np.sqrt(
        0.5 * ((sxx - syy)**2 + (syy - szz)**2 + (szz - sxx)**2 + 6.0 * (sxy**2 + syz**2 + szx**2))
    )
    
    # Principal strains per element via eigenvalue decomposition of symmetric 3x3 strain
    eig_vals_eps = np.linalg.eigvalsh(eps)  # sorted ascending: e3, e2, e1
    max_principal_strain_elem = eig_vals_eps[:, 2]  # e1 (maximum principal strain)
    
    # Project element von Mises and strains to nodes via area/volume averaging
    detJ = np.linalg.det(J)
    elem_vols = np.abs(detJ) / 6.0
    
    nodal_vm_sum = np.zeros(num_nodes, dtype=np.float64)
    nodal_eps_sum = np.zeros(num_nodes, dtype=np.float64)
    nodal_vol_sum = np.zeros(num_nodes, dtype=np.float64)
    
    for i in range(4):
        node_ids = elements[:, i]
        np.add.at(nodal_vm_sum, node_ids, vm_element * elem_vols)
        np.add.at(nodal_eps_sum, node_ids, max_principal_strain_elem * elem_vols)
        np.add.at(nodal_vol_sum, node_ids, elem_vols)
        
    safe_nodal_vol = np.maximum(nodal_vol_sum, 1e-12)
    nodal_von_mises = nodal_vm_sum / safe_nodal_vol
    nodal_max_principal_strain = nodal_eps_sum / safe_nodal_vol
    
    # Total strain energy: U = 1/2 * u^T K u
    total_strain_energy = float(0.5 * np.dot(u_full, K.dot(u_full)))
    
    runtime = time.time() - start_time
    
    return FESolution(
        nodes=nodes,
        elements=elements,
        nodal_displacements_mm=nodal_displacements,
        displacement_magnitudes_mm=disp_magnitudes,
        element_stresses_MPa=sigma,
        element_von_mises_MPa=vm_element,
        nodal_von_mises_MPa=nodal_von_mises,
        element_strains=eps,
        element_max_principal_strain=max_principal_strain_elem,
        nodal_max_principal_strain=nodal_max_principal_strain,
        reaction_forces_N=reaction_forces,
        reaction_force_total_N=total_reaction_force.tolist(),
        reaction_moment_total_Nmm=total_reaction_moment.tolist(),
        applied_force_total_N=applied_force_total.tolist(),
        total_strain_energy_mJ=total_strain_energy,
        solver_type=chosen_solver,
        solver_runtime_seconds=float(runtime),
        num_dofs=int(num_dofs),
        youngs_modulus_MPa=float(youngs_modulus_MPa),
        poisson_ratio=float(poisson_ratio),
        algebraic_residual_norm=algebraic_residual,
        normalized_force_residual=norm_force_residual,
        normalized_moment_residual=norm_moment_residual,
        absolute_moment_residual_Nmm=abs_moment_residual,
        requested_solver=requested_solver,
        actual_solver=actual_solver,
        cg_maxiter=cg_maxiter,
        cg_iterations=cg_iterations,
        cg_converged=cg_converged,
        cg_final_residual=cg_final_residual,
        fallback_attempted=fallback_attempted,
        fallback_status=fallback_status,
    )

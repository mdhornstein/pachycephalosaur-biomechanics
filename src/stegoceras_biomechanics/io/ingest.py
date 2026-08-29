"""Ingestion tooling for local authenticated downloads and raw scan validation."""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import shutil
import zipfile
import tarfile
import yaml

from stegoceras_biomechanics.io.manifest import compute_sha256, load_manifest


def get_downloads_dir(project_root: Optional[Path] = None) -> Path:
    """Return path to data/raw/downloads/ staging directory."""
    if project_root is None:
        project_root = Path(__file__).resolve().parents[3]
    return project_root / "data" / "raw" / "downloads"


def scan_downloads(project_root: Optional[Path] = None) -> List[Path]:
    """Scan the downloads staging directory for newly placed archive files."""
    downloads_dir = get_downloads_dir(project_root)
    if not downloads_dir.exists():
        return []
    
    extensions = {".zip", ".tar", ".gz", ".tgz", ".dcm", ".obj", ".stl", ".ply", ".gltf", ".glb"}
    found = [p for p in downloads_dir.iterdir() if p.is_file() and p.suffix.lower() in extensions]
    return sorted(found)


def _is_safe_path(base_dir: Path, target_path: Path) -> bool:
    """Verify that target_path resolves strictly inside base_dir."""
    try:
        resolved_base = base_dir.resolve()
        resolved_target = target_path.resolve()
        # Check if resolved_target is within resolved_base
        return resolved_base == resolved_target or resolved_base in resolved_target.parents
    except Exception:
        return False


def unpack_archive(archive_path: Path, target_dir: Path) -> List[Path]:
    """Safely extract a ZIP or TAR archive into a destination folder with path-traversal protection.
    
    Args:
        archive_path: Path to archive.
        target_dir: Target directory.
        
    Returns:
        List of extracted file paths.
        
    Raises:
        ValueError: If archive contains unsafe path traversal attempts.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    resolved_target_dir = target_dir.resolve()
    extracted = []
    
    if archive_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                member_path = member.filename
                # Path traversal check
                if Path(member_path).is_absolute() or ".." in Path(member_path).parts:
                    raise ValueError(f"Unsafe archive member detected (path traversal): {member_path}")
                
                dest = (resolved_target_dir / member_path).resolve()
                if not _is_safe_path(resolved_target_dir, dest):
                    raise ValueError(f"Unsafe archive destination detected: {member_path} -> {dest}")
                
                zip_ref.extract(member, resolved_target_dir)
                extracted.append(dest)
                
    elif archive_path.suffix.lower() in [".tar", ".gz", ".tgz"]:
        with tarfile.open(archive_path, 'r:*') as tar_ref:
            for member in tar_ref.getmembers():
                member_path = member.name
                if Path(member_path).is_absolute() or ".." in Path(member_path).parts:
                    raise ValueError(f"Unsafe archive member detected (path traversal): {member_path}")
                if member.issym() or member.islnk():
                    # Reject symlinks that could escape sandbox
                    link_target = Path(member.linkname)
                    if link_target.is_absolute() or ".." in link_target.parts:
                        raise ValueError(f"Unsafe archive link detected: {member_path} -> {member.linkname}")
                        
                dest = (resolved_target_dir / member_path).resolve()
                if not _is_safe_path(resolved_target_dir, dest):
                    raise ValueError(f"Unsafe archive destination detected: {member_path} -> {dest}")
                
                tar_ref.extract(member, resolved_target_dir)
                extracted.append(dest)
    else:
        # Single file copy
        dest = resolved_target_dir / archive_path.name
        shutil.copy2(archive_path, dest)
        extracted = [dest]
        
    return extracted


def ingest_file(source_path: Path, dataset_id: str, project_root: Optional[Path] = None) -> Dict[str, any]:
    """Ingest a validated file or archive into the canonical repository structure.
    
    Args:
        source_path: Path to downloaded source file.
        dataset_id: Target dataset identifier from manifest.
        project_root: Workspace root directory.
        
    Returns:
        Ingestion result dictionary with paths, size, and SHA256 checksum.
    """
    if project_root is None:
        project_root = Path(__file__).resolve().parents[3]
        
    manifest = load_manifest()
    entry = None
    for item in manifest.get("datasets", []):
        if item.get("dataset_id") == dataset_id:
            entry = item
            break
            
    if entry is None:
        raise ValueError(f"Dataset ID '{dataset_id}' not found in manifest.")
        
    local_rel = entry.get("local_path")
    if not local_rel:
        raise ValueError(f"No local_path defined for dataset '{dataset_id}'.")
        
    dest_path = project_root / local_rel
    sha256 = compute_sha256(source_path)
    file_size = source_path.stat().st_size
    
    if dest_path.suffix:  # Is a specific file path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest_path)
        extracted_files = [dest_path]
    else:  # Is a directory destination
        dest_path.mkdir(parents=True, exist_ok=True)
        extracted_files = unpack_archive(source_path, dest_path)
        
    return {
        "dataset_id": dataset_id,
        "source": str(source_path),
        "destination": str(dest_path),
        "file_size_bytes": file_size,
        "sha256": sha256,
        "extracted_file_count": len(extracted_files),
    }

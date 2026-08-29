"""Dataset manifest parser, validator, and SHA-256 integrity manager."""

from pathlib import Path
from typing import Any, Dict, List, Optional
import hashlib
import yaml


def compute_sha256(filepath: Path, chunk_size: int = 65536) -> str:
    """Compute the SHA-256 hex digest for a local file.
    
    Args:
        filepath: Path to the target file.
        chunk_size: Buffer size in bytes.
        
    Returns:
        Hexadecimal SHA-256 string.
    """
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_manifest(manifest_path: Optional[Path] = None) -> Dict[str, Any]:
    """Load and parse the YAML dataset manifest.
    
    Args:
        manifest_path: Optional explicit path. Defaults to data/metadata/dataset_manifest.yaml.
        
    Returns:
        Parsed dictionary representing the manifest.
    """
    if manifest_path is None:
        manifest_path = Path(__file__).resolve().parents[3] / "data" / "metadata" / "dataset_manifest.yaml"
        
    if not manifest_path.exists():
        raise FileNotFoundError(f"Dataset manifest not found at: {manifest_path}")
        
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    return data


def get_dataset_entry(dataset_id: str, manifest: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Retrieve a specific dataset record by ID."""
    if manifest is None:
        manifest = load_manifest()
        
    for entry in manifest.get("datasets", []):
        if entry.get("dataset_id") == dataset_id:
            return entry
    return None


def audit_local_inventory(manifest: Optional[Dict[str, Any]] = None, project_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Audit the presence and integrity of all manifest datasets in the local workspace.
    
    Returns:
        List of audit status dictionaries for each registered dataset.
    """
    if manifest is None:
        manifest = load_manifest()
    if project_root is None:
        project_root = Path(__file__).resolve().parents[3]
        
    audit_results = []
    
    for item in manifest.get("datasets", []):
        local_rel = item.get("local_path")
        status = {
            "dataset_id": item.get("dataset_id"),
            "element": item.get("element"),
            "provenance_tier": item.get("provenance_tier"),
            "expected_path": local_rel,
            "exists": False,
            "is_dir": False,
            "file_count": 0,
            "size_bytes": 0,
            "sha256": None,
            "checksum_match": None,
        }
        
        if local_rel:
            full_path = project_root / local_rel
            if full_path.exists():
                status["exists"] = True
                if full_path.is_dir():
                    status["is_dir"] = True
                    files = [p for p in full_path.glob("**/*") if p.is_file() and p.name != ".gitkeep"]
                    status["file_count"] = len(files)
                    status["size_bytes"] = sum(p.stat().st_size for p in files)
                else:
                    status["is_dir"] = False
                    status["file_count"] = 1
                    status["size_bytes"] = full_path.stat().st_size
                    computed_hash = compute_sha256(full_path)
                    status["sha256"] = computed_hash
                    expected_hash = item.get("sha256_checksum")
                    if expected_hash and expected_hash != "UNKNOWN":
                        status["checksum_match"] = (computed_hash == expected_hash)
                        
        audit_results.append(status)
        
    return audit_results

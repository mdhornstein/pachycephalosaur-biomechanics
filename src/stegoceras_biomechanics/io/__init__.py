"""I/O package for dataset manifest parsing, checksum computation, and data ingestion."""

from stegoceras_biomechanics.io.manifest import (
    compute_sha256,
    load_manifest,
    get_dataset_entry,
    audit_local_inventory,
)
from stegoceras_biomechanics.io.ingest import (
    get_downloads_dir,
    scan_downloads,
    unpack_archive,
    ingest_file,
)

__all__ = [
    "compute_sha256",
    "load_manifest",
    "get_dataset_entry",
    "audit_local_inventory",
    "get_downloads_dir",
    "scan_downloads",
    "unpack_archive",
    "ingest_file",
]

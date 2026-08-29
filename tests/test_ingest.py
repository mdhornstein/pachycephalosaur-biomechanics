"""Test data ingestion and archive safety mechanisms."""

from pathlib import Path
import zipfile
import tarfile
import pytest

from stegoceras_biomechanics.io.ingest import unpack_archive, _is_safe_path


def test_safe_zip_extraction(tmp_path):
    """Verify standard clean zip extraction."""
    zip_path = tmp_path / "clean.zip"
    target_dir = tmp_path / "extracted"
    
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("subfolder/file1.txt", "content1")
        zf.writestr("file2.txt", "content2")
        
    extracted = unpack_archive(zip_path, target_dir)
    assert len(extracted) == 2
    assert (target_dir / "subfolder" / "file1.txt").exists()
    assert (target_dir / "file2.txt").exists()


def test_malicious_zip_path_traversal_rejected(tmp_path):
    """Verify rejection of zip archives containing path traversal members."""
    zip_path = tmp_path / "malicious.zip"
    target_dir = tmp_path / "extracted_safe"
    
    with zipfile.ZipFile(zip_path, "w") as zf:
        # Member attempting to escape target directory
        zf.writestr("../escaped.txt", "malicious payload")
        
    with pytest.raises(ValueError, match="Unsafe archive member"):
        unpack_archive(zip_path, target_dir)
        
    assert not (tmp_path / "escaped.txt").exists()


def test_malicious_tar_path_traversal_rejected(tmp_path):
    """Verify rejection of tar archives containing path traversal members."""
    tar_path = tmp_path / "malicious.tar"
    target_dir = tmp_path / "extracted_safe"
    
    # Create tar with escaping name
    with tarfile.open(tar_path, "w") as tf:
        info = tarfile.TarInfo(name="../escaped_tar.txt")
        info.size = len(b"payload")
        import io
        tf.addfile(info, io.BytesIO(b"payload"))
        
    with pytest.raises(ValueError, match="Unsafe archive member"):
        unpack_archive(tar_path, target_dir)
        
    assert not (tmp_path / "escaped_tar.txt").exists()

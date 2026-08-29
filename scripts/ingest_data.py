#!/usr/bin/env python3
"""Data Ingestion & Integrity Audit CLI for Stegoceras Biomechanics Project.

Provides tools to audit workspace dataset inventory, verify SHA-256 checksums,
and ingest newly downloaded raw CT archives and 3D surface meshes from staging.
"""

import argparse
import sys
from pathlib import Path

# Add src to path for direct script execution
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root / "src"))

from stegoceras_biomechanics.io.manifest import load_manifest, audit_local_inventory, compute_sha256
from stegoceras_biomechanics.io.ingest import scan_downloads, ingest_file, get_downloads_dir


def print_banner():
    print("=" * 80)
    print("🦕 STEGOCERAS VALIDUM (UALVP 2) - DATASET INGESTION & PROVENANCE AUDIT")
    print("=" * 80)


def cmd_audit(args):
    print_banner()
    print(f"Auditing workspace inventory against: data/metadata/dataset_manifest.yaml\n")
    results = audit_local_inventory(project_root=project_root)
    
    table_fmt = "{:<25} {:<12} {:<28} {:<10} {:<12}"
    print(table_fmt.format("Dataset ID", "Element", "Provenance Tier", "Exists?", "Size / Files"))
    print("-" * 90)
    
    for item in results:
        status_str = "✅ YES" if item["exists"] else "❌ NO"
        if item["exists"]:
            if item["is_dir"]:
                size_str = f"{item['file_count']} files ({item['size_bytes'] / (1024*1024):.1f} MB)"
            else:
                size_str = f"{item['size_bytes'] / (1024*1024):.2f} MB"
        else:
            size_str = "N/A"
            
        print(table_fmt.format(
            item["dataset_id"],
            str(item["element"])[:11],
            item["provenance_tier"],
            status_str,
            size_str
        ))
        
    print("-" * 90)
    print("\n💡 INSTRUCTIONS FOR ACQUIRING UALVP 2 PRIMARY CT DATA:")
    print("1. Log in to your MorphoSource account at https://www.morphosource.org/")
    print("2. Navigate to Cranium Media 000018284: https://www.morphosource.org/concern/media/000018284")
    print("3. Click 'Download', submit research use statement (>= 50 chars), and accept CC BY-NC 4.0 terms.")
    print("4. Place the downloaded archive into: data/raw/downloads/")
    print("5. Run: uv run python scripts/ingest_data.py --scan-downloads\n")


def cmd_scan_downloads(args):
    print_banner()
    downloads_dir = get_downloads_dir(project_root)
    print(f"Scanning downloads staging directory: {downloads_dir}\n")
    found = scan_downloads(project_root)
    
    if not found:
        print(f"No archive or mesh files found in {downloads_dir}.")
        print("To ingest data, please place downloaded files into this folder and re-run.")
        return
        
    print(f"Found {len(found)} candidate file(s):")
    for f in found:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  • {f.name} ({size_mb:.2f} MB) | SHA-256: {compute_sha256(f)[:16]}...")
        
    print("\nTo ingest a specific file into the project structure, run:")
    print("  uv run python scripts/ingest_data.py --ingest <filename> --dataset <DATASET_ID>")


def cmd_ingest(args):
    print_banner()
    source_file = Path(args.ingest)
    if not source_file.is_absolute():
        source_file = get_downloads_dir(project_root) / source_file
        
    if not source_file.exists():
        print(f"❌ Error: Source file not found: {source_file}")
        sys.exit(1)
        
    print(f"Ingesting: {source_file.name}")
    print(f"Target dataset: {args.dataset}\n")
    
    try:
        res = ingest_file(source_file, args.dataset, project_root=project_root)
        print("✅ Ingestion successful!")
        print(f"  • Destination: {res['destination']}")
        print(f"  • File size: {res['file_size_bytes']} bytes ({res['file_size_bytes'] / (1024*1024):.2f} MB)")
        print(f"  • Extracted files: {res['extracted_file_count']}")
        print(f"  • SHA-256 Checksum: {res['sha256']}")
    except Exception as e:
        print(f"❌ Ingestion failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Dataset Ingestion & Provenance Audit CLI for Stegoceras Biomechanics Project"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    parser_audit = subparsers.add_parser("audit", help="Audit local workspace dataset inventory")
    parser_scan = subparsers.add_parser("scan-downloads", help="Scan staging directory for downloaded files")
    parser_ingest = subparsers.add_parser("ingest", help="Ingest a downloaded file into repository structure")
    parser_ingest.add_argument("ingest", help="Filename in downloads/ or absolute path")
    parser_ingest.add_argument("--dataset", required=True, help="Target Dataset ID (e.g., UALVP2-MS-CRAN-01)")
    
    # Default behavior if no subcommand
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()
    if args.command == "audit":
        cmd_audit(args)
    elif args.command == "scan-downloads":
        cmd_scan_downloads(args)
    elif args.command == "ingest":
        cmd_ingest(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

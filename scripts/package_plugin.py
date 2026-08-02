"""Build or check the deterministic plugin archive."""

from __future__ import annotations

import argparse
import sys

from repo_tools import (
    archive_check_errors,
    archive_matches_source,
    build_archive_bytes,
    find_repo_root,
    package_repository,
    validate_repository,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build or check deterministic skill.zip.")
    parser.add_argument("root", nargs="?", help="repository root; defaults to the script's repository")
    parser.add_argument("--check", action="store_true", help="prove the existing archive matches current source")
    parser.add_argument("--skip-official", action="store_true", help="skip the official validator")
    args = parser.parse_args(argv)
    root = find_repo_root(args.root) if args.root else find_repo_root()
    official = False if args.skip_official else None
    if args.check:
        errors = validate_repository(root, run_official=not args.skip_official, check_archive=True)
        if errors:
            print(f"Archive freshness: FAIL ({len(errors)} issue(s))")
            for error in errors:
                print(f"- {error}")
            return 1
        print("Archive freshness: PASS (skill.zip matches validated source)")
        return 0
    try:
        archive = package_repository(root, official_validator=official)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if not archive_matches_source(root):
        print("Archive build: FAIL (post-build freshness check failed)", file=sys.stderr)
        return 1
    print(f"Archive build: PASS ({archive.name}, {len(build_archive_bytes(root))} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

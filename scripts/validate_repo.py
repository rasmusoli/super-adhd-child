"""Run the local repository audit."""

from __future__ import annotations

import argparse
import sys

from repo_tools import discover_official_validator, find_repo_root, validate_repository


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Super ADHD Child plugin repository.")
    parser.add_argument("root", nargs="?", help="repository root; defaults to the script's repository")
    parser.add_argument("--skip-official", action="store_true", help="skip the official validator even when discoverable")
    parser.add_argument("--official-validator", help="path to the official validate_plugin.py")
    parser.add_argument("--no-archive", action="store_true", help="validate source without requiring a fresh skill.zip")
    args = parser.parse_args(argv)
    root = find_repo_root(args.root) if args.root else find_repo_root()
    validator = None if args.skip_official else args.official_validator
    errors = validate_repository(
        root,
        run_official=not args.skip_official,
        official_validator=validator,
        check_archive=not args.no_archive,
    )
    discovered = discover_official_validator(validator) if not args.skip_official else None
    if not args.skip_official:
        print(f"Official plugin validator: {'discovered' if discovered else 'not discoverable; local audit continues'}")
    if errors:
        print(f"Repository validation: FAIL ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

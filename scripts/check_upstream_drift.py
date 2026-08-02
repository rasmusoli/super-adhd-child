"""Report upstream drift without modifying vendored files."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from repo_tools import find_repo_root


def _load_inventory(root: Path) -> tuple[dict | None, list[str]]:
    path = root / "UPSTREAM_INVENTORY.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"UPSTREAM_INVENTORY.json: cannot read valid JSON: {exc}"]
    if not isinstance(value, dict) or value.get("schemaVersion") != 1 or not isinstance(value.get("upstreams"), list):
        return None, ["UPSTREAM_INVENTORY.json: expected schemaVersion 1 and an upstreams array"]
    errors: list[str] = []
    for entry in value["upstreams"]:
        required = ("name", "repository", "branch", "pinnedCommit", "vendoredPaths", "localNamespaceTransformation", "intentionalExclusions", "locallyModifiedFiles")
        if not isinstance(entry, dict) or any(not entry.get(field) for field in required):
            errors.append("UPSTREAM_INVENTORY.json: every upstream needs repository, pin, paths, transformation, exclusions, and local modifications")
            continue
        if not isinstance(entry["pinnedCommit"], str) or len(entry["pinnedCommit"]) != 40:
            errors.append(f"UPSTREAM_INVENTORY.json: invalid pinned commit for {entry.get('name', '<unknown>')}")
    return value, errors


def _inventory_path_errors(root: Path, inventory: dict) -> list[str]:
    errors: list[str] = []
    for entry in inventory["upstreams"]:
        for value in entry["vendoredPaths"] + entry["locallyModifiedFiles"]:
            if "*" in value:
                if not list(root.glob(value)):
                    errors.append(f"UPSTREAM_INVENTORY.json: path pattern matches nothing: {value}")
            else:
                candidate = root / value.rstrip("/")
                if not candidate.exists():
                    errors.append(f"UPSTREAM_INVENTORY.json: referenced path is missing: {value}")
    return errors


def _remote_head(entry: dict) -> tuple[str | None, str | None]:
    try:
        result = subprocess.run(
            ["git", "ls-remote", entry["repository"], f"refs/heads/{entry['branch']}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    if result.returncode != 0:
        return None, result.stderr.strip() or f"git ls-remote exited {result.returncode}"
    fields = result.stdout.strip().split()
    return (fields[0], None) if fields else (None, "remote returned no branch head")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check pinned upstream inventory without changing files.")
    parser.add_argument("root", nargs="?", help="repository root; defaults to the script's repository")
    parser.add_argument("--offline", action="store_true", help="validate inventory and paths without network access")
    parser.add_argument("--strict", action="store_true", help="return nonzero when a remote cannot be queried")
    args = parser.parse_args(argv)
    root = find_repo_root(args.root) if args.root else find_repo_root()
    inventory, errors = _load_inventory(root)
    if inventory is None:
        for error in errors:
            print(f"- {error}")
        return 1
    errors.extend(_inventory_path_errors(root, inventory))
    if errors:
        print(f"Upstream inventory: FAIL ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Upstream inventory: PASS ({len(inventory['upstreams'])} pinned source(s))")
    if args.offline:
        print("Remote drift: SKIP (offline mode; no files changed)")
        return 0
    drift = False
    unavailable = False
    for entry in inventory["upstreams"]:
        head, error = _remote_head(entry)
        if error:
            print(f"Remote drift: SKIP {entry['name']} ({error})")
            unavailable = True
            continue
        if head == entry["pinnedCommit"]:
            print(f"Remote drift: PASS {entry['name']} remains at pinned commit")
        else:
            print(f"Remote drift: NEWER {entry['name']} ({head}; pinned {entry['pinnedCommit']})")
            drift = True
    return 1 if drift or (args.strict and unavailable) else 0


if __name__ == "__main__":
    sys.exit(main())

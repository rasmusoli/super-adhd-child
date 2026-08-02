"""Dependency-free validation and deterministic packaging helpers."""

from __future__ import annotations

import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Iterable, Iterator, Sequence
from urllib.parse import unquote


EXPECTED_SKILLS = (
    "adhd-ideation",
    "brainstorming",
    "dispatching-parallel-agents",
    "executing-plans",
    "finishing-a-development-branch",
    "receiving-code-review",
    "requesting-code-review",
    "subagent-driven-development",
    "systematic-debugging",
    "test-driven-development",
    "using-git-worktrees",
    "using-super-adhd-child",
    "using-superpowers",
    "verification-before-completion",
    "writing-plans",
    "writing-skills",
)

PACKAGE_DIRS = (".codex-plugin", "skills")
PACKAGE_FILES = ("README.md", "LICENSE", "THIRD_PARTY_NOTICES.md")
ARCHIVE_NAME = "skill.zip"

ALLOWED_MANIFEST_FIELDS = {
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "skills",
    "interface",
}
ALLOWED_INTERFACE_FIELDS = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "defaultPrompt",
    "websiteURL",
    "screenshots",
}
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|[0-9A-Za-z-]*[A-Za-z-][0-9A-Za-z-]*))*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
INLINE_PATH = re.compile(r"^[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.[A-Za-z0-9]+$")
SHA = re.compile(r"\b[0-9a-f]{40}\b")
NAMESPACED_SKILL = re.compile(r"\b([a-z][a-z0-9-]*-[a-z0-9-]+):([a-z0-9-]+)\b")


def inventory_exclusion_errors(root: Path | str, inventory: dict) -> list[str]:
    """Validate machine-readable runtime exclusions and reject reintroduced paths."""

    root = Path(root).resolve()
    errors: list[str] = []
    for entry in inventory.get("upstreams", []):
        if not isinstance(entry, dict):
            continue
        excluded = entry.get("excludedPaths")
        if not isinstance(excluded, list):
            errors.append(
                f"UPSTREAM_INVENTORY.json: excludedPaths must be a list for {entry.get('name', '<unknown>')}"
            )
            continue
        for value in excluded:
            if not isinstance(value, str) or not value or Path(value).is_absolute():
                errors.append(
                    f"UPSTREAM_INVENTORY.json: excluded path must be a relative nonempty string: {value!r}"
                )
                continue
            relative = Path(value)
            if ".." in relative.parts or not value.startswith("skills/"):
                errors.append(f"UPSTREAM_INVENTORY.json: excluded path must stay beneath skills/: {value}")
                continue
            if not (root / relative).parent.is_dir():
                errors.append(f"UPSTREAM_INVENTORY.json: excluded path parent is missing: {value}")
            if (root / relative).exists():
                errors.append(f"{value}: excluded runtime path is present")
    return errors


def declared_excluded_paths(root: Path | str) -> set[str]:
    """Return declared excluded paths for archive defense-in-depth."""

    try:
        inventory = json.loads((Path(root).resolve() / "UPSTREAM_INVENTORY.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    paths: set[str] = set()
    for entry in inventory.get("upstreams", []) if isinstance(inventory, dict) else []:
        if isinstance(entry, dict) and isinstance(entry.get("excludedPaths"), list):
            paths.update(value for value in entry["excludedPaths"] if isinstance(value, str))
    return paths


def find_repo_root(start: Path | str | None = None) -> Path:
    """Find the nearest plugin root without depending on the current cwd."""

    candidate = Path(start or Path(__file__).resolve()).expanduser().resolve()
    if candidate.is_file():
        candidate = candidate.parent
    for directory in (candidate, *candidate.parents):
        if (directory / ".codex-plugin" / "plugin.json").is_file():
            return directory
    raise FileNotFoundError("could not find .codex-plugin/plugin.json from the requested path")


def _text_files(root: Path) -> Iterator[Path]:
    excluded = {".git", "__pycache__", ".superpowers", "tests", "docs"}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in excluded for part in path.relative_to(root).parts):
            continue
        if path.name == ARCHIVE_NAME or path.suffix.lower() in {".pyc", ".zip"}:
            continue
        try:
            path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        yield path


def _packaged_markdown(root: Path) -> Iterator[Path]:
    for directory_name in PACKAGE_DIRS:
        directory = root / directory_name
        if directory.is_dir():
            yield from sorted(directory.rglob("*.md"))
    for file_name in PACKAGE_FILES:
        path = root / file_name
        if path.suffix.lower() == ".md" and path.is_file():
            yield path


def _parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return {}, [f"{path}: cannot read skill: {exc}"]
    if not lines or lines[0].strip() != "---":
        return {}, [f"{path}: missing YAML frontmatter"]
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return {}, [f"{path}: unterminated YAML frontmatter"]
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        match = FRONTMATTER_FIELD.match(line)
        if not match:
            errors.append(f"{path}: invalid frontmatter line: {line}")
            continue
        fields[match.group(1)] = match.group(2).strip().strip("\"'")
    for required in ("name", "description"):
        if not fields.get(required):
            errors.append(f"{path}: frontmatter missing {required}")
    return fields, errors


def _without_fenced_blocks(markdown: str) -> str:
    output: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in markdown.splitlines(keepends=True):
        stripped = line.lstrip()
        if not in_fence and (stripped.startswith("```") or stripped.startswith("~~~")):
            in_fence = True
            fence_marker = stripped[:3]
            output.append("\n")
            continue
        if in_fence and stripped.startswith(fence_marker):
            in_fence = False
            output.append("\n")
            continue
        output.append("" if in_fence else line)
    return "".join(output)


def _relative_link_errors(path: Path, root: Path) -> list[str]:
    markdown = path.read_text(encoding="utf-8")
    visible = _without_fenced_blocks(markdown)
    errors: list[str] = []
    for raw_target in LINK.findall(visible):
        target = raw_target.strip().strip("<>")
        if (
            not target
            or target.startswith(("#", "/", "//"))
            or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target)
        ):
            continue
        target_path = unquote(target.split("#", 1)[0])
        if not target_path:
            continue
        resolved = (path.parent / target_path).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{path.relative_to(root)}: relative link escapes repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(root)}: missing relative link target: {target}")
    return errors


def _missing_inline_path_errors(path: Path, root: Path) -> list[str]:
    visible = _without_fenced_blocks(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    explicit_references = re.findall(
        r"\b(?:reference|file|source|document)\s*:\s*`([^`]+)`",
        visible,
        flags=re.IGNORECASE,
    )
    for value in explicit_references:
        value = value.strip()
        if not INLINE_PATH.match(value) or value.startswith(("http", "file")):
            continue
        resolved = (path.parent / value).resolve()
        try:
            resolved.relative_to(root.resolve())
        except ValueError:
            continue
        if not resolved.exists():
            errors.append(f"{path.relative_to(root)}: referenced local file is missing: {value}")
    return errors


def _support_script_errors(root: Path) -> list[str]:
    errors: list[str] = []
    candidates: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if "scripts" not in relative.parts:
            continue
        if path.suffix == ".sh" or not path.suffix:
            candidates.append(path)
    for path in candidates:
        if not os.access(path, os.X_OK):
            errors.append(f"{path.relative_to(root)}: support script is not executable")
    return errors


def _archive_members(root: Path) -> list[tuple[str, Path | None]]:
    excluded_directories = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".cache"}
    excluded_paths = declared_excluded_paths(root)

    def excluded(path: Path) -> bool:
        relative = path.relative_to(root)
        if any(part in excluded_directories for part in relative.parts):
            return True
        if relative.as_posix() in excluded_paths:
            return True
        return path.name in {".DS_Store"} or path.name.endswith((".pyc", ".tmp", ".swp", "~"))

    members: dict[str, Path | None] = {}
    for directory_name in PACKAGE_DIRS:
        directory = root / directory_name
        if not directory.is_dir():
            continue
        if excluded(directory):
            continue
        members[f"{directory_name}/"] = None
        for path in directory.rglob("*"):
            if excluded(path):
                continue
            relative = path.relative_to(root).as_posix()
            if path.is_dir():
                members[f"{relative}/"] = None
            elif path.is_file() and path.name != ARCHIVE_NAME:
                members[relative] = path
    for file_name in PACKAGE_FILES:
        path = root / file_name
        if path.is_file():
            members[file_name] = path
    return sorted(members.items())


def expected_archive_entries(root: Path | str) -> list[str]:
    return [name for name, _ in _archive_members(Path(root).resolve())]


def build_archive_bytes(root: Path | str) -> bytes:
    root = Path(root).resolve()
    with tempfile.NamedTemporaryFile(prefix="skill-", suffix=".zip") as temporary:
        with zipfile.ZipFile(
            temporary,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for name, path in _archive_members(root):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                if name.endswith("/"):
                    info.external_attr = (stat.S_IFDIR | 0o755) << 16
                    archive.writestr(info, b"")
                else:
                    mode = stat.S_IMODE(path.stat().st_mode)
                    info.external_attr = (stat.S_IFREG | mode) << 16
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, path.read_bytes())
        temporary.flush()
        temporary.seek(0)
        return temporary.read()


def archive_matches_source(root: Path | str) -> bool:
    root = Path(root).resolve()
    archive = root / ARCHIVE_NAME
    return archive.is_file() and archive.read_bytes() == build_archive_bytes(root)


def _archive_errors(root: Path) -> list[str]:
    archive = root / ARCHIVE_NAME
    if not archive.is_file():
        return ["skill.zip: archive is missing"]
    if not archive_matches_source(root):
        return ["skill.zip: archive is stale or was not built deterministically"]
    try:
        with zipfile.ZipFile(archive) as opened:
            actual = opened.namelist()
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"skill.zip: invalid archive: {exc}"]
    expected = expected_archive_entries(root)
    return [] if actual == expected else [
        f"skill.zip: contents differ from expected source set (expected {len(expected)}, found {len(actual)})"
    ]


def _manifest_errors(root: Path) -> list[str]:
    path = root / ".codex-plugin" / "plugin.json"
    errors: list[str] = []
    if not path.is_file():
        return [".codex-plugin/plugin.json: manifest is missing"]
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f".codex-plugin/plugin.json: invalid JSON: {exc}"]
    if not isinstance(manifest, dict):
        return [".codex-plugin/plugin.json: top-level value must be an object"]
    unsupported = sorted(set(manifest) - ALLOWED_MANIFEST_FIELDS)
    errors.extend(f".codex-plugin/plugin.json: unsupported manifest field: {field}" for field in unsupported)
    if manifest.get("name") != "super-adhd-child":
        errors.append(".codex-plugin/plugin.json: name must be super-adhd-child")
    if not isinstance(manifest.get("version"), str) or not SEMVER.fullmatch(manifest["version"]):
        errors.append(".codex-plugin/plugin.json: version must be a strict semantic version")
    if manifest.get("skills") != "./skills/":
        errors.append('.codex-plugin/plugin.json: skills must be "./skills/"')
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append(".codex-plugin/plugin.json: interface must be an object")
    else:
        errors.extend(
            f".codex-plugin/plugin.json: unsupported interface field: {field}"
            for field in sorted(set(interface) - ALLOWED_INTERFACE_FIELDS)
        )
        prompts = interface.get("defaultPrompt", [])
        if not any("Use ADHD mode" in prompt for prompt in prompts if isinstance(prompt, str)):
            errors.append(".codex-plugin/plugin.json: default prompts need an explicit ADHD invocation")
    return errors


def _skill_errors(root: Path) -> list[str]:
    skills_dir = root / "skills"
    errors: list[str] = []
    actual = sorted(path.name for path in skills_dir.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()) if skills_dir.is_dir() else []
    missing = sorted(set(EXPECTED_SKILLS) - set(actual))
    unexpected = sorted(set(actual) - set(EXPECTED_SKILLS))
    errors.extend(f"skills: missing expected skill: {name}" for name in missing)
    errors.extend(f"skills: unexpected skill directory: {name}" for name in unexpected)
    for name in EXPECTED_SKILLS:
        path = skills_dir / name / "SKILL.md"
        if not path.is_file():
            continue
        fields, frontmatter_errors = _parse_frontmatter(path)
        errors.extend(frontmatter_errors)
        if fields.get("name") and fields["name"] != name:
            errors.append(f"{path}: frontmatter name does not match directory name")
        if fields.get("name") and not SKILL_NAME.fullmatch(fields["name"]):
            errors.append(f"{path}: frontmatter name is not a lowercase hyphenated name")
    return errors


def _dependency_errors(root: Path) -> list[str]:
    forbidden_names = {
        "package.json",
        "package-lock.json",
        "npm-shrinkwrap.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "Gemfile",
        "Cargo.toml",
        "go.mod",
    }
    errors = [
        f"{path.relative_to(root)}: runtime dependency manifest is forbidden"
        for path in root.rglob("*")
        if path.is_file() and path.name in forbidden_names
    ]
    forbidden_commands = re.compile(r"^\s*(?:npm|pnpm|yarn)\s+(?:install|add|ci)\b|^\s*(?:pip|pip3)\s+install\b|^\s*apt(?:-get)?\s+install\b")
    for path in _text_files(root):
        if path.suffix.lower() not in {".js", ".cjs", ".sh"}:
            continue
        content = path.read_text(encoding="utf-8")
        if any(forbidden_commands.search(line) for line in content.splitlines()):
            errors.append(f"{path.relative_to(root)}: runtime dependency installation command is forbidden")
    return errors


def _source_and_routing_errors(root: Path) -> list[str]:
    errors: list[str] = []
    notices = root / "THIRD_PARTY_NOTICES.md"
    if not notices.is_file():
        errors.append("THIRD_PARTY_NOTICES.md: attribution notice is missing")
    else:
        notice_text = notices.read_text(encoding="utf-8")
        for sha in ("44c9b2d6e889982ac18c27d05a19fefe335194e1", "eaeba4e98b388b8d1d31a31572d91ff989e04c00"):
            if sha not in notice_text:
                errors.append(f"THIRD_PARTY_NOTICES.md: pinned source SHA is missing: {sha}")
        if "https://github.com/obra/superpowers" not in notice_text or "https://github.com/UditAkhourii/adhd" not in notice_text:
            errors.append("THIRD_PARTY_NOTICES.md: upstream repository attribution is incomplete")
    router = root / "skills" / "using-super-adhd-child" / "SKILL.md"
    collaboration = root / "skills" / "using-superpowers" / "SKILL.md"
    adhd = root / "skills" / "adhd-ideation" / "SKILL.md"
    router_text = router.read_text(encoding="utf-8") if router.is_file() else ""
    collaboration_text = collaboration.read_text(encoding="utf-8") if collaboration.is_file() else ""
    adhd_text = adhd.read_text(encoding="utf-8") if adhd.is_file() else ""
    router_lower = " ".join(router_text.lower().split())
    collaboration_lower = " ".join(collaboration_text.lower().split())
    adhd_lower = " ".join(adhd_text.lower().split())
    if "manual-first" not in router_lower or "do not use adhd automatically" not in router_lower:
        errors.append("using-super-adhd-child: manual-first routing contract is missing")
    if "super-adhd-child:brainstorming" not in router_text or "super-adhd-child:brainstorming" not in adhd_text:
        errors.append("using-super-adhd-child: ADHD-to-brainstorming handoff is missing")
    for marker in ("isolated subagents are unavailable", "capacity-sized batches", "estimates rather than guarantees"):
        if marker not in adhd_lower:
            errors.append(f"adhd-ideation: capability-aware guidance is missing: {marker}")
    if "inherited model" not in collaboration_lower:
        errors.append("using-superpowers: capability-aware guidance is missing: inherited model")
    if "/adhd" in (root / "README.md").read_text(encoding="utf-8") and "does not register" not in (root / "README.md").read_text(encoding="utf-8"):
        errors.append("README.md: /adhd must be described as unregistered or textual, not as a host command")
    return errors


def _inventory_errors(root: Path) -> list[str]:
    path = root / "UPSTREAM_INVENTORY.json"
    if not path.is_file():
        return ["UPSTREAM_INVENTORY.json: upstream inventory is missing"]
    try:
        inventory = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"UPSTREAM_INVENTORY.json: invalid JSON: {exc}"]
    if not isinstance(inventory, dict) or inventory.get("schemaVersion") != 1 or not isinstance(inventory.get("upstreams"), list):
        return ["UPSTREAM_INVENTORY.json: expected schemaVersion 1 and an upstreams array"]
    errors: list[str] = []
    fields = (
        "name",
        "repository",
        "branch",
        "pinnedCommit",
        "vendoredPaths",
        "localNamespaceTransformation",
        "intentionalExclusions",
        "locallyModifiedFiles",
    )
    for entry in inventory["upstreams"]:
        if not isinstance(entry, dict) or any(not entry.get(field) for field in fields):
            errors.append("UPSTREAM_INVENTORY.json: every upstream needs structured attribution and maintenance fields")
            continue
        if "excludedPaths" not in entry:
            errors.append(f"UPSTREAM_INVENTORY.json: excludedPaths is missing for {entry.get('name', '<unknown>')}")
        if not isinstance(entry["pinnedCommit"], str) or not SHA.fullmatch(entry["pinnedCommit"]):
            errors.append(f"UPSTREAM_INVENTORY.json: invalid pinned commit for {entry['name']}")
        for value in entry["vendoredPaths"] + entry["locallyModifiedFiles"]:
            if "*" in value:
                if not list(root.glob(value)):
                    errors.append(f"UPSTREAM_INVENTORY.json: path pattern matches nothing: {value}")
            elif not (root / value.rstrip("/")).exists():
                errors.append(f"UPSTREAM_INVENTORY.json: referenced path is missing: {value}")
    errors.extend(inventory_exclusion_errors(root, inventory))
    return errors


def _namespace_errors(root: Path) -> list[str]:
    errors: list[str] = []
    stale_cleanup_name = "close" + "_agent"
    stale_generic_label = "Agent" + "/Task"
    candidates = [root / name for name in PACKAGE_FILES if name != "THIRD_PARTY_NOTICES.md"]
    for directory_name in PACKAGE_DIRS:
        directory = root / directory_name
        if directory.is_dir():
            candidates.extend(directory.rglob("*"))
    for path in candidates:
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "superpowers:" in content:
            errors.append(f"{path.relative_to(root)}: unintended superpowers: namespace reference")
        if stale_cleanup_name in content or stale_generic_label in content:
            errors.append(f"{path.relative_to(root)}: stale agent lifecycle wording")
    return errors


def _skill_reference_errors(root: Path) -> list[str]:
    """Reject namespaced references that do not resolve to shipped skills."""

    shipped = {
        path.parent.name
        for path in (root / "skills").glob("*/SKILL.md")
    }
    errors: list[str] = []
    for path in _packaged_markdown(root):
        visible = _without_fenced_blocks(path.read_text(encoding="utf-8"))
        for namespace, name in NAMESPACED_SKILL.findall(visible):
            if namespace != "super-adhd-child" or name not in shipped:
                errors.append(
                    f"{path.relative_to(root)}: namespaced skill reference is not shipped: {namespace}:{name}"
                )
    return errors


def validate_repository(
    root: Path | str,
    *,
    run_official: bool = True,
    official_validator: Path | str | None = None,
    check_archive: bool = True,
) -> list[str]:
    """Return human-readable validation errors; an empty list means valid."""

    root = Path(root).resolve()
    errors: list[str] = []
    if not root.is_dir():
        return [f"repository root does not exist: {root}"]
    errors.extend(_manifest_errors(root))
    errors.extend(_skill_errors(root))
    errors.extend(_dependency_errors(root))
    errors.extend(_source_and_routing_errors(root))
    errors.extend(_inventory_errors(root))
    errors.extend(_namespace_errors(root))
    errors.extend(_skill_reference_errors(root))
    errors.extend(_support_script_errors(root))
    for markdown in _packaged_markdown(root):
        errors.extend(_relative_link_errors(markdown, root))
        errors.extend(_missing_inline_path_errors(markdown, root))
    if check_archive:
        errors.extend(_archive_errors(root))
    if run_official:
        errors.extend(_official_validator_errors(root, official_validator))
    return errors


def discover_official_validator(explicit: Path | str | None = None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    environment_path = os.environ.get("CODEX_OFFICIAL_VALIDATOR")
    if environment_path:
        candidates.append(Path(environment_path).expanduser())
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        candidates.append(Path(codex_home) / "skills/.system/plugin-creator/scripts/validate_plugin.py")
    candidates.append(Path.home() / ".codex/skills/.system/plugin-creator/scripts/validate_plugin.py")
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    return None


def _official_validator_errors(root: Path, explicit: Path | str | None) -> list[str]:
    validator = discover_official_validator(explicit)
    if validator is None:
        return []
    result = subprocess.run(
        [sys.executable, str(validator), str(root)],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode == 0:
        return []
    output = result.stdout.strip().splitlines()
    detail = output[-1] if output else f"exit code {result.returncode}"
    return [f"official plugin validator failed: {detail}"]


def package_repository(root: Path | str, *, official_validator: Path | str | None = None) -> Path:
    """Validate source, then atomically replace skill.zip with deterministic bytes."""

    root = Path(root).resolve()
    errors = validate_repository(
        root,
        run_official=official_validator is not False,
        official_validator=official_validator if official_validator is not False else None,
        check_archive=False,
    )
    if errors:
        raise ValueError("cannot package invalid repository:\n" + "\n".join(errors))
    archive = root / ARCHIVE_NAME
    temporary = root / f".{ARCHIVE_NAME}.tmp"
    try:
        temporary.write_bytes(build_archive_bytes(root))
        os.replace(temporary, archive)
    finally:
        temporary.unlink(missing_ok=True)
    return archive


def archive_check_errors(root: Path | str) -> list[str]:
    return _archive_errors(Path(root).resolve())

"""Build a plugin archive for ChatGPT from one of the plugins in this repository.

Run from the repository root::

    uv run python scripts/build_chatgpt_archive.py uk-open-data
    uv run python scripts/build_chatgpt_archive.py uk-open-data \
        --connector-url https://example.org/mcp

The plugin folders here are laid out for one assistant's marketplace. This script
writes the same skills in the portable Agent Plugins layout that ChatGPT reads:
a ``plugin.json`` at the root, ``skills/`` beside it, and ``mcp.json`` when a
connector address is given. Eval folders are left out. Nothing in the plugin
folder is changed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

import skills_ref

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
OPENAI = "com.openai"
CONNECTOR_NAME = "kindtech"
PORTABLE_FIELDS = ("version", "description", "homepage", "license", "keywords")
AUTHOR_FIELDS = ("name", "email", "url")
PLUGIN_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
# Limits OpenAI publishes for the listing text, in characters.
INTERFACE_LIMITS = {
    "displayName": 30,
    "shortDescription": 30,
    "longDescription": 4000,
    "developerName": 80,
}
LEFT_OUT = {"evals", "__pycache__"}
# A fixed date on every entry, so the same source always gives the same archive.
ZIP_DATE = (2026, 1, 1, 0, 0, 0)


class BuildError(Exception):
    """The plugin cannot be packaged. The message says what to fix."""


def main(argv: list[str] | None = None) -> int:
    """Build the archive and return the exit status."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("plugin", help="the folder name under plugins/")
    parser.add_argument(
        "--connector-url",
        help="the https address of the hosted connector; leave out for skills only",
    )
    parser.add_argument("--root", default=".", type=Path, help="the repository root")
    parser.add_argument("--out", default="dist", type=Path, help="the output folder")
    args = parser.parse_args(argv)
    try:
        archive = build_archive(args.root, args.plugin, args.out, args.connector_url)
    except BuildError as error:
        print(f"Cannot build: {error}", file=sys.stderr)
        return 1
    with zipfile.ZipFile(archive) as built:
        names = built.namelist()
    print(f"Wrote {archive} ({archive.stat().st_size:,} bytes, {len(names)} files):")
    for name in names:
        print(f"  {name}")
    return 0


def build_archive(
    root: Path, plugin: str, out_dir: Path, connector_url: str | None = None
) -> Path:
    """Write the archive for ``plugin`` into ``out_dir`` and return its path."""
    plugin_dir = root / "plugins" / plugin
    files = collect_files(root, plugin_dir, connector_url)
    version = json.loads(files["plugin.json"])["version"]
    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"{plugin}-chatgpt-{version}.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as built:
        for name in sorted(files):
            entry = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            built.writestr(entry, files[name])
    return archive


def collect_files(
    root: Path, plugin_dir: Path, connector_url: str | None = None
) -> dict[str, bytes]:
    """Return every file of the archive, keyed by its path inside it."""
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.is_file():
        raise BuildError(f"{manifest_path} is missing")
    source = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = {"plugin.json": _as_json(portable_manifest(source, plugin_dir))}
    skills = _skill_files(plugin_dir)
    if not skills:
        raise BuildError(f"{plugin_dir} has no skill to package")
    files.update(skills)
    if connector_url:
        files["mcp.json"] = _as_json(mcp_config(connector_url))
    licence = root / "LICENSE"
    if licence.is_file():
        files["LICENSE"] = licence.read_bytes()
    return files


def portable_manifest(source: dict, plugin_dir: Path) -> dict:
    """Turn a marketplace plugin manifest into a portable ``plugin.json``."""
    name = str(source.get("name", ""))
    if not PLUGIN_NAME.match(name) or len(name) > 64:
        raise BuildError(f'"{name}" is not a valid plugin name')
    if not source.get("version"):
        raise BuildError('the plugin manifest needs a "version"')
    manifest: dict = {"$schema": PLUGIN_SCHEMA, "name": name}
    manifest.update({f: source[f] for f in PORTABLE_FIELDS if source.get(f)})
    author = source.get("author") or {}
    if author:
        manifest["author"] = {f: author[f] for f in AUTHOR_FIELDS if author.get(f)}
    if source.get("repository"):
        manifest["repository"] = str(source["repository"])
    interface = _load_interface(plugin_dir)
    if interface:
        manifest["extensions"] = {OPENAI: {"interface": interface}}
    return manifest


def mcp_config(connector_url: str) -> dict:
    """Describe the hosted connector: one remote server that needs no sign-in."""
    parts = urlsplit(connector_url)
    if parts.scheme != "https" or not parts.hostname or parts.username:
        raise BuildError("the connector address must be a plain https:// address")
    server = {
        "type": "streamable-http",
        "url": connector_url,
        "extensions": {OPENAI: {"auth": {"type": "none"}}},
    }
    return {"$schema": MCP_SCHEMA, "mcpServers": {CONNECTOR_NAME: server}}


def _load_interface(plugin_dir: Path) -> dict:
    path = plugin_dir / "platforms" / "chatgpt.json"
    if not path.is_file():
        return {}
    interface = json.loads(path.read_text(encoding="utf-8")).get("interface", {})
    for field, limit in INTERFACE_LIMITS.items():
        if len(str(interface.get(field, ""))) > limit:
            raise BuildError(f"{path}: {field} is longer than {limit} characters")
    return interface


def _skill_files(plugin_dir: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for skill_dir in sorted((plugin_dir / "skills").glob("*/")):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        errors = skills_ref.validate(skill_dir)
        if errors:
            raise BuildError(f"{skill_dir}: {'; '.join(errors)}")
        for path in sorted(skill_dir.rglob("*")):
            inside = path.relative_to(skill_dir)
            hidden = any(part.startswith(".") for part in inside.parts)
            if path.is_file() and not hidden and not LEFT_OUT & set(inside.parts):
                name = f"skills/{skill_dir.name}/{inside.as_posix()}"
                files[name] = path.read_bytes()
    return files


def _as_json(data: dict) -> bytes:
    return (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


if __name__ == "__main__":
    sys.exit(main())

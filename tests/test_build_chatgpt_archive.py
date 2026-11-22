"""Tests for the ChatGPT archive build."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

import build_chatgpt_archive as build

SKILL = """---
name: need-evidence
description: Writes evidence of local need for a grant application from totals.
license: Apache-2.0
---

# Need evidence
"""
MANIFEST = {
    "name": "uk-open-data",
    "version": "0.1.0",
    "description": "UK open data for charities.",
    "author": {"name": "Kindtech", "url": "https://github.com/KindTechUK"},
    "repository": "https://github.com/KindTechUK/plugins",
    "license": "Apache-2.0",
    "keywords": ["charity"],
}


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A repository with one plugin that holds one skill and its evals."""
    plugin = tmp_path / "plugins" / "uk-open-data"
    skill = plugin / "skills" / "need-evidence"
    _write(plugin / ".claude-plugin" / "plugin.json", json.dumps(MANIFEST))
    _write(skill / "SKILL.md", SKILL)
    _write(skill / "references" / "method.md", "Method.\n")
    _write(skill / "evals" / "a-case" / "prompt.md", "A request.\n")
    _write(skill / ".hidden", "not for the archive\n")
    _write(tmp_path / "LICENSE", "Apache License\n")
    return tmp_path


def test_archive_holds_the_portable_layout_without_evals(repo: Path) -> None:
    archive = build.build_archive(repo, "uk-open-data", repo / "dist")
    assert archive.name == "uk-open-data-chatgpt-0.1.0.zip"
    with zipfile.ZipFile(archive) as built:
        assert built.namelist() == [
            "LICENSE",
            "plugin.json",
            "skills/need-evidence/SKILL.md",
            "skills/need-evidence/references/method.md",
        ]
        manifest = json.loads(built.read("plugin.json"))
    assert manifest == {
        "$schema": build.PLUGIN_SCHEMA,
        "name": "uk-open-data",
        "version": "0.1.0",
        "description": "UK open data for charities.",
        "license": "Apache-2.0",
        "keywords": ["charity"],
        "author": {"name": "Kindtech", "url": "https://github.com/KindTechUK"},
        "repository": "https://github.com/KindTechUK/plugins",
    }


def test_connector_address_adds_one_remote_server(repo: Path) -> None:
    url = "https://example.org/mcp"
    archive = build.build_archive(repo, "uk-open-data", repo / "dist", url)
    with zipfile.ZipFile(archive) as built:
        config = json.loads(built.read("mcp.json"))
    assert config["$schema"] == build.MCP_SCHEMA
    assert list(config["mcpServers"]) == ["kindtech"]
    server = config["mcpServers"]["kindtech"]
    assert server["type"] == "streamable-http"
    assert server["url"] == url
    assert server["extensions"]["com.openai"]["auth"] == {"type": "none"}


def test_connector_address_comes_from_the_plugin_unless_given(repo: Path) -> None:
    server = {"type": "http", "url": "https://example.org/mcp"}
    config = {"mcpServers": {"kindtech": server}}
    _write(repo / "plugins" / "uk-open-data" / ".mcp.json", json.dumps(config))
    from_plugin = build.build_archive(repo, "uk-open-data", repo / "a")
    given = build.build_archive(
        repo, "uk-open-data", repo / "b", "https://staging.example.org/mcp"
    )
    with zipfile.ZipFile(from_plugin) as built:
        assert json.loads(built.read("mcp.json"))["mcpServers"]["kindtech"]["url"] == (
            "https://example.org/mcp"
        )
    with zipfile.ZipFile(given) as built:
        assert json.loads(built.read("mcp.json"))["mcpServers"]["kindtech"]["url"] == (
            "https://staging.example.org/mcp"
        )


@pytest.mark.parametrize(
    "url", ["http://example.org/mcp", "example.org/mcp", "https://me:pw@example.org"]
)
def test_connector_address_must_be_plain_https(repo: Path, url: str) -> None:
    with pytest.raises(build.BuildError, match="plain https"):
        build.build_archive(repo, "uk-open-data", repo / "dist", url)


def test_listing_text_is_added_and_checked_for_length(repo: Path) -> None:
    path = repo / "plugins" / "uk-open-data" / "platforms" / "chatgpt.json"
    _write(path, json.dumps({"interface": {"displayName": "UK open data"}}))
    files = build.collect_files(repo, repo / "plugins" / "uk-open-data")
    manifest = json.loads(files["plugin.json"])
    assert manifest["extensions"]["com.openai"]["interface"] == {
        "displayName": "UK open data"
    }
    _write(path, json.dumps({"interface": {"displayName": "x" * 31}}))
    with pytest.raises(build.BuildError, match="displayName is longer than 30"):
        build.collect_files(repo, repo / "plugins" / "uk-open-data")


def test_same_source_gives_the_same_archive(repo: Path) -> None:
    first = build.build_archive(repo, "uk-open-data", repo / "one").read_bytes()
    second = build.build_archive(repo, "uk-open-data", repo / "two").read_bytes()
    assert first == second


def test_plugin_without_a_skill_is_refused(repo: Path) -> None:
    (
        repo / "plugins" / "uk-open-data" / "skills" / "need-evidence" / "SKILL.md"
    ).unlink()
    with pytest.raises(build.BuildError, match="no skill to package"):
        build.build_archive(repo, "uk-open-data", repo / "dist")


def test_skill_that_breaks_the_spec_is_refused(repo: Path) -> None:
    path = repo / "plugins" / "uk-open-data" / "skills" / "need-evidence" / "SKILL.md"
    path.write_text(SKILL.replace("name: need-evidence", "name: Wrong Name"))
    with pytest.raises(build.BuildError, match="need-evidence"):
        build.build_archive(repo, "uk-open-data", repo / "dist")


def test_main_reports_a_missing_plugin(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert build.main(["nope", "--root", str(repo)]) == 1
    assert "Cannot build" in capsys.readouterr().err


def test_main_lists_what_it_wrote(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    out = repo / "dist"
    assert build.main(["uk-open-data", "--root", str(repo), "--out", str(out)]) == 0
    assert "skills/need-evidence/SKILL.md" in capsys.readouterr().out


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

"""Tests for the skill linter: a good repository passes, each broken one fails."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

import lint_skills

REPO_ROOT = Path(__file__).resolve().parents[1]
TODAY = date(2026, 11, 18)
SKILL = "need-evidence"
GOOD_SKILL = """---
name: need-evidence
description: Writes evidence of local need for a grant application from totals.
license: Apache-2.0
metadata:
  owner: example-owner
  version: "0.1.0"
  maturity: sandbox
  supervision: review
  reviewed: "2026-11-01"
---

# Need evidence

## Before you start

Ask which area the charity works in. See [the method](references/method.md).

## Steps

1. Run the lens.

## Output

One page.

## Gotchas

## Guardrails

GUARDRAILS_GO_HERE

## Sources and freshness

Checked on 1 November 2026.
""".replace("GUARDRAILS_GO_HERE", "\n".join(lint_skills.GUARDRAILS))


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A small repository that passes every rule."""
    _write_json(
        tmp_path / ".claude-plugin" / "marketplace.json",
        {
            "name": "kindtech",
            "plugins": [{"name": "uk-open-data", "source": "./plugins/uk-open-data"}],
        },
    )
    plugin = tmp_path / "plugins" / "uk-open-data"
    _write_json(
        plugin / ".claude-plugin" / "plugin.json",
        {
            "name": "uk-open-data",
            "description": "UK open data for charities.",
            "version": "0.1.0",
            "license": "Apache-2.0",
        },
    )
    skill = plugin / "skills" / SKILL
    _write(skill / "SKILL.md", GOOD_SKILL)
    _write(skill / "references" / "method.md", "How the figures are worked out.\n")
    for case in ("writes-up-result", "refuses-pasted-rows", "unrelated-request"):
        _write(skill / "evals" / case / "prompt.md", "A request.\n")
        _write(skill / "evals" / case / "graders" / "01-check.md", "A check.\n")
    queries = [
        {"query": f"request {n}", "should_trigger": n % 2 == 0} for n in range(16)
    ]
    _write_json(skill / "evals" / "triggers.json", queries)
    _write_json(
        skill / "evals" / "benchmark.json",
        {
            "date": "2026-11-18",
            "model": "a-model",
            "runs": 3,
            "with_skill": 0.9,
            "without_skill": 0.4,
        },
    )
    return tmp_path


def test_good_repository_has_no_problems(repo: Path) -> None:
    assert lint_skills.lint_repo(repo, TODAY) == []


def test_this_repository_has_no_problems() -> None:
    assert lint_skills.lint_repo(REPO_ROOT) == []


def test_template_carries_the_standard_guardrails() -> None:
    template = (REPO_ROOT / "templates" / "SKILL.md").read_text(encoding="utf-8")
    sections = lint_skills._sections(template)
    assert sections["Guardrails"] == list(lint_skills.GUARDRAILS)
    assert set(lint_skills.REQUIRED_SECTIONS) <= set(sections)


def test_main_exits_with_1_and_prints_the_problem(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _edit_skill(repo, "- Give a source for every number.\n", "")
    assert lint_skills.main([str(repo)]) == 1
    assert "Guardrails" in capsys.readouterr().out


def test_main_exits_with_0_for_a_good_repository(repo: Path) -> None:
    assert lint_skills.main([str(repo)]) == 0


@pytest.mark.parametrize(
    ("old", "new", "expected"),
    [
        ("- Give a source for every number.\n", "", "Guardrails section must be"),
        ("Never invent figures", "Try not to invent figures", "Guardrails section"),
        ("## Gotchas\n", "", '"## Gotchas" section'),
        ("license: Apache-2.0", "license: MIT", '"license" must be'),
        ("  owner: example-owner\n", "", 'metadata needs "owner"'),
        ("maturity: sandbox", "maturity: finished", "maturity must be one of"),
        ("supervision: review", "supervision: none", "supervision must be one of"),
        ('reviewed: "2026-11-01"', 'reviewed: "last week"', "YYYY-MM-DD"),
        ('reviewed: "2026-11-01"', 'reviewed: "2027-01-01"', "in the future"),
        ("references/method.md", "references/missing.md", "does not exist"),
        ("references/method.md", "../other/SKILL.md", "outside the skill folder"),
        ("1. Run the lens.", "1. Ask Claude to run the lens.", "names an assistant"),
        ("name: need-evidence", "name: Need Evidence", "Agent Skills spec"),
        ("One page.", "One page.\n" * 500, "lines long"),
        ("One page.", "For example SE13 7AB.", "real full postcode"),
    ],
)
def test_broken_skill_is_reported(
    repo: Path, old: str, new: str, expected: str
) -> None:
    _edit_skill(repo, old, new)
    assert expected in _messages(repo)


def test_invented_postcode_is_allowed(repo: Path) -> None:
    _edit_skill(repo, "One page.", "For example SE13 7VC.")
    assert lint_skills.lint_repo(repo, TODAY) == []


def test_skill_without_skill_md_is_reported(repo: Path) -> None:
    (_skill_dir(repo) / "SKILL.md").unlink()
    assert "has no SKILL.md" in _messages(repo)


def test_plugin_skill_needs_three_eval_cases(repo: Path) -> None:
    case = _skill_dir(repo) / "evals" / "unrelated-request"
    (case / "graders" / "01-check.md").unlink()
    messages = _messages(repo)
    assert "needs at least 3 eval cases, has 2" in messages
    assert "at least one file in graders/" in messages


def test_plugin_skill_needs_trigger_queries(repo: Path) -> None:
    path = _skill_dir(repo) / "evals" / "triggers.json"
    _write_json(path, [{"query": "one request", "should_trigger": True}])
    assert "near misses that should not" in _messages(repo)


def test_plugin_skill_must_beat_the_assistant_alone(repo: Path) -> None:
    path = _skill_dir(repo) / "evals" / "benchmark.json"
    benchmark = json.loads(path.read_text(encoding="utf-8"))
    _write_json(path, {**benchmark, "with_skill": 0.4})
    assert "does not beat the assistant alone" in _messages(repo)


def test_plugin_skill_needs_a_recorded_baseline(repo: Path) -> None:
    (_skill_dir(repo) / "evals" / "benchmark.json").unlink()
    assert "benchmark.json: is missing" in _messages(repo)


def test_sandbox_skill_needs_no_evals(repo: Path) -> None:
    _write(repo / "sandbox" / SKILL / "SKILL.md", GOOD_SKILL)
    _write(repo / "sandbox" / SKILL / "references" / "method.md", "Method.\n")
    assert lint_skills.lint_repo(repo, TODAY) == []


def test_sandbox_skill_cannot_claim_a_higher_maturity(repo: Path) -> None:
    text = GOOD_SKILL.replace("maturity: sandbox", "maturity: tested")
    _write(repo / "sandbox" / SKILL / "SKILL.md", text)
    _write(repo / "sandbox" / SKILL / "references" / "method.md", "Method.\n")
    assert 'must have the maturity "sandbox"' in _messages(repo)


def test_plugin_with_a_skill_must_be_listed(repo: Path) -> None:
    path = repo / ".claude-plugin" / "marketplace.json"
    _write_json(path, {"name": "kindtech", "plugins": []})
    assert "is not listed in" in _messages(repo)


def test_listed_plugin_must_exist_and_hold_a_skill(repo: Path) -> None:
    path = repo / ".claude-plugin" / "marketplace.json"
    listed = [
        {"name": "uk-open-data", "source": "./plugins/uk-open-data"},
        {"name": "research", "source": "./plugins/research"},
        {"name": "uk-nonprofit", "source": "./somewhere-else"},
    ]
    _write_json(path, {"name": "kindtech", "plugins": listed})
    _write_json(
        repo / "plugins" / "uk-nonprofit" / ".claude-plugin" / "plugin.json",
        {"name": "wrong-name", "description": "Charity practice.", "version": "0.1.0"},
    )
    messages = _messages(repo)
    assert 'lists "research", which has no folder' in messages
    assert 'must have the source "./plugins/uk-nonprofit"' in messages
    assert "is listed in the marketplace but has no skill" in messages
    assert '"name" must be "uk-nonprofit"' in messages
    assert '"license" must be "Apache-2.0"' in messages


def test_manifest_that_is_not_json_is_reported(repo: Path) -> None:
    _write(repo / ".claude-plugin" / "marketplace.json", "{not json")
    assert "is not valid JSON" in _messages(repo)


def _messages(repo: Path) -> str:
    problems = lint_skills.lint_repo(repo, TODAY)
    return "\n".join(f"{p.path}: {p.message}" for p in problems)


def _skill_dir(repo: Path) -> Path:
    return repo / "plugins" / "uk-open-data" / "skills" / SKILL


def _edit_skill(repo: Path, old: str, new: str) -> None:
    path = _skill_dir(repo) / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new), encoding="utf-8")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, data: object) -> None:
    _write(path, json.dumps(data, indent=2))

"""Check every skill and manifest in this repository against the house rules.

Run from the repository root::

    uv run python scripts/lint_skills.py

The rules are described in AGENTS.md. The script prints one line per problem and
exits with status 1 when it finds any.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import skills_ref
from skills_ref.errors import ParseError
from skills_ref.parser import parse_frontmatter

LICENCE = "Apache-2.0"
MAX_SKILL_LINES = 500
MIN_OUTPUT_CASES = 3
MIN_TRIGGER_QUERIES = 8
MATURITY_LEVELS = ("sandbox", "tested", "maintained")
SUPERVISION_LEVELS = ("unsupervised", "review", "expert-required")
HOUSE_FIELDS = ("owner", "version", "maturity", "supervision", "reviewed")
REQUIRED_SECTIONS = (
    "Before you start",
    "Steps",
    "Output",
    "Gotchas",
    "Guardrails",
    "Sources and freshness",
)
GUARDRAILS = (
    "- Never invent figures, beneficiaries, quotes or funder names.",
    "- Give a source for every number.",
    "- Work from totals. Never ask for, repeat or work from a record about one "
    "person, such as a name, an address, a full postcode or a case note.",
    "- Say what a person must check before the output is used.",
)
# Names the eval runner keeps for itself inside an evals folder.
RESERVED_EVAL_NAMES = {"results", "mocks", "files", "node_modules"}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".csv", ".txt", ".sh", ".py"}

ASSISTANT_NAMES = re.compile(
    r"\b(claude|anthropic|chatgpt|openai|codex|gemini|copilot)\b", re.IGNORECASE
)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
POSTCODE = re.compile(r"\b[A-Z]{1,2}\d[A-Z\d]? ?\d([A-Z]{2})\b")
# No real postcode ends with any of these letters, so an example that uses one
# cannot be somebody's home.
NEVER_IN_A_POSTCODE = set("CIKMOV")


@dataclass(frozen=True)
class Problem:
    """One broken rule, and the file or folder it was found in."""

    path: Path
    message: str


def main(argv: list[str] | None = None) -> int:
    """Lint the repository and return the exit status."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "root", nargs="?", default=".", type=Path, help="the repository root"
    )
    args = parser.parse_args(argv)
    problems = lint_repo(args.root)
    for problem in problems:
        print(f"{problem.path}: {problem.message}")
    if problems:
        print(f"\n{len(problems)} problem(s) found.")
        return 1
    print(f"{len(find_skills(args.root))} skill(s) checked, no problems found.")
    return 0


def lint_repo(root: Path, today: date | None = None) -> list[Problem]:
    """Return every problem in the manifests and skills under ``root``."""
    problems = lint_manifests(root)
    for skill_dir in find_skills(root):
        problems += lint_skill(skill_dir, root, today or date.today())
    return [Problem(_relative(p.path, root), p.message) for p in problems]


def find_skills(root: Path) -> list[Path]:
    """Return every skill folder: in a plugin, or in the sandbox."""
    folders = [*root.glob("plugins/*/skills/*"), *root.glob("sandbox/*")]
    return sorted(f for f in folders if f.is_dir())


def lint_manifests(root: Path) -> list[Problem]:
    """Check the marketplace manifest and each plugin manifest agree."""
    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    marketplace, problems = _load_json(marketplace_path)
    listed: dict[str, str] = {}
    if isinstance(marketplace, dict):
        if not marketplace.get("name"):
            problems.append(Problem(marketplace_path, 'needs a "name"'))
        for entry in marketplace.get("plugins", []):
            listed[str(entry.get("name"))] = str(entry.get("source"))
    for name, source in listed.items():
        if source != f"./plugins/{name}":
            message = f'plugin "{name}" must have the source "./plugins/{name}"'
            problems.append(Problem(marketplace_path, message))
    plugin_dirs = sorted(d for d in root.glob("plugins/*") if d.is_dir())
    for name in sorted(set(listed) - {d.name for d in plugin_dirs}):
        message = f'lists "{name}", which has no folder under plugins/'
        problems.append(Problem(marketplace_path, message))
    for plugin_dir in plugin_dirs:
        problems += _lint_plugin(plugin_dir, plugin_dir.name in listed)
    return problems


def lint_skill(skill_dir: Path, root: Path, today: date) -> list[Problem]:
    """Check one skill folder against the open spec and the house rules."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [Problem(skill_dir, "has no SKILL.md")]
    spec_errors = skills_ref.validate(skill_dir)
    if spec_errors:
        return [Problem(skill_md, f"Agent Skills spec: {e}") for e in spec_errors]
    text = skill_md.read_text(encoding="utf-8")
    try:
        frontmatter, body = parse_frontmatter(text)
    except ParseError as error:
        return [Problem(skill_md, str(error))]
    in_sandbox = skill_dir.parent == root / "sandbox"
    messages = _check_frontmatter(frontmatter, in_sandbox, today)
    messages += _check_body(text, body, skill_dir)
    problems = [Problem(skill_md, m) for m in messages]
    problems += _check_example_postcodes(skill_dir)
    if not in_sandbox:
        problems += _check_evals(skill_dir)
    return problems


def _lint_plugin(plugin_dir: Path, is_listed: bool) -> list[Problem]:
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    manifest, problems = _load_json(manifest_path)
    if isinstance(manifest, dict):
        if manifest.get("name") != plugin_dir.name:
            message = f'"name" must be "{plugin_dir.name}", the folder name'
            problems.append(Problem(manifest_path, message))
        for field in ("description", "version"):
            if not manifest.get(field):
                problems.append(Problem(manifest_path, f'needs a "{field}"'))
        if manifest.get("license") != LICENCE:
            problems.append(Problem(manifest_path, f'"license" must be "{LICENCE}"'))
    has_skills = any((plugin_dir / "skills").glob("*/SKILL.md"))
    if has_skills and not is_listed:
        message = "has a skill but is not listed in .claude-plugin/marketplace.json"
        problems.append(Problem(plugin_dir, message))
    if is_listed and not has_skills:
        message = "is listed in the marketplace but has no skill to install"
        problems.append(Problem(plugin_dir, message))
    return problems


def _check_frontmatter(frontmatter: dict, in_sandbox: bool, today: date) -> list[str]:
    messages = []
    name = str(frontmatter.get("name", ""))
    if ASSISTANT_NAMES.search(name.replace("-", " ")):
        messages.append("the name must not contain the name of an assistant")
    if frontmatter.get("license") != LICENCE:
        messages.append(f'"license" must be "{LICENCE}"')
    house = frontmatter.get("metadata")
    if not isinstance(house, dict):
        return [*messages, f'needs a "metadata" map with {", ".join(HOUSE_FIELDS)}']
    for field in HOUSE_FIELDS:
        if not house.get(field):
            messages.append(f'metadata needs "{field}"')
    maturity = house.get("maturity")
    if maturity and maturity not in MATURITY_LEVELS:
        messages.append(f"maturity must be one of: {', '.join(MATURITY_LEVELS)}")
    if in_sandbox and maturity in MATURITY_LEVELS and maturity != "sandbox":
        messages.append('a skill in sandbox/ must have the maturity "sandbox"')
    supervision = house.get("supervision")
    if supervision and supervision not in SUPERVISION_LEVELS:
        levels = ", ".join(SUPERVISION_LEVELS)
        messages.append(f"supervision must be one of: {levels}")
    if house.get("reviewed"):
        messages += _check_review_date(house["reviewed"], today)
    return messages


def _check_review_date(value: str, today: date) -> list[str]:
    try:
        reviewed = date.fromisoformat(value)
    except ValueError:
        return ['"reviewed" must be a date written as YYYY-MM-DD']
    if reviewed > today:
        return ['"reviewed" is in the future']
    return []


def _check_body(text: str, body: str, skill_dir: Path) -> list[str]:
    messages = []
    line_count = len(text.splitlines())
    if line_count > MAX_SKILL_LINES:
        messages.append(
            f"is {line_count} lines long; keep it to {MAX_SKILL_LINES} and move "
            "detail into references/"
        )
    sections = _sections(body)
    for title in REQUIRED_SECTIONS:
        if title not in sections:
            messages.append(f'needs a "## {title}" section')
    if "Guardrails" in sections and sections["Guardrails"] != list(GUARDRAILS):
        messages.append(
            "the Guardrails section must be the standard block, word for word "
            "(copy it from templates/SKILL.md)"
        )
    named = sorted({m.group(0).lower() for m in ASSISTANT_NAMES.finditer(text)})
    if named:
        messages.append(
            f"names an assistant ({', '.join(named)}); write for any assistant"
        )
    for target in MARKDOWN_LINK.findall(body):
        messages += _check_link(target, skill_dir)
    return messages


def _sections(body: str) -> dict[str, list[str]]:
    """Map each ``## `` heading to its non-empty lines."""
    sections: dict[str, list[str]] = {}
    current: list[str] | None = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = sections.setdefault(line[3:].strip(), [])
        elif current is not None and line.strip():
            current.append(line.strip())
    return sections


def _check_link(target: str, skill_dir: Path) -> list[str]:
    if re.match(r"^([a-z]+:|#)", target):
        return []
    linked = (skill_dir / target.split("#")[0]).resolve()
    if not linked.is_relative_to(skill_dir.resolve()):
        return [f'the link "{target}" points outside the skill folder']
    if not linked.exists():
        return [f'the link "{target}" points to a file that does not exist']
    return []


def _check_example_postcodes(skill_dir: Path) -> list[Problem]:
    problems = []
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(
            not NEVER_IN_A_POSTCODE & set(m.group(1)) for m in POSTCODE.finditer(text)
        ):
            problems.append(
                Problem(
                    path,
                    "holds what could be a real full postcode; end an invented one "
                    "with a letter no real postcode uses (C, I, K, M, O or V)",
                )
            )
    return problems


def _check_evals(skill_dir: Path) -> list[Problem]:
    evals_dir = skill_dir / "evals"
    if not evals_dir.is_dir():
        message = "a skill in a plugin needs an evals/ folder; drafts go in sandbox/"
        return [Problem(skill_dir, message)]
    problems = []
    cases = [
        d
        for d in sorted(evals_dir.iterdir())
        if d.is_dir() and d.name not in RESERVED_EVAL_NAMES
    ]
    complete = [
        c for c in cases if (c / "prompt.md").is_file() and any(c.glob("graders/*.md"))
    ]
    for case in sorted(set(cases) - set(complete)):
        message = "an eval case needs a prompt.md and at least one file in graders/"
        problems.append(Problem(case, message))
    if len(complete) < MIN_OUTPUT_CASES:
        message = f"needs at least {MIN_OUTPUT_CASES} eval cases, has {len(complete)}"
        problems.append(Problem(evals_dir, message))
    problems += _check_trigger_queries(evals_dir / "triggers.json")
    problems += _check_benchmark(evals_dir / "benchmark.json")
    return problems


def _check_trigger_queries(path: Path) -> list[Problem]:
    queries, problems = _load_json(path)
    if problems:
        return problems
    well_formed = isinstance(queries, list) and all(
        isinstance(q, dict)
        and isinstance(q.get("query"), str)
        and isinstance(q.get("should_trigger"), bool)
        for q in queries
    )
    if not well_formed:
        message = 'must be a list of {"query": "...", "should_trigger": true or false}'
        return [Problem(path, message)]
    should = sum(q["should_trigger"] for q in queries)
    if min(should, len(queries) - should) < MIN_TRIGGER_QUERIES:
        message = (
            f"needs at least {MIN_TRIGGER_QUERIES} requests that should load the "
            f"skill and {MIN_TRIGGER_QUERIES} near misses that should not"
        )
        return [Problem(path, message)]
    return []


def _check_benchmark(path: Path) -> list[Problem]:
    benchmark, problems = _load_json(path)
    if problems:
        return problems
    if not isinstance(benchmark, dict):
        return [Problem(path, "must be a JSON object")]
    messages = [
        f'needs "{field}"'
        for field in ("date", "model", "runs")
        if not benchmark.get(field)
    ]
    scores = [benchmark.get("with_skill"), benchmark.get("without_skill")]
    if not all(isinstance(s, int | float) and 0 <= s <= 1 for s in scores):
        messages.append('"with_skill" and "without_skill" must be scores from 0 to 1')
    elif scores[0] <= scores[1]:
        messages.append(
            "the skill does not beat the assistant alone "
            f"({scores[0]} with, {scores[1]} without); improve it or retire it"
        )
    return [Problem(path, m) for m in messages]


def _load_json(path: Path) -> tuple[object, list[Problem]]:
    if not path.is_file():
        return None, [Problem(path, "is missing")]
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as error:
        return None, [Problem(path, f"is not valid JSON ({error})")]


def _relative(path: Path, root: Path) -> Path:
    return path.relative_to(root) if path.is_relative_to(root) else path


if __name__ == "__main__":
    sys.exit(main())

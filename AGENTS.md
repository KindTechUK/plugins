# Kindtech plugins: guide for contributors

For anyone, person or agent, changing this repository.

The shared [contributing guide](https://github.com/KindTechUK/.github/blob/main/CONTRIBUTING.md) and [AI policy](https://github.com/KindTechUK/.github/blob/main/AI_POLICY.md) apply here. This file adds what is specific to this repository.

## What this repository is

A marketplace of plugins for AI assistants, written for UK charities. A plugin is a folder of skills, and a skill is a folder with a `SKILL.md` that tells an assistant how to do one job well. Three rules shape everything here:

- **Every skill proves it helps.** A skill ships with tests, and the tests are run with the skill and without it. A skill that does not beat the assistant alone does not belong in a plugin.
- **The logic lives in code, not in the skill.** Figures come from the `uk-open-data` command or the Kindtech connector. A skill says when to call them and how to present what comes back.
- **The model sees totals, never rows.** No skill asks for, repeats or works from a record about one person.

## Layout

```
.claude-plugin/marketplace.json   the catalogue: lists each plugin that has a skill
plugins/
  uk-nonprofit/                   UK charity practice, skills only
  uk-open-data/                   skills that use UK open data
  research/                       skills that call a research command line tool
    .claude-plugin/plugin.json    name, description, version
    skills/<skill-name>/
      SKILL.md
      references/                 dated facts with sources, one level deep
      scripts/                    optional
      evals/                      the tests (see "Tests for a skill")
sandbox/<skill-name>/             drafts, not in any plugin
templates/SKILL.md                start a new skill from this
scripts/lint_skills.py            the house rules, as code
tests/                            tests for the scripts
```

## Set up and checks

Use `uv` only, never `pip`.

```bash
uv sync
uv run ruff format --check .
uv run ruff check .
uv run pytest
uv run python scripts/lint_skills.py
```

Run all four checks before you push. CI runs the same ones on every pull request, and none of them costs anything or calls a model.

Python rules are the same as in the other Kindtech repositories: type hints, docstrings on public functions, lines of 88 characters at most, and a test for every new behaviour.

## Rules for every skill

The linter enforces these. Start from `templates/SKILL.md`.

- Follow the open [Agent Skills specification](https://agentskills.io) and nothing beyond it, so the same folder works in any assistant. The allowed frontmatter fields are `name`, `description`, `license`, `compatibility`, `allowed-tools` and `metadata`.
- `name` matches the folder name: lower case letters, numbers and hyphens, 64 characters at most.
- `description` is in the third person, says what the skill produces and when to use it in the words a charity worker would type, and is 1,024 characters at most.
- `license` is `Apache-2.0`.
- House fields go in `metadata`: `owner` (a GitHub handle), `version`, `maturity`, `supervision` and `reviewed` (the date a person last checked the skill, as YYYY-MM-DD).
- `supervision` says how much checking the output needs: `unsupervised`, `review` (a person reads it before it is used) or `expert-required` (a qualified person signs it off).
- `SKILL.md` has these sections: Before you start, Steps, Output, Gotchas, Guardrails, Sources and freshness. It is 500 lines at most. Longer detail goes in `references/`, linked from `SKILL.md`.
- The Guardrails section is the standard block, word for word.
- Write for any assistant. Do not name one in a skill.
- Facts that change, such as thresholds, deadlines and rates, come from a tool or sit in a dated file under `references/`. They never sit in `SKILL.md` prose.
- Gotchas starts empty and grows from real failures. Each one is a specific fact a person can check.
- If a skill needs another skill, say so in its body. Marketplaces do not install one skill for another.
- An invented postcode in an example or a test ends with a letter no real postcode uses (C, I, K, M, O or V), for example `SE13 7VC`. It then cannot be anybody's home.

## Maturity labels

| Label | What it means | Where it lives |
| --- | --- | --- |
| `sandbox` | Valid frontmatter. Nothing else is promised. | `sandbox/`, or a plugin once it has tests that beat the assistant alone |
| `tested` | Tests that beat the assistant alone, a named owner, and one charity has tried it on a real task | a plugin |
| `maintained` | Tests run again on each new model, reviewed in the last six months, Gotchas in use | a plugin |

A skill leaves the repository when the assistant passes its tests without it, or when its owner steps away and nobody takes it on.

## Tests for a skill

Any skill inside `plugins/` needs an `evals/` folder with three things.

1. **At least three cases**, one folder each, in the layout `claude plugin eval` reads:

   ```
   evals/<case-name>/
     prompt.md      run settings, then the request as a charity worker would type it
     case.yaml      the name and a description of a good result
     graders/       one checkable statement per file
   ```

   Build the cases from what goes wrong when the assistant does the task without the skill. Include at least one request the skill should leave alone.

2. **`evals/triggers.json`**: at least eight requests that should load the skill and eight near misses that should not, as a list of `{"query": "...", "should_trigger": true}`.

3. **`evals/benchmark.json`**: the last recorded run, with `date`, `model`, `runs`, `with_skill` and `without_skill` (scores from 0 to 1). The linter fails if the skill does not beat the assistant alone.

Running the cases costs money, because each one is a real model run, with the skill and without it. From the skill's folder:

```bash
claude plugin eval . --scaffold --runs 3 --judge-model sonnet --no-publish
```

`--scaffold` lets a case copy its input files into place with the script named in its `case.yaml`, so read that script before you run someone else's case. Add `--max-cost-usd 0` to check that the cases load without running anything, and set a real ceiling on every paid run. Add `--case <name>` to run one case again after a change that touches only that case.

Give each case that should load the skill a `tool_used` grader for the `Skill` tool with `arm: with-only`. It is not scored. It shows whether the skill loaded at all, which is the first thing to check when a case scores no better with the skill than without it.

Results are written to `evals/results/`, which is not committed. Copy the scores into `benchmark.json` by hand. Keys beyond the five the linter reads are welcome: the judge model, the cost, the score for each case and the runs on other models.

## Adding a skill

1. Open an issue that says what the skill is for and who would use it.
2. Do the task three times with no skill and write down what went wrong.
3. Turn those failures into cases and record the scores without the skill.
4. Write only as much skill as it takes to pass the cases. Start it in `sandbox/` if it is not ready.
5. Run the cases with the skill, and keep going until it beats the assistant alone.
6. Move the folder into the right plugin, add the plugin to `.claude-plugin/marketplace.json` if it is not listed yet, and open a pull request.

## Commits and pull requests

- Conventional commit subjects: `feat:`, `fix:`, `docs:`, `chore:`, `ci:`. One change per pull request.
- Do not add `Co-authored-by` or other tool trailers to commits. Say in the pull request description which AI tools did a meaningful part of the work, or write "None".
- Agents: list only the checks you ran, and say what you could not run. Do not add a sign-off for a person.
- If you changed a skill, say whether you ran its cases again, and update `benchmark.json` if you did.

## Content

- No personal data about real people in skills, tests, examples or docs. Use invented people.
- No credentials, tokens or keys anywhere, including in test files.
- Every figure in an example has a source, or is plainly marked as invented.

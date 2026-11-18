# Kindtech plugins

Skills that bring UK charity know-how and UK open data into AI assistants, each one tested against the assistant alone.

Most skill libraries for charities are written for the United States and none publishes test results. This one is written for UK charities, and a skill only ships once its tests show that it helps.

## What is here

| Plugin | What it is for | Needs |
| --- | --- | --- |
| [`uk-open-data`](plugins/uk-open-data) | Answering a charity's questions with UK open data, such as evidence of local need for a grant application | The `uk-open-data` command, or the Kindtech connector |
| [`uk-nonprofit`](plugins/uk-nonprofit) | UK charity practice: regulation, fundraising and reporting | Nothing |
| [`research`](plugins/research) | Research that keeps a source for every finding | A terminal |

No skill has been published yet. The first one, local-need evidence for a grant application, is on its way, and the install steps will be added here with it.

## How a skill earns its place

Every skill carries a label that says how far it can be trusted.

| Label | What it means |
| --- | --- |
| `sandbox` | A draft. Nothing is promised. |
| `tested` | It has tests that beat the assistant alone, a named owner, and a charity has tried it on a real task. |
| `maintained` | Its tests are run again on each new model, and a person has reviewed it in the last six months. |

Each skill also says how much checking its output needs before you use it, and ends by telling you what a person must check. A skill is retired when the assistant passes its tests without it.

## What the skills will not do

- Invent a figure, a beneficiary, a quote or a funder.
- Give a number without its source.
- Ask for, repeat or work from a record about one person. Figures are worked out in code, and the assistant sees totals only.

## Contributing

You do not need to write code to help. If you work at a charity, the most useful thing is to open an issue describing a task you wish your assistant did better.

To write or change a skill, read [AGENTS.md](AGENTS.md), which holds the rules and the checks, and the shared [contributing guide](https://github.com/KindTechUK/.github/blob/main/CONTRIBUTING.md).

## Licence

[Apache-2.0](LICENSE).

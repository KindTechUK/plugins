# uk-open-data

Answer a charity's questions with UK open data. The figures are worked out in code from
official sources by the [uk-open-data package](https://github.com/KindTechUK/uk-open-data),
the engine behind Kindtech Evidence. The assistant is given totals with their sources and
never sees a record about one person.

The skills here work in two ways. Where the assistant can run commands, they use the
`uk-open-data` command on your own computer. In a chat app, they use the Kindtech
connector, which takes totals only.

What you can get today, 20 November 2026: the skills, from this repository. The command
is not released yet and the connector is not open to the public yet, so for now a skill
words a result you already hold, tells you which totals to bring, and gives no figure of
its own. This paragraph changes when they open.

## Install

In Claude Code:

```
/plugin marketplace add KindTechUK/plugins
/plugin install uk-open-data@kindtech
```

In another assistant that reads skills, copy a folder from `skills/` into its skills folder.

## Skills

| Skill | What it does | Maturity | Checking it needs |
| --- | --- | --- | --- |
| [`local-need-evidence`](skills/local-need-evidence) | Writes evidence of local need and of who you reach, for a bid or a board paper, from five Kindtech Evidence analyses: reach against deprivation, need against reach, who you are missing, where provision is thin, and distance to your nearest site. Gives a quick answer or shows the steps. England and Wales, depending on the analysis. | sandbox | A person reads it before it is used |

To propose a skill, read the [guide at the top of the repository](../../AGENTS.md).

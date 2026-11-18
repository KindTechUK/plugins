# uk-open-data

Answer a charity's questions with UK open data. The figures are worked out in code by
the [Kindtech open data package](https://github.com/KindTechUK/kindtech) from official
sources. The assistant is given totals with their sources and never sees a record about
one person.

The skills here work in two ways. Where the assistant can run commands, they use the
`uk-open-data` command on your own computer. In a chat app, they use the Kindtech
connector when you have added it.

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
| [`local-need-evidence`](skills/local-need-evidence) | Writes the evidence-of-need part of a grant application from official deprivation statistics, and shows whether you reach people in the most deprived neighbourhoods. England only. | sandbox | A person reads it before it is used |

To propose a skill, read the [guide at the top of the repository](../../AGENTS.md).

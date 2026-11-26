# uk-open-data

Answer a charity's questions with UK open data. The figures are worked out in code from
official sources by the [uk-open-data package](https://github.com/KindTechUK/uk-open-data),
the engine behind Kindtech Evidence. The assistant is given totals with their sources and
never sees a record about one person.

The skills here work in two ways. Where the assistant can run commands, they use the
`uk-open-data` command on your own computer. In a chat app, they use the Kindtech
connector, which takes totals only.

Installing the plugin in Claude Code also adds the Kindtech connector, at
`https://app.kindte.ch/mcp`, so a skill can work out figures from totals in the chat. In
another assistant, add that address as a connector yourself.

## Privacy

What leaves your computer depends on how a skill gets its figures.

- **The Kindtech connector**, at `https://app.kindte.ch/mcp`, hosted on Azure in the UK
  South region. It is given totals only: counts or volumes for each area or group. It refuses
  a row about one person or one site, a full postcode and a street address. Every tool only
  reads: nothing you send is changed or published. Its log records one line for each answer
  it gives: which analysis ran, what kind of totals it was given, and that the answer was
  given in a chat.
- **Public services it asks.** To place a postcode district, the connector may ask
  postcodes.io when it holds no postcode table of its own. To draw a map, it fetches public
  area outlines from the ONS by area code. Each result says what was sent, under
  `privacy.sent_to_third_parties`.
- **The `uk-open-data` command** runs on your own computer. Postcodes in your file are sent
  to postcodes.io, and nothing else from the file, unless a postcode table is installed
  there. Before the first run, the skill tells you which will happen and lets you choose.

The assistant you use sees the totals you give it and what comes back. Its own privacy
terms apply to that.

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

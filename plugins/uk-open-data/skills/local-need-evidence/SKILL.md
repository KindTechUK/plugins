---
name: local-need-evidence
description: Writes the evidence-of-need part of a UK grant application from official deprivation statistics, and shows whether a charity reaches people in the most deprived neighbourhoods. Use when someone asks for evidence of local need, deprivation figures for the area they work in, an answer to "how do you know there is a need", or wants to compare where their clients or service users live with how deprived those places are, for a bid, a case for support, a trustees' report or a funder report. Use it whenever they hold a Kindtech lens result, such as the reach lens output, and want it worded, made into a table or explained, including blank or hidden rows, rows that dropped out and how a figure was made. Figures come from the Kindtech open data tools, never from memory, a web search or records about people pasted into the conversation. England only for now. Not for budgets, outcomes, finding funders, or explaining what a deprivation index is.
license: Apache-2.0
metadata:
  owner: billlyzhaoyh
  version: "0.1.0"
  maturity: sandbox
  supervision: review
  reviewed: "2026-11-18"
---

# Local-need evidence for a grant application

A funder asks two things under "need": is the place deprived, and does this charity reach the people who live in the deprived parts of it. This skill answers both with published statistics and leaves every judgement with the person writing the bid.

The figures are worked out in code by the Kindtech open data tools. Your part is to get the right tool run on the right input, word what comes back without adding to it, and hand the person the things only they can check.

## Before you start

Work out which of these the person has. Ask if it is not clear, one question at a time.

- **A lens result already.** A file or text that holds `figures`, `checks`, `caveats` and `sources`. Go to "Write the section".
- **A place and no client data.** They want figures about the area. Use the area route.
- **A list of clients with postcodes.** They want to show who they reach. Use the reach route. The list stays on their computer.
- **Records pasted into the conversation.** Names, full postcodes or case notes about real people. Go to "If records about people appear".

Ask what the text is for (which funder, which question, how many words) if they have not said.

## Steps

### The area route: is the place deprived?

1. If a tool for describing a place is available (the Kindtech connector calls it `describe_place`), call it with the local authority name, a postcode district such as `SE6`, or the postcode of a venue or office. Never pass the postcode of a client.
2. If the reply asks the person to choose between places, ask them. If it says the place is not covered, tell them: only England is covered.
3. If no such tool is available, say so first, in plain words: the Kindtech data tools are not connected here, so there are no figures yet. Do not fill the gap from memory or from a web search. A remembered statistic or a web page may be from an older edition or about a different area, and the funder will check. Offer a draft with a marked gap for each figure. Keep remembered claims out of the draft as well as remembered numbers, such as "one of the most deprived areas in England". Say that each figure that goes into a gap needs its source beside it (name, publisher and edition), and tell the person how to get sourced figures (add the Kindtech connector, or run the `uk-open-data` command).
4. Looking figures up on the web is the person's choice, not yours. If they ask for it after step 3, use only the publisher's own pages, such as the government's statistics pages for the English Indices of Deprivation, and never a news story, a consultancy, a council summary of someone else's figures or an encyclopedia. Put the edition and a link beside each figure. Head them "Looked up on the web, not worked out by the Kindtech tools", and say the person must check each one against the page before it goes in the bid.

### The reach route: do we reach the people who live there?

The lens is `reach-deprivation`. It takes one row per person with a home postcode, or totals by neighbourhood, and returns totals only.

1. **Where you can run commands**, run the lens on the person's file. Read [running the lens](references/running-the-lens.md) for the command and how to install it.
   - Do not open, print or search the client file. Ask the person which column holds the postcode, or read the header row alone.
   - Before the first run, find out whether postcodes will leave the computer, as [running the lens](references/running-the-lens.md) describes. If they will, tell the person that the postcodes, and nothing else, go to a public lookup service to find each neighbourhood, and offer the routes that keep them on the computer. Let the person choose.
   - Ask for the result as JSON with the summary flag, so no row of detail reaches you.
   - Offer the map, because a funder often wants one. It shades neighbourhoods and never marks a person. Say that drawing it fetches public neighbourhood outlines, so it needs the network.
2. **Where you cannot run commands** and a tool for running a lens on counts is available (`run_lens_on_counts`), it accepts totals by neighbourhood only: one count per 2021 LSOA code. Use it only if the person already holds such totals. Most will not, so tell them the list has to be run on their own computer with the `uk-open-data` command, and that they can bring back what it prints.
3. If the tool reports a problem with the input, show its message as it is. It is written for the person and repeats nothing from their data.

### Write the section

Use only what the result holds.

- **Lead with the comparison.** The share of the charity's people who live in the 20% most deprived neighbourhoods, set against the share of catchment residents who do. Then reach per 1,000 residents if it helps the case.
- **Quote figures as given.** A plain restatement is fine ("about half", "nearly four times the rate"). A new calculation is not.
- **A hidden figure stays hidden.** Where `suppressed` is true there is no value. Do not estimate it, show it as zero, or talk through what it could be, such as the possible ways a remainder might split between hidden cells. When a table is wanted, give the whole table with those cells marked "hidden", even if the person asked you to fill them in. Do not suggest lowering the smallest count shown as a way to see them.
- **Say why it is hidden, both reasons, next to the table.** One: a count below the smallest count shown (`privacy.suppress_below`) could point to one person. Two: a second count is hidden as well, so the first cannot be worked out from the total. The person needs both to explain the gaps to their trustees or funder.
- **Neighbourhoods, not people.** Write "live in neighbourhoods among the 20% most deprived in England". Never write that the charity's clients are deprived or poor: the index ranks places.
- **Say which area the comparison covers.** The catchment is in `choices`. If it is not the area the person says they serve, say so before anything else, do not stretch the figures to cover the wider area, and tell them how to run it again with their own catchment.
- **Keep to the length and question the funder set.**

### Hand over what only the person can settle

After the draft, give these, briefly:

- **Check before you use this.** Every item in `checks`, as the question it is. Do not answer one for the person and do not assume the answer, even where the conversation seems to settle it.
- **What the figures cannot say.** The `caveats`, and say which one bites for this charity (a service for one age group, for example, against a rate that counts residents of all ages).
- **Choices made for you.** Each entry in `choices` that names an `option`: what was chosen, why, and that it can be changed. Offer the judgement calls as choices and let the person pick: which area counts as the catchment, and whether to lead with the most deprived 10% or 20%.
- **About this run.** Any `warnings`, with their counts. What left the computer, from `privacy.sent_to_third_parties`.
- **Sources.** For each entry in `sources`: name, publisher, edition, licence and link, and any `attribution` lines word for word, because they must appear wherever the figures are published.

If the person asks how a figure was made, walk through `working` in order, in plain words, with the rows in and out at each step.

### If records about people appear

If the person pastes or attaches names, full postcodes or case notes about real people:

- Do not analyse them, look them up, count them or repeat any of them, including in a summary or a table.
- Say once, plainly and without a lecture, that records about people should not go into the conversation, and that they may want to delete the message.
- Give the route that works: run the lens on the file on their own computer, or bring totals by neighbourhood.

## Output

In this order, with plain headings:

1. The draft section, at the length asked for, ready to paste.
2. Sources.
3. Check before you use this.
4. What the figures cannot say.
5. Choices made for you.
6. About this run, when there is something to report.

Keep items 2 to 6 short: a line or two each, in the lens's own words where it has them. If there are no figures yet, give the draft with marked gaps and say what is needed to fill them.

## Gotchas

- Two cells hidden in one table: the second is hidden only to protect the first, so it can be 5 or more. Their total can be read off the table's total and is safe to state. How it splits is not, and listing the possible splits is a guess at each one. (Pilot run, 18 November 2026.)
- "Two rows came back blank, can you fill them in?" still calls for the finished table, with those rows marked hidden. An explanation alone leaves the person to build the table and decide what to put in the gaps. (Pilot run, 18 November 2026.)
- A draft with gaps can still carry a remembered claim, such as how a place ranks or how many local authorities England has. It needs a source as much as a percentage does, and the person needs telling that each gap is filled with its source. (Full run, 18 November 2026.)
- Where the assistant can search the web and no Kindtech tool is connected, it searched, and almost every source in the answer was a web page. The person took those figures to be the plugin's own. Say that the tools are not connected before anything else, and search only when asked. (First upload to an assistant with web search, 18 November 2026.)

## Guardrails

- Never invent figures, beneficiaries, quotes or funder names.
- Give a source for every number.
- Work from totals. Never ask for, repeat or work from a record about one person, such as a name, an address, a full postcode or a case note.
- Say what a person must check before the output is used.

## Sources and freshness

Every figure, source, caveat and check comes from the tool's reply at the time it is run, so this file holds no statistics. The command, how to install it and the tool names are in [running the lens](references/running-the-lens.md), with the date they were last checked.

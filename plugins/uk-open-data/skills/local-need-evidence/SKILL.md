---
name: local-need-evidence
description: Writes evidence of local need, and of who a charity reaches, from official UK statistics, for a bid, a case for support, a board or trustees' paper or a funder report. Use when a charity wants need or deprivation figures for the area it serves; asks whether it reaches the most deprived neighbourhoods, which communities it reaches less than their share, where need is high and its reach or provision thin, or how far people live from its nearest site; or holds a Kindtech Evidence result to word, put in a table or explain, blank or hidden rows included. Not for budgets, outcomes, finding funders, staff or volunteer rotas, or explaining what a deprivation index is.
license: Apache-2.0
metadata:
  owner: billlyzhaoyh
  version: "0.2.0"
  maturity: sandbox
  supervision: review
  reviewed: "2026-11-18"
---

# Evidence of local need and reach

Funders, boards and trustees ask a charity about need and reach that its own records cannot answer alone. Five Kindtech Evidence analyses answer with published statistics, worked out in code. Your part: get the right analysis run through the right door, word what comes back without adding to it, and hand the person every judgement that is theirs to make.

## Before you start

Work out these, asking one question at a time where one is not clear.

**What the person holds.**

- **A result already**: a file or text with `answer`, `figures`, `checks`, `caveats` and `sources`. Go to "Write the section".
- **A place and no data of their own**: the area route.
- **Totals**, such as clients for each council, people for each ethnic group or sessions for each council: "Run an analysis".
- **A file on their computer** with one row per person or per site: "Run an analysis". The file stays where it is.
- **Records about people in the conversation**, or an offer to paste them: "If records about people appear".

**Which analysis answers the question.** [The five analyses](references/analyses.md) maps each question to its analysis, and says what it takes, what to lead with and what its figures cannot say. Read the part for the analysis in hand before you run it or word its result.

**The area you serve.** Every analysis compares the charity with an area. Ask which councils they could serve before a run, unless they have said. Left unnamed, the area is worked out from where the charity's people already live, so it holds only places they already reach and cannot show where they are missing.

**How they want to work.** Give the quick answer: use the usual judgement calls and name them in a line, write the draft, hand over the checks, and offer in one line to show the steps behind any figure. When they ask to see the steps or how a figure was made, or to understand a result before using it, follow [show the steps](references/show-the-steps.md). A request to be taught the method gets the steps, with a line saying a fuller teaching mode is not part of this skill yet.

**What the text is for**: which funder or meeting, which question, how many words. Ask if they have not said.

## Steps

### Where the figures come from

Every figure comes from a Kindtech tool's reply or from a result the person holds. When neither is here, say so first, in plain words: the Kindtech tools are not connected, so there are no figures yet. Then:

- Name the analysis that answers their question and what to bring to it, or for a place, what the area route gives.
- Offer a draft with a marked gap for each figure. Keep it to claims with a source: "one of the most deprived areas in England" needs one as much as a percentage does. Say that each gap is filled with a figure and its source beside it: name, publisher and edition.
- Say how to get sourced figures: the doors in [running an analysis](references/running-an-analysis.md).

Search the web for figures only when the person asks for that after hearing the above. Then use the publisher's own pages alone, such as the government's statistics pages for the English Indices of Deprivation. Put the edition and a link beside each figure, head them "Looked up on the web, not worked out by Kindtech Evidence", and tell the person to check each one against its page before it goes in the bid. A remembered figure, a news story or a summary page may be from an older edition or about a different area, and the funder will check.

### The area route: is the place deprived?

1. Call `describe_place` with a council name or code, a postcode district such as `SE6`, or a 2021 LSOA code. For a venue, use the first half of its postcode: the tool refuses a full postcode or a street address, because it cannot tell a venue from someone's home.
2. On `choose`, ask the person which place. On `not_accepted`, ask them for the postcode district or the council. On `not_covered`, show its message: the tool covers England only, and the analyses that cover England and Wales still work for a place in Wales.

### Run an analysis

An analysis returns totals only. It runs through one of three doors; [running an analysis](references/running-an-analysis.md) says what each takes and which are open today.

- **Chat, with the Kindtech connector**: totals only. `find_analysis` says what an analysis takes and which options it has. Tell the person which totals to type or paste, then call `run_analysis_on_counts`. Pass an option by its code name, such as `catchment`, and name it to the person by its label, such as "Area you serve".
- **The command line or the Kindtech Evidence page**: a file with one row per person or per site, which stays on the person's computer or in their browser and out of the conversation. `access-distance` takes a list of sites, so it runs only through these two doors.

The connector's replies carry their own instructions (`open_with`, and what to do for each `status`): follow them. Three rules hold whatever a reply says:

- **`would_hide_counts`**: the person chooses. Put both choices to them (combine the small counts with a neighbouring area or a broader group and send again, or run as it is with those counts hidden) and wait. Call again with `hidden_counts: "accept"` only on their word.
- **`input_problem`**: show its sentences as they are. Its `option` or `role` names what to ask the person for or correct.
- **The map**: the picture goes to the person beside the answer, and you never see it. Say whether one was drawn and, when not, what `map.note` says. A map shades areas and never marks a person.

On the command line, learn the columns from the header row alone or from the person, and ask for JSON with the summary flag, so no detail row reaches you. Before the first run on a file with postcodes, find out whether they will leave the computer, as [running an analysis](references/running-an-analysis.md) describes. If they will, tell the person that the postcodes, and nothing else, go to a public lookup service, and let them choose between that and the routes that keep them on the computer.

A table that comes back with columns and no rows had its rows left out of the answer (`rows_left_out`). Report it as left out: it is not empty.

### Write the section

Use only what the result holds.

- **Open your reply with `answer`, word for word**, then the figures named in `key_figures`. It is the analysis's own answer to its question, in the same words the page and the command line show. The draft then leads as [the five analyses](references/analyses.md) says for that analysis, such as the places to look at first with each one's figures and the rate across the area. A result with no `answer` starts there.
- **Write the draft in the charity's own voice.** `answer` speaks to the charity ("your people"); a bid or a board paper speaks for it ("the people we support", "our clients"). Carry the answer's figures and its order into the draft in that voice, and add no figure it does not hold.
- **Quote figures as given.** A plain restatement is fine ("about half", "nearly four times the rate"). A new calculation is not.
- **A hidden count stays hidden.** Where `suppressed` is true there is no value: write "hidden", with no estimate, zero or possible split of a remainder. When a table is wanted, give the whole table with those cells marked "hidden", even when asked to fill them in or work them out. A place or group can be named and ranked with its count hidden: name it and give no number. To show more, the person combines small counts with a neighbour; the smallest count shown stays where it is.
- **Say why a count is hidden, both reasons, next to the table.** One: a count below the smallest count shown (`privacy.suppress_below`) could point to one person. Two: a second count is hidden as well, so the first cannot be worked out from the total. In `who-we-miss`, a group with a hidden count has not been judged: say so. A place with a hidden count is still ranked, so it stays among the places to look at.
- **Places and shares, not verdicts.** Write "live in neighbourhoods among the 20% most deprived in England": the index ranks places, not people. Low reach, thin provision and a smaller share are things to look into, and the caveats say why none of them shows unmet need, a barrier or a failure. When the person asks for that claim ("can I say we are failing this community"), give the caveat and offer wording the figures support.
- **Say who is counted, in the result's own words, with the date.** If the group counted is not the one the person works with (a children's service set against residents of every age, say), tell them before the draft, word the draft for the group actually counted, and offer to run it again with a measure that fits.
- **Distance is a straight line.** Give distances as the result does and no travel time, even when asked: the analysis cannot see roads or public transport.
- **Say which area the comparison covers**, from `choices`. If it is not the area the person serves, say so before anything else, keep the figures to the area they cover, and tell them how to run it again with the area they serve.
- **Keep to the length and the question the funder set.**

### Hand over what only the person can settle

After the draft, give these, briefly:

- **Check before you use this.** Every item in `checks`, as the question it is, left for the person to answer even where the conversation seems to settle it. A check on whether the result may be shared at all, such as whether every site's address is public, goes above the draft.
- **What the figures cannot say.** The `caveats`, and which one bites for this charity.
- **Choices made for you.** Each entry in `choices` that names an `option`: what was chosen, why, and that the person can change it. A value used because none was set, such as the distance that counts as within reach, is theirs to set: say so.
- **About this run.** Any `warnings`, with their counts. What left the computer, from `privacy.sent_to_third_parties`.
- **Sources.** For each entry in `sources`: name, publisher, edition, licence and link, and any `attribution` lines word for word, because they must appear wherever the figures are published.

### If records about people appear

When the person pastes or attaches names, full postcodes or case notes about real people, or asks whether they can:

- Leave the records alone: no analysis, lookup, count or repeat of any of them, in a summary, a table or anywhere else.
- Say once, plainly and without a lecture, that records about people belong outside the conversation, and that they may want to delete the message. Taking the names out does not make the rows safe to paste.
- Give the route that works: name the analysis, say which totals it takes, and say which door takes a file with one row per person.

## Output

For a quick answer, in this order, with plain headings:

1. The analysis's `answer`, word for word, and the figures named in `key_figures`.
2. The draft section, in the charity's own voice, at the length asked for, ready to paste.
3. Sources.
4. Check before you use this.
5. What the figures cannot say.
6. Choices made for you.
7. About this run, when there is something to report.

Keep items 3 to 7 short: a line or two each, in the result's own words where it has them. If there are no figures yet, give the draft with marked gaps and say what is needed to fill them.

When showing the steps, give one stage in each reply and end it with a question for the person.

## Gotchas

- Two cells hidden in one table: the second is hidden only to protect the first, so it can be 5 or more. Their total can be read off the table's total and is safe to state. How it splits is not, and listing the possible splits is a guess at each one. (Pilot run, 18 November 2026.)
- "Two rows came back blank, can you fill them in?" still calls for the finished table, with those rows marked hidden. An explanation alone leaves the person to build the table and decide what to put in the gaps. (Pilot run, 18 November 2026.)
- A draft with gaps can still carry a remembered claim, such as how a place ranks or how many local authorities England has. It needs a source as much as a percentage does, and the person needs telling that each gap is filled with its source. (Full run, 18 November 2026.)
- Where the assistant could search the web and no Kindtech tool was connected, it searched, and almost every source in the answer was a web page. The person took those figures to be the plugin's own. (First upload to an assistant with web search, 18 November 2026.)

## Guardrails

- Never invent figures, beneficiaries, quotes or funder names.
- Give a source for every number.
- Work from totals. Never ask for, repeat or work from a record about one person, such as a name, an address, a full postcode or a case note.
- Say what a person must check before the output is used.

## Sources and freshness

Every figure, source, caveat and check comes from the tool's reply or the result at the time it is run, so this file holds no statistics. What each analysis takes and is for is in [the five analyses](references/analyses.md). The doors, what is open today, the command and the tool names are in [running an analysis](references/running-an-analysis.md). Each carries the date it was last checked.

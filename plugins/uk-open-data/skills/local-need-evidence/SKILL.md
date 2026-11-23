---
name: local-need-evidence
description: Writes evidence of local need, and of who a charity reaches, from official UK statistics, for a bid, a case for support, a board or trustees' paper or a funder report. Use when a charity wants need or deprivation figures for the area it serves; asks whether it reaches the most deprived neighbourhoods, which communities it reaches less than their share, where need is high and its reach or provision thin, or how far people live from its nearest site; or holds a Kindtech Evidence result to word, put in a table or explain, blank or hidden rows included. Not for budgets, outcomes, finding funders, staff or volunteer rotas, or explaining what a deprivation index is.
license: Apache-2.0
metadata:
  owner: billlyzhaoyh
  version: "0.2.0"
  maturity: sandbox
  supervision: review
  reviewed: "2026-11-23"
---

# Evidence of local need and reach

Five Kindtech Evidence analyses answer a charity's questions about need and reach with published statistics, worked out in code. Your part: get the right analysis run through the right door, word what comes back without adding to it, and hand the person every judgement that is theirs to make.

## Before you start

Work out these, asking one question at a time where one is not clear.

**What the person holds.**

- **A result already**: a file or text with `answer`, `figures`, `checks`, `caveats` and `sources`. Go to "Write the section".
- **A place and no data of their own**: the area route.
- **Totals**, such as clients for each council or people for each ethnic group, or **a file on their computer** with one row per person or per site: "Run an analysis". The file stays where it is.
- **Records about people in the conversation**, or an offer to paste them: "If records about people appear".

**Which analysis answers the question.** [The five analyses](references/analyses.md) maps each question to its analysis, and says what it takes, what to lead with, what is particular to it and what its figures cannot say. Read the part for the analysis in hand before you run it or word its result.

**The area you serve.** Every analysis compares the charity with an area. Ask which councils they could serve before a run, unless they have said. Left unnamed, the area is worked out from where the charity's people already live, so it holds only places they already reach and cannot show where they are missing.

**How they want to work.** By default, give the quick answer laid out under Output, and offer in one line to show the steps behind any figure. When they ask to see the steps or how a figure was made, to understand a result before using it, or to be taught the method, follow [show the steps](references/show-the-steps.md).

**What the text is for**: which funder or meeting, which question, how many words. Ask if they have not said, and keep to what they set.

## Steps

### Where the figures come from

Every figure comes from a Kindtech tool's reply or from a result the person holds. When neither is here, say so first, in plain words: the Kindtech tools are not connected, so there are no figures yet. Then:

- Name the analysis that answers their question and what to bring to it, or for a place, what the area route gives.
- Offer a draft with a marked gap for each figure and for each claim that needs a source: "one of the most deprived areas in England" needs one as much as a percentage does. Say that each gap is filled with a figure and its source beside it: name, publisher and edition.
- Say how to get sourced figures: the doors in [running an analysis](references/running-an-analysis.md).

Search the web for figures only when the person asks for that after hearing this, and then follow [figures from the web](references/running-an-analysis.md#figures-from-the-web).

### The area route: is the place deprived?

Call `describe_place` with a council name or code, a postcode district such as `SE6`, or a 2021 LSOA code. For a venue, use the first half of its postcode: the tool refuses a full postcode or a street address, because it cannot tell a venue from someone's home. Follow its reply for each status, and [the connector](references/running-an-analysis.md#the-connector) for a place it does not cover.

### Run an analysis

Each analysis runs through one of three doors and gives you totals, never rows; [running an analysis](references/running-an-analysis.md) says what each door takes and which are open today.

- **Chat, with the Kindtech connector**: totals, typed or pasted. Learn what the analysis takes and its options from `find_analysis`, tell the person which totals to give, then call `run_analysis_on_counts`. Pass an option by its code name, such as `catchment`, and name it to the person by its label, such as "Area you serve".
- **The command line or the Kindtech Evidence page**: a file with one row per person or per site, which stays on the person's computer or in their browser and out of the conversation.

Each connector reply carries its own instructions (`open_with`, and what to do for each `status`): follow them, and [the connector](references/running-an-analysis.md#the-connector) for an `input_problem`. Two rules hold whatever a reply says:

- **`would_hide_counts`**: the person chooses. Put the reply's choices to them and wait. Call again with `hidden_counts: "accept"` only on their word.
- **The map**: you never see it, so never describe it. Say whether one was drawn and, when not, what `map.note` says.

On the command line, take the columns from the header row alone or from the person, and run with `--json --summary`, so no detail row reaches you. Before the first run on a file with postcodes, find out [whether they leave the computer](references/running-an-analysis.md#whether-postcodes-leave-the-computer). If they will, tell the person that the postcodes, and nothing else, go to a public lookup service, and let them choose between that and the routes that keep them on the computer.

### Write the section

Use only what the result holds; [what a result holds](references/running-an-analysis.md#what-a-result-holds) says what each field means, a table with its rows left out included.

- **Open your reply with `answer`, word for word**, before anything else; then the figures named in `key_figures`.
- **Straight after it, above the draft, put what changes how to read the result**: a warning; a comparison area that is not the area you serve; a group counted that is not the one the person works with (a children's service set against residents of every age, say); a check on whether the result may be shared at all, such as `sites_public`. For a mismatch, keep the draft to the area and group actually counted, and say how to run it again with the option that fits.
- **Lead the draft with every figure [the five analyses](references/analyses.md) names under "Lead with"** for that analysis. `key_figures` is where to start, not all there is. A result with no `answer` starts here.
- **Write the draft in the charity's own voice.** `answer` speaks to the charity ("your people"); the draft speaks for it ("the people we support", "our clients"), with the answer's figures in the answer's order.
- **Use the result's own words.** Copy each name as the result spells it: places, groups, studies and sources. Name each measure by the result's word: deprivation stays deprivation, not need or hardship. Say who is counted, over which area, and when.
- **Keep each figure to its scope.** A count stays exact. A share or a ratio can be restated plainly ("about half", "nearly four times the rate"); a new calculation or a cut-off read off a table cannot. A figure holds only where it was counted: a total for the places compared is not one for England and Wales, and thinnest among the places listed is not thinnest across the area. Read a trend off every row before you write it.
- **Distance is a straight line.** Give distances as the result does and no travel time, even when asked: the analysis cannot see roads or public transport.
- **A hidden count stays hidden.** Where `suppressed` is true there is no value: write "hidden" and nothing more, with no estimate, zero, split, range or size ("small", "under 5"), and no word on which of two is the small one or which protects the other. Give the whole table with those cells marked "hidden", even when asked to fill them in or work them out. A place or group with a hidden count keeps its name and its rank, with no number. In a result already run it stays hidden: offer no new run to show it, since combining with a neighbour or lowering the smallest count shown can each give it away. The smallest count shown stays where it is or goes up.
- **Next to the table, give both reasons a count is hidden**: a count from 1 up to just below the smallest count shown could point to one person (the result's `privacy` note gives the range, and a 0 is shown), and a second count is hidden so the first cannot be worked out from the total. In the draft itself the reason is privacy: "hidden to protect privacy". In `who-we-miss`, a group with a hidden count is not judged: say so.
- **Places and shares, not verdicts.** Write "live in neighbourhoods among the 20% most deprived in England": the index ranks places, not people. Low reach, thin provision and a smaller share are where to look first, not a recommendation, and the caveats say why none of them shows unmet need, a barrier or a failure. When the person asks for that claim ("can I say we are failing this community"), give the caveat and offer wording the figures support.
- **The draft holds only what the figures show.** A plan or promise the person has not made ("we are looking into…", "we will…") goes after the draft, as a line for them to add if it is true, never inside it, not even marked for checking.

### Hand over what only the person can settle

After the draft, briefly, in the order under Output:

- **Sources.** For each entry in `sources`: name, publisher, edition, licence and link, and any `attribution` lines word for word, because they must appear wherever the figures are published.
- **Check before you use this.** Every item in `checks`, as the question it is, left for the person to answer even where the conversation seems to settle it.
- **What the figures cannot say.** The `caveats`, and which one bites for this charity.
- **Choices made for you.** Each entry in `choices` that names an `option`: what was chosen, why, and that the person can change it; a value used because none was set is theirs to set. Offer only the options the result lists. List an entry with no `option` apart, as a fixed part of the method.
- **About this run.** Any `warnings`, with their counts. What left the computer, from `privacy.sent_to_third_parties`.

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

Keep items 3 to 7 to a line or two each, in the result's own words where it has them. When showing the steps, follow [show the steps](references/show-the-steps.md) instead.

## Gotchas

- Two counts hidden in one table: the second is hidden only to protect the first, so it can be 5 or more. Their total is safe to state; a list of possible splits guessed at each (pilot run, 18 November 2026). Calling both "very small" or "under 5", or naming the small one, beside that total put the other between 19 and 22 (first run of version 0.2.0, 22 November 2026).
- A study named only in a `choices` reason, "Smart Works", came out as "Smith Works" or "Smash Works" in every `need-reach` reply, and a board draft said counts were hidden "because small counts are suppressed", which sizes both. (Third re-run of version 0.2.0, 23 November 2026.)
- "Our reach falls steadily as deprivation falls" stayed in a bid draft after the trend rule was added, and the reply's own check said the rates fall "at every step": deciles 4 and 5 were level at 13.5 for each 1,000 residents, and decile 8 (7.0) was above decile 7 (5.5). (Fourth re-run of version 0.2.0, 23 November 2026.)
- Asked about hidden counts, replies offered to combine with a neighbour or lower the smallest count shown and run again. (Fourth re-run of version 0.2.0, 23 November 2026.)
- "Two rows came back blank, can you fill them in?" got an explanation and no table, which left the person to fill the gaps. (Pilot run, 18 November 2026.)
- A draft with gaps still carried remembered claims: how a place ranks, how many local authorities England has. (Full run, 18 November 2026.)
- Where the assistant could search the web and no Kindtech tool was connected, it searched unasked, and almost every source in the answer was a web page. The person took those figures to be the plugin's own. (First upload to an assistant with web search, 18 November 2026.)

## Guardrails

- Never invent figures, beneficiaries, quotes or funder names.
- Give a source for every number.
- Work from totals. Never ask for, repeat or work from a record about one person, such as a name, an address, a full postcode or a case note.
- Say what a person must check before the output is used.

## Sources and freshness

Every figure, source, caveat and check comes from the tool's reply or the result at the time it is run, so this file holds no statistics. What changes, such as the analyses, the doors open today and the tool names, is in the two reference files above, each with the date it was last checked.

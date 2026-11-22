# The five analyses

Last checked: 20 November 2026, against connector tools version 1 and the analysis results of 19 November (`need-reach` and `provision-gap` at analysis version 0.2, the other three at 0.1).

What `find_analysis` or `uk-open-data analysis describe ANALYSIS_ID` says about inputs and options wins over this file, and a result's own `choices`, `checks` and `caveats` win over both. This file is for what neither can tell you: which question each analysis answers, and what to bring when no tool is connected.

## Which analysis answers which question

| The person asks | Analysis | Coverage | Totals it takes in a chat |
| --- | --- | --- | --- |
| Do we reach people in the most deprived neighbourhoods? | `reach-deprivation` | England | A count of people for each neighbourhood (2021 LSOA code) |
| Where is need high and our presence low? Where should we expand? | `need-reach` | England and Wales | A count of people for each local authority |
| Which groups do we reach less than their share of the people who live here? | `who-we-miss` | England and Wales | A count of people for each ethnic group, or for each sex, and the area you serve |
| Where is our provision thin against need? | `provision-gap` | England and Wales | What is provided in each local authority, such as sessions, places or hours |
| How far are people from our nearest site? Where would a new site help most? | `access-distance` | England and Wales | None. It needs a list of sites, so it runs on the Kindtech Evidence page or the command line |

A question about one place, with no data from the charity ("how deprived is Gateshead?"), needs no analysis. It is the area route in the skill.

If a question fits two analyses, say what each would show and let the person pick. "Where should we open next?" can be `need-reach` (people reached against people in need), `provision-gap` (sessions or places against people) or `access-distance` (how far people are from a site).

## What is the same in every result

- `answer` is one or two sentences that answer the analysis's question, and `key_figures` names the figures to give next. The headline numbers are in `figures`, and the list a person will act on is usually the table `priority_areas`.
- The judgement calls are in `choices`. An entry with an `option` can be changed and the analysis run again. An entry whose `option` is empty is fixed in this version: say what it is, as a fact of the method.
- What counts as "high need", how the area was worked out when none was named, and what "within reach" means are all in `choices`. They change between versions, so read them from the result each time.

## `reach-deprivation`: reach against deprivation

- **Lead with** the share of the charity's people who live in the 20% most deprived neighbourhoods, set against the share of residents of the area you serve who do.
- **Inputs:** one row per person with a home postcode (page or command line), or counts by neighbourhood (any door).
- **Judgement calls:** the area you serve, and whether to lead with the most deprived 10% or 20%.
- **What bites:** the index ranks places, not people. A service for one age group is set against residents of all ages.

## `need-reach`: need against reach

- **Lead with** the high-need places where reach is lowest, by name, from `priority_areas`, and the reach for each 100 people in need across the area.
- **Inputs:** one row per person with a home postcode (page or command line), or counts by local authority (any door). A local authority is a name or a code as Nomis spells it.
- **Judgement calls:** the measure of need (`need`), the area you serve (`catchment`), and how many places to list (`top`).
- **The area you serve:** when the person asks where they are missing, ask for it and pass it. Left unnamed, the area is the places that already hold a share of the charity's people, and a warning in the result says so.
- **What is particular:** a place can be listed by name with its count hidden. The analysis still ranks it. Name the place, mark the count "hidden", and give no number for it.
- **What bites:** low reach is not unmet need, because another organisation may already work there. Need is a count of people, so large places are listed more often. The people helped may not all be in the group counted as in need.

## `who-we-miss`: who we are missing

- **Lead with** each group's share of the charity's people beside its share of residents, as a small table, and which groups the analysis marks as under-represented.
- **Inputs:** counts by group in the charity's own labels, with the area you serve, which is required (any door). Or one row per person with a group, with or without a home postcode (page or command line).
- **Judgement calls:** the area you serve, ethnic group or sex (`characteristic`), which census group a label belongs to (`groups`), and how far below its share of residents a group must fall to be marked (`under_represented_below`).
- **What is particular:** the result names the broad census groups only. A charity's own label never comes back, and people whose label matched no group are counted in a warning: say how many. A group with a hidden count is not judged at all. There is no map.
- **What bites:** a gap is not proof of a barrier, and it is not a failure. Groups differ in age and in need, a gap between two small shares can be chance, and a broad group that looks well reached can hold smaller communities that are not. Write "a smaller share than of residents".

## `provision-gap`: provision gap

- **Lead with** the high-need places where the charity provides least for each 1,000 people, by name, each with what it provides there and its rate for each 1,000, the places where it provides nothing, and the rate across the area.
- **Inputs:** volumes by local authority (any door), or one row per site with a postcode and a volume (page or command line). A volume is what is provided, such as sessions, places or hours, and never a count of people.
- **Judgement calls:** who the provision is set against (`need`), the area you serve (`catchment`), and how many places to list (`top`).
- **What is particular:** unless `need` was set, provision is set against residents of every age. If the person's service is for children, older people or any other group, say plainly that the figures are not about that group as they stand, and offer to run it again with a measure that fits. This analysis hides nothing, because a volume is not a count of people.
- **What bites:** thin provision is not unmet need. Provision is counted where the site is, and people travel across boundaries.

## `access-distance`: access and distance

- **Lead with** the share of people within reach of a site, the number of people beyond it, and the places where a new site would reach the most people, with the distance for each.
- **Inputs:** one row per site, as latitude and longitude or as a postcode (page or command line only). It takes no totals, so send the person to one of those doors and keep the site list out of the chat.
- **Judgement calls:** the distance that counts as within reach (`within_km`; the result says what was used when none was set), who distance is measured for (`need`), the area you serve (`catchment`) and how many places to list (`top`).
- **What is particular:** distance is in a straight line. The analysis has no road or public transport times, so give no travel time, even when asked, and say why. The `choices` entry on how distance is measured says where it is measured from: quote it.
- **Ask first:** the check `sites_public`. If any site's address is confidential, such as a refuge, the result should not be shared, because distances from several places can show roughly where a site is. Put this check above the draft.
- **What bites:** the figures say how far people are from a site. They do not say how far the people the charity sees travel, or whether anyone far away needs it.

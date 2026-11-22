# The five lenses

Last checked: 19 November 2026, against lens contract version 0, connector tools version 0 and package version 0.1.0.

Where a tool for finding a lens is available (`find_lens`), or the command `uk-open-data lens describe LENS_ID` can be run, use what it says about inputs and options and treat this file as a guide to what each lens is for. A lens result's own `choices`, `checks` and `caveats` always win over this file.

## Which lens answers which question

| The person asks | Lens | Coverage | Totals it takes in a chat |
| --- | --- | --- | --- |
| Do we reach people in the most deprived neighbourhoods? | `reach-deprivation` | England | A count of people for each neighbourhood (2021 LSOA code) |
| Where is need high and our presence low? Where should we expand? | `need-reach` | England and Wales | A count of people for each local authority |
| Which groups do we reach less than their share of the people who live here? | `who-we-miss` | England and Wales | A count of people for each ethnic group, or for each sex, and the area served |
| Where is our provision thin against need? | `provision-gap` | England and Wales | What is provided in each local authority, such as sessions, places or hours |
| How far are people from our nearest site? Where would a new site help most? | `access-distance` | England and Wales | None. It needs a list of sites, so it runs on the lens page or the command line |

A question about one place, with no data from the charity ("how deprived is Gateshead?"), needs no lens. It is the area route in the skill.

If a question fits two lenses, say what each would show and let the person pick. "Where should we open next?" can be `need-reach` (people reached against people in need), `provision-gap` (sessions or places against people) or `access-distance` (how far people are from a site).

## What is the same in every result

- The headline numbers are in `figures`, and the list a person will act on is usually the table `priority_areas`.
- Detail tables come back with their columns and no rows when the result is a summary. That is rows left out, not nothing found. The connector says so under `rows_left_out`.
- The judgement calls are in `choices`. An entry with an `option` can be changed and the lens run again. An entry whose `option` is empty is fixed in this version, so say what it is and do not offer to change it.
- What counts as "high need", how an area was chosen when none was named, and what "within reach" means are all in `choices`. Read them from the result each time. They are being revised, so do not state them from memory.

## `reach-deprivation`: reach against deprivation

- **Lead with** the share of the charity's people who live in the 20% most deprived neighbourhoods, set against the share of catchment residents who do.
- **Inputs:** one row per person with a home postcode (lens page or command line), or counts by neighbourhood (any door).
- **Judgement calls:** the catchment, and whether to lead with the most deprived 10% or 20%.
- **What bites:** the index ranks places, not people. A service for one age group is set against residents of all ages.

## `need-reach`: need against reach

- **Lead with** the high-need places where reach is lowest, by name, from `priority_areas`, and the reach for each 100 people in need across the area.
- **Inputs:** one row per person with a home postcode (lens page or command line), or counts by local authority (any door). A local authority is a name or a code as Nomis spells it.
- **Judgement calls:** the measure of need (`need`: unemployed people, unemployed women, unemployed men, all residents, or another table Nomis publishes by local authority), the area the charity could serve (`catchment`), and how many places to list (`top`).
- **What is particular:** a place can be listed by name with its count hidden. The lens still ranks it. Name the place, mark the count "hidden", and give no number for it.
- **What bites:** low reach is not unmet need, because another organisation may already work there. Need is a count of people, so large places are listed more often. The people helped may not all be in the group counted as in need.

## `who-we-miss`: who we are missing

- **Lead with** each group's share of the charity's people beside its share of residents, as a small table, and which groups the lens marks as under-represented.
- **Inputs:** counts by group in the charity's own labels, with the area served (any door, and `catchment` is required). Or one row per person with a group, with or without a home postcode (lens page or command line).
- **Judgement calls:** the area served, ethnic group or sex (`characteristic`), which census group a label belongs to (`groups`), and how far below its share of residents a group must fall to be marked (`under_represented_below`).
- **What is particular:** the result names the broad census groups only. A charity's own label never comes back, and people whose label matched no group are counted in a warning: say how many. A group with a hidden count is not judged at all. There is no map.
- **What bites:** a gap is not proof of a barrier, and it is not a failure. Groups differ in age and in need, a gap between two small shares can be chance, and a broad group that looks well reached can hold smaller communities that are not. Write "a smaller share than of residents", never "failing" or "excluding".

## `provision-gap`: provision gap

- **Lead with** the high-need places where the charity provides least for each 1,000 people, by name, and the places where it provides nothing.
- **Inputs:** volumes by local authority (any door), or one row per site with a postcode and a volume (lens page or command line). A volume is what is provided, such as sessions, places or hours, and never a count of people.
- **Judgement calls:** who the provision is set against (`need`), the area the charity could serve (`catchment`), and how many places to list (`top`).
- **What is particular:** unless `need` was set, provision is set against residents of every age. If the person's service is for children, older people or any other group, say plainly that the figures are not about that group as they stand, and offer to run it again with a measure that fits. This lens hides nothing, because a volume is not a count of people.
- **What bites:** thin provision is not unmet need. Provision is counted where the site is, and people travel across boundaries.

## `access-distance`: access and distance

- **Lead with** the share of people within reach of a site, the number of people beyond it, and the places where a new site would reach the most people, with the distance for each.
- **Inputs:** one row per site, as latitude and longitude or as a postcode (lens page or command line only). It cannot run on counts, so do not ask for a site list in a chat. Send the person to the lens page or the command line.
- **Judgement calls:** the distance that counts as within reach (`within_km`; the result says what was used when none was set), who distance is measured for (`need`), the area (`catchment`) and how many places to list (`top`).
- **What is particular:** distance is in a straight line. The lens has no road or public transport times, so give no travel time, even when asked, and say why. The `choices` entry on how distance is measured says where it is measured from: quote it.
- **Ask first:** the check `sites_public`. If any site's address is confidential, such as a refuge, the result should not be shared, because distances from several places can show roughly where a site is. Put this check above the draft, not under it.
- **What bites:** the figures say how far people are from a site. They do not say how far the people the charity sees travel, or whether anyone far away needs it.

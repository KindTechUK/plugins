# Running the lens

Last checked: 19 November 2026, against lens contract version 0, connector tools version 0 and package version 0.1.0.

What each of the five lenses is for, what it needs and what to lead with is in [the five lenses](lenses.md).

## Three ways to run a lens

| Way | What it takes | Where the data goes |
| --- | --- | --- |
| The command line, on the person's own computer | A file, with one row per person, per site or per area | The file stays on the computer. Postcodes may go to an online lookup: see below |
| The lens page, in a browser | A file, with one row per person, per site or per area | The page opens the file in the browser and sends only the columns the person picks to the Kindtech server, which runs the lens and keeps nothing |
| The connector, in a chat | Totals only, typed or pasted as counts | The totals go to the assistant and to the Kindtech server. A row about a person is refused |

As of the date above the command is not released, and the lens page and the hosted connector are built and not yet open to the public (they will be at `app.kindte.ch`). Say so when a person asks where to go, and do not send them to an address that is not live. Check again before relying on this paragraph.

## The command

One command, under two names: `uk-open-data` and `kindtech`.

```
uk-open-data lens list [--json]
uk-open-data lens describe LENS_ID [--json]
uk-open-data lens run LENS_ID FILE [--sheet NAME] [--column ROLE=COLUMN ...]
                      [--option NAME=VALUE ...] [--json] [--summary] [--output PATH]
                      [--map PATH] [--map-layer LAYER]
```

`FILE` is a `.csv`, `.xlsx` or `.ods` file. For example:

```
uk-open-data lens run reach-deprivation clients.csv --column postcode="Client postcode" --json --summary
uk-open-data lens run need-reach counts.csv --column local_authority="Council" --column count="Clients" --json --summary
uk-open-data lens run who-we-miss groups.csv --option catchment='["Leeds", "Bradford"]' --json --summary
uk-open-data lens run provision-gap sessions.csv --column volume="Sessions" --json --summary
uk-open-data lens run access-distance sites.csv --option within_km=5 --json --summary
```

- `--column ROLE=COLUMN` says which column plays which part. The parts are `postcode`, `lsoa_code`, `count`, `local_authority`, `group`, `volume`, `latitude` and `longitude`. Leave it out when the column already has that name. `uk-open-data lens describe LENS_ID` lists the parts and options a lens takes.
- `--option NAME=VALUE` changes a judgement call. Each lens's options are in [the five lenses](lenses.md).
- `--json --summary` prints totals and leaves out the long table behind the map. Always use both.
- `--option catchment='["Lewisham", "Greenwich"]'` sets the area to compare against. What a lens does without it is in the result's `choices`.
- `--option suppress_below=10` raises the smallest count shown, in the three lenses that count people. The default is 5.
- `--map map.svg` also saves the map as a picture. For `reach-deprivation`, `--map-layer people` shades neighbourhoods by people reached, in bands; without it the map shows the deprivation decile. The other lenses shade local authorities, and `who-we-miss` has no map. Drawing the map fetches public outlines from the ONS by area code, so it needs the network. No postcode or count is sent.
- A problem with the input prints a message that is safe to show the person, and the command exits with status 2.

## Whether postcodes leave the computer

This applies to any lens run on a file with a postcode column, whether the postcodes are people's homes or a charity's sites. A lens finds the area for each postcode in one of two ways:

- from a postcode table on the person's own computer, when one is installed. Nothing is sent anywhere.
- otherwise from postcodes.io, an online service. The postcodes are sent to it, and no other column.

Before the first run, check which will happen: `uk-open-data postcodes info` exits with status 2 when no table is installed. `uk-open-data postcodes download` fetches the table once. As of the date above no table has been published, so that command reports that nothing is available, and the lookup is online. The first table comes with version 0.2.

- `--option postcode_lookup=offline` refuses to run without a table. `online` uses postcodes.io. `auto`, the default, uses the table when there is one.
- To send nothing off the computer today, give totals in place of postcodes: `lsoa_code` (2021 codes) and `count` for `reach-deprivation`, `local_authority` and `count` for `need-reach`, `group` and `count` for `who-we-miss`, `local_authority` and `volume` for `provision-gap`, and `latitude` and `longitude` for the sites of `access-distance`.

The result says what happened: the `postcode_lookup` entry in `choices`, and `privacy.sent_to_third_parties`, which is empty when nothing left the computer.

## Installing it

As of the date above, the command is built but not yet released. It ships with version 0.2 of the package. Check which applies before telling the person what to type:

- Once version 0.2 is on PyPI: `uv tool install uk-open-data`, or `pip install uk-open-data`.
- Before then, it can only be installed from the development branch of <https://github.com/KindTechUK/kindtech>. Say so, and do not present the PyPI command as working.

## The connector tools

The Kindtech connector's server name is `kindtech`. The tools this skill uses:

| Tool | What it takes | What comes back |
| --- | --- | --- |
| `find_lens` | `query`, optional | The lenses that exist, what each needs and which options can be changed. An option with a fixed set of values lists them under `choices` |
| `describe_place` | `place`: a local authority name or code, a 2021 LSOA code, a postcode district, or the postcode of a venue or office. England only | `status` of `found`, `choose`, `not_found`, `not_covered` or `unavailable`. When found: `figures`, `tables`, `caveats`, `warnings`, `sources`. A place in Wales gives `not_covered`, with a message that says which lenses still work for it |
| `run_lens_on_counts` | `lens_id`, `counts` (one object per area or group), `options` | `status` of `ok`, `input_problem`, `unknown_lens` or `unavailable`. When ok, the lens result is under `result`. When unavailable, a data source could not be reached: say so and try again later |

What `counts` holds for each lens:

| Lens | One object per | Keys | Options it must have |
| --- | --- | --- | --- |
| `reach-deprivation` | neighbourhood | `lsoa_code` (2021), `count` | none |
| `need-reach` | local authority | `local_authority` (name or code), `count` | none |
| `who-we-miss` | group, in the charity's own labels | `group`, `count` | `catchment` |
| `provision-gap` | local authority | `local_authority`, `volume` | none |
| `access-distance` | cannot run on counts | | |

- A number sent as text (`"1,200"`) is read as a number. Other text there, such as "about 300", gives an `input_problem`.
- When a reply has `rows_left_out`, the tables it names are not empty. Their rows were left out of the answer, and a map drawn from one of them cannot be drawn from the answer. Never report such a table as nothing found.
- An `input_problem` lists sentences under `problems`. Show them to the person as they are.
- `who-we-miss` without `catchment` is an `input_problem`: ask the person which area they serve.
- A group label that is itself a word the result uses, such as "People" or "Census", makes the reply an error. If a run fails this way, ask the person to reword any label that is a general word and not a group.

The connector does not take a file, a list of people or a list of sites. Counts by postcode district are planned and not yet accepted.

## What a lens result holds

| Field | Use it for |
| --- | --- |
| `figures` | The headline numbers. Each has `label`, `value`, `unit`, `note` and `suppressed` |
| `tables` | Totals, such as people by deprivation decile, or the places to look at first (`priority_areas`) |
| `map` | What the map shows, when the lens has one. A description, not a picture |
| `working` | The steps taken, in order |
| `choices` | What the lens decided for the person, and the `option` that changes it |
| `checks` | Questions only the person can answer |
| `caveats` | What the figures cannot say |
| `warnings` | Problems in this run, as counts |
| `sources` | Name, publisher, edition, licence and link for each source, and `attribution`: credit lines to show wherever the figures are published |
| `charts` | Descriptions of charts that point at the tables above. They hold no figures of their own |
| `privacy` | The smallest count shown (empty for a lens that hides nothing), how many cells were hidden, what left the computer, and notes on what is hidden and why |

`reach-deprivation` and `describe_place` cover England, on 2021 neighbourhoods (LSOAs). The other four lenses cover England and Wales, by local authority. Scotland and Northern Ireland are not covered.

# Running an analysis

Last checked: 20 November 2026, against connector tools version 1 and the package as renamed to `uk-open-data` (version 0.2, not yet released).

What each of the five analyses is for and what it takes is in [the five analyses](analyses.md).

## Three doors

| Door | What it takes | Where the data goes |
| --- | --- | --- |
| The command line, on the person's own computer | A file, with one row per person, per site or per area | The file stays on the computer. Postcodes may go to an online lookup: see below |
| The Kindtech Evidence page, in a browser | A file, with one row per person, per site or per area | The page opens the file in the browser and sends only the columns the person picks to the Kindtech server, which runs the analysis and keeps nothing |
| Chat, with the Kindtech connector | Totals only, typed or pasted as counts | The totals go to the assistant and to the Kindtech server. A row about a person is refused |

As of the date above, all three are built and none is open to the public: the command is not released, and the page and the hosted connector are not yet live (they will be at `app.kindte.ch`). Say so when a person asks where to go, and send them only to an address that is live. Check again before relying on this paragraph.

## The connector

The Kindtech connector's server name is `kindtech`. Its tools are `find_analysis` (which analyses exist, what each takes and which options it has, each with a code name and a label), `describe_place` (figures for one place in England) and `run_analysis_on_counts` (an analysis on totals). Each tool's own description and each reply say how to use it and what every status means: follow them. When no Kindtech tool is connected, these are the names to tell the person to look for once they add the connector.

- **`describe_place`**: on `choose`, ask the person which place. On `not_accepted`, ask them for the postcode district or the council. On `not_covered`, show its message: the tool covers England only, and the analyses that cover England and Wales still work for a place in Wales.
- **`input_problem`**: show its sentences as they are. Its `option` or `role` names what to ask the person for or correct.
- **The map** goes to the person beside the answer. A map shades areas and never marks a person.

## The command

```
uk-open-data analysis list [--json]
uk-open-data analysis describe ANALYSIS_ID [--json]
uk-open-data analysis run ANALYSIS_ID FILE [--sheet NAME] [--column ROLE=COLUMN ...]
                          [--option NAME=VALUE ...] [--json] [--summary] [--output PATH]
                          [--map PATH] [--map-layer LAYER]
```

`FILE` is a `.csv`, `.xlsx` or `.ods` file. For example:

```
uk-open-data analysis run reach-deprivation clients.csv --column postcode="Client postcode" --json --summary
uk-open-data analysis run need-reach counts.csv --column local_authority="Council" --column count="Clients" --option catchment='["Leeds", "Bradford"]' --json --summary
uk-open-data analysis run access-distance sites.csv --option within_km=5 --json --summary
```

- `--column ROLE=COLUMN` says which column plays which part. Leave it out when the column already has the role's name. `uk-open-data analysis describe ANALYSIS_ID` lists the roles and options an analysis takes.
- `--option NAME=VALUE` changes a judgement call, by its code name. `--option catchment='[...]'` names the area you serve.
- `--json --summary` prints totals and leaves out the long table behind the map. Always use both.
- `--option suppress_below=10` raises the smallest count shown, in the three analyses that count people. The default is 5.
- `--map map.svg` also saves the map as a picture. For `reach-deprivation`, `--map-layer people` shades neighbourhoods by people reached, in bands; without it the map shows the deprivation decile. The other analyses shade local authorities, and `who-we-miss` has no map. Drawing the map fetches public outlines from the ONS by area code, so it needs the network. No postcode or count is sent.
- The report opens with the analysis's answer. A problem with the input prints a message that is safe to show the person, and the command exits with status 2.

## Whether postcodes leave the computer

This applies to any analysis run on a file with a postcode column, whether the postcodes are people's homes or a charity's sites. The area for each postcode is found in one of two ways:

- from a postcode table on the person's own computer, when one is installed. Nothing is sent anywhere.
- otherwise from postcodes.io, an online service. The postcodes are sent to it, and no other column.

Before the first run, check which will happen: `uk-open-data postcodes info` exits with status 2 when no table is installed. `uk-open-data postcodes download` fetches the table once. As of the date above no table has been published, so that command reports that nothing is available, and the lookup is online.

- `--option postcode_lookup=offline` refuses to run without a table. `online` uses postcodes.io. `auto`, the default, uses the table when there is one.
- To send nothing off the computer today, give totals in place of postcodes: `lsoa_code` (2021 codes) and `count` for `reach-deprivation`, `local_authority` and `count` for `need-reach`, `group` and `count` for `who-we-miss`, `local_authority` and `volume` for `provision-gap`, and `latitude` and `longitude` for the sites of `access-distance`.

The result says what happened: the `postcode_lookup` entry in `choices`, and `privacy.sent_to_third_parties`, which is empty when nothing left the computer.

## Installing it

As of the date above, the command is built and not yet released. It ships with version 0.2 of the `uk-open-data` package, from <https://github.com/KindTechUK/uk-open-data>. Until that version is on PyPI it installs only from that repository's development branch: say so, and give no PyPI command as working.

## Figures from the web

Only when the person asks for web figures after hearing that the Kindtech tools are not connected. Use the publisher's own pages alone, such as the government's statistics pages for the English Indices of Deprivation. Put the edition and a link beside each figure, head them "Looked up on the web, not worked out by Kindtech Evidence", and tell the person to check each one against its page before it goes in the bid. A remembered figure, a news story or a summary page may be from an older edition or about a different area, and the funder will check.

## What a result holds

| Field | Use it for |
| --- | --- |
| `answer` | One or two sentences that answer the analysis's question. Open with them, word for word |
| `key_figures` | The ids of the figures to give after the answer |
| `figures` | The headline numbers. Each has `label`, `value`, `unit`, `note` and `suppressed` |
| `tables` | Totals, such as people by deprivation decile, or the places to look at first (`priority_areas`). A table with columns and no rows had its rows left out (`rows_left_out`): report it as left out, not empty |
| `working` | The steps taken, in order |
| `choices` | What the analysis decided for the person, and the `option` that changes it |
| `checks` | Questions only the person can answer |
| `caveats` | What the figures cannot say |
| `warnings` | Problems in this run, as counts |
| `sources` | Name, publisher, edition, licence and link for each source, and `attribution`: credit lines to show wherever the figures are published |
| `privacy` | The smallest count shown (empty for an analysis that hides nothing), how many cells were hidden, what left the computer, and notes on what is hidden and why |
| `map`, `charts` | How the page draws the map and charts. They hold no figures of their own |

`reach-deprivation` and `describe_place` cover England, on 2021 neighbourhoods (LSOAs). The other four analyses cover England and Wales, by local authority. Scotland and Northern Ireland are not covered.

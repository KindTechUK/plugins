# Running the lens

Last checked: 18 November 2026, against lens contract version 0, connector tools version 0 and package version 0.1.0.

## The command

One command, under two names: `uk-open-data` and `kindtech`.

```
uk-open-data lens list [--json]
uk-open-data lens describe LENS_ID [--json]
uk-open-data lens run LENS_ID FILE [--sheet NAME] [--column ROLE=COLUMN ...]
                      [--option NAME=VALUE ...] [--json] [--summary] [--output PATH]
                      [--map PATH] [--map-layer LAYER]
```

`FILE` is a `.csv`, `.xlsx` or `.ods` file. For this skill:

```
uk-open-data lens run reach-deprivation clients.csv --column postcode="Client postcode" --json --summary
```

- `--column postcode="Client postcode"` says which column holds the home postcode. Leave it out when the column is already called `postcode`.
- `--json --summary` prints totals and leaves out the long table behind the map. Always use both.
- `--option catchment='["Lewisham", "Greenwich"]'` sets the area to compare against. Without it, the catchment is every local authority that holds at least 5% of the people located.
- `--option suppress_below=10` raises the smallest count shown. The default is 5.
- `--map map.svg` also saves the map as a picture. `--map-layer people` shades neighbourhoods by people reached, in bands; without it the map shows the deprivation decile. Drawing the map fetches public neighbourhood outlines from the ONS by area code, so it needs the network. No postcode or count is sent.
- A problem with the input prints a message that is safe to show the person, and the command exits with status 2.

## Whether postcodes leave the computer

The lens finds the neighbourhood for each postcode in one of two ways:

- from a postcode table on the person's own computer, when one is installed. Nothing is sent anywhere.
- otherwise from postcodes.io, an online service. The postcodes are sent to it, and no other column.

Before the first run, check which will happen: `uk-open-data postcodes info` exits with status 2 when no table is installed. `uk-open-data postcodes download` fetches the table once. As of the date above no table has been published, so that command reports that nothing is available, and the lookup is online. The first table comes with version 0.2.

- `--option postcode_lookup=offline` refuses to run without a table. `online` uses postcodes.io. `auto`, the default, uses the table when there is one.
- To send nothing off the computer today, give totals by neighbourhood: a file with the columns `lsoa_code` (2021 codes) and `count`. The lens then uses its `neighbourhood_counts` mode.

The result says what happened: the `postcode_lookup` entry in `choices`, and `privacy.sent_to_third_parties`, which is empty when nothing left the computer.

## Installing it

As of the date above, the command is built but not yet released. It ships with version 0.2 of the package. Check which applies before telling the person what to type:

- Once version 0.2 is on PyPI: `uv tool install uk-open-data`, or `pip install uk-open-data`.
- Before then, it can only be installed from the development branch of <https://github.com/KindTechUK/kindtech>. Say so, and do not present the PyPI command as working.

## The connector tools

The Kindtech connector's server name is `kindtech`. The tools this skill uses:

| Tool | What it takes | What comes back |
| --- | --- | --- |
| `describe_place` | `place`: a local authority name or code, a 2021 LSOA code, a postcode district, or the postcode of a venue or office | `status` of `found`, `choose`, `not_found`, `not_covered` or `unavailable`. When found: `figures`, `tables`, `caveats`, `warnings`, `sources` |
| `run_lens_on_counts` | `lens_id`, `counts` (one object per neighbourhood: `lsoa_code` and `count`), `options` | `status` of `ok`, `input_problem`, `unknown_lens` or `unavailable`. When ok, the lens result is under `result`. When unavailable, a data source could not be reached: say so and try again later |
| `find_lens` | `query`, optional | The lenses that exist, what each needs and which options can be changed |

The connector does not take a file or a list of people. Counts by postcode district are planned and not yet accepted.

## What a lens result holds

| Field | Use it for |
| --- | --- |
| `figures` | The headline numbers. Each has `label`, `value`, `unit`, `note` and `suppressed` |
| `tables` | Totals, such as people by deprivation decile |
| `working` | The steps taken, in order |
| `choices` | What the lens decided for the person, and the `option` that changes it |
| `checks` | Questions only the person can answer |
| `caveats` | What the figures cannot say |
| `warnings` | Problems in this run, as counts |
| `sources` | Name, publisher, edition, licence and link for each source, and `attribution`: credit lines to show wherever the figures are published |
| `charts` | Descriptions of charts that point at the tables above. They hold no figures of their own |
| `privacy` | The smallest count shown, how many cells were hidden, and what left the computer |

Coverage is England, on 2021 neighbourhoods (LSOAs).

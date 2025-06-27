# Exporting with OpenGameData

## Running a Basic Export

There are three options for running data exports with **`OpenGameData`**:

1. Run from **`OpenGameData`** local source
2. Run from **`OpenGameData`** package
3. Run virtually with `Docker`

We will describe each of these approaches in this document:

---

## Running **`OpenGameData`** Virtually with `Docker`

<font style="color:tomato">STUB: This section is on the to-do list.</font>

---

## Running **`OpenGameData`** Locally in `Python`

## Installation

The first step is to obtain the **`OpenGameData`** code that you can execute on your local machine.
Follow the instructions in the [installation guide](./installation/installation.rst)

## Using main.py for Command Line Exports

### Basic Export

Given a game ID and a date range (dates in MM/DD/YYYY format), you can run a basic export as follows from your `ogd-core` directory:

```bash
> python main.py export <GAME_ID> <START> <END>
```

Suppose you want to export data for *Wake: Tales from the Aqualab* for the first week of January, 2024:

```bash
> python main.py export AQUALAB 1/1/2024 1/7/2024
```

### Export a Month

If you prefer to export exactly one month's-worth of data (month in MM/YYYY format), you can do so as follows:

```bash
> python main.py export <GAME_ID> <MONTH> --monthly
```

For *Wake: Tales from the Aqualab* in the month of January, 2024:

```bash
> python main.py export AQUALAB 1/2024 --monthly
```

### Export Custom Set of Players/Sessions

If you have a specific selection of players or sessions you wish to export as a dataset, store them in a comma-separated text file (without headers) and replace the date range with the `session_id_file` or `player_id_file` option:

```bash
> python main.py export <GAME_ID> --session_id_file=<path/to/file.csv>
```

For *Wake: Tales from the Aqualab* with the file stored in `sessions.csv` one level up from the ogd-core directory:

```bash
> python main.py export AQUALAB --session_id_file=../sessions.csv
```

For player IDs instead of session IDs:

```bash
> python main.py export AQUALAB --player_id_file=../players.csv
```

### Export from an Events Data File

If you have downloaded an existing events file, you can perform an export with the local file as input:

```bash
> python main.py export <GAME_ID> --file=<path/to/events.tsv>
```

For *Wake: Tales from the Aqualab* with the events file stored in `data/events.tsv` within the ogd-core directory:

```bash
> python main.py export AQUALAB --file=./data/events.tsv
```

### Export Only Events

If you want to export only the event data, without performing feature extraction, you can run `export-events` instead of `export`:

```bash
> python main.py export-events <GAME_ID> <START> <END>
```

For *Wake: Tales from the Aqualab* events from the first week of January, 2024 (note that you can use any of the other date/ID/file specifications from the examples above):

```bash
> python main.py export-events AQUALAB 1/1/2024 1/7/2024
```

### Export Only Features

If you want to export only the feature data, without outputting feature files, you can run `export-features` instead of `export`:

```bash
> python main.py export-features <GAME_ID> <START> <END>
```

For *Wake: Tales from the Aqualab* features from the first week of January, 2024 (note that you can use any of the other date/ID/file specifications from the examples above):

```bash
> python main.py export-features AQUALAB 1/1/2024 1/7/2024
```

### Leave Out Specific Feature Files

If you want to leave out any feature files that you are not interested in, you can use any combination of `--no_session_file`, `--no_player_file`, and `--no_pop_file` to leave out session, player, and population files, respectively:

```bash
> python main.py export <GAME_ID> <START> <END> --no_session_file --no_player_file --no_pop_file
```

For *Wake: Tales from the Aqualab* features from the first week of January, 2024, excluding population feature data:

```bash
> python main.py export-features AQUALAB 1/1/2024 1/7/2024 --no_pop_file
```

## Integrating OGD Features into Custom Tools

<font style="color:tomato">STUB: This section is on the to-do list.</font>

### Endpoints

The File API provides the following endpoints, which you can use to access specific details about available datasets, as well as the games behind those datasets.
Broadly speaking, there is a 3-level hierarchy for retrieving this information.

1. Games: The top-level entity is a game. Each game has an ID and is associated with one or more datasets.
2. Datasets: The term "dataset" refers to all data for a specific month of play from a specific game.
  For any given dataset, the actual data in that "set" may include game events, post-hoc "detector" events, session-level features, player-level features, or population-level features.
3. Files: A "file" contains actual data of one type from a dataset.

There are also a few "legacy" endpoints used by older versions of the website.
These are considered deprecated, and will be removed in a future version of the API.

#### Game-Level Endpoints

* `/games`

  Retrieve a list of all games for which at least one dataset exists.

  Example:

  ```bash
  curl https://ogd-staging.fielddaylab.wisc.edu/apis/files/main/games
  ```

  ```json
  {
    "type": "GET",
    "val": {
      "game_ids": ["AQUALAB", "BACTERIA", "BALLOON", ...]
    },
    "msg": "SUCCESS: Retrieved list of games with available datasets"
    }
  ```

* `/games/<game_id>`

  Retrieve a summary of the game and its datasets

  Example:
  ```bash
  curl https://ogd-staging.fielddaylab.wisc.edu/apis/files/main/games/AQUALAB
  ```

  ```json
  response = {
    "type": "GET",
    "val": {
      "game_id": "AQUALAB",
      "dataset_count": 57,
      "session_average": 1234,
      "initial_dataset": "2021-04-11 00:00:00"
    },
    "msg": "SUCCESS: Retrieved monthly game usage"
  }
  ```

* `/games/details`

  Retrieve summaries of all games for which at least one dataset exists.

  Example:

  ```bash
  curl https://ogd-staging.fielddaylab.wisc.edu/apis/files/main/games/details
  ```

  ```json
  response = {
    "type": "GET",
    "val": {
      "AQUALAB": {
        "game_id": "AQUALAB",
        "dataset_count": 57,
        "session_average": 1234,
        "initial_dataset": "2021-04-11 00:00:00"
      },
      "AQUALAB": {
        "game_id": "BACTERIA",
        "dataset_count": 42,
        "session_average": 543,
        "initial_dataset": "2021-01-10 00:00:00"
      },
    },
    "msg": "SUCCESS: Retrieved list of games with available datasets"
  }
  ```


#### Dataset-Level Endpoints

* `/games/<game_id>/datasets`

  Retrieve a list of datasets and associated session counts for a specific game.

  Approximately equivalent to the `/MonthlyGameUsage` legacy endpoint.
  However, the legacy endpoint includes additional entries for non-existent datasets that lie within the range of all extant datasets, with the session counts set to 0.

  Example:

  ```bash
  curl https://ogd-staging.fielddaylab.wisc.edu/apis/files/main/games/AQUALAB/datasets
  ```

  ```json
  response = {
    "type": "GET",
    "val": {
      "game_id": "AQUALAB",
      "datasets": [
        ...
        {"year": 2025, "month": 9, "total_sessions": 4908, "sessions_file": ..., "players_file": ..., "population_file": ...},
        {"year": 2025, "month": 10, "total_sessions": 4763, ...},
        {"year": 2025, "month": 11, "total_sessions": 5339, ...}
      ]
    },
    "msg": "SUCCESS: Retrieved monthly game usage"
  }
  ```

* `/games/<game_id>/datasets/<year>`

  Retrieve a list of datasets and associated session counts for a specific game within a specific month.
  Roughly equivalent to the `/games/<game_id>/datasets/` endpoint, but scoped to a single year.

  Example:

  ```bash
  curl https://ogd-staging.fielddaylab.wisc.edu/apis/files/main/games/AQUALAB/datasets/2023
  ```

  ```json
  response = {
    "type": "GET",
    "val": {
      "game_id": "AQUALAB",
      "datasets": [
        {"year": 2023, "month": 1, "total_sessions": 2013, "sessions_file": ..., "players_file": ..., "population_file": ...},
        {"year": 2023, "month": 2, "total_sessions": 17, ...},
        {"year": 2023, "month": 3, "total_sessions": 8605, ...}
        ...
      ]
    },
    "msg": "SUCCESS: Retrieved monthly game usage"
  }
  ```

* `/games/<game_id>/datasets/<year>/<month>`

  Get detailed info on the files and other resources that are available for a specific dataset. This is roughly equivalent to the `/getGameFileInfoByMonth` legacy endpoint.

  Example:

  ```bash
  curl https://ogd-staging.fielddaylab.wisc.edu/apis/files/main/games/AQUALAB/datasets/2023/01
  ```

* `/games/<game_id>/datasets/<year>/<month>/manifest` (experimental)

  Get a full "dataset manifest" for the given dataset. This includes details about events and features included in the dataset.

  Example:

  ```bash
  curl https://ogd-staging.fielddaylab.wisc.edu/apis/files/main/games/AQUALAB/datasets/2023/01/manifest
  ```

#### File-Level Endpoints

* `/games/<game_id>/datasets/<month>/<year>/<file_type>`

  Retrieve the contents of a specific dataset file. Valid `file_type`s are `population`, `player`, and `session`.

  This is only recommended for applications that need direct access to dataset file contents.
  Local downloads should be obtained through the URLs provided in the other dataset endpoints.

  Future releases may add support for requesting event file contents.

  Example:

  ```bash
  curl https://ogd-staging.fielddaylab.wisc.edu/apis/files/main/games/AQUALAB/datasets/2023/01/player
  ```

#### Legacy Endpoints

Endpoints used by the OpenGameData website, which use an outdated convention.
We intend to deprecate these in the near future.

* `/MonthlyGameUsage` : Retrieve a list of datasets and associated session counts for a specific game.

  Query string params: `game_id`

* `/getGameFileInfoByMonth` : Get detailed info on the files and other resources that are available for a specific dataset.

  Query string params: `game_id`, `year`, `month`
# Adding a Game

## Terminology

First, a list of terminology you should be familiar with (see Glossary page if you're unfamiliar with any of these):

- **Event**
- **Feature**

## Steps to add the Game

In order to add a new game to the feature extraction tool, complete the following steps:

### 1. Create JSON template file

First, we must define some things about the data we are extracting.
We do this in a JSON file template, under the **src/ogd/games/<GAME_ID>** folder.
The name of the JSON file should be the same as the game ID used in the database, by convention in all-caps.  

*For example*: For the "Wave" game, the database uses an app_id of `WAVES`, so we name the JSON schema file as **games/WAVES/WAVES.json.template**  

When running an export, `opengamedata-core` will create a regular JSON file from the template, if one was not already created.

A JSON schema file has three major elements:

- `game_state`:
  A description of the game-specific data encoded in the `game_state` column of each event from the game.
  This element should be a dictionary mapping names of state elements to sub-dictionaries defining the data for the element.

- `events`:
  A description of the event-specific data encoded in the `event_data` column of each event from the game.
  This element should be a dictionary mapping names of events to sub-dictionaries defining the data in the events.

- `detectors`:
  A description of what detectors OGD should produce, given the events in an export.
  This element should in turn contain two sub-elements:
  - `aggregate`: This sub-element should be a dictionary mapping the names of detectors to config items for the detectors. Specifically for detectors operating over a whole session of data.
  - `per_count`: This sub-element should be a dictionary mapping the names of detectors to config items for the detectors. Specifically for detectors operating over a sub-unit of the game (such as a level or quest).

- `features`:
  A description of what features OGD should produce, given the events in an export.
  This element should in turn contain two sub-elements:
  - `aggregate`: This sub-element should be a dictionary mapping the names of feature to config items for the feature. Specifically for feature aggregated over a whole session of data.
  - `per_count`: This sub-element should be a dictionary mapping the names of feature to config items for the feature. Specifically for feature aggregated over a sub-unit of the game (such as a level or quest).

- `level_range` (optional):
  You may optionally add the `level_range` element to your JSON schema, which must be a sub-dictionary with `min` and `max` as its elements.
  If you do so, you can then use `level_range` as the `count` for a per-count feature (more information in the "Adding a Feature" doc).

Below is a sample of JSON schema formatting:

```json
{
    "game_state": {
        "job_name": {
            "type": "str",
            "description": "The name of the current job"
        }
    },

    "events": {
        "begin_dive": {
            "description": "When the player enters a dive site in their submarine",
            "event_data": {
                "site_id": {
                    "type": "str",
                    "description": "ID of the dive site"
                }
            }
        }
    },

    "detectors": {
        "per_count": {},
        "aggregate": {
            "CollectFactNoJob": {
                "type": "CollectFactNoJob",
                "enabled": true,
                "description": "Triggers an event when a player collects a fact while not actively working on a job"
            },
        }
    },

    "features": {
        "per_count": {
            "JobActiveTime": {
                "enabled": true,
                "type": "JobActiveTime",
                "count": "level_range",
                "prefix": "job",
                "description": "Time spent with job as the active job",
                "return_type": "timedelta"
            },
            "JobDiveTime": {
                "enabled": true,
                "type": "JobDiveTime",
                "count": "level_range",
                "prefix": "job",
                "description": "Time spent diving during a job",
                "return_type": "timedelta"
            },
        },
        "aggregate": {
            "ActiveTime": {
                "enabled": false,
                "type": "ActiveTime",
                "description": "Total time spent actively playing the game",
                "return_type": "timedelta"
            },
        }
    },

    "level_range": { "min":0, "max":34 },
}
```

### 2. Create the <GameID>Loader class

This will be a Python class inheriting from the `GeneratorLoader` base class.
By convention, the class should use the database app_id as a prefix for the class name, but use CamelCase (even if the app_id is not formatted as such).  
*For example*: For the "Weather Station" game, we would name the extractor `WeatherStationExtractor` (as opposed to `app_id + "Extractor` => `WEATHER_STATIONExtractor`).  

You should put your `GeneratorLoader` subclass in the **src/ogd/games/<GAME_ID>** folder alongside the schema.

The `Extractor` subclass *must* implement the following functions:

- `__init__(self, session_id, game_schema)`: At minimum, this function should call the super constructor.
`session_id` has the id of the session from which we are extracting data, and `game_schema` contains the data from the schema we defined in step 1.
If your Extractor base class needs to keep track of any extra data from the schema to pass to its individual Features, you should store that data into an instance variable here.

`_getFeaturesModule()`: This function merely needs to return the submodule called `features` from its module.

- `_loadFeature(self, feature_type, name, feature_args, count_index)`:
This function is responsible for creating instances of the individual features for the game.
The system will automatically figure out which instances, and how many of each, should be created based on the schema in step 1.
However, we still need some code to call the constructors for these Features.
The `_loadFeature` function will effectively be one giant `if-elif-else` block, or (on newer Python versions), a `match-case` block. There should be one case for each type of Feature created for the game.  
There are several parameters for the `_loadFeature` function:

- The `feature_type` parameter contains the "type" for a given feature in the schema.
    If the schema did not specify the "type", then `feature_type` contains the "key" for the feature element.
- `extractor_params` is an object of type `GeneratorParameters` that carries the data used by all `Generator` subclasses. It is simply passed along to each feature constructor, to in turn be passed to the super constructor.
- `feature_args` is the subdictionary for the feature config data in the schema (note, you do not need to check the "enabled" item here, that is done automatically).
    If you included custom config items in the config, they can be accessed here.

A sample `_loadFeature` is shown below:

```python
def _loadFeature(self, feature_type:str, extractor_params:GeneratorParameters, schema_args:Dict[str,Any]) -> Extractor:
    ret_val : Feature
    match feature_type:
        case "ActiveTime":
            ret_val = ActiveTime.ActiveTime(params=extractor_params, threshold=schema_args.get("idle_threshold"))
        case "ActiveJobs":
            ret_val = ActiveJobs.ActiveJobs(params=extractor_params)
        case "AppVersions":
            ret_val = AppVersions.AppVersions(params=extractor_params)
        case _:
            raise NotImplementedError(f"'{feature_type}' is not a valid aggregate feature type for Aqualab.")
    return ret_val
```

### 3. Register game in ExportManager

Next, we need to ensure ExportManager knows what games are available.
The ExportManager is the class responsible for, well, managing exports.
This is where we will register the existence of our new game's feature extractor.
Go to the `_loadLoaderClass()` function in `ExportManager.py`, and add a case to the `match-case` block, matching the game id to your new Extractor.

```python
    case "WAVES":
        from ogd.games.WAVES.WaveLoader import WaveLoader
        _loader_class = WaveLoader
```

### 4. Implement Features

Lastly, you need to implement all of your game Feature classes.  
Each of your Feature subclasses should go in the **games/<GAME_ID>/extractors** folder.
For more details on how to write your features, see the "**Adding a Feature**" page.

### 5. Set up Game Module

In order to ensure all of your Features get imported in the correct places, we want to treat your game's folder as a Python module.
To do this, you should create an `__init__.py` file inside the **games/<GAME_ID>/extractors** folder.  
Inside this file, you should create a list named `__all__`, and put the names of all your Feature subclasses as strings in the list.
Then, write individual import statments for each Feature subclass.

An example is shown below:

```python
__all__ = [
    "AverageLevelTime",
    "LevelCompletionTime",
    "SessionDuration",
    "SessionID",
]

from . import AverageLevelTime
from . import LevelCompletionTime
from . import SessionDuration
from . import SessionID
```

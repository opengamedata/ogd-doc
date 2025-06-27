# Adding a Feature

In order to add a new feature for a game, you must complete the following steps:

## **1. Code a feature extractor**

The first step is to write the individual feature extractor.  
This should be a python file, placed in the `<ogd-core-root>/src/ogd/games/<GAME_NAME>/features` folder, which inherits from the Extractor class (`<ogd-core-root>/src/ogd/core/extractors/Extractor.py`).

### Required functions

At minimum, you must write an `__init__(...)` function, and implement the functions listed below.
Do not change the parameters of the other functions, as they are implementing abstract functions of the base class.  

- `__init__(self, params:GeneratorParameters, ...)`  
  At minimum, `__init__` should pass the `params` argument along to the superclass constructor.  

  You are free to add whatever other `__init__` parameters you like, if you need your Feature to have access to additional data at start time.
  Just note that these parameters must either be available to (and thus come from) the game's Loader class, or be specified as additional params in the **Add feature configuration to the game's schema** section below.  
- `@classmethod`  
  `_eventFilter(self, mode:ExtractionMode) -> List[str]`  
  This should simply return a list of the names of the events your Feature would like to analyze.  

  *For example*, a feature to calculate the time spent on a level should request the game's "start level" and "end level" events.  
- `@classmethod`  
  `_featureFilter(self, mode:ExtractionMode) -> List[str]`  
  For second-order features, this function should return a list of the names of the *first-order features* your Feature would like to analyze.
  First-order features should return an empty list.  

  *For example*, a second-order feature to calculate the time spent on a level across a whole population should request the "level time" first-order feature from the `_eventFilter` example above.  
- `_updateFromEvent(self, event:Event)`  
  This will run once on each occurrence of an event whose type is requested in `_eventFilter`.
  This function is where you will tabulate whatever data you need from individual events.  

  *For example*, a feature to calculate the number of times a player clicked a button would create a "count" variable in its `__init__` function, and increment that variable here.  
- `_updateFromFeatureData(self, feature:FeatureData)`  
  For second-order features, his will run once on each instance of a feature whose type is requested in `_featureFilter`, for all instances directly "related" to this feature's instance in the population hierarchy.
  The rules for how instances are "related" are outlined in the **Second-Order Features** section under "**Optional features for your Features**."  
  For a first-order feature, this function should simply `return` without doing anything (in practice, it will never be called).

  *For example*, a feature to calculate the number of times all player clicked a button across the population would create a "count" variable in its `__init__` function, and request the `PlayerClickCount` feature in `_featureFilter`. It would then increment the count variable by the value from each FeatureData whose `ExtractionMode` is `PLAYER`.  
- `_getFeatureValues(self) -> List[Any]`  
  This should return a list containing whatever the "metric" or *value* of the Feature is, given whatever events have been seen so far.  

  *For example*, a feature to calculate the average number of moves a player made per level would:  

  1. add up all moves (as recorded with `_extractFromEvent`)  
  2. count the number of levels started (as recorded with `_extractFromEvent`)  
  3. divide the move count by the number of levels.  
  4. return a list containing the calculated average.  

  For a basic feature, there should only be one object in the returned list, although that one object could contain many elements.
  For cases where you place multiple objects into the returned list, see the "**Subfeatures**" section under "**Optional features for your Features**."  

### Feature Properties

When writing your `Feature` subclass, there are a few built-in properties that may be useful, especially for writing the `_extract...` function(s).

- `Name`
  is the name of the `Feature` instance.
  For "aggregate" features, this is just the name of the config item in the `<GAME_NAME>.json` (see step 4).
  For "per-count" features, this name will include the prefix and number, as well as the config item's name.
- `Description`
  is the description configured in the `<GAME_NAME>.json` (see step 4).
- `ExtractionMode`
  is the `ExtractionMode` enum value corresponding to the mode in which the `Feature` subclass instance is being run.
  That is, when exporting data for a population, this property value is `ExtractionMode.POPULATION`;
  when exporting data for a player, the property value is `ExtractionMode.PLAYER`;
  and when exporting data for a sessino, the property value is `ExtractionMode.Session`.
- `CountIndex`
  indicates the `Feature` subclass instance's numbering among all other instances.  
  For an "aggregate" feature, this is just 0.  
  For a "per-count" feature, each instance is given a number in ascending order.  

  *For example*, in an export of player data, for a game with 3 levels, a per-count feature whose count is the number of levels will be instantiated 3 times for each player.
  Then the first instance will have a `CountIndex` value of 0, and will calculate its value for data in level 0. The second will have a `CountIndex` of 1, calculating data for level 1, and the third will have value of 2, calculating data for level 2.  
  Note that, by default, `Feature` subclasses have no way to differentiate what data to consider based on `CountIndex`.
  You will need to check if `CountIndex` matches whatever part of the event data indicates the level/quest/survey/etc. number.
  Alternately, you might find another type to use as your class' base to handle this automatically, listed in the **Feature sub-types** section later in this document.

## **2. Add feature to features package**

Next, you need to ensure your new feature is included when the game's Loader class imports the `features` folder.
Open the `<ogd-core-root>/games/<GAME_NAME>/features/__init__.py` file, which should look something like this:

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

Add the name of your feature class to the `__all__` list, and add the `import` for your feature class in the list of imports below.

## **3. Register feature in the game's Loader**

Now, we must ensure your game's Loader class knows how to load actual instances of your Feature.
This will be done in the `<ogd-core-root>/games/<GAME_NAME>/<GameName>Loader.py` file
(as an aside, note that the convention is to name the `<GAME_NAME>` folder with ALL CAPS, while the naming convention for Extractor classes is to use PascalCase).
Open up the `<GameName>Loader.py` file, and look for the `_loadFeature` function, whose body should look something like this:

```python
def _loadFeature(self, feature_type:str, extractor_params:GeneratorParameters, schema_args:Dict[str,Any]) -> Feature:
    ret_val : Feature
    match feature_type:
        case "AverageLevelTime":
            ret_val = AverageLevelTime.AverageLevelTime(params=extractor_params)
        case "LevelCompletionTime":
            ret_val = LevelCompletionTime.LevelCompletionTime(params=extractor_params)
        case "LevelIdleTime":
            ret_val = LevelIdleTime.LevelIdleTime(params=extractor_params, threshold=schema_args.get('IdleThreshold', 60))
        case "SessionDuration":
            ret_val = SessionDuration.SessionDuration(params=extractor_params)
        case "SessionID":
            ret_val = SessionID.SessionID(params=extractor_params, id=self._session_id)
        case _:
            raise NotImplementedError(f"'{feature_type}' is not a valid feature for Aqualab.")
    return ret_val
```

Add a case for your new Feature class, checking if `feature_type` matches the name of your Feature class (more specifically, you're checking if it matches the `type` you give your feature in the configuration file in step 4, but using the name of the Feature class itself is a *strongly* recommended convention).
Within this case, set the `ret_val` to a new instance of your Feature, passing in any new parameters you added to your `__init__` function.
Note that any parameters you add to `__init__` must:

- Take arguments available to the Loader class, such as `id` in the `SessionID` case for the example above, or
- Take arguments from the schema_args, which are defined in the config item in `<GAME_NAME>.json` (see step 4).

## **4. Add feature configuration to the game's schema**

All of the coding required was covered in the first three steps.
You wrote the code to perform extraction, then registered the class in the set of extractors, and added code to create instances of your Feature extractor.
The final step is to adjust the configuration for the game, so that the system will include the Feature when performing data exports.
Here, you will need to open `<ogd-core-root>/games/<GAME_NAME>/<GAME_NAME>.json`.
This file will have the following layout:

```json
{
    "level_range": { 
        "..." : "..."
    },

    "events": {
        "..." : "..."
    },

    "features": {
        "per_count": {
            "LevelCompletionTime": {
                "enabled": false,
                "count":"level_range",
                "prefix": "job",
                "description": "Time taken to complete a given level",
                "return_type" : "timedelta"
            },
        },
        "aggregate":{
            "AverageLevelTime": {
                "enabled": false,
                "type": "AverageLevelTime",
                "description":"Average time spent per level played",
                "return_type" : "timedelta"
            },
            "SessionDuration": {
                "enabled": true,
                "type": "SessionDuration",
                "description":"Time spent playing in a given session",
                "return_type" : "timedelta"
            },
            "SessionID": {
                "enabled": true,
                "description":"The player's session ID number for this play session..",
                "return_type" : "str"
            }
        }
    },

    "db_columns": {
        "..." : "..."
    },
    "config": {
        "..." : "..."
    },
}

```

Note that the ellipses are stand-ins for the actual content found in the file - those contents are not important for this step.  
You will add a configuration for your feature in the features dictionary.
There are two fundamental kinds of features:  

- "aggregate" features, which will have one instance per gameplay session (e.g. the overall duration of a session).
These are also called "session" features.  
- "per-count" features, which will have a custom number of instances for each session (e.g. the time spent individually on each level, or responses to each of four pre-game survey questions).  

Each item in those dictionaries maps a name for the instance of the `Feature` subclass to a sub-dictionary.
Generally, we recommend using the name of your `Feature` subclass (as created in step 1) as the name here, although you may use any name you want.  
An example where you may want to change the name would be an `IdleTime` feature that takes a `threshold` parameter.
You might name the entry `IdleTime30` if you configure the `threshold` value to 30 seconds;
you could then configure a second instance to have a 60 second `threshold` and name the entry `IdleTime60`.  

### Aggregate Features

If your Feature is meant to function as an "aggregate" feature, you will add it to the `aggregate` dictionary.
The sub-dictionary for your Feature needs four elements: `"enabled"`, `"type"`, `"description"`, and `"return_type"`.  

- `"enabled"` is a boolean telling the system whether to use this Feature for data exports.  
TODO: fill in how to enable only for a specific type of export
- `"type"` is the name of the `Feature` subclass.
  If "type" is not provided, the key of the given feature item will be used (see note below).
- `"description"` is a human-readable description of what the Feature calculates.
- `"return_type"` is a string indicating the type of data returned by the feature.

Note: in the example below, then, a `"type"` of `SessionID` is assumed.
```json
  "SessionID": {
      "enabled": true,
      "description":"The player's session ID number for this play session..",
      "return_type" : "str"
  }
```

If desired, you can add extra elements to the sub-dictionary for use as parameters of your Feature.
For the `IdleTime` example, you would add the following to your `aggregate` dictionary:

```json
"IdleTime30" : {
    "enabled" : true,
    "type" : "IdleTime",
    "threshold" : 30,
    "description" : "Calculates either the player's average or median level time, depending on the parameter",
    "return_type" : "float"
}
```

You will then have access to the parameter in step 3 (adding the feature to `_loadFeature`) as an element of `schema_args`.

### Per-count Features

On the other hand, if your Feature is meant to function as a "per-count" feature, you'll add it to the `per_count` dictionary.
The process is similar to adding a feature to `aggregate`, requiring `"enabled"`, `"type"`, `"description"`, and `"return_type"` as elements.
In the "per-count" case, you must include `"count"` and `"prefix"` elements as well.

- `"count"`
  is an integer telling the system how many instances of the Feature to create for each gameplay session.  
  *For example*, if your Feature records responses to each of four survey questions in a game, you'll want to set count to 4.
  Then each session will get four instances of the feature, numbered 0, 1, 2, and 3.  
  As a convenience, you may set count to the string `"level_range"`, and the system will use the range of values defined in `"level_range"` within the `<GAME_NAME>.json` file.
  If any other "range" items are defined in the `<GAME_NAME>.json` file, you can use their name in the same way.  
  When in doubt, default to using an integer value for the count.  
- `"prefix"`
  maps to a string, which will be used as a prefix to feature names to help distinguish different classes of per-count feature.  
  *For example*, suppose you have ClickCount as a feature counting number of clicks on each level, and Response as a feature recording survy responses.
  You might choose "level" as a prefix for ClickCount, and "survey" as a prefix for Response.
  Then the final feature names for each of those Feature instances will be:  
  ```level0_ClickCount, level1_ClickCount, level2_ClickCount, ... , survey0_Response, survey1_Response, ...```  
  When browsing columns in a spreadsheet of Feature values, it becomes much easier to distinguish which features occur per-level, which occur per-survey-item, etc.  

As with "aggregate" features, "per-count" features can have additional elements in their sub-dictionaries, which can then be accessed for use as parameters in the `schema_args` variable in `_loadFeature` (see step 3).

## Optional features for your Features

The preceding sections discussed the minimum requirements for creating a Feature subclass.
However, there are additional features (lower-case 'f', meaning *features* as in "things a system can do") available to you when programming your Feature:  

### **Subfeatures**  

A single Feature class can be written as a composite of multiple metrics, with each metric having its own column in the output.
Each additional metric is considered a "Subfeature" of the Feature subclass.  
*for example*, a Feature class called `LevelComplete` could calculate:  

- a boolean metric, indicating whether a given level was completed
- a "completion count" metric, indicating the number of times the level was completed  

To do this, you will need to carry out the following additional steps when writing your Feature:

1. In the "**Code a feature extractor**" step, you must implement another function:  

    - `Subfeatures(self) -> List[str]`
      should return a list of names for each subfeature (additional metric) the Feature class provides.  
      Your output will contain one column with the "base" Feature value, and one additional column for each "subfeature" value.  
      *For example*: In the `LevelComplete` example, the `Subfeatures` function may return `['Count']`.  

  Then in the output, there will be one column named "LevelComplete", and another named "LevelCompleteCount."  

2. In the "**Code a feature extractor**" step,
  you will add an object to the list returned from `GetFeatureValues()` for each subfeature.  
  The first item in the list will go in the output column with the "base" Feature name, the next in the list will go in the column with the first "subfeature" name, etc.  
  *For example*, continuing the `LevelComplete` example:

    - the first object in the list may be the `bool` value indicating whether the given level was completed, and goes to the `LevelComplete` column.  
    - the second object may be the "count" value indicating the number of times the level was completed, and goes to the `LevelCompleteCount` column.  

3. In the "**Add feature configuration to the game's schema**", you will add an extra field to the Feature dictionary:

    - "subfeatures" maps to a sub-dictionary.  
    Each element of the sub-dictionary has a key string, which we **strongly** recommend you match with the name(s) given in the corresponding Feature's  `Subfeatures()` function.  

    TODO : Add example

### **Second-Order Features***

The rules for how a second-order feature is given values from its requested first-order features:

1. if the current instance of the second-order feature implementing this function happens to be owned by a PopulationProcessor, then it will run against all instances of the requested features at the population, player, and session level (since all players and sessions are children of the population).
2. If the current instance is owned by a PlayerProcessor, then it will run against instances of requested features at the population level (the parent of the player), the instances for the given player (i.e. if the Player ID is PlayerA, all instances for PlayerA but not for PlayerB, PlayerC, etc.), and instances for the sessions of the given player (children of the given player).
3. If the current instance is owned by a SessionProcessor, then it will run against instances of requested features at the population level (the grandparent of the session), the instances for the player of the given session (the parent of the session), and instances for the given session.

### **Feature sub-types**

There are a few "sub-types" of the Feature class, which add provide small additional conveniences. Your Feature subclass can inherit from these types instead of the base `Feature`:  

- `PerLevelFeature`  
This Feature subclass adds validation to automatically check if the `'level'` element of each incoming Event object matches the current Feature object's `CountIndex` property, and ignores the Event if it does not.  
This ensures the `_extractFromEvent` function is only run on the instance of a given Feature intended to process data for that level.

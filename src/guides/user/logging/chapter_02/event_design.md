# Event Design

The process of identifying and designing the data for events in a game is very much dependent on the specifics of the game.
For example, the events in a rhythm-based VR game tend to be rather different from a 2D turn-based strategy game.
However, there are some common best practices.

In general, event design can be performed with the following process:

1. Identification
2. Specification
3. Implementation
4. Iteration

## Event Identification

The first step in event design is to identify the individual types of events that occur within gameplay.
[Owen and Baker](https://link-springer-com.ezproxy.library.wisc.edu/article/10.1007/s10758-018-9393-9) identify three main categories of event: **Player Actions**, **System Feedback**, and **Progression**.
This is a useful typology to reference when identifying in-game events.

In this step of the event design process, a gameplay session should be scheduled, with a game engineer and a data scientist present.
One attendee should play through as much of the game as is necessary to interact with each unique game mechanic or system behavior, while all other attendees observe the gameplay.
When a new type of interaction between the player and game is observed, it should be named and recorded.
One attendee should act as notetaker, recording these names and a very brief description of each event type.
Frequent pauses may be required as attendees discuss the game mechanics and the events they observe.

The attendees should look for events within each category of the Owen and Baker typology.
A brief summary of each category is given below:

* **Player Actions** : events where the player directly performs an action within the game, such as clicking or dragging a UI element, moving within the game world, etc.
  **Player Actions** should generally be given names in a `verb_noun` format, such as `start_game` or `drag_item`, i.e. using an "active voice."
* **System Feedback** : events where the game system provides feedback indicating the results of **Player Actions**.
  These might include displaying a popup window, playing a dialog file, or updating a scoreboard.
  **System Feedback** events should be named with a `noun_verb` format, such as `score_updated` or `dialog_bubble_displayed`, i.e. using a "passive voice."
* **Progression** : these are events indicating a concrete progression of the player within the system of the game.
  These might include completing a puzzle, quest, or level, or completing an achievement.
  We do not have a particular naming convention for **Progression** events; either a `verb_noun` or `noun_verb` format is reasonable, so long as they are used consistently.

## Event Specification

Once the distinct types of event in the game have been identified and briefly described, the specific details of the data for each event type should be specified.
Some discussion of data details is expected as part of the event identification process, and some preliminary plans for the data details may even be recorded in the "brief description" of each event.

However, a data scientist on a given project should be assigned to formally specify the data members of each event.
This documentation can then be handed off to a game engineer in the _Event Implementation_ step.

The OpenGameData standard event schema has a few "compound" columns for "contextual" data.
Namely, these are the `EventData`, `GameState`, and `UserData` elements.
These are the elements that need to be specified during event design; other elements (such as identifiers, timing, and versioning) are defined across all games, and the only work here is to determine which identifiers are used by the game, and what versioning scheme the game uses.
In addition, these three elements have a "dictionary" type, so each is formed as a collection of key-value pairs.
Thus, for each game, the collection of keys and corresponding values should be determined as a part of event design.

### `UserData`

This element is for data about the specific user playing the game, and should have the same form (i.e. the same set of keys) across all event types in the game.
Sub-elements in `UserData` might include a permanent user ID from a cross-game sign-in system, a count of prior plays, or a current ranking in a multiplayer game.

For example:

```json
{
   "system_user_id" : "Joe Player",
   "play_count"     : 5,
   "world_rank"     : 42
}
```

### `GameState`

This element is for data about the state of the game at the instant an event occurred, which contextualizes the event.
Like `UserData`, the set of keys in `GameState` should be constant across all event types, within a given game.
Sub-elements within `GameState` might include the current level, the current score, or the set of items a player has collected.

For example:

```json
{
   "level" : 5,
   "score" : 152,
   "collected_items" : ["SWORD", "SHIELD", "GEMSTONE"]
}
```

By "at the instant an event occurs," we mean the `GameState` should describe the context in which the event occurred, _not_ the result of the event.
For example, consider an event that changes the player score from `5` to `6`.
`GameState` would record `5` as the score, as this _was_ the score when the event occurred.
The new score, which is the _result_ of the event, would be left for the `EventData` column.

In general, most `GameState` data could simply be inferred from past events.
For example, for any given event, the current level could be determined by looking for the most recent `new_level` event (or whatever name is chosen).
Thus, there is a tension between what data is useful to include in the `GameState`, and what context should simply be calculated as needed from past event data.
As a general heuristic, we include data that we believe to be useful for contextualizing all (or most) events in a given game (e.g. the current level), and exclude data that is only useful in specific cases (e.g. the number of attempts at a difficult task that exists only in level 5), leaving it to be inferred during post-hoc data analysis.

### `EventData`

This element is for all data that is wholly specific to an individual type of event.
Like the other "contextual" elements, `EventData` is a dictionary mapping string keys to values.
Unlike the other two, however, the set of keys is only constant across a single event type.
The sub-elements of `EventData` are so specific to an individual game's events that it is difficult to give general examples.
Instead, we'll illustrate a few possible events for a single hypothetical puzzle game, where players select and move blocks to solve a puzzle.

```json
{
   "EventName" : "select_puzzle_piece"
   ... (other columns)
   "EventData" : {
      "piece_id" : 3,
      "piece_type" : "SQUARE",
      "position" : [4, 0]
   },
   ...
} 

{
   "EventName" : "place_puzzle_piece"
   ... 
   "EventData" : {
      "piece_id" : 7,
      "piece_type" : "CIRCLE",
      "position" : [2, 5],
      "total_moves" : 27
   },
   ...
} 

{
   "EventName" : "complete_puzzle"
   ... 
   "EventData" : {
      "puzzle_id" : 5,
      "total_moves" : 32
   },
   ...
} 
```

Note that each type of event represented above has its own distinct set of keys, though there are many keys shared in common.
This is a common pattern.
Many different events will involve operations on the same set of in-game objects or variables, so the `EventData` keys for different event types will often be similar, sometimes even identical.

### OpenGameData Schema Files

The OpenGameData software uses a particular specification format to auto-generate documentation of a game's events.
You can read more about it in the [game schemas](../04_core-architecture/overview/game_schemas.md) page.

## Event Implementation

Once the events for a game have been specified, they should be implemented into the game via a logging package.
This step of Event Design should be considered a game engineering task; that is, implementation should generally be performed by a game engineer, rather than a data scientist.

As a game engineering task, it is helpful to consider aspects like efficiency and robustness at this stage of event design.
In particular, it is important to ensure event logging does not impact the user experience while playing the game.
Comprehensive error handling should be used to ensure logging system bugs or network issues do not crash or impact the game.
Similarly, if it is determined that the set of events and sets of context-data keys will require too much processing power or bandwidth for a given game, revisions to the _Event Specification_ may be required.

Other steps may be taken to improve the efficiency of logging, such as batching events to be sent as a single request to the logging server.
Certain elements of the OGD Event Schema are constant within a given gameplay session (such as `UserID`, `SessionID`, `AppVersion`, and `LogVersion`), and a logging implementation could avoid sending these with every single event individually, leaving the logging server to attach these IDs and versions to the individual events.

OpenGameData provides logging packages for Unity and JavaScript, as well as a PHP-based event "receiver" for the logging server.
For information on using these in a logging implementation, see the appropriate link(s) below.

* For Unity game projects : [opengamedata-unity documentation](https://github.com/opengamedata/opengamedata-unity/blob/main/README.md)
* For JavaScript-based game projects : [opengamedata-js-log documentation](https://github.com/opengamedata/opengamedata-js-log/blob/main/README.md)
* For event logging server : [opengamedata-logger documentation](https://github.com/opengamedata/opengamedata-logger/blob/master/README.md)

## Iteration

In general, event design is an iterative process.
After identifying, specifying, and implementing a set of events in a game, preliminary data should be collected and analyzed.
If there are any shortcomings in the data, such as missing events or events lacking sufficient context, a new iteration should be performed.
This consists of _identifying_ shortcomings of the current event set (or schema), _specifying_ changes to the schema to address the shortcomings, and _implementing_ the changes into the game's logging code.

## Best Practices & Naming Conventions

Below, we list some recommended practices and naming conventions.
These are, in general, arbitrary but reasonable, and are recommended to create consistency across game projects.

### Event Names

* Formatting:  
  We use a `snake_case` format for event names.
  (This is arbitrary and kinda dumb as a `PascalCase` or `CONSTANT_CASE` format would be far more consistent with our other coding conventions, but historically we used `snake_case` for almost all names in SQL. C'est la vie.)
* Name form:  
  All event types should be named with an object and a verb, with the order of the two used to help distinguish the event category.
    * **Player Actions** should have an "active" `verb_object` form, with a present-tense verb, such as `click_button`.
    * **System Feedback** events should have a "passive" `object_verb` form, with a past-tense verb, such as `dialog_displayed`.

### Context Data Elements

* Formatting:  
  We use a `snake_case` format for all keys in the context elements (`EventData`, `GameState`, and `UserData`).
  This is consistent with our general coding conventions, where variables use `snake_case` formatting.

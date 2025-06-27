# Event Schemas

This document covers the standard Open Game Data Event Schema, as well as how to design custom per-event schemas for specific parts of the `Event` data structure.

The OpenGameData Event Schema attempts to capture all relevant data for events across any genre of game in a way that maintains consistency from game to game, as well as compatibility with tabular forms of data storage and manipulation.
Any event will have a set of standard columns, with user-specific, game-specific, and event-specific data relegated to individual columns.
This tradeoff requires some additional work to parse sub-items, relative to a pure tabluar format, but ensures processing code a consistent interface across games.

The columns associated with each event loosely fall under 6 categories:

* Identification
* Timing
* Versioning
* User-Specific
* Game-Specific
* Event-Specific

The table below summarizes each category:

| Category       | Summary |
| ---            | ---     |
| Identification | These are columns used to identify the game, the individual player (where possible) and the session that generated an event |
| Timing         | These columns indicate when an event occurred, both in aboslute time and within a session |
| Versioning     | These columns are used to identify which version of a game, and which version of the game's logging schema, generated an event |
| Contextual     | This category is for any data whose format may vary across different games, events, or user profiling systems. It has sub-categories of user-specific, game-specific, and event-specific data. |

The `Event` class of `opengamedata-core` provides an interface for working with event data.
Each `Event` has a property corresponding to one column in the OpenGameData Event Schema.
The next table summarizes the actual columns and the properties exposing those columns in `Event` objects:

| Property           | Data Type   | Category       | Summary |
| ---                | ---         | ---            | ---     |
| AppID              | `str`       | Identification | An ID of the game that generated the Event. By convention, this is the name (or working title) of the game, in all-caps. For games with long titles, the AppID is generally shortened. For example, the Field Day Lab game *Wake: Tales from the Aqualab* has an AppID of `"AQUALAB"`. |
| UserID             | `str`       | Identification | An ID for an individual user of the game, tracked across multiple sessions of gameplay. **NOTE**: Not all games provide user IDs. |
| SessionID          | `str`       | Identification | The Session ID of the session that generated the Event. |
| EventName          | `str`       | Identification | The name of the specific type of Event that occurred. |
| Timestamp          | `datetime`  | Timing         | A UTC timestamp indicating the moment, according to the game instance, at which the event occurred. |
| TimeOffset         | `timedelta` | Timing         | The offset from GMT time (in the UTC `Timestamp` column) to the game client's local time zone. |
| EventSequenceIndex | `int`       | Timing         | An increasing integer index indicating the order in which events in a session occurred. That is, the first event in a session has EventSequenceIndex == 1, the next 2, 3, and so on. |
| AppVersion         | `str`       | Versioning     | A semantic versioning string (format `major.minor.revision`) indicating the version of the game itself that generated the event. |
| AppBranch          | `str`       | Versioning     | If the player was using a parallel branch of the game (for example, a version of the game identical to AppVersion 1.0.0, but with a specific reading skill questionnaire included for a study), the branch name can be set for this column (for example, `"ReadingSkillStudy"`). This saves effort in devising a way to fit parallel versions into a sequential versioning scheme. |
| LogVersion         | `str`       | Versioning     | A versioning string (preferably with semantic format `major.minor.revision`) indicating the version of the game's logging schema. This should increment any time a change is made to the add new types of event, remove existing events, or modify the sub-schemas of the user-, game-, or event-specific columns. |
| UserData           | `dict`      | Contextual     | A JSON-style dictionary for any data (other than ID) specific to a user. Typically, this would include profile data from systems that keep track of players across multiple games in the system. We generally avoid including elements in this column specific to a particular game or event, as this is often better-suited to the `GameState` or `EventData` columns. **NOTE**: As of October 2023, few if any games currently in the OpenGameData system use the `UserData` column. |
| GameState          | `dict`      | Contextual    | A JSON-style dictionary for any data (other than app ID) specific to a particular game. This is used to provide context for each specific event. For example, in a level-based puzzle game, the `GameState` column might include the current level and score. By convention, we record the state at the instant before the event occurred, and reserve any updated state values for the `EventData` column. For example, "current score" would be an element of `GameState`, common across all events, while "new score" would be an element of `EventData`, as it is specific to only those events that modify score. |
| EventData          | `dict`      | Contextual    | A JSON-style dictionary for any data (other than event name) specific to a particular type of event. This is used to indicate what, specifically, happened within a given event. For example, in a level-based puzzle game, the `EventData` for an event named `"place_tile"` might include the location and type of tile placed, as well as the new score on the level after placing the tile. |

## Event Tables

While the table above specifies all elements of the OpenGameData Event Schema, it may be helpful to visualize the data in tabular form, as the schema is designed for compatibility with tabular formats.
Given the list of elements above, then, a few example rows for a hypothetical puzzle game are given below.

| AppID     | UserID       | SessionID   | Event Name   | Timestamp          | TimeOffset     | EventSequenceIndex | AppVersion | AppBranch | LogVersion | UserData | GameState | EventData |
| ---       | ---          | ---         | ---          | ---                | ---            | ---                | ---        | ---       | ---        | ---      | ---       | ---       |
| "Puzzler" | "RedHerring" | "123456789" | "start_game" | 2021-01-01T12:34:56.789012 | +00:00 | 1                  | "1.2.3"    | "main"    | "1.0.0"    | { "system_player_id" : "user01234" } | { "level" : 0 } | {  } |
| "Puzzler" | "RedHerring" | "123456789" | "start_level" | 2021-01-01T12:34:57.000000 | +00:00 | 2                 | "1.2.3"    | "main"    | "1.0.0"    | { "system_player_id" : "user01234" } | { "level" : 0 } | { "new_level" : 1 } |
| "Puzzler" | "RedHerring" | "123456789" | "move_piece" | 2021-01-01T12:34:58.000000 | +00:00 | 3                  | "1.2.3"    | "main"    | "1.0.0"    | { "system_player_id" : "user01234" } | { "level" : 1 } | { "piece_id" : 5, "old_position" : [0, 3], "new_position" : [2, 3] } |
| "Puzzler" | "RedHerring" | "123456789" | "move_piece" | 2021-01-01T12:34:59.000000 | +00:00 | 4                  | "1.2.3"    | "main"    | "1.0.0"    | { "system_player_id" : "user01234" } | { "level" : 1 } | { "piece_id" : 2, "old_position" : [4, 1], "new_position" : [5, 2] } |
| "Puzzler" | "RedHerring" | "123456789" | "complete_level" | 2021-01-01T12:35:00.000000 | +00:00 | 5              | "1.2.3"    | "main"    | "1.0.0"    | { "system_player_id" : "user01234" } | { "level" : 1 } | {  } |
| "Puzzler" | "GreenGiant" | "987654321" | "start_game" | 2021-01-01T12:56:78.901234 | +02:00 | 1                  | "1.2.3"    | "new-ui"  | "1.0.0"    | { "system_player_id" : "user56789" } | { "level" : 0 } | {  } |

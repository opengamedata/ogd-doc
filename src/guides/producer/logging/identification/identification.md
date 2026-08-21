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

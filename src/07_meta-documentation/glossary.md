# Unit 7, Chapter 7: Glossary

This page contains some important terminology for OpenGameData.
Refer here if you are uncertain what a particular term means.

- **Event**:
  A record of some game event, stored as a single row in the database.  

- **feature**:  
  Some *metric* or other piece of *data*, useful for analysis, that we can observe from gameplay event logs.
  For example, a feature could be as simple as a boolean representing "player started level 1."
  On the other hand, a feature could be very complex, such as a string encoding the entire sequence of a gameplay session.
  In OpenGameData, we write implementations of an abstract `Feature` class, where each implementation calculates a feature given event logs as input.  
- **Feature**:  
  The code that extracts a "feature" from event logs.  

Features may be calculated at varying levels of analysis, described in the following definitions:

- **per-session feature**:  
  A feature that is calculated for an entire gameplay session.
- **per-custom-count feature**:  
  A feature that may have multiple instances over a gameplay session.
  This could include levels, survey prompts, in-game quizzes, etc.  
  *For example*: A feature may be "clicks in the level", and there are 20 levels
- **per-level feature**:  
  A per-custom-count feature that specifically has one instance for each level in a game.  
  This is a sort of "informal" feature in OpenGameData - there are special bits available in OpenGameData to make Feature development easier for games that include a notion of "level," but these are optional.  
- **population feature**:  
  A feature that records data across many sessions of gameplay.  

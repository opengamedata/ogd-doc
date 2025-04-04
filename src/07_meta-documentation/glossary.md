# Unit 7, Chapter 7: Glossary

This page contains some important terminology for OpenGameData.
Refer here if you are uncertain what a particular term means.

Note, the list below uses "user" terminology to decribe the terms - in general, the terminology below applies equally to "sessions" and "populations" as well.

- **event**:
  A record of some game event, stored as a single row in the database.  
- **Event**:
  A record of some game event, whose structure conforms to the OpenGameData **Event** standard.
- **Detector**:
  A module of code that "detects" certain user behaviors, based on the user's event stream, and inserts new "generated" events into the stream.
  In OpenGameData, we write implementations of an abstract `Detector` class, where each implementation generates new events given event logs as input.  
- **feature**:  
  Some *metric* or other piece of *data*, useful for analysis, that we can observe from gameplay event logs.
  _For example_, a feature could be a simple boolean representing whether "the player started level 1."
  On the other hand, a feature could be complex, such as a string encoding the entire sequence of a gameplay session.
- **Feature**:  
  A record of some feature, whose structure conforms to the OpenGameData **Feature** standard.
- **Extractor**:  
  A code module that "extracts" **Feature** values from the user's event stream, and returns that value to be associated with the user.
  In OpenGameData, we write implementations of an abstract `Extractor` class, where each implementation calculates a feature given event logs as input.  

Features may be calculated at varying levels of analysis, described in the following definitions:

- **Aggregate Feature**:  
  A **Feature** that is calculated and yields one value across an entire session, user, or population event stream.
- **Unitized Feature**:  
  A **Feature** that is defined for some _unit_ of gameplay within a game, such as levels, survey prompts, in-game quizzes, etc.  
  Then there is one instance of the **Feature** for each instance of the unit.
  *For example*: A feature may be "clicks in the level", with one instance for each of 20 in-game levels.
- **Per-Level Feature**:  
  An **Unitized Feature** that specifically has one instance for each level in a game.  
  OpenGameData makes a special base module available to allow easier **Feature** engineering for games that include a notion of "level," but its use is optional.  
- **Population Feature**:  
  A **Feature** (whether _aggregate_ or _unitized_) that is extracted from data across many sessions of gameplay.  
  By default, all **Feature**s can be extracted at the session, player, _and_ population levels; however, features that perform special accounting for multiple players (e.g. a feature that yields a distribution of values) can be marked as population-only.

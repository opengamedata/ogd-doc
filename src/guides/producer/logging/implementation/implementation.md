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

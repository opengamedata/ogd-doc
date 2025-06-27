## OpenGameData Logger and Logging Clients

OpenGameData provides packages for logging events from game clients, and a PHP logger script to receive these events and place them into a database.

### Client-Logger Communications

The logging clients communicate with the logger script via HTTP POST requests.
These use request parameters for data that is constant within a gameplay session, such as versioning and identifier variables, and a base-64-encoded body for data that varies per-event.
This allows the system to support packaging multiple events into a single request for games that either log events frequently or experience poor internet connections.

In particular, the following parameters are included in the header of each request:

1. `app_id`: identifier for given app, should match the game's name in the database
2. `app_version`: the current version of the app
3. `app_branch`: (optional) the branch of the app
4. `log_version`: the current version of the app's logging code/schema
5. `session_id`: a unique ID for the current game session
6. `user_id`: (optional) the player's personal ID
7. `user_data`: (optional) gives further data associated with player ID

Then the POST URL for a given request will have the following form:

`https://hostname.com/path/to/log.php?app_id={1}&app_version={2}&app_branch{3}&log_version{4}&session_id={5}&user_id={6}&user_data={7}`

The body of the request, as mentioned above, is base-64 encoded.
The encoded data is an array, containing one or more JSON-style dictionaries, each containing data for a single event.
The elements of these dictionaries are as follows:

- `client_time`: client's timestamp resolved to the second
- `client_offset`: offset of client's local time from UTC
- `event_name`: the type of event logged
- `event_data`: a JSON string containing all the logged information
- `game_state`: a JSON string containing information about the state of the game when the event occurred
- `event_sequence_index`: integer that increments with each log, showing the true order of the logs

These are decoded by the logger script, and recombined with the parameter items to form full events for storage into the configured database.

### `opengamedata-unity`

The OGD client for the Unity game engine is developed and maintained at GitHub.
Documentation on its use is included in the repository README.
You can access it at the following URL: [https://github.com/opengamedata/opengamedata-unity](https://github.com/opengamedata/opengamedata-unity)

If you wish to use the `opengamedata-unity` package, you can install it in your project from OpenUPM.
The package page can be accessed at [https://openupm.com/packages/com.fieldday.opengamedata-unity](https://openupm.com/packages/com.fieldday.opengamedata-unity/)

### `opengamedata-js-log`

The OGD client for general JavaScript projects is also maintained at GitHub, along with README documentation.
You can access it at the following URL: [https://github.com/opengamedata/opengamedata-js-log](https://github.com/opengamedata/opengamedata-js-log)

To use the `opengamedata-js-log` package, you can install it in your project from NPM.
The package can be accessed at [https://www.npmjs.com/package/opengamedata-js-log](https://www.npmjs.com/package/opengamedata-js-log)

### `opengamedata-logger`


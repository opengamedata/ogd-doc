# Introduction for Game Studios

This document outlines the steps necessary to integrate a new game with the Open Game Data infrastructure.

The OGD pipeline is made up of the following steps:

1. **Game Client Logging**
2. **Data Storage**
3. **Data Transformations**  
    a. New Event Detection  
    b. Feature Extraction  
    c. (*future work*) Model Training  
4. **Monthly Outputs**

We provide various Open Game Data packages for use in each step of this process; you may freely use these, or substitute your own solution in for a given step.
If you are only interested in event logging, the data transformations step may be ommitted from your project.

## Game Client Logging

In this step of the pipeline, the game sends out telemetry events to be captured in a database.
The steps needed to implement this part of the pipeline are:

1. [Identify and Design Game Events](#identify-and-design-game-events)
2. [Implement Events](#implement-events)
3. [Gameplay Testing](#gameplay-testing)
4. [Documentation](#documentation)
5. [Iteration](#iteration)

We'll describe these steps in more detail below.

### Identify and Design Game Events

- Description: Choose the events to be logged, and design the structure of the data to be sent with each event.
- Time Required: 1-4 hours, depending on the size/complexity of the game

In this very initial step, you will identify the events in your game, describe the data that belongs to each event, and document that description for later implementation.
These events should be chosen to allow post-hoc reconstruction of gameplay.
Please see [Event Design](./event_design.md) for more information about choosing which events to log.
If your game already implements some form of event logging, you may continue with your existing set of events, and simply port them to the Open Game Data system.

To maintain consistency of data across games, we use a standardized schema for events.
If you use one of the logging packages provided by OpenGameData, this schema will be implicitly enforced; if you use a custom logging solution, we highly recommend following the standardized schema for maximum compatibility.
Please see [Open Game Data Event Schemas](./event_schema.md) for more details.

### Implement Events

- Description: Implement logging for each event within the game code.
- Time Required: 1-3 working days, depending on the size and complexity of the set of events to implement.

Once you have determined a set of events and the data to be logged with them, you will need to implement logging within your game. We recommend using one of the Open Game Data packages to ease this process.
We currently have packages for Unity and JavaScript game projects.
To get started, please see the readme guide for the package appropriate for your game:

* For Unity: `opengamedata-unity` user's [guide](https://github.com/opengamedata/opengamedata-unity#readme)
* For JavaScript: `opengamedata-js-log` user's [guide](https://github.com/opengamedata/opengamedata-js-log#readme)

**Note** : If your implementation uses the Open Game Data logging servers, a table will need to be created for your game during this step.
This will include a database table on the main production server and optionally the CI/testing server.

### Gameplay Testing

- Description: Test the logging implementation, recording any bugs that may have been created.
- Time Required: Varies, likely 1-2 working days

After implementing new event logging in a game, the implementation should be tested for correctness and completeness.
In particular, you should ensure the following:

- The logging implementation does not lead to crashes in the game
- The logging implementaiton does not create performance issues in the game, such as slow framerates.
- Events are successfully sent to the logging server (see the [event monitoring guide](./event_monitor.md) for more information).
- Events have the correct content.

### Documentation

- Description: Produce documents formalizing and describing the event implementation.
- Time Required: 1-2 working days, depending on the number of events implemented

Strictly speaking, progress on this step can be made at any time after step 1.
Once the set of events has been agreed upon, formal documentation can begin.
There are two pieces of documentation we recommend:

1. Game project `readme` file

    This refers to a readme file included with the game source.
    The readme may contain other information, depending on the needs of the game project.
    In either case, this file should include semi-formal documentation of the events logged by the game.
    By "semi-formal," we mean the documentation should at least include the names of all events and a listing of the specific data included with each event type, but details of format and any supporting text are left to the writer.

2. `GAME_ID.json` file in `opengamedata-core`

    This refers to a specific `json` file for use within `opengamedata-core`.
    Among the uses of this file are automatic generation of a dataset readme file whenever data is exported via `opengamedata-core`.
    This is a formal documentation of events, in the sense there is a very specific format to use, with a prescribed set of elements to be listed for each type of event.
    Details are in the documentation of [game schemas](../04_core-architecture/overview/game_schemas.md).

Both of these documents are important points of reference.
In general, the `readme` file is useful for reviewing the state of logging and onboarding any new developers who may need to interact with the logging code, while the `json` file is useful as a specification of what should be implemented (where the documents differ, the `json` should be treated as the target, and the `readme` updated to reflect any fixes to the implementation).

### Iteration

- Description: Iterate on steps 1-4 (updating event definitions, implementing changes, testing) until satisfied with implementation.
- Time Required: Per iteration, 30 minutes updating definitions, 2 hours implementing changes and updating documentation, 2 hours testing changes is typically a reasonable rate, number of iterations required varies widely.

Once all steps have an initial implementation, the process should be repeated iteratively to fix issues with the initial implementation.
Further iterations are also recommended if and when the game changes significantly.
"Significantly" is intentionally vague as there are no hard-and-fast rules for all games to determine when updates to logging are needed.
A general guideline is that changes to game content typically do not require changes to logging, but changes to game structure do.
For example, the addition or removal of game levels may not require changes to logging, but the introduction of a new mechanic or removal of a UI button almost always require updates to logging.

**Note** : It is strongly recommended to increase the `log_version` logged by the game whenever a new release includes changes to event logging.

## Data Storage

Once you have implemented logging in your game, you'll need a database to receive and store the logged events.
In principle, any table-based database system may be used to record Open Game Data events; in practice, we have ready support for MySQL as a short-term container for new events, and for BigQuery for long-term archival of older events. Logging to another database system may require some additional development effort.

If you wish to utilize our existing logging infrastructure to capture your game events, please [contact us](TODO) to discuss integration with our instance of the OGD logging system.

If you prefer to create your own instance of logging infrastructure, there are two major steps to complete.
These are:

1. Set up logging to MySQL short-term database
2. Set up automatic archival to BigQuery.

### Logging to MySQL

This major step can be accomplished by doing the following:

1. Set up a "logging" server with PHP and MySQL:  
    This server will host the logging service.
    Please see our [reference platform](../07_meta-documentation/software_platform/software_platform.rst) documentation for recommended software versions.
2. Create a MySQL database to hold game events:  
    This database should contain a table for each game, with each table having columns and data types corresponding to the OGD schema
3. Set up an instance of `opengamedata-logger` package:  
    This repository contains PHP scripts to receive a request containing event data, and insert the data into a local database.
    The config file should be set with credentials for writing to the MySQL database.
    The [readme](https://github.com/opengamedata/opengamedata-logger#readme) may be useful for understanding how `opengamedata-logger` works.  
4. Direct game logging client to your server:  
    If you used `opengamedata-unity` or `opengamedata-js-log` for event logging, you can configure the package to make requests through your server's instance of the PHP scripts.

### Archiving to BigQuery

This step can be accomplished by doing the following:

1. Create a Google Cloud project to host game data
2. Create a BigQuery project:  
    This project should, in turn, have datasets for each game, and each dataset should have tables with columns and data types corresponding to the MySQL schema.
3. Use `opengamedata-automation` to automatically archive data from MySQL to BigQuery

## Data Transformations

### Event Detectors

### Feature Extractors

## Monthly Outputs
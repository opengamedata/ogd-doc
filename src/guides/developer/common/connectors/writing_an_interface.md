## Writing an `Interface`

All interfaces inherit from an `Interface` base class, which in turn inherits from `StorageConnector`.
Thus, each interface must implement the functions required by its base classes.

### `StorageContainer` Functions

First, `StorageConnector` subclasses must implement an `_open` and `_close` function for connecting to and disconnecting from a corresponding storage resource (such as a file or database).
Typically, this is as simple as importing and using an appropriate package for the resource you want to connect to.
For example, the `MySQLEventInterface` imports the following:

```python
from mysql.connector import connection, cursor
```

It then uses the imported `connection` module to establish and close connections to a MySQL database.

### `Interface` Functions

Second, every `Interface` subclass must implement functions to allow a user to first collect some information on the data contained in the connected resource.

## Work In Progress below

Mostly this is for Events, but we also will allow reading Features.
Their functions allow querying of the ID, version, and timing information available in the source.

In particular, they have the following functions:

* AvailableIDs - gets list of session or player IDs available, subject to date and version filters
* AvailableDates - gets range of dates, subject to ID and version filters
* AvailableVersions - gets list of log or app versions available, subject to ID or date filters

These functions allow higher-level logic to pre-check what's available before loading it.

### Event & Feature Interfaces

These define actual data retrieval.

They have the following function:

* GetEventCollection - takes an EventTableSchema, gets a collection of events, subject to ID, date, and version filters; only ID filter is required. Generally a good idea to use other filtering at AvailableIDs step to get session/player IDs, rather than trying to re-filter here, but option is available.
* GetFeatureCollection - takes FeatureTableSchema, gets a collection of feature data objects, subject to ID, date, and version filters.

### Event & Feature Outerfaces

These define how to send data out of the system.



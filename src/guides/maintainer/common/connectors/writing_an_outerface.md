## Writing an `Outerface`

In the `opengamedata-core` code, the `DataOuterface` base class is itself a subclass of the `Interface` base class.
Thus, like any `Interface`, it must implement the `_open` and `_close` functions.
In addition, `DataOuterface` adds its own set of abstract functions for implementing the writing of data.
We'll discuss this in greater detail below.

### `__init__` Data

The `DataOuterface` base class is initialized from two objects, a `GameSourceSchema` and a set of `ExportMode`s:

```python
  def __init__(self, game_id, config:GameSourceSchema, export_modes:Set[ExportMode]):
```

The `GameSourceSchema` and `ExportMode` set can be accessed by `self._config` and `self.ExportModes`, respectively (to modify the modes, you should use the private data member `self._modes`)
You can optionally add parameters for your `DataOuterface`'s constructor, but this is generally not recommended as there is no built-in way to ensure the values of those parameters can be set in a config file.

#### The `GameSourceSchema`

The `GameSourceSchema` class contains four pieces:

* A `DataHostConfig` object, (`self._config.DataHost`) which includes the location and credential information needed to access a data host, such as a database or file system.
* A database name (`self._config.DatabaseName`) and table name (`self._config.TableName`), which can be used for cases where the data host is a database system, to locate the data once the config information has been used to establish a connection.
  These can be ignored for cases where they are not applicable, such as when the data host is just a local file.
* A `TableSchema`, which indicates what columns are available in the format supported on the data host (such as the columns of the specific database table indicated by `self._config.TableName`), and how those columns map to the elements of the specific data type handled by the `DataOuterface`.

When writing a `DataOuterface` subclass, you do not need to directly interact with the `TableSchema`, but the `DataHostConfig` and (optionally) database/table names will be used in your code for connecting to the game source.

The set of `ExportMode` enum objects indicates which types of data output have been requested.
You typically will not need to interact directly with this set, but in some cases it may be useful.
Specifically, if you are writing a `DataOuterface` for a file system, you can elect to open only the files corresponding to the requested output modes.

### Implementing the `Interface` Functions

The `Interface` base class defines abstract functions `_open` and `_close`.
These must be implemented by each new interface or outerface.

```python
    def _open(self) -> bool:

    def _close(self) -> bool:
```

These functions are simple in concept but nontrivial in implementation.
The `_open` function should create and store (as an element of `self`) an open connection to the `DataHost`, and `_close` should close that connection.

#### The `_open` function

Practically, `_open` should use whatever Python package is available for communicating with the given database or file type, and return `True` if the connection was opened without errors.
In case of errors, it is acceptable to simply raise an error and let the system cancel the data export, though if there are any means to retry a connection, we recommend implementing a short retry loop of up to 5 retry attempts.
It is also acceptable to print a reasonable error message and return `False`.

As discussed above, the `DataHostConfig` should contain the location and any necessary credentials to open a connection.
The specific instance received should be from a subclass of `DataHostConfig` specific to the system for which you are writing a `DataOuterface`.
Refer to that class' interface to see what data members are available.
If no such class exists, it may need to be written before the `DataOuterface` can be fully implemented.

If you are writing a `DataOuterface` that needs separate connections for each type of output (e.g. outputting to static files), you can use `self.ExportModes` to determine which connections to open.

#### The `_close` function

Like `_open`, the `_close` function should return `True` if the connection to the data host was terminated without errors.
In case of errors, we prefer to handle within the `_close` function rather than raising an error to a higher level, although raising an error is acceptable.

### Implementing the `DataOuterface` Functions

The `DataOuterface` base class defines a significant number of abstract functions to be implemented.
These cover five different kinds of output:
1. "Raw" events
2. "Processed" events
3. "Session" features
4. "Player" features
5. "Population" features

From an implementation perspective, there is little to no difference in how "raw" and "processed" events are output, nor is there typically any difference between outputting "session", "player", and "population" features.
The primary difference is that, in several cases (such as outputting data to files), it is useful to separate these kinds of data into different output locations.
Thus, while it is not necessarily the most efficient organization of functions, we implement one function for each kind of output, where the functions within the event and feature categories are largely identical to one another.

```python
    def _destination(self, mode:ExportMode) -> str:

    def _removeExportMode(self, mode:ExportMode) -> str:

    def _writeRawEventsHeader(self, header:List[str]) -> None:

    def _writeProcessedEventsHeader(self, header:List[str]) -> None:

    def _writeSessionHeader(self, header:List[str]) -> None:

    def _writePlayerHeader(self, header:List[str]) -> None:

    def _writePopulationHeader(self, header:List[str]) -> None:

    def _writeRawEventLines(self, events:List[Event]) -> None:

    def _writeProcessedEventLines(self, events:List[Event]) -> None:

    def _writeSessionLines(self, sessions:List[List[FeatureData]]) -> None:

    def _writePlayerLines(self, players:List[List[FeatureData]]) -> None:

    def _writePopulationLines(self, populations:List[List[FeatureData]]) -> None:
```
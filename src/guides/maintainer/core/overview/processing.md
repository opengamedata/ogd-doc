## Data Processing

### Requests

The `Request` class contains data defining a set of data to export, the set of generators to use, and the outputs.
In particular, it has the following properties:

| Property       | Description |
| ---            | ---         |
| `GameID`       | The game whose data will be exported |
| `Interface`    | The interface for accessing the data |
| `Range`        | The set of dates, session IDs, or player IDs to be retrieved from the interface for export |
| `Outerfaces`   | A set of outerfaces, where exported data will be sent |
| `Export[Type]` | [Type] is any of `RawEvents`, `ProcessedEvents`, `Sessions`, `Players`, or `Population`. Each is a boolean indicating whether that type of data should be output to the outerfaces |

### Export Manager

The processing of data begins at the `ExportManager` class.
This class is responsible for overseeing the execution of given `Request` instances;
most of the actual work is delegated down to lower-level managers.
The work done directly by `ExportManager` consists of pre-processing, processing, and post-processing phases.

#### Pre-processing

This phase mostly consists of opening the outerfaces and setting up the other managers for delegation.
The `ExportManager` also attempts to locate the `[Game]Loader` class for the game whose data is being exported, if the loader class exists.

#### Processing

#### Post-processing

### Event Manager

### Feature Manager

Keeps a `PopulationProcessor`, plus `PlayerProcessor`s for each player ID encountered in the dataset, and `SessionProcessor`s for each session ID.

### Processors

At their most basic, all processors simply have a game schema, process events, and return lines.

#### Generator Processors

Processors for generators add a loader class, an instantiation of that loader, and a registry.

### Registries

### Generators

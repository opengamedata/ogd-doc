## Overview of `Config` and `Schema` Classes in OGD-Common Library

This section will give an overview of the categories and class hierarchies of each config and schema class in the `opengamedata-common` Python library, which we will also refer to informally as OGD-Common or Common, for short.

In order to manage configuration data, as well as descriptions of the configuration or structure of external data and data sources, OpenGameData uses a broad collection of classes called `Schema`s.
Within this broad collection is a subcategory of classes called `Config`s.

The distinction between these groups is as follows:

* `Config` classes are used for the case of data related to the configuration of an OpenGameData tool.
    This may include things like the location of a local file for writing, or the credentials to access a database.
* `Schema` classes are used for any other case where data related to external data or tools are needed.
    This may include things like descriptions of events logged by a particular game, or the mapping of columns from an external data source to the internal structure used by OpenGameData.

### Examples Uses of `Config` and `Schema`

The two clearest, most practical examples of this distinction relate to data connections, and feature extraction:

1. **Data Connections** : `ogd-common` uses `StorageConnector` subclasses, discussed in the chapter on "Interfaces," to connect to data stores either to import or export data.
    Data stores may include a local file, an external file host, or a database:

    ```{mermaid}
    ---
    title: Basic Data Stores
    ---
    flowchart TD

    StorageConnector --> local[(Local File)]
    StorageConnector --> remote[(Remote Fileserver)]
    StorageConnector --> Database[(Database)]
    ```

    However, each data store might in turn contain multiple resources, such as files or database tables.
    To handle this, there are several classes of the `Config` variety that handle the configuration of a `StorageConnector`, such as the location and credentials to access a given data storage resource.
    On the other hand, the location and table structure of individual resources _within_ a data store are properties of that external store, thus they are handled with classes of the `Schema` variety.
2. **Feature Extraction** : The writing and execution of feature extractor modules requires both a knowledge of the event types logged by a game, and a way to specify which extractor modules to execute.
    Both the game-defined events and executed extractor modules are included in the `README.md` files included with each data export.
    Classes of the `Schema` variety are used for managing the specifications of game events, and `Config` classes are used to manage the specification of extractor modules.

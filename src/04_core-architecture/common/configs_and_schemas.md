## `Config`s and `Schema`s

In order to manage configuration data, as well as descriptions of the configuration or structure of external data and data sources, OpenGameData uses a broad collection of classes called `Schema`s.
Within this broad collection is a subcategory of classes called `Config`s.

The distinction between these groups is as follows:

* `Config` classes are used for the case of data related to the configuration of an OpenGameData tool.
    This may include things like the location of a local file for writing, or the credentials to access a database.
* `Schema` classes are used for any other case where data related to external data or tools are needed.
    This may include things like descriptions of events logged by a particular game, or the mapping of columns from an external data source to the internal structure used by OpenGameData.

The two clearest, most practical examples of this distinction relate to data connections, and feature extraction:

1. **Data Connections** : `ogd-common` uses `StorageConnector` subclasses, discussed in the chapter on "Interfaces," to connect to data storage resources either to import or export data.
    Resources may include a local file, an external file host, or a database:

    ```{mermaid}
    flowchart LR

    StorageConnector --> local["Local File"]
    StorageConnector --> remote["Remote Fileserver"]
    StorageConnector --> Database
    ```

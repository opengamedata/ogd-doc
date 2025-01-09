## `Config`s and `Schema`s

In order to manage configuration data, as well as descriptions of the configuration or structure of external data and data sources, OpenGameData uses a broad collection of classes called `Schema`s.
Within this broad collection is a subcategory of classes called `Config`s.

The distinction between these groups is as follows:

* `Config` classes are used for the case of data related to the configuration of an OpenGameData tool.
    This may include things like the location of a local file for writing, or the credentials to access a database.
* `Schema` classes are used for any other case where data related to external data or tools are needed.
    This may include things like descriptions of events logged by a particular game, or the mapping of columns from an external data source to the internal structure used by OpenGameData.

The two clearest, most practical examples of this distinction relate to data connections, and feature extraction:

1. **Data Connections** : `ogd-common` uses `StorageConnector` subclasses, discussed in the chapter on "Interfaces," to connect to data stores either to import or export data.
    Data stores may include a local file, an external file host, or a database:

    ```{mermaid}
    flowchart TD

    StorageConnector --> local[(Local File)]
    StorageConnector --> remote[(Remote Fileserver)]
    StorageConnector --> Database[(Database)]
    ```

    However, each data store might in turn contain multiple resources, such as files or database tables:

    ```{mermaid}
    flowchart TD

    StorageConnector --> remote[(Remote Fileserver)]
    remote[(Remote Fileserver)] -.-> file1.tsv
    remote[(Remote Fileserver)] -.-> file2.tsv
    remote[(Remote Fileserver)] -.-> file3.tsv
    StorageConnector --> Database[(Database)]
    Database[(Database)] -.-> database1
    database1 -.-> table1
    database1 -.-> table2
    Database[(Database)] -.-> database2
    database2 -.-> table3
    ```

    To handle this, there are several classes of the `Config` variety that handle the configuration of a `StorageConnector`, such as the location and credentials to access a given data storage resource.
    On the other hand, the location and table structure of individual resources within a data store are properties of that external store, thus they are handled with classes of the `Schema` variety.
2. **Feature Extraction** : The writing and execution of feature extractor modules requires both a knowledge of the event types logged by a game, and a way to specify which extractor modules to execute.
    Both the game-defined events and executed extractor modules are included in the `README.md` files included with each data export.
    Classes of the `Schema` variety are used for managing the specifications of game events, and `Config` classes are used to manage the specification of extractor modules.

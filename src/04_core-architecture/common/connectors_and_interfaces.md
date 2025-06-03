## `Connector`s, `Interface`s, and `Outerface`s

### Overview

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

However, each data store might in turn contain multiple resources, such as files or database tables:

```{mermaid}
---
title: Detailed Data Stores
---
flowchart TD

StorageConnector --> local[(Local File)]
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

### `StorageConnector` and subclasses

OpenGameData uses classes called `StorageConnector`s to establish connections to data stores.
Further, `Interface` and `Outerface` classes are used for data input and output, where an `Interface` class has specific functions for retrieving data from a store, and an `Outerface` has functions for writing data to a store.
For any given storage medium, then, there may be a `Connector`, `Interface`, and `Outerface` class:

```{mermaid}
---
title: Storage Connector Hierarchy
---
classDiagram
StorageConnector <|-- MySQLConnector
Interface <|-- MySQLInterface
MySQLConnector <|-- MySQLInterface
MySQLConnector <|-- MySQLOuterface
Outerface <|-- MySQLOuterface
```

File input and output via `Interface` and `Outerface` classes is significant enough to deserve a chapter of its own.
Thus, please refer to Unit 4, Chapter 3: Interfaces and Outerfaces for details.

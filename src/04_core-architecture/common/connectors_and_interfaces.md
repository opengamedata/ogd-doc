## `Connector`s, `Interface`s, and `Outerface`s

OpenGameData uses classes called `StorageConnector`s to establish connections to data stores.
Further, `Interface` and `Outerface` classes are used for data input and output, where an `Interface` class has specific functions for retrieving data from a store, and an `Outerface` has functions for writing data to a store.
For any given storage medium, then, there may be a `Connector`, `Interface`, and `Outerface` class:

```{mermaid}
classDiagram
StorageConnector <|-- MySQLConnector
Interface <|-- MySQLInterface
MySQLConnector <|-- MySQLInterface
MySQLConnector <|-- MySQLOuterface
Outerface <|-- MySQLOuterface
```

File input and output via `Interface` and `Outerface` classes is significant enough to deserve a chapter of its own.
Thus, please refer to Unit 4, Chapter 3: Interfaces and Outerfaces for details.

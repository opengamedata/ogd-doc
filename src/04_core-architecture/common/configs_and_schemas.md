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

    To handle this, there are several classes of the `Config` variety that handle the configuration of a `StorageConnector`, such as the location and credentials to access a given data storage resource.
    On the other hand, the location and table structure of individual resources _within_ a data store are properties of that external store, thus they are handled with classes of the `Schema` variety.
2. **Feature Extraction** : The writing and execution of feature extractor modules requires both a knowledge of the event types logged by a game, and a way to specify which extractor modules to execute.
    Both the game-defined events and executed extractor modules are included in the `README.md` files included with each data export.
    Classes of the `Schema` variety are used for managing the specifications of game events, and `Config` classes are used to manage the specification of extractor modules.

### Schema Classes in OGD-Common Library

This section will give an overview of the structures of each schema class in the `opengamedata-common` Python library, which we will also refer to informally as OGD-Common or Common, for short.

#### `Schema`

This is the base class for all `Schema` and `Config` classes in Common.
It defines the following abstract functions for all other `Schema` and `Config`s to implement:

* `AsMarkdown` : A property returning a markdown-formatted string summarizing the `Schema` subclass data.
* `FromDict` : A function to instantiate the `Schema` subclass from a JSON-style dictionary.
* `Default` : A function to generate a default instance of the `Schema` subclass.

`Schema` also provides the following utility functions as part of the interface for all its subclasses:

* `FromFile` : A simple function to instantiate the `Schema` class/subclass from a file, assumed to contain a JSON-style dictionary.
    It invokes a `_fromFile` private function whose default implementation assumes a file with `.json` extension, and JSON-style formatting of the file contents.
    `Schema` subclasses that are meant to be loaded from other file formats may overload the `_fromFile` function.
* `ParseElement` : A utility function that retrieves a specified element from a dictionary of yet-unparsed schema elements, utilizing the `conversion` module functions in `ogd.common.utils.type` to ensure the retrieved value has been converted to the desired type.
    * `ParseElement` also allows for multiple candidate keys to be given for the element, in order to support 'legacy' formats.
        For example, if an older specification had an element with key `"DB"` and a newer specification uses `"DATABASE"`, the old key name can be used as a fallback in case the newer key is missing.
    * Further, `ParseElement` supports multiple candidate types to be given for the element, in order to support formats that allow different kinds of data to be used for the same key.
        For example, if a "range" element is allowed to be either a 2-element list or 2-element tuple of ints, both `List` and `Tuple` can be given for the type.

Structurally, the `Schema` base class only stores a schema name and a dictionary of "non-standard elements."
When a `Schema` subclass is instantiated from a JSON-style dictionary with the FromDict or FromFile functions, any elements not used by classes in the inheritance chain go into the "non-standard elements."
Both the name and non-standards are accessible outside the class via properties:

* `Name`
* `NonStandardElements`
* `NonStandardElementNames`

#### `TableSchema`

This class stores a location and structure for a database table containing feature or event data.
These are each stored using component `Schema` subclasses, which are accessed by properties:

* `Structure` : A `TableStructureSchema` subclass, either `EventTableStructureSchema` or `FeatureTableStructureSchema`, which have differing elements based on which columns are in the respective standard elements for Events and Features.
    For full details on these differences, read the unit 2 section on event schemas and the unit 3 section on feature data
    <font style='color:tomato'>TODO: Link to the sections (note the unit 3 section is not yet written).</font>  
* `Columns` : The `Columns` specifications stored within the `Structure` object - this is provided for convenience of access.
* `Location` : A `TableLocationSchema`, or a subclass.
    This contains information on how a table is accessed within a resource, via a `StorageConnector`.
    For example, a `StorageConnector` may be configured with a `DataStoreConfig` to grant access to a database, and the `TableLocationSchema` contains information on where the given table is located within the database.

##### Table Structures vs. Data Structure Specifications

In order to understand the functionality of the schema classes that manage table structures, it is important to make a distinction between the use of the terms "table" and "data structure" for this discussion.

OpenGameData tools use internal representations of events and features.
These each have specifications, which are given elsewhere.
<font style='color:tomato'>TODO: Link to the specs, wherever we have them right now.</font>  
We will refer to these internal representations as the **data structures**, and the individual pieces of data within those **structures** as **elements**.

On the other hand, game data is stored in files, databases, or other table-based (tabular) formats.
We call these **data tables**, and each **data table** is made up of **columns**.

In a perfect world, the structure of all **data tables** would match our **data structures**

It is useful to think of **data structures** in this context as ideal abstractions of events and features, and of **data tables** as the concrete, real-world implementations.
Then in order for OpenGameData tools to operate on any data, we need a way to use the **columns** of **data tables** to fill the **elements** in an instantiation of the corresponding **data structures**.

##### `TableStructureSchema`s

The `TableStructureSchema` base class is meant, via its subclasses, to store information about the structure of a table storing game data.
Table structures can be complicated to manage, because over time and across organizations, the details of columns in data tables may vary.
This could be due to changes in the data structure specification (e.g. an element of the structure is removed in newer specs), or due to porting an existing system to operate with OpenGameData (e.g. an existing system contains elements in its structure that are not found in the spec).
These issues become apparent when column sets differ across data tables.

The `TableStructureSchema` classes allow us to:

1. Document the columns of the source data table
2. Define a mapping of data table **columns** to data structure **elements**.  
    This is an important distinction.
    Tables have **columns**, which are real-world and vary over time and across organizations.
    The specification of an OGD `Event` or `FeatureData` has **elements**, and OGD will always use the latest specification internally.
    Thus, we have this mapping to indicate how the literal table columns should be used to construct instances of OGD's internal data structures.

In fact, these correspond the exact structural data available from a `TableStructureSchema`, or any of its subclasses, via properties:

* `Columns` : A `List` of `ColumnSchema` objects. While `ColumnSchema` is not given its own section here, these are simply schemas whose own structural elements are as follows:

    * `ReadableName` : A human-readable version of the column name - the `Name` property provided by the `Schema` base class will contain the actual name of the column within the data table.
    * `Description` : A simple text description of what data the column stores.
    * `ValueType` : The data type stored in the column.

    The `ColummnSchema` class does nothing else special or unique - it simply makes the specification of a real-world column's contents available.
* `ColumnNames` : A list of all the `Name` values from the `ColumnSchema`s given by the `Columns` property. Note this is _not_ a list of the `ReadableName` values.
* `ColumnMap` : A mapping from element names to `ColumnMapIndex` values.
    `ColumnMapIndex` is simply an alias for a value that could be an `int`, a `List[int]`, a `Dict[str, int]`, or `None`.
* Other Properties : The class also has a series of properties for accessing individual parts of the column mapping.
    For each **element** common to event and feature data structures, there is a pair of properties.
    These are the "index" and "column" props, named like `<ElementName>Index` and `<ElementName>Column`.
    The "index" property gets the `ColumnMapIndex` for the element, indicating which column(s) of the table is/are mapped to the element.
    The "column" property gets the _name_ of the column mapped to the element, or string with comma-separated names of the column.
* `_fromDict` Abstract Function : Finally, `TableStructureSchema` implements a `FromDict` function, allowing it to handle construction of the data it holds.
    In turn, it defers to its subclasses to implement a new abstract function called `_fromDict`, which is meant to handle parsing for the specific data added by subclasses.

##### `EventTableStructureSchema` and `FeatureTableStructureSchema`

These subclasses of `TableStructureSchema` add more properties for the specific elements of their data structures.

In addition, they implement the abstract functions for `AsMarkdown` and `Default`, which `TableStructureSchema` does not.
Further, they implement the `_fromDict` abstract function introduced by `TableStructureSchema`.
Finally, they implement `RowToEvent` and `RowToFeatureData`, respectively, for converting raw data from a data table into the specific data structures.

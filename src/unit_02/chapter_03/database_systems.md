## Choosing a Database System

<font style="color:tomato">STUB: This page is on the to-do list; only section headers have been added so far.</font>

### MySQL

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

### BigQuery

This step can be accomplished by doing the following:

1. Create a Google Cloud project to host game data
2. Create a BigQuery project:  
    This project should, in turn, have datasets for each game, and each dataset should have tables with columns and data types corresponding to the MySQL schema.
3. Use `opengamedata-automation` to automatically archive data from MySQL to BigQuery

### PostgreSQL
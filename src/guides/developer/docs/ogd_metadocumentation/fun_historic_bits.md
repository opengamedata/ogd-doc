# Unit 7, Chapter 6 : Fun Historical Bits

This document just holds bits of historic trivia and code snippets that I find fun in looking back on the development of OpenGameData.

## Model Class Comment

This comment was left-over from the `Model` class used in the original teacher dashboard, or a near descendant of that class.
The `Model` class and other aspects of that dashboard system formed the basis for the modular `Generator` system we have now,
which replaced the original "monolithic extractor" system.

```python
## @class Model
#  Abstract base class for session-level Wave features.
#  Models only have one public function, called Eval.
#  The Eval function takes a list of row data, computes some statistic, and returns a list of results.
#  If the model works on features from session data, it should calculate one result for each row (each row being a session).
#  If the model works on a raw list of recent events, it should calculate a single result (each row being an event).
```

An additional note of interest is that at the time, `Model` had the option of taking in rows of feature data.
Not sure if we ever really used this or not, but it appears we had some version of the "second-order features" concept as well,
some time before we'd ever formalized that idea in the "miniextractors" (now "Generator") architecture.

## A Long-Unfinished Thought

Sometimes, you start to write a note about something, get interrupted mid-thought, and never come back to finish it.
This incomplete comment was last modified over 4 years prior to its eventual removal from `Request.py` in 2025
(and 2 years prior to the last edit to the function body).
It's anybody's guess (the original authors included) what the `RetrieveIDs` function was meant to "use" at the time the comment was started:

```python
    ## Method to retrieve the list of IDs for all sessions covered by the request.
    #  Note, this will use the 
    def RetrieveIDs(self) -> Optional[List[str]]:
        return self.Range.IDs
```

## "Interface" PyProject

During a cleanup of one of the old server directories that once ran a copy of `opengamedata-core`, I rediscovered that at some point there was an attempt to set up a package for the OGD interface classes as its own separate package for inclusion in other projects, with a `setup.cfg` as shown below.
This would have pre-dated the "real," successful creation of the `OGDUtils` and `opengamedata-core` packages by a couple years - the `pyproject`-related files were dated 09/23/2021.

```toml
[metadata]
name = opengamedata-interfaces
version = 0.0.1
author = Luke Swanson
author_email = swansonl@cs.wisc.edu
description = Data Interfaces package for OpenGameData.
long_description = Data Interfaces package for OpenGameData.
url = https://github.com/opengamedata/opengamedata-core/tree/master/interfaces/
project_urls =
    Bug Tracker = https://github.com/opengamedata/opengamedata-core/issues
classifiers =
    Programming Langauage :: Python :: 3
    License :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find
python_requires = >= 3.6

[options.packages.find]
where = src
```

## General-use (My)SQL Class

This is/was among the oldest code in the entire OpenGameData project, prior to its retirement from `opengamedata-common` for release 2.0.0.
It was written in summer of 2019, back when Field Day was located in the "blue house" on the UW-Madison campus, and remained mostly-untouched through multiple refactorings and reorganizations, including the split out from `ogd-core` to `ogd-common`.
In 2.0.0, we finally reached a point where the connection code needed to be split up; most of it remained afterwards, just in a new location.

The portion of the `SQL` class that was totally retired was the `SELECT` function, which was originally created all those years ago with the assumption that we would eventually have enough different ways we'd want to query the data that we'd make use of the many common clauses available in a SELECT statement.
In practice, we pretty much stuck to the same small handful of queries, either getting the IDs over a date range, or getting all rows from a set of IDs.
Thus, there was never really a great use of the function, and going to an approach of writing queries individually made it a little easier to be clear on which queries, or parts of queries, were truly correctly parameterized.

```python
## @class SQL
#  A utility class containing some functions to assist in retrieving from a database.
#  Specifically, helps to connect to a database, make selections, and provides
#  a nicely formatted 500 error message.
class SQL:

    # Function to set up a connection to a database, via an ssh tunnel if available.
    @staticmethod
    def ConnectDB(schema:GameStoreConfig) -> Tuple[Optional[sshtunnel.SSHTunnelForwarder], Optional[connection.MySQLConnection]]:
        """
        Function to set up a connection to a database, via an ssh tunnel if available.

        :param db_settings: A dictionary mapping names of database parameters to values.
        :type db_settings: Dict[str,Any]
        :param ssh_settings: A dictionary mapping names of ssh parameters to values, or None if no ssh connection is desired., defaults to None
        :type ssh_settings: Optional[Dict[str,Any]], optional
        :return: A tuple consisting of the tunnel and database connection, respectively.
        :rtype: Tuple[Optional[sshtunnel.SSHTunnelForwarder], Optional[connection.MySQLConnection]]
        """
        ret_val : Tuple[Optional[sshtunnel.SSHTunnelForwarder], Optional[connection.MySQLConnection]] = (None, None)

        tunnel  : Optional[sshtunnel.SSHTunnelForwarder] = None
        db_conn : Optional[connection.MySQLConnection]   = None
        # Logger.Log("Preparing database connection...", logging.INFO)
        if schema.StoreConfig is not None and isinstance(schema.StoreConfig, MySQLConfig):
            if schema.StoreConfig.HasSSH:
                Logger.Log(f"Preparing to connect to MySQL via SSH, on host {schema.StoreConfig.SSH.Host}", level=logging.DEBUG)
                if (schema.StoreConfig.SSH.Host != "" and schema.StoreConfig.SSH.User != "" and schema.StoreConfig.SSH.Pass != ""):
                    tunnel,db_conn = SQL._connectToMySQLviaSSH(sql=schema.StoreConfig, db=schema.DatabaseName)
                else:
                    Logger.Log(f"SSH login had empty data, preparing to connect to MySQL directly instead, on host {schema.StoreConfig.DBHost}", level=logging.DEBUG)
                    db_conn = SQL._connectToMySQL(login=schema.StoreConfig, db=schema.DatabaseName)
                    tunnel = None
            else:
                Logger.Log(f"Preparing to connect to MySQL directly, on host {schema.StoreConfig.DBHost}", level=logging.DEBUG)
                db_conn = SQL._connectToMySQL(login=schema.StoreConfig, db=schema.DatabaseName)
                tunnel = None
            # Logger.Log("Done preparing database connection.", logging.INFO)
            ret_val = (tunnel, db_conn)
        else:
            Logger.Log(f"Unable to connect to MySQL, game source schema does not have a valid MySQL config!", level=logging.ERROR)

        return ret_val

    # Function to help connect to a mySQL server.
    @staticmethod
    def _connectToMySQL(login:MySQLConfig, db:str) -> Optional[connection.MySQLConnection]:
        """Function to help connect to a mySQL server.

        Simply tries to make a connection, and prints an error in case of failure.
        :param login: A SQLLogin object with the data needed to log into MySQL.
        :type login: SQLLogin
        :return: If successful, a MySQLConnection object, otherwise None.
        :rtype: Optional[connection.MySQLConnection]
        """
        try:
            Logger.Log(f"Connecting to SQL (no SSH) at {login.AsConnectionInfo}...", logging.DEBUG)
            db_conn = connection.MySQLConnection(host     = login.DBHost,    port    = login.DBPort,
                                                 user     = login.DBUser,    password= login.DBPass,
                                                 database = db, charset = 'utf8')
            Logger.Log(f"Connected.", logging.DEBUG)
            return db_conn
        #except MySQLdb.connections.Error as err:
        except Exception as err:
            msg = f"""Could not connect to the MySql database.
            Login info: {login.AsConnectionInfo} w/port type={type(login.DBPort)}.
            Full error: {type(err)} {str(err)}"""
            Logger.Log(msg, logging.ERROR)
            traceback.print_tb(err.__traceback__)
            return None

    ## Function to help connect to a mySQL server over SSH.
    @staticmethod
    def _connectToMySQLviaSSH(sql:MySQLConfig, db:str) -> Tuple[Optional[sshtunnel.SSHTunnelForwarder], Optional[connection.MySQLConnection]]:
        """Function to help connect to a mySQL server over SSH.

        Simply tries to make a connection, and prints an error in case of failure.
        :param sql: A SQLLogin object with the data needed to log into MySQL.
        :type sql: SQLLogin
        :param ssh: An SSHLogin object with the data needed to log into MySQL.
        :type ssh: SSHLogin
        :return: An open connection to the database if successful, otherwise None.
        :rtype: Tuple[Optional[sshtunnel.SSHTunnelForwarder], Optional[connection.MySQLConnection]]
        """
        tunnel    : Optional[sshtunnel.SSHTunnelForwarder] = None
        db_conn   : Optional[connection.MySQLConnection] = None
        MAX_TRIES : Final[int] = 5
        tries : int = 0
        connected_ssh : bool = False

        # First, connect to SSH
        while connected_ssh == False and tries < MAX_TRIES:
            if tries > 0:
                Logger.Log("Re-attempting to connect to SSH.", logging.INFO)
            try:
                Logger.Log(f"Connecting to SSH at {sql.SSHConf.AsConnectionInfo}...", logging.DEBUG)
                tunnel = sshtunnel.SSHTunnelForwarder(
                    (sql.SSH.Host, sql.SSH.Port), ssh_username=sql.SSH.User, ssh_password=sql.SSH.Pass,
                    remote_bind_address=(sql.DBHost, sql.DBPort), logger=Logger.std_logger
                )
                tunnel.start()
                connected_ssh = True
                Logger.Log(f"Connected.", logging.DEBUG)
            except Exception as err:
                msg = f"Could not connect via SSH: {type(err)} {str(err)}"
                Logger.Log(msg, logging.ERROR)
                Logger.Print(msg, logging.ERROR)
                traceback.print_tb(err.__traceback__)
                tries = tries + 1
        if connected_ssh == True and tunnel is not None:
            # Then, connect to MySQL
            try:
                Logger.Log(f"Connecting to SQL (via SSH) at {sql.DBUser}@{sql.DBHost}:{tunnel.local_bind_port}/{db}...", logging.DEBUG)
                db_conn = connection.MySQLConnection(host     = sql.DBHost,    port    = tunnel.local_bind_port,
                                                     user     = sql.DBUser,    password= sql.DBPass,
                                                     database = db, charset ='utf8')
                Logger.Log(f"Connected", logging.DEBUG)
                return (tunnel, db_conn)
            except Exception as err:
                msg = f"Could not connect to the MySql database: {type(err)} {str(err)}"
                Logger.Log(msg, logging.ERROR)
                Logger.Print(msg, logging.ERROR)
                traceback.print_tb(err.__traceback__)
                if tunnel is not None:
                    tunnel.stop()
                return (None, None)
        else:
            return (None, None)

    @staticmethod
    def disconnectMySQL(db:Optional[connection.MySQLConnection], tunnel:Optional[sshtunnel.SSHTunnelForwarder]=None) -> None:
        if db is not None:
            db.close()
            Logger.Log("Closed MySQL database connection", logging.DEBUG)
        else:
            Logger.Log("No MySQL database to close.", logging.DEBUG)
        if tunnel is not None:
            tunnel.stop()
            Logger.Log("Stopped MySQL tunnel connection", logging.DEBUG)
        else:
            Logger.Log("No MySQL tunnel to stop", logging.DEBUG)

    # Function to build and execute SELECT statements on a database connection.
    @staticmethod
    def SELECT(cursor        :cursor.MySQLCursor,          db_name        : str,                   table    : str,
               columns       :List[str]           = [],    filter         : Optional[str] = None,
               sort_columns  :Optional[List[str]] = None,  sort_direction : str           = "ASC", grouping : Optional[str] = None,
               distinct      :bool                = False, offset         : int           = 0,     limit    : int           = -1,
               fetch_results :bool                = True,  params         : Tuple         = tuple()) -> Optional[List[Tuple]]:
        """Function to build and execute SELECT statements on a database connection.

        :param cursor: A database cursor, retrieved from the active connection.
        :type cursor: cursor.MySQLCursor
        :param db_name: The name of the database to which we are connected.
        :type db_name: str
        :param table: The name of the table from which we want to make a selection.
        :type table: str
        :param columns: A list of columns to be selected. If empty (or None), all columns will be used (SELECT * FROM ...). Defaults to None
        :type columns: List[str], optional
        :param filter: A string giving the constraints for a WHERE clause (The "WHERE" term itself should not be part of the filter string), defaults to None
        :type filter: str, optional
        :param sort_columns: A list of columns to sort results on. The order of columns in the list is the order given to SQL. Defaults to None
        :type sort_columns: List[str], optional
        :param sort_direction: The "direction" of sorting, either ascending or descending., defaults to "ASC"
        :type sort_direction: str, optional
        :param grouping: A column name to group results on. Subject to SQL rules for grouping, defaults to None
        :type grouping: str, optional
        :param distinct: A bool to determine whether to select only rows with distinct values in the column, defaults to False
        :type distinct: bool, optional
        :param limit: The maximum number of rows to be selected. Use -1 for no limit., defaults to -1
        :type limit: int, optional
        :param fetch_results: A bool to determine whether all results should be fetched and returned, defaults to True
        :type fetch_results: bool, optional
        :return: A collection of all rows from the selection, if fetch_results is true, otherwise None.
        :rtype: Optional[List[Tuple]]
        """
        d          = "DISTINCT" if distinct else ""
        cols       = ",".join([f"{col}" for col in columns]) if len(columns) > 0 else "*"
        sort_cols  = ",".join([f"`{col}`" for col in sort_columns]) if sort_columns is not None and len(sort_columns) > 0 else None
        table_path = db_name + "." + str(table)

        sel_clause = f"SELECT {d} {cols} FROM {table_path}"
        where_clause = "" if filter    is None else f"WHERE {filter}"
        group_clause = "" if grouping  is None else f"GROUP BY {grouping}"
        sort_clause  = "" if sort_cols is None else f"ORDER BY {sort_cols} {sort_direction}"
        lim_clause   = "" if limit < 0         else f"LIMIT {str(max(offset, 0))}, {str(limit)}" # don't use a negative for offset
        query = f"{sel_clause} {where_clause} {group_clause} {sort_clause} {lim_clause};"
        return SQL.Query(cursor=cursor, query=query, params=params, fetch_results=fetch_results)

    @staticmethod
    def Query(cursor:cursor.MySQLCursor, query:str, params:Optional[Tuple], fetch_results: bool = True) -> Optional[List[Tuple]]:
        result : Optional[List[Tuple]] = None
        # first, we do the query.
        Logger.Log(f"Running query: {query}\nWith params: {params}", logging.DEBUG, depth=3)
        start = datetime.now()
        cursor.execute(query, params)
        time_delta = datetime.now()-start
        Logger.Log(f"Query execution completed, time to execute: {time_delta}", logging.DEBUG)
        # second, we get the results.
        if fetch_results:
            result = cursor.fetchall()
            time_delta = datetime.now()-start
            Logger.Log(f"Query fetch completed, total query time:    {time_delta} to get {len(result) if result is not None else 0:d} rows", logging.DEBUG)
        return result
```


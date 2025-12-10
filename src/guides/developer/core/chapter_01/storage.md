# Data Storage

Data is currently spread across multiple systems:  

- `OpenGameData`:
The primary, "state of the art" storage system logs event data to a MySQL database.
Within this database, there is one table for each game, though all tables share a common schema.
Once nightly, the data from this MySQL database are moved to BigQuery for long-term warehousing and storage.  
Games using this system: **Wake** (Aqualab), **Mashopolis**, **IceCube VR**, **Waddle** (Penguins)

- `Firebase + BigQuery`:
This system logs event data to Google Firebase, using the Firebase "universal" schema.
Any data that does not fit into an existing column within this schema is relegated to the `event_params` field.
Once nightly, the Firebase events are moved to BigQuery for long-term warehousing and storage.  
Firebase events can not be accessed directly.
Games using this system: **Legend of the Lost Emerald** (Shipwrecks)

- `Logger`:
This system uses a pair of MySQL database servers. Events are initially logged to `fieldday-logger`, and are copied via MySQL's replication feature for long-term storage to `fieldday-store`.
Both database servers have a MySQL database named `logger`, which in turn have a single table for all games, named `log`.  
Games using this system: **Jo Wilder**, **Lakeland**, all **Yard Games**

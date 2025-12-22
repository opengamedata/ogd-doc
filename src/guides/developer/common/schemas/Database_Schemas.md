# Database Schemas

Below are the table schemas for each of the existing databases.

## `OpenGameData`

The `OpenGameData` database (named `opengamedata` in MySQL, no upper-case letters) contains one table for each game; however, the table schema is identical across tables.

The table names are:

- AQUALAB
- BACTERIA
- BALLOON
- CRYSTAL
- CYCLE_CARBON
- CYCLE_NITROGEN
- CYCLE_WATER
- EARTHQUAKE
- ICECUBE
- JOWILDER
- LAKELAND
- MAGNET
- MASHOPOLIS
- PENGUINS
- SHADOWSPECT
- SHIPWRECKS
- STEMPORTS
- WAVES
- WIND

| Column Name     | Column Type     | Nullable |
| --------------- | --------------- | -------- |
| id              | int(32)         | NO       |
| session_id      | varchar(32)     | NO       |
| user_id         | varchar(64)     | YES      |
| user_data       | text            | YES      |
| client_time     | datetime        | NO       |
| client_time_ms  | smallint(6)     | NO       |
| client_offset   | time            | YES      |
| server_time     | timestamp       | NO       |
| event_source    | enum('GAME','GENERATED') | NO   |
| game_state      | text            | YES      |
| app_version     | smallint(6)     | NO       |
| app_branch      | varchar(32)     | YES      |
| log_version     | smallint(6)     | NO       |
| event_sequence_index | bigint(64) | NO       |
| remote_addr     | varchar(32)     | NO       |
| http_user_agent | text            | YES      |

## Logger

The Logger database (named `logger` in MySQL, no upper-case letters) contains a single table named `log`.
It has the following schema:

| Column Name           | Column Type     | Nullable |
| --------------------- | ------------------ | -------- |
| id                    | int(32)         | NO       |
| app_id                | varchar(32)     | NO       |
| app_id_fast           | enum('UNDEFINED','WAVES','CRYSTAL','JOWILDER','LAKELAND')      | NO   |
| app_version           | int(32)         | NO       |
| session_id            | varchar(32)     | YES      |
| persistent_session_id | varchar(32)     | YES      |
| player_id             | varchar(6)      | YES      |
| level                 | int(32)         | NO       |
| event                 | enum('BEGIN','COMPLETE','SUCCEED','FAIL','CUSTOM','UNDEFINED') | YES  |
| event_custom          | int(32)         | NO       |
| event_data_simple     | int(32)         | NO       |
| event_data_complex    | text            | YES      |
| client_time           | timestamp       | NO       |
| client_time_ms        | int(32)         | NO       |
| server_time           | timestamp       | NO       |
| remote_addr           | varchar(32)     | YES      |
| req_id                | bigint(64)      | NO       |
| session_n             | bigint(64)      | NO       |
| http_user_agent       | text            | YES      |

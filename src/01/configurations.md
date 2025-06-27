# Configuring OpenGameData

An example configuration file (based on the config template):

```python
settings = {
    "BATCH_SIZE":1000,
    "LOG_FILE":False,
    "DEBUG_LEVEL":"INFO",
    "FAIL_FAST":False,
    "FILE_INDEXING" : 
    {
        "LOCAL_DIR"     : "./data/",
        "REMOTE_URL"    : "https://fieldday-web.ad.education.wisc.edu/opengamedata/",
        "TEMPLATES_URL" : "https://github.com/opengamedata/opengamedata-samples"
    },
    "GAME_SOURCES" :
    {
        "OPENGAMEDATA_BQ" : {
            "DB_TYPE"    : "BIGQUERY",
            "PROJECT_ID" : "wcer-field-day-ogd-1798",
            "PROJECT_KEY": "./config/ogd.json"
        },
        "OPENGAMEDATA_MYSQL": {
            "DB_TYPE" : "MySQL",
            "DB_HOST" : "127.0.0.1",
            "DB_PORT" : 3306,
            "DB_USER" : "username",
            "DB_PW"   : "password",
            "SSH_HOST": "mysql.host.com",
            "SSH_USER": "user",
            "SSH_PASS": "aFakePassword",
            "SSH_PORT": 22
        },
    },
    "GAME_SOURCE_MAP":
    {
        "AQUALAB" : { "source":"OPENGAMEDATA_BQ",    "database":"aqualab",      "table":"aqualab_daily",  "schema":"OPENGAMEDATA_BIGQUERY" },
        "BACTERIA": { "source":"OPENGAMEDATA_BQ",    "database":"bacteria",     "table":"bacteria_daily", "schema":"OPENGAMEDATA_BIGQUERY" },
        "BALLOON" : { "source":"OPENGAMEDATA_MYSQL", "database":"opengamedata", "table":"balloon",        "schema":"OPENGAMEDATA_MYSQL"    }
    }
}
```

<font style="color:tomato">STUB: This section is on the to-do list.</font>

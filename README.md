# Description

PostgreSQL database metadata (DDL) grabber to files and schema diff.

# Dependencies

* [Python 3](https://www.python.org/downloads/)
* [psycopg](https://pypi.org/project/psycopg/)

# Installation

```bash
pip install postgres_ddl
```

# Config file

```jsonc
{
    // Database connects (Required)
    "connects": {
        "default": {
            "host": "localhost",
            "port": 5432,
            "database": "db",
            "username": "some_user",
            "password": "some_password"
        }
        // ...
    },

    // Work path (Required)
    "path": "/some/path/to/grabber/result/folder",

    // File writing threads (Optional)
    "threads": 8,

    // Newline symbol in files (Optional)
    "new_line": "\n",

    // Indent (Optional)
    "indent": 2,

    // Schemas settings
    "schemas": {

        // Exclude schemas (Optional)
        "exclude": [
            "information_schema",
            "pg_catalog"
        ]
    },

    // Tables settings
    "tables": {

        // Show sequence grants in tables files (Optional)
        "sequence_grants_show": false
    },

    // Functions settings
    "functions": {

        // Functions folder name (Optional)
        "folder_name": "functions",

        // Functions parameters sign (Optional)
        "param_sign": ":=" // or "=>"
    },

    // Triggers settings
    "triggers": {

        // Triggers folder name (Optional)
        "folder_name": "triggers"
    },

    // Foreign servers settings
    "foreign_servers": {

        // Show user mappings in foreign servers files (Optional)
        "user_mappings_show": true
    },

    // Logging settings
    "logs": {

        // Log level (Optional)
        "level": "INFO" // or "DEBUG"
    }
}
```

# Database grabbing to files

From command-line:

```bash
python "grab.py" --help
#   usage: grab.py [-h] [-c CONFIG] [-n NAME]
#   options:
#       -h, --help           show this help message and exit
#       -c, --config CONFIG  Path to config file
#       -n, --name NAME      Connect name from config file

python "grab.py" -c /some/path/to/config.json -n db_test
```

From python script:

```py
from postgres_ddl.Grabber import Grabber

Grabber(
    path_config  = "/some/path/to/config.json",
    connect_name = "db_test"
).Run()
```

Database will be exported to `path` folder from config file.

# Compare (diff) databases

From command-line:

```bash
python "diff.py" --help
#   usage: diff.py [-h] [-c CONFIG] [-s SOURCE] [-t TARGET]
#   options:
#       -h, --help           show this help message and exit
#       -c, --config CONFIG  Path to config file
#       -s, --source SOURCE  Source connect name from config file
#       -t, --target TARGET  Target connect name from config file

python "diff.py" -c /some/path/to/config.json -s db_test -t db_target
```

From python script:

```py
from postgres_ddl.Diff import Diff

Diff(
    path_config    = "/some/path/to/config.json",
    connect_source = "db_test",
    connect_target = "db_target"
).Run()
```

# Links

* [GitHub](https://github.com/ish1mura/postgres_ddl)
* [PyPI](https://pypi.org/project/postgres-ddl/)

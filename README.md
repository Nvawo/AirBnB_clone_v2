# AirBnB Clone - MySQL (Part II)

The HBnB console now supports two storage engines, selected with an
environment variable:

- **FileStorage**: JSON file (default)
- **DBStorage**: MySQL through SQLAlchemy (`HBNB_TYPE_STORAGE=db`)

## Environment variables
| Variable | Purpose |
|---|---|
| HBNB_MYSQL_USER | MySQL user (hbnb_dev) |
| HBNB_MYSQL_PWD | MySQL password (hbnb_dev_pwd) |
| HBNB_MYSQL_HOST | MySQL host (localhost) |
| HBNB_MYSQL_DB | Database name (hbnb_dev_db) |
| HBNB_TYPE_STORAGE | `db` selects DBStorage, anything else FileStorage |
| HBNB_ENV | `test` drops all tables on start |

## Requirements
Python 3, MySQL, `pip3 install SQLAlchemy mysqlclient`

## Setup
    sudo service mysql start
    sudo mysql < setup_mysql_dev.sql

## Usage
    echo 'create State name="California"' | HBNB_MYSQL_USER=hbnb_dev \
    HBNB_MYSQL_PWD=hbnb_dev_pwd HBNB_MYSQL_HOST=localhost \
    HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db ./console.py

## Files
- models/base_model.py: BaseModel and `Base`
- models/state.py, models/city.py: SQLAlchemy models
- models/engine/db_storage.py: DBStorage engine
- models/engine/file_storage.py: FileStorage engine
- models/__init__.py: storage switch

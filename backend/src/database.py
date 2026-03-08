import sqlite3
import os
from datetime import date

sqlite3.register_adapter(date, lambda val: val.isoformat())
sqlite3.register_converter("DATE", lambda val: date.fromisoformat(val.decode()))

# Path to database
DB_PATH = os.path.join("data", "finance.db") # /data/finance.db
SCHEMA_PATH = os.path.join("schema.sql") # /schema.sql

def get_connection():
    """ Returns a connection to SQLite database """

    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row # allows us to access columns by name
    conn.execute("PRAGMA foreign_keys = ON") # enable foreign key constraints
    return conn

def init_db():
    """ Initializes the database using schema.sql """

    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    
    with get_connection() as conn:
        conn.executescript(schema)
        print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
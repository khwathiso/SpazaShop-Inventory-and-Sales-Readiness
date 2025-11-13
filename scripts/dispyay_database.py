import sqlite3
import pandas as pd
import os

#This will dynamically build the absolute database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "../db/spaza_shop.db")

conn = sqlite3.connect(db_path)

# Get all table names
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables:\n", tables, "\n")

# Pick the first table
if not tables.empty:
    table_name = tables.iloc[0, 0]

    # Display all data from that table
    df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
    print(f" Data from table '{table_name}':\n", df)
else:
    print("No tables found in the database, Sorry!")

conn.close()

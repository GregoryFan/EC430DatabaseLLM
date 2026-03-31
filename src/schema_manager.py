import pandas as pd
import sqlite3
from dotenv import load_dotenv
import os

# This file is responsible for managing the database schema,
# Responsibilities:
# Discover existing tables in the database
# Represent table schemas as structured objects (table, columns, types)
# Compare schemas to determine compatibility (append vs create)
# Provide schema information to other components (e.g., Query Service, LLM)

#Function that dictates whether data from pandas table headers is similar
#to existing data. 
# Returns table name, or None.

load_dotenv("CONFIG_FILE")
DB_PATH = os.getenv("DB_PATH", "database.db").strip().lower()

def find_similar_table(pandas_headers):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        #get the headers
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_info = cursor.fetchall()
        table_headers = [info[1] for info in table_info]

        matching_headers = set(pandas_headers) & set(table_headers)
        non_matching_headers = set(pandas_headers) - set(table_headers)

        if len(matching_headers) > len(non_matching_headers):
            print(f"Table '{table_name}' is similar enough to the CSV file. Information will be updated there.")
            conn.close()
            return table_name, non_matching_headers
    
    print("No similar tables found. A new table will be created.")
    conn.close()
    return None, None

#Function that retrieves all tables and provides their schema in a readable way.
#Schemas will be provided as [table_name, [columns], [types]]

def get_tables():
    #Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    #Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()

    #just get all the info
    table_schemas = []
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_info = cursor.fetchall()
        columns = [info[1] for info in table_info]
        types = [info[2] for info in table_info]
        table_schemas.append((table_name, columns, types))

    conn.close()
    return table_schemas

def run_user_query(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
        return results, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()

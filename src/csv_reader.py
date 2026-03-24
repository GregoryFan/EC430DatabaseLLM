import pandas as pd
import sqlite3 
from sys import argv

def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)

        #Query the SQL Database for tables
        #Check if any tables are similar enough to the CSV file
        #If there are more matching headers than non-matching headers, then we can assume that the CSV file is similar enough to the table to be inserted into the table
        #If there are no tables that are similar enough, then we can create a new table

        chosenAction, table_name = check_similar_tables(data.columns)

        conn = sqlite3.connect("database.db")
        if chosenAction == "similar":
            conn.execute(f"INSERT INTO {table_name} VALUES ({','.join(['?' for _ in data.columns])})", data.values.tolist())
            conn.commit()
            conn.close()
        
        elif chosenAction == "new":
            conn.execute(f"CREATE TABLE {file_path[:-4]} ({', '.join(data.columns)})")
            conn.execute(f"INSERT INTO {file_path[:-4]} VALUES ({','.join(['?' for _ in data.columns])})", data.values.tolist())
            conn.commit()
            conn.close()

        return 200
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return 400
    
def check_similar_tables(csv_headers):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        #get the headers
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        table_info = cursor.fetchall()
        table_headers = [info[1] for info in table_info]

        matching_headers = set(csv_headers) & set(table_headers)
        non_matching_headers = set(csv_headers) - set(table_headers)

        if len(matching_headers) > len(non_matching_headers):
            print(f"DEBUG Table '{table_name}' is similar enough to the CSV file.")
            return "similar", table_name
    
    print("DEBUG No similar tables found. A new table will be created.")
    return "new", None

# Testing
if __name__ == "__main__":
    if(len(argv) < 2):
        print("Please provide a file path to the CSV file.")
        exit(1)
    file_path = argv[1]
    status = load_csv(file_path)

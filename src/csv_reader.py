import pandas as pd
import sqlite3 
import schema_manager
from sys import argv

def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)

        data_name = file_path[:-4]

        
        #For goodness of data, drop all columns with the same first column.
        first_col = data.columns[0]
        data_duplicates = data[data.duplicated(subset=[first_col], keep='first')]
        clean_data = data.drop_duplicates(subset=[first_col], keep='first')
        
        if len(data_duplicates > 0):
            print("Dropping following data due to having the same id as another.\nFirst columns (NOT id) must be unique.")
            print(data_duplicates)
        
        #Query the SQL Database for tables
        #Check if any tables are similar enough to the CSV file
        #If there are more matching headers than non-matching headers, then we can assume that the CSV file is similar enough to the table to be inserted into the table
        #If there are no tables that are similar enough, then we can create a new table

        table_name, new_cols = schema_manager.find_similar_table(data.columns)

        conn = sqlite3.connect("database.db")

        #Updating Table Logic
        if table_name != None:
            #Add new columns, if any
            if len(new_cols) > 0:
                #Get everything together
                cols = []
                for col in new_cols:
                    col_type = pandas_to_type(data[col].dtype)
                    cols.append(f"{col} {col_type}")
                col_schema = f"{', '.join(cols)}"

                #Make the query
                updateQuery = f"""
                ALTER TABLE {table_name}
                ADD {col_schema}
                """
                print(updateQuery)
                conn.execute(updateQuery)
            
            before = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            #Updating Values
            placeholders_list = f'{', '.join(['?' for _ in data.columns])}'
            col_names = f'({', '.join([col for col in data.columns])})'
            query = f"""
            INSERT INTO {table_name}  {col_names} 
            VALUES ({placeholders_list})
            ON CONFLICT({data.columns[0]})
            DO UPDATE SET {', '.join([f"{col}=excluded.{col}" for col in data.columns])}
            """
            conn.executemany(query, clean_data.values.tolist())
            after = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            
            #To inform users
            added = after - before
            updated = len(clean_data) - added
            print(f"Added {added} new entries. \nUpdated {updated} existing entries.")

            conn.commit()
            conn.close()
        
        #Creating New Table Logic
        else:
            #makes col query with name, type.
            cols = []
            use_as_key = True
            for col in data.columns:
                col_type = pandas_to_type(data[col].dtype)
                if(use_as_key):
                    cols.append(f"{col} {col_type} UNIQUE")
                    use_as_key = False
                else:
                    cols.append(f"{col} {col_type}")
            col_schema = f"{', '.join(cols)}"

            #creates table query with added id autoincrement for tracking.
            create_query = f"""
            CREATE TABLE {data_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {col_schema}
            )
            """
            conn.execute(create_query)

            #inserting initial values query
            placeholders_list = f'{', '.join(['?' for _ in data.columns])}'
            col_names = f'({', '.join([col for col in data.columns])})'
            insert_query = f"INSERT OR IGNORE INTO {data_name} {col_names} VALUES ({placeholders_list})"

            conn.executemany(insert_query, clean_data.values.tolist())

            conn.commit()
            conn.close()
    
        return 200
    
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return 400
    
#Gets data type from pandas
def pandas_to_type(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "REAL"
    else:
        return "TEXT"

# Testing
if __name__ == "__main__":
    if(len(argv) < 2):
        print("Please provide a file path to the CSV file.")
        exit(1)
    file_path = argv[1]
    
    status = load_csv(file_path)

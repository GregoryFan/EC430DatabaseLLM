import schema_manager
import csv_reader
import sqlite3


#Load in the data and test the following:
#Find similar tables
#Get the table schema

#All things considered csv_reader tests the find similar table function 
#when it reads a csv, so we can just test get_tables only instead.

def test_setup():
    status = csv_reader.load_csv("students.csv", "TESTDB.db")
    assert status == 200
    status = csv_reader.load_csv("food.csv", "TESTDB.db")
    assert status == 200

def test_get_tables():
    tables = schema_manager.get_tables("TESTDB.db")
    for table in tables:
        if table[0] == "students":
            assert table[1] == ["id", "Name", "Age", "Major"] and table[2] == ["INTEGER", "TEXT", "INTEGER", "TEXT"]
        elif table[0] == "food":
            assert table[1] == ["id", "food", "stock", "price"] and table[2] == ["INTEGER", "TEXT", "INTEGER", "REAL"]

#Tests if file is there and has the error message.
def test_schema_logger():
    schema_manager.log_query_error("Test Origin", "Test error message", "This is a test error detail.")
    assert open("errors_log.txt", "r").read().strip().split("\n")[-1] == "Origin: Test Origin\n Query: Test error message\nError: This is a test error detail."

def test_cleanup():
    conn = sqlite3.connect("TESTDB.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS students;")
    cursor.execute("DROP TABLE IF EXISTS food;")
    conn.commit()
    conn.close()


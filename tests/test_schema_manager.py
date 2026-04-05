import schema_manager
import csv_reader


#Load in the data and test the following:
#Find similar tables
#Get the table schema

#All things considered csv_reader tests the find similar table function 
#when it reads a csv, so we can just test get_tables only instead.

def test_setup():
    status = csv_reader.read_csv("students.csv")
    assert status == 200
    status = csv_reader.read_csv("food.csv")
    assert status == 200

def test_get_tables():
    tables = schema_manager.get_tables()
    for table in tables:
        if table[0] == "students":
            assert table[1] == ["id", "Name", "Age", "Major"] and table[2] == ["INTEGER", "TEXT", "INTEGER", "TEXT"]
        elif table[0] == "food":
            assert table[1] == ["id", "food", "stock", "price"] and table[2] == ["INTEGER", "TEXT", "INTEGER", "REAL"]


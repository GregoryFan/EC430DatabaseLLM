import sqlite3
import csv_reader
import pytest

#Cases to test:
#1. Normal data insertion.
#2. Data insertion with duplicate key ids.
#3. Data insertion with new columns, but same table.
#4. Data insertion with completely new table.

#Lastly, remember to clean up table afterwards.

#Normal Insertion
def test_normal_insertioin():
    conn = sqlite3.connect("TESTDB.db")
    status = csv_reader.load_csv("students.csv", "TESTDB.db")

    #Make sure if it returned just fine.
    assert status == 200

    #Then, go actually check the data.
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()

    assert len(results) == 3
    assert results[0][1] == "Greg"
    assert results[1][1] == "Michael"
    assert results[2][1] == "Mint"
    assert results[0][2] == 21
    assert results[1][2] == 67
    assert results[2][2] == 61
    assert results[0][3] == "Mathematics"
    assert results[1][3] == "Computer Engineer"
    assert results[2][3] == "Electrical Engineer"
    conn.close()

def test_duplicate_key_insertion():
    conn = sqlite3.connect("TESTDB.db")
    status = csv_reader.load_csv("students.csv", "TESTDB.db")

    #Make sure if it returned just fine.
    assert status == 200

    #Then, go actually check the data. Should be the same as before, since duplicate key ids should be dropped.
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()
    assert len(results) == 3
    assert results[0][1] == "Greg"
    assert results[1][1] == "Michael"
    assert results[2][1] == "Mint"
    assert results[0][2] == 21
    assert results[1][2] == 67
    assert results[2][2] == 61
    assert results[0][3] == "Mathematics"
    assert results[1][3] == "Computer Engineer"
    assert results[2][3] == "Electrical Engineer"
    conn.close()

def test_new_column_insertion():
    conn = sqlite3.connect("TESTDB.db")
    status = csv_reader.load_csv("students2.csv", "TESTDB.db")

    #Make sure if it returned just fine.
    assert status == 200

    #Then, go actually check the data. Should be the same as before, but with an extra column of data.
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()
    assert len(results) == 3
    assert results[0][1] == "Greg"
    assert results[1][1] == "Michael"
    assert results[2][1] == "Mint"
    assert results[0][2] == 21
    assert results[1][2] == 67
    assert results[2][2] == 61
    assert results[0][3] == "Mathematics"
    assert results[1][3] == "Computer Engineer"
    assert results[2][3] == "Electrical Engineer"
    assert results[0][4] == "Male"
    assert results[1][4] == "Male"
    assert results[2][4] == "Female"
    conn.close()
    

def test_new_table_insertion():
    conn = sqlite3.connect("TESTDB.db")
    status = csv_reader.load_csv("food.csv", "TESTDB.db")

    #Make sure if it returned just fine.
    assert status == 200

    #Then, go actually check the data. Should be the same as before, but with an extra column of data.
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food")
    results = cursor.fetchall()

    #Data presence tested before. Just see if the table is there.
    assert len(results) == 3
    conn.close()

def test_cleanup():
    conn = sqlite3.connect("TESTDB.db")
    conn.execute("DROP TABLE students")
    conn.execute("DROP TABLE food")
    conn.commit()
    conn.close()




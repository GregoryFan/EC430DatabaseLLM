import sql_verifier
import csv_reader
import sqlite3


#Essentially, run through everything and test all SQL SELECT queries
#Also make sure to attempt bad queries.

#Setup
def test_setup():
    status = csv_reader.load_csv("students.csv", "TESTDB.db")
    assert status == 200
    status = csv_reader.load_csv("food.csv", "TESTDB.db")
    assert status == 200
    
#Not a query
def test_bad_query():
    query = "not a query"
    assert not sql_verifier.validate_query(query, "TESTDB.db")

#Dropping is not allowed
def test_drop_query():
    query = "DROP TABLE students"
    assert not sql_verifier.validate_query(query, "TESTDB.db")

#Updating is also not allowed
def test_alter_query():
    query = "ALTER TABLE students ADD COLUMN gpa REAL"
    assert not sql_verifier.validate_query(query, "TESTDB.db")

#Secondary malicious queries with a select shield
def test_secondary_bad_query():
    query = "SELECT * FROM students; DROP TABLE students"
    assert not sql_verifier.validate_query(query, "TESTDB.db")

#Default good case.
def test_good_query():
    query = "SELECT * FROM students"
    assert sql_verifier.validate_query(query, "TESTDB.db")

#Where clauses
def test_where_query():
    query = "SELECT * FROM students WHERE name = 'TEST'"
    assert sql_verifier.validate_query(query, "TESTDB.db")

#Lower commands
def test_lower_query():
    query = "SELECT * FROM students WHERE LOWER(name) = 'test'"
    assert sql_verifier.validate_query(query, "TESTDB.db")

#Joins 
def test_join_query():
    query = "SELECT students.name, courses.course_name FROM students JOIN courses ON students.course_id = courses.id"
    assert sql_verifier.validate_query(query, "TESTDB.db")

#Counts
def test_count_query():
    query = "SELECT COUNT(*) FROM students"
    assert sql_verifier.validate_query(query, "TESTDB.db")

#Sums
def test_sum_query():
    query = "SELECT SUM(gpa) FROM students"
    assert sql_verifier.validate_query(query)






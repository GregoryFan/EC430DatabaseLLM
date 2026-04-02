import llm_interface
#Because it's rather hard to test the openai part, we will only be testing prompt constructing.
#Methods to test:
#Building the data prompt.
#Building the previous attempts prompt.


def test_build_schema_string():
    tables = []
    table1 = ["students", ["id", "name", "age", "major"], ["INTEGER", "TEXT", "INTEGER", "TEXT"]]
    tables.append(table1)
    table2 = ["food", ["id", "food", "stock", "price"], ["INTEGER", "TEXT", "INTEGER", "REAL"]]
    tables.append(table2)

    schema_string = llm_interface.build_schema_string(tables)
    expected_string = "Table 0 name: students. Columns: id with type INTEGER, name with type TEXT, age with type INTEGER, major with type TEXT. End of Table students. Table 1 name: food. Columns: id with type INTEGER, food with type TEXT, stock with type INTEGER, price with type REAL. End of Table food. "
    assert schema_string == expected_string

def test_build_previous_attempts_string():
    previous_attempts = [["test query", "test error"], ["test query2", "test error2"]]
    pa_string = llm_interface.build_previous_attempts_string(previous_attempts)
    assert pa_string == "You have attempted this before, but ran into the following problems for the following queries: Query: test query, Problem: test error. Query: test query2, Problem: test error2. Use this information to better infer what the data is like. Do NOT use the same query, if possible. Usual suspects are case-sensitivity."
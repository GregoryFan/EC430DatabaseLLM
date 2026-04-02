import query_service

#im going to be so real i have no idea how to test this


#Tests the case where there is an error on query execution
def test_check_result_error():
    query = "test query"
    error = "test error"
    results = ""
    attempt = query_service.check_result(query, results, error)
    assert attempt == [query, f"Error on execution: {error}"]

#Tests the case where nothing is received from the query, potential fault.
def test_check_result_no_results():
    query = "test query"
    error = None
    results1 = []
    results2 = [(None,)]
    results3 = 0
    attempt1, restart1 = query_service.check_result(query, results1, error)
    attempt2, restart2 = query_service.check_result(query, results2, error)
    attempt3, restart3 = query_service.check_result(query, results3, error)
    assert attempt1 == [query, "Returned zero rows. Likely a missed filtering."] and restart1 == True
    assert attempt2 == [query, "Returned zero rows. Likely a missed filtering."] and restart2 == True
    assert attempt3 == [query, "Returned zero rows. Likely a missed filtering."] and restart3 == True

#Tests the case where a count where zero is returned, and the query is a WHERE clause.
def test_check_result_count_empty():
    query = "SELECT * FROM students WHERE name = 'TEST'"
    error = None
    results = [(0,)]
    attempt, restart = query_service.check_result(query, results, error)
    assert attempt == [query, "Returned zero rows. Likely a missed filtering."] and restart == True

#simple pass case test
def test_check_result_success():
    query = "TEST"
    error = None
    results = [(1,)]
    attempt, restart = query_service.check_result(query, results, error)
    assert attempt == "" and restart == False
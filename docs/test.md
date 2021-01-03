[flask Test tutorial](https://flask.palletsprojects.com/en/1.1.x/testing/#testing)
[pytest Parametrize tutorial](https://docs.pytest.org/en/stable/example/parametrize.html)
[pytest collection convention](https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery)

The First Test
Now it’s time to start testing the functionality of the application. Let’s check that the application shows “No entries here so far” if we access the root of the application (/). To do this, we add a new test function to test_flaskr.py, like this:

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data
Notice that our test functions begin with the word test; this allows pytest to automatically identify the function as a test to run.

By using client.get we can send an HTTP GET request to the application with the given path. The return value will be a response_class object. We can now use the data attribute to inspect the return value (as string) from the application. In this case, we ensure that 'No entries here so far' is part of the output.

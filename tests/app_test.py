from fjell import app, http, test


def test_simple_app():
    testapp = app.Application(__name__)
    testapp.add_route("GET", "/", lambda req: "hello world")
    client = test.Client(testapp.wsgi_app)

    resp = client.get("/")

    assert isinstance(resp, http.Response)
    assert 200 == resp.status_code
    assert b"hello world" == resp.data

from io import BytesIO

from hello import app, build_greeting, normalize_name


def run_wsgi_request(path="/", method="GET", body=b""):
    status_holder = {}

    def start_response(status, headers):
        status_holder["status"] = status
        status_holder["headers"] = headers

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "CONTENT_LENGTH": str(len(body)),
        "wsgi.input": BytesIO(body),
    }

    response = b"".join(app(environ, start_response)).decode("utf-8")
    return status_holder["status"], dict(status_holder["headers"]), response


def test_build_greeting_returns_expected_text():
    assert build_greeting("Alice") == "Hello, Alice"


def test_normalize_name_trims_whitespace():
    assert normalize_name("  Alice  ") == "Alice"


def test_get_renders_form():
    status, headers, response = run_wsgi_request()

    assert status == "200 OK"
    assert "text/html" in headers["Content-Type"]
    assert "<form method='post' action='/'>" in response
    assert "name='name'" in response


def test_post_with_valid_name_shows_greeting():
    body = b"name=Alice"
    status, _, response = run_wsgi_request(method="POST", body=body)

    assert status == "200 OK"
    assert "Hello, Alice" in response


def test_post_with_invalid_name_shows_error():
    body = b"name=+++"
    status, _, response = run_wsgi_request(method="POST", body=body)

    assert status == "200 OK"
    assert "Please provide a valid name." in response

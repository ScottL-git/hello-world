"""Small testable web app that greets a user by name."""

from __future__ import annotations

from html import escape
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server


def build_greeting(name: str) -> str:
    """Return greeting text for a valid name."""
    return f"Hello, {name}"


def normalize_name(raw_name: str) -> str:
    """Normalize a name by trimming whitespace."""
    return raw_name.strip()


def render_page(name: str = "", message: str = "", error: str = "") -> str:
    """Render the greeting page."""
    safe_name = escape(name)
    safe_message = escape(message)
    safe_error = escape(error)

    message_html = f"<p>{safe_message}</p>" if safe_message else ""
    error_html = f"<p style='color: red;'>{safe_error}</p>" if safe_error else ""

    return f"""<!doctype html>
<html lang='en'>
  <head>
    <meta charset='utf-8'>
    <title>Hello App</title>
  </head>
  <body>
    <h1>Hello App</h1>
    <form method='post' action='/'>
      <label for='name'>Name</label>
      <input id='name' name='name' type='text' value='{safe_name}' />
      <button type='submit'>Greet</button>
    </form>
    {message_html}
    {error_html}
  </body>
</html>
"""


def app(environ, start_response):
    """WSGI entrypoint for the hello web app."""
    method = environ.get("REQUEST_METHOD", "GET").upper()

    if method == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", "0") or "0")
        except ValueError:
            content_length = 0

        body = environ["wsgi.input"].read(content_length).decode("utf-8")
        form_data = parse_qs(body)
        raw_name = form_data.get("name", [""])[0]
        name = normalize_name(raw_name)

        if name:
            page = render_page(name=name, message=build_greeting(name))
        else:
            page = render_page(name=raw_name, error="Please provide a valid name.")
    else:
        page = render_page()

    body_bytes = page.encode("utf-8")
    headers = [
        ("Content-Type", "text/html; charset=utf-8"),
        ("Content-Length", str(len(body_bytes))),
    ]
    start_response("200 OK", headers)
    return [body_bytes]


def main() -> int:
    """Run a local development server."""
    with make_server("127.0.0.1", 8000, app) as server:
        print("Serving on http://127.0.0.1:8000")
        server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

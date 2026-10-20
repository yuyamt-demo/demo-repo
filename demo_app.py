# Synthetic security training fixture. Never deploy or expose publicly.
# Deliberately vulnerable: query input is interpolated into SQL.
import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


DB = sqlite3.connect(":memory:")
DB.executescript("CREATE TABLE notes (id INTEGER, owner TEXT, body TEXT); INSERT INTO notes VALUES (1, 'alice', 'Synthetic private note'), (2, 'bob', 'Synthetic second note');")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        owner = query.get("owner", ["alice"])[0]
        sql = f"SELECT id, body FROM notes WHERE owner = '{owner}'"
        rows = DB.execute(sql).fetchall()
        body = json.dumps(rows).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()


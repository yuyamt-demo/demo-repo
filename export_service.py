"""Synthetic security review fixture. Do not deploy this module.

WSGI export endpoint: HTTP query input is untrusted. No authentication middleware
is configured. The function is provided for static scan review only; this
repository has no server launcher or deployment job for it.
"""
import subprocess
from urllib.parse import parse_qs


def application(environ, start_response):
    if environ.get("PATH_INFO") != "/api/export":
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Not found"]
    query = parse_qs(environ.get("QUERY_STRING", ""))
    folder = query.get("folder", ["synthetic-notes"])[0]
    # Regression under review: untrusted folder is concatenated into a shell command.
    result = subprocess.run(
        "tar -czf /tmp/synthetic-export.tar.gz " + folder,
        shell=True,
        capture_output=True,
        text=True,
        timeout=5,
    )
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [result.stdout.encode(), result.stderr.encode()]

"""Vercel serverless — generates bulk employee CSV."""

import csv
import io
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from employee_generator import CSV_HEADERS, random_employee


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        try:
            count = max(1, min(5000, int(params.get("count", ["10"])[0])))
        except (ValueError, TypeError):
            count = 10

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for _ in range(count):
            writer.writerow(random_employee())

        data = buf.getvalue().encode()
        filename = f"employees_{count}.csv"

        self.send_response(200)
        self.send_header("Content-Type", "text/csv")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/csv")
        self.end_headers()

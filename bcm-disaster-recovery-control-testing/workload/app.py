#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sqlite3

DB_PATH = "/data/transactions.db"
HOST = "0.0.0.0"
PORT = 8080


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps(
                    {
                        "status": "healthy",
                        "database": DB_PATH
                    }
                ).encode()
            )
            return

        if self.path == "/transactions":
            conn = sqlite3.connect(DB_PATH)

            rows = conn.execute("""
                SELECT id, created_at, amount, status
                FROM transactions
                ORDER BY id DESC
                LIMIT 20
            """).fetchall()

            conn.close()

            data = [
                {
                    "id": row[0],
                    "created_at": row[1],
                    "amount": row[2],
                    "status": row[3],
                }
                for row in rows
            ]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            return

        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    init_db()
    HTTPServer((HOST, PORT), Handler).serve_forever()

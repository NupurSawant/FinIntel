"""
SQL Service - PostgreSQL ingestion and read-only query execution.

Two separate database connections are used, deliberately:
  - Admin connection (PG_ADMIN_USER): used ONLY by ingest_sql_file() to run
    an uploaded .sql file (CREATE TABLE / INSERT / etc). This is the only
    code path in the entire service that can write anything.
  - Read-only connection (PG_READONLY_USER): used ONLY by run_readonly_query(),
    which is what the SQL Agent's tool actually calls when answering
    questions. This role has SELECT-only DB-level grants (see setup SQL),
    plus the connection itself is opened with
    default_transaction_read_only=on as a second, independent layer of
    defense, plus a regex check rejecting anything that isn't a SELECT as a
    third layer, before the query ever reaches Postgres.
"""

import logging
import os
import re

import psycopg2
import psycopg2.extras

logger = logging.getLogger("finance_workflow")

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "9000")
PG_DATABASE = os.getenv("PG_DATABASE", "finance_db")

PG_ADMIN_USER = os.getenv("PG_ADMIN_USER", "postgres")
PG_ADMIN_PASSWORD = os.getenv("PG_ADMIN_PASSWORD", "")

PG_READONLY_USER = os.getenv("PG_READONLY_USER", "finance_readonly")
PG_READONLY_PASSWORD = os.getenv("PG_READONLY_PASSWORD", "")

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|TRUNCATE|GRANT|REVOKE)\b",
    re.IGNORECASE,
)


def _admin_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_ADMIN_USER,
        password=PG_ADMIN_PASSWORD,
    )


def _readonly_connection():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_READONLY_USER,
        password=PG_READONLY_PASSWORD,
        options="-c default_transaction_read_only=on",
    )


def ingest_sql_file(file_path: str) -> dict:
    """
    Executes an uploaded .sql file (schema + data) using the admin
    connection. Runs inside a transaction - if anything in the script
    fails, nothing is committed.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        sql_text = f.read()

    conn = _admin_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql_text)
        logger.info("Ingested SQL file: %s", file_path)
    finally:
        conn.close()

    return {"tables": list_tables()}


def list_tables() -> list[str]:
    conn = _admin_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """)
            return [row[0] for row in cur.fetchall()]
    finally:
        conn.close()


def get_schema_description() -> str:
    """
    Human-readable schema description (table + column names/types) for every
    table currently in the public schema. Injected into the SQL Agent's task
    context at query time, the same way 'Available Documents' is injected
    for the RAG Agent - the tool itself stays schema-agnostic.
    """
    conn = _admin_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position;
                """)
            rows = cur.fetchall()
    finally:
        conn.close()

    if not rows:
        return "No tables currently exist in the database. No SQL file has been uploaded yet."

    tables: dict[str, list[str]] = {}
    for table_name, column_name, data_type in rows:
        tables.setdefault(table_name, []).append(f"{column_name} {data_type}")

    lines = []
    for table_name, columns in tables.items():
        lines.append(f"{table_name}(\n  " + ",\n  ".join(columns) + "\n)")
    return "\n\n".join(lines)


def run_readonly_query(query: str) -> str:
    """
    Executes a read-only SQL SELECT query using the read-only role.
    Three independent layers reject non-SELECT statements:
      1. This regex check, before anything reaches Postgres
      2. default_transaction_read_only=on on the connection itself
      3. The finance_readonly role's DB-level grants (SELECT only)
    """
    stripped = query.strip().rstrip(";")

    if not stripped.lower().startswith("select"):
        return "Rejected: only SELECT statements are permitted."
    if FORBIDDEN_KEYWORDS.search(stripped):
        return "Rejected: query contains a forbidden write/DDL keyword."

    conn = _readonly_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(stripped)
            rows = cur.fetchall()
    except psycopg2.Error as e:
        return f"SQL execution error: {e}"
    finally:
        conn.close()

    if not rows:
        return "Query executed successfully but returned no rows."

    columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    lines = [header, separator]
    for row in rows[:50]:
        lines.append(
            "| "
            + " | ".join(str(row[c]) if row[c] is not None else "" for c in columns)
            + " |"
        )
    if len(rows) > 50:
        lines.append(f"\n*(Note: {len(rows) - 50} additional rows truncated)*")
    return "\n".join(lines)

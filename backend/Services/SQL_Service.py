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

from Services.DB_Service import get_admin_connection, get_readonly_connection

FORBIDDEN_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|TRUNCATE|GRANT|REVOKE)\b",
    re.IGNORECASE,
)


def _admin_connection():
    return get_admin_connection()


def _readonly_connection():
    return get_readonly_connection()


def ingest_sql_content(sql_text: str) -> dict:
    """
    Executes SQL content string (schema + data) using the admin
    connection. Runs inside a transaction - if anything in the script
    fails, nothing is committed.
    """
    conn = _admin_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql_text)
        logger.info("Ingested SQL content successfully.")
    finally:
        conn.close()

    return {"tables": list_tables()}


def ingest_sql_file(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8-sig") as f:
        sql_text = f.read()
    return ingest_sql_content(sql_text)


def list_tables() -> list[str]:
    try:
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
    except Exception as e:
        logger.warning("PostgreSQL connection unavailable: %s", e)
        return []


def get_schema_description() -> str:
    """
    Human-readable schema description (table + column names/types) for every
    table currently in the public schema. Injected into the SQL Agent's task
    context at query time, the same way 'Available Documents' is injected
    for the RAG Agent - the tool itself stays schema-agnostic.
    """
    try:
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
    except Exception as e:
        logger.warning("PostgreSQL connection unavailable: %s", e)
        return "No tables currently exist in the database. Database is currently unconfigured."

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

    Returned output is formatted for clear human reading instead of a raw
    pipe-delimited dump.
    """
    stripped = query.strip().rstrip(";")

    if not stripped.lower().startswith("select"):
        return "Rejected: only SELECT statements are permitted."
    if FORBIDDEN_KEYWORDS.search(stripped):
        return "Rejected: query contains a forbidden write/DDL keyword."

    try:
        conn = _readonly_connection()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(stripped)
                rows = cur.fetchall()
        finally:
            conn.close()
    except Exception as e:
        return f"SQL execution error or database unavailable: {e}"

    if not rows:
        return "Query executed successfully but returned no rows."

    columns = list(rows[0].keys())
    preview_rows = rows[:10]

    def display_value(value):
        if value is None:
            return "NULL"
        if isinstance(value, float):
            return f"{value:,.2f}"
        return str(value)

    lines = []
    lines.append("Query executed successfully.")
    lines.append(f"Returned {len(rows)} row(s) across {len(columns)} column(s).")
    lines.append(f"Columns: {', '.join(columns)}")
    lines.append("")
    lines.append("Result preview:")
    lines.append("| " + " | ".join(columns) + " |")
    lines.append("| " + " | ".join(["---"] * len(columns)) + " |")

    for row in preview_rows:
        formatted = [display_value(row.get(c)) for c in columns]
        lines.append("| " + " | ".join(formatted) + " |")

    if len(rows) > 10:
        lines.append("")
        lines.append(f"Note: {len(rows) - 10} additional rows are truncated in this preview.")

    return "\n".join(lines)
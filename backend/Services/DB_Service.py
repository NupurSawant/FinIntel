"""Managed PostgreSQL/Neon persistence for the Vercel deployment."""

import logging
import os

import psycopg2

logger = logging.getLogger("finance_workflow")


def get_neon_dsn() -> str:
    dsn = os.getenv("DATABASE_URL") or os.getenv("NEON_DB_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL (Neon/PostgreSQL) is required on Vercel.")
    return dsn


def _init_schema_and_tables(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE SCHEMA IF NOT EXISTS app_data;
            CREATE TABLE IF NOT EXISTS app_data.conversations (
                id SERIAL PRIMARY KEY, user_id TEXT NOT NULL,
                title TEXT NOT NULL DEFAULT 'New conversation',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS app_data.messages (
                id SERIAL PRIMARY KEY,
                conversation_id INT REFERENCES app_data.conversations(id) ON DELETE CASCADE,
                role TEXT NOT NULL, content TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL, password_hash VARCHAR(255) NOT NULL,
                verified BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
    conn.commit()


def get_admin_connection():
    conn = psycopg2.connect(get_neon_dsn())
    _init_schema_and_tables(conn)
    return conn


def get_readonly_connection():
    return psycopg2.connect(
        get_neon_dsn(), options="-c default_transaction_read_only=on"
    )

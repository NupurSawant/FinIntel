"""
Database Service - Manages PostgreSQL database connections dynamically
based on whether the application is running in Deployed state or Offline/Local state.
"""

import logging
import os
import psycopg2

logger = logging.getLogger("finance_workflow")

# Default Neon DB Online DSN (Used in Deployed State)
DEFAULT_NEON_DSN = (
    "postgresql://neondb_owner:npg_t8IbqdEcPV5Q@"
    "ep-misty-band-aygcnsg8.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require"
)


def is_deployed() -> bool:
    """
    Determines if the application is currently running in a Deployed state.
    Checks environment variables such as IS_DEPLOYED, VERCEL, ENVIRONMENT, NODE_ENV.
    """
    is_dep = os.getenv("IS_DEPLOYED", "").strip().lower()
    if is_dep in ("true", "1", "yes", "deployed", "production"):
        return True

    if os.getenv("VERCEL") == "1":
        return True

    env_name = os.getenv("ENVIRONMENT") or os.getenv("NODE_ENV") or os.getenv("APP_ENV") or ""
    if env_name.strip().lower() in ("production", "deployed", "prod"):
        return True

    return False


def get_neon_dsn() -> str:
    """Returns the Neon DB connection URI string."""
    return os.getenv("NEON_DB_URL") or os.getenv("DATABASE_URL") or DEFAULT_NEON_DSN


def _init_schema_and_tables(conn):
    """Ensures app_data schema, conversations, messages, and users tables exist."""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE SCHEMA IF NOT EXISTS app_data;

                CREATE TABLE IF NOT EXISTS app_data.conversations (
                    id SERIAL PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL DEFAULT 'New conversation',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS app_data.messages (
                    id SERIAL PRIMARY KEY,
                    conversation_id INT REFERENCES app_data.conversations(id) ON DELETE CASCADE,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    verified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()
    except Exception as e:
        logger.warning("Could not auto-initialize database tables: %s", e)
        conn.rollback()


def get_admin_connection():
    """
    Returns an Admin PostgreSQL connection.
    Connects to online Neon DB if deployed, or local PostgreSQL if offline.
    """
    if is_deployed():
        dsn = get_neon_dsn()
        logger.info("Connecting to Online Neon DB (Admin Mode)...")
        conn = psycopg2.connect(dsn)
    else:
        host = os.getenv("PG_HOST", "localhost")
        port = os.getenv("PG_PORT", "9000")
        dbname = os.getenv("PG_DATABASE", "finance_db")
        user = os.getenv("PG_ADMIN_USER", "postgres")
        password = os.getenv("PG_ADMIN_PASSWORD", "")
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
        )

    _init_schema_and_tables(conn)
    return conn


def get_readonly_connection():
    """
    Returns a Read-Only PostgreSQL connection.
    Enforces default_transaction_read_only=on on the connection session.
    """
    if is_deployed():
        dsn = get_neon_dsn()
        logger.info("Connecting to Online Neon DB (Read-Only Mode)...")
        return psycopg2.connect(
            dsn,
            options="-c default_transaction_read_only=on",
        )

    host = os.getenv("PG_HOST", "localhost")
    port = os.getenv("PG_PORT", "9000")
    dbname = os.getenv("PG_DATABASE", "finance_db")
    user = os.getenv("PG_READONLY_USER", "finance_readonly")
    password = os.getenv("PG_READONLY_PASSWORD", "")
    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        options="-c default_transaction_read_only=on",
    )

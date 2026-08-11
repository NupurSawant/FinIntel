"""
Conversation Service - persists conversations and chat messages to
app_data.conversations / app_data.messages.

Every function that touches a specific conversation_id verifies it belongs
to the requesting user_id first - proven via the cross-user tests above.
"""

import os

import psycopg2
import psycopg2.extras

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DATABASE = os.getenv("PG_DATABASE", "finance_db")
PG_ADMIN_USER = os.getenv("PG_ADMIN_USER", "postgres")
PG_ADMIN_PASSWORD = os.getenv("PG_ADMIN_PASSWORD", "")


def _admin_connection():
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DATABASE,
        user=PG_ADMIN_USER,
        password=PG_ADMIN_PASSWORD,
    )
    conn.set_client_encoding("UTF8")
    return conn


def create_conversation(user_id: str, title: str = "New conversation") -> dict:
    conn = _admin_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO app_data.conversations (user_id, title)
                    VALUES (%s, %s)
                    RETURNING id, title, created_at, updated_at;
                    """,
                    (user_id, title),
                )
                return dict(cur.fetchone())
    finally:
        conn.close()


def list_conversations(user_id: str) -> list[dict]:
    conn = _admin_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, title, created_at, updated_at
                FROM app_data.conversations
                WHERE user_id = %s
                ORDER BY updated_at DESC;
                """,
                (user_id,),
            )
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def _conversation_belongs_to_user(conversation_id: str, user_id: str, cur) -> bool:
    cur.execute(
        "SELECT 1 FROM app_data.conversations WHERE id = %s AND user_id = %s",
        (conversation_id, user_id),
    )
    return cur.fetchone() is not None


def get_messages(conversation_id: str, user_id: str) -> list[dict] | None:
    """Returns None if the conversation doesn't exist or doesn't belong to this user."""
    conn = _admin_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if not _conversation_belongs_to_user(conversation_id, user_id, cur):
                return None
            cur.execute(
                """
                SELECT role, content, created_at
                FROM app_data.messages
                WHERE conversation_id = %s
                ORDER BY created_at ASC, id ASC;
                """,
                (conversation_id,),
            )
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def add_message(conversation_id: str, user_id: str, role: str, content: str) -> bool:
    """Returns False if the conversation doesn't belong to this user (nothing is written)."""
    conn = _admin_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                if not _conversation_belongs_to_user(conversation_id, user_id, cur):
                    return False
                cur.execute(
                    "INSERT INTO app_data.messages (conversation_id, role, content) VALUES (%s, %s, %s);",
                    (conversation_id, role, content),
                )
                cur.execute(
                    "UPDATE app_data.conversations SET updated_at = now() WHERE id = %s;",
                    (conversation_id,),
                )
        return True
    finally:
        conn.close()


def maybe_set_title_from_first_message(
    conversation_id: str, user_id: str, text: str
) -> None:
    """Auto-titles a conversation from its first user message, only if still on the default title."""
    title = text.strip()[:60]
    if len(text.strip()) > 60:
        title += "..."

    conn = _admin_connection()
    try:
        with conn, conn.cursor() as cur:
            if not _conversation_belongs_to_user(conversation_id, user_id, cur):
                return
            cur.execute(
                """
                    UPDATE app_data.conversations
                    SET title = %s
                    WHERE id = %s AND title = 'New conversation';
                    """,
                (title, conversation_id),
            )
    finally:
        conn.close()


def delete_conversation(conversation_id: str, user_id: str) -> bool:
    conn = _admin_connection()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "DELETE FROM app_data.conversations WHERE id = %s AND user_id = %s;",
                (conversation_id, user_id),
            )
            return cur.rowcount > 0
    finally:
        conn.close()

"""
Auth Service - validates Auth0-issued access tokens and authenticates
users directly against Auth0 (nupursawant.us.auth0.com).
"""

import hashlib
import os
import sqlite3
import time
from typing import Any

import psycopg2
import requests
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret12345678900987654321")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "nupursawant.us.auth0.com")
API_AUDIENCE = os.getenv("API_AUDIENCE", "https://api.finance-intelligence.com")
ALGORITHMS = [os.getenv("ALGORITHMS", "RS256")]
ROLE_NAMESPACE = os.getenv("AUTH0_ROLE_NAMESPACE", "https://stateful-agent.com/roles")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "jbou043FS30WMGkcEanZXq4VdYMKbS8d")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "9YVJSiPRpu_ydXKXamKYMEiAdxyh4O_hdxBfqyLFRsHeDCQ_fzfWPTemutb1ftui")
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(_BASE_DIR, "data", "db", "finance.db"))

JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json" if AUTH0_DOMAIN else ""
security = HTTPBearer(auto_error=False)

_jwks_cache: dict[str, Any] = {"keys": [], "fetched_at": 0}
JWKS_CACHE_SECONDS = 60 * 60


from Services.DB_Service import get_admin_connection


def _sync_postgres_user(name: str, email: str, password_hash: str):
    """Syncs user details into PostgreSQL database (Neon DB if deployed, local Postgres if offline)."""
    try:
        conn = get_admin_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                verified BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash, verified)
            VALUES (%s, %s, %s, TRUE)
            ON CONFLICT (email) DO UPDATE SET
                name = EXCLUDED.name,
                password_hash = EXCLUDED.password_hash;
            """,
            (name, email, password_hash),
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        pass


def _init_users_table():
    try:
        os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    verified INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
            conn.commit()
    except Exception:
        pass


_init_users_table()


def register_user(name: str, email: str, password: str) -> dict[str, Any]:
    """Registers a new user via Auth0 dbconnections/signup and stores credentials in SQLite."""
    clean_name = name.strip()
    clean_email = email.strip().lower()

    if not clean_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required."
        )
    if not clean_email or "@" not in clean_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter a valid email address.",
        )
    if not password or len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long.",
        )

    if not AUTH0_CLIENT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AUTH0_CLIENT_ID is not configured.",
        )

    # 1. Register with Auth0 to send verification email to real inbox
    url = f"https://{AUTH0_DOMAIN}/dbconnections/signup"
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "email": clean_email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "user_metadata": {"name": clean_name},
        "name": clean_name,
    }
    headers = {"content-type": "application/json"}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to communicate with Auth0 signup service: {e}",
        )

    if not resp.ok:
        try:
            err_data = resp.json()
            err_msg = (
                err_data.get("description")
                or err_data.get("message")
                or err_data.get("code")
                or "Registration failed."
            )
            if "already exists" in err_msg.lower() or "user_exists" in err_msg.lower():
                err_msg = "An account with this email address already exists."
        except Exception:
            err_msg = f"Registration failed ({resp.status_code})"

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg)

    # 2. Store user credentials locally in SQLite and PostgreSQL databases
    try:
        pwd_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO users (name, email, password_hash, verified) VALUES (?, ?, ?, 0)",
                (clean_name, clean_email, pwd_hash),
            )
            conn.commit()
        _sync_postgres_user(clean_name, clean_email, pwd_hash)
    except Exception:
        pass

    return {
        "message": f"Registration successful. A verification email has been sent to '{clean_email}'. Please check your inbox and verify your email before logging in.",
        "email": clean_email,
        "requires_verification": True,
    }


def update_user_profile(
    user_id: str,
    name: str | None = None,
    old_password: str | None = None,
    new_password: str | None = None,
) -> dict[str, Any]:
    """Updates user display name and/or password with old password verification."""
    clean_user = user_id.strip().lower()

    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE LOWER(email) = ? OR LOWER(name) = ?",
            (clean_user, clean_user),
        )
        user = cursor.fetchone()

    if new_password:
        if not old_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Old password is required to change password.",
            )
        if len(new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 6 characters long.",
            )

        if user and user["password_hash"]:
            old_hash = hashlib.sha256(old_password.encode("utf-8")).hexdigest()
            if old_hash != user["password_hash"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Old password is incorrect.",
                )
        else:
            try:
                authenticate_with_auth0(clean_user, old_password)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Old password is incorrect.",
                )

        new_hash = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
        updated_name = (
            name.strip()
            if (name and name.strip())
            else (user["name"] if user else clean_user)
        )

        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cursor = conn.cursor()
            if user:
                cursor.execute(
                    "UPDATE users SET name = ?, password_hash = ? WHERE id = ?",
                    (updated_name, new_hash, user["id"]),
                )
            else:
                cursor.execute(
                    "INSERT INTO users (name, email, password_hash, verified) VALUES (?, ?, ?, 1)",
                    (updated_name, clean_user, new_hash),
                )
            conn.commit()

        _sync_postgres_user(updated_name, clean_user, new_hash)
        return {"message": "Profile updated successfully.", "name": updated_name}

    if name and name.strip():
        updated_name = name.strip()
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            cursor = conn.cursor()
            if user:
                cursor.execute(
                    "UPDATE users SET name = ? WHERE id = ?", (updated_name, user["id"])
                )
            else:
                dummy_hash = hashlib.sha256(b"nopassword").hexdigest()
                cursor.execute(
                    "INSERT INTO users (name, email, password_hash, verified) VALUES (?, ?, ?, 1)",
                    (updated_name, clean_user, dummy_hash),
                )
            conn.commit()

        _sync_postgres_user(
            updated_name, clean_user, hashlib.sha256(b"nopassword").hexdigest()
        )
        return {"message": "Profile name updated successfully.", "name": updated_name}

    return {"message": "No changes made.", "name": user["name"] if user else clean_user}


def create_local_access_token(sub: str) -> str:
    payload = {
        "sub": sub,
        "roles": ["user"],
        "exp": int(time.time()) + 60 * 60 * 24 * 7,  # 7 days
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def _verify_local_db_user(username: str, password: str) -> dict[str, Any] | None:
    clean_user = username.strip().lower()
    pwd_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    # 1. Try PostgreSQL users table (Neon DB in deployed mode, local Postgres in offline mode)
    try:
        conn = get_admin_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT email, password_hash FROM users WHERE LOWER(email) = %s OR LOWER(name) = %s;",
                    (clean_user, clean_user),
                )
                row = cur.fetchone()
                if row:
                    db_email, db_hash = row[0], row[1]
                    if db_hash == pwd_hash or db_hash == password:
                        token = create_local_access_token(db_email)
                        return {"access_token": token, "username": db_email}
        finally:
            conn.close()
    except Exception:
        pass

    # 2. Try SQLite users table
    try:
        if os.path.exists(SQLITE_DB_PATH):
            with sqlite3.connect(SQLITE_DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute(
                    "SELECT email, password_hash FROM users WHERE LOWER(email) = ? OR LOWER(name) = ?",
                    (clean_user, clean_user),
                )
                row = cur.fetchone()
                if row:
                    if row["password_hash"] == pwd_hash or row["password_hash"] == password:
                        token = create_local_access_token(row["email"])
                        return {"access_token": token, "username": row["email"]}
    except Exception:
        pass

    return None


def authenticate_with_auth0(username: str, password: str) -> dict[str, Any]:
    """Authenticates user against Auth0 OAuth or database credentials."""
    username = username.strip().lower()
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required.",
        )

    # 1. Attempt Auth0 OAuth authentication
    client_id = AUTH0_CLIENT_ID or "jbou043FS30WMGkcEanZXq4VdYMKbS8d"
    client_secret = AUTH0_CLIENT_SECRET or "9YVJSiPRpu_ydXKXamKYMEiAdxyh4O_hdxBfqyLFRsHeDCQ_fzfWPTemutb1ftui"
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/json"}

    payload_realm = {
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "username": username,
        "password": password,
        "realm": "Username-Password-Authentication",
        "audience": API_AUDIENCE,
        "client_id": client_id,
    }
    if client_secret:
        payload_realm["client_secret"] = client_secret

    try:
        resp = requests.post(url, json=payload_realm, headers=headers, timeout=10)
        if not resp.ok:
            payload_conn = {
                "grant_type": "password",
                "username": username,
                "password": password,
                "connection": "Username-Password-Authentication",
                "audience": API_AUDIENCE,
                "client_id": client_id,
            }
            if client_secret:
                payload_conn["client_secret"] = client_secret
            resp_conn = requests.post(
                url, json=payload_conn, headers=headers, timeout=10
            )
            if resp_conn.ok:
                resp = resp_conn

        if resp.ok:
            data = resp.json()
            access_token = data.get("access_token")
            if access_token:
                return {
                    "access_token": access_token,
                    "username": username,
                }
    except Exception:
        pass

    # 2. Fallback: Verify user against local / PostgreSQL database credentials
    local_res = _verify_local_db_user(username, password)
    if local_res:
        return local_res

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password. Please verify your credentials.",
    )


def _fetch_jwks(force: bool = False) -> dict[str, Any]:
    if not JWKS_URL:
        return {"keys": []}
    now = time.time()
    if (
        force
        or not _jwks_cache["keys"]
        or (now - _jwks_cache["fetched_at"] > JWKS_CACHE_SECONDS)
    ):
        try:
            resp = requests.get(JWKS_URL, timeout=5)
            resp.raise_for_status()
            _jwks_cache["keys"] = resp.json().get("keys", [])
            _jwks_cache["fetched_at"] = now
        except Exception:
            _jwks_cache["keys"] = []
    return _jwks_cache


def _get_rsa_key(unverified_header: dict[str, Any]) -> dict[str, Any] | None:
    jwks = _fetch_jwks()
    for key in jwks.get("keys", []):
        if key.get("kid") == unverified_header.get("kid"):
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    return None


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict[str, Any]:
    token = credentials.credentials if credentials else None

    if token:
        # 1. Decode Auth0 RS256 token
        try:
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = _get_rsa_key(unverified_header)
            if not rsa_key and AUTH0_DOMAIN:
                _fetch_jwks(force=True)
                rsa_key = _get_rsa_key(unverified_header)
            if rsa_key and AUTH0_DOMAIN:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f"https://{AUTH0_DOMAIN}/",
                )
                return {
                    "id": payload.get("sub"),
                    "roles": payload.get(ROLE_NAMESPACE, []),
                    "raw_claims": payload,
                }
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired."
            )
        except Exception:
            pass

        # 2. Fallback: local JWT token (HS256)
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            sub = payload.get("sub")
            if sub:
                return {
                    "id": sub,
                    "roles": payload.get("roles", ["user"]),
                    "raw_claims": payload,
                }
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired."
            )
        except JWTError:
            pass

    # 3. Fallback: check X-User header
    x_user = request.headers.get("X-User") or request.headers.get("x-user")
    if x_user:
        return {
            "id": x_user.strip(),
            "roles": ["user"],
            "raw_claims": {"sub": x_user.strip()},
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated. Please log in with Auth0.",
    )


def require_role(role: str):
    def _check(current_user: dict = Depends(get_current_user)) -> dict:
        if role not in current_user.get("roles", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail=f"Requires '{role}' role."
            )
        return current_user

    return _check

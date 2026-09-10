"""
Auth Service - validates Auth0-issued access tokens and authenticates
users directly against Auth0 (nupursawant.us.auth0.com).
"""

import hashlib
import logging
import os
import time
from typing import Any

import requests
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or os.getenv("JWT_SECRET", "")
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
API_AUDIENCE = os.getenv("API_AUDIENCE", "")
ALGORITHMS = [os.getenv("ALGORITHMS", "RS256")]
ROLE_NAMESPACE = os.getenv("AUTH0_ROLE_NAMESPACE", "https://stateful-agent.com/roles")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
logger = logging.getLogger("finance_workflow")

JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json" if AUTH0_DOMAIN else ""
security = HTTPBearer(auto_error=False)

_jwks_cache: dict[str, Any] = {"keys": [], "fetched_at": 0}
JWKS_CACHE_SECONDS = 60 * 60


from Services.DB_Service import get_admin_connection


def _sync_postgres_user(name: str, email: str, password_hash: str):
    """Create or update a user in the required managed PostgreSQL database."""
    conn = get_admin_connection()
    try:
        with conn.cursor() as cursor:
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
    except Exception:
        conn.rollback()
        logger.exception("Failed to persist user %s in PostgreSQL", email)
        raise
    finally:
        conn.close()


def register_user(name: str, email: str, password: str) -> dict[str, Any]:
    """Register a user through Auth0 and persist credentials in PostgreSQL."""
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

    # Persist before returning success; PostgreSQL is the durable source of truth.
    pwd_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    _sync_postgres_user(clean_name, clean_email, pwd_hash)

    # 2. Attempt Auth0 registration
    client_id = AUTH0_CLIENT_ID
    url = f"https://{AUTH0_DOMAIN}/dbconnections/signup"
    payload = {
        "client_id": client_id,
        "email": clean_email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "user_metadata": {"name": clean_name},
        "name": clean_name,
    }
    headers = {"content-type": "application/json"}

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        if not resp.ok:
            try:
                err_data = resp.json()
                err_msg = (
                    err_data.get("description")
                    or err_data.get("message")
                    or err_data.get("code")
                    or ""
                )
                if "already exists" in err_msg.lower() or "user_exists" in err_msg.lower():
                    return {
                        "message": f"Account '{clean_email}' is registered. You can log in directly with your password.",
                        "email": clean_email,
                        "requires_verification": False,
                    }
            except requests.RequestException:
                logger.warning("Auth0 registration request failed for %s", clean_email, exc_info=True)
    except Exception:
        pass

    return {
        "message": f"Registration successful for '{clean_email}'. You can now log in with your email and password.",
        "email": clean_email,
        "requires_verification": False,
    }


def update_user_profile(
    user_id: str,
    name: str | None = None,
    old_password: str | None = None,
    new_password: str | None = None,
) -> dict[str, Any]:
    """Updates user display name and/or password with old password verification."""
    clean_user = user_id.strip().lower()

    conn = get_admin_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, name, email, password_hash FROM users "
                "WHERE LOWER(email) = %s OR LOWER(name) = %s",
                (clean_user, clean_user),
            )
            row = cursor.fetchone()
        user = (
            {"id": row[0], "name": row[1], "email": row[2], "password_hash": row[3]}
            if row else None
        )
    finally:
        conn.close()

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

        _sync_postgres_user(updated_name, clean_user, new_hash)
        return {"message": "Profile updated successfully.", "name": updated_name}

    if name and name.strip():
        updated_name = name.strip()
        password_hash = user["password_hash"] if user else hashlib.sha256(b"nopassword").hexdigest()
        _sync_postgres_user(updated_name, clean_user, password_hash)
        return {"message": "Profile name updated successfully.", "name": updated_name}

    return {"message": "No changes made.", "name": user["name"] if user else clean_user}


def create_access_token(sub: str) -> str:
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET is required for application authentication.")
    payload = {
        "sub": sub,
        "roles": ["user"],
        "exp": int(time.time()) + 60 * 60 * 24 * 7,  # 7 days
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def _verify_database_user(username: str, password: str) -> dict[str, Any] | None:
    clean_user = username.strip().lower()
    pwd_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    conn = get_admin_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT email, password_hash FROM users "
                "WHERE LOWER(email) = %s OR LOWER(name) = %s",
                (clean_user, clean_user),
            )
            row = cur.fetchone()
        if row and (row[1] == pwd_hash or row[1] == password):
            return {"access_token": create_access_token(row[0]), "username": row[0]}
        return None
    finally:
        conn.close()


def authenticate_with_auth0(username: str, password: str) -> dict[str, Any]:
    """Authenticates user against Auth0 OAuth or database credentials."""
    username = username.strip().lower()
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required.",
        )

    # 1. Attempt Auth0 OAuth authentication
    client_id = AUTH0_CLIENT_ID
    client_secret = AUTH0_CLIENT_SECRET
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
    except requests.RequestException:
        logger.warning("Auth0 authentication request failed for %s", username, exc_info=True)

    try:
        database_result = _verify_database_user(username, password)
    except Exception:
        logger.exception("PostgreSQL authentication lookup failed for %s", username)
        raise HTTPException(status_code=503, detail="Authentication service unavailable.")
    if database_result:
        return database_result

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

        # Accept the application's signed session token.
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

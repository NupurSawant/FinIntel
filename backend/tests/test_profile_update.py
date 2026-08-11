import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib
import sqlite3

import pytest
from fastapi import HTTPException

from Services.Auth_Service import SQLITE_DB_PATH, update_user_profile


def test_profile_name_and_password_update():
    email = "profile_test@example.com"
    old_pwd = "oldpassword123"
    new_pwd = "newpassword456"

    # Insert test user directly into SQLite
    os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
    old_hash = hashlib.sha256(old_pwd.encode("utf-8")).hexdigest()
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO users (name, email, password_hash, verified) VALUES (?, ?, ?, 1)",
            ("Original Name", email, old_hash),
        )
        conn.commit()

    # 1. Update Name
    res1 = update_user_profile(user_id=email, name="Updated Name")
    assert res1["name"] == "Updated Name"

    # 2. Update Password with wrong old password -> Should raise HTTPException 400
    with pytest.raises(HTTPException) as exc_info:
        update_user_profile(
            user_id=email, old_password="wrongpassword", new_password=new_pwd
        )
    assert exc_info.value.status_code == 400
    assert "Old password is incorrect" in exc_info.value.detail

    # 3. Update Password with correct old password -> Should succeed
    res2 = update_user_profile(
        user_id=email, old_password=old_pwd, new_password=new_pwd
    )
    assert "successfully" in res2["message"]

    # 4. Verify new password works and old password no longer works
    with pytest.raises(HTTPException):
        update_user_profile(
            user_id=email, old_password=old_pwd, new_password="anotherpassword"
        )

    res3 = update_user_profile(
        user_id=email, old_password=new_pwd, new_password="finalpassword789"
    )
    assert "successfully" in res3["message"]

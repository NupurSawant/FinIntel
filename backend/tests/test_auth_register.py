import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register_validation():
    # Test missing name
    res1 = client.post(
        "/auth/register",
        json={"name": "", "email": "test@example.com", "password": "password123"},
    )
    assert res1.status_code == 400

    # Test invalid email
    res2 = client.post(
        "/auth/register",
        json={"name": "Test User", "email": "invalidemail", "password": "password123"},
    )
    assert res2.status_code == 400

    # Test short password
    res3 = client.post(
        "/auth/register",
        json={"name": "Test User", "email": "test@example.com", "password": "123"},
    )
    assert res3.status_code == 400

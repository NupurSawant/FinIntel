import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Services.SQL_Service import FORBIDDEN_KEYWORDS, run_readonly_query


def test_forbidden_sql_keywords():
    assert FORBIDDEN_KEYWORDS.search("DROP TABLE users") is not None
    assert FORBIDDEN_KEYWORDS.search("DELETE FROM accounts") is not None
    assert FORBIDDEN_KEYWORDS.search("UPDATE portfolios SET risk = 0") is not None
    assert FORBIDDEN_KEYWORDS.search("INSERT INTO logs VALUES(1)") is not None
    assert FORBIDDEN_KEYWORDS.search("SELECT * FROM portfolio_holdings") is None


def test_run_readonly_query_blocks_non_select():
    res = run_readonly_query("DROP TABLE asset_risk_logs;")
    assert "only SELECT statements are permitted" in res


def test_run_readonly_query_formats_readable_result(monkeypatch):
    class FakeRowCursor:
        def __init__(self):
            self.rows = [
                {"asset_name": "NVDA Core Equity", "risk_score": 8.9},
                {"asset_name": "Crypto Emerging ETF", "risk_score": 8.5},
            ]

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def execute(self, query):
            return None

        def fetchall(self):
            return self.rows

    class FakeConn:
        def cursor(self, cursor_factory=None):
            return FakeRowCursor()

        def close(self):
            return None

    monkeypatch.setattr(
        "Services.SQL_Service._readonly_connection",
        lambda: FakeConn(),
    )

    res = run_readonly_query("SELECT asset_name, risk_score FROM portfolio_holdings LIMIT 2")

    assert "Query executed successfully" in res
    assert "Returned 2 row(s)" in res
    assert "NVDA Core Equity" in res
    assert "| asset_name | risk_score |" in res

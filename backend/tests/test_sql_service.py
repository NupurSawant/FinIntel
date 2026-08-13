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

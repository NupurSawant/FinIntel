import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Services.Ollama_Router_Service import (
    _mentions_uploaded_document,
    _mentions_database_query,
    classify_and_maybe_answer,
)


def test_document_reference_keywords():
    assert _mentions_uploaded_document("Check the uploaded PDF report") is True
    assert _mentions_uploaded_document("Show me company policy document") is True
    assert _mentions_uploaded_document("Hello, how are you?") is False


def test_database_query_keywords():
    assert _mentions_database_query("Select all rows from portfolio_holdings") is True
    assert _mentions_database_query("Show sql table records") is True
    assert _mentions_database_query("What is asset allocation?") is False


def test_classify_document_override():
    res = classify_and_maybe_answer("From Attached Document - Explain Credit Risk")
    assert res["classification"] == "complex"
    assert res["answer"] == ""


def test_classify_database_override():
    res = classify_and_maybe_answer("Query the database table for asset risk logs")
    assert res["classification"] == "complex"
    assert res["answer"] == ""

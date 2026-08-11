from Observability.langfuse_client import coerce_for_langfuse


def test_coerce_for_langfuse_serializes_exception_details():
    payload = {
        "query": "what is a mutual fund?",
        "error": ValueError("boom"),
    }

    result = coerce_for_langfuse(payload)

    assert result["query"] == "what is a mutual fund?"
    assert result["error"]["type"] == "ValueError"
    assert result["error"]["message"] == "boom"

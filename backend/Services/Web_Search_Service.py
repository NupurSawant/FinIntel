"""
Web Search Service - live web search via Tavily, for current/real-world
information that isn't in our internal database or uploaded documents
(current events, general definitions, things outside our synthetic
portfolio data).

Fails gracefully: if TAVILY_API_KEY isn't set, or the API call fails for
any reason (network issue, rate limit, bad key), this returns an empty
list rather than raising - the calling tool then reports "no results"
to the agent instead of crashing the whole crew run.
"""

import logging
import os

logger = logging.getLogger("finance_workflow")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
TAVILY_SEARCH_DEPTH = os.getenv("TAVILY_SEARCH_DEPTH", "advanced")
TAVILY_MAX_RESULTS = int(os.getenv("TAVILY_MAX_RESULTS", "5"))


def web_search(query: str, max_results: int = None) -> list[dict]:
    if not TAVILY_API_KEY:
        logger.warning(
            "Web search called but TAVILY_API_KEY is not set - returning no results."
        )
        return []

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(
            query=query,
            max_results=max_results or TAVILY_MAX_RESULTS,
            search_depth=TAVILY_SEARCH_DEPTH,
            include_answer=True,
        )
    except Exception as e:
        logger.warning("Web search failed (%s) - returning no results.", e)
        return []

    results: list[dict] = []

    answer = response.get("answer")
    if answer:
        results.append({"title": "Tavily AI summary", "url": "", "content": answer})

    for r in response.get("results", []):
        results.append(
            {
                "title": r.get("title", "Untitled"),
                "url": r.get("url", ""),
                "content": r.get("content", ""),
            }
        )

    return results

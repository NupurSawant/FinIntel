from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from Services.Web_Search_Service import web_search


class WebSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="Search query for current, real-world information not available in our internal data or uploaded documents.",
    )


class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = (
        "Searches the live web for current, real-world financial/market information - "
        "e.g. today's stock prices, recent market news, current events, or general "
        "financial definitions - that isn't in our internal portfolio database or "
        "uploaded documents. Always cite the source URL when using information from "
        "this tool. If no results are found, say so explicitly rather than guessing."
    )
    args_schema: type[BaseModel] = WebSearchInput

    def _run(self, query: str) -> str:
        results = web_search(query)
        if not results:
            return (
                "No web search results found, or web search is not configured "
                "(missing TAVILY_API_KEY). Answer using internal data or general "
                "knowledge instead, and note that live web data wasn't available."
            )

        formatted = []
        for r in results:
            source_line = f"[SOURCE: {r['title']}" + (
                f" | {r['url']}]" if r["url"] else "]"
            )
            formatted.append(f"{source_line}\n{r['content']}\n")
        return "\n---\n".join(formatted)

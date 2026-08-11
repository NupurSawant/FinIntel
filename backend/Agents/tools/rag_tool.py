from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from Services.RAG_Service import rag_service


class RAGSearchInput(BaseModel):
    query: str = Field(
        ...,
        description="Natural language question to search the uploaded documents for.",
    )
    top_k: int = Field(3, description="Number of top matching passages to return.")


class RAGSearchTool(BaseTool):
    name: str = "document_search"
    description: str = (
        "Searches documents the user has uploaded (PDF, DOCX, or TXT) and returns "
        "the most relevant passages along with their exact source filename, for "
        "grounding answers with traceable citations. Returns an empty result if no "
        "documents have been uploaded yet."
    )
    args_schema: type[BaseModel] = RAGSearchInput

    def _run(self, query: str, top_k: int = 3) -> str:
        results = rag_service.search(query, k=top_k)
        if not results:
            return "No uploaded documents matched this query, or no documents have been uploaded yet."
        formatted = []
        for r in results:
            formatted.append(
                f"[SOURCE: {r['source']} | relevance={r['score']:.3f}]\n{r['text']}\n"
            )
        return "\n---\n".join(formatted)

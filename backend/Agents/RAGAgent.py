from crewai import Agent

from Agents.tools import RAGSearchTool
from llm import llm


def RAGAgent(llm_config=llm) -> Agent:
    agent_llm = llm_config.get_llm()
    rag_tool = RAGSearchTool()

    rag_agent = Agent(
        role="RAG Agent",
        goal=(
            "Answer questions using ONLY the content of documents the user has uploaded. "
            "Always search the uploaded documents first before answering. Cite the exact "
            "source filename for every claim. If the uploaded documents don't contain "
            "relevant information, say so explicitly instead of answering from general "
            "knowledge."
        ),
        backstory=(
            "You are a document analyst who never fabricates a source. You only report "
            "what the document search tool actually returns, and clearly say when no "
            "uploaded document is relevant to the question."
        ),
        tools=[rag_tool],
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
    )
    return rag_agent

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
            "Always search uploaded documents first and cite source filenames for claims. "
            "Adapt response structure dynamically to the user's query—providing direct conversational answers "
            "or structured summaries based on what was asked. If uploaded documents lack relevant information, "
            "say so explicitly."
        ),
        backstory=(
            "You are a meticulous document analyst who cites exact source files and presents document insights "
            "in a clean, natural conversational style tailored to the user's prompt."
        ),
        tools=[rag_tool],
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
    )
    return rag_agent

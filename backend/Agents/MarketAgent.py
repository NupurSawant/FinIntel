from crewai import Agent

from Agents.tools.web_search_tool import WebSearchTool
from llm import llm


def MarketAgent(llm_config=llm) -> Agent:
    agent_llm = llm_config.get_llm()

    market_agent = Agent(
        role="Market Agent",
        goal=(
            "Evaluate portfolio performance relative to benchmarks across sectors and regions, "
            "identifying which holdings drive performance and why. Adapt your response format dynamically "
            "to match the analyst's query—providing direct answers, clear bullet points, or comparison tables "
            "as appropriate."
        ),
        backstory=(
            "You are a market analyst who tracks sector rotation, benchmark-relative performance, "
            "and macro trend signals. You back every claim with computed numbers and live search tools, "
            "delivering natural and dynamically structured responses tailored to user requests."
        ),
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
        tools=[WebSearchTool()],
    )

    return market_agent

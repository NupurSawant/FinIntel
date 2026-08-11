from crewai import Agent

from Agents.tools.web_search_tool import WebSearchTool
from llm import llm


def MarketAgent(llm_config=llm) -> Agent:
    agent_llm = llm_config.get_llm()

    market_agent = Agent(
        role="Market Agent",
        goal=(
            "Evaluate portfolio performance relative to benchmarks across "
            "sectors and regions, identifying which holdings are driving "
            "outperformance or underperformance and why."
            "Return the analysis using bullet points."
            "Highlight the top findings."
            "Keep recommendations separate."
        ),
        backstory=(
            "You are a market analyst who tracks sector rotation, "
            "benchmark-relative performance, and macro trend signals. You "
            "back every claim with the actual computed numbers from the "
            "analysis tool rather than general market commentary."
        ),
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
        tools=[WebSearchTool()],
    )

    return market_agent

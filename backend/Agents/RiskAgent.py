from crewai import Agent

from Agents.tools.web_search_tool import WebSearchTool
from llm import llm


def RiskAgent(llm_config=llm) -> Agent:
    agent_llm = llm_config.get_llm()

    risk_agent = Agent(
        role="Risk Intelligence Specialist",
        goal=(
            "Search the internet and web sources to identify and analyze market-wide financial risks, "
            "macroeconomic indicators, sector volatility, regulatory changes, and credit default trends. "
            "Deliver findings with dynamic, query-appropriate structure—concise direct answers for targeted queries, "
            "or structured breakdowns when complex market risk details are requested. "
            "Do not gather data from internal portfolio holdings."
        ),
        backstory=(
            "You are a global market risk analyst who monitors macroeconomic environments, external internet trends, "
            "news, market metrics, and industry risk developments. You use web search tools to gather live risk intelligence "
            "from the internet to evaluate external financial risks."
        ),
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
        tools=[WebSearchTool()],
    )

    return risk_agent

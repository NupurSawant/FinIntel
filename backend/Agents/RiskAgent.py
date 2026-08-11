from crewai import Agent

from Agents.tools.web_search_tool import WebSearchTool
from llm import llm


def RiskAgent(llm_config=llm) -> Agent:
    agent_llm = llm_config.get_llm()

    risk_agent = Agent(
        role="Risk Agent",
        goal=(
            "Identify and quantify risk exposures (such as concentration, volatility, or VaR) "
            "in the portfolio. Deliver findings with dynamic, query-appropriate structure—concise "
            "direct answers for targeted queries, or structured breakdowns when complex risk details are requested."
        ),
        backstory=(
            "You are a conservative risk manager responsible for flagging exposures before they become losses. "
            "You provide clear, well-structured financial risk insights dynamically adapted to the user's intent."
        ),
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
        tools=[WebSearchTool()],
    )

    return risk_agent

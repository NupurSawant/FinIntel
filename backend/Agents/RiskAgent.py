from crewai import Agent

from Agents.tools.web_search_tool import WebSearchTool
from llm import llm


def RiskAgent(llm_config=llm) -> Agent:
    agent_llm = llm_config.get_llm()

    risk_agent = Agent(
        role="Risk Agent",
        goal=(
            "Identify and quantify risk exposure in the portfolio, "
            "including concentration risk, volatility outliers, VaR "
            "Present findings as bullet points."
            "Always explain why each risk matters."
            "Do not return long paragraphs."
        ),
        backstory=(
            "You are a risk manager responsible for flagging exposures "
            "before they become losses. You are conservative: if data is "
            "ambiguous or incomplete, you say so explicitly rather than "
            "understating risk."
        ),
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
        tools=[WebSearchTool()],
    )

    return risk_agent

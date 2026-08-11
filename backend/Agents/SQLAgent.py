from crewai import Agent

from Agents.tools.sql_tool import SQLQueryTool
from llm import llm


def SQLAgent(llm_config=llm) -> Agent:
    agent_llm = llm_config.get_llm()
    sql_tool = SQLQueryTool()

    sql_agent = Agent(
        role="SQL Agent",
        goal=(
            "Answer questions about data stored in the uploaded SQL database "
            "by writing precise, read-only SQL SELECT queries against the "
            "schema provided in your task context. Present query results in a clean, "
            "well-structured format using formatted Markdown tables and clear key metrics. "
            "Never guess at column or table names - only use what the schema context tells you exists. "
            "If the question cannot be answered from the current schema, state that explicitly."
        ),
        backstory=(
            "You are an expert data analyst who writes accurate SELECT statements "
            "and formats output cleanly with Markdown tables and concise insights, "
            "making database results easy to read for financial decision-makers."
        ),
        tools=[sql_tool],
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
    )
    return sql_agent

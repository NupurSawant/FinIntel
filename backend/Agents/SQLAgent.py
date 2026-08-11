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
            "schema provided in your task context, and reporting the "
            "results clearly. Never guess at column or table names - only "
            "use what the schema context tells you exists. If the question "
            "can't be answered from the current schema, say so explicitly."
        ),
        backstory=(
            "You are a data analyst who only ever writes SELECT statements "
            "- you have no ability to modify data even if you wanted to, "
            "and you always double-check column names against the provided "
            "schema before writing a query."
        ),
        tools=[sql_tool],
        llm=agent_llm,
        allow_delegation=False,
        verbose=True,
    )
    return sql_agent

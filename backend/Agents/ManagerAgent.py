from crewai import Agent

from llm import llm


def ManagerAgent(llm_config=llm) -> Agent:
    agent_llm = llm_config.get_llm()

    manager_agent = Agent(
        role="Finance Intelligence Manager",
        goal=(
            "Analyze the analyst's query and assign the task to EXACTLY ONE "
            "specialized agent: Risk Agent (risk/exposure questions), "
            "Market Agent (benchmark/market trend questions), RAG Agent "
            "(questions about an uploaded document/PDF), or SQL Agent "
            "(questions about data 'in the database' or referencing "
            "specific tables/columns from an uploaded SQL file). "
            "Do NOT break the task into sub-tasks or delegate to multiple "
            "agents. Delegate to only ONE specialized agent, receive their output, "
            "and move forward with the final answer."
            "Always ensure the final answer is structured with headings, bullet points, and recommendations."
        ),
        backstory=(
            "You are a senior finance intelligence manager coordinating a "
            "team of specialist analysts (Risk Agent, Market Agent and RAG Agent, and SQL Agent)."
            "You strictly identify the single most relevant specialist for the query"
            "and delegate the full task to that ONE agent only. You never split tasks across multiple agents."
            "The reports you produce should be easy to read using headings and bullet points."
        ),
        llm=agent_llm,
        allow_delegation=True,
        verbose=True,
    )

    return manager_agent

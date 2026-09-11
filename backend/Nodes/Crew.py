import logging
import os

from crewai import Crew, Process, Task

from llm import llm
from Observability.langfuse_client import observe_span
from state import GraphState

logger = logging.getLogger("finance_workflow")
logging.basicConfig(level=getattr(logging, llm.LOG_LEVEL, logging.INFO))

from Agents.ManagerAgent import ManagerAgent
from Agents.MarketAgent import MarketAgent
from Agents.RAGAgent import RAGAgent
from Agents.RiskAgent import RiskAgent
from Agents.SQLAgent import SQLAgent
from Services.Market_Service import MarketService
from Services.RAG_Service import rag_service
from Services.SQL_Service import get_schema_description
from Utils.ticker_extractor import extract_tickers

_DATABASE_QUERY_KEYWORDS = [
    "database",
    "sql",
    "table",
    "row",
    "column",
    "record",
    "asset_risk_logs",
    "portfolio_holdings",
    "investment_decisions",
    "market_indicators",
    "portfolios",
    "risk score",
    "risk scores",
    "asset names",
    "from the database",
    "from database",
    "query",
]


def _is_database_query(query: str) -> bool:
    lowered = query.lower()
    return any(kw in lowered for kw in _DATABASE_QUERY_KEYWORDS)


def _is_document_query(query: str) -> bool:
    if _is_database_query(query):
        return False
    lowered = query.lower()
    return any(
        keyword in lowered
        for keyword in (
            "document",
            "attached",
            "attachment",
            "pdf",
            "report",
            "manual",
            "policy",
            "guideline",
            "uploaded",
        )
    )


def _run_google_document_answer(query: str) -> str:
    """Answer document questions with Gemini, keeping Groq out of the RAG path."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    passages = rag_service.search(query, k=5)
    if not passages:
        passages = rag_service.overview(chunks_per_doc=2)

    context_parts = []
    remaining_chars = 14000
    for passage in passages:
        text = passage.get("text", "")[:3500]
        part = f"Source: {passage.get('source', 'unknown')}\n{text}"
        if len(part) > remaining_chars:
            break
        context_parts.append(part)
        remaining_chars -= len(part)

    if not context_parts:
        return "I could not find any indexed content in the attached document."

    model = os.getenv("GOOGLE_RAG_MODEL", "gemini-2.0-flash")
    document_llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0,
    )
    prompt = (
        "Answer the user's question using only the supplied document passages. "
        "For a summary, cover the main purpose, key topics, important findings, "
        "risks or requirements, and practical conclusions. Cite source filenames. "
        "If the passages do not support a claim, say that it is not stated.\n\n"
        f"User question:\n{query}\n\nDocument passages:\n"
        + "\n\n---\n\n".join(context_parts)
    )
    response = document_llm.invoke(prompt)
    return str(response.content).strip()


def build_finance_crew(query: str, revision_instructions: str = "") -> Crew:
    manager = ManagerAgent(llm)
    market_agent = MarketAgent(llm)
    risk_agent = RiskAgent(llm)
    rag_agent = RAGAgent(llm)
    sql_agent = SQLAgent(llm)

    market_service = MarketService()

    symbols = extract_tickers(query)

    if symbols:
        detected_symbols = ", ".join(symbols)
        market_data = market_service.compare_assets(symbols)
    else:
        detected_symbols = "None"
        market_data = "No specific market symbols detected."

    available_documents = rag_service.list_documents()
    if available_documents:
        documents_note = (
            f"Documents currently uploaded and available to search: {', '.join(available_documents)}.\n\n"
            "Routing Rules:\n"
            "1. If the user asks about PDF documents, reports, manuals, policies, "
            "guidelines, attached documents, or uploaded PDFs, delegate to the RAG Agent.\n"
            "2. If the user asks about SQL tables, database records, uploaded database data, "
            "rows, columns, portfolio_holdings, asset_risk_logs, investment_decisions, "
            "market_indicators, or portfolios, delegate to the SQL Agent.\n"
            "3. The word 'uploaded' alone does NOT mean the query is about a PDF. "
            "Determine whether the uploaded resource is a PDF document or a SQL database "
            "before selecting an agent.\n"
            "4. Delegate to exactly ONE specialist."
        )
    else:
        documents_note = "No documents have been uploaded yet."

    database_schema = get_schema_description()

    is_database_query = _is_database_query(query)

    print("====================================")
    print("Detected Symbols:", detected_symbols)
    print("Market Data:", market_data)
    print("Available Documents:", available_documents)
    print("====================================")

    if is_database_query:
        task_description = (
            f"Analyst query:\n{query}\n\n"
            "This is a direct SQL/database query. Use the provided schema and SQL Agent to query the database and present the results in a clean, professional, and well-structured format.\n"
            "Formatting guidelines:\n"
            "- Present tabular query results using clean Markdown tables with column headers.\n"
            "- For aggregate or single-value metrics, present key numbers clearly in bold or bullet points.\n"
            "- Provide a brief 1-2 sentence explanation of what the retrieved database results represent.\n"
            "- Do not force heavy report templates (like 'Key Risks' or 'Recommendation') unless explicitly requested by the user.\n\n"
            f"Available Database Schema:\n{database_schema}\n"
        )
        task_expected_output = (
            "Return a clean, well-structured response with formatted Markdown tables or key metrics alongside a concise explanation of the database results."
        )
    else:
        task_description = (
            f"Analyst query:\n{query}\n\n"
            "Analyze the analyst's request carefully.\n"
            "Determine whether the request requires:\n"
            "- SQL database records\n"
            "- PDF/document retrieval\n"
            "- Market data\n"
            "- Internet financial risk analysis\n\n"
            "Always prioritize SQL Agent when the user requests database tables, "
            "database records, uploaded database data, rows, columns, or SQL schema.\n"
            "If the query contains any of these terms:\n"
            "database\n"
            "SQL\n"
            "table\n"
            "record\n"
            "row\n"
            "column\n"
            "asset_risk_logs\n"
            "portfolio_holdings\n"
            "investment_decisions\n"
            "market_indicators\n"
            "portfolios\n"
            "delegate to SQL Agent.\n\n"
            "Always prioritize RAG Agent only when the user requests information "
            "contained in uploaded PDF documents, reports, manuals, policies, or guidelines.\n"
            "Delegate to EXACTLY ONE specialist.\n\n"
            f"Detected Symbols:\n{detected_symbols}\n\n"
            f"Market Data:\n{market_data}\n\n"
            "Use the market data above whenever it is relevant.\n"
            "Do not invent prices, volatility, or market statistics.\n"
            "If no market data is available, answer using general financial knowledge and clearly mention that no live market data was retrieved.\n\n"
            f"Uploaded Documents:\n{documents_note}\n\n"
            f"Available Database Schema:\n{database_schema}\n\n"
            "Live Web Search:\n"
            "Market Agent and Risk Agent can search the live web for current stock prices, "
            "recent market news, macroeconomic risks, sector risk trends, regulatory changes, "
            "or general financial risk information from internet sources. "
            "Use Risk Agent with web search to analyze market-wide risks, macroeconomic threats, "
            "and industry risk factors from external web sources rather than internal portfolio database holdings.\n\n"
            "DYNAMIC RESPONSE STYLING & STRUCTURE:\n"
            "- Act as a natural, intelligent financial AI chat assistant.\n"
            "- Dynamically tailor the output structure to what the user's query specifically requests.\n"
            "- Do NOT force rigid static sections like 'Summary', 'Key Risks', 'Recommendation', or 'Sources' unless the user specifically asked for a formal report or risk analysis.\n"
            "- For simple or direct questions, answer directly and concisely in natural conversational prose.\n"
            "- For analytical, multi-faceted, or comparison requests, structure your response logically using relevant custom headings, bullet points, or markdown tables.\n"
            "- Naturally cite source documents or database tables when used.\n"
            "- Maintain a professional, clean, and highly readable chat response style at all times."
        )
        task_expected_output = (
            "A clear, natural, and dynamically structured response tailored specifically to the user's prompt, using headings, tables, or bullet points only as appropriate to the request context."
        )

    if revision_instructions:
        task_description += (
            f"\nIMPORTANT - this is a REVISION pass. A prior draft was "
            f"reviewed and found insufficient. Address these specific "
            f"issues before finalizing:\n{revision_instructions}\n"
        )

    synthesis_task = Task(
        description=task_description,
        expected_output=task_expected_output,
        agent=manager,
    )

    crew = Crew(
        agents=[market_agent, risk_agent, rag_agent, sql_agent],
        tasks=[synthesis_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew


def _select_specialist_agent(
    query: str, available_documents: list[str], detected_symbols: list[str]
) -> str:
    if _is_database_query(query):
        return "sql_agent"
    if available_documents:
        return "rag_agent"
    if detected_symbols:
        return "market_agent"
    return "risk_agent"


def run_finance_crew(query: str, revision_instructions: str = "") -> str:
    with observe_span(
        "crew_execution",
        input_data={"query": query, "revision_instructions": revision_instructions},
        metadata={"provider": "crewai", "workflow": "finance_crew"},
        as_type="agent",
        provider="crewai",
    ) as span:
        if _is_document_query(query):
            result = _run_google_document_answer(query)
            if span is not None:
                span.update(
                    output={"result": result},
                    metadata={
                        "provider": "google_ai_studio",
                        "workflow": "rag_document_answer",
                        "model": os.getenv("GOOGLE_RAG_MODEL", "gemini-2.0-flash"),
                    },
                )
            return result

        crew = build_finance_crew(query, revision_instructions)
        result = crew.kickoff()
        specialist_agent = _select_specialist_agent(
            query,
            rag_service.list_documents(),
            extract_tickers(query),
        )
        if span is not None:
            span.update(
                output={"result": str(result)},
                metadata={
                    "provider": "crewai",
                    "workflow": "finance_crew",
                    "used_agents": ["manager", specialist_agent, "critic"],
                    "specialist_agent": specialist_agent,
                },
            )
        return str(result)


def crew_node(state: GraphState) -> GraphState:
    revision_instructions = state.get("revision_instructions", "")
    logger.info(
        "Running Crew_Node (revise_count=%s, revision_instructions=%s)",
        state.get("revise_count", 0),
        bool(revision_instructions),
    )
    draft = run_finance_crew(
        state["query"], revision_instructions=revision_instructions
    )
    return {**state, "draft_answer": draft}

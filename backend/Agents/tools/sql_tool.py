from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from Services.SQL_Service import run_readonly_query


class SQLQueryInput(BaseModel):
    query: str = Field(
        ...,
        description=(
            "A single, read-only SQL SELECT statement to run against the "
            "currently uploaded database. The schema is provided in your "
            "task context."
        ),
    )


class SQLQueryTool(BaseTool):
    name: str = "sql_query"
    description: str = (
        "Executes a read-only SQL SELECT query against the currently "
        "uploaded PostgreSQL database and returns the results. Only SELECT "
        "statements are permitted - any write or schema-modifying statement "
        "is rejected at multiple levels (this tool, the database "
        "connection, and the database role's own permissions), so it is "
        "always safe to call. The current schema (tables and columns) is "
        "provided in your task description - write your SQL against that "
        "exact schema."
    )
    args_schema: type[BaseModel] = SQLQueryInput

    def _run(self, query: str) -> str:
        return run_readonly_query(query)

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(
        ..., description="The analyst's financial query in natural language."
    )
    conversation_id: str | None = Field(
        None, description="Conversation to save this exchange into."
    )


class QueryResponse(BaseModel):
    status: str = Field(..., description="'completed' | 'blocked' | 'escalated'")
    final_response: str
    message: str | None = None
    confidence: float | None = None
    route: str | None = None
    # detected_intents: Optional[List[str]] = None
    # critic_issues: Optional[List[str]] = None
    # revise_count: Optional[int] = None


class IngestResponse(BaseModel):
    filename: str
    chunks_ingested: int
    total_documents: int
    message: str


class RetrieveRequest(BaseModel):
    query: str = Field(..., description="Query to search uploaded documents for.")
    top_k: int = Field(3, ge=1, le=10)


class RetrievalPassage(BaseModel):
    source: str
    text: str
    score: float


class RetrieveResponse(BaseModel):
    query: str
    results: list[RetrievalPassage]


class DocumentListResponse(BaseModel):
    documents: list[str]


class SQLIngestResponse(BaseModel):
    tables: list[str]
    message: str


class SchemaResponse(BaseModel):
    tables: list[str]
    schema_description: str


class RegisterRequest(BaseModel):
    name: str = Field(..., description="Full name of the user")
    email: str = Field(..., description="Real email address of the user")
    password: str = Field(..., description="Account password")


class RegisterResponse(BaseModel):
    message: str
    email: str
    requires_verification: bool = True


class UpdateProfileRequest(BaseModel):
    name: str | None = None
    old_password: str | None = None
    new_password: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    username: str
    email: str | None = None


class ConversationSummary(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


class ConversationListResponse(BaseModel):
    conversations: list[ConversationSummary]


class MessageItem(BaseModel):
    role: str
    content: str
    created_at: str


class MessagesResponse(BaseModel):
    messages: list[MessageItem]

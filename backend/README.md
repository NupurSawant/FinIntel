# Finance Risk Intelligence API

The API is deployed as a Vercel Python function (`/api/index.py`). The React
app and API are built and served by Vercel.

## Vercel environment variables

Required: `GROQ_API_KEY`, `GROQ_MODEL` (default `llama-3.1-8b-instant`),
`GOOGLE_API_KEY`, `GOOGLE_EMBEDDING_MODEL` (default
`gemini-embedding-001`), `GOOGLE_VISION_MODEL` (default
`gemini-2.0-flash`), `DATABASE_URL` (Neon/PostgreSQL), `QDRANT_URL`, and
`QDRANT_API_KEY`.

Also configure `JWT_SECRET` and any enabled integration keys
(`TAVILY_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`). Never commit
values; use Vercel Project Settings or `vercel env`.

PostgreSQL/Neon is required for durable users, conversations, and SQL data.
Qdrant Cloud is required for document vectors. Uploaded files use ephemeral
`/tmp` storage and must not be treated as durable.

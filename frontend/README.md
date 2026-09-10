# Finance Risk Intelligence frontend

This React/Vite app is deployed with the FastAPI function to Vercel. The
repository is intentionally Vercel-only; configure the deployment in Vercel
and do not run a separate local backend.

## Environment variables

Set these in Vercel Project Settings: `GROQ_API_KEY`,
`GROQ_MODEL=llama-3.3-70b-versatile`, `GOOGLE_API_KEY`,
`GOOGLE_EMBEDDING_MODEL=models/text-embedding-004`,
`GOOGLE_VISION_MODEL=gemini-2.0-flash`, `DATABASE_URL`, `QDRANT_URL`,
`QDRANT_API_KEY`, and `JWT_SECRET`. Optional integrations are
`TAVILY_API_KEY`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_SECRET_KEY`.

Neon/PostgreSQL and Qdrant Cloud are required for durable state. Upload
processing may use ephemeral Vercel `/tmp` storage; uploaded files themselves
are not persisted on local disk.

# Finance Risk Intelligence frontend

This React/Vite app is deployed to Vercel and calls the FastAPI backend hosted
at `https://finintel-1afu.onrender.com`.

## Environment variables

Set this frontend variable in Vercel Project Settings:

```text
VITE_API_BASE_URL=https://finintel-1afu.onrender.com
```

Backend-only variables such as `GROQ_API_KEY`, `GOOGLE_API_KEY`,
`DATABASE_URL`, `QDRANT_API_KEY`, and `JWT_SECRET` must be configured in the
Render service, not exposed to the frontend.

Neon/PostgreSQL and Qdrant Cloud are required for durable state. Upload
processing may use ephemeral Vercel `/tmp` storage; uploaded files themselves
are not persisted on local disk.

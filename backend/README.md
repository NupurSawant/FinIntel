Run the API:

uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

Langfuse Cloud observability:

- Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY in your environment or .env.
- Every /query request now creates Langfuse observations for the HTTP request, router, graph execution, crew execution, critic review, and route decision.
- In Langfuse Cloud you will see:
  - input and output payloads
  - latency for each step
  - provider/model information (Ollama for the router, CrewAI/LangGraph for the workflow)
  - the selected execution path and the specialist agent used by the crew

QDrant API Key = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6MzA0MDA5MjgtZmYwNy00ZWI4LWIxOTEtMjA1OGY3MDc4NGY0In0.FvftdSNUyJD5R06B1om5Hak2ybS3gArF_z28wVZyByA

Cluster Endpoint = https://b9ad2bff-698a-4bf4-988f-30a63aaf6f43.eu-central-1-0.aws.cloud.qdrant.io

Cluster ID - b9ad2bff-698a-4bf4-988f-30a63aaf6f43


ollama run llama3.2
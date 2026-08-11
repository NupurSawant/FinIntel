import os

from Observability.langfuse_client import langfuse

print(os.getenv("LANGFUSE_PUBLIC_KEY"))
print(os.getenv("LANGFUSE_SECRET_KEY"))

print(langfuse.auth_check())

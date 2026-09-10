"""Shared provider configuration for every chat, agent, and router call.

The deployment uses Groq's OpenAI-compatible API for text generation.  Keeping
construction here ensures agents and the pre-router cannot accidentally use a
different provider or credentials.
"""

import os

from crewai import LLM as CrewLLM
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


class LLM:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    groq_base_url: str = "https://api.groq.com/openai/v1"

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", 0.70))
    MAX_REVISE_RETRIES: int = int(os.getenv("MAX_REVISE_RETRIES", 3))

    def get_llm(self, deployment_name: str | None = None) -> CrewLLM:
        return CrewLLM(
            model=f"groq/{deployment_name or self.groq_model}",
            api_key=self.groq_api_key,
            base_url=self.groq_base_url,
        )

    def get_langchain_llm(self, deployment_name: str | None = None) -> ChatOpenAI:
        return ChatOpenAI(
            model=deployment_name or self.groq_model,
            api_key=self.groq_api_key,
            base_url=self.groq_base_url,
            temperature=0,
        )


llm = LLM()

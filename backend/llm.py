import os

from crewai import LLM as CrewLLM
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class LLM:
    azure_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")
    azure_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", 0.70))
    MAX_REVISE_RETRIES: int = int(os.getenv("MAX_REVISE_RETRIES", 3))

    def get_llm(self, deployment_name: str = None) -> CrewLLM:
        deployment = deployment_name or self.azure_deployment or "gpt-4o-mini"
        return CrewLLM(
            model=f"azure/{deployment}",
            api_key=self.azure_api_key,
            base_url=self.azure_endpoint,
            api_version=self.azure_api_version,
        )

    def get_langchain_llm(self, deployment_name: str = None) -> AzureChatOpenAI:
        deployment = deployment_name or self.azure_deployment or "gpt-4o-mini"
        return AzureChatOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.azure_api_key,
            azure_deployment=deployment,
            api_version=self.azure_api_version,
            temperature=0,
        )


llm = LLM()

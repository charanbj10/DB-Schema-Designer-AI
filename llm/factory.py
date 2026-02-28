import os
from dotenv import load_dotenv
from .openai_strategy import OpenAIStrategy
from .ollama_strategy import OllamaStrategy

load_dotenv()

def get_llm_strategy():
    provider = os.getenv("LLM_PROVIDER").lower()

    if provider == "openai":
        return OpenAIStrategy()

    elif provider == "ollama":
        return OllamaStrategy()

    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
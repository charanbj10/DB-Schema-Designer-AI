import os
from dotenv import load_dotenv
from .openai_strategy import OpenAIStrategy
from .ollama_strategy import OllamaStrategy
from .gemini_strategy import GeminiStrategy
from .groq_strategy import GroqStrategy

load_dotenv()

def get_llm_strategy():
    provider = os.getenv("LLM_PROVIDER").lower()

    if provider == "openai":
        return OpenAIStrategy()

    elif provider == "ollama":
        return OllamaStrategy()
    elif provider == "gemini":
        return GeminiStrategy()
    elif provider == "groq" :
        return GroqStrategy()

    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")
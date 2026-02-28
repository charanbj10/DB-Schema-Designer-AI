from ollama import Client
from .strategy import LLMStrategy

class OllamaStrategy(LLMStrategy):

    def __init__(self, model="llama3"):
        self.model = model
        self.client = Client()

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response["message"]["content"]
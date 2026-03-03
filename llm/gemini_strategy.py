import os
from google import genai
from .strategy import LLMStrategy


class GeminiStrategy(LLMStrategy):

    def __init__(self, model_name: str = "gemini-2.0-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        combined_prompt = f"""
            SYSTEM:
            {system_prompt}

            USER:
            {user_prompt}
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=combined_prompt
        )

        return response.text
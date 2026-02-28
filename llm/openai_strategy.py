from openai import OpenAI
from .strategy import LLMStrategy

class OpenAIStrategy(LLMStrategy):

    def __init__(self):
        self.client = OpenAI()

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )

        return response.choices[0].message.content
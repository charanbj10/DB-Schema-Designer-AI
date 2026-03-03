from .strategy import LLMStrategy
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class GroqStrategy(LLMStrategy):

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", "content": system_prompt,
                },
                {
                    "role": "user", "content": user_prompt,
                }
            ],
            temperature=0.1,
            max_tokens=4096,
        )

        return response.choices[0].message.content
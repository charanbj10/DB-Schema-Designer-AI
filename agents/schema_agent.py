class SchemaAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, prd: str, lld: str, feedback: str = None) -> str:
        system_prompt = "You are a senior database engineer."

        improvement_note = ""
        if feedback:
            improvement_note = f"""
Improve the schema based on these issues:
{feedback}
"""

        user_prompt = f"""
PRD:
{prd}

LLD:
{lld}

{improvement_note}

Generate:

1. MongoDB Schema (optimized)
2. PostgreSQL Schema (optimized)
3. Index strategy
4. Justifications

Be detailed and production-ready.
"""
        return self.llm.chat(system_prompt, user_prompt)
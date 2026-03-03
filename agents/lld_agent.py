class LLDAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, prd: str, hld: str) -> str:
        system_prompt = "You are a senior tech lead."

        user_prompt = f"""
PRD:
{prd}

HLD:
{hld}

Generate Low Level Design (LLD):

1. Data Models
2. Relationships
3. Transaction Boundaries
4. Access Patterns
5. Edge Cases

Respond in structured markdown.
"""
        return self.llm.chat(system_prompt, user_prompt)
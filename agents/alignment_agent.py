class AlignmentAgent:

    def __init__(self, llm):
        self.llm = llm

    def review(self, client_input: str, schema_output: str) -> str:
        system_prompt = "You are a senior architecture auditor."

        system_prompt = f"""
Compare the schema with the original client requirement.

Client Requirement:
{client_input}

Schema:
{schema_output}

Return STRICT JSON:

{{
  "alignment_score": integer (1-10),
  "confidence": integer (0-100),
  "issues": ["..."],
  "summary": "short explanation"
}}
"""
        return self.llm.chat(system_prompt, system_prompt)
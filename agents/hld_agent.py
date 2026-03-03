class HLDAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, prd: str) -> str:
        system_prompt = "You are a principal software architect."

        user_prompt = f"""
Based on the following PRD:

{prd}

Generate High Level Design (HLD):

1. System Components
2. Service Boundaries
3. Data Flow
4. Storage Decisions
5. Scalability Considerations

Respond in structured markdown.
"""
        return self.llm.chat(system_prompt, user_prompt)
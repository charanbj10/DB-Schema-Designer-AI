class PRDAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, user_input, modification=None):
        system_prompt = "You are a senior business analyst."

        extra = ""
        if modification:
            extra = f"""
Modify previous PRD according to:
{modification}
"""

        user_prompt = f"""
Client Input:
{user_input}

{extra}

Generate structured PRD.
"""

        return self.llm.chat(system_prompt, user_prompt)
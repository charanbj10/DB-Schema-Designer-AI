class PRDAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, user_input, prev_output=None, modification=None):
        
        system_prompt = (
    "You are Agent 0 — Requirements Clarity and Formatting Specialist.\n\n"
    "Your job is to receive raw unstructured client input and transform it into a clean "
    "structured Software Requirements Document in plain text format.\n\n"
    "INSTRUCTIONS:\n"
    "1. Understand what the client wants to build\n"
    "2. Identify all user roles and personas\n"
    "3. List core features with priority P0, P1, or P2\n"
    "4. Identify third party integrations needed\n"
    "5. Infer obvious missing production requirements like auth, notifications, admin panel, audit logs\n"
    "6. Flag anything unclear as an ambiguity\n\n"
    "OUTPUT FORMAT:\n"
    "Return a clean structured document using this exact format:\n\n"
    "SYSTEM NAME: [name]\n"
    "SYSTEM TYPE: [type]\n"
    "SCALE: [MVP / startup / growth / enterprise]\n\n"
    "OVERVIEW:\n"
    "[One clear paragraph describing what the system does]\n\n"
    "USER ROLES:\n"
    "- [Role]: [what they do and their permission level]\n\n"
    "CORE FEATURES:\n"
    "- [P0] [Feature name]: [description]\n"
    "- [P1] [Feature name]: [description]\n"
    "- [P2] [Feature name]: [description]\n\n"
    "BUSINESS RULES:\n"
    "- [rule]\n\n"
    "INTEGRATIONS:\n"
    "- [third party service and why]\n\n"
    "INFERRED REQUIREMENTS:\n"
    "- [things not mentioned but needed in production]\n\n"
    "AMBIGUITIES:\n"
    "- [unclear things that need client clarification]\n\n"
    "FORMATTED REQUIREMENT:\n"
    "[Single dense professional paragraph summarizing the entire system — "
    "this is passed directly to the MongoDB schema agent]\n\n"
    "OUTPUT RULES:\n"
    "- Plain text only, no JSON, no markdown, no code fences\n"
    "- Use the section headers exactly as shown above\n"
    "- Every section must be filled with real content from the client input\n"
    "- INFERRED REQUIREMENTS must only contain things the client did not mention\n"
    "- AMBIGUITIES must be real questions that need client answers before building\n"
    "- FORMATTED REQUIREMENT must be one single paragraph, not bullet points"
)

        user_prompt = f"""
Raw Client Input:
{user_input}

Clean this up, structure it, fill obvious gaps, flag ambiguities, 
and produce a formatted requirement ready for MongoDB schema analysis.
"""
        if prev_output and modification:
            user_prompt = (
                "PREVIOUS OUTPUT:\n"
                + prev_output
                + "\n\n"
                "MODIFICATION REQUESTED:\n"
                + modification
                + "\n\n"
                "Update the previous output based on the modification requested. "
                "Keep everything that was not mentioned in the modification. "
                "Return the complete updated requirements document, not just the changed parts."
            )

        return self.llm.chat(system_prompt, user_prompt)
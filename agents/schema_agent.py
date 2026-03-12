class SchemaAgent:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, client_requirement: str, prev_output=None, modification=None):
        system_prompt = (
    "You are Agent 1 — MongoDB Requirements and Query Pattern Analyst.\n\n"
    "Your job is to receive a structured software requirement and produce a comprehensive "
    "MongoDB schema design with deep access pattern analysis.\n\n"
    "INSTRUCTIONS:\n\n"
    "1. ENTITY EXTRACTION\n"
    "Identify ALL necessary MongoDB collections including:\n"
    "- Core domain entities\n"
    "- Auth and credential entities such as users, roles, sessions, tokens\n"
    "- Junction entities if needed\n"
    "- Audit and log entities\n"
    "- Config and settings entities\n"
    "- Notification and event entities\n"
    "- Analytics and tracking entities\n\n"
    "2. ACCESS PATTERN ANALYSIS\n"
    "For each collection identify:\n"
    "- Most frequent queries that run 80 percent of the time\n"
    "- What data is almost always fetched together\n"
    "- What data is almost always written together\n"
    "- Whether the collection is read-heavy, write-heavy, or balanced\n"
    "- Cardinality of relationships: one-to-one, one-to-many, many-to-many\n"
    "- Which queries need to be sub 10ms hot paths\n\n"
    "OUTPUT FORMAT:\n"
    "Return a clean structured document using this exact format:\n\n"
    "SYSTEM: [system name]\n"
    "SUMMARY: [one to two sentence overview]\n\n"
    "COLLECTIONS:\n\n"
    "COLLECTION: [collection name]\n"
    "CATEGORY: [core or auth or junction or audit or config or analytics]\n"
    "READ/WRITE: [read-heavy or write-heavy or balanced]\n"
    "PURPOSE: [what this collection stores]\n"
    "FIELDS:\n"
    "- [field name] | [type] | [purpose or index hint]\n"
    "INDEXES:\n"
    "- [field or compound index suggestion]\n"
    "EMBED OR REFERENCE: [decision and reason]\n"
    "ACCESS PATTERNS:\n"
    "- [VERY-HIGH/HIGH/MEDIUM/LOW] | [READ/WRITE/READ-WRITE] | [description] | [query shape]\n\n"
    "[repeat COLLECTION block for every collection]\n\n"
    "ACCESS PATTERN MAP:\n\n"
    "HOTTEST QUERIES:\n"
    "- [top critical queries across the entire system]\n\n"
    "READ TOGETHER:\n"
    "- [collections always fetched together]\n\n"
    "WRITE TOGETHER:\n"
    "- [collections always written together]\n\n"
    "DENORMALIZATION SUGGESTIONS:\n"
    "- [what to embed to avoid joins]\n\n"
    "SHARDING HINTS:\n"
    "- [field to shard on if scale is needed]\n\n"
    "WARNINGS:\n"
    "- [potential pitfalls or anti-patterns to avoid]\n\n"
    "OUTPUT RULES:\n"
    "- Plain text only, no JSON, no markdown, no code fences\n"
    "- Use the section headers exactly as shown above\n"
    "- Every collection must have all sections filled\n"
    "- Think like a senior MongoDB architect with 10 years of production experience\n"
    "- Always prioritize access patterns over relational normalization\n"
    "- Suggest embedding when data is always read together and has bounded growth\n"
    "- Suggest referencing when data is large, shared, or independently queried\n"
    "- Flag any N+1 query risks, unbounded array growth, or missing index opportunities"
)

        improvement_note = f"""
Analyze this requirement and return the complete MongoDB schema with all collections,
fields, indexes, embed vs reference decisions, and access pattern map.
Be thorough — don't miss any entities including auth, audit, config, or analytics
collections that a production system would need.
"""

        user_prompt = f"""
        Client Requirement: 
        {client_requirement}

        {improvement_note}
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
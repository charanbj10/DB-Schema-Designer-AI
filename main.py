from llm.factory import get_llm_strategy
import json
import re

llm = get_llm_strategy()

MAX_ITERATIONS = 3
ALIGNMENT_THRESHOLD = 8


# -------------------------------
# Utility
# -------------------------------
def extract_json(text):
    try:
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass
    return None


# -------------------------------
# AGENT 1: PRD (Business Analyst)
# -------------------------------
def prd_agent(user_input, modification=None):
    system = "You are a senior business analyst."

    extra = ""
    if modification:
        extra = f"""
Modify the previous PRD according to the user's change:
{modification}
"""

    prompt = f"""
Client Input:
{user_input}

{extra}

Generate a Product Requirement Document (PRD) including:

1. Use Case Description
2. Functional Requirements
3. Non-Functional Requirements
4. Entities
5. Constraints
6. Assumptions

Respond in structured markdown.
"""
    return llm.chat(system, prompt)


# -------------------------------
# AGENT 2: HLD
# -------------------------------
def hld_agent(prd):
    system = "You are a principal software architect."

    prompt = f"""
Based on the following PRD:

{prd}

Generate High Level Design (HLD):

1. System Components
2. Service Boundaries
3. Data Flow
4. Storage Decisions
5. Scalability Considerations
"""
    return llm.chat(system, prompt)


# -------------------------------
# AGENT 3: LLD
# -------------------------------
def lld_agent(prd, hld):
    system = "You are a senior tech lead."

    prompt = f"""
PRD:
{prd}

HLD:
{hld}

Generate Low Level Design:

1. Data Models
2. Relationships
3. Transaction Boundaries
4. Access Patterns
5. Edge Cases
"""
    return llm.chat(system, prompt)


# -------------------------------
# AGENT 4: Schema Generator
# -------------------------------
def schema_agent(prd, lld, feedback=None):
    system = "You are a senior database engineer."

    improvement_note = ""
    if feedback:
        improvement_note = f"""
Improve the schema based on these issues:
{feedback}
"""

    prompt = f"""
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
"""
    return llm.chat(system, prompt)


# -------------------------------
# AGENT 5: Alignment Review
# -------------------------------
def alignment_review_agent(client_input, schema_output):
    system = "You are a senior architecture auditor."

    prompt = f"""
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
    return llm.chat(system, prompt)


# -------------------------------
# MAIN
# -------------------------------
def main():

    print("\n🚀 AI Architecture Engine\n")
    client_input = input("Enter your product idea:\n\n")

    # -------- PRD CONFIRMATION LOOP --------
    while True:

        print("\n--- Generating PRD ---\n")
        prd = prd_agent(client_input)
        print(prd)

        user_action = input(
            "\nType CONFIRM to proceed OR type modifications:\n\n"
        )

        if user_action.strip().lower() == "confirm":
            break
        else:
            print("\n🔁 Updating PRD...\n")
            prd = prd_agent(client_input, user_action)

    # -------- HLD --------
    print("\n--- Generating HLD ---\n")
    hld = hld_agent(prd)
    print(hld)

    # -------- LLD --------
    print("\n--- Generating LLD ---\n")
    lld = lld_agent(prd, hld)
    print(lld)

    # -------- ITERATIVE SCHEMA GENERATION --------
    feedback = None

    for attempt in range(1, MAX_ITERATIONS + 1):

        print(f"\n--- Schema Attempt {attempt} ---\n")
        schema = schema_agent(prd, lld, feedback)
        print(schema)

        print("\n--- Alignment Review ---\n")
        review = alignment_review_agent(client_input, schema)
        print(review)

        parsed = extract_json(review)

        if not parsed:
            print("\n⚠ JSON parsing failed. Stopping.")
            break

        score = parsed.get("alignment_score", 0)
        confidence = parsed.get("confidence", 0)
        issues = parsed.get("issues", [])

        print(f"\nAlignment Score: {score}/10")
        print(f"Confidence: {confidence}%")

        if score >= ALIGNMENT_THRESHOLD:
            print("\n✅ Schema sufficiently aligned.")
            break

        print("\n⚠ Misalignment detected. Improving...\n")
        feedback = "\n".join(issues)

    print("\n🎯 Process Completed.")


if __name__ == "__main__":
    main()
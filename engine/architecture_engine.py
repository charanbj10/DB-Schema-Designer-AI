from config import MAX_ITERATIONS, ALIGNMENT_THRESHOLD
from utils.json_utils import extract_json

class ArchitectureEngine:

    def __init__(self, prd, hld, lld, schema, alignment):
        self.prd_agent = prd
        self.hld_agent = hld
        self.lld_agent = lld
        self.schema_agent = schema
        self.alignment_agent = alignment

    def run(self, client_input):

       # -------------------------
        # PRD CONFIRMATION LOOP
        # -------------------------
        while True:

            print("\n--- Generating PRD ---\n")
            prd = self.prd_agent.generate(client_input)
            print(prd)

            user_action = input(
                "\nType CONFIRM to proceed OR type modifications:\n\n"
            ).strip().lower()

            if user_action == "confirm":
                break

            print("\n🔁 Updating PRD...\n")
            prd = self.prd_agent.generate(client_input, modification=user_action)

        hld = self.hld_agent.generate(prd)
        print("HLD : \n", hld)
        lld = self.lld_agent.generate(prd, hld)
        print("LLD : \n", lld)
        feedback = None

        for attempt in range(MAX_ITERATIONS):

            schema = self.schema_agent.generate(prd, lld, feedback)
            review = self.alignment_agent.review(client_input, schema)

            parsed = extract_json(review)

            if not parsed:
                break

            score = parsed.get("alignment_score", 0)
            issues = parsed.get("issues", [])

            if score >= ALIGNMENT_THRESHOLD:
                return schema

            feedback = "\n".join(issues)

        return schema
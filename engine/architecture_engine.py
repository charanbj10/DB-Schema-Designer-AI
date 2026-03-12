from engine.schema_executor import SchemaExecutor
from agents.prd_agent import PRDAgent
from agents.schema_agent import SchemaAgent
from agents.schema_creator_agent import SchemaCreatorAgent
from llm.factory import get_llm_strategy

llm = get_llm_strategy()

class ArchitectureEngine:

    def __init__(self, mongo_uri: str, db_name: str):
        self.schema_agent = SchemaAgent(llm)
        self.prd_agent = PRDAgent(llm)
        self.schema_creator = SchemaCreatorAgent(llm)
        self.executor = SchemaExecutor(mongo_uri, db_name)

    # def run(self, client_input):

    #    # -------------------------
    #     # PRD CONFIRMATION LOOP
    #     # -------------------------

    #     print("\n--- Formatting Requirement ---\n")
    #     client_requirement = self.prd_agent.generate(client_input)

    #     while True:
    #         print(client_requirement)

    #         user_action = input(
    #             "\nType CONFIRM to proceed OR type modifications:\n\n"
    #         ).strip().lower()

    #         if user_action == "confirm":
    #             break

    #         print("\n🔁 Updating Client Requirement...\n")
    #         client_requirement = self.prd_agent.generate(client_input, prev_output=client_requirement, modification=user_action)


    #     schema_pattern = self.schema_agent.generate(client_requirement)
    #     print("Schema Pattern Analized : \n\n")

    #     while True :
    #         print(schema_pattern)
    #         print("\n\n")

    #         schema = self.schema_creator.generate(schema_pattern)
    #         print("Schema Generated : \n\n")
    #         print(schema)
    #         print("\n\n")

    #         user_action = input(
    #             "\nType CONFIRM to proceed OR type modifications:\n\n"
    #         ).strip().lower()

    #         if user_action == "confirm":
    #             break
            
    #         print("\n🔁 Updating Schema Pattern...\n")
    #         schema_pattern = self.schema_agent.generate(client_requirement, prev_output=schema, modification=user_action)

    #     # for attempt in range(MAX_ITERATIONS):

    #         # schema = self.schema_agent.generate(prd, lld, feedback)
    #         # review = self.alignment_agent.review(client_input, schema)

    #         # parsed = extract_json(review)

    #         # if not parsed:
    #         #     break

    #         # score = parsed.get("alignment_score", 0)
    #         # issues = parsed.get("issues", [])

    #         # if score >= ALIGNMENT_THRESHOLD:
    #         #     return schema

    #         # feedback = "\n".join(issues)

    #     return schema
    
    def insert_to_mongodb(self, schema) -> dict:
        return self.executor.execute(schema)

    def formatReqAgent(self, user_input: str, prev_output = None, modification = None) :
        print("\n--- Formatting Requirement ---\n")
        client_requirement = self.prd_agent.generate(user_input, prev_output, modification)
        return client_requirement
    
    def generateSchema(self, formatted_requirement: str, prev_output = None, modification = None) :
        print("\n--- Analyzing Schema Pattern ---")

        schema_pattern = self.schema_agent.generate(formatted_requirement, prev_output, modification)

        print("\n Generating Schema :")
        schema = self.schema_creator.generate(schema_pattern)
        return schema
# from llm.factory import get_llm_strategy
# import os
# from agents.prd_agent import PRDAgent
# from agents.schema_agent import SchemaAgent
# from agents.schema_creator_agent import SchemaCreatorAgent

# from engine.architecture_engine import ArchitectureEngine


# def main():
#     llm = get_llm_strategy()

#     engine = ArchitectureEngine(
#         PRDAgent(llm),
#         SchemaAgent(llm),
#         SchemaCreatorAgent(llm),
#         mongo_uri = os.getenv("MONGO_URI"),
#         db_name = os.getenv("DB_NAME")
#     )

#     client_input = input("Enter your product idea:\n")
#     final_schema = engine.run(client_input)

#     print("\n🎯 Final Schema:\n")
#     print(final_schema)

#     confirm = input("\nInsert schema into MongoDB? (yes/no): ").strip().lower()
#     if confirm == "yes":
#         print("\n[Inserting into MongoDB...]\n")
#         results = engine.insert_to_mongodb(final_schema)
#         for collection, status in results.items():
#             print(f"  {collection}: {status}")
#         print("\nDone.")


# if __name__ == "__main__":
#     main()
import os
from engine.architecture_engine import ArchitectureEngine
from api.session.session_store import session_store
from dotenv import load_dotenv
load_dotenv()

engine = ArchitectureEngine(
    mongo_uri=os.getenv("MONGO_URI"),
    db_name=os.getenv("DB_NAME"),
)

def generate_schema() -> str:
    session_store.reset_schema()

    final_schema = engine.generateSchema(
        formatted_requirement=session_store.format_requirement
    )
    session_store.schema = final_schema
    return final_schema


def modify_schema(modification: str) -> str:
    final_schema = engine.generateSchema(
        formatted_requirement=session_store.format_requirement,
        prev_output=session_store.schema,
        modification=modification
    )

    session_store.schema = final_schema
    return final_schema


def confirm_schema() -> None:
    session_store.schema_confirmed = True


def insert_to_mongo() -> dict:
    return engine.insert_to_mongodb(
        schema=session_store.schema
    )
import os
from engine.architecture_engine import ArchitectureEngine
from api.session.session_store import session_store
from dotenv import load_dotenv
load_dotenv()

engine = ArchitectureEngine(
    mongo_uri=os.getenv("MONGO_URI"),
    db_name=os.getenv("DB_NAME"),
)

def get_formatted_requirement(user_input: str) -> str:
    session_store.reset_requirement()
    session_store.reset_schema()
    session_store.raw_input = user_input

    output = engine.formatReqAgent(user_input)

    session_store.format_requirement = output
    return output


def modify_requirement(modification: str) -> str:
    updated = engine.formatReqAgent(
        user_input=session_store.raw_input,
        prev_output=session_store.format_requirement,
        modification=modification
    )
    session_store.format_requirement = updated
    return updated


def confirm_requirement() -> None:
    session_store.req_confirmed = True
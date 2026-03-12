# mcp/tools/create_tool.py

from datetime import datetime
from mcp.schema_reader import SchemaReader
from mcp.query_parser import parse_fields_block


def create_tool(db, parsed: dict) -> dict:
    collection = parsed["collection"]
    fields     = parsed.get("fields", {})

    fields["is_deleted"] = False
    fields["deleted_at"] = None
    fields["created_at"] = datetime.utcnow()
    fields["updated_at"] = datetime.utcnow()

    result = db[collection].insert_one(fields)

    return {
        "operation":    "CREATE",
        "collection":   collection,
        "inserted_id":  str(result.inserted_id),
        "status":       "created"
    }
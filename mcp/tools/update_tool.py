# mcp/tools/update_tool.py

from datetime import datetime
from mcp.query_parser import parse_filter, parse_fields_block


def update_tool(db, parsed: dict) -> dict:
    collection    = parsed["collection"]
    filter_str    = parsed.get("filter", "none")
    update_fields = parsed.get("update_fields", {})

    mongo_filter = parse_filter(filter_str)
    mongo_filter["is_deleted"] = {"$ne": True}

    update_fields["updated_at"] = datetime.utcnow()

    result = db[collection].update_many(
        mongo_filter,
        {"$set": update_fields}
    )

    return {
        "operation":     "UPDATE",
        "collection":    collection,
        "filter":        mongo_filter,
        "matched":       result.matched_count,
        "modified":      result.modified_count,
        "status":        "updated"
    }
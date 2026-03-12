# mcp/tools/delete_tool.py

from datetime import datetime
from mcp.query_parser import parse_filter


def delete_tool(db, parsed: dict) -> dict:
    collection  = parsed["collection"]
    filter_str  = parsed.get("filter", "none")
    soft_delete = parsed.get("soft_delete", "yes").lower() == "yes"

    mongo_filter = parse_filter(filter_str)

    if soft_delete:
        result = db[collection].update_many(
            mongo_filter,
            {"$set": {
                "is_deleted": True,
                "deleted_at": datetime.utcnow()
            }}
        )
        return {
            "operation":  "DELETE",
            "type":       "soft",
            "collection": collection,
            "filter":     mongo_filter,
            "modified":   result.modified_count,
            "status":     "soft deleted"
        }

    result = db[collection].delete_many(mongo_filter)
    return {
        "operation":  "DELETE",
        "type":       "hard",
        "collection": collection,
        "filter":     mongo_filter,
        "deleted":    result.deleted_count,
        "status":     "hard deleted"
    }